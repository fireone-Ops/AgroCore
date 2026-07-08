from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('aprovado', True)
        return self.create_user(email, nome, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    class Perfil(models.TextChoices):
        PRODUTOR = 'produtor', 'Produtor'
        AGRONOMO = 'agronomo', 'Agrônomo'
        GERENTE  = 'gerente',  'Gerente'
        OPERADOR = 'operador', 'Operador'

    nome          = models.CharField(max_length=150)
    email         = models.EmailField(unique=True)
    password      = models.TextField(db_column='senha_hash')
    perfil        = models.CharField(max_length=20, choices=Perfil.choices, default=Perfil.PRODUTOR)
    aprovado      = models.BooleanField(default=False)
    bloqueado     = models.BooleanField(default=False)
    tentativas    = models.IntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f'{self.nome} ({self.email})'