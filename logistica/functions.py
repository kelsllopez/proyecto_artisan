from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
#Etiquetas
import qrcode
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageFont, ImageDraw


def obtener_nombre(usuario):
    if usuario.first_name:
        return usuario.first_name + " " + usuario.last_name
    else:
        return usuario.username

def historial_create_envio(user,envio):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(envio).pk,
    object_id       = envio.pk,
    object_repr     = "{} - {}".format(envio.pk,envio.lugar_o.nombre),
    action_flag     = ADDITION,
    change_message = "Se ha generado el envio #{} con origen {} y destino {} por el usuario {}".format(envio.pk,envio.lugar_o.nombre,envio.lugar_d.nombre,nombre)
)

def historial_update_envio(user,envio,recepcion):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(envio).pk,
    object_id       = envio.pk,
    object_repr     = "{} - {}".format(envio.pk,envio.lugar_o.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha {} el envio #{} con origen {} y destino {} por el usuario {}".format(recepcion,envio.pk,envio.lugar_o.nombre,envio.lugar_d.nombre,nombre)
)

def historial_delete_envio(user,envio):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(envio).pk,
    object_id       = envio.pk,
    object_repr     = "{} - {}".format(envio.pk,envio.lugar_o.nombre),
    action_flag     = DELETION,
    change_message = "Se ha eliminado el envio #{} con origen {} y destino {} por el usuario {}".format(envio.pk,envio.lugar_o.nombre,envio.lugar_d.nombre,nombre)
) 

def historial_create_pallet(user,pallet):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pallet).pk,
    object_id       = pallet.pk,
    object_repr     = "{} - {}".format(pallet.pk,pallet.nombre),
    action_flag     = ADDITION,
    change_message = "Se ha agregado el pallet {} en {} por el usuario {}".format(pallet.nombre,pallet.lugar.nombre,nombre)
)

def historial_update_pallet(user,pallet):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pallet).pk,
    object_id       = pallet.pk,
    object_repr     = "{} - {}".format(pallet.pk,pallet.nombre),
    action_flag     = CHANGE,
    change_message = "Se ha actualizado el pallet {} en {} por el usuario {}".format(pallet.nombre,pallet.lugar.nombre,nombre)
)
def historial_delete_pallet(user,pallet):
    nombre = obtener_nombre(user)
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pallet).pk,
    object_id       = pallet.pk,
    object_repr     = "{} - {}".format(pallet.pk,pallet.nombre),
    action_flag     = DELETION,
    change_message = "Se ha eliminado el pallet {} en {} por el usuario {}".format(pallet.nombre,pallet.lugar.nombre,nombre)
)

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

def generar_etiqueta(p,bultos):
    m = 6
    dimensiones = (378*m,189*m)
    image = Image.new('RGB', (dimensiones[0],dimensiones[1]),(255,255,255))
    draw = ImageDraw.Draw(image)
    draw.fontmode = 'L'
    try:
        for index,bulto in enumerate(bultos):
            qr = qrcode.QRCode(box_size=1,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
            oc = bulto.ordendecompra
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
        oc = bulto.ordendecompra
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