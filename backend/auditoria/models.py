from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import Usuario
from fazendas.models import Fazenda


class Log(models.Model):
    """Registro de auditoria de todas as ações do sistema"""
    class Acao(models.TextChoices):
        CRIADO = 'CRIADO', 'Criado'
        ATUALIZADO = 'ATUALIZADO', 'Atualizado'
        DELETADO = 'DELETADO', 'Deletado'
        ACESSADO = 'ACESSADO', 'Acessado'
        EXPORTADO = 'EXPORTADO', 'Exportado'
        APROVADO = 'APROVADO', 'Aprovado'
        REJEITADO = 'REJEITADO', 'Rejeitado'
        CANCELADO = 'CANCELADO', 'Cancelado'
        RESOLVIDO = 'RESOLVIDO', 'Resolvido'
        OUTRO = 'OUTRO', 'Outro'
    
    class ModuloAfetado(models.TextChoices):
        ACCOUNTS = 'ACCOUNTS', 'Contas'
        FAZENDAS = 'FAZENDAS', 'Fazendas'
        CULTURAS = 'CULTURAS', 'Culturas'
        ESTOQUE = 'ESTOQUE', 'Estoque'
        MAQUINARIO = 'MAQUINARIO', 'Maquinário'
        ALERTAS = 'ALERTAS', 'Alertas'
        SOLICITACOES = 'SOLICITACOES', 'Solicitações'
        ADMIN = 'ADMIN', 'Administração'
        OUTRO = 'OUTRO', 'Outro'
    
    # Usuário responsável
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='logs_auditoria')
    
    # Fazenda afetada
    fazenda = models.ForeignKey(Fazenda, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs_auditoria')
    
    # Ação e módulo
    acao = models.CharField(max_length=20, choices=Acao.choices)
    modulo = models.CharField(max_length=20, choices=ModuloAfetado.choices)
    
    # Descrição
    descricao = models.TextField()
    
    # Entidade afetada (usando Generic Foreign Key)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    objeto_afetado = GenericForeignKey('content_type', 'object_id')
    nome_objeto = models.CharField(max_length=255, blank=True, help_text='Nome do objeto afetado')
    
    # Detalhes das mudanças
    dados_anteriores = models.JSONField(null=True, blank=True, help_text='JSON com valores anteriores')
    dados_novos = models.JSONField(null=True, blank=True, help_text='JSON com valores novos')
    campos_alterados = models.JSONField(null=True, blank=True, help_text='Lista de campos alterados')
    
    # Informações técnicas
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    endpoint = models.CharField(max_length=500, blank=True)
    
    # Timestamp
    criado_em = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'logs'
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['usuario', 'criado_em']),
            models.Index(fields=['fazenda', 'criado_em']),
            models.Index(fields=['acao', 'modulo']),
        ]
    
    def __str__(self):
        return f'{self.get_acao_display()} - {self.usuario.nome} - {self.criado_em.strftime("%d/%m/%Y %H:%M:%S")}'
    
    @property
    def usuario_nome(self):
        return self.usuario.nome if self.usuario else 'Desconhecido'
    
    @property
    def fazenda_nome(self):
        return self.fazenda.nome if self.fazenda else 'N/A'


class RelatorioAuditoria(models.Model):
    """Relatórios de auditoria pré-gerados para exportação"""
    class TipoRelatorio(models.TextChoices):
        POR_USUARIO = 'POR_USUARIO', 'Por Usuário'
        POR_FAZENDA = 'POR_FAZENDA', 'Por Fazenda'
        POR_ACAO = 'POR_ACAO', 'Por Ação'
        POR_PERIODO = 'POR_PERIODO', 'Por Período'
        COMPLETO = 'COMPLETO', 'Completo'
    
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        GERANDO = 'GERANDO', 'Gerando'
        PRONTO = 'PRONTO', 'Pronto'
        ERRO = 'ERRO', 'Erro'
    
    # Identificação
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TipoRelatorio.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    
    # Criador
    criado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    
    # Filtros
    usuario_filtro = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='relatorios_sobre_mim'
    )
    fazenda_filtro = models.ForeignKey(
        Fazenda, on_delete=models.SET_NULL, null=True, blank=True
    )
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    
    # Dados
    total_registros = models.IntegerField(default=0)
    arquivo = models.FileField(upload_to='auditoria/relatorios/', null=True, blank=True)
    formato = models.CharField(max_length=10, choices=[
        ('CSV', 'CSV'),
        ('PDF', 'PDF'),
        ('XLSX', 'Excel'),
        ('JSON', 'JSON'),
    ], default='CSV')
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True)
    gerado_em = models.DateTimeField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'relatorios_auditoria'
        verbose_name = 'Relatório de Auditoria'
        verbose_name_plural = 'Relatórios de Auditoria'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f'{self.titulo} ({self.get_status_display()})'

