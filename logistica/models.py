from django.db import models
from produccion.models import CajaLote
from inventario.models import Bodega, InventarioProducto, InsumoBulto, InventarioInsumo
from ventas.models import OrdenDeVenta
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User

class Envio(models.Model):
    lugar_o = models.ForeignKey(Bodega, verbose_name="Lugar de Origen", on_delete=models.CASCADE, related_name="origen")
    lugar_d = models.ForeignKey(Bodega, verbose_name="Lugar de Destino", on_delete=models.CASCADE, related_name="destino")
    fecha_envio = models.DateTimeField(verbose_name="Fecha de envio")
    fecha_recepcion = models.DateTimeField(verbose_name="Fecha de recepción", null=True)
    estado = models.BooleanField(verbose_name="Recepcionado", default=0)
    encargado_recepcion = models.ForeignKey(User, verbose_name="Encargado Recepción", null=True, default=None, on_delete=models.SET_NULL)
    encargado_envio = models.ForeignKey(User, verbose_name="Encargado Envio", null=True, default=None, on_delete=models.SET_NULL,related_name="encargado_envio")
    medio_transporte = models.CharField(max_length=255, verbose_name="Medio de Transporte")
    numero_documento = models.CharField(max_length=255, verbose_name="Número de documento")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'envio'
        ordering = ['-pk']
        verbose_name_plural = 'envios'
        permissions = (
                            ('envio.listar', 'Puede ver los envios'),
                            ('envio.detalle', 'Puede ver los detalles del envio'),
                            ('envio.crear', 'Puede crear un envio'),
                            ('envio.etiquetas','Puede ver las etiquetas del envio'),
                            ('envio.eliminar', 'Puede eliminar una envio'),
                            ('envio.actualizar', 'Puede actualizar un envio'),
        )

    def __str__(self):
        return "Envio {} - {}".format(self.lugar_o.nombre, self.lugar_d.nombre)

    def obtener_lotes(self):
        lotes = []
        loteenvios = self.loteenvio_set.all()
        for loteenvio in loteenvios:
            if loteenvio.cajalote.lote not in lotes:
                lotes.append(loteenvio.cajalote.lote)
        return lotes


class Pallet(models.Model):
    nombre = models.CharField(verbose_name="Nombre del Pallet", unique=True,max_length=255)
    lugar = models.ForeignKey(Bodega,on_delete=models.SET_NULL, null=True,verbose_name="Lugar")
    envio = models.ForeignKey(Envio,on_delete=models.SET_NULL, default=None,blank=True,verbose_name="Envio",null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'pallet'
        verbose_name_plural = 'pallets'
        permissions = (
                        ('pallet.listar', 'Puede ver los pallets'),
                        ('pallet.detalle','Puede ver el codigo de barra del pallet'),
                        ('pallet.crear', 'Puede agregar un pallet'),
                        ('pallet.eliminar', 'Puede eliminar un pallet'),
                        ('pallet.actualizar','Puede actualizar un pallet'),
        )
    
    def generarRegistro(self):
        self.registropallet_set.create(envio=self.envio)
    
    def finalizarRegistro(self, estado):
        registro = self.registropallet_set.last()
        registro.completado = estado
        registro.save()


class RegistroPallet(models.Model):
    pallet = models.ForeignKey(Pallet, verbose_name="pallet", on_delete=models.CASCADE)
    envio = models.ForeignKey(Envio, verbose_name="envio", on_delete=models.CASCADE)
    completado = models.BooleanField(default=False, verbose_name="completado")

    class Meta:
        default_permissions = ()
        verbose_name = 'registro pallet'
        verbose_name_plural = 'registro pallets'


class InsumoEnvio(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, default=None, null=True)
    insumobulto = models.ForeignKey(InsumoBulto, on_delete=models.CASCADE)
    recepcionado = models.BooleanField(default=None, verbose_name="Recepcionado", null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'envio insumo bulto'
        verbose_name_plural = 'envios insumo bulto'

    def manejarinventario(self, lugar, accion):
        inventario = InventarioInsumo.objects.filter(insumo=self.insumobulto.insumo, bodega=lugar).first()
        if inventario:
            if accion == 'sumar':
                inventario.cantidad += self.insumobulto.total()
            else:
                inventario.cantidad -= self.insumobulto.total()
            inventario.save()

class LoteEnvio(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, default=None, null=True)
    cajalote = models.ForeignKey(CajaLote, verbose_name="Caja Lote", on_delete=models.CASCADE)
    recepcionado = models.BooleanField(default=None, verbose_name="Recepcionado", null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'envio lote'
        verbose_name_plural = 'envios lote'

    def recepcionar(self):
        self.recepcionado = True
        producto = self.cajalote.lote.producto
        lugar = self.envio.lugar_d
        inventario = InventarioProducto.objects.filter(producto=producto, bodega=lugar).first()
        inventario.cantidad += self.cajalote.cantidad
        inventario.save()
        self.cajalote.lugar = lugar
        self.cajalote.estado = 'Recepcionado'
        self.cajalote.save()
        self.save()

    def manejarinventario(self, lugar, accion):
        producto = self.cajalote.lote.producto
        inventario = InventarioProducto.objects.filter(producto=producto, bodega=lugar).first()
        if inventario:
            if accion == 'sumar':
                inventario.cantidad += self.cajalote.cantidad
            else:
                inventario.cantidad -= self.cajalote.cantidad
            inventario.save()


class Ruta(models.Model):
    nombre = models.CharField(verbose_name="Nombre de la ruta", max_length=255)
    persona = models.ForeignKey(User, verbose_name="Transportista", on_delete=models.CASCADE)
    estado = models.CharField(verbose_name="Estado",max_length=255,choices=(('Abierto','Abierto'),('Cerrado','Cerrado')),default="Abierto")
    patente = models.CharField(verbose_name="Patente del Vehiculo",default="",blank=True,max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'ruta'
        ordering = ['-pk']
        verbose_name_plural = 'rutas'
        unique_together = ['nombre', 'persona']
        permissions = (
            ('rutas.listar', 'Puede ver las rutas'),
            ('rutas.misrutas', 'Puede ver las rutas asignadas'),
            ('rutas.detalle', 'Puede ver el detalle de la ruta'),
            ('rutas.crear', 'Puede crear una ruta'),
            ('rutas.cerrar', 'Puede cerrar una ruta'),
            ('rutas.eliminar', 'Puede eliminar una ruta'),
            ('rutas.actualizar', 'Puede actualizar una ruta'),
        )


class RutaOv(models.Model):
    ruta = models.ForeignKey(Ruta, verbose_name="Ruta", on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenDeVenta, verbose_name="Orden de Venta", on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()
        verbose_name = 'rutas orden deventa'
        ordering = ['-pk']
        verbose_name_plural = 'rutas orden deventa'

@receiver(models.signals.pre_delete, sender=InsumoEnvio)
def arreglar_inventarioinsumo(sender, instance, **kwargs):
    if instance.recepcionado:
        instance.manejarinventario(instance.envio.lugar_o, "sumar")
        instance.manejarinventario(instance.envio.lugar_d, "restar")
    else:
        instance.manejarinventario(instance.envio.lugar_o, "sumar")
    bulto = instance.insumobulto
    bulto.bodega = instance.envio.lugar_o
    bulto.save()

@receiver(models.signals.pre_delete, sender=LoteEnvio)
def arreglar_inventario(sender, instance, **kwargs):
    if instance.recepcionado:
        instance.manejarinventario(instance.envio.lugar_o, "sumar")
        instance.manejarinventario(instance.envio.lugar_d, "restar")
    else:
        instance.manejarinventario(instance.envio.lugar_o, "sumar")

@receiver(models.signals.post_delete, sender=LoteEnvio)
def eliminar_estado(sender,instance,**kwargs):
    instance.cajalote.lugar = instance.envio.lugar_o
    instance.cajalote.save()
    lote = instance.cajalote.lote
    cajas = lote.cajalote_set.all()
    loteenvios = [caja.loteenvio_set.first() for caja in cajas if caja.loteenvio_set.first() is not None]
    cantidad = len(loteenvios)
    if cantidad == 0:
        estado = lote.estadolote_set.filter(nombre="En Transito").first()
        if estado == lote.estadolote_set.last():
            lote.estadolote_set.remove(estado)
    if cantidad < len(lote.cajas()):
        estado = lote.estadolote_set.filter(nombre="Recepcionado").first()
        if estado == lote.estadolote_set.last():
            lote.estadolote_set.remove(estado)

@receiver(models.signals.post_save,sender=LoteEnvio)
def restar_inventario(sender,instance,created,**kwargs):
    if created:
        instance.manejarinventario(instance.envio.lugar_o,"restar")

