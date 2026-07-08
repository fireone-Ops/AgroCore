from rest_framework.routers import DefaultRouter
from .views import TipoPragaViewSet, DeteccaoPragaViewSet, DadosClimaticosViewSet, AlertaViewSet

router = DefaultRouter()
router.register(r'tipos-pragas',    TipoPragaViewSet,      basename='tipo-praga')
router.register(r'deteccoes',       DeteccaoPragaViewSet,  basename='deteccao')
router.register(r'dados-climaticos',DadosClimaticosViewSet,basename='dados-climaticos')
router.register(r'alertas',         AlertaViewSet,         basename='alerta')

urlpatterns = router.urls