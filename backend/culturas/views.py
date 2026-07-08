from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Cultura, Plantio, Colheita, Laudo
from .serializers import CulturaSerializer, PlantioSerializer, ColheitaSerializer, LaudoSerializer

class CulturaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CulturaSerializer
    queryset = Cultura.objects.all()


class PlantioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlantioSerializer

    def get_queryset(self):
        qs = Plantio.objects.select_related('fazenda', 'cultura', 'responsavel')

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)

        return qs

    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)


class ColheitaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ColheitaSerializer

    def get_queryset(self):
        qs = Colheita.objects.select_related('plantio', 'responsavel')

        plantio = self.request.query_params.get('plantio')
        if plantio:
            qs = qs.filter(plantio_id=plantio)

        return qs

    def perform_create(self, serializer):
        serializer.save(responsavel=self.request.user)


class LaudoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LaudoSerializer

    def get_queryset(self):
        qs = Laudo.objects.select_related('fazenda', 'agronomo')

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)

        return qs

    def perform_create(self, serializer):
        serializer.save(agronomo=self.request.user)