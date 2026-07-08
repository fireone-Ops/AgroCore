from django.contrib import admin
from .models import Item, movimentacao, Armazenamento, Relatorio


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'unidade', 'estoque_minimo')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo')


@admin.register(movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('item', 'tipo', 'quantidade', 'data', 'descricao')
    list_filter = ('tipo', 'data')
    search_fields = ('item__nome', 'descricao')
    readonly_fields = ('data',)


@admin.register(Armazenamento)
class ArmazenamentoAdmin(admin.ModelAdmin):
    list_display = ('item', 'local', 'capacidade')
    list_filter = ('local',)
    search_fields = ('item__nome', 'local')


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('item', 'periodo', 'data_inicio', 'data_fim', 'saldo_final')
    list_filter = ('periodo', 'data_inicio')
    search_fields = ('item__nome',)
    readonly_fields = ('data_geracao',)
