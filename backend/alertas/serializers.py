from rest_framework import serializers
from .models import TipoPraga, DadosClimaticos, DeteccaoPraga, Alerta, Dashboard


class TipoPragaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPraga
        fields = ['id', 'nome', 'descricao', 'severidade_max', 'culturas_afetadas']
        read_only_fields = ['id']


class DadosClimaticosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosClimaticos
        fields = [
            'id', 'fazenda', 'data', 'fonte',
            'temperatura_min', 'temperatura_max', 'umidade',
            'precipitacao', 'velocidade_vento', 'condicao', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class DeteccaoPragaSerializer(serializers.ModelSerializer):
    tipo_praga = TipoPragaSerializer(read_only=True)
    tipo_praga_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = DeteccaoPraga
        fields = [
            'id', 'plantio', 'fazenda', 'tipo_praga', 'tipo_praga_id',
            'severidade', 'area_afetada_percentual', 'descricao',
            'latitude', 'longitude', 'data_deteccao', 'data_atualizacao',
            'recomendacoes', 'tratamento_realizado', 'data_tratamento', 'observacoes'
        ]
        read_only_fields = ['id', 'data_deteccao', 'data_atualizacao']


class AlertaSerializer(serializers.ModelSerializer):
    deteccao_praga = DeteccaoPragaSerializer(read_only=True)
    
    class Meta:
        model = Alerta
        fields = [
            'id', 'tipo', 'severidade', 'status',
            'fazenda', 'plantio', 'deteccao_praga', 'dados_climaticos',
            'titulo', 'descricao', 'recomendacoes',
            'notificado', 'data_notificacao', 'criado_em', 'atualizado_em', 'data_resolucao'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'data_notificacao', 'data_resolucao']


class DashboardSerializer(serializers.ModelSerializer):
    ultima_praga = DeteccaoPragaSerializer(read_only=True)
    ultimo_dado_climatico = DadosClimaticosSerializer(read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'fazenda', 'total_alertas', 'alertas_criticos', 'alertas_altos',
            'alertas_medios', 'alertas_baixos', 'alertas_nao_lidos',
            'ultima_praga', 'ultimo_dado_climatico', 'atualizado_em'
        ]
        read_only_fields = ['fazenda', 'atualizado_em']
