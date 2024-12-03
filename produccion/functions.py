from django.contrib.admin.models import CHANGE, LogEntry, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
import barcode
from barcode.writer import ImageWriter
from barcode import generate
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime,timedelta
from PIL import Image, ImageFont, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
import qrcode

def historial_crear_elaboracion(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Elaboración {}".format(pauta.pk),
    action_flag     = ADDITION,
    change_message = "La elaboración {} ha sido iniciada por el usuario {}".format(pauta.pk,user)
    )


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def historial_eliminar_elaboracion(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Elaboración {}".format(pauta.pk),
    action_flag     = DELETION,
    change_message = "La elaboración {} ha sido eliminada por el usuario {}".format(pauta.pk,user)
    )

def historial_actualizar_elaboracion(user,pauta):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(pauta).pk,
    object_id       = pauta.pk,
    object_repr     = "Elaboración {}".format(pauta.pk),
    action_flag     = CHANGE,
    change_message = "La elaboración {} ha sido actualizada por el usuario {}".format(pauta.pk,user)
    )

def historial_crear_lote(user,lote):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(lote).pk,
    object_id       = lote.pk,
    object_repr     = "Lote {}".format(lote.numero),
    action_flag     = ADDITION,
    change_message = "El lote {} ha sido creado por el usuario {}".format(lote.numero,user)
    )

def historial_actualizar_lote(user,lote):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(lote).pk,
    object_id       = lote.pk,
    object_repr     = "Lote {}".format(lote.numero),
    action_flag     = CHANGE,
    change_message = "El lote {} ha sido actualizado por el usuario {}".format(lote.numero,user)
    )

def historial_eliminar_lote(user,lote):
    LogEntry.objects.log_action(
    user_id         = user.pk, 
    content_type_id = ContentType.objects.get_for_model(lote).pk,
    object_id       = lote.pk,
    object_repr     = "Lote {}".format(lote.numero),
    action_flag     = DELETION,
    change_message = "El lote {} ha sido eliminado por el usuario {}".format(lote.numero,user)
    )

def obtener_lunes(dt,dias):
    if dias is None:
        dia = (dt - timedelta(days=dt.weekday()))
    else:
        if dias < 7:
            dia = dt
        else:
           dia = (dt - timedelta(days=dt.weekday())) 
    return dia.replace(hour=0,minute=0,second=0,microsecond=0)

def generar_codigo(p,lote,i, unidad):
    m = 3
    titulo = 'ELABORADORA DE ALIMENTOS GOURMET LTDA.'
    producto = f"{lote.producto.nombre} ({lote.producto.presentacion} {lote.producto.unidad})".upper()
    sap = f'SAP {lote.producto.sap}'
    unidades = f'{unidad} unds. por caja'
    fecha_f = lote.pauta_produccion.fecha + timedelta(lote.producto.duracion)
    fecha = f'FECHA DE VENC: {fecha_f.strftime("%d/%m/%Y")}'
    dun14 = lote.producto.dun14
    dimensiones = (378*m,265*m)

    img = Image.new('RGB', dimensiones, color="white")
    draw = ImageDraw.Draw(img)
    draw.fontmode = 'L'
    font = ImageFont.truetype("malgunbd.ttf", 12*m)
    fonts = ImageFont.truetype("malgunbd.ttf", 14*m)
    fontu = ImageFont.truetype("malgunbd.ttf", 14*m)
    fontf = ImageFont.truetype("malgunbd.ttf", 14*m)
    fontp = ImageFont.truetype("tahoma.ttf",18*m)
    fonti = ImageFont.truetype("tahoma.ttf",7*m)
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    w, h = draw.textsize(titulo,font=font)
    draw.text(((img.width - w)/2,15.7*m),titulo, (0,0,0), font=font)
    fontsize=18*m
    w, h = draw.textsize(producto,font=fontp)
    while w > img.width:
        fontsize-=1
        fontp = ImageFont.truetype("tahoma.ttf",fontsize)
        w, h = draw.textsize(producto,font=fontp)
    draw.text(((img.width - w)/2,50*m),producto, (0,0,0), font=fontp)
    if(dun14 is not None and len(dun14) == 14 and lote.producto.unidades == unidad):
        fp = BytesIO()
        writer=ImageWriter()
        bar_class = barcode.get_barcode_class('code128')
        code128 = bar_class(dun14, writer)
        code128.write(fp, {"module_height":6.3*m, "module_width":0.2*m, "font_size": 5*m, "text_distance": 0.2*m*2, "quiet_zone": 1,})
        fp.seek(0)
        codigo = Image.open(fp)
        img.paste(codigo,( (img.width - codigo.width)//2 ,80*m))
    else:
        draw = ImageDraw.Draw(img)
        fontsize=58*m
        fontp = ImageFont.truetype("tahoma.ttf",fontsize)
        w, h = draw.textsize("CAJA ABIERTA",font=fontp)
        while w > img.width -20:
            print(fontsize)
            fontsize-=1
            fontp = ImageFont.truetype("tahoma.ttf",fontsize)
            w, h = draw.textsize("CAJA ABIERTA",font=fontp)
        draw.text(((img.width - w)/2,100*m),"CAJA ABIERTA", (0,0,0), font=fontp)
    draw = ImageDraw.Draw(img)
    if (sap is not None and len(sap) > 4):
        w, h = draw.textsize(sap,font=fonts)
        draw.text((img.width - w -10*m,230*m),sap, (0,0,0), font=fonts)
    w, h = draw.textsize(unidades,font=fontu)
    draw.text((img.width - w -10*m,190*m),unidades, (0,0,0), font=fontu)
    w, h = draw.textsize(fecha,font=fontf)
    draw.text((img.width - w -10*m,210*m),fecha, (0,0,0), font=fontf)
    qr = qrcode.QRCode(box_size=1,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(f"{lote.id} {i} {unidad}")
    codigo = qr.make_image(fill="black")
    codigo = codigo.resize((75*m,75*m))
    img.paste(codigo,(10*m,190*m))
    draw.text((20*m,185*m),"Código Interno", (0,0,0), font=fonti)
    pan = ImageReader(img)
    p.drawImage(pan,0,0,dimensiones[0]/m,dimensiones[1]/m,None,True)
    p.showPage()
    return
