# auditoria/urls.py
from rest_framework.routers import DefaultRouter
from .views import LogViewSet, RelatorioAuditoriaViewSet

router = DefaultRouter()
router.register(r'logs',       LogViewSet,                basename='log')
router.register(r'relatorios', RelatorioAuditoriaViewSet, basename='relatorio-auditoria')

urlpatterns = router.urls
