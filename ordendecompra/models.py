from django.db import models
from proveedores.models import Proveedor,ProveedorInsumo
from nucleo.models import Insumo
import html2text
from inventario.models import Bodega,InventarioInsumo
from django.contrib.auth.models import User
from django.template import loader
from django.forms import model_to_dict
from inventario.tasks import enviar_email
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from simple_history.models import HistoricalRecords
import os
# Create your models here.

from django.contrib.auth.models import Permission

#Permission.__str__ = lambda self: '%s | %s' % (str(self.content_type).split('|')[1][1:].capitalize(), self.name)
class OrdenDeCompra(models.Model):
    proveedor = models.ForeignKey(Proveedor, verbose_name="Proovedor",on_delete=models.SET_NULL,null=True,related_name="proveedor")
    insumos = models.ManyToManyField(ProveedorInsumo, verbose_name="Insumos",through="OrdenDeCompraInsumo")
    bodega = models.ForeignKey(Bodega, verbose_name="Lugar",on_delete=models.SET_NULL,null=True,blank=True)
    pagada = models.BooleanField(verbose_name="Pagada",help_text="Si la orden de compra ha sido pagada.",default=False)
    numero = models.BigIntegerField(verbose_name="Numero",unique=True)
    condiciones = models.TextField(verbose_name="Condiciones",null=True,blank=True,default="Por favor incluir la siguiente glosa en la factura: DESARROLLO DE PORTAFOLIO DE POSTRES VEGETALES A BASE DE ALMENDRA Y DESECHOS DE SU PRODUCCIÓN”, código 19IR-LR-121872")
    estado = models.CharField(max_length=50,verbose_name="Estado", choices=[ ('Inicial','Inicial'),('Validada','Validada'),('Semi-Recepcionada','Semi-Recepcionada'),('Recepcionada','Recepcionada'),('Etiquetada', 'Etiquetada'),('Pagada','Pagada'),])
    fecha = models.DateField(verbose_name="Fecha de emisión")
    total_neto = models.FloatField(verbose_name="Total Neto",default=0)
    guia_despacho = models.CharField(verbose_name="Guia de despacho",blank=True,null=True,max_length=50)
    numero_factura = models.CharField(verbose_name="Numero de factura",blank=True,null=True,max_length=50)
    fecha_recepcion = models.DateField(verbose_name="Fecha de recepción",blank=True,null=True)
    fecha_facturacion = models.DateField(verbose_name="Fecha de documento",blank=True,null=True)
    fecha_pago =  models.DateField(verbose_name="Fecha de pago",blank=True,null=True)
    pago = models.CharField(max_length=100,verbose_name="Forma de pago",blank=True,null=True,choices=[ ('cheque','Cheque'),('deposito bancario','Depósito Bancario'),('transferencia','Transferencia Electrónica'),('efectivo','Efectivo'),('otra','Otra')])
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")
    history = HistoricalRecords()
    

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compra'
        ordering = ['numero']
        default_permissions = ()
        permissions = (
                        ('listar', 'Puede ver las ordenes de compra'),
                        ('crear', 'Puede crear una orden de compra'),
                        ('pdf', 'Permite generar el pdf de una orden de compra'),
                        ('recepcionar','Permite recepcionar una orden de compra'),
                        ('rechazar','Permite rechazar una orden de compra'),
                        ('validar','Permite validar una orden de compra'),
                        ('eliminar', 'Permite eliminar una orden de compra'),
                        ('pagar','Permite pagar una orden'),
                        ('eliminararchivo','Permite eliminar archivos asociados a las ordenes de compra'),
                        ('verarchivo','Permite ver los archivos adjuntos'),
                        ('dividir','Permite dividir un bulto de insumos')
                    )

    def __str__(self):
        return "Orden de compra {}".format(self.numero)

    def toJSON(self):
        dict = model_to_dict(self)
        dict['nombre_proveedor'] = self.proveedor.empresa_nombre
        return dict

    def totalNeto(self):
        total = 0
        insumos = self.ordendecomprainsumo_set.all()
        for insumo in insumos:
            total += insumo.cantidad*insumo.neto
        return total

    def iva(self):
        return self.totalNeto() * settings.IVA

    def total(self):
        return self.totalNeto() + self.iva()

    def obtenerBultos(self):
        # obtenemos los bultos
        bultosfinales = []
        bultos = self.insumobulto_set.all()
        for bulto in bultos:
            if len(bulto.padre.all()) > 0:
                continue
            bultosfinales.append(bulto)
        return bultosfinales

    def registros(self):
        registros = Registro.objects.filter(orden=self)
        return registros

    def ultimo_registro(self):
        registro = Registro.objects.filter(orden=self).exclude(estado='Rechazada').last()
        return registro

class Registro(models.Model):
    orden = models.ForeignKey(OrdenDeCompra,verbose_name="Orden de compra",on_delete=models.CASCADE)
    estado = models.CharField(max_length=255,verbose_name="Estado")
    empleado = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,related_name="empleado")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'Registro'
        default_permissions = ()
        verbose_name_plural = 'Registros'

    def __str__(self):
        return "Orden N° {}: a cambiado a {}".format(self.orden.numero,self.estado)

class Archivo(models.Model):
    orden = models.ForeignKey(OrdenDeCompra,verbose_name="Orden de compra",on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='ordendecompra/adjuntos',verbose_name="Archivos Adjuntos")

    def nombre(self):
        return self.archivo.url.split('/')[-1].capitalize()
    
    class Meta:
        default_permissions = ()
class OrdenDeCompraInsumo(models.Model):
    insumo = models.ForeignKey(ProveedorInsumo, verbose_name="Insumo", on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenDeCompra, verbose_name="Orden de compra", on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(verbose_name="Cantidad")
    cantidad_recibida = models.BigIntegerField(verbose_name="Cantidad Recibida", default=0)
    neto = models.FloatField(verbose_name="Valor Neto")
    moneda = models.FloatField(verbose_name="Moneda", default=0)
    conversion = models.FloatField(verbose_name="Conversion", blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        default_permissions = ()
        ordering = ['pk']

    def __str__(self):
        return "{} - {} ({})".format(self.orden,self.insumo,self.cantidad)
    
    def total(self):
        return (self.cantidad * self.neto)

""" class HistorialInsumo(models.Model):
    insumo = models.ForeignKey(Insumo,verbose_name="Insumo",on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor,verbose_name="Proveedor",on_delete=models.CASCADE)
    precio = models.IntegerField(verbose_name="Valor Neto")
    cantidad = models.IntegerField(verbose_name="Cantidad")

    class Meta:
        default_permissions = () """

@receiver(models.signals.post_delete, sender=Archivo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)

""" #Crear el historial de los insumos, para graficos o costeo de inventario
@receiver(models.signals.post_save,sender=OrdenDeCompraInsumo)
def auto_generar_historial(sender, instance, **kwargs):
    #si se esta creando
    if instance.created:
        insumo = instance.insumo.insumo
        proveedor = instance.insumo.proveedor
        precio = instance.neto
        cantidad = instance.cantidad
        historial = HistorialInsumo(insumo=insumo,proveedor=proveedor,precio=precio,cantidad=cantidad)
        historial.save() """

def textify(html):
    h = html2text.HTML2Text()

    # Don't Ignore links, they are useful inside emails
    h.ignore_links = False
    return h.handle(html)

#Enviar correos al momento de crear una orden de compra
@receiver(models.signals.post_save, sender=Registro)
def enviar_correo_inicial(sender, instance, **kwargs):
    if instance.created and instance.estado == 'Inicial':
        orden = instance.orden
        insumos = orden.ordendecomprainsumo_set.all()
        mensaje = "<table style='border-collapse: collapse;width: 100%;margin-top:10px;margin-bottom:10px;'><thead><tr><th style='border: 1px solid #ddd;padding:8px;padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #04AA6D;color: white;'>Insumo</td><th style='border: 1px solid #ddd;padding:8px;padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #04AA6D;color: white;'>Cantidad</th></tr></thead><tbody>"
        for i in insumos:
            mensaje += '<tr><td style="border: 1px solid #ddd;padding:8px;">{}</td><td style="border: 1px solid #ddd;padding:8px;">{} unidades</td></tr>'.format(i.insumo.insumo.nombre.capitalize(), i.cantidad)
        mensaje += '</tbody></table>'
        html_message = "Hola FLAX,<br>El empleado {} ha solicitado los siguientes insumos al proveedor <b>{}</b><br>".format((instance.empleado.first_name + " " + instance.empleado.last_name).upper(),orden.proveedor.empresa_nombre.upper()) + mensaje + "Si desea validar la orden de compra haga click<a href='{}'>aquí</a>".format(settings.EMAIL_WEB + reverse('ordendecompra:validar',args=[orden.id]))
        message = html_message.replace('<br>', '\n')
        subject="Orden de compra #{}".format(orden.numero)
        supervisores = orden.bodega.supervisorbodega_set.all()
        for s in supervisores:
            html_message = loader.render_to_string('nucleo/emails/correooc.html', {
                'user': s.supervisor,
                'empleado': instance.empleado,
                'insumos': insumos,
                'link': settings.EMAIL_WEB + reverse('ordendecompra:validar', args=[orden.id]),
            })
            enviar_email.delay(subject,html_message,message.replace('FLAX',f"{s.supervisor.first_name} {s.supervisor.last_name}"),s.supervisor.email)
        html_message = loader.render_to_string('nucleo/emails/correooc.html', {
                'user': None,
                'empleado': instance.empleado,
                'insumos': insumos,
                'link': settings.EMAIL_WEB + reverse('ordendecompra:validar', args=[orden.id]),
            })
        enviar_email.delay(subject,html_message,message.replace('FLAX',f"Administrador"),settings.EMAIL_ADMIN)
    if instance.estado in ['Semi-Recepcionada','Recepcionada']:
        orden = instance.orden
        insumos = orden.ordendecomprainsumo_set.all()
        cambio = False
        for insumo in insumos:
            if insumo.insumo.moneda.nombre == 'CLP':
                if insumo.insumo.precio/insumo.insumo.formato != insumo.neto/insumo.insumo.formato:
                    cambio = True
                    insumo.cambio = True
            else:
                insumo.cambio = False
        if(cambio):
            subject="Recepción OC #{} - CAMBIO VALOR NETO".format(orden.numero)
        else:
            subject="Recepción OC #{}".format(orden.numero)
        supervisores = orden.bodega.supervisorbodega_set.all()
        for s in supervisores:
            html_message = loader.render_to_string('nucleo/emails/recepcionaroc.html', {
                'user': s.supervisor,
                'empleado': instance.empleado,
                'insumos': insumos,
            })
            enviar_email.delay(subject,html_message,textify(html_message),s.supervisor.email)
        html_message = loader.render_to_string('nucleo/emails/recepcionaroc.html', {
                'user': None,
                'empleado': instance.empleado,
                'insumos': insumos,
            })
        enviar_email.delay(subject,html_message,textify(html_message),settings.EMAIL_ADMIN)



#Agregar la opción de valorizar bodega de insumos
def valorizar(self):
    inventario = InventarioInsumo.objects.filter(bodega=self).all()
    inventarioprecio = []
    total = 0
    for i in inventario:
        insumo = i.insumo
        #obtener el valor neto de la ultima orden de compra por ubicación
        ordendecomprainsumo = OrdenDeCompraInsumo.objects.filter(insumo__insumo=insumo).last()
        if ordendecomprainsumo:
            formato = ordendecomprainsumo.insumo.formato
            precio = ordendecomprainsumo.neto
            precioporunidad = round( (precio / formato),3)
            precioinventario = round(precioporunidad * i.cantidad,3)
            inventarioprecio.append( {'inventario':i,'precio': precioinventario,'preciou':precioporunidad})
            total+=precioinventario
        else:
            inventarioprecio.append( {'inventario':i,'precio': 0,'preciou':0})
    return total,inventarioprecio
Bodega.add_to_class('valorizar',valorizar)

        