from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q, Sum
from .models import Solicitacao
from .serializers import SolicitacaoSerializer, SolicitacaoCriarSerializer, SolicitacaoAprovarSerializer

class SolicitacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return SolicitacaoCriarSerializer
        return SolicitacaoSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Solicitacao.objects.filter(
            Q(fazenda__produtor=user) | Q(solicitante=user)
        ).distinct()

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        st = self.request.query_params.get('status')
        if st:
            qs = qs.filter(status=st)

        return qs

    def perform_create(self, serializer):
        solicitacao = serializer.save(solicitante=self.request.user)
        solicitacao.requer_aprovacao = bool(
            solicitacao.custo_estimado and solicitacao.custo_estimado > 5000
        )
        solicitacao.save()

    def perform_update(self, serializer):
        solicitacao = serializer.save()
        solicitacao.requer_aprovacao = bool(
            solicitacao.custo_estimado and solicitacao.custo_estimado > 5000
        )
        solicitacao.save()

    # ---- ações especiais ----

    @action(detail=False, methods=['get'])
    def minhas(self, request):
        """GET /solicitacoes/minhas/ — apenas as do usuário logado."""
        qs = Solicitacao.objects.filter(solicitante=request.user)
        serializer = SolicitacaoSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def para_aprovar(self, request):
        """GET /solicitacoes/para_aprovar/ — pendentes que o produtor pode aprovar."""
        qs = Solicitacao.objects.filter(
            fazenda__produtor=request.user,
            status=Solicitacao.Status.PENDENTE,
            requer_aprovacao=True,
        )
        serializer = SolicitacaoSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """POST /solicitacoes/<pk>/aprovar/ — aprova ou rejeita."""
        try:
            solicitacao = Solicitacao.objects.get(
                pk=pk,
                fazenda__produtor=request.user,
                status=Solicitacao.Status.PENDENTE,
            )
        except Solicitacao.DoesNotExist:
            return Response(
                {'erro': 'Solicitação não encontrada ou não pode ser modificada'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SolicitacaoAprovarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.validated_data['aprovado']:
            solicitacao.status = Solicitacao.Status.APROVADA
            solicitacao.data_aprovacao = timezone.now()
            mensagem = 'Solicitação aprovada!'
        else:
            solicitacao.status = Solicitacao.Status.REJEITADA
            solicitacao.motivo_rejeicao = serializer.validated_data.get('motivo_rejeicao', '')
            mensagem = 'Solicitação rejeitada.'

        solicitacao.aprovador = request.user
        solicitacao.save()

        return Response({'mensagem': mensagem, 'solicitacao': SolicitacaoSerializer(solicitacao).data})

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """GET /solicitacoes/estatisticas/?fazenda=<id>"""
        qs = Solicitacao.objects.filter(fazenda__produtor=request.user)
        fazenda = request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        custo_aprovado = (
            qs.filter(status=Solicitacao.Status.APROVADA)
            .aggregate(total=Sum('custo_estimado'))['total'] or 0
        )

        return Response({
            'total': qs.count(),
            'pendentes':  qs.filter(status=Solicitacao.Status.PENDENTE).count(),
            'aprovadas':  qs.filter(status=Solicitacao.Status.APROVADA).count(),
            'rejeitadas': qs.filter(status=Solicitacao.Status.REJEITADA).count(),
            'canceladas': qs.filter(status=Solicitacao.Status.CANCELADA).count(),
            'custo_total_aprovado': custo_aprovado,
        })