from django.db import models
from accounts.models import Usuario
from fazendas.models import Fazenda


class Solicitacao(models.Model):
    class Tipo(models.TextChoices):
        MANUTENCAO = 'MANUTENCAO', 'Manutenção'
        COMPRA = 'COMPRA', 'Compra'
        SERVICO = 'SERVICO', 'Serviço'
        OUTRA = 'OUTRA', 'Outra'

    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        APROVADA = 'APROVADA', 'Aprovada'
        REJEITADA = 'REJEITADA', 'Rejeitada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        CONCLUIDA = 'CONCLUIDA', 'Concluída'

    # Campos principais
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OUTRA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    
    # Relacionamentos
    fazenda = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name='solicitacoes')
    solicitante = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='solicitacoes_feitas')
    aprovador = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='solicitacoes_aprovadas'
    )
    
    # Detalhes da solicitação
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    custo_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Campos de controle
    requer_aprovacao = models.BooleanField(
        default=True,
        help_text='Se custo > R$ 5.000, requer aprovação'
    )
    motivo_rejeicao = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'solicitacoes'
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.titulo} ({self.get_status_display()})'
    
    def salvar_com_verificacao(self):
        """Verifica se a solicitação requer aprovação baseado no custo"""
        if self.custo_estimado and self.custo_estimado > 5000:
            self.requer_aprovacao = True
        self.save()
