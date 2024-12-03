from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from difflib import SequenceMatcher
#qr code
import qrcode
from io import BytesIO
from django.http import HttpResponse
import rsa
from PIL import Image, ImageFont, ImageDraw

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

    context = {
        'name':usuario.first_name + " " + usuario.last_name,
        'usuario':usuario.username,
        'contrasena':password,
        'pin':usuario.perfil.pin,
    }

    cifrado = rsa.encrypt(str(usuario.pk).encode(),settings.KEYS['publica']).hex()
    qr = qrcode.QRCode(box_size=10,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(request.build_absolute_uri(reverse_lazy('loginqr',args=[cifrado])))
    img = qr.make_image(fill_color="black",back_color="white")
    stream = BytesIO()
    font = ImageFont.truetype("arial.ttf", 15)
    draw = ImageDraw.Draw(img)
    nombre = usuario.first_name + " " + usuario.last_name
    draw.text((img.width*0.8,img.height*0.95),"{}".format(nombre.upper()),font=font)
    img.save(stream)
    
    email_subject = 'Bienvenido a Artisan'
    email_bodyt = render_to_string('nucleo/emails/registro.html',context)
    email_body = render_to_string('nucleo/emails/registro.html',context)
    email = EmailMultiAlternatives(email_subject,
    email_bodyt, settings.DEFAULT_FROM_EMAIL, [usuario.email,])
    email.attach_alternative(email_body,"text/html")
    email.attach("qr.png",stream.getvalue(),'image/png')
    return email.send(fail_silently=False)

def limpiar_palabra(palabra):
    return palabra.replace('á','a').replace('é','e').replace('í','i').replace('ú','u').replace('ó','o')

def comparar_palabra(palabra, palabra2):
    palabra = limpiar_palabra(palabra.lower())
    palabra2 = limpiar_palabra(palabra2.lower())
    return SequenceMatcher(None, palabra, palabra2).ratio()