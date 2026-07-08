from django.db import models
from django.db.models import Sum


class Item(models.Model):
    class Tipo(models.TextChoices):
        Sementes      = 'SEMENTES',      'Sementes'
        Graos         = 'GRÃOS',         'Grãos'
        Combustiveis  = 'COMBUSTIVEIS',  'Combustíveis'
        Fertilizantes = 'FERTILIZANTES', 'Fertilizantes'
        Pesticidas    = 'PESTICIDAS',    'Pesticidas'

    fazenda = models.ForeignKey(
        'fazendas.Fazenda',
        on_delete=models.CASCADE,
        related_name='itens',
    )

    nome          = models.CharField(max_length=255)
    tipo          = models.CharField(max_length=50, choices=Tipo.choices, default=Tipo.Sementes)
    unidade       = models.CharField(max_length=50)
    estoque_minimo = models.FloatField(default=0)

    def __str__(self):
        return f'{self.nome} ({self.fazenda.nome})'


class movimentacao(models.Model):
    class Tipo(models.TextChoices):
        Entrada = 'ENTRADA', 'Entrada'
        Saida   = 'SAIDA',   'Saída'

    item      = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo      = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.Entrada)
    quantidade = models.FloatField()
    data      = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.item.nome} ({self.quantidade})'


def calcular_estoque(item):
    entradas = item.movimentacoes.filter(tipo='ENTRADA').aggregate(total=Sum('quantidade'))['total'] or 0
    saidas   = item.movimentacoes.filter(tipo='SAIDA').aggregate(total=Sum('quantidade'))['total'] or 0
    return entradas - saidas


class Armazenamento(models.Model):
    item       = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='armazenamentos')
    local      = models.CharField(max_length=100)
    capacidade = models.FloatField()

    def __str__(self):
        return f'{self.local} — {self.item.nome}'


class Relatorio(models.Model):
    class Periodo(models.TextChoices):
        Diario     = 'DIARIO',     'Diário'
        Semanal    = 'SEMANAL',    'Semanal'
        Mensal     = 'MENSAL',     'Mensal'
        Customizado = 'CUSTOMIZADO', 'Customizado'

    item                = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='relatorios')
    periodo             = models.CharField(max_length=20, choices=Periodo.choices, default=Periodo.Mensal)
    data_inicio         = models.DateTimeField()
    data_fim            = models.DateTimeField()
    quantidade_consumida = models.FloatField(default=0)
    quantidade_adicionada = models.FloatField(default=0)
    saldo_inicial       = models.FloatField(default=0)
    saldo_final         = models.FloatField(default=0)
    data_geracao        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relatório {self.item.nome} - {self.periodo} ({self.data_inicio:%d/%m/%Y} a {self.data_fim:%d/%m/%Y})'