from django.contrib import admin
from .models import TipoPraga, DadosClimaticos, DeteccaoPraga, Alerta, Dashboard


@admin.register(TipoPraga)
class TipoPragaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'severidade_max', 'criado_em')
    search_fields = ('nome', 'descricao')
    list_filter = ('severidade_max', 'criado_em')


@admin.register(DadosClimaticos)
class DadosClimaticosAdmin(admin.ModelAdmin):
    list_display = ('fazenda', 'data', 'fonte', 'temperatura_min', 'temperatura_max', 'umidade')
    list_filter = ('fonte', 'data', 'fazenda')
    search_fields = ('fazenda__nome', 'condicao')
    readonly_fields = ('criado_em',)


@admin.register(DeteccaoPraga)
class DeteccaoPragaAdmin(admin.ModelAdmin):
    list_display = ('tipo_praga', 'fazenda', 'severidade', 'area_afetada_percentual', 'data_deteccao', 'tratamento_realizado')
    list_filter = ('severidade', 'tratamento_realizado', 'data_deteccao', 'tipo_praga')
    search_fields = ('tipo_praga__nome', 'fazenda__nome', 'descricao')
    readonly_fields = ('data_deteccao', 'data_atualizacao')


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'severidade', 'status', 'fazenda', 'criado_em', 'notificado')
    list_filter = ('tipo', 'severidade', 'status', 'notificado', 'criado_em')
    search_fields = ('titulo', 'descricao', 'fazenda__nome')
    readonly_fields = ('criado_em', 'atualizado_em', 'data_notificacao', 'data_resolucao')
    filter_horizontal = ('usuarios_notificados',)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('fazenda', 'total_alertas', 'alertas_criticos', 'alertas_altos', 'atualizado_em')
    list_filter = ('atualizado_em',)
    search_fields = ('fazenda__nome',)
    readonly_fields = (
        'fazenda', 'total_alertas', 'alertas_criticos', 'alertas_altos',
        'alertas_medios', 'alertas_baixos', 'alertas_nao_lidos', 'atualizado_em'
    )
