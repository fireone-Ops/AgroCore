from rest_framework import serializers
from .models import Solicitacao
from accounts.serializers import UsuarioSerializer


class SolicitacaoSerializer(serializers.ModelSerializer):
    solicitante = UsuarioSerializer(read_only=True)
    aprovador = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Solicitacao
        fields = [
            'id',
            'tipo',
            'status',
            'titulo',
            'descricao',
            'custo_estimado',
            'requer_aprovacao',
            'fazenda',
            'solicitante',
            'aprovador',
            'motivo_rejeicao',
            'observacoes',
            'criado_em',
            'atualizado_em',
            'data_aprovacao'
        ]
        read_only_fields = ['id', 'solicitante', 'aprovador', 'criado_em', 'atualizado_em', 'data_aprovacao', 'requer_aprovacao']


class SolicitacaoCriarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitacao
        fields = [
            'tipo',
            'titulo',
            'descricao',
            'custo_estimado',
            'fazenda',
            'observacoes'
        ]


class SolicitacaoAprovarSerializer(serializers.Serializer):
    aprovado = serializers.BooleanField(required=True)
    motivo_rejeicao = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('aprovado') and not data.get('motivo_rejeicao'):
            raise serializers.ValidationError("Motivo da rejeição é obrigatório quando não aprovada")
        return data
