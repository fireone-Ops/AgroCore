from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import LoginSerializer, RegistroSerializer

Usuario = get_user_model()

MAX_TENTATIVAS = 5  


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email    = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # 1. Busca o usuário pelo email antes de autenticar
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Não revela se o email existe ou não
            return Response(
                {'erro': 'Credenciais inválidas'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 2. Verifica se a conta está bloqueada
        if usuario.bloqueado:
            return Response(
                {'erro': 'Conta bloqueada por excesso de tentativas. Entre em contato com o administrador.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. Verifica se o usuário foi aprovado pelo produtor
        if not usuario.aprovado:
            return Response(
                {'erro': 'Conta ainda não aprovada. Aguarde a autorização do produtor.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. Tenta autenticar
        user = authenticate(request, email=email, password=password)

        if user is None:
            # Senha errada — incrementa tentativas
            usuario.tentativas += 1

            if usuario.tentativas >= MAX_TENTATIVAS:
                usuario.bloqueado = True
                usuario.save(update_fields=['tentativas', 'bloqueado'])
                return Response(
                    {'erro': f'Conta bloqueada após {MAX_TENTATIVAS} tentativas inválidas. Entre em contato com o administrador.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

            usuario.save(update_fields=['tentativas'])
            restantes = MAX_TENTATIVAS - usuario.tentativas
            return Response(
                {'erro': f'Credenciais inválidas. {restantes} tentativa(s) restante(s) antes do bloqueio.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 5. Login bem-sucedido — zera tentativas
        usuario.tentativas = 0
        usuario.save(update_fields=['tentativas'])

        refresh = RefreshToken.for_user(user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
        })


class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'mensagem': 'Usuário registrado com sucesso! Aguarde aprovação do produtor.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response(
                {'erro': 'Token de refresh é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh_token = RefreshToken(refresh)
            return Response({'access': str(refresh_token.access_token)})
        except Exception:
            return Response(
                {'erro': 'Token inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Blacklist do refresh token se o simplejwt tiver configurado
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass  # blacklist não configurada — logout só no cliente

        return Response({'mensagem': 'Logout realizado com sucesso.'})