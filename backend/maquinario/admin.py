from django.contrib import admin
from .models import Maquinario, Manutenção, Telemetria, Atividade


@admin.register(Maquinario)
class MaquinarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'serialNumber', 'fazenda', 'possui_telemetria')
    list_filter = ('tipo', 'possui_telemetria', 'fazenda')
    search_fields = ('nome', 'serialNumber', 'tipo')


@admin.register(Manutenção)
class ManutencoAdmin(admin.ModelAdmin):
    list_display = ('maquinario', 'tipo', 'status', 'data_inicio', 'responsavel', 'custo')
    list_filter = ('tipo', 'status', 'data_inicio')
    search_fields = ('maquinario__nome', 'descricao', 'responsavel')
    readonly_fields = ('criado_em',)


@admin.register(Telemetria)
class TelemetriaAdmin(admin.ModelAdmin):
    list_display = ('maquinario', 'status', 'motor_ligado', 'ip', 'data_hora')
    list_filter = ('status', 'motor_ligado', 'data_hora')
    search_fields = ('maquinario__nome', 'ip')
    readonly_fields = ('data_hora',)


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('maquinario', 'descricao', 'origem', 'data_inicio', 'data_fim')
    list_filter = ('origem', 'data_inicio')
    search_fields = ('maquinario__nome', 'descricao')
