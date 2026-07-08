from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display  = ('email', 'nome', 'perfil', 'aprovado', 'bloqueado')
    search_fields = ('email', 'nome')
    ordering      = ('email',)

    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Dados',        {'fields': ('nome', 'perfil')}),
        ('Status',       {'fields': ('aprovado', 'bloqueado', 'tentativas', 'is_active', 'is_staff', 'is_superuser')}),
        ('Datas',        {'fields': ('last_login', 'criado_em', 'atualizado_em')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'perfil', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login', 'criado_em', 'atualizado_em')