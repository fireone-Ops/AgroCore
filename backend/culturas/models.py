from django.db import models
from accounts.models import Usuario
from fazendas.models import Fazenda

class Cultura(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    mes_inicio = models.IntegerField()
    mes_fim = models.IntegerField()
    
    class Meta:
        db_table = 'culturas'

    def __str__(self):
        return self.nome
        
class Plantio(models.Model):
    class Status(models.TextChoices):
        PLANEJADO = 'PLANEJADO', 'Planejado'
        EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em Andamento'
        PLANTADO = 'PLANTADO', 'Plantado'
        COLHIDO = 'COLHIDO', 'Colhido'
        PERDIDO = 'PERDIDO', 'Perdido'

    fazenda = models.ForeignKey(Fazenda, on_delete=models.PROTECT)
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    responsavel = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    data_plantio = models.DateField()
    area_plantada = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANEJADO)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'plantios'
    
    def __str__(self):
        return f'{self.cultura} - {self.fazenda}'

class Colheita(models.Model):
    plantio = models.ForeignKey(Plantio, on_delete=models.PROTECT, related_name='colheitas')
    responsavel = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='colheitas')
    data_colheita = models.DateField()
    area_colhida = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_kg = models.DecimalField(max_digits=12, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'colheitas'

    def __str__(self):
        return f'Colheita - {self.plantio}'
    
class Laudo(models.Model):

    class Tipo(models.TextChoices):
        SOLO = 'SOLO', 'Solo'
        PRAGA = 'PRAGA', 'Praga'
        RISCO = 'RISCO', 'Risco'
        GERAL = 'GERAL', 'Geral'

    fazenda = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name='laudos')
    plantio = models.ForeignKey(Plantio, on_delete=models.SET_NULL, null=True, blank=True, related_name='laudos')
    agronomo = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='laudos')
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    recomendacoes = models.TextField(blank=True, null=True)
#campo para informações do solo
    ph_solo = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    umidade_solo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#campo sobre pragas
    tipo_praga = models.CharField(max_length=100, blank=True, null=True)
    severidade_praga = models.CharField(max_length=50, blank=True, null=True)
    #campo para riscos
    tipo_risco = models.CharField(max_length=500, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'laudos'

    def __str__(self):
        return f'Laudo - {self.tipo} - {self.fazenda}'