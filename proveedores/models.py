from django.db import models
from nucleo.models import Insumo,Moneda
from django.conf import settings
# Create your models here.



class Proveedor(models.Model):
    # datos empresa
    empresa_nombre = models.CharField(max_length=255,verbose_name="Razón Social")
    empresa_rut = models.CharField(max_length=50,verbose_name="Rut Empresa",unique=True)
    empresa_giro = models.CharField(max_length=100,verbose_name="Giro Empresa",null=True,blank=True)
    empresa_region = models.CharField(max_length=255,verbose_name="Región",null=True,blank=True,choices=settings.REGIONES)
    empresa_comuna = models.CharField(max_length=255,verbose_name="Comuna",null=True,blank=True)
    empresa_direccion = models.CharField(max_length=255,verbose_name="Dirección Empresa",null=True,blank=True)
    # datos de venta
    ventas_nombre = models.CharField(max_length=255,verbose_name="Nombre Contacto Comercial",null=True,blank=True)
    ventas_email = models.EmailField(max_length=255,verbose_name="Correo Electrónico Contacto Comercial")
    ventas_celular = models.CharField(max_length=255,verbose_name="Celular Contacto Comercial",null=True,blank=True)
    # datos de banco
    cuenta_corriente = models.CharField(max_length=255,verbose_name="Número de cuenta corriente",null=True,blank=True)
    banco = models.CharField(max_length=255,verbose_name="Banco",choices=settings.LISTA_BANCOS,null=True,blank=True)
    transferencia_email = models.EmailField(max_length=255,verbose_name="Correo Electrónico Transferencias",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'proovedor'
        verbose_name_plural = 'proveedores'
        ordering = ['-created']
        default_permissions = ()
        permissions = (
            ('listar', 'Puede ver el listado de los proveedores'),
            ('crear', 'Puede crear un proveedor'),
            ('eliminar', 'Permite eliminar un proveedor'),
            ('actualizar', 'Permite actualizar un proveedor'),
            ('detalle', 'Permite ver el detalle de un proveedor')
        )

    def __str__(self):
        return self.empresa_rut + " - " + self.empresa_nombre

    def insumos(self):
        insumos = ProveedorInsumo.objects.filter(proveedor=self).all()
        return insumos


class ProveedorInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, verbose_name="insumo", on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, verbose_name="proveedor", on_delete=models.CASCADE)
    nombre_insumo = models.CharField(max_length=255, verbose_name="Nombre Insumo en ficha tecnica proveedor")
    formato = models.FloatField(verbose_name="Formato De Compra")
    moneda = models.ForeignKey(Moneda, verbose_name="Vincular a este precio", default=None, null=True, on_delete=models.SET_NULL)
    precio = models.FloatField(verbose_name="Precio")
    lead = models.IntegerField(verbose_name="Lead Time", default=15)
    mostrar = models.BooleanField(verbose_name="Mostrar", default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'Asociación Proveedor Insumo'
        default_permissions = ()
        verbose_name_plural = 'Asociaciones Proveedores Insumos'
        ordering = ['-created']
        default_permissions = ()
        permissions = (
            ('insumo.listar', 'Puede ver el listado de las asociaciones'),
            ('insumo.crear', 'Puede crear una asociación'),
            ('insumo.actualizar', 'Puede actualizar una asociación'),
            ('insumo.eliminar', 'Puede eliminar una asociación')
        )

    def __str__(self):
        return self.insumo.nombre + " " + self.proveedor.empresa_nombre

    def getValor(self):
        return round((self.precio * self.moneda.valor), 2)
