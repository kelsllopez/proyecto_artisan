from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType

def obtener_nombre(user):
    if user.first_name != '':
        return user.first_name + " " + user.last_name
    else:
        return user.username

def historial_crear_pauta(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Pauta de elaboración {}".format(pauta.nombre),
    action_flag     = ADDITION,
    change_message = "La pauta de elaboración {} ha sido añadida por el usuario {}".format(pauta.nombre,obtener_nombre(user))
    )

def historial_actualizar_pauta(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Pauta de elaboración {}".format(pauta.nombre),
    action_flag     = CHANGE,
    change_message = "La pauta de elaboración {} ha sido actualizada por el usuario {}".format(pauta.nombre,obtener_nombre(user))
    )

def historial_eliminar_pauta(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Pauta de elaboración {}".format(pauta.nombre),
    action_flag     = DELETION,
    change_message = "La pauta de elaboración {} ha sido eliminada por el usuario {}".format(pauta.nombre,obtener_nombre(user))
    )

def historial_crear_parametro_pauta(user,columna):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(columna).pk,
    object_id       = columna.pk,
    object_repr     = "Parámetro {}".format(columna.nombre),
    action_flag     = ADDITION,
    change_message = "El parámetro {} ha sido añadido por el usuario {}".format(columna.nombre,obtener_nombre(user))
    )

def historial_actualizar_parametro_pauta(user,columna):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(columna).pk,
    object_id       = columna.pk,
    object_repr     = "Parámetro {}".format(columna.nombre),
    action_flag     = CHANGE,
    change_message = "El parámetro {} ha sido actualizado por el usuario {}".format(columna.nombre,obtener_nombre(user))
    )

def historial_eliminar_parametro_pauta(user,columna):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(columna).pk,
    object_id       = columna.pk,
    object_repr     = "Parámetro {}".format(columna.nombre),
    action_flag     = DELETION,
    change_message = "El parámetro {} ha sido eliminado por el usuario {}".format(columna.nombre,obtener_nombre(user))
    )