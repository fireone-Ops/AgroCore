from rest_framework import serializers
from .models import Maquinario, Manutenção, Telemetria, Atividade


class MaquinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquinario
        fields = [
            'id', 'fazenda', 'nome', 'serialNumber', 'tipo',
            'possui_telemetria', 'horimetro_atual', 'capacidade_tanque',
        ]
        read_only_fields = ['id', 'horimetro_atual']  # horímetro é atualizado automaticamente


class ManutencoSerializer(serializers.ModelSerializer):
    maquinario    = MaquinarioSerializer(read_only=True)
    maquinario_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Manutenção
        fields = [
            'id', 'maquinario', 'maquinario_id', 'tipo', 'status',
            'descricao', 'data_inicio', 'data_fim', 'custo',
            'responsavel', 'observacoes', 'criado_em',
        ]
        read_only_fields = ['id', 'criado_em']


class TelemetriaSerializer(serializers.ModelSerializer):
    maquinario    = MaquinarioSerializer(read_only=True)
    maquinario_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Telemetria
        fields = ['id', 'maquinario', 'maquinario_id', 'ip', 'status', 'motor_ligado', 'data_hora']
        read_only_fields = ['id', 'data_hora']


class AtividadeSerializer(serializers.ModelSerializer):
    maquinario    = MaquinarioSerializer(read_only=True)
    maquinario_id = serializers.IntegerField(write_only=True)
    horas_trabalhadas = serializers.FloatField(read_only=True)  # calculado via @property

    class Meta:
        model = Atividade
        fields = [
            'id', 'maquinario', 'maquinario_id', 'descricao', 'origem',
            'data_inicio', 'data_fim',
            # novos campos
            'horimetro_inicio', 'horimetro_fim', 'horas_trabalhadas',
            'combustivel_litros', 'problema_reportado',
        ]
        read_only_fields = ['id', 'horas_trabalhadas']

    def validate(self, data):
        """Garante que horimetro_fim >= horimetro_inicio."""
        inicio = data.get('horimetro_inicio')
        fim    = data.get('horimetro_fim')
        if inicio is not None and fim is not None and fim < inicio:
            raise serializers.ValidationError(
                {'horimetro_fim': 'O horímetro final não pode ser menor que o inicial.'}
            )
        return data