from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item, movimentacao, Armazenamento, Relatorio, calcular_estoque
from .serializers import ItemSerializer, MovimentacaoSerializer, ArmazenamentoSerializer, RelatorioSerializer
from fazendas.models import Fazenda


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get_queryset(self):
    
        qs = Item.objects.filter(fazenda__produtor=self.request.user).select_related('fazenda')

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)

        return qs

    def perform_create(self, serializer):
        fazenda_id = self.request.data.get('fazenda_id')
        try:
            fazenda = Fazenda.objects.get(pk=fazenda_id, produtor=self.request.user)
        except Fazenda.DoesNotExist:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Fazenda não encontrada ou sem permissão.')
        serializer.save(fazenda=fazenda)

    @action(detail=True, methods=['get'], url_path='estoque_atual')
    def estoque_atual(self, request, pk=None):
        item = self.get_object()
        saldo = calcular_estoque(item)
        return Response({
            'item': item.nome,
            'fazenda': item.fazenda.nome,
            'saldo': saldo,
            'estoque_minimo': item.estoque_minimo,
            'abaixo_do_minimo': saldo <= item.estoque_minimo,
        })


class MovimentacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        qs = movimentacao.objects.filter(
            item__fazenda__produtor=self.request.user
        ).select_related('item', 'item__fazenda')

        item = self.request.query_params.get('item')
        if item:
            qs = qs.filter(item_id=item)

        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(item__fazenda_id=fazenda)

        return qs


class ArmazenamentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ArmazenamentoSerializer

    def get_queryset(self):
        return Armazenamento.objects.filter(
            item__fazenda__produtor=self.request.user
        ).select_related('item', 'item__fazenda')


class RelatorioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RelatorioSerializer

    def get_queryset(self):
        qs = Relatorio.objects.filter(
            item__fazenda__produtor=self.request.user
        ).select_related('item', 'item__fazenda')

        item = self.request.query_params.get('item')
        if item:
            qs = qs.filter(item_id=item)

        return qs