from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Maquinario, Manutenção, Telemetria, Atividade
from .serializers import MaquinarioSerializer, ManutencoSerializer, TelemetriaSerializer, AtividadeSerializer


class CriarMaquinarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MaquinarioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarMaquinariosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, pk):
        try:
            maquinario = Maquinario.objects.get(pk=pk)
            serializer = MaquinarioSerializer(maquinario)
            return Response(serializer.data)
        except Maquinario.DoesNotExist:
            return Response({'ERRO': 'Maquinário não localizado'})


class CriarManutencaoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ManutencoSerializer(data=request.data)
        
        if serializer.is_valid():
            maquinario_id = request.data.get('maquinario_id')
            try:
                maquinario = Maquinario.objects.get(pk=maquinario_id)
                serializer.save(maquinario=maquinario)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Maquinario.DoesNotExist:
                return Response({'ERRO': 'Maquinário não localizado'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarManutencaoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, pk):
        try:
            manutencao = Manutenção.objects.get(pk=pk)
            serializer = ManutencoSerializer(manutencao)
            return Response(serializer.data)
        except Manutenção.DoesNotExist:
            return Response({'ERRO': 'Manutenção não localizada'})


class CriarTelemetriaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TelemetriaSerializer(data=request.data)
        
        if serializer.is_valid():
            maquinario_id = request.data.get('maquinario_id')
            try:
                maquinario = Maquinario.objects.get(pk=maquinario_id)
                serializer.save(maquinario=maquinario)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Maquinario.DoesNotExist:
                return Response({'ERRO': 'Maquinário não localizado'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarTelemetriaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, pk):
        try:
            telemetria = Telemetria.objects.get(pk=pk)
            serializer = TelemetriaSerializer(telemetria)
            return Response(serializer.data)
        except Telemetria.DoesNotExist:
            return Response({'ERRO': 'Telemetria não localizada'})


class CriarAtividadeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AtividadeSerializer(data=request.data)
        
        if serializer.is_valid():
            maquinario_id = request.data.get('maquinario_id')
            try:
                maquinario = Maquinario.objects.get(pk=maquinario_id)
                serializer.save(maquinario=maquinario)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Maquinario.DoesNotExist:
                return Response({'ERRO': 'Maquinário não localizado'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarAtividadeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, pk):
        try:
            atividade = Atividade.objects.get(pk=pk)
            serializer = AtividadeSerializer(atividade)
            return Response(serializer.data)
        except Atividade.DoesNotExist:
            return Response({'ERRO': 'Atividade não localizada'})
