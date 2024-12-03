from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from .models import InventarioInsumo

def obtener_nombre(usuario):
    if usuario.first_name:
        return usuario.first_name + " " + usuario.last_name
    else:
        return usuario.username

def historial_update_inventarioi(user,inventarioinsumo):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(inventarioinsumo).pk,
    object_id       = inventarioinsumo.pk,
    object_repr     = "Inventario Insumo {} - {}".format(inventarioinsumo.insumo.nombre,inventarioinsumo.bodega.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha actualizado el inventario de {} en {} de manera MANUAL por el usuario {}".format(inventarioinsumo.insumo.nombre,inventarioinsumo.bodega.nombre,user.first_name + " " + user.last_name)
    )

def historial_create_bodega(user,bodega):
    LogEntry.objects.log_action(
    user_id = user.pk,
    content_type_id = ContentType.objects.get_for_model(bodega).pk,
    object_id = bodega.pk,
    object_repr = "Bodega {}".format(bodega.nombre),
    action_flag= ADDITION,
    change_message= "El usuario {} ha creado la bodega {}".format(obtener_nombre(user),bodega.nombre)
    )

def historial_update_bodega(user,bodega,prev_bodega):
    LogEntry.objects.log_action(
    user_id = user.pk,
    content_type_id = ContentType.objects.get_for_model(bodega).pk,
    object_id = bodega.pk,
    object_repr = "Bodega {}".format(bodega.nombre),
    action_flag= CHANGE,
    change_message= "El usuario {} ha modificado el nombre de la bodega {} a {}".format(obtener_nombre(user),prev_bodega.nombre,bodega.nombre)
    )

def historial_delete_bodega(user,bodega):
    LogEntry.objects.log_action(
    user_id = user.pk,
    content_type_id = ContentType.objects.get_for_model(bodega).pk,
    object_id = bodega.pk,
    object_repr = "Bodega {}".format(bodega.nombre),
    action_flag= DELETION,
    change_message= "El usuario {} ha eliminado la bodega {}".format(obtener_nombre(user),bodega.nombre)
    )