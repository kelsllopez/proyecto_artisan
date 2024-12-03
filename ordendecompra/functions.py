from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from .models import Registro
#codigo de barra
from reportlab.graphics.barcode import code128
import barcode
from io import BytesIO
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import qrcode
from PIL import Image, ImageFont, ImageDraw

def historial_crear_oc(user,orden):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(orden).pk,
    object_id       = orden.pk,
    object_repr     = "Orden de compra {}".format(orden.numero),
    action_flag     = ADDITION,
    change_message = "La orden de compra {} ha sido solicitada el usuario {}".format(orden.numero,user)
    )

def historial_rechazar_oc(user,orden):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(orden).pk,
    object_id       = orden.pk,
    object_repr     = "Orden de compra {}".format(orden.numero),
    action_flag     = DELETION,
    change_message = "La orden de compra {} ha sido rechazada por el usuario {}".format(orden.numero,user)
    )

def historial_eliminar_oc(user,orden):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(orden).pk,
    object_id       = orden.pk,
    object_repr     = "Orden de compra {}".format(orden.numero),
    action_flag     = DELETION,
    change_message = "La orden de compra {} ha sido eliminada por el usuario {}".format(orden.numero,user)
    )

def historial_cambiar_estado_oc(user,orden):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(orden).pk,
    object_id       = orden.pk,
    object_repr     = "Orden de compra {}".format(orden.numero),
    action_flag     = CHANGE,
    change_message = "La orden de compra {} ha sido {} por el usuario {}".format(orden.numero,orden.estado,user)
    )

def registrarCambioEstado(orden,empleado):
    registro = {'orden':orden,'estado':orden.estado,'empleado':empleado}
    Registro(**registro).save()

def historial_eliminara_oc(user,archivo):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(archivo.orden).pk,
    object_id       = archivo.orden.pk,
    object_repr     = "Orden de compra {}".format(archivo.orden.numero),
    action_flag     = CHANGE,
    change_message = "Se ha eliminado el archivo {} de la orden n° {} por el usuario {}".format(archivo,archivo.orden.numero,user)
    )

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def escribir(draw,texto,tamanom,m,pos):
    fontp = ImageFont.truetype("tahoma.ttf",14*m)
    w, h = draw.textsize(texto,font=fontp)
    fontsize =14*m
    while w > tamanom:
        fontsize-=1
        fontp = ImageFont.truetype("tahoma.ttf",fontsize)
        w, h = draw.textsize(texto,font=fontp)
    draw.text(pos,texto, (0,0,0), font=fontp)
    return


def generar_etiqueta(p,oc,bultos):
    m = 6
    dimensiones = (378*m,189*m)
    image = Image.new('RGB', (dimensiones[0],dimensiones[1]),(255,255,255))
    draw = ImageDraw.Draw(image)
    draw.fontmode = 'L'
    try:
        for index,bulto in enumerate(bultos):
            qr = qrcode.QRCode(box_size=1,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(f"I {oc.numero} {bulto.id}")
            codigo = qr.make_image(fill="black")
            codigo = codigo.resize((100*m,100*m))
            if(index == 0):
                escribir(draw,"OC #{} B{}".format(oc.numero,bulto.pk),180*m-10,m,(8*m,8*m))
                escribir(draw,"{} ({}u)".format(bulto.insumo.nombre,float(round(bulto.cantidad,3))),180*m-10,m,(8*m,28*m))
                if bulto.lotep != '':
                    escribir(draw,f"Lote: {bulto.lotep}",180*m-10,m,(8*m,48*m))
                else:
                    escribir(draw,f"Sin Lote",180*m-10,m,(8*m,48*m))
                escribir(draw,f"{oc.proveedor.empresa_nombre}",180*m-10,m,(8*m,68*m))
                image.paste(codigo,(0*m,88*m))
            else:
                inicio = 205
                escribir(draw,"OC #{} B{}".format(oc.numero,bulto.pk),170*m,m,(inicio*m,8*m))
                escribir(draw,"{} ({}u)".format(bulto.insumo.nombre,float(round(bulto.cantidad,3))),170*m-10,m,(inicio*m,28*m))
                if bulto.lotep != "":
                    escribir(draw,f"Lote: {bulto.lotep}",170*m,m,(inicio*m,48*m))
                else:
                    escribir(draw,f"Sin Lote",170*m,m,(inicio*m,48*m))
                escribir(draw,f"{oc.proveedor.empresa_nombre}",170*m,m,(inicio*m,68*m))
                image.paste(codigo,((inicio-8)*m,88*m))
    except:
        bulto = bultos
        qr = qrcode.QRCode(box_size=1,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(f"I {oc.numero} {bulto.id}")
        codigo = qr.make_image(fill="black")
        codigo = codigo.resize((100*m,100*m))
        escribir(draw,"OC #{} B{}".format(oc.numero,bulto.pk),180*m-10,m,(8*m,8*m))
        escribir(draw,"{} ({}u)".format(bulto.insumo.nombre,float(round(bulto.cantidad,3))),180*m-10,m,(8*m,28*m))
        if bulto.lotep != "":
            escribir(draw,f"Lote: {bulto.lotep}",180*m-10,m,(8*m,48*m))
        else:
            escribir(draw,f"Sin Lote: {bulto.lotep}",180*m-10,m,(8*m,48*m))
        escribir(draw,f"{oc.proveedor.empresa_nombre}",180*m-10,m,(8*m,68*m))
        image.paste(codigo,(0*m,88*m))
    pan = ImageReader(image)
    p.drawImage(pan,0,0,dimensiones[0]/m,dimensiones[1]/m,None,True)
    p.showPage()
    return