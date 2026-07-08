from django.db import migrations, models
 
 
class Migration(migrations.Migration):
 
    initial = True
 
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
 
    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Campo correto desde o início — db_column='senha_hash'
                ('password', models.TextField(db_column='senha_hash')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('perfil', models.CharField(
                    choices=[
                        ('produtor', 'Produtor'),
                        ('agronomo', 'Agrônomo'),
                        ('gerente', 'Gerente'),
                        ('operador', 'Operador'),
                    ],
                    default='produtor',
                    max_length=20,
                )),
                ('aprovado',   models.BooleanField(default=False)),
                ('bloqueado',  models.BooleanField(default=False)),
                ('tentativas', models.IntegerField(default=0)),
                ('is_active',  models.BooleanField(default=True)),
                ('is_staff',   models.BooleanField(default=False)),
                ('criado_em',     models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(
                    blank=True,
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.group',
                    verbose_name='groups',
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.permission',
                    verbose_name='user permissions',
                )),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'db_table': 'usuarios',
            },
        ),
    ]
 