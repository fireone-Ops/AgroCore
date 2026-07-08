from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q, Count
import csv, json
from io import StringIO
from .models import Log, RelatorioAuditoria
from .serializers import LogSerializer, RelatorioAuditoriaSerializer


class LogViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    Logs são imutáveis (RNF07). Nenhum endpoint de criação/edição/exclusão
    é exposto — logs são criados internamente pelo sistema via signals ou middleware.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Log.objects.filter(
            Q(fazenda__produtor=user) | Q(usuario=user)
        ).order_by('-criado_em')

        usuario = self.request.query_params.get('usuario')
        if usuario:
            qs = qs.filter(usuario_id=usuario)

        fazenda = self.request.query_params.get('fazenda')
        if fazenda:
            qs = qs.filter(fazenda_id=fazenda)

        acao = self.request.query_params.get('acao')
        if acao:
            qs = qs.filter(acao=acao)

        modulo = self.request.query_params.get('modulo')
        if modulo:
            qs = qs.filter(modulo=modulo)

        data_inicio = self.request.query_params.get('data_inicio')
        if data_inicio:
            qs = qs.filter(criado_em__gte=data_inicio)

        data_fim = self.request.query_params.get('data_fim')
        if data_fim:
            qs = qs.filter(criado_em__lte=data_fim)

        return qs

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """GET /logs/estatisticas/?fazenda=<id>&dias=30"""
        fazenda_id = request.query_params.get('fazenda')
        dias = int(request.query_params.get('dias', 30))
        from datetime import timedelta
        data_inicio = timezone.now() - timedelta(days=dias)

        qs = Log.objects.filter(criado_em__gte=data_inicio)
        if fazenda_id:
            qs = qs.filter(fazenda_id=fazenda_id, fazenda__produtor=request.user)
        else:
            qs = qs.filter(fazenda__produtor=request.user)

        return Response({
            'total': qs.count(),
            'por_acao': {a[0]: qs.filter(acao=a[0]).count() for a in Log.Acao.choices},
            'por_modulo': {m[0]: qs.filter(modulo=m[0]).count() for m in Log.ModuloAfetado.choices},
            'usuarios_ativos': list(
                qs.values('usuario__nome').annotate(total=Count('id')).order_by('-total')[:10]
            ),
            'periodo_dias': dias,
        })


class RelatorioAuditoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RelatorioAuditoriaSerializer

    def get_queryset(self):
        qs = RelatorioAuditoria.objects.filter(criado_por=self.request.user)
        st = self.request.query_params.get('status')
        if st:
            qs = qs.filter(status=st)
        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs

    def perform_create(self, serializer):
        relatorio = serializer.save(criado_por=self.request.user)
        self._gerar_relatorio(relatorio)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """GET /relatorios/<pk>/download/"""
        relatorio = self.get_object()
        if not relatorio.arquivo:
            return Response(
                {'erro': 'Arquivo ainda não está pronto'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            'url': relatorio.arquivo.url,
            'nome': relatorio.arquivo.name,
            'formato': relatorio.formato,
        })

    # ---- helpers privados ----

    def _gerar_relatorio(self, relatorio):
        relatorio.status = RelatorioAuditoria.Status.GERANDO
        relatorio.save()
        try:
            qs = Log.objects.all()
            if relatorio.usuario_filtro:
                qs = qs.filter(usuario=relatorio.usuario_filtro)
            if relatorio.fazenda_filtro:
                qs = qs.filter(fazenda=relatorio.fazenda_filtro)
            if relatorio.data_inicio:
                qs = qs.filter(criado_em__gte=relatorio.data_inicio)
            if relatorio.data_fim:
                qs = qs.filter(criado_em__lte=relatorio.data_fim)

            relatorio.total_registros = qs.count()

            if relatorio.formato == 'CSV':
                self._gerar_csv(relatorio, qs)
            elif relatorio.formato == 'JSON':
                self._gerar_json(relatorio, qs)

            relatorio.status = RelatorioAuditoria.Status.PRONTO
            relatorio.gerado_em = timezone.now()
        except Exception as e:
            relatorio.status = RelatorioAuditoria.Status.ERRO
        relatorio.save()

    def _gerar_csv(self, relatorio, logs):
        from django.core.files.base import ContentFile
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Usuário', 'Fazenda', 'Ação', 'Módulo', 'Descrição', 'IP', 'Data'])
        for log in logs:
            writer.writerow([
                log.id, log.usuario_nome, log.fazenda_nome,
                log.get_acao_display(), log.get_modulo_display(),
                log.descricao, log.ip_address or '',
                log.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
            ])
        relatorio.arquivo.save(
            f'auditoria_{relatorio.id}.csv',
            ContentFile(output.getvalue().encode('utf-8'))
        )

    def _gerar_json(self, relatorio, logs):
        from django.core.files.base import ContentFile
        dados = [{
            'id': log.id, 'usuario': log.usuario_nome, 'fazenda': log.fazenda_nome,
            'acao': log.get_acao_display(), 'modulo': log.get_modulo_display(),
            'descricao': log.descricao, 'dados_anteriores': log.dados_anteriores,
            'dados_novos': log.dados_novos, 'ip_address': log.ip_address,
            'criado_em': log.criado_em.isoformat(),
        } for log in logs]
        relatorio.arquivo.save(
            f'auditoria_{relatorio.id}.json',
            ContentFile(json.dumps(dados, indent=2, ensure_ascii=False).encode('utf-8'))
        )