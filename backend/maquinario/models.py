from django.db import models
from fazendas.models import Fazenda


class Maquinario(models.Model):
    fazenda       = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='maquinarios')
    nome          = models.CharField(max_length=100)
    serialNumber  = models.CharField(max_length=100, unique=True)
    tipo          = models.CharField(max_length=50)
    possui_telemetria = models.BooleanField(default=False)

  
    # Horímetro atual da máquina (horas totais acumuladas no hodômetro)
    horimetro_atual = models.FloatField(
        default=0,
        help_text='Horas totais acumuladas no horímetro da máquina.'
    )
    # Capacidade do tanque em litros — usado para calcular % consumida por uso
    capacidade_tanque = models.FloatField(
        null=True, blank=True,
        help_text='Capacidade total do tanque em litros (opcional).'
    )

    def __str__(self):
        return f'{self.nome} ({self.fazenda.nome})'


class Manutenção(models.Model):
    class Tipo(models.TextChoices):
        Preventiva = 'PREVENTIVA', 'Preventiva'
        Corretiva  = 'CORRETIVA',  'Corretiva'

    class Status(models.TextChoices):
        Programada   = 'PROGRAMADA',   'Programada'
        EmAndamento  = 'EM_ANDAMENTO', 'Em andamento'
        Realizada    = 'REALIZADA',    'Realizada'

    maquinario  = models.ForeignKey(Maquinario, on_delete=models.CASCADE, related_name='manutencoes')
    tipo        = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.Preventiva)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.Programada)
    descricao   = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim    = models.DateTimeField(null=True, blank=True)
    custo       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    responsavel = models.CharField(max_length=100, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    criado_em   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.maquinario.nome} ({self.get_status_display()})'


class Telemetria(models.Model):
    class Status(models.TextChoices):
        Manual     = 'MANUAL',     'Manual'
        Automatico = 'AUTOMATICO', 'Automático'

    maquinario   = models.ForeignKey(Maquinario, on_delete=models.CASCADE, related_name='telemetrias')
    ip           = models.GenericIPAddressField(null=True, blank=True)
    status       = models.CharField(max_length=20, choices=Status.choices, default=Status.Manual)
    motor_ligado = models.BooleanField(default=False)
    data_hora    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Telemetria {self.maquinario.nome} - Motor: {"Ligado" if self.motor_ligado else "Desligado"}'


class Atividade(models.Model):
    maquinario = models.ForeignKey(Maquinario, on_delete=models.CASCADE, related_name='atividades')
    descricao  = models.CharField(max_length=255)
    origem     = models.CharField(max_length=20, choices=[
        ('manual',     'Manual'),
        ('automatica', 'Automática'),
    ])
    data_inicio = models.DateTimeField()
    data_fim    = models.DateTimeField(null=True, blank=True)

    
    # Horímetro registrado pelo operador antes e depois do uso
    horimetro_inicio = models.FloatField(
        null=True, blank=True,
        help_text='Leitura do horímetro no início da atividade (horas).'
    )
    horimetro_fim = models.FloatField(
        null=True, blank=True,
        help_text='Leitura do horímetro ao fim da atividade (horas).'
    )
    # Combustível consumido neste uso específico
    combustivel_litros = models.FloatField(
        null=True, blank=True,
        help_text='Litros de combustível consumidos nesta atividade.'
    )
    # Problemas reportados pelo operador
    problema_reportado = models.TextField(
        null=True, blank=True,
        help_text='Falha ou problema observado pelo operador durante o uso.'
    )

    @property
    def horas_trabalhadas(self):
        """Calcula horas trabalhadas a partir dos horímetros, se informados."""
        if self.horimetro_inicio is not None and self.horimetro_fim is not None:
            return round(self.horimetro_fim - self.horimetro_inicio, 2)
        return None

    def save(self, *args, **kwargs):
        """
        Ao finalizar uma atividade (horimetro_fim preenchido),
        atualiza automaticamente o horímetro atual da máquina.
        """
        super().save(*args, **kwargs)
        if self.horimetro_fim is not None:
            maq = self.maquinario
            if self.horimetro_fim > maq.horimetro_atual:
                maq.horimetro_atual = self.horimetro_fim
                maq.save(update_fields=['horimetro_atual'])

    def __str__(self):
        return f'{self.maquinario.nome} - {self.descricao}'