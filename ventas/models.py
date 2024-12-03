from tabnanny import verbose
from django.contrib.auth.models import User
from django.db import models
from produccion.models import CajaLote
from clientes.models import Cliente, ClienteLocal
from inventario.models import Bodega,InventarioProducto
import os
from django.dispatch import receiver
from django.conf import settings
from django.core import validators
from nucleo.models import Producto

# Modelos de Ventas


class ListaPrecio(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre de Lista de Precios")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Lista de Precios"
        verbose_name_plural = "Listas de Precios"
        ordering = ['nombre']
        default_permissions = ()
        permissions = (
            ('listap.listar', 'Puede ver el listado de los locales'),
            ('listap.crear', 'Puede crear un local'),
            ('listap.eliminar', 'Permite eliminar un local'),
            ('listap.actualizar', 'Permite actualizar un local'),
            ('listap.detalle', 'Permite ver el detalle de un local')
        )

    def __str__(self):
        return self.nombre


class ListaPrecioProducto(models.Model):
    lista = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE, verbose_name="Lista Asociada")
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE, related_name="listaproductos")
    precio = models.FloatField(verbose_name="Precio")

    class Meta:
        verbose_name = "Producto Lista de Precios"
        verbose_name_plural = "Productos Listas de Precios"
        ordering = ['producto__nombre']
        default_permissions = ()
        unique_together = [['lista', 'producto']]


class OrdenDeVenta(models.Model):
    lugar = models.ForeignKey(Bodega, verbose_name="Lugar", on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=255, choices=(('Pendiente', 'Pendiente'), ('Pickeado', 'Pickeado'), ('Facturado', 'Facturado'), ('Asignado', 'Asignado')), default='Pendiente')
    local = models.ForeignKey(ClienteLocal, verbose_name="Local", on_delete=models.SET_NULL, null=True)
    complitud = models.FloatField(verbose_name="Nivel de servicio", default=0)
    fecha = models.DateField(verbose_name="Fecha creación orden de Venta")
    fecha_f = models.DateField(verbose_name="Fecha factura ov", null=True, default=None)
    fecha_e = models.DateTimeField(verbose_name="Fecha de entrega", default=None, blank=True, null=True)
    entregado = models.ForeignKey(User, verbose_name="Encargado de Entrega", on_delete=models.CASCADE, default=None, blank=True, null=True)
    condiciones = models.TextField(verbose_name="Condiciones", null=True, blank=True)
    n_orden_cliente = models.CharField(verbose_name="Número orden de compra cliente", max_length=255, blank=True)
    envio = models.FloatField(verbose_name="Costo de Envio", default=0, validators=[validators.MinValueValidator(0)])

    class Meta:
        verbose_name = 'Orden de Venta'
        verbose_name_plural = 'Ordenes de Venta'
        default_permissions = ()
        ordering = ['-pk']
        permissions = (
            ('orden.listar', 'Puede ver el listado de las ordenes de venta'),
            ('orden.pickear', 'Permite realizar el pickeo de la orden'),
            ('orden.crear', 'Puede crear una orden de venta'),
            ('orden.abrir', 'Puede abrir cajas'),
            ('orden.retroceder', 'Puede retroceder la orden'),
            ('orden.excel', 'Puede exportar las ov en formato excel'),
            ('orden.entregar', 'Puede entregar una orden de venta'),
            ('orden.eliminar', 'Permite eliminar una orden de venta'),
            ('orden.actualizar', 'Permite actualizar una orden de venta'),
            ('orden.detalle', 'Permite ver el detalle de una orden de venta')
        )

    def totalNeto(self):
        total = 0
        productos = self.ordendeventaproducto_set.all()
        for p in productos:
            total += p.totalNeto()
        return total
    
    def totalDescuento(self):
        total = 0
        productos = self.ordendeventaproducto_set.all()
        for p in productos:
            total += p.totalDescuento()
        return total
    
    def get_facturas(self):
        facturas = []
        for p in self.ordendeventaproducto_set.all():
            if p.factura != "" and p.factura not in facturas:
                facturas.append(p.factura)
        return facturas
    
    def calcularComplitud(self):
        productos = self.ordendeventaproducto_set.all()
        unidades = 0
        unidadesi = 0
        for p in productos:
            pendientes = OrdenDeVentaProducto.objects.filter(orden__pk__lte=int(self.pk),orden__lugar=self.lugar, producto=p.producto, orden__estado='Pendiente').exclude(orden__pk=int(self.pk)).all()
            inventario, created = InventarioProducto.objects.get_or_create(bodega=self.lugar, producto=p.producto, defaults={'cantidad': 0}) 
            for pe in pendientes:
                inventario.cantidad -= pe.cantidad
            ci = inventario.cantidad
            if inventario.cantidad > 0:
                if inventario.cantidad > p.cantidad:
                    unidadesi += p.cantidad
                else:
                    unidadesi += inventario.cantidad
            unidades+=p.cantidad
        porcentaje = 0
        try:
           porcentaje = round( (unidadesi/unidades) *100,2)
        except Exception as ex:
            porcentaje = 0
        return porcentaje

    def iva(self):
        return (self.totalNeto() - self.totalDescuento()) * settings.IVA

    def total(self):
        return self.totalNeto() + self.iva() + self.envio - self.totalDescuento()


class OrdenDeVentaProducto(models.Model):
    orden = models.ForeignKey(OrdenDeVenta, verbose_name="Orden de venta", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="producto", on_delete=models.CASCADE, related_name="productos")
    codigo_cliente = models.CharField(verbose_name="Codigo Cliente", default=None, blank=True, max_length=255)
    cantidad = models.BigIntegerField(verbose_name="Cantidad")
    cantidad_fc = models.BigIntegerField(verbose_name="Cantidad Facturada", default=0)
    factura = models.CharField(verbose_name="N° Factura", max_length=255, blank=True, default="")
    precio = models.FloatField(verbose_name="Precio")
    descuento = models.FloatField(verbose_name="Descuento",default=0)
    cantidad_en = models.BigIntegerField(verbose_name="Cantidad Entregada", default=0)

    class Meta:
        verbose_name = 'Producto Orden de Venta'
        verbose_name_plural = 'Productos Orden de Venta'
        default_permissions = ()

    def totalNeto(self):
        if self.orden.estado == 'Recepción Parcial':
            return self.cantidad_en * self.precio
        if self.cantidad_fc == 0:
            return self.cantidad * self.precio
        else:
            return self.cantidad_fc * self.precio

    def totalDescuento(self):
        if self.orden.estado == 'Recepción Parcial':
            return self.cantidad_en * self.descuento/100*self.precio
        if self.cantidad_fc == 0:
            return self.cantidad * self.descuento/100*self.precio
        else:
            return self.cantidad_fc * self.descuento/100*self.precio

    def iva(self):
        return (self.totalNeto() - self.totalDescuento()) * settings.IVA

    def total(self):
        return self.totalNeto() + self.iva() - self.totalDescuento()


class OrdenDeVentaCajaLote(models.Model):
    orden = models.ForeignKey(OrdenDeVenta, verbose_name="Orden de venta", on_delete=models.CASCADE)
    caja = models.ForeignKey(CajaLote, verbose_name="Caja lote", on_delete=models.CASCADE)
    cerrada = models.BooleanField(verbose_name="Estado Caja",default=True)
    cantidad = models.IntegerField(verbose_name="Cantidad",default=0)

    class Meta:
        verbose_name = 'Cajas OV'
        verbose_name_plural = 'CAJAS OV'
        default_permissions = ()


class ArchivoOrdenDeVenta(models.Model):
    orden = models.ForeignKey(OrdenDeVenta, verbose_name="Orden de venta", on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='ordendeventa/adjuntos', verbose_name="Archivos Adjuntos")

    def nombre(self):
        return self.archivo.url.split('/')[-1].capitalize()

    class Meta:
        default_permissions = ()
        permissions = (
            ('archivo.listar', 'Puede ver archivos adjuntos ov'),
            ('archivo.crear', 'Puede agregar un archivo a ov'),
            ('archivo.eliminar', 'Permite eliminar un archivo adjunto ov'),
        )

# calcular complitud pre save
@receiver(models.signals.pre_save, sender=OrdenDeVenta)
def calcularComplitud(sender,instance,**kwargs):
    if instance.estado == 'Pendiente':
        print('entramos!')
        instance.complitud = instance.calcularComplitud()
        print(instance.complitud)


# eliminación automatica de archivos
@receiver(models.signals.post_delete, sender=ArchivoOrdenDeVenta)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Entramos')
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)
