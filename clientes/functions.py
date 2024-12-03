from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType

def obtener_nombre(usuario):
    if usuario.first_name:
        return usuario.first_name + " " + usuario.last_name
    else:
        return usuario.username

def historial_create_cliente(user,cliente):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente).pk,
    object_id       = cliente.pk,
    object_repr     = "Cliente {}".format(cliente.nombre),
    action_flag     = ADDITION,
    change_message = "Se ha creado el cliente {} - {} por el usuario {}".format(cliente.nombre,cliente.rut,nombre)
    )

def historial_update_cliente(user,cliente):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente).pk,
    object_id       = cliente.pk,
    object_repr     = "Cliente {}".format(cliente.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha actualizado el cliente {} - {} por el usuario {}".format(cliente.nombre,cliente.rut,nombre)
    )

def historial_delete_cliente(user,cliente):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente).pk,
    object_id       = cliente.pk,
    object_repr     = "Cliente {}".format(cliente.nombre),
    action_flag     = DELETION,
    change_message = "Se ha borrado el cliente {} - {} por el usuario {}".format(cliente.nombre,cliente.rut,nombre)
    )

def historial_create_cliente_local(user,cliente_local):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente_local).pk,
    object_id       = cliente_local.pk,
    object_repr     = "Cliente {} - {}".format(cliente_local.cliente.nombre,cliente_local.local),
    action_flag     = ADDITION,
    change_message = "Se ha creado el local {} para el cliente {} por el usuario {}".format(cliente_local.local,cliente_local.cliente.nombre,nombre)
    )

def historial_update_cliente_local(user,cliente_local):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente_local).pk,
    object_id       = cliente_local.pk,
    object_repr     = "Cliente {} - {}".format(cliente_local.cliente.nombre,cliente_local.local),
    action_flag     = CHANGE,
    change_message = "Se ha creado actualizado el local {} para el cliente {} por el usuario {}".format(cliente_local.local,cliente_local.cliente.nombre,nombre)
    )

def historial_delete_cliente_local(user,cliente_local):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(cliente_local).pk,
    object_id       = cliente_local.pk,
    object_repr     = "Cliente {} - {}".format(cliente_local.cliente.nombre,cliente_local.local),
    action_flag     = DELETION,
    change_message = "Se ha creado eliminado el local {} para el cliente {} por el usuario {}".format(cliente_local.local,cliente_local.cliente.nombre,nombre)
    )