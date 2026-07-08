from django.contrib import admin
from .models import Cultura, Plantio, Colheita, Laudo


@admin.register(Cultura)
class CulturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'mes_inicio', 'mes_fim')
    search_fields = ('nome', 'descricao')


@admin.register(Plantio)
class PlantioAdmin(admin.ModelAdmin):
    list_display = ('cultura', 'fazenda', 'status', 'data_plantio', 'area_plantada', 'responsavel')
    list_filter = ('status', 'data_plantio', 'cultura')
    search_fields = ('cultura__nome', 'fazenda__nome', 'responsavel__nome')
    readonly_fields = ('criado_em',)


@admin.register(Colheita)
class ColheitaAdmin(admin.ModelAdmin):
    list_display = ('plantio', 'data_colheita', 'area_colhida', 'quantidade_kg', 'responsavel')
    list_filter = ('data_colheita', 'plantio__cultura')
    search_fields = ('plantio__cultura__nome', 'responsavel__nome')
    readonly_fields = ('criado_em',)


@admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fazenda', 'agronomo', 'criado_em')
    list_filter = ('tipo', 'criado_em', 'fazenda')
    search_fields = ('titulo', 'descricao', 'agronomo__nome')
    readonly_fields = ('criado_em',)
