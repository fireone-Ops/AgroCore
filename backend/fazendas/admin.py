from django.contrib import admin
from .models import Fazenda


@admin.register(Fazenda)
class FazendaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'produtor', 'localizacao', 'cidade', 'estado', 'area_total', 'ativa')
    list_filter = ('ativa', 'tipo_solo', 'estado', 'criado_em')
    search_fields = ('nome', 'localizacao', 'cidade', 'produtor__nome', 'produtor__email')
    readonly_fields = ('criado_em', 'atualizado_em')
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('nome', 'produtor', 'ativa')
        }),
        ('Localização', {
            'fields': ('localizacao', 'cidade', 'estado')
        }),
        ('Características', {
            'fields': ('area_total', 'tipo_solo')
        }),
        ('Timestamps', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
