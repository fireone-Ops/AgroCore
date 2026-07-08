import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fazendas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fazenda', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='itens',
                    to='fazendas.fazenda',
                )),
                ('nome', models.CharField(max_length=255)),
                ('tipo', models.CharField(
                    choices=[
                        ('SEMENTES', 'Sementes'),
                        ('GRÃOS', 'Grãos'),
                        ('COMBUSTIVEIS', 'Combustíveis'),
                        ('FERTILIZANTES', 'Fertilizantes'),
                        ('PESTICIDAS', 'Pesticidas'),
                    ],
                    default='SEMENTES',
                    max_length=50,
                )),
                ('unidade', models.CharField(max_length=50)),
                ('estoque_minimo', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='movimentacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(
                    choices=[('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')],
                    default='ENTRADA',
                    max_length=20,
                )),
                ('quantidade', models.FloatField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
                ('item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='movimentacoes',
                    to='estoque.item',
                )),
            ],
        ),
        migrations.CreateModel(
            name='Armazenamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(max_length=100)),
                ('capacidade', models.FloatField()),
                ('item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='armazenamentos',
                    to='estoque.item',
                )),
            ],
        ),
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.CharField(
                    choices=[
                        ('DIARIO', 'Diário'),
                        ('SEMANAL', 'Semanal'),
                        ('MENSAL', 'Mensal'),
                        ('CUSTOMIZADO', 'Customizado'),
                    ],
                    default='MENSAL',
                    max_length=20,
                )),
                ('data_inicio', models.DateTimeField()),
                ('data_fim', models.DateTimeField()),
                ('quantidade_consumida', models.FloatField(default=0)),
                ('quantidade_adicionada', models.FloatField(default=0)),
                ('saldo_inicial', models.FloatField(default=0)),
                ('saldo_final', models.FloatField(default=0)),
                ('data_geracao', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='relatorios',
                    to='estoque.item',
                )),
            ],
        ),
    ]