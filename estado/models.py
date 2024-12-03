from django.db import models
from nucleo.models import Insumo, Producto
# Create your models here.


class ConjuntoEstado(models.Model):
    nombre = models.CharField(verbose_name="Nombre Conjunto", max_length=255)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'conjunto'
        ordering = ['-pk']
        verbose_name_plural = 'conjuntos'
        permissions = (
            ('conjuto.listar', 'Puede ver los conjuntos'),
            ('conjuto.detalle', 'Puede ver los detalles del conjunto'),
            ('conjuto.crear', 'Puede crear un conjunto'),
            ('conjuto.eliminar', 'Puede eliminar un conjunto'),
            ('conjuto.actualizar', 'Puede actualizar un conjunto'),
        )
    
    def __str__(self) -> str:
        return self.nombre.upper()


class Estado(models.Model):
    nombre = models.CharField(verbose_name="Nombre Estado", max_length=255)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    peso = models.BooleanField(verbose_name="Pedir Peso", default=False)
    uc = models.BooleanField(verbose_name="Pedir Unidades Para Calidad", default=False)
    uff = models.BooleanField(verbose_name="Pedir Unidades Fuera de Formato", default=False)
    unc = models.BooleanField(verbose_name="Pedir Unidades No Consumibles", default=False)

    class Meta:
        default_permissions = ()

    def __str__(self) -> str:
        return self.nombre.upper()

class EstadoConjunto(models.Model):
    conjunto = models.ForeignKey(ConjuntoEstado, on_delete=models.CASCADE, verbose_name="Conjunto")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")
    pos = models.IntegerField(verbose_name="Posicion")

    class Meta:
        default_permissions = ()
        unique_together = [['conjunto', 'estado']]
        ordering = ['pos']

    def __str__(self) -> str:
        return f"{self.conjunto.nombre} - {self.estado.nombre}"

class EstadoInsumo(models.Model):
    estado = models.ForeignKey(Estado, verbose_name="Estado Asociado", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        unique_together = [['estado', 'insumo']]


    def __str__(self) -> str:
        return f"{self.insumo.nombre} - {self.estado.nombre}"
    
class EstadoProducto(models.Model):
    estado = models.ForeignKey(Estado, verbose_name="Estado Asociado", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        unique_together = [['estado', 'producto']]

    def __str__(self) -> str:
        return f"{self.producto.nombre} - {self.estado.nombre}"