from re import VERBOSE
from django.db import models
from nucleo.models import Rama, Insumo, Producto
from simple_history.models import HistoricalRecords
# Create your models here.


class Columna(models.Model):
    nombre = models.CharField(verbose_name="Parámetro", max_length=255)
    tipo = models.CharField(max_length=255, choices=(('0', 'Entero',), ('1', 'Decimal'), ('2', 'Fecha'), ('3','Checkbox'),('4','Texto')), default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Parámetro'
        verbose_name_plural = 'Parámetros'
        default_permissions = ()
        permissions = (
            ('columna.listar', 'Permite listar los parámetros'),
            ('columna.crear', 'Permite crear un parámetro'),
            ('columna.eliminar', 'Permite eliminar un parámetro'),
            ('columna.actualizar', 'Permite actualizar un parámetro'),
        )

    def __str__(self):
        return self.nombre


class Pauta(models.Model):
    nombre = models.CharField(verbose_name="Nombre Pauta", max_length=255)
    tipo = models.CharField(verbose_name="Tipo de Pauta", choices=(('PIP', 'PIP'), ('Linea', 'Linea')), default='PIP', max_length=255)
    rendimiento = models.FloatField(verbose_name="Rendimiento PIP", default="8.5", help_text="Cantidad de kilos o litros necesarios para producir 1 kilo de producto pip.",null=True,blank=True)
    ingredientes = models.ManyToManyField(Insumo, through="Ingrediente", verbose_name="Ingredientes")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Pauta de elaboración'
        verbose_name_plural = 'Pautas de elaboración'
        ordering = ['-id']
        default_permissions = ()
        permissions = (
            ('listar', 'Permite listar las pautas de elaboración'),
            ('crear', 'Permite crear una pauta de elaboración'),
            ('eliminar', 'Permite eliminar una pauta de elaboración'),
            ('actualizar', 'Permite actualizar una pauta de elaboración'),
            ('detalle', 'Permite ver el detalle de una pauta')
        )

    def __str__(self):
        return "{}".format(self.nombre)

class PautaProducto(models.Model):
    pauta = models.ForeignKey(Pauta, verbose_name="Pauta Asociada", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Grupo Producto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pauta Producto'
        verbose_name_plural = 'Pauta Producto'
        ordering = ['-id']
        default_permissions = ()


class IngredienteProducto(models.Model):
    pauta = models.ForeignKey(Pauta, verbose_name="Pauta Asociada", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, verbose_name="Grupo Producto", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pauta Ingrediente Producto'
        verbose_name_plural = 'Pauta Ingrediente Producto'
        ordering = ['-id']
        unique_together = ['pauta', 'producto']
        default_permissions = ()


class IngredienteProductoRestriccion(models.Model):
    producto = models.ForeignKey(Producto, verbose_name="Grupo Producto", on_delete=models.CASCADE)
    pauta = models.ForeignKey(Pauta, verbose_name="Pauta Asociada", on_delete=models.CASCADE)
    simbolo = models.IntegerField(choices=( (0,"<"),(1,">"),(2,"="),(3,"<="),(4,">=")),verbose_name="Operacion")
    pmasa = models.FloatField(verbose_name="Porcentaje de masa")

    class Meta:
        verbose_name = 'Restriccion Ingrediente Producto'
        verbose_name_plural = 'Restriccion Ingrediente Producto'
        ordering = ['-id']
        default_permissions = ()


class Ingrediente(models.Model):
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    pauta = models.ForeignKey(Pauta, verbose_name="Pauta Asociada", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad")
    unidad = models.CharField(max_length=255)
    opcional = models.BooleanField(verbose_name="Insumo Opcional", default=False)
    original = models.BooleanField(verbose_name="Viene con la pauta por defecto", default=True)
    lider = models.BooleanField(verbose_name="Ingrediente al 100%", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Ingrediente'
        default_permissions = ()
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        return self.insumo.nombre


class InsumoProceso(models.Model):
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    pauta = models.ForeignKey(Pauta, verbose_name="Pauta Asociada", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Insumo Proceso'
        default_permissions = ()
        verbose_name_plural = "Insumo Proceso"
        unique_together = [['insumo', 'pauta']]

    def __str__(self):
        return f"Insumo Proceso {self.insumo.nombre}"


class Etapa(models.Model):
    orden = models.IntegerField(verbose_name="Orden")
    nombre = models.CharField(verbose_name="Nombre Etapa",max_length=255)
    pauta = models.ForeignKey(Pauta,verbose_name="Pauta Asociada",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Etapa'
        default_permissions = ()
        verbose_name_plural = 'Etapas'
    
    def __str__(self):
        return self.nombre

class Instruccion(models.Model):
    orden = models.IntegerField(verbose_name="Orden")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    etapa = models.ForeignKey(Etapa, verbose_name="Etapa Asociada", on_delete=models.CASCADE)
    puntocontrol = models.BooleanField(default=False,verbose_name="Punto de control")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Instrucción'
        default_permissions = ()
        verbose_name_plural = 'Instrucciones'

    def __str__(self):
        return self.descripcion


class InstruccionColumna(models.Model):
    instruccion = models.ForeignKey(Instruccion, verbose_name="Instrucción asociada", on_delete=models.CASCADE)
    columna = models.ForeignKey(Columna, verbose_name="Columna asociada", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()