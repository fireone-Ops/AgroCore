from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Fazenda, AcessoFazenda

Usuario = get_user_model()


class FazendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fazenda
        fields = ('id', 'nome', 'localizacao', 'cidade', 'estado', 'area_total', 'tipo_solo', 'produtor', 'ativa', 'criado_em', 'atualizado_em')
        read_only_fields = ('id', 'produtor', 'criado_em', 'atualizado_em')


class AcessoFazendaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.nome', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = AcessoFazenda
        fields = ('id', 'fazenda', 'usuario', 'usuario_nome', 'usuario_email', 'email', 'perfil', 'ativo', 'criado_em')
        read_only_fields = ('id', 'criado_em', 'usuario_nome', 'usuario_email', 'usuario')

    def validate(self, attrs):
        fazenda = attrs.get('fazenda')
        if fazenda and fazenda.produtor != self.context['request'].user:
            raise serializers.ValidationError({'fazenda': 'Você só pode criar acessos para suas fazendas.'})
        return attrs

    def validate_email(self, value):
        try:
            usuario = Usuario.objects.get(email=value)
        except Usuario.DoesNotExist as exc:
            raise serializers.ValidationError('Usuário não encontrado para este e-mail.') from exc

        if usuario == self.context['request'].user:
            raise serializers.ValidationError('Você não pode conceder acesso a si mesmo.')
        return value

    def create(self, validated_data):
        email = validated_data.pop('email')
        usuario = Usuario.objects.get(email=email)
        return AcessoFazenda.objects.create(usuario=usuario, **validated_data)