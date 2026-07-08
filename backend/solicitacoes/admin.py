from django.contrib import admin
from .models import Solicitacao


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'custo_estimado', 'solicitante', 'fazenda', 'criado_em')
    list_filter = ('status', 'tipo', 'requer_aprovacao', 'criado_em')
    search_fields = ('titulo', 'descricao', 'solicitante__nome')
    readonly_fields = ('criado_em', 'atualizado_em', 'data_aprovacao')
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('titulo', 'descricao', 'tipo', 'status')
        }),
        ('Aprovação', {
            'fields': ('requer_aprovacao', 'aprovador', 'motivo_rejeicao', 'data_aprovacao')
        }),
        ('Financeiro', {
            'fields': ('custo_estimado',)
        }),
        ('Relacionamentos', {
            'fields': ('fazenda', 'solicitante')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
