from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, MovimentacaoViewSet, ArmazenamentoViewSet, RelatorioViewSet

router = DefaultRouter()
router.register(r'itens',          ItemViewSet,          basename='item')
router.register(r'movimentacoes',  MovimentacaoViewSet,  basename='movimentacao')
router.register(r'armazenamentos', ArmazenamentoViewSet, basename='armazenamento')
router.register(r'relatorios',     RelatorioViewSet,     basename='relatorio')

urlpatterns = router.urls
