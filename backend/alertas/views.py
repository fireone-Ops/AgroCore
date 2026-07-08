from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import TipoPraga, DadosClimaticos, DeteccaoPraga, Alerta, Dashboard
from .serializers import (
    TipoPragaSerializer, DadosClimaticosSerializer,
    DeteccaoPragaSerializer, AlertaSerializer, DashboardSerializer,
)



class TipoPragaViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Catálogo de pragas — somente leitura para usuários comuns."""
    permission_classes = [IsAuthenticated]
    serializer_class = TipoPragaSerializer
    queryset = TipoPraga.objects.all()


class DeteccaoPragaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeteccaoPragaSerializer

    def get_queryset(self):
        qs = DeteccaoPraga.objects.select_related('fazenda', 'tipo_praga')
        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)
        tratado = self.request.query_params.get('tratado')
        if tratado is not None:
            qs = qs.filter(tratamento_realizado=tratado.lower() == 'true')
        return qs

    def perform_create(self, serializer):
        deteccao = serializer.save()
        # Alerta automático para severidade alta/crítica
        if deteccao.severidade in ['ALTA', 'CRITICA']:
            Alerta.objects.create(
                tipo=Alerta.Tipo.PRAGA,
                severidade=deteccao.severidade,
                status=Alerta.Status.NOVO,
                fazenda=deteccao.fazenda,
                plantio=deteccao.plantio,
                deteccao_praga=deteccao,
                titulo=f'Detecção de {deteccao.tipo_praga.nome}',
                descricao=deteccao.descricao,
                recomendacoes=deteccao.recomendacoes,
            )
            dashboard, _ = Dashboard.objects.get_or_create(fazenda=deteccao.fazenda)
            dashboard.atualizar_contadores()


class DadosClimaticosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DadosClimaticosSerializer

    def get_queryset(self):
        qs = DadosClimaticos.objects.select_related('fazenda')
        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)
        dias = int(self.request.query_params.get('dias', 7))
        from datetime import timedelta
        qs = qs.filter(data__gte=timezone.now() - timedelta(days=dias))
        return qs

    def perform_create(self, serializer):
        dados = serializer.save()
        # Alerta automático para clima adverso
        adverso = (
            dados.temperatura_min < 5 or dados.temperatura_max > 40 or
            dados.umidade > 90 or dados.precipitacao > 100 or
            dados.velocidade_vento > 50
        )
        if adverso:
            Alerta.objects.create(
                tipo=Alerta.Tipo.CLIMA_ADVERSO,
                severidade=Alerta.Severidade.ALTA if dados.velocidade_vento > 50 else Alerta.Severidade.MEDIA,
                status=Alerta.Status.NOVO,
                fazenda=dados.fazenda,
                dados_climaticos=dados,
                titulo=f'Clima adverso — {dados.condicao}',
                descricao=(
                    f'Temp: {dados.temperatura_min}–{dados.temperatura_max}°C, '
                    f'Umidade: {dados.umidade}%, Precipitação: {dados.precipitacao}mm'
                ),
                recomendacoes='Verifique as condições de plantações e máquinas.',
            )
            dashboard, _ = Dashboard.objects.get_or_create(fazenda=dados.fazenda)
            dashboard.atualizar_contadores()


class AlertaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlertaSerializer

    def get_queryset(self):
        qs = Alerta.objects.select_related('fazenda', 'deteccao_praga').filter(
            fazenda__produtor=self.request.user
        )
        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)
        st = self.request.query_params.get('status')
        if st:
            qs = qs.filter(status=st)
        severidade = self.request.query_params.get('severidade')
        if severidade:
            qs = qs.filter(severidade=severidade)
        if self.request.query_params.get('nao_lidos') == 'true':
            qs = qs.filter(notificado=False)
        return qs

    def perform_create(self, serializer):
        alerta = serializer.save()
        dashboard, _ = Dashboard.objects.get_or_create(fazenda=alerta.fazenda)
        dashboard.atualizar_contadores()

    # ---- ações especiais ----

    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        alerta = self.get_object()
        alerta.marcar_como_resolvido()
        dashboard, _ = Dashboard.objects.get_or_create(fazenda=alerta.fazenda)
        dashboard.atualizar_contadores()
        return Response({'mensagem': 'Alerta resolvido!', 'alerta': AlertaSerializer(alerta).data})

    @action(detail=True, methods=['post'])
    def notificar(self, request, pk=None):
        alerta = self.get_object()
        alerta.notificar_usuarios()
        alerta.usuarios_notificados.add(request.user)
        return Response({'mensagem': 'Usuários notificados!', 'alerta': AlertaSerializer(alerta).data})

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """GET /alertas/dashboard/?fazenda=<id>"""
        fazenda_id = request.query_params.get('fazenda')
        if not fazenda_id:
            return Response({'erro': 'Parâmetro fazenda é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        from fazendas.models import Fazenda
        try:
            fazenda = Fazenda.objects.get(id=fazenda_id, produtor=request.user)
        except Fazenda.DoesNotExist:
            return Response({'erro': 'Fazenda não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        dash, _ = Dashboard.objects.get_or_create(fazenda=fazenda)
        dash.atualizar_contadores()
        return Response(DashboardSerializer(dash).data)

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """GET /alertas/estatisticas/?fazenda=<id>&dias=30"""
        fazenda_id = request.query_params.get('fazenda')
        dias = int(request.query_params.get('dias', 30))
        from datetime import timedelta
        data_inicio = timezone.now() - timedelta(days=dias)

        qs = Alerta.objects.filter(fazenda__produtor=request.user, criado_em__gte=data_inicio)
        if fazenda_id:
            qs = qs.filter(fazenda_id=fazenda_id)

        return Response({
            'total': qs.count(),
            'por_tipo': {t[0]: qs.filter(tipo=t[0]).count() for t in Alerta.Tipo.choices},
            'por_severidade': {s[0]: qs.filter(severidade=s[0]).count() for s in Alerta.Severidade.choices},
            'por_status': {s[0]: qs.filter(status=s[0]).count() for s in Alerta.Status.choices},
            'periodo_dias': dias,
        })