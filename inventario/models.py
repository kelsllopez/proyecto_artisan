from django.db import models
from django.utils import safestring
from django.shortcuts import reverse
from inventario.tasks import enviar_email
from nucleo.models import Insumo, Producto
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from django.db.models import F
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

import traceback


# Create your models here.
class Bodega(models.Model):
    nombre = models.CharField(max_length=255,verbose_name="Ubicación de la bodega", unique=True)

    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "bodega"
        verbose_name_plural = "bodegas"
        ordering = ["-id"]
        default_permissions = ()
        permissions = (
                        ('bodega.listar', 'Puede ver el listado de las bodegas'),
                        ('bodega.crear', 'Puede crear una bodega'),
                        ('bodega.eliminar', 'Permite eliminar una bodega'),
                        ('bodega.actualizar','Permite actualizar una bodega'),
                        ('bodega.valorizar','Permite valorizar la bodega')
                    )
    
    def __str__(self):
        return self.nombre.upper()

class SupervisorBodega(models.Model):
    supervisor = models.ForeignKey(User, verbose_name="Supervisor de Planta", default=None, null=True, on_delete=models.SET_NULL)
    bodega = models.ForeignKey(Bodega, verbose_name="Bodega", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "supervisor bodega"
        verbose_name_plural = "supervisor bodegas"
        ordering = ["-id"]
        default_permissions = ()

class HistorialBodega(models.Model):
    bodega = models.ForeignKey(Bodega, verbose_name="Bodega", on_delete=models.CASCADE)
    manual = models.BooleanField(verbose_name="Historial Manual",default=False)
    fecha = models.DateTimeField(verbose_name="Fecha de Historial")

    class Meta:
        verbose_name = "historial bodega"
        verbose_name_plural = "historial bodegas"
        ordering = ["-id"]
        default_permissions = ()
        permissions = (
            ('historial.listar', 'Puede ver el listado de los historiales de bodega'),
            ('historial.crear', 'Puede crear un historial de bodega'),
        )
    

    def totali(self):
        total = 0
        insumos = self.historialbodegainsumo_set.all()
        for i in insumos:
            total+=i.precio_global()
        return total

    def __str__(self):
        return f"{self.bodega.nombre} {self.fecha}"
    

class HistorialBodegaProducto(models.Model):
    historialbodega = models.ForeignKey(HistorialBodega,verbose_name="Bodega",on_delete=models.CASCADE,null=True,default=None)
    producto = models.ForeignKey(Producto,verbose_name="Producto",on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(verbose_name="Cantidad")
    precio = models.FloatField(verbose_name="Precio del producto a la fecha")
    class Meta:
        verbose_name = "historial bodega producto"
        verbose_name_plural = "historial bodega productos"
        ordering = ["-id"]
        default_permissions = ()

class HistorialBodegaInsumo(models.Model):
    historialbodega = models.ForeignKey(HistorialBodega,verbose_name="Bodega",on_delete=models.CASCADE,null=True,default=None)
    insumo = models.ForeignKey(Insumo,verbose_name="Insumo",on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(verbose_name="Cantidad")
    precio = models.FloatField(verbose_name="Precio del insumo a la fecha")
    class Meta:
        verbose_name = "historial insumo"
        verbose_name_plural = "historial insumo"
        ordering = ["insumo__nombre"]
        default_permissions = ()
    
    def precio_global(self):
        if self.cantidad > 0:
            return round(self.precio * self.cantidad,2)
        else:
            return 0
    
    def precio_unidad(self):
        if self.cantidad > 0:
            return round( (self.precio),2)
        else:
            return 0

class InventarioProducto(models.Model):
    bodega = models.ForeignKey(Bodega, verbose_name="bodega",on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Producto",on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(verbose_name="Cantidad")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "inventario Producto"
        verbose_name_plural = "inventario Productos"
        ordering = ['producto__nombre']
        unique_together = ['bodega', 'producto']
        default_permissions = ()
        permissions = (
                        ('inventariop.listar', 'Puede ver el listado de los productos'),
                        ('inventariop.actualizar','Permite actualizar un producto'),
                        ('inventariop.global','Permite el listado de los productos globales')
                    )
    
    def __str__(self):
        return self.producto.nombre
    
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('bodega', 'producto'):
            inventario_producto = InventarioProducto.objects.filter(bodega=self.bodega, producto=self.producto).get()
            return safestring.mark_safe('Lo sentimos, ya existe <b>{}</b> asociado al bodega <b>{}</b> Si deseas editar ese inventario haz click <a style="font-weight:700" href="{}">aquí</a>'.format(self.producto, self.bodega,reverse('admin:inventario_inventarioproducto_change',args=(inventario_producto.id,))))
        else:
            return super(InventarioProducto, self).unique_error_message(model_class, unique_check)
    

class InventarioInsumo(models.Model):
    bodega = models.ForeignKey(Bodega, verbose_name="Bodega", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    estado = models.CharField(verbose_name="Estado", default="Bien", max_length=20)
    cantidad = models.FloatField(verbose_name="Cantidad")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Inventario Insumo"
        verbose_name_plural = "Inventarios Insumos"
        ordering = ['insumo__nombre']
        unique_together = ['bodega', 'insumo']
        default_permissions = ()
        permissions = (
            ('inventarioi.listar', 'Puede ver el listado de los insumos'),
            ('inventarioi.global', 'Puede ver el listado de los insumos globales'),
            ('inventarioi.actualizar', 'Permite actualizar un insumo'),
        )

    def __str__(self):
        return f"{self.insumo.nombre} - {self.bodega.nombre}"

    def obtener_transito(self):
        cantidad = 0
        transito = InsumoBulto.objects.filter(bodega=None,insumo=self.insumo).all()
        for t in transito:
            cantidad+= t.cantidad * t.formato
        return cantidad

    def valorizar(self):
        # sacamos las ordenes de compra del insumo actuales
        if (self.insumo.pip):
            insumo = self.insumo
            lugar = self.bodega
            # buscar todas las elaboraciones donde se haya producido este insumo PIP

            print(insumo)
            print(lugar)

 #           producciones = InsumoProcesoProduccion.objects.filter(pauta_produccion = lugar, plantilla_ip = insumo).order_by('-')

            producciones = apps.get_model(app_label='produccion', model_name='insumoprocesoproduccion').objects.filter(pauta_produccion__lugar=lugar, plantilla_ip__insumo=insumo).order_by('-id').all()
            precios = 0
            total = 0

            for p in producciones:
                print(p)
                cdp = p.pauta_produccion.cdp

                if(p.cantidad > 0):

                    precios += ((p.cantidad - p.cantidadu) * cdp/p.cantidad)
    
                total += (p.cantidad - p.cantidadu)

            try:
                pu = 0
                if(total > 0):
                    pu = precios/total

                return pu
            except Exception as ex:
                traceback.print_exc()
                print(ex)
                return 0
        else:
            precio = 0
            cantidad = self.cantidad
            total = self.cantidad
            ordendecomprainsumo = apps.get_model('ordendecompra.ordendecomprainsumo')
            if cantidad > 0:
                insumo = self.insumo
                revisadas = []
                while cantidad > 0:
                    ultima = ordendecomprainsumo.objects.filter(insumo__insumo=insumo).exclude(id__in=revisadas).order_by('id').last()
                    if ultima:
                        revisadas.append(ultima.pk)
                        diferencia = cantidad - ultima.cantidad*ultima.insumo.formato
                        pu = ultima.neto/ultima.insumo.formato
                        if diferencia >= 0:
                            cantidad=diferencia
                            precio+= ultima.cantidad*ultima.insumo.formato * pu
                        else:
                            precio+= cantidad * pu
                            cantidad = 0
                    else:
                        cantidad = 0
                if total > 0:
                    return precio/total
                else:
                    return precio
            else:
                insumo = self.insumo
                # obtenemos la ultima orden de compra
                orden = ordendecomprainsumo.objects.filter(insumo__insumo=insumo).order_by('id').last()
                if (orden):
                    if orden.insumo.formato <= 0:
                        orden.insumo.formato = 1
                    pu = orden.neto/orden.insumo.formato
                    return pu
            return 0


    @classmethod
    def obtener_o_crear(cls, bodega_id, insumo_id, cantidad):
        try:
            bodega = Bodega.objects.get(id=bodega_id)
            insumo = Insumo.objects.get(id=insumo_id)
        except ObjectDoesNotExist:
            raise ValueError("Bodega o Insumo no encontrado.")

        inventario_insumo, created = cls.objects.get_or_create(
            bodega=bodega,
            insumo=insumo,
            defaults={'cantidad': cantidad}
        )
        
        if not created:
            inventario_insumo.cantidad += cantidad  # Actualiza la cantidad si ya existe
            inventario_insumo.save()
        
        return inventario_insumo

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('bodega', 'insumo'):
            inventario_insumo = InventarioInsumo.objects.get(bodega=self.bodega, insumo=self.insumo)
            return safestring.mark_safe(
                'Lo sentimos, ya existe <b>{}</b> asociado a la bodega <b>{}</b>. Si deseas editar ese inventario, haz clic <a style="font-weight:700" href="{}">aquí</a>'.format(
                    self.insumo, self.bodega, reverse('admin:inventario_inventarioinsumo_change', args=(inventario_insumo.id,))
                )
            )
        return super(InventarioInsumo, self).unique_error_message(model_class, unique_check)


class InsumoBulto(models.Model):
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.SET_NULL, null=True)
    ordendecompra = models.ForeignKey('ordendecompra.OrdenDeCompra', verbose_name="Orden de compra asociada", on_delete=models.SET_NULL, null=True)
    bodega = models.ForeignKey(Bodega, verbose_name="bodega", on_delete=models.SET_NULL, null=True)
    lotep = models.CharField(max_length=255,verbose_name="Lote Proveedor",default="",blank=True)
    cantidad = models.FloatField(verbose_name="Cantidad de unidades en el bulto")
    cantidadu = models.FloatField(verbose_name="Cantidad de unidades utilizadas",default=0)
    formato = models.FloatField(verbose_name="Formato", default=0)
    formatoo = models.FloatField(verbose_name="Formato Original", default=1)
    numero = models.IntegerField(verbose_name="Número bulto")
    default_permissions = ()

    def disponible(self):
        return self.cantidad - self.cantidadu

    def generarNumero(self):
        # buscamos el ultimo insumo
        ultimo_insumo = InsumoBulto.objects.filter(insumo=self.insumo).exclude(pk=self.pk).last()
        if ultimo_insumo:
            numero = ultimo_insumo.numero+1
        else:
            numero = 1
        return numero
   
    def total(self):
        return round(self.cantidad * self.formato,2)

    def enviar(self):
        ii, created = InventarioInsumo.objects.get_or_create(insumo=self.insumo, bodega=self.bodega, defaults={'cantidad': 0})
        if ii:
            self.bodega = None
            ii.cantidad -= self.cantidad * self.formato
            ii.save()
            self.save()

    def recepcionar(self, bodega):
        ii, created = InventarioInsumo.objects.get_or_create(insumo=self.insumo, bodega=bodega, defaults={'cantidad': 0})
        if ii:
            self.bodega = bodega
            ii.cantidad += self.cantidad * self.formato
            ii.save()
            self.save()

    def cancelar(self, bodega):
        ii, created = InventarioInsumo.objects.get_or_create(insumo=self.insumo, bodega=bodega, defaults={'cantidad': 0})
        if ii:
            self.bodega = bodega
            ii.cantidad += self.cantidad * self.formato
            ii.save()
            self.save()
    # metodo personalizado de guardado para generar el codigo
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.numero = self.generarNumero()
        super(InsumoBulto, self).save(*args, **kwargs)

class InsumoBultoHijo(models.Model):
    insumobultopadre = models.ForeignKey(InsumoBulto, on_delete=models.CASCADE, verbose_name="Bulto Padre",related_name="padre")
    insumobultohijo = models.ForeignKey(InsumoBulto, on_delete=models.CASCADE, verbose_name="Bulto Hijo",related_name="hijo")

    class Meta:
        verbose_name = 'Insumo Bulto Hijo'
        verbose_name_plural = 'Insumo Bulto Hijos'
        default_permissions = ()

#Actualizar el estado del insumo al momento de guardar
@receiver(models.signals.pre_save, sender=InventarioInsumo)
def actualizar_estado_insumo(sender,instance,**kwargs):
    stock_critico = instance.insumo.stock_critico
    if instance.cantidad <= stock_critico:
        instance.estado = 'Peligro'
    else:
        instance.estado = 'Bien'

#enviar correo de stock critico
@receiver(models.signals.post_save, sender=InventarioInsumo)
def enviar_correo_stock_critico(sender,instance,**kwargs):
    if instance.estado == 'Peligro':
        inventario_insumo = instance
        insumo = inventario_insumo.insumo
        html_message = "Hola,<br>recientemente se actualizo el stock del insumo <b>{}</b> en la bodega de <b>{}</b>, dejandolo en estado <b style='color:red'>CRÍTICO</b>".format(insumo.nombre,inventario_insumo.bodega.nombre)
        message = "Hola,\nrecienemente se actualizo el stock del insumo {} en la bodega de {}, dejandolo en estado CRÍTICO".format(insumo.nombre,inventario_insumo.bodega.nombre)
        subject="Stock Crítico en insumo: {} - {}".format(insumo.nombre,inventario_insumo.bodega.nombre),
        try:
            enviar_email.delay(subject, html_message, message, "katalinagatita7520@gmail.com")
        except Exception as e:
            print(f"Error al enviar correo: {e}")
#actualizar permisos al momento de actualizar
@receiver(models.signals.pre_save,sender=Bodega)
def actualizar_permisos(sender,instance,**kwargs):
    bodega = Bodega.objects.filter(pk=instance.id).first()
    if bodega:
        nombre = bodega.nombre.lower().replace(' ','-')
        nombre_nuevo = instance.nombre.lower().replace(' ','-')
        if(nombre != nombre_nuevo):
            permisoi = Permission.objects.filter(codename='inventarioi_{}'.format(nombre)).first()
            if permisoi:
                permisoi.codename='inventarioi_{}'.format(nombre_nuevo)
                permisoi.name = 'Inventario Insumos - {}'.format(instance.nombre)
                permisoi.save()
            permisop = Permission.objects.filter(codename='inventariop_{}'.format(nombre)).first()
            if permisop:
                permisop.codename='inventariop_{}'.format(nombre_nuevo)
                permisop.name = 'Inventario Productos - {}'.format(instance.nombre)
                permisop.save()

#crear permisos al momento de crear una nueva bodega
@receiver(models.signals.post_save,sender=Bodega)
def crear_permisos(sender,instance,**kwargs):
    nombre = instance.nombre.lower().replace(' ','-')
    if instance.created:
        content_type = ContentType.objects.get_for_model(instance)
        Permission.objects.get_or_create(
            codename='inventarioi_{}'.format(nombre),
            name='Inventario Insumos - {}'.format(instance.nombre),
            content_type=content_type,
        )
        Permission.objects.get_or_create(
            codename='inventariop_{}'.format(nombre),
            name='Inventario Productos - {}'.format(instance.nombre),
            content_type=content_type,
        )

#eliminar permisos al momento de borrar una bodega
@receiver(models.signals.post_delete,sender=Bodega)
def eliminar_permiso(sender,instance,**kwargs):
    nombre = instance.nombre.lower().replace(' ','-')
    permisoi = Permission.objects.filter(codename='inventarioi_{}'.format(nombre)).first()
    if permisoi:
        permisoi.delete()
    permisop = Permission.objects.filter(codename='inventariop_{}'.format(nombre)).first()
    if permisop:
        permisop.delete()
