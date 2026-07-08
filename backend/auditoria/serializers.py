from rest_framework import serializers
from .models import Log, RelatorioAuditoria


class LogSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome', read_only=True)
    fazenda_nome = serializers.CharField(source='fazenda.nome', read_only=True, allow_null=True)
    
    class Meta:
        model = Log
        fields = [
            'id', 'usuario', 'usuario_nome', 'fazenda', 'fazenda_nome',
            'acao', 'modulo', 'descricao', 'nome_objeto',
            'dados_anteriores', 'dados_novos', 'campos_alterados',
            'ip_address', 'endpoint', 'criado_em'
        ]
        read_only_fields = [
            'id', 'usuario_nome', 'fazenda_nome', 'criado_em',
            'dados_anteriores', 'dados_novos', 'campos_alterados'
        ]


class RelatorioAuditoriaSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.nome', read_only=True)
    usuario_filtro_nome = serializers.CharField(source='usuario_filtro.nome', read_only=True, allow_null=True)
    fazenda_filtro_nome = serializers.CharField(source='fazenda_filtro.nome', read_only=True, allow_null=True)
    
    class Meta:
        model = RelatorioAuditoria
        fields = [
            'id', 'titulo', 'tipo', 'status',
            'criado_por', 'criado_por_nome',
            'usuario_filtro', 'usuario_filtro_nome',
            'fazenda_filtro', 'fazenda_filtro_nome',
            'data_inicio', 'data_fim',
            'total_registros', 'arquivo', 'formato',
            'criado_em', 'gerado_em', 'atualizado_em'
        ]
        read_only_fields = [
            'id', 'criado_por_nome', 'usuario_filtro_nome', 'fazenda_filtro_nome',
            'total_registros', 'arquivo', 'criado_em', 'gerado_em', 'atualizado_em'
        ]
