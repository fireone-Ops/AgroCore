from rest_framework.routers import DefaultRouter
from .views import FazendaViewSet, AcessoFazendaViewSet

router = DefaultRouter()
router.register(r'', FazendaViewSet, basename='fazenda')
router.register(r'acessos', AcessoFazendaViewSet, basename='acesso')

urlpatterns = router.urls

