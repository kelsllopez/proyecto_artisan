from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType


def obtener_nombre(usuario):
    if usuario.first_name:
        return usuario.first_name + " " + usuario.last_name
    else:
        return usuario.username

def historial_create_equipo(user,equipo):
    if equipo.area is not None:
        area = equipo.area.nombre
    else:
        area = 'Sin Área'

    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(equipo).pk,
    object_id       = equipo.pk,
    object_repr     = "Equipo {}".format(equipo.nombre),
    action_flag     = ADDITION,
    change_message = "Se ha creado el equipo {} en {} por el usuario {}".format(equipo.nombre,area,nombre)
)

def historial_update_equipo(user,equipo):
    if equipo.area is not None:
        area = equipo.area.nombre
    else:
        area = 'Sin Área'
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(equipo).pk,
    object_id       = equipo.pk,
    object_repr     = "Equipo {}".format(equipo.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha actualizado el equipo {} en {} por el usuario {}".format(equipo.nombre,area,nombre)
)

def historial_delete_equipo(user,equipo):
    if equipo.area is not None:
        area = equipo.area.nombre
    else:
        area = 'Sin Área'
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(equipo).pk,
    object_id       = equipo.pk,
    object_repr     = "Equipo {}".format(equipo.nombre),
    action_flag     = DELETION,
    change_message = "Se ha eliminado el equipo {} en {} por el usuario {}".format(equipo.nombre,area,nombre)
)

def historial_create_area(user,area):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(area).pk,
    object_id       = area.pk,
    object_repr     = "Área {}".format(area.nombre),
    action_flag     = ADDITION,
    change_message = "Se ha creado el área {} en {} por el usuario {}".format(area.nombre,area.lugar,nombre)
)

def historial_update_area(user,area):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(area).pk,
    object_id       = area.pk,
    object_repr     = "Área {}".format(area.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha actualizado el área {} en {} por el usuario {}".format(area.nombre,area.lugar,nombre)
)

def historial_delete_area(user,area):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(area).pk,
    object_id       = area.pk,
    object_repr     = "Área {}".format(area.nombre),
    action_flag     = DELETION,
    change_message = "Se ha eliminado el área {} en {} por el usuario {}".format(area.nombre,area.lugar,nombre)
)