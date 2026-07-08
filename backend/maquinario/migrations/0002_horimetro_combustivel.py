from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maquinario', '0001_initial'),
    ]

    operations = [
        # Campos novos em Maquinario
        migrations.AddField(
            model_name='maquinario',
            name='horimetro_atual',
            field=models.FloatField(default=0, help_text='Horas totais acumuladas no horímetro da máquina.'),
        ),
        migrations.AddField(
            model_name='maquinario',
            name='capacidade_tanque',
            field=models.FloatField(blank=True, null=True, help_text='Capacidade total do tanque em litros.'),
        ),

        # Campos novos em Atividade
        migrations.AddField(
            model_name='atividade',
            name='horimetro_inicio',
            field=models.FloatField(blank=True, null=True, help_text='Leitura do horímetro no início da atividade.'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='horimetro_fim',
            field=models.FloatField(blank=True, null=True, help_text='Leitura do horímetro ao fim da atividade.'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='combustivel_litros',
            field=models.FloatField(blank=True, null=True, help_text='Litros de combustível consumidos nesta atividade.'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='problema_reportado',
            field=models.TextField(blank=True, null=True, help_text='Falha ou problema observado pelo operador.'),
        ),
    ]