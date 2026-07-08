from django.db import models
from django.utils import timezone
from accounts.models import Usuario
from fazendas.models import Fazenda
from culturas.models import Plantio


class TipoPraga(models.Model):
    """Catálogo de pragas conhecidas"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    severidade_max = models.CharField(max_length=50, choices=[
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ], default='MEDIA')
    culturas_afetadas = models.CharField(max_length=500, help_text='Culturas separadas por vírgula')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tipos_pragas'
        verbose_name = 'Tipo de Praga'
        verbose_name_plural = 'Tipos de Pragas'
    
    def __str__(self):
        return self.nome


class DadosClimaticos(models.Model):
    """Dados climáticos integrados de fontes externas"""
    class FonteDados(models.TextChoices):
        OPENWEATHER = 'openweather', 'OpenWeather API'
        IBGE = 'ibge', 'IBGE'
        INMET = 'inmet', 'INMET'
        MANUAL = 'manual', 'Entrada Manual'
    
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='dados_climaticos')
    data = models.DateTimeField()
    fonte = models.CharField(max_length=20, choices=FonteDados.choices)
    
    # Dados climáticos
    temperatura_min = models.FloatField(help_text='Temperatura mínima em °C')
    temperatura_max = models.FloatField(help_text='Temperatura máxima em °C')
    umidade = models.FloatField(help_text='Umidade do ar em %')
    precipitacao = models.FloatField(default=0, help_text='Precipitação em mm')
    velocidade_vento = models.FloatField(default=0, help_text='Velocidade do vento em km/h')
    
    # Condição climática
    condicao = models.CharField(max_length=100, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'dados_climaticos'
        verbose_name = 'Dado Climático'
        verbose_name_plural = 'Dados Climáticos'
        ordering = ['-data']
    
    def __str__(self):
        return f'{self.fazenda.nome} - {self.data.strftime("%d/%m/%Y %H:%M")}'


class DeteccaoPraga(models.Model):
    """Registro de detecção de pragas na fazenda/plantação"""
    class Severidade(models.TextChoices):
        BAIXA = 'BAIXA', 'Baixa'
        MEDIA = 'MEDIA', 'Média'
        ALTA = 'ALTA', 'Alta'
        CRITICA = 'CRITICA', 'Crítica'
    
    plantio = models.ForeignKey(Plantio, on_delete=models.CASCADE, related_name='deteccoes_praga', null=True, blank=True)
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='deteccoes_praga')
    tipo_praga = models.ForeignKey(TipoPraga, on_delete=models.PROTECT)
    
    severidade = models.CharField(max_length=20, choices=Severidade.choices, default=Severidade.MEDIA)
    area_afetada_percentual = models.FloatField(help_text='Percentual da área afetada')
    descricao = models.TextField()
    
    # Localização precisa se possível
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    data_deteccao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    # Observações
    recomendacoes = models.TextField(null=True, blank=True)
    tratamento_realizado = models.BooleanField(default=False)
    data_tratamento = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'deteccoes_pragas'
        verbose_name = 'Detecção de Praga'
        verbose_name_plural = 'Detecções de Pragas'
        ordering = ['-data_deteccao']
    
    def __str__(self):
        return f'{self.tipo_praga.nome} - {self.fazenda.nome} ({self.get_severidade_display()})'


class Alerta(models.Model):
    """Sistema de alertas do TerraCore"""
    class Tipo(models.TextChoices):
        PRAGA = 'PRAGA', 'Praga'
        CLIMA_ADVERSO = 'CLIMA_ADVERSO', 'Clima Adverso'
        PLANTIO_FORA_EPOCA = 'PLANTIO_FORA_EPOCA', 'Plantio Fora de Época'
        ESTOQUE_BAIXO = 'ESTOQUE_BAIXO', 'Estoque Baixo'
        MANUTENCAO_NECESSARIA = 'MANUTENCAO_NECESSARIA', 'Manutenção Necessária'
        OUTRO = 'OUTRO', 'Outro'
    
    class Severidade(models.TextChoices):
        BAIXA = 'BAIXA', 'Baixa'
        MEDIA = 'MEDIA', 'Média'
        ALTA = 'ALTA', 'Alta'
        CRITICA = 'CRITICA', 'Crítica'
    
    class Status(models.TextChoices):
        NOVO = 'NOVO', 'Novo'
        EM_ANALISE = 'EM_ANALISE', 'Em Análise'
        ACIONADO = 'ACIONADO', 'Acionado'
        RESOLVIDO = 'RESOLVIDO', 'Resolvido'
        DESCARTADO = 'DESCARTADO', 'Descartado'
    
    # Identificação
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    severidade = models.CharField(max_length=20, choices=Severidade.choices, default=Severidade.MEDIA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOVO)
    
    # Relacionamentos
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='alertas')
    plantio = models.ForeignKey(Plantio, on_delete=models.SET_NULL, null=True, blank=True)
    deteccao_praga = models.ForeignKey(DeteccaoPraga, on_delete=models.SET_NULL, null=True, blank=True)
    dados_climaticos = models.ForeignKey(DadosClimaticos, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Conteúdo
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    recomendacoes = models.TextField(null=True, blank=True)
    
    # Notificações
    notificado = models.BooleanField(default=False)
    data_notificacao = models.DateTimeField(null=True, blank=True)
    usuarios_notificados = models.ManyToManyField(Usuario, blank=True, related_name='alertas_recebidos')
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'alertas'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status', 'fazenda']),
            models.Index(fields=['severidade', 'criado_em']),
        ]
    
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.fazenda.nome}'
    
    def marcar_como_resolvido(self):
        self.status = self.Status.RESOLVIDO
        self.data_resolucao = timezone.now()
        self.save()
    
    def notificar_usuarios(self):
        """Marca alerta como notificado e registra timestamp"""
        self.notificado = True
        self.data_notificacao = timezone.now()
        self.save()


class Dashboard(models.Model):
    """Snapshot de alertas por fazenda para dashboard em tempo real"""
    fazenda = models.OneToOneField(Fazenda, on_delete=models.CASCADE, related_name='dashboard')
    
    total_alertas = models.IntegerField(default=0)
    alertas_criticos = models.IntegerField(default=0)
    alertas_altos = models.IntegerField(default=0)
    alertas_medios = models.IntegerField(default=0)
    alertas_baixos = models.IntegerField(default=0)
    
    alertas_nao_lidos = models.IntegerField(default=0)
    
    # Últimas detecções
    ultima_praga = models.ForeignKey(DeteccaoPraga, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    ultimo_dado_climatico = models.ForeignKey(DadosClimaticos, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard'
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
    
    def __str__(self):
        return f'Dashboard - {self.fazenda.nome}'
    
    def atualizar_contadores(self):
        """Atualiza contadores de alertas"""
        from django.db.models import Q
        
        alertas = Alerta.objects.filter(fazenda=self.fazenda, status__in=[
            Alerta.Status.NOVO,
            Alerta.Status.EM_ANALISE,
            Alerta.Status.ACIONADO
        ])
        
        self.total_alertas = alertas.count()
        self.alertas_criticos = alertas.filter(severidade=Alerta.Severidade.CRITICA).count()
        self.alertas_altos = alertas.filter(severidade=Alerta.Severidade.ALTA).count()
        self.alertas_medios = alertas.filter(severidade=Alerta.Severidade.MEDIA).count()
        self.alertas_baixos = alertas.filter(severidade=Alerta.Severidade.BAIXA).count()
        self.alertas_nao_lidos = alertas.filter(notificado=False).count()
        
        self.ultima_praga = DeteccaoPraga.objects.filter(fazenda=self.fazenda).first()
        self.ultimo_dado_climatico = DadosClimaticos.objects.filter(fazenda=self.fazenda).first()
        
        self.save()
