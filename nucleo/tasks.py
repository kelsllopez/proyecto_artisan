from __future__ import absolute_import, unicode_literals
import requests
from bs4 import BeautifulSoup
# Renombramos el import de task
from celery import shared_task as celery_task
import datetime
from .models import Moneda
from time import sleep
from django.contrib.auth.models import User
from django.conf import settings
import re
# qr code
import qrcode
from io import BytesIO
import rsa
from PIL import Image, ImageFont, ImageDraw
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@celery_task(name='enviar_correo_task')
def enviar_correo_task(usuario_id, password, url):
    usuario = User.objects.filter(pk=usuario_id).first()
    if usuario:
        context = {
            'name': usuario.first_name + " " + usuario.last_name,
            'usuario': usuario.username,
            'contrasena': password,
            'pin': usuario.perfil.pin,
        }

        cifrado = rsa.encrypt(str(usuario.pk).encode(), settings.KEYS['publica']).hex()
        qr = qrcode.QRCode(box_size=10, border=3, error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(url)
        img = qr.make_image(fill_color="black", back_color="white")
        stream = BytesIO()
        font = ImageFont.truetype("arial.ttf", 15)
        draw = ImageDraw.Draw(img)
        nombre = usuario.first_name + " " + usuario.last_name
        draw.text((img.width * 0.8, img.height * 0.95), "{}".format(nombre.upper()), font=font)
        img.save(stream)

        email_subject = 'Bienvenido a Artisan'
        email_bodyt = render_to_string('nucleo/emails/registro.html', context)
        email_body = render_to_string('nucleo/emails/registro.html', context)
        email = EmailMultiAlternatives(email_subject,
                                       email_bodyt, settings.DEFAULT_FROM_EMAIL, [usuario.email, ])
        email.attach_alternative(email_body, "text/html")
        email.attach("qr.png", stream.getvalue(), 'image/png')
        email.send(fail_silently=False)
        return True


@celery_task
def obtenerPrecioEUR():
    url = 'https://si3.bcentral.cl/indicadoressiete/secure/Serie.aspx?gcode=PRE_EUR&param=cgBnAE8AOQBlAGcAIwBiAFUALQBsAEcAYgBOAEkASQBCAEcAegBFAFkAeABkADgASAA2AG8AdgB2AFMAUgBYADIAQwBzAEEARQBMAG8ASgBWADQATABrAGQAZAB1ADIAeQBBAFAAZwBhADIAbABWAHcAXwBXAGgATAAkAFIAVAB1AEIAbAB3AFoAdQBRAFgAZwA5AHgAdgAwACQATwBZADcAMwAuAGIARwBFAFIASwAuAHQA'
    request = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })
    contenido = BeautifulSoup(request.text, 'lxml')

    tds = contenido.findAll('td')
    ahora = datetime.datetime.now()
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    valores = {}
    for td in tds:
        span = td.find('span')
        if span is not None and span.text != '':
            id = span['id']
            mes = [mes for mes in meses if mes in id][0]
            dia = int(re.findall(r'\d{1,2}', id)[0]) - 1
            valor = float(span.text.replace(',', '.'))
            valores.setdefault(mes, {})[str(dia)] = valor

    mes = meses[ahora.month - 1]
    dia = list(valores[mes].keys())[-1]
    valor = valores[mes][dia]
    moneda = Moneda.objects.filter(nombre='EUR').first()
    moneda.valor = valor
    moneda.fecha = '{} {} {}'.format(dia, mes, ahora.year)
    moneda.save()
    return True


@celery_task
def obtenerPrecioUSD():
    url = 'https://si3.bcentral.cl/indicadoressiete/secure/Serie.aspx?gcode=PRE_TCO&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAdwA1ADQAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA='
    request = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })
    contenido = BeautifulSoup(request.text, 'lxml')

    tds = contenido.findAll('td')
    ahora = datetime.datetime.now()
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    valores = {}
    for td in tds:
        span = td.find('span')
        if span is not None and span.text != '':
            id = span['id']
            mes = [mes for mes in meses if mes in id][0]
            dia = int(re.findall(r'\d{1,2}', id)[0]) - 1
            valor = float(span.text.replace(',', '.'))
            valores.setdefault(mes, {})[str(dia)] = valor

    mes = meses[ahora.month - 1]
    dia = list(valores[mes].keys())[-1]
    valor = valores[mes][dia]
    moneda = Moneda.objects.filter(nombre='USD').first()
    moneda.valor = valor
    moneda.fecha = '{} {} {}'.format(dia, mes, ahora.year)
    moneda.save()
    return True
