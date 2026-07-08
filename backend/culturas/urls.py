from rest_framework.routers import DefaultRouter
from .views import CulturaViewSet, PlantioViewSet, ColheitaViewSet, LaudoViewSet

router = DefaultRouter()
router.register(r'culturas',  CulturaViewSet,  basename='cultura')
router.register(r'plantios',  PlantioViewSet,  basename='plantio')
router.register(r'colheitas', ColheitaViewSet, basename='colheita')
router.register(r'laudos',    LaudoViewSet,    basename='laudo')

urlpatterns = router.urls