from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Fazenda, AcessoFazenda
from .serializers import FazendaSerializer, AcessoFazendaSerializer


class FazendaViewSet(viewsets.ModelViewSet):
   
    permission_classes = [IsAuthenticated]
    serializer_class = FazendaSerializer

    def get_queryset(self):
        qs = Fazenda.objects.filter(produtor=self.request.user)

        # ativa=true  →  apenas ativas
        # ativa=false →  apenas inativas
        # sem param    →  todas
        ativa = self.request.query_params.get('ativa')
        if ativa is not None:
            qs = qs.filter(ativa=ativa.lower() == 'true')

        return qs

    def perform_create(self, serializer):
        serializer.save(produtor=self.request.user)

    @action(detail=True, methods=['post'])
    def ativar(self, request, pk=None):
        fazenda = self.get_object()
        fazenda.ativa = not fazenda.ativa
        fazenda.save()
        estado = 'ativada' if fazenda.ativa else 'desativada'
        return Response({'mensagem': f'Fazenda {estado} com sucesso!'})


class AcessoFazendaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AcessoFazendaSerializer

    def get_queryset(self):
        return AcessoFazenda.objects.filter(fazenda__produtor=self.request.user)

    def perform_create(self, serializer):
        serializer.save()