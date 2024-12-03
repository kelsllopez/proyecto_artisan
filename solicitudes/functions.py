from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType


def historial_solicitud(user, solicitud, tipo):
    tipos = {'agregado': ADDITION, 'cambiado': CHANGE, 'borrado': DELETION}
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(solicitud).pk,
        object_id=solicitud.pk,
        object_repr=f"Solicitud {solicitud.pk} - {solicitud.lugar_o.nombre}",
        action_flag=tipos[tipo],
        change_message=f"El usuario {user.first_name} {user.last_name} de identificador: {user.pk} a {tipo} la solicitud."
    )
    return True
