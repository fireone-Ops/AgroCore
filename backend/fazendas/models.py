from django.db import models
from accounts.models import Usuario


class Fazenda(models.Model):
    class TipoSolo(models.TextChoices):
        ARGISSOLOS = 'argissolos', 'Argissolos'
        CAMBISSOLOS = 'cambissolos', 'Cambissolos'
        CHERMOSOLOS = 'chermosolos', 'Chermosolos'
        ESPODOSSOLOS = 'espodossolos', 'Espodossolos'
        GLEISSOLOS = 'gleissolos', 'Gleissolos'
        LATOSSOLOS = 'latossolos', 'Latossolos'
        LUVISSOLOS = 'luvissolos', 'Luvissolos'
        NEOSSOLOS = 'neossolos', 'Neossolos'
        NITOSSOLOS = 'nitossolos', 'Nitossolos'
        ORGANOSSOLOS = 'organossolos', 'Organossolos'
        PLANOSSOLOS = 'planossolos', 'Planossolos'
        PLINTOSSOLOS = 'plintossolos', 'Plintossolos'
        VERTISSOLOS = 'vertissolos', 'Vertissolos'

    nome = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    area_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_solo = models.CharField(max_length=20, choices=TipoSolo.choices, blank=True, null=True)
    produtor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='fazendas')
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'fazendas'
        verbose_name = 'Fazenda'
        verbose_name_plural = 'Fazendas'
    def __str__(self):
        return self.nome


class AcessoFazenda(models.Model):
    class PerfilAcesso(models.TextChoices):
        PRODUTOR = 'produtor', 'Produtor'
        AGRONOMO = 'agronomo', 'Agrônomo'
        GERENTE = 'gerente', 'Gerente'
        OPERADOR = 'operador', 'Operador'

    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='acessos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='acessos_fazenda')
    perfil = models.CharField(max_length=20, choices=PerfilAcesso.choices, default=PerfilAcesso.OPERADOR)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'acessos_fazenda'
        unique_together = ('fazenda', 'usuario')

    def __str__(self):
        return f'{self.usuario} -> {self.fazenda} ({self.perfil})'