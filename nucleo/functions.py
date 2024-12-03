from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from difflib import SequenceMatcher
from nucleo.tasks import enviar_correo_task
from django.urls import reverse_lazy
from django.conf import settings
import rsa

def obtener_nombre(usuario):
    if usuario.first_name:
        return usuario.first_name + " " + usuario.last_name
    else:
        return usuario.username

def historial_crear_insumo(user,insumo):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(insumo).pk,
    object_id       = insumo.pk,
    object_repr     = "Insumo {}".format(insumo.nombre),
    action_flag     = ADDITION,
    change_message = "El empleado {} ha agregado el insumo {}".format(obtener_nombre(user),insumo.nombre)
    )

def historial_actualizar_insumo(user,insumo):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(insumo).pk,
    object_id       = insumo.pk,
    object_repr     = "Insumo {}".format(insumo.nombre),
    action_flag     = CHANGE,
    change_message = "El empleado {} ha modificado el insumo {}".format(obtener_nombre(user),insumo.nombre)
    )

def historial_eliminar_insumo(user,insumo):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(insumo).pk,
    object_id       = insumo.pk,
    object_repr     = "Insumo {}".format(insumo.nombre),
    action_flag     = DELETION,
    change_message = "El empleado {} ha eliminado el insumo {}".format(obtener_nombre(user),insumo.nombre)
    )

def historial_crear_rama(user,rama):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(rama).pk,
    object_id       = rama.pk,
    object_repr     = "Área de negocio: {}".format(rama.nombre),
    action_flag     = ADDITION,
    change_message = "El empleado {} ha agregado el área de negocio: {}".format(obtener_nombre(user),rama.nombre)
    )

def historial_actualizar_rama(user,rama):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(rama).pk,
    object_id       = rama.pk,
    object_repr     = "Área de negocio: {}".format(rama.nombre),
    action_flag     = CHANGE,
    change_message = "El empleado {} ha modificado el área de negocio: {}".format(obtener_nombre(user),rama.nombre)
    )

def historial_eliminar_rama(user,rama):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(rama).pk,
    object_id       = rama.pk,
    object_repr     = "Área de negocio: {}".format(rama.nombre),
    action_flag     = DELETION,
    change_message = "El empleado {} ha eliminado el área de negocio: {}".format(obtener_nombre(user),rama.nombre)
    )

def historial_crear_producto(user,producto):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(producto).pk,
    object_id       = producto.pk,
    object_repr     = "Producto: {}".format(producto.nombre),
    action_flag     = ADDITION,
    change_message = "El empleado {} ha agregado el producto: {}".format(obtener_nombre(user),producto.nombre)
    )

def historial_actualizar_producto(user,producto):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(producto).pk,
    object_id       = producto.pk,
    object_repr     = "Producto: {}".format(producto.nombre),
    action_flag     = CHANGE,
    change_message = "El empleado {} ha modificado el producto: {}".format(obtener_nombre(user),producto.nombre)
    )

def historial_eliminar_producto(user,producto):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(producto).pk,
    object_id       = producto.pk,
    object_repr     = "Producto: {}".format(producto.nombre),
    action_flag     = DELETION,
    change_message = "El empleado {} ha eliminado el producto: {}".format(obtener_nombre(user),producto.nombre)
    )


def enviar_correo(usuario,password,request):
    cifrado = rsa.encrypt(str(usuario.pk).encode(),settings.KEYS['publica']).hex()
    url = request.build_absolute_uri(reverse_lazy('loginqr',args=[cifrado]))
    enviar_correo_task.delay(usuario.pk,password,url)
    return True
    

def limpiar_palabra(palabra):
    return palabra.replace('á','a').replace('é','e').replace('í','i').replace('ú','u').replace('ó','o')

def comparar_palabra(palabra, palabra2):
    palabra = limpiar_palabra(palabra.lower())
    palabra2 = limpiar_palabra(palabra2.lower())
    return SequenceMatcher(None, palabra, palabra2).ratio()