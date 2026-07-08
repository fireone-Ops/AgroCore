from rest_framework import serializers
from .models import Cultura, Plantio, Colheita, Laudo

class CulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ('id', 'nome', 'mes_inicio', 'mes_fim', 'descricao')
        read_only_fields = ('id',)

class PlantioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantio
        fields = ('id', 'cultura', 'fazenda', 'responsavel', 'data_plantio', 'area_plantada', 'status', 'observacoes', 'criado_em')
        read_only_fields = ('id', 'responsavel', 'criado_em')

class ColheitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colheita
        fields = ('id', 'plantio', 'responsavel', 'data_colheita', 'area_colhida', 'quantidade_kg', 'observacoes', 'criado_em')
        read_only_fields = ('id', 'responsavel', 'criado_em')

class LaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = ('id', 'fazenda', 'plantio', 'agronomo', 'tipo', 'titulo', 'descricao', 'recomendacoes', 'ph_solo', 
                 'umidade_solo', 'tipo_praga', 'nivel_severidade_praga', 'tipo_risco', 'criado_em')
        read_only_fields = ('id', 'agronomo', 'criado_em')