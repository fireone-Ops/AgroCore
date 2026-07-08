from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'perfil', 'aprovado', 'bloqueado']
        read_only_fields = ['id']


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password', 'password_confirm', 'perfil']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'As senhas não coinciden'})
        return data

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            nome=validated_data['nome'],
            perfil=validated_data.get('perfil', Usuario.Perfil.PRODUTOR),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)