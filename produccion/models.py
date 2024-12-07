from django.db.models.signals import pre_delete
from estado.models import Estado, ConjuntoEstado
from inventario.models import Bodega, InventarioProducto, InventarioInsumo, InsumoBulto
from django.db import models
from pauta.models import Pauta, Ingrediente, Instruccion, Columna, InsumoProceso
from nucleo.models import Producto, Insumo, Linea
from django.contrib.auth.models import User
from django.db.models import F
from django.apps import apps
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
from django.db import models
from simple_history.models import HistoricalRecords

class PautaProduccion(models.Model):
    plantilla_pauta = models.ForeignKey(Pauta, verbose_name="Pauta de elaboración a seguir", on_delete=models.SET_NULL, null=True)
    lugar = models.ForeignKey(Bodega, verbose_name="Lugar", on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(verbose_name="Fecha de fabricación")
    cantidad = models.FloatField(verbose_name="Cantidad a elaborar")
    masa_final = models.FloatField(verbose_name="Masa Final", blank=True, null=True)
    rendimiento = models.FloatField(verbose_name="Rendimiento", default=8.5)
    estado = models.CharField(verbose_name="Estado Pauta", max_length=255, choices=(('En Elaboración', 'En Elaboración'), ('Segmentación', 'Segmentación'), ('Finalizada', 'Finalizada')), default="En Elaboración")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    cdp = models.FloatField(verbose_name="Costo directo produccion", default=0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Pauta Producción'
        verbose_name_plural = 'Pautas Producción'
        default_permissions = ()
        permissions = (
            ('pauta.listar', 'Permite listar las pautas de producción'),
            ('pauta.crear', 'Permite crear una pauta de producción'),
            ('pauta.detalle', 'Permite ver el detalle de una pauta de producción'),
            ('pauta.eliminar', 'Permite eliminar una pauta de producción'),
            ('pauta.actualizar', 'Permite actualizar una pauta de producción'),
        )

    def __str__(self):
        if self.plantilla_pauta:
            return f'Pauta de elaboración: {self.plantilla_pauta.nombre} (ID: {self.pk})'
        return f'Pauta de elaboración: Sin plantilla (ID: {self.pk})'



    def calcularCDP(self):
        if self.pk is None:
            return 0  # O manejar el caso como sea apropiado

        total = 0
        ingredientes = self.ingredienteproduccion_set.all()

        for i in ingredientes:
            bodega = InventarioInsumo.objects.filter(bodega=self.lugar, insumo=i.plantilla_ingrediente.insumo).first()
            unidades = {'cc': 0.001, 'n/a': 1, 'kilogramo': 1, 'litro': 1, 'unidad': 1, 'gramo': 0.001, 'miligramo': 0.000001, 'mililitro': 0.001, 'caja': 1, 'cajas': 1}
            unidad = unidades.get(i.unidad.lower(), 1)

            if bodega:
                valorbodega = bodega.valorizar()

                if bodega.insumo.pip:
                    producciones = apps.get_model('produccion.insumoprocesoproduccion').objects.filter(cantidadu__lt=F('cantidad'), pauta_produccion__lugar=self.lugar, plantilla_ip__insumo=i.plantilla_ingrediente.insumo).order_by('id').all()
                    asignar = i.cantidad * unidad
                    for p in producciones:
                        disponible = p.cantidad - p.cantidadu
                        if asignar >= disponible:
                            p.cantidadu = p.cantidad
                            asignar -= disponible
                        else:
                            p.cantidadu += asignar
                            asignar = 0
                        p.save()
                
                cantidadu = i.cantidad * unidad
                total += valorbodega * cantidadu

        return total


class BultoPautaProduccion(models.Model):
    pauta = models.ForeignKey(PautaProduccion, verbose_name="Pauta", on_delete=models.CASCADE)
    bulto = models.ForeignKey(InsumoBulto, verbose_name="Bulto", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad")

    class Meta:
        verbose_name = 'Participante Elaboración'
        verbose_name_plural = 'Participantes Elaboración'
        default_permissions = ()


class ParticipanteProduccion(models.Model):
    pauta = models.ForeignKey(PautaProduccion, verbose_name="Pauta", on_delete=models.CASCADE)
    participante = models.ForeignKey(User, verbose_name="Participante", on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = 'Participante Elaboración'
        verbose_name_plural = 'Participantes Elaboración'
        default_permissions = ()


class IngredienteProduccion(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE)
    plantilla_ingrediente = models.ForeignKey(Ingrediente, verbose_name="Ingrediente", on_delete=models.CASCADE,default=None,null=True)
    cantidad = models.FloatField(verbose_name="Cantidad Usada")
    unidad = models.CharField(verbose_name="unidad", max_length=255)

    class Meta:
        verbose_name = 'Ingrediente Pauta Producción'
        verbose_name_plural = 'Ingredientes Pautas Producción'
        default_permissions = ()


class InsumoProcesoProduccion(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE)
    plantilla_ip = models.ForeignKey(InsumoProceso, verbose_name="Insumo Produccion", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad Producida", default=0)
    cantidadu = models.FloatField(verbose_name="Cantidad Utilizada", default=0)
    comentario = models.CharField(verbose_name="Comentarios", max_length=255, default="")

    class Meta:
        verbose_name = 'Insumo Proceso Produccion'
        verbose_name_plural = 'Insumos Proceso Producción'
        default_permissions = ()


class InsumoPipUtilizado(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE)
    insumoproceso = models.ForeignKey(InsumoProcesoProduccion, verbose_name="Insumo proceso utilizado",on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad Utilizada")

    class Meta:
        verbose_name = 'Insumo Proceso Produccion'
        verbose_name_plural = 'Insumos Proceso Producción'
        default_permissions = ()


class InstruccionProduccion(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE)
    plantilla_instruccion = models.ForeignKey(Instruccion, verbose_name="Instrucción", on_delete=models.SET_NULL, null=True)
    plantilla_columna = models.ForeignKey(Columna, verbose_name="Columna", on_delete=models.SET_NULL, null=True)
    valor = models.CharField(max_length=255, verbose_name="Valor")

    class Meta:
        verbose_name = 'Instrucción Pauta Producción'
        verbose_name_plural = 'Instrucciones Pautas Producción'
        default_permissions = ()
        ordering = ['plantilla_columna__id']

class LineaProduccion(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE, null=True)
    linea = models.ForeignKey(Linea, verbose_name="Linea de Producto", on_delete=models.SET_NULL, null=True)
    pva = models.ForeignKey(ConjuntoEstado,verbose_name="Procesos de valor agregado",on_delete=models.SET_NULL,null=True)
    final = models.BooleanField(verbose_name="Resultado Final", default=True)
    cantidad = models.FloatField(verbose_name="Cantidad Elaborada")

    class Meta:
        verbose_name = 'Producto Producción'
        verbose_name_plural = 'Productos Producción'
        default_permissions = ()

class ProductoProduccion(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.SET_NULL, null=True)
    final = models.BooleanField(verbose_name="Resultado Final", default=True)
    cantidad = models.FloatField(verbose_name="Cantidad Elaborada")

    class Meta:
        verbose_name = 'Producto Producción'
        verbose_name_plural = 'Productos Producción'
        default_permissions = ()


class Lote(models.Model):
    pauta_produccion = models.ForeignKey(PautaProduccion, verbose_name="Pauta Producción", on_delete=models.CASCADE, null=True)
    numero = models.CharField(verbose_name="Numero de Lote", max_length=255)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.SET_NULL, null=True)
    linea = models.ForeignKey(Linea, verbose_name="Linea de Producto",null=True,default=None,on_delete=models.SET_NULL)
    pva = models.ForeignKey(ConjuntoEstado, verbose_name="Procesos de Valor Agregado",null=True,default=None,on_delete=models.SET_NULL)
    mostrar = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de fabricación")
    cantidad = models.FloatField(verbose_name="Cantidad En Kilogramos o Unidades")
    comentario = models.CharField(verbose_name="Comentarios", max_length=255)
    cdp = models.FloatField(verbose_name="Costo Directo Produccion",default=0)

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        default_permissions = ()
        ordering = ['-fecha']
    
    def obtenerProductos(self):
        productos = Producto.objects.filter(linea=self.linea,conjunto=self.pva).all()
        return productos

    # metodo personalizado de guardado para generar el codigo
    def save(self, *args, **kwargs):
        if self._state.adding:
            fecha = self.pauta_produccion.fecha
            ano = str(fecha.year)[2:]
            mes = str(fecha.month).zfill(2)
            dia = str(fecha.day)
            if(self.producto is not None):
                codigo = self.producto.codigo
                totalproductos = len(Lote.objects.filter(producto=self.producto, pauta_produccion__fecha__year=fecha.year, pauta_produccion__fecha__month=fecha.month, pauta_produccion__fecha__day=dia).all()) + 1
                self.numero = ano+mes+dia+"-"+codigo+"-"+str(totalproductos).zfill(2)
            else:
                codigo = self.linea.generarCodigo()
                totalgrupos = len(Lote.objects.filter(linea=self.linea, pauta_produccion__fecha__year=fecha.year, pauta_produccion__fecha__month=fecha.month, pauta_produccion__fecha__day=dia).all()) + 1
                self.numero = ano+mes+dia+"-"+codigo+"-"+str(totalgrupos).zfill(2)
        super(Lote, self).save(*args, **kwargs)
    
    #funcion para calcular el margen
    def margen(self):
        #vemos si el lote esta cerrado
        if self.estadolote_set.last().nombre == 'Cerrado':
            #obtenemos las cajas del lote
            cajas = self.cajalote_set.all()
            total = 0
            unidades = 0
            for caja in cajas:
                #buscamos las ventas de esta caja
                venta = caja.ordendeventacajalote_set.last()
                if venta:
                    infoventa = venta.orden.ordendeventaproducto_set.filter(producto=self.producto).last()
                    precio = infoventa.precio
                    cantidad = venta.cantidad
                    total+=precio*cantidad
                    unidades+=cantidad
            try:
                devolver = total/unidades
            except:
                if(unidades == 0):
                    devolver = total
                else:
                    devolver = 0
            return devolver
        return 0



    #devuelve la cantidad actual de unidades
    def cantidadactual(self):
        estados = self.estadolote_set.all()
        transformar = lambda x: x if x is not None else 0
        total = 0
        actual = self.cantidad
        for e in estados:
            total+= transformar(e.unidadesNC) + transformar(e.unidadesFF) + transformar(e.unidadesC)
            if(e.peso > 0):
                self.cantidad = e.peso
        return self.cantidad - total
    
    def totalsinenviar(self):
        estados = self.estadolote_set.all()
        transformar = lambda x: x if x is not None else 0
        total = 0
        for e in estados:
            total+= transformar(e.unidadesNC) + transformar(e.unidadesFF) + transformar(e.unidadesC)
        return self.cantidad - total
    
    #devuelve el ultimo estado del lote
    def estado(self):
        return self.estadolote_set.last()
    
    def ultimo_peso(self):
        estado = self.estado()
        if estado and estado.peso != 0:
            return estado.peso
        else:
            if self.producto is None:
                return self.cantidad
            else:
                unidades = {'gr': 0.001,'kg':1,'ml':0.001,'lt':1,'cc':0.001}
                return self.cantidad * self.producto.presentacion * unidades[self.producto.unidad.lower()]
        return 0
    
    def proximo_estado(self):
        actual = self.estado()
        producto = self.producto
        if producto is None:
            if self.pva is not None:
                conjuntos = self.pva.estadoconjunto_set.all()
                if actual.nombre == 'Inicial':
                    if len(conjuntos) > 0:
                        return conjuntos[0].estado
                    else:
                        return Estado(nombre='Separación')
                else:
                    estado = [estado for estado in conjuntos if estado.estado.nombre == actual.nombre]
                    if len(estado) > 0:
                        pos = estado[0].pos
                        estado = [estado for estado in conjuntos if estado.pos > pos]
                        if len(estado) > 0:
                            return estado[0].estado
                        #no quedan estados
                        else:
                            if(actual.nombre not in ["Separación", "Empaque Final"]):
                                if producto is None:
                                    return Estado(nombre='Separación')
                                else:
                                    return Estado(nombre='Empaque Final')
        if((type(producto).__name__ == 'Producto') and (actual.nombre == 'Inicial')):
            return Estado(nombre='Empaque Final')
        return Estado(nombre='Inicial')
    
    """ def proximo_estado(self):
        actual = self.estado()
        producto = self.producto if self.producto is not None else None
        if producto.conjunto is not None:
            conjuntos = producto.conjunto.estadoconjunto_set.all()
            if actual.nombre == 'Inicial':
                if len(conjuntos) > 0:
                    return conjuntos[0].estado
                else:
                    return Estado(nombre='Separación')
            else:
                estado = [estado for estado in conjuntos if estado.estado.nombre == actual.nombre]
                if len(estado) > 0:
                    pos = estado[0].pos
                    estado = [estado for estado in conjuntos if estado.pos > pos]
                    if len(estado) > 0:
                        return estado[0].estado
                    #no quedan estados
                    else:
                        if(actual.nombre not in ["Separación", "Empaque Final"]):
                            if(type(producto).__name__ == 'GrupoProducto'):
                                return Estado(nombre='Separación')
                            else:
                                return Estado(nombre='Empaque Final')
        
        if((type(producto).__name__ == 'Producto') and (actual.nombre == 'Inicial')):
            return Estado(nombre='Empaque Final')
        if((type(producto).__name__ == 'GrupoProducto') and (actual.nombre == 'Inicial')):
            return Estado(nombre='Separación')
        return None """

    #calcula cuantas unidades han sido enviadas
    def enviadas(self):
        lotes = self.cajalote_set.all()
        total = 0
        for l in lotes:
            envio = l.loteenvio_set.last()
            if envio is not None:
                if envio.recepcionado is None:
                    total+=l.cantidad
        return total
    
    #calcula las unidades que van en transito
    def transito(self,user,envio):
        lotes = self.cajalote_set.all()
        cantidad = 0
        for l in lotes:
            enviod = l.loteenvio_set.filter(envio=envio).first()
            if enviod is not None and enviod.recepcionado is None:
                cantidad+=l.cantidad
        #condicion para generar el estado de en transito
        if cantidad > 0:
            if self.estadolote_set.last().nombre == 'Empacado':
                self.estadolote_set.create(nombre="En Transito",encargado=user,fecha=datetime.now(),lugar=user.perfil.lugar)
    
    #funcion para recepcionar el lote
    def recepcionado(self,user,envio):
        lotes = self.cajalote_set.all()
        cantidad = 0
        for l in lotes:
            enviod = l.loteenvio_set.first()
            if enviod is not None and enviod.recepcionado is not None:
                cantidad+=l.cantidad
        if cantidad >= self.cantidadactual():
            if self.estadolote_set.last().nombre == 'En Transito':
                self.estadolote_set.create(nombre="Recepcionado",encargado=user,fecha=datetime.now(),lugar=user.perfil.lugar)

    #funcion para saber las cajas asociadas al lote
    def cajas(self):
        cajas = self.cajalote_set.all()
        return cajas


class CajaLote(models.Model):
    lote = models.ForeignKey(Lote, verbose_name="Lote", on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField(verbose_name="Cantidad por caja")
    cantidad_a = models.IntegerField(verbose_name="Cantidad por caja", default=0)
    caja = models.IntegerField(verbose_name="Caja")
    recepcionado = models.BooleanField(default=None, verbose_name="Recepcionado", null=True)
    estado = models.CharField(default='Produccion', choices=(('Produccion', 'Produccion'), ('Transito', 'Transito'), ('Recepcionado', 'Recepcionado'), ('Abierto', 'Abierto'), ('Pickeado', 'Pickeado'), ('Cerrado','Cerrado'), ('Cliente', 'Cliente')), max_length=20)
    lugar = models.ForeignKey(Bodega, verbose_name="Lugar", on_delete=models.SET_NULL, null=True)

    class Meta:
        default_permissions = ()
        verbose_name = 'caja lote'
        verbose_name_plural = 'cajas lote'
        unique_together = ('lote', 'caja')

class CajaLotePautaProduccion(models.Model):
    pauta = models.ForeignKey(PautaProduccion, verbose_name="Pauta", on_delete=models.CASCADE)
    producto = models.ForeignKey(CajaLote, verbose_name="Caja Lote", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad")

    class Meta:
        verbose_name = 'Caja Pauta Produccion'
        verbose_name_plural = 'Caja Pauta Produccion'
        default_permissions = ()

class EstadoLote(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Estado")
    lote = models.ForeignKey(Lote, verbose_name="Lote", on_delete=models.CASCADE, blank=True, null=True)
    encargado = models.ForeignKey(User, verbose_name="Encargado", on_delete=models.SET_NULL, null=True)
    estadoGlobal = models.ForeignKey(Estado, verbose_name="Estado", on_delete=models.SET_NULL, null=True, default=None)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    peso = models.FloatField(verbose_name="Peso", blank=True, null=True, default=0)
    unidadesNC = models.IntegerField(verbose_name="Unidades No Consumibles", blank=True, null=True, default=0)
    unidadesFF = models.IntegerField(verbose_name="Unidades Fuera de Formato", blank=True, null=True, default=0)
    unidadesC = models.IntegerField(verbose_name="Unidades Para Calidad", blank=True, null=True, default=0)
    lugar = models.ForeignKey(Bodega, verbose_name="Lugar", on_delete=models.CASCADE, blank=True, null=True)
    observacion = models.TextField(verbose_name="Observación", blank=True)

    class Meta:
        verbose_name = 'Estado de Lote'
        verbose_name_plural = 'Estados de Lotes'
        default_permissions = ()
        permissions = (
            ('elote.eliminar', 'Permite eliminar un estado de lote'),
            ('elote.actualizar', 'Permite actualizar un estado de lote'),
        )

    def ultima(self):
        return 'pan'
    
class EstadoLoteInsumo(models.Model):
    estado = models.ForeignKey(EstadoLote,verbose_name="Estado Lote",on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo,verbose_name="Insumo",on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad")

    class Meta:
        verbose_name = 'Estado Lote Insumo'
        verbose_name_plural = 'Estado Lote Insumos'
        default_permissions = ()
        permissions = (
            ('elote.eliminar', 'Permite eliminar un estado de lote'),
            ('elote.actualizar', 'Permite actualizar un estado de lote'),
        )

class CalidadProduccion(models.Model):
    # Relación con la Pauta de Producción
    pauta_produccion = models.ForeignKey(PautaProduccion, on_delete=models.CASCADE, related_name="calidad_produccion", verbose_name="Pauta de Producción")
    instrucciones = models.ForeignKey(
        InstruccionProduccion,
        verbose_name="instrucciones",
        on_delete=models.CASCADE,
        null=True,  # Permite valores nulos
        blank=True   # Permite que sea opcional en formularios
    )
    # PCC2 - Filtrado de Producto Final
    filtro_instalado = models.CharField(max_length=255, verbose_name="Filtro Instalado")
    filtro_integrado = models.CharField(max_length=255, verbose_name="Filtro Integrado")

    # Envasado y Almacenamiento
    inicio_envasado = models.CharField(max_length=255, verbose_name="Inicio Envasado")
    fin_envasado = models.CharField(max_length=255, verbose_name="Fin Envasado")
    unidades_botellas_lt = models.CharField(max_length=255,verbose_name="Unidades Botellas (lt)")
    unidades_360gr = models.CharField(max_length=255,verbose_name="Unidades 360gr")
    unidades_150gr = models.CharField(max_length=255,verbose_name="Unidades 150gr")
    merma_kg = models.CharField(max_length=10, verbose_name="Merma (kg)")

    # Evaluación Sensorial
    ph = models.CharField(max_length=50, verbose_name="pH")
    textura = models.CharField(max_length=50, verbose_name="Textura")
    sabor = models.CharField(max_length=50, verbose_name="Sabor")
    color = models.CharField(max_length=50, verbose_name="Color")
    olor = models.CharField(max_length=50, verbose_name="Olor")
    aspecto = models.CharField(max_length=50, verbose_name="Aspecto")

    # Responsables
    elaboracion = models.CharField(max_length=255, verbose_name="Responsable Elaboración")
    envasado = models.CharField(max_length=255, verbose_name="Responsable Envasado")
    verificacion = models.CharField(max_length=255, verbose_name="Responsable Verificación")

    # Observaciones
    observaciones = models.CharField(max_length=255,verbose_name="Observaciones")

    # Historial (si lo deseas)
    history = HistoricalRecords()

    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    estado_aprobacion = models.TextField(max_length=50, choices=(('Desaprobado', 'Desaprobado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')), default="Pendiente")


    def __str__(self):
        return f"Calidad Producción {self.id} - Pauta {self.pauta_produccion.id}"

    class Meta:
        verbose_name = "Calidad de Producción"
        verbose_name_plural = "Calidades de Producción"



#Agregar el inventario al crear el insumo
@receiver(models.signals.post_save,sender=EstadoLoteInsumo)
def agregar_inventario_estadoinsumo(sender,instance,created,**kwargs):
    if created:
        inventario,created = InventarioInsumo.objects.get_or_create(bodega=instance.estado.lote.pauta_produccion.lugar,insumo=instance.insumo,defaults={'cantidad': 0})
        if inventario:
            inventario.cantidad+= instance.cantidad
            inventario.save()

#Eliminar el inventario al eliminar el insumo
@receiver(models.signals.pre_delete,sender=EstadoLoteInsumo)
def eliminar_inventario_estadoinsumo(sender,instance,**kwargs):
    inventario,created = InventarioInsumo.objects.get_or_create(bodega=instance.estado.lote.pauta_produccion.lugar,insumo=instance.insumo,defaults={'cantidad': 0})
    if inventario:
        inventario.cantidad-= instance.cantidad
        inventario.save()



#Agregar el inventario de la zona, si es que se mueve el lote a empacado
@receiver(models.signals.post_save, sender=EstadoLote)
def agregar_inventario_estado(sender,instance, **kwargs):
    if instance.nombre == 'Empacado' and instance.lote is not None:
        inventario,created = InventarioProducto.objects.get_or_create(bodega=instance.lugar,producto=instance.lote.producto,defaults={'cantidad': 0})
        if inventario:
            inventario.cantidad+= instance.lote.cantidadactual()
            inventario.save()


#Eliminar el inventario de la zona, si es que se elimina el estado del lote
@receiver(models.signals.pre_delete,sender=EstadoLote)
def eliminar_inventario_estado(sender,instance,**kwargs):
    if instance.nombre in ['Empacado','En Transito', 'Recepcionado']:
        inventario = InventarioProducto.objects.filter(producto=instance.lote.producto,bodega=instance.lote.pauta_produccion.lugar).first()
        if inventario:
            inventario.cantidad-= instance.lote.cantidadactual()
            inventario.save()

#cerrar lote
@receiver(models.signals.post_save,sender=CajaLote)
def cerrar_lote_caja(sender,instance,**kwargs):
    #obtenemos el lote 
    lote = instance.lote
    if lote.estadolote_set.last().nombre != 'Cerrado':
        #obtenemos las cajas del lote
        cajas = lote.cajalote_set.all()
        cantidad = len(cajas)
        listas = 0
        for c in cajas:
            if c.estado in ['Cerrado','Cliente']:
                listas+=1
        if cantidad == listas:
            lote.estadolote_set.create(nombre='Cerrado')

#cambiar estado caja lote cuando se abre
@receiver(models.signals.pre_save,sender=CajaLote)
def cambiar_estado_caja(sender,instance,**kwargs):
    if instance.cantidad_a == instance.cantidad:
        instance.estado = 'Cerrado'

#Calcular el cdp antes de guardar
@receiver(models.signals.pre_save,sender=PautaProduccion)
def calcularCDPPauta(sender,instance,**kwargs):
    if(instance.cdp == 0):
        total = instance.calcularCDP()
        instance.cdp = total

#eliminar Bulto
@receiver(models.signals.pre_delete,sender=BultoPautaProduccion)
def agregarBultoCantidadU(sender,instance,**kwargs):
    bulto = instance.bulto
    bulto.cantidadu-=instance.cantidad
    bulto.save()

#agregar Bulto
@receiver(models.signals.pre_save,sender=BultoPautaProduccion)
def sacarBultoCantidadU(sender,instance,**kwargs):
    bulto = instance.bulto
    bulto.cantidadu+=instance.cantidad
    bulto.save()  