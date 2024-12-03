from django.apps.registry import apps
from django.db import models
import numpy as np
import math
from django.contrib.auth.models import User
from django.conf import settings
import rsa
from django.core.validators import MinValueValidator

def nombreCompleto(self):
    if self.first_name:
        return "{} {}".format(self.first_name, self.last_name)
    return self.username


def cifrarID(self):
    return rsa.encrypt(str(self.pk).encode(),settings.KEYS['publica']).hex()


def verPanelAdministrativo(self):
    if self.is_superuser:
        return True
    permisos_panel = ['nucleo.insumo.listar','nucleo.producto.listar','proveedores.listar','inventario.bodega.listar','clientes.cliente.listar','nucleo.rama.listar','nucleo.producto.listar','pauta.listar','equipo.listar']
    for permiso in permisos_panel:
        if self.has_perm(permiso):
            return True
    return False

User.add_to_class("__str__", nombreCompleto)
User.add_to_class("panelAdministrativo",verPanelAdministrativo)
User.add_to_class("cifrarID",cifrarID)


class Moneda(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre Moneda",unique=True)
    valor = models.FloatField(verbose_name="Valor Moneda")
    fecha = models.CharField(max_length=255, verbose_name="Fecha de extraccion")

    class Meta:
        default_permissions = ()
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        ordering = ["-id"]

    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre genérico del insumo")
    unidad = models.CharField(max_length=50, verbose_name="Unidad de medida", choices=(
        ('', '---------'),
        ('N/A', 'N/A'),
        ('Unidad', 'Unidades'),
        ('Caja', 'Cajas'),
        ('Kilogramo', 'Kilogramos'),
        ('Litro', 'Litros')
    ))
    stock_critico = models.FloatField(verbose_name="Stock Crítico")
    pip = models.BooleanField(default=False,verbose_name="Si es un insumo que se genera al interior de la empresa.")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "insumo"
        verbose_name_plural = "insumos"
        unique_together = ['nombre', 'unidad']
        ordering = ["-created"]
        default_permissions = ()
        permissions = (
            ('insumo.listar', 'Puede listar los insumos'),
            ('insumo.crear', 'Puede crear un insumo'),
            ('insumo.eliminar', 'Puede eliminar un insumo'),
            ('insumo.actualizar', 'Puede actualizar un insumo'),
        )

    def __str__(self):
        return self.nombre.upper() + " - " + self.unidad.upper()


class Rama(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del área de negocio", unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "rama"
        verbose_name_plural = "ramas"
        ordering = ["nombre"]
        default_permissions = ()
        permissions = (
            ('rama.listar', 'Puede ver las áreas de negocio'),
            ('rama.crear', 'Puede crear una área de negocio'),
            ('rama.eliminar', 'Puede eliminar un área de negocio'),
            ('rama.actualizar', 'Puede actualizar un área de negocio'),
        )

    def __str__(self):
        return self.nombre.upper()


class Linea(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la Linea")
    rama = models.ForeignKey(Rama, on_delete=models.SET_NULL, null=True, verbose_name="Área de negocio", help_text="El área de negocio del producto.")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "linea de producto"
        verbose_name_plural = "lineas de producto"
        ordering = ["nombre"]
        default_permissions = ()
        permissions = (
            ('linea.listar', 'Puede ver las lineas de negocio'),
            ('linea.crear', 'Puede crear una linea de negocio'),
            ('linea.eliminar', 'Puede eliminar un linea de negocio'),
            ('linea.actualizar', 'Puede actualizar una linea de negocio'),
        )

    def __str__(self):
        return "{} - {}".format(self.rama.nombre.upper(),self.nombre.upper())
    
    def obtenerIngredientes(self):
        # obtenemos los productos
        ingredientes = {}
        productos = self.producto_set.filter(conjunto__isnull=False).all()
        unidades = {'kg':1,'lt':1,'gr':1000,'ml':1000,'cc':1000}
        for p in productos:
            #obtenemos sus ingredientes
            pingredientes = p.producto.insumoelaboracionproducto_set.all()
            for ingrediente in pingredientes:
                cantidad = unidades[p.producto.unidad] / p.producto.presentacion
                if cantidad < 0:
                    cantidad = 1 / cantidad
                #vemos si existe la llave
                if ingrediente.insumo.pk in ingredientes.keys():
                    ingredientes[ingrediente.insumo.pk] = {'ingrediente':ingrediente.insumo,'cantidad':ingrediente.cantidad * unidades[p.producto.unidad] / p.producto.presentacion}
                else:
                    ingredientes[ingrediente.insumo.pk] = {'ingrediente':ingrediente.insumo,'cantidad':ingrediente.cantidad * unidades[p.producto.unidad] / p.producto.presentacion}
        return ingredientes
    
    def generarCodigo(self):
        nombre_grupo = self.nombre.split(' ')
        # si el nombre de la rama posee 1 palabra
        if(len(nombre_grupo) == 1):
            self.codigo = (nombre_grupo[0][:2]*2).upper()
        else:
            self.codigo = ''.join([palabra[:1].upper() for palabra in nombre_grupo])
        self.codigo += str(1).zfill(2)
        return self.codigo


class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del producto", help_text="El nombre que poseera el producto.")
    codigo = models.CharField(max_length=255, verbose_name="Código del producto")
    linea = models.ForeignKey(Linea, on_delete=models.SET_NULL, null=True, default=None, related_name="productos", verbose_name="Linea de negocio", help_text="La linea de negocio del producto.")
    descripcion = models.TextField(verbose_name="Descripción del producto", blank=True, default="", help_text="Descripción del producto para ficha técnica.")
    presentacion = models.BigIntegerField(verbose_name="Presentación", help_text="El peso o volumen del producto")
    pautapip = models.ForeignKey('pauta.Pauta', related_name="pautapip", verbose_name="Pauta de elaboración PIP", default=None, blank=True, null=True, on_delete=models.SET_NULL)
    pautalinea = models.ForeignKey('pauta.Pauta', related_name="pautalinea", verbose_name="Pauta de Linea", default=None, blank=True, null=True, on_delete=models.SET_NULL)
    unidad = models.CharField(max_length=50, verbose_name="Unidad", choices=(
        ('', '---------'),
        ('gr', 'gramos'),
        ('kg', 'kilogramos'),
        ('lt', 'litros'),
        ('cc', 'centimetros cúbico')
    ), help_text="La unidad de medida del producto.")
    duracion = models.IntegerField(verbose_name="Vida útil del producto",help_text="La vida util del producto luego de ser elaborado.")
    maduracion = models.BigIntegerField(verbose_name="Maduración",help_text="La cantidad de días que el producto debe pasar en maduración.")
    stock_critico = models.BigIntegerField(verbose_name="Stock Crítico",help_text="La cantidad de stock minimo de este producto antes de levantar alertas.")
    unidades = models.IntegerField(verbose_name="Unidades por caja", default=24,help_text="La cantidad de unidades por caja de este producto.")
    dun14 = models.CharField(max_length=14, verbose_name="DUN14",default="",blank=True,help_text="El codigo DUN14 del producto.")
    id_comercio_net = models.CharField(max_length=255, verbose_name="Identificador comercio electrónico", null=True, blank=True)
    descriptores = models.ManyToManyField(Insumo, verbose_name="Descriptores", through="InsumoDirectoProducto")
    conjunto = models.ForeignKey('estado.ConjuntoEstado', verbose_name="Estado", on_delete=models.SET_NULL, default=None, null=True, blank=True,help_text="Los procesos de valor agregado a los cuales debe someterse este producto.")
    sap = models.CharField(verbose_name="SAP", max_length=12, default="",blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "producto"
        default_permissions = ()
        verbose_name_plural = "productos"
        ordering = ["id"]
        default_permissions = ()
        permissions = (
            ('producto.listar', 'Puede ver los productos'),
            ('producto.crear', 'Puede crear un producto'),
            ('producto.eliminar', 'Puede eliminar un producto'),
            ('producto.actualizar', 'Puede actualizar un producto'),
        )

    def costo_seco(self):
        #obtenemos los insumos
        total = 0
        insumos = self.insumodirectoproducto_set.all()
        for i in insumos:
            ordendecomprainsumo = apps.get_model('ordendecompra.ordendecomprainsumo').objects.filter(insumo__insumo=i.insumo).first()
            if ordendecomprainsumo:
                suma = 0
                try:
                    suma = round(ordendecomprainsumo.neto / ordendecomprainsumo.insumo.formato,10)
                except Exception as ex:
                    suma = ordendecomprainsumo.neto
            else:
                suma = 0
            total+= suma * i.porcentaje_uso/100 * i.cantidad
        return total

    def ean13(self):
        # sacamos el digito verificador del ean13
        ean13 = self.dun14[1:-1]
        pares = [int(ean13[digito]) for digito in range(len(ean13)) if digito % 2 == 0][:-1]
        impares = [int(ean13[digito]) for digito in range(len(ean13)) if digito % 2 != 0]
        sumapares = np.sum(pares)
        sumaimpares = np.sum(impares) * 3
        suma = sumapares + sumaimpares
        redondeo = int(math.ceil(suma / 10.0)) * 10
        digito = redondeo-suma
        return ean13 + str(digito)
        # digito_inicial = (self.unidades // 10) * 1
        # if digito_inicial == 0:
        #     digito_inicial = 1
        # dun14 = str(digito_inicial) + ean13
        # pares = [int(dun14[digito]) for digito in range(len(dun14)) if (digito+1) % 2 == 0]
        # impares = [int(dun14[digito]) for digito in range(len(dun14)) if (digito+1) % 2 != 0]
        # sumapares = np.sum(pares)
        # sumaimpares = np.sum(impares) * 3
        # suma = sumapares + sumaimpares
        # redondeo = int(math.ceil(suma / 10.0)) * 10
        # digito = redondeo - suma

    def __str__(self):
        return self.nombre + " ({} {})".format(self.presentacion, self.unidad)
    
    def generarCodigo(self):
        nombre_rama = self.linea.rama.nombre.split(' ')
        # si el nombre de la rama posee 1 palabra
        if(len(nombre_rama) == 1):
            self.codigo = (nombre_rama[0][:2]*2).upper()
        else:
            self.codigo = (nombre_rama[0][:2] + nombre_rama[1][:2]).upper()
        # buscamos el ultimo producto agregado de la rama
        ultimo_producto_rama = Producto.objects.filter(codigo__contains=self.codigo).exclude(pk=self.pk).order_by('-codigo').first()
        if ultimo_producto_rama:
            numbers = [str(word) for word in ultimo_producto_rama.codigo if word.isdigit()]
            numero = int(''.join(numbers))
            print(numero)
        else:
            numero = 0
        self.codigo += str(numero+1).zfill(2)
        return self.codigo
    
    def obtenerCDP(self):
        #obtenemos los lotes
        lotes = self.lote_set.all()
        total = 0
        contador = 0
        for l in lotes:
            cdp = l.cdp
            if cdp > 0:
                total+=cdp
                contador+=1
        if total > 0:
            return total / contador
        else:
            return 0
    
    def obtenerEmpaque(self):
        descriptores = self.descriptores
        for d in descriptores:
            print(d)
    
    def obtenerMargen(self):
        #obtenemos los lotes
        lotes = self.lote_set.all()
        total = 0
        contador = 0
        for l in lotes:
            cdp = l.margen()
            if cdp > 0:
                total+=cdp
                contador+=1
        if total > 0:
            return total / contador
        else:
            return 0

    # metodo personalizado de guardado para generar el codigo
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.codigo = self.generarCodigo()
        super(Producto, self).save(*args, **kwargs)

class InsumoElaboracionProducto(models.Model):
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="cantidad por kilo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "insumo producto"
        verbose_name_plural = "insumos producto"
        ordering = ["insumo__nombre"]
        unique_together = ['producto', 'insumo']
        default_permissions = ()


class InsumoDirectoProducto(models.Model):
    producto = models.ForeignKey(Producto, verbose_name="Producto",on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo",on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="cantidad")
    porcentaje_uso = models.FloatField(verbose_name="Porcentaje uso",default=0)
    detalle = models.CharField(max_length=255,verbose_name="Detalle del insumo directo")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "insumo directo de producción"
        verbose_name_plural = "insumos directos de producción"
        ordering = ["producto__nombre"]
        unique_together = ['producto','insumo']
        default_permissions = ()
    
    def transformar(self):
        return str(self.porcentaje_uso).replace(',','.')

    def __str__(self):
        return self.insumo.nombre.upper()




class Permiso(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Permiso")
    class Meta:
        default_permissions = ()
        permissions = (
            ('permiso.crear.usuario', 'Permite Crear Usuarios'),
            ('permiso.actualizar.usuario', 'Permite Actualizar Usuarios'),
            ('permiso.eliminar.usuario', 'Permite Eliminar Usuarios'),
            ('permiso.listar.usuario', 'Permite Listar Usuarios'),
        )