from django.contrib import admin
from .models import Log, RelatorioAuditoria


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'modulo', 'fazenda', 'descricao', 'criado_em')
    list_filter = ('acao', 'modulo', 'criado_em', 'fazenda')
    search_fields = ('usuario__nome', 'descricao', 'nome_objeto', 'fazenda__nome')
    readonly_fields = (
        'usuario', 'acao', 'modulo', 'descricao', 'nome_objeto',
        'dados_anteriores', 'dados_novos', 'campos_alterados',
        'ip_address', 'user_agent', 'endpoint', 'criado_em'
    )
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('usuario', 'fazenda', 'acao', 'modulo', 'descricao')
        }),
        ('Objeto Afetado', {
            'fields': ('content_type', 'object_id', 'nome_objeto')
        }),
        ('Mudanças', {
            'fields': ('dados_anteriores', 'dados_novos', 'campos_alterados'),
            'classes': ('collapse',)
        }),
        ('Informações Técnicas', {
            'fields': ('ip_address', 'user_agent', 'endpoint', 'criado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(RelatorioAuditoria)
class RelatorioAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'status', 'criado_por', 'total_registros', 'criado_em')
    list_filter = ('tipo', 'status', 'criado_em')
    search_fields = ('titulo', 'criado_por__nome')
    readonly_fields = (
        'criado_por', 'total_registros', 'arquivo',
        'criado_em', 'gerado_em', 'atualizado_em'
    )
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('titulo', 'tipo', 'status', 'criado_por')
        }),
        ('Filtros', {
            'fields': ('usuario_filtro', 'fazenda_filtro', 'data_inicio', 'data_fim')
        }),
        ('Resultado', {
            'fields': ('total_registros', 'formato', 'arquivo'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'gerado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

