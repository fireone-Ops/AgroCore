from rest_framework import serializers
from .models import Item, movimentacao, Armazenamento, Relatorio


class ItemSerializer(serializers.ModelSerializer):
    fazenda_id = serializers.IntegerField(write_only=True)
    fazenda_nome = serializers.CharField(source='fazenda.nome', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'fazenda_id', 'fazenda_nome', 'nome', 'tipo', 'unidade', 'estoque_minimo']
        read_only_fields = ['id', 'fazenda_nome']


class MovimentacaoSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = movimentacao
        fields = ['id', 'item', 'item_id', 'tipo', 'quantidade', 'data', 'descricao']
        read_only_fields = ['id', 'data']


class ArmazenamentoSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Armazenamento
        fields = ['id', 'item', 'item_id', 'local', 'capacidade']
        read_only_fields = ['id']


class RelatorioSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Relatorio
        fields = [
            'id', 'item', 'item_id', 'periodo',
            'data_inicio', 'data_fim',
            'quantidade_consumida', 'quantidade_adicionada',
            'saldo_inicial', 'saldo_final',
        ]