from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Não importar aqui para evitar import circular


def registrar_log_auditoria(usuario, acao, modulo, descricao, objeto, fazenda=None, 
                            dados_anteriores=None, dados_novos=None, campos_alterados=None,
                            ip_address=None, user_agent=None, endpoint=None):
    """Função auxiliar para registrar logs de auditoria"""
    from auditoria.models import Log
    
    nome_objeto = str(objeto) if objeto else ''
    content_type = ContentType.objects.get_for_model(objeto.__class__) if objeto else None
    object_id = objeto.id if objeto and hasattr(objeto, 'id') else None
    
    log = Log.objects.create(
        usuario=usuario,
        acao=acao,
        modulo=modulo,
        descricao=descricao,
        fazenda=fazenda,
        content_type=content_type,
        object_id=object_id,
        nome_objeto=nome_objeto,
        dados_anteriores=dados_anteriores,
        dados_novos=dados_novos,
        campos_alterados=campos_alterados,
        ip_address=ip_address,
        user_agent=user_agent,
        endpoint=endpoint
    )
    
    return log
