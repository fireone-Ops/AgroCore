from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/fazendas/', include('fazendas.urls')),
    path('api/culturas/', include('culturas.urls')),
    path('api/estoque/', include('estoque.urls')),
    path('api/maquinario/', include('maquinario.urls')),
    path('api/solicitacoes/', include('solicitacoes.urls')),
    path('api/alertas/', include('alertas.urls')),
    path('api/auditoria/', include('auditoria.urls')),
    path('api/accounts/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]