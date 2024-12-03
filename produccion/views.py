from estado.models import ConjuntoEstado
from logistica.models import LoteEnvio
from inventario.models import InventarioProducto,InsumoBulto
from nucleo.models import Producto, Rama, Linea
from django.views.generic.detail import DetailView
from rest_framework.response import Response
from rest_framework.views import APIView
from .functions import generar_codigo, add_margin, historial_actualizar_elaboracion, historial_actualizar_lote, historial_crear_elaboracion, historial_crear_lote, historial_eliminar_elaboracion, historial_eliminar_lote,obtener_lunes
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .forms import EstadoLoteCreateForm, PautaProduccionCreateForm, PautaProduccionUpdateForm
from .serializers import CajaLoteSerializer, LoteDetalleSerializer, LoteMaduracionSerializer, LoteSerializer, PautaProduccionSerializer, PautaProduccionDetalleSerializer
from django.views.generic import TemplateView,CreateView, View, UpdateView
from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from nucleo.mixins import ValidatePermissionRequiredMixin
from .models import CajaLote, EstadoLote, InsumoProcesoProduccion, Lote, PautaProduccion
from pauta.models import Columna, Pauta
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from inventario.models import InventarioInsumo
from django.http.response import Http404, HttpResponseRedirect
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime,timedelta
from PIL import Image, ImageFont, ImageDraw
from django.db.models import Sum

#API DE LAS PAUTAS DE ELABORACION GENERAL
@method_decorator(login_required,'dispatch')
class PautaProduccionViewSet(ValidatePermissionRequiredMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #las ordenes de compras que seran mostradas en la api rest
    queryset = PautaProduccion.objects.all()
    #la clase serializer que proviene de .serializers
    serializer_class = PautaProduccionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PautaProduccion.objects
        else:
            return PautaProduccion.objects.filter(lugar=self.request.user.perfil.lugar)

#API DE LOS LOTES
@method_decorator(login_required,'dispatch')
class LoteViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #las ordenes de compras que seran mostradas en la api rest
    queryset = Lote.objects.all()
    #la clase serializer que proviene de .serializers
    serializer_class = LoteSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Lote.objects
        else:
            return Lote.objects.filter(pauta_produccion__lugar=self.request.user.perfil.lugar)

#API PARA OBTENER EL DETALLE DE CADA LOTE
@method_decorator(login_required,'dispatch')
class LoteRetrieveApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los lotes.'
    serializer_class = LoteDetalleSerializer

    def get_queryset(self):
        return Lote.objects.filter()

#Api para obtener los lotes en maduración a partir de un producto
@method_decorator(login_required,'dispatch')
class LoteMaduracionPorProducto(ValidatePermissionRequiredMixin,APIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los lotes.'
    
    def get(self,request,*args,**kwargs):
        #la id del producto que vamos a observar su maduración
        id_producto = int(self.kwargs.get('pk'))
        #la escala de días que se utilizara
        dias = self.request.GET.get('dias')
        #si la escala existe, la intentamos pasar a int, y si no la devolvemos a None
        if dias is not None:
            try:
                dias = int(dias)
            except:
                dias = None
        #obtenemos el producto
        producto = Producto.objects.filter(pk=id_producto).first()
        if producto:
            #sacamos los lotes que tengan ese producto
            if self.request.user.is_superuser:
                lotes = Lote.objects.filter(producto_id=id_producto).all()
            else:
                lotes = Lote.objects.filter(producto_id=id_producto,pauta_produccion__lugar=self.request.user.perfil.lugar).all()
            lotes_f = []
            #verificamos que el ultimo estado sea el de maduración
            for lote in lotes:
                ultimo_estado = lote.estadolote_set.last()
                if ultimo_estado.nombre == 'En Maduración':
                    final = {'lote':lote,'estado':ultimo_estado}
                    lotes_f.append(final)
            
            #generamos las fechas para este producto
            dt = datetime.now()
            #obtenemos el comienzo de la semana
            start = dt - timedelta(days=dt.weekday())
            #obtenemos las semanas de maduración redondeadas
            if dias is None:
                maduracion = (producto.maduracion // 7) * 7
            else:
                maduracion = dias
            #generamos la lista de fechas
            lista = [-maduracion*4,-maduracion*3,-maduracion*2,-maduracion*1,0,maduracion*1,maduracion*2,maduracion*3,maduracion*4,maduracion*5]
            #la matriz que luego se mostrara al usuario en el apartado de maduración
            matriz = [[0 for col in range(11)] for row in range(4)]
            #las fechas
            fechas = [obtener_lunes(start + timedelta(days=i),dias) for i in lista]
            for lote in lotes_f:
                lotef = lote['lote']
                estado = lote['estado']
                fecha_i = obtener_lunes(estado.fecha,dias)
                fecha_f = obtener_lunes(estado.fecha + timedelta(days=lotef.producto.maduracion),dias)
                #llenar el día 0 (cuando empezo su fabricación)
                inicio = 0
                fin = 0
                for i in range(len(fechas)):
                    if fechas[i] <= fecha_i:
                        inicio = i
                    if fechas[i] <= fecha_f:
                        fin = i
                matriz[0][inicio+1]+=lotef.cantidad
                matriz[1][fin+1]+=lotef.cantidad
            #si es que la variable dias no esta definida se utiliza la maduración del producto por defecto
            if dias is None:
                diasx = [producto.maduracion *0,producto.maduracion *1,producto.maduracion *2,producto.maduracion *3]
            else:
                diasx = [dias*0,dias*1,dias*2,dias*3]
            #agregamos los días a la tabla
            for i in range(len(diasx)):
                matriz[i][0] = "{} días".format(diasx[i])
            #devolvemos la respuesta
            return Response({
                "fechas": fechas,
                "matriz": matriz,
                "estado": "ok",
                })
        return Response({
                "estado": "error"
                })

#API PARA OBTENER LA INFORMACIÓN DE LA PAUTA POR LUGAR (BODEGA)
@method_decorator(login_required,'dispatch')
class PautaProduccionRetrieveApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las elaboraciones.'
    serializer_class = PautaProduccionDetalleSerializer

    def get_queryset(self):
        return PautaProduccion.objects.filter()
    
    def get_serializer_context(self):
        context = super(PautaProduccionRetrieveApi, self).get_serializer_context()
        context.update({'lugar':self.request.user.perfil.lugar.pk})
        return context


# Lista de las elaboraciones para PIP
@method_decorator(login_required, 'dispatch')
class PautaProduccionList(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'produccion.pauta.listapip'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las elaboraciones.'
    template_name = 'produccion/pauta/productos_pip/list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtrar las pautas de producción donde la plantilla (pauta) es de tipo 'PIP'
        context['pautas'] = PautaProduccion.objects.filter(plantilla_pauta__tipo='PIP')
        return context



@method_decorator(login_required, 'dispatch')
class PautaProduccionListLinea(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'produccion.pauta.listalinea'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las elaboraciones.'
    template_name = 'produccion/pauta/producto_linea/lista_linea.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # Filtrar las pautas de producción donde la plantilla (pauta) es de tipo 'Linea'
            context['pautas_produccion'] = PautaProduccion.objects.filter(plantilla_pauta__tipo='Linea')
            return context
    



    
#Listar Pauta
@method_decorator(login_required,'dispatch')
class PautaDetailView(ValidatePermissionRequiredMixin,DetailView):
    #permiso necesario
    permission_required = 'produccion.pauta.detalle'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar una elaboración.'
    #template a utilizar
    model = PautaProduccion
    template_name = 'produccion/pauta/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombres = []
        ids = []
        instrucciones = context['object'].instruccionproduccion_set.all()
        for i in instrucciones:
            if i.plantilla_columna.nombre not in nombres:
                nombres.append(i.plantilla_columna.nombre)
                ids.append(i.plantilla_columna.id)
        context['parametros'] = Columna.objects.filter(pk__in=ids).order_by('id').all()
        return context

#Crear elaboración
@method_decorator(login_required,'dispatch')
class PautaProduccionCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso necesario
    permission_required = 'produccion.pauta.crear_pip'
    
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para fabricar una elaboración.'
    #template a utilizar
    template_name = 'produccion/pauta/productos_pip/create.html'
    #formulario a utilizar
    #formulario a utilizar
    form_class = PautaProduccionCreateForm
    success_url = reverse_lazy('produccion:lote:lista')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
       # Filtrar solo las plantillas de tipo 'PIP'
        form.fields['plantilla_pauta'].queryset =  Pauta.objects.filter(tipo='PIP')
        return form

    def form_valid(self, form):
        self.object = form.save()
        #obtenemos la plantilla que se esta utilizando
        plantilla_pauta = self.object.plantilla_pauta
        #guardamos los productos finales
        id_grupos = [int(id) for id in self.request.POST.getlist('grupo_id[]')]
        pva_grupos = [int(id) for id in self.request.POST.getlist('grupo_pva[]')]
        cantidades_grupos = [float(id) for id in self.request.POST.getlist('grupo_cantidad[]')]
        for i,id in enumerate(id_grupos):
            self.object.lineaproduccion_set.create(linea_id=id,cantidad=cantidades_grupos[i],final=False,pva_id=pva_grupos[i])
        #guardamos los productos finales
        id_productos = [int(id) for id in self.request.POST.getlist('producto_id[]')]
        cantidades_productos = [float(id) for id in self.request.POST.getlist('producto_cantidad[]')]
        for i,id in enumerate(id_productos):
            self.object.productoproduccion_set.create(producto_id=id,cantidad=cantidades_productos[i],final=False)
        #obtenemos los bultos
        bultos = [InsumoBulto.objects.filter(pk=int(x)).first() for x in self.request.POST.getlist('bultos[]')]
        #obtenemos las etapas
        plantilla_etapas = plantilla_pauta.etapa_set.all()
        #obtenemos las instrucciones
        for i,e in enumerate(plantilla_etapas):
            etapa_instruccion  = e.instruccion_set.all()
            for indexi,instruccion in enumerate(etapa_instruccion):
                for indexc,columna in enumerate(instruccion.instruccioncolumna_set.all()):
                    creado = self.object.instruccionproduccion_set.create(plantilla_instruccion_id=instruccion.id,plantilla_columna=columna.columna,valor=self.request.POST.get(f'etapa{i}instruccion{indexi}columna{indexc}',''))
        #guardamos las cantidades utilizadas
        cantidadingrediente = self.request.POST.getlist('cantidadingrediente[]')
        unidadingrediente = self.request.POST.getlist('unidadingrediente[]')
        insumoingrediente = [int(id) for id in self.request.POST.getlist('insumoingrediente[]')]
        for i,cantidad in enumerate(cantidadingrediente):
            #verificamos que el ingrediente pertenezca a la pauta
            ingrediented = plantilla_pauta.ingrediente_set.filter(insumo_id=insumoingrediente[i]).first()
            if ingrediented is None:
                ingrediented = plantilla_pauta.ingrediente_set.create(insumo_id=insumoingrediente[i],original=False,cantidad=float(cantidad),unidad=unidadingrediente[i])
            ingrediente,creado = self.object.ingredienteproduccion_set.get_or_create(plantilla_ingrediente=ingrediented,cantidad=float(cantidad),unidad=unidadingrediente[i])
            #RESTAR LOS INSUMOS DEL INVENTARIO
                    # Depuración - Verificamos los valores de la bodega y el insumo
  
            #obtención del inventario del insumo
            inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=ingrediente.plantilla_ingrediente.insumo,defaults={'cantidad': 0})
            #transformamos el ingrediente y su cantidad a la unidad estandar kilo/litro
            unidades = {'cc':1000,'gramo':1000,'kilogramo':1,'kilo':1,'miligramo':10000,'litro':1,'mililitro':1000,'tonelada':0.001,'kilolitro':0.001,'unidad':1,'caja':1,'n/a':1}
            cantidad_utilizada = round(ingrediente.cantidad / unidades[ingrediente.unidad],3)
            cantidad_bultos = cantidad_utilizada
            for b in bultos:
                if(b.insumo == ingrediente.plantilla_ingrediente.insumo and cantidad_bultos > 0):
                    disponible = (b.cantidad - b.cantidadu) * b.formato
                    if(cantidad_bultos > disponible):
                        cantidad_bultos-=disponible
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
                    elif(cantidad_bultos < disponible):
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=cantidad_bultos/b.formato)
                        cantidad_bultos = 0
                    else:
                        cantidad_bultos = 0
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
            #restamos al inventario la cantidad utilizada del insumo
            inventario.cantidad = round(inventario.cantidad - cantidad_utilizada,3)
            inventario.save()
        self.object.lugar = self.request.user.perfil.lugar
        #obtenemos sus grupos asociados
        idgrupos = [int(x) for x in self.request.POST.getlist('grupol_id[]')]
        pvagrupos = [int(x) for x in self.request.POST.getlist('grupol_pva[]')]

        cantidadgrupos = [float(x) for x in self.request.POST.getlist('grupol_cantidad[]')]
        #creamos los lotes de productos
        idproductos = [int(x) for x in self.request.POST.getlist('productol_id[]')]
        cantidadproductos = [float(x) for x in self.request.POST.getlist('productol_cantidad[]')]
        if(len(idgrupos) > 0):
            self.object.masa_final = sum(cantidadgrupos)
        if(len(idproductos) > 0):
            total = 0
            unidades = {'gr':0.001,'cc':0.001,'kg':1,'lt':1}
            for i,id in enumerate(idproductos):
                producto = Producto.objects.filter(pk=id).first()
                if producto:
                    total+= producto.presentacion * unidades[producto.unidad] * cantidadproductos[i]
            self.object.masa_final = total
        if self.object.masa_final is not None and self.object.masa_final > 0:
            self.object.rendimiento = round(self.object.cantidad / self.object.masa_final,2)
            self.object.estado = 'Segmentación'
        self.object.save()
        #valor de masa por kilos
        if self.object.masa_final is not None and self.object.masa_final != 0:
            valormasa = self.object.cdp / self.object.masa_final
        else:
            valormasa = 0
        for i,g in enumerate(idgrupos):
            if cantidadgrupos[i] > 0:
                #ver si el grupo de verdad existe
                check = Linea.objects.filter(pk=g).first()
                checkpva = ConjuntoEstado.objects.filter(pk=pvagrupos[i]).first()
                if check and checkpva:
                    lote = self.object.lote_set.create(producto=None,linea=check,pva=checkpva,cantidad=float(cantidadgrupos[i]),comentario="",cdp=valormasa*float(cantidadgrupos[i]))
                    historial_crear_lote(self.request.user,lote)
                    lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
        for i,g in enumerate(idproductos):
            if cantidadproductos[i] > 0:
                #ver si el producto de verdad existe
                check = Producto.objects.filter(pk=g).first()
                if check:
                    unidades = {'kg':1,'lt':1,'unidad':1,'gr':0.001,'mg':0.000001,'cc':0.001,'caja':1,'cajas':1,'n/a':1}
                    cantidadu = unidades[check.unidad]
                    peso = cantidadu * check.presentacion * int(cantidadproductos[i])
                    valor = peso * valormasa
                    lote = self.object.lote_set.create(producto=check,grupoproducto=None,cantidad=int(cantidadproductos[i]),comentario="",cdp=valor)
                    historial_crear_lote(self.request.user,lote)
                    lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
        #obtenemos sus ips asociados
        ips = plantilla_pauta.insumoproceso_set.all()
        paso = False
        try:
            cantidadip = [float(x) for x in self.request.POST.getlist('cantidadip[]')]
            paso = True
        except:
            cantidadip = self.request.POST.getlist('cantidadip[]')
            paso = False
        descripcionip = self.request.POST.getlist('descripcionip[]')
        for i,p in enumerate(ips):
            if cantidadip[i] != "":
                self.object.insumoprocesoproduccion_set.create(cantidad=float(cantidadip[i]),comentario=descripcionip[i],plantilla_ip=p)
                #sumamos al inventario la cantidad
                inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=p.insumo,defaults={'cantidad': 0})
                inventario.cantidad+=float(cantidadip[i])
                inventario.save()
        if (len(idgrupos) == len(idproductos) == 0) and paso:
            self.object.masa_final = sum(cantidadip)
            self.object.estado = 'Finalizada'
        if len(self.object.lote_set.all()) > 0:
            self.object.estado = 'Finalizada'
        self.object.save()
        historial_crear_elaboracion(self.request.user,self.object)
        return super().form_valid(form)


#Crear elaboración
@method_decorator(login_required,'dispatch')
class PautaProduccionCreateViewLinea(ValidatePermissionRequiredMixin,CreateView):
    #permiso necesario
    permission_required = 'produccion.pauta.crear_linea'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para fabricar una elaboración.'
    #template a utilizar
    template_name = 'produccion/pauta/producto_linea/create_linea.html'
    #formulario a utilizar
    form_class = PautaProduccionCreateForm
    success_url = reverse_lazy('produccion:lote:lista')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
       # Filtrar solo las plantillas de tipo 'PIP'
        form.fields['plantilla_pauta'].queryset =  Pauta.objects.filter(tipo='Linea')
        return form

    def form_valid(self, form):
        self.object = form.save()
        #obtenemos la plantilla que se esta utilizando
        plantilla_pauta = self.object.plantilla_pauta
        #guardamos los productos finales
        id_grupos = [int(id) for id in self.request.POST.getlist('grupo_id[]')]
        pva_grupos = [int(id) for id in self.request.POST.getlist('grupo_pva[]')]
        cantidades_grupos = [float(id) for id in self.request.POST.getlist('grupo_cantidad[]')]
        for i,id in enumerate(id_grupos):
            self.object.lineaproduccion_set.create(linea_id=id,cantidad=cantidades_grupos[i],final=False,pva_id=pva_grupos[i])
        #guardamos los productos finales
        id_productos = [int(id) for id in self.request.POST.getlist('producto_id[]')]
        cantidades_productos = [float(id) for id in self.request.POST.getlist('producto_cantidad[]')]
        for i,id in enumerate(id_productos):
            self.object.productoproduccion_set.create(producto_id=id,cantidad=cantidades_productos[i],final=False)
        #obtenemos los bultos
        bultos = [InsumoBulto.objects.filter(pk=int(x)).first() for x in self.request.POST.getlist('bultos[]')]
        #obtenemos las etapas
        plantilla_etapas = plantilla_pauta.etapa_set.all()
        #obtenemos las instrucciones
        for i,e in enumerate(plantilla_etapas):
            etapa_instruccion  = e.instruccion_set.all()
            for indexi,instruccion in enumerate(etapa_instruccion):
                for indexc,columna in enumerate(instruccion.instruccioncolumna_set.all()):
                    creado = self.object.instruccionproduccion_set.create(plantilla_instruccion_id=instruccion.id,plantilla_columna=columna.columna,valor=self.request.POST.get(f'etapa{i}instruccion{indexi}columna{indexc}',''))
        #guardamos las cantidades utilizadas
        cantidadingrediente = self.request.POST.getlist('cantidadingrediente[]')
        unidadingrediente = self.request.POST.getlist('unidadingrediente[]')
        insumoingrediente = [int(id) for id in self.request.POST.getlist('insumoingrediente[]')]
        for i,cantidad in enumerate(cantidadingrediente):
            #verificamos que el ingrediente pertenezca a la pauta
            ingrediented = plantilla_pauta.ingrediente_set.filter(insumo_id=insumoingrediente[i]).first()
            if ingrediented is None:
                ingrediented = plantilla_pauta.ingrediente_set.create(insumo_id=insumoingrediente[i],original=False,cantidad=float(cantidad),unidad=unidadingrediente[i])
            ingrediente,creado = self.object.ingredienteproduccion_set.get_or_create(plantilla_ingrediente=ingrediented,cantidad=float(cantidad),unidad=unidadingrediente[i])
            #RESTAR LOS INSUMOS DEL INVENTARIO
            #obtención del inventario del insumo
            inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=ingrediente.plantilla_ingrediente.insumo,defaults={'cantidad': 0})
            #transformamos el ingrediente y su cantidad a la unidad estandar kilo/litro
            unidades = {'cc':1000,'gramo':1000,'kilogramo':1,'kilo':1,'miligramo':10000,'litro':1,'mililitro':1000,'tonelada':0.001,'kilolitro':0.001,'unidad':1,'caja':1,'n/a':1}
            cantidad_utilizada = round(ingrediente.cantidad / unidades[ingrediente.unidad],3)
            cantidad_bultos = cantidad_utilizada
            for b in bultos:
                if(b.insumo == ingrediente.plantilla_ingrediente.insumo and cantidad_bultos > 0):
                    disponible = (b.cantidad - b.cantidadu) * b.formato
                    if(cantidad_bultos > disponible):
                        cantidad_bultos-=disponible
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
                    elif(cantidad_bultos < disponible):
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=cantidad_bultos/b.formato)
                        cantidad_bultos = 0
                    else:
                        cantidad_bultos = 0
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
            #restamos al inventario la cantidad utilizada del insumo
            inventario.cantidad = round(inventario.cantidad - cantidad_utilizada,3)
            inventario.save()
        self.object.lugar = self.request.user.perfil.lugar
        #obtenemos sus grupos asociados
        idgrupos = [int(x) for x in self.request.POST.getlist('grupol_id[]')]
        pvagrupos = [int(x) for x in self.request.POST.getlist('grupol_pva[]')]

        cantidadgrupos = [float(x) for x in self.request.POST.getlist('grupol_cantidad[]')]
        #creamos los lotes de productos
        idproductos = [int(x) for x in self.request.POST.getlist('productol_id[]')]
        cantidadproductos = [float(x) for x in self.request.POST.getlist('productol_cantidad[]')]
        if(len(idgrupos) > 0):
            self.object.masa_final = sum(cantidadgrupos)
        if(len(idproductos) > 0):
            total = 0
            unidades = {'gr':0.001,'cc':0.001,'kg':1,'lt':1}
            for i,id in enumerate(idproductos):
                producto = Producto.objects.filter(pk=id).first()
                if producto:
                    total+= producto.presentacion * unidades[producto.unidad] * cantidadproductos[i]
            self.object.masa_final = total
        if self.object.masa_final is not None and self.object.masa_final > 0:
            self.object.rendimiento = round(self.object.cantidad / self.object.masa_final,2)
            self.object.estado = 'Segmentación'
        self.object.save()
        #valor de masa por kilos
        if self.object.masa_final is not None and self.object.masa_final != 0:
            valormasa = self.object.cdp / self.object.masa_final
        else:
            valormasa = 0
        for i,g in enumerate(idgrupos):
            if cantidadgrupos[i] > 0:
                #ver si el grupo de verdad existe
                check = Linea.objects.filter(pk=g).first()
                checkpva = ConjuntoEstado.objects.filter(pk=pvagrupos[i]).first()
                if check and checkpva:
                    lote = self.object.lote_set.create(producto=None,linea=check,pva=checkpva,cantidad=float(cantidadgrupos[i]),comentario="",cdp=valormasa*float(cantidadgrupos[i]))
                    historial_crear_lote(self.request.user,lote)
                    lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
        for i,g in enumerate(idproductos):
            if cantidadproductos[i] > 0:
                #ver si el producto de verdad existe
                check = Producto.objects.filter(pk=g).first()
                if check:
                    unidades = {'kg':1,'lt':1,'unidad':1,'gr':0.001,'mg':0.000001,'cc':0.001,'caja':1,'cajas':1,'n/a':1}
                    cantidadu = unidades[check.unidad]
                    peso = cantidadu * check.presentacion * int(cantidadproductos[i])
                    valor = peso * valormasa
                    lote = self.object.lote_set.create(producto=check,grupoproducto=None,cantidad=int(cantidadproductos[i]),comentario="",cdp=valor)
                    historial_crear_lote(self.request.user,lote)
                    lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
        #obtenemos sus ips asociados
        ips = plantilla_pauta.insumoproceso_set.all()
        paso = False
        try:
            cantidadip = [float(x) for x in self.request.POST.getlist('cantidadip[]')]
            paso = True
        except:
            cantidadip = self.request.POST.getlist('cantidadip[]')
            paso = False
        descripcionip = self.request.POST.getlist('descripcionip[]')
        for i,p in enumerate(ips):
            if cantidadip[i] != "":
                self.object.insumoprocesoproduccion_set.create(cantidad=float(cantidadip[i]),comentario=descripcionip[i],plantilla_ip=p)
                #sumamos al inventario la cantidad
                inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=p.insumo,defaults={'cantidad': 0})
                inventario.cantidad+=float(cantidadip[i])
                inventario.save()
        if (len(idgrupos) == len(idproductos) == 0) and paso:
            self.object.masa_final = sum(cantidadip)
            self.object.estado = 'Finalizada'
        if len(self.object.lote_set.all()) > 0:
            self.object.estado = 'Finalizada'
        self.object.save()
        historial_crear_elaboracion(self.request.user,self.object)
        return super().form_valid(form)


#actualizar Elaboración
@method_decorator(login_required,'dispatch')
class PautaProduccionUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso necesario
    permission_required = 'produccion.pauta.actualizar'
    #modelo a utilizar
    model = PautaProduccion
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una elaboración.'
    #template a utilizar
    template_name = 'produccion/pauta/update.html'
    #formulario a utilizar
    form_class = PautaProduccionUpdateForm
    success_url = reverse_lazy('produccion:lote:lista')
    #como llamar el objeto
    context_object_name = "pauta"

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            context['total'] = 0
            for producto in self.object.lineaproduccion_set.all():
                if producto.final == False:
                    context['total']+=producto.cantidad
        context.update(kwargs)
        
        return super().get_context_data(**context)

    #proceso de guardado
    def form_valid(self, form):
        self.object = form.save()
        #obtenemos la plantilla que se esta utilizando
        plantilla_pauta = self.object.plantilla_pauta
        #guardamos los grupos finales
        id_grupos = [int(id) for id in self.request.POST.getlist('grupo_id[]')]
        pva_grupos = [int(id) for id in self.request.POST.getlist('grupo_pva[]')]
        cantidades_grupos = [float(id) for id in self.request.POST.getlist('grupo_cantidad[]')]
        for i,id in enumerate(id_grupos):
            #vemos si ya existe para esa id
            existe = self.object.lineaproduccion_set.filter(linea=id,pva=pva_grupos[i],final=False).first()
            if existe:
                existe.cantidad = cantidades_grupos[i]
                existe.save()
            else:
                self.object.grupoproductoproduccion_set.create(linea=id,pva=pva_grupos[i],cantidad=cantidades_grupos[i],final=False)
        #borramos los que no estan
        eliminar = [grupo for grupo in self.object.lineaproduccion_set.all() if ( (grupo.linea.id not in id_grupos) and (grupo.pva.id not in pva_grupos) )]
        for e in eliminar:
            e.delete()
        #guardamos los productos finales
        id_productos = [int(id) for id in self.request.POST.getlist('producto_id[]')]
        cantidades_productos = [float(id) for id in self.request.POST.getlist('producto_cantidad[]')]
        for i,id in enumerate(id_productos):
            #vemos si ya existe para esa id
            existe = self.object.productoproduccion_set.filter(producto_id=id,final=False).first()
            if existe:
                existe.cantidad = cantidades_productos[i]
                existe.save()
            else:
                self.object.productoproduccion_set.create(producto_id=id,cantidad=cantidades_productos[i],final=False)
        #borramos los que no estan
        eliminar = [producto for producto in self.object.productoproduccion_set.all() if producto.producto.id not in id_productos]
        for e in eliminar:
            e.delete()
        #obtenemos las etapas
        plantilla_etapas = plantilla_pauta.etapa_set.all()
        for i,e in enumerate(plantilla_etapas):
            etapa_instruccion  = e.instruccion_set.all()
            for indexi,instruccion in enumerate(etapa_instruccion):
                for indexc,columna in enumerate(instruccion.instruccioncolumna_set.all()):
                    ins,created = self.object.instruccionproduccion_set.get_or_create(
                    plantilla_instruccion=instruccion,
                    plantilla_columna=columna.columna,
                    defaults={'valor':self.request.POST.get(f'etapa{i}instruccion{indexi}columna{indexc}','')}
                )
                if created is False:
                    ins.valor = self.request.POST.get(f'etapa{i}instruccion{indexi}columna{indexc}','')
                    ins.save()
       #obtenemos sus grupos asociados
        idgrupos = [int(x) for x in self.request.POST.getlist('grupol_id[]')]
        pvagrupos = [int(x) for x in self.request.POST.getlist('grupol_pva[]')]
        cantidadgrupos = [float(x) for x in self.request.POST.getlist('grupol_cantidad[]')]
        #creamos los lotes de productos
        idproductos = [int(x) for x in self.request.POST.getlist('productol_id[]')]
        cantidadproductos = [float(x) for x in self.request.POST.getlist('productol_cantidad[]')]
        if(len(idgrupos) > 0):
            if sum(cantidadgrupos) > 0:
                self.object.masa_final
        if(len(idproductos) > 0):
            total = 0
            unidades = {'gr':0.001,'cc':0.001,'kg':1,'lt':1}
            for i,id in enumerate(idproductos):
                producto = Producto.objects.filter(pk=id).first()
                if producto and cantidadproductos[i] > 0:
                    total+= producto.presentacion * unidades[producto.unidad] * cantidadproductos[i]
            if total > 0:
                self.object.masa_final = total
        #valor de masa por kilos
        if self.object.masa_final is not None and self.object.masa_final > 0:
            valormasa = self.object.cdp / self.object.masa_final
        else:
            valormasa = 0
        for i,g in enumerate(idgrupos):
            #ver si el grupo de verdad existe
            check = Linea.objects.filter(pk=g).first()
            checkpva = ConjuntoEstado.objects.filter(pk=pvagrupos[i]).first()
            if cantidadgrupos[i] > 0:
                if check and checkpva:
                    #ver si el grupo ya existe en esta pauta
                    existe = self.object.lote_set.filter(producto=None,linea=check,pva=checkpva).first()
                    if existe:
                        existe.cantidad = float(cantidadgrupos[i])
                        existe.cdp = valormasa*float(cantidadgrupos[i])
                        historial_actualizar_lote(self.request.user,existe)
                        existe.save()
                    else:
                        lote = self.object.lote_set.create(producto=None,linea=check,pva=checkpva,cdp=valormasa*float(cantidadgrupos[i]),cantidad=float(cantidadgrupos[i]),comentario="")
                        historial_crear_lote(self.request.user,lote)
                        lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
            else:
                existe = self.object.lote_set.filter(producto=None,linea=check,pva=checkpva).first()
                if existe:
                    historial_eliminar_lote(self.request.user,existe)
                    existe.delete()
        #eliminar los que no existe
        eliminar = [lote for lote in self.object.lote_set.filter(producto=None).all() if ( (lote.linea.id not in idgrupos) and (lote.pva.id not in pvagrupos))]
        for e in eliminar:
            e.delete()
        #obtenemos sus productos asociados
        for i,p in enumerate(idproductos):
            #ver si el producto de verdad existe
            check = Producto.objects.filter(pk=p).first()
            if cantidadproductos[i] > 0:
                if check:
                    unidades = {'kg':1,'lt':1,'unidad':1,'gr':0.001,'mg':0.000001,'cc':0.001,'caja':1,'cajas':1,'n/a':1}
                    cantidadu = unidades[check.unidad]
                    peso = cantidadu * check.presentacion * int(cantidadproductos[i])
                    valor = peso * valormasa
                    #ver si el grupo ya existe en esta pauta
                    existe = self.object.lote_set.filter(producto=check,grupoproducto=None).first()
                    if existe:
                        existe.cantidad = int(cantidadproductos[i])
                        existe.cdp = valor
                        historial_actualizar_lote(self.request.user,existe)
                        existe.save()
                    else:
                        lote = self.object.lote_set.create(producto=check,grupoproducto=None,cdp=valor,cantidad=int(cantidadproductos[i]),comentario="")
                        historial_crear_lote(self.request.user,lote)
                        lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar)
            else:
                existe = self.object.lote_set.filter(producto=check,linea=None,pva=None).first()
                if existe:
                    historial_eliminar_lote(self.request.user,existe)
                    existe.delete()
        #eliminar los que no existe
        eliminar = [lote for lote in self.object.lote_set.filter(linea=None,pva=None).all() if lote.producto_id not in idproductos]
        for e in eliminar:
            e.delete()
        #obtenemos los bultos
        bultos = [InsumoBulto.objects.filter(pk=int(x)).first() for x in self.request.POST.getlist('bultos[]')]
        #obtenemos sus ingredientes
        ingredientes = plantilla_pauta.ingrediente_set.all()
        #actualizamos las cantidades utilizadas
        cantidadingrediente = self.request.POST.getlist('cantidadingrediente[]')
        unidadingrediente = self.request.POST.getlist('unidadingrediente[]')
        insumoingrediente = [int(id) for id in self.request.POST.getlist('insumoingrediente[]')]
        for i,cantidad in enumerate(cantidadingrediente):
            #verificamos que el ingrediente pertenezca a la pauta
            ingrediented = plantilla_pauta.ingrediente_set.filter(insumo_id=insumoingrediente[i]).first()
            if ingrediented is None:
                ingrediented = plantilla_pauta.ingrediente_set.create(insumo_id=insumoingrediente[i],original=False,cantidad=float(cantidad),unidad=unidadingrediente[i])
            else:
                if ingrediented.original is False:
                    ingrediented.cantidad = float(cantidad)
                    ingrediented.save()
            ingrediente,creado = self.object.ingredienteproduccion_set.get_or_create(plantilla_ingrediente=ingrediented,defaults={'cantidad':float(cantidad),'unidad':unidadingrediente[i]})
            #RESTAR LOS INSUMOS DEL INVENTARIO
            #obtención del inventario del insumo
            inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=ingrediente.plantilla_ingrediente.insumo,defaults={'cantidad': 0})
            #transformamos el ingrediente y su cantidad a la unidad estandar kilo/litro
            unidades = {'gramo':1000,'kilogramo':1,'kilo':1,'miligramo':10000,'litro':1,'mililitro':1000,'cc':1000,'tonelada':0.001,'kilolitro':0.001,'unidad':1,'caja':1,'n/a':1}
            cantidad_utilizada = round(ingrediente.cantidad / unidades[ingrediente.unidad],3)
            cantidad_nueva = round(float(cantidadingrediente[i]) / unidades[unidadingrediente[i]],3)
            cantidad_bultos = cantidad_nueva
            #eliminamos los anteriores
            self.object.bultopautaproduccion_set.all().delete()
            for b in bultos:
                if(b.insumo == ingrediente.plantilla_ingrediente.insumo and cantidad_bultos > 0):
                    disponible = (b.cantidad - b.cantidadu) * b.formato
                    if(cantidad_bultos > disponible):
                        cantidad_bultos-=disponible
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
                    elif(cantidad_bultos < disponible):
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=cantidad_bultos/b.formato)
                        cantidad_bultos = 0
                    else:
                        cantidad_bultos = 0
                        self.object.bultopautaproduccion_set.create(bulto=b,cantidad=disponible/b.formato)
            #restamos al inventario la cantidad utilizada del insumo
            inventario.cantidad = round(inventario.cantidad + cantidad_utilizada - cantidad_nueva,3)
            inventario.save()
            ingrediente.cantidad = float(cantidadingrediente[i])
            ingrediente.unidad = unidadingrediente[i]
            ingrediente.save()
        #eliminamos los ingredientes que no pertencen
        ingredientespro = self.object.ingredienteproduccion_set.all()
        lista = [ingrediente for ingrediente in ingredientespro if ingrediente.plantilla_ingrediente.insumo.id not in insumoingrediente]
        for ingrediente in lista:
            #obtención del inventario del insumo
            inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=ingrediente.plantilla_ingrediente.insumo,defaults={'cantidad': 0})
            #transformamos el ingrediente y su cantidad a la unidad estandar kilo/litro
            unidades = {'gramo':1000,'kilogramo':1,'kilo':1,'miligramo':10000,'litro':1,'mililitro':1000,'cc':1000,'tonelada':0.001,'kilolitro':0.001,'unidad':1,'caja':1,'n/a':1}
            cantidad_utilizada = round(ingrediente.cantidad / unidades[ingrediente.unidad],3)
            #restamos al inventario la cantidad utilizada del insumo
            inventario.cantidad = round(inventario.cantidad + cantidad_utilizada,3)
            inventario.save()
            ingrediente.delete()
        #obtenemos sus ips asociados
        ips = plantilla_pauta.insumoproceso_set.all()
        #obtenemos los ips actuales
        try:
            cantidadip = [float(x) for x in self.request.POST.getlist('cantidadip[]')]
            paso=True
        except:
            cantidadip = self.request.POST.getlist('cantidadip[]')
            paso=False
        descripcionip = self.request.POST.getlist('descripcionip[]')
        for i,p in enumerate(ips):
            inventario,created = InventarioInsumo.objects.get_or_create(bodega=self.request.user.perfil.lugar,insumo=p.insumo,defaults={'cantidad': 0})
            if cantidadip[i] != "":
                ip,creado = self.object.insumoprocesoproduccion_set.get_or_create(defaults={'cantidad':float(cantidadip[i]),'comentario':descripcionip[i]},plantilla_ip=p)
                if creado is False:
                    cantidada = ip.cantidad
                    #sumamos al inventario la cantidad
                    inventario.cantidad-=cantidada
                    ip.cantidad = float(cantidadip[i])
                    ip.comentario = descripcionip[i]
                    inventario.cantidad+=float(cantidadip[i])
                else:
                    inventario.cantidad = float(cantidadip[i])
                ip.save()
            else:
                if InsumoProcesoProduccion.objects.filter(plantilla_ip=p,pauta_produccion=self.object).exists():
                    ipp = self.object.insumoprocesoproduccion_set.get(plantilla_ip=p).first()
                    inventario.cantidad-=ipp.cantidad
                    ipp.delete()
            inventario.save()

        if self.object.masa_final is not None and self.object.masa_final >= 0:
            if self.object.masa_final > 0:
                self.object.rendimiento = round(self.object.cantidad / self.object.masa_final,2)
                self.object.estado = 'Segmentación'
            else:
                self.object.estado = 'Inicial'
        if (len(idgrupos) == len(idproductos) == 0) and paso:
            self.object.masa_final = sum(cantidadip)
            self.object.estado = 'Finalizada'
        if len(self.object.lote_set.all()) > 0:
            self.object.estado = 'Finalizada'
            

        
        self.object.save()
        historial_actualizar_elaboracion(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())
#eliminar Elaboración
@method_decorator(login_required,'dispatch')
class PautaProduccionDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'produccion.pauta.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            pauta = get_object_or_404(PautaProduccion,pk=kwargs.get('pk'))
            historial_eliminar_elaboracion(self.request.user,pauta)
            pauta.delete()
            return JsonResponse({'estado':'ok','pauta':pauta.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})


#LOTES

#Lista de los lotes
@method_decorator(login_required,'dispatch')
class LoteList(ValidatePermissionRequiredMixin,TemplateView):
    #permiso necesario
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los lotes.'
    #template a utilizar
    template_name = 'produccion/lote/list.html'

#Detalle de lote
@method_decorator(login_required,'dispatch')
class LoteDetailView(ValidatePermissionRequiredMixin,DetailView):
    #permiso necesario
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el lote.'
    #template a utilizar
    template_name = 'produccion/lote/detail.html'
    model = Lote

    def get(self, request, *args, **kwargs):
        from reportlab.graphics import renderPDF
        unidad = request.GET.get('unidad')
        if unidad is not None:
            try:
                unidad = int(unidad)
            except:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            self.object = self.get_object()
            unidad = self.object.producto.unidades
            cantidad_actual = self.object.cantidadactual()
            cajas = int(cantidad_actual // int(unidad)) 
            resto = int(cantidad_actual % int(unidad))
            if resto != 0:
                cajas+=1
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf'.format(self.object.numero)
            dimensiones = (378,265)
            p = canvas.Canvas(response,pagesize=dimensiones)
            p.setTitle("Lote {}".format(self.object.numero))
            for i in range(1,cajas+1):
                unidades = resto if (i==cajas and resto !=0) else unidad
                check = CajaLote.objects.filter(lote=self.object,caja=i,cantidad=unidades).first()
                if check is None:
                    self.object.cajalote_set.create(caja=i,cantidad=unidades,lugar=self.object.pauta_produccion.lugar)
                generar_codigo(p,self.object,i,unidades)
            p.save()
            return response
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

#En Maduración
@method_decorator(login_required, "dispatch")
class LoteMaduracionView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'produccion.pauta.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver la maduración'
    template_name = 'produccion/lote/maduracion/maduracion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dias_busqueda = self.request.GET.get('dias', None)

        if dias_busqueda is not None:
            context["productos"] = Producto.objects.filter(maduracion=dias_busqueda)
        else:
            context["productos"] = Producto.objects.all()

        return context

    
#API Para Consultar estado del lote al momento de escanear
@method_decorator(login_required,'dispatch')
class LoteRetrieveScanApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los lotes.'
    serializer_class = LoteSerializer

    def get_queryset(self):
        caja = self.request.GET.get('caja')
        unidades = self.request.GET.get('unidades')
        lote = Lote.objects.filter(pk=self.kwargs.get('pk')).first()
        #obtenemos la caja, y verificamos que se encuentre en el lugar desde donde se realizara el envio
        cajalote = CajaLote.objects.filter(lote=lote,caja=int(caja),cantidad=int(unidades),lugar=self.request.user.perfil.lugar).first()
        #si es que existe la caja
        if cajalote:
            lote_e = cajalote.loteenvio_set.last()
            #si es que la caja ya ha sido transportada una vez
            if lote_e is not None:
                #si el ultimo envio ya termino
                if lote_e.recepcionado is not None:
                    return Lote.objects.filter(pk=self.kwargs.get('pk'))
                else:
                    raise Http404
            #si la caja no ha sido transportada en ninguna oportunidad
            else:
                return Lote.objects.filter(pk=self.kwargs.get('pk'))
        #si no existe se devuelve error
        else:
            raise Http404


#API Para Consultar la cajalote al momento de escanear
@method_decorator(login_required,'dispatch')
class CajaLoteRetrieveScanApi(ValidatePermissionRequiredMixin,RetrieveAPIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los lotes.'
    serializer_class = CajaLoteSerializer

    def get_object(self):
        caja = self.request.GET.get('caja')
        unidades = self.request.GET.get('unidades')
        lote = Lote.objects.filter(pk=self.kwargs.get('pk')).first()
        #obtenemos la caja, y verificamos que se encuentre en el lugar desde donde se realizara el envio
        cajalote = CajaLote.objects.filter(lote=lote,caja=int(caja),cantidad=int(unidades),lugar=self.request.user.perfil.lugar).first()
        #si es que existe la caja
        if cajalote:
            if cajalote.estado in ['Recepcionado','Produccion']:
                return cajalote
        else:
            raise Http404

#Generación codigos de barra interno
class LoteCodigoBarraView(ValidatePermissionRequiredMixin,DetailView):
    #permiso necesario
    permission_required = 'produccion.pauta.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el lote.'
    #template a utilizar
    template_name = 'produccion/lote/print.html'
    model = Lote

    def get(self, request, *args, **kwargs):
        from reportlab.graphics import renderPDF
        unidad = request.GET.get('unidad')
        if unidad != '' and unidad is not None:
            try:
                unidad = int(unidad)
            except:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            self.object = self.get_object()
            cantidad_actual = self.object.cantidadactual()
            cajas = int(cantidad_actual // int(unidad)) 
            resto = int(cantidad_actual % int(unidad))
            if resto != 0:
                cajas+=1
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf'.format(self.object.numero)
            dimensiones = (15*mm,15*mm)
            p = canvas.Canvas(response,pagesize=dimensiones)
            p.setTitle("Lote {}".format(self.object.numero))
            for i in range(1,cajas+1):
                unidades = resto if (i==cajas and resto !=0) else unidad
                check = CajaLote.objects.filter(lote=self.object,caja=i,cantidad=unidades).first()
                if check is None:
                    self.object.cajalote_set.create(caja=i,cantidad=unidades,lugar=self.object.pauta_produccion.lugar)
                generar_codigo(p,self.object,i,unidades)
            
               #image = image.resize(image,100,100)

            p.save()
            return response
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

#Eliminar Lote
@method_decorator(login_required,'dispatch')
class LoteDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'produccion.pauta.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            lote = get_object_or_404(Lote,pk=kwargs.get('pk'))
            historial_eliminar_lote(self.request.user,lote)
            lote.delete()
            return JsonResponse({'estado':'ok','lote':lote.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Cambiar Estado de lote
@method_decorator(login_required,'dispatch')
class LoteUpdateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso
    permission_required = 'produccion.pauta.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar los lotes.'
    #template a utilizar
    template_name = 'produccion/lote/create.html'
    form_class = EstadoLoteCreateForm
    model = Lote
    success_url = reverse_lazy('produccion:lote:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lote = Lote.objects.filter(pk=int(self.kwargs.get('pk'))).first()
        if lote is None:
            raise Http404('Error')
        context['estado'] = lote.proximo_estado()
        context['pesoa'] = lote.ultimo_peso()
        if context['estado'] is None:
            raise Http404('No hay proximo estado.')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        estado = self.object.estadolote_set.last()
        if estado and estado.nombre == 'Empacado':
            raise Http404

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.encargado = self.request.user
        self.object.lote = Lote.objects.filter(pk=int(self.kwargs.get('pk'))).first()
        proximo = self.object.lote.proximo_estado()
        self.object.nombre = proximo.nombre
        self.object.estadoGlobal = self.object.lote.proximo_estado() if proximo.nombre not in ["Separación",'Empaque Final'] else None
        self.object.nombre = self.object.nombre if proximo.nombre != 'Empaque Final' else 'Empacado'
        self.object.lugar = self.object.lote.pauta_produccion.lugar
        self.object.save()
        #vemos si es que hay productos
        productos =[int(id) for id in self.request.POST.getlist('id_producto[]')]
        pauta = self.object.lote.pauta_produccion
        if len(productos) > 0:
            unidadese = [int(id) for id in self.request.POST.getlist('unidadese[]')]
            unidadesc = [int(id) for id in self.request.POST.getlist('unidadesc[]')]
            unidadesff = [int(id) for id in self.request.POST.getlist('unidadesff[]')]
            unidadesnc = [int(id) for id in self.request.POST.getlist('unidadesnc[]')]
            for i, p in enumerate(productos):
                if (unidadese[i] > 0):
                    producto = Producto.objects.filter(pk=p).first()
                    if producto:
                        unidades = {'kg':1,'gr':0.001,'lt':1,'ml':0.001}
                        unidad = unidades[producto.unidad]
                        presentacion = unidad * producto.presentacion
                        cdp = self.object.lote.cdp / self.object.lote.cantidadactual()
                        cdpp = presentacion * cdp
                        print(cdpp)
                        lote = pauta.lote_set.create(producto_id=p, pva=self.object.lote.pva,linea=self.object.lote.linea, cantidad=unidadese[i], comentario="",cdp=cdpp)
                        historial_crear_lote(self.request.user,lote)
                        lote.estadolote_set.create(nombre="Inicial",lugar=self.request.user.perfil.lugar,unidadesNC=unidadesnc[i],unidadesFF=unidadesff[i],unidadesC=unidadesc[i])
        #vemos si hay insumos
        insumos = [int(id) for id in self.request.POST.getlist('insumo_id[]')]
        if len(insumos) > 0:
            cantidad_insumos = [float(id) for id in self.request.POST.getlist('insumo_cantidad[]')]
            #verificamos que el insumo exista en la pauta
            #ver si es que hay conjunto
            conjunto = self.object.lote.producto.conjunto
            if conjunto is not None:
                check = conjunto.estadoconjunto_set.filter(estado__nombre=self.object.nombre).first()
                if check:
                    for i,id in enumerate(insumos):
                        insumos = check.estado.estadoinsumo_set.filter(insumo_id=id).first()
                        if insumos is not None:
                            self.object.estadoloteinsumo_set.create(insumo_id=id,cantidad=cantidad_insumos[i])
        return HttpResponseRedirect(self.get_success_url())
    
    def get(self, request, *args, **kwargs):
        from reportlab.graphics import renderPDF
        unidad = request.GET.get('unidad')
        if unidad is not None:
            try:
                unidad = int(unidad)
            except:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
            self.object = self.get_object()
            unidad = self.object.producto.unidades
            cantidad_actual = self.object.cantidadactual()
            cajas = int(cantidad_actual // int(unidad)) 
            resto = int(cantidad_actual % int(unidad))
            if resto != 0:
                cajas+=1
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf'.format(self.object.numero)
            dimensiones = (378,265)
            p = canvas.Canvas(response,pagesize=dimensiones)
            p.setTitle("Lote {}".format(self.object.numero))
            for i in range(1,cajas+1):
                unidades = resto if (i==cajas and resto !=0) else unidad
                check = CajaLote.objects.filter(lote=self.object,caja=i,cantidad=unidades).first()
                if check is None:
                    self.object.cajalote_set.create(caja=i,cantidad=unidades,lugar=self.object.pauta_produccion.lugar)
                generar_codigo(p,self.object,i,unidades)
            p.save()
            return response
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

#Eliminar estado de lote
@method_decorator(login_required,'dispatch')
class EstadoLoteDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'produccion.elote.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            estado = get_object_or_404(EstadoLote,pk=kwargs.get('pk'))
            if estado.nombre == 'Separación':
                linea = estado.lote.linea
                if linea:
                    qr = [producto for producto in Producto.objects.filter(conjunto=estado.lote.pva,linea=linea).all()]
                    lotes = estado.lote.pauta_produccion.lote_set.filter(producto__in=qr)
                    check = False
                    for l in lotes:
                        if l.estado() in ['Empacado','En Transito','Recepcionado']:
                            check = True
                    if check:
                        return JsonResponse({'estado':'fallo'})
                    for l in lotes:
                        l.delete()
            #historial_eliminar_lote(self.request.user,estado)
            estado.delete()
            return JsonResponse({'estado':'ok','elote':estado.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#ENVIOS#

#Prueba de envio
@method_decorator(login_required,'dispatch')
class EnvioView(ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'produccion/envios/prueba.html'

#Prueba de envio
from django.utils import timezone
import json
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import now

import pandas as pd
from django.shortcuts import render
from .models import PautaProduccion, Lote
from django.db.models import Q
from .models import PautaProduccion, Lote
import pandas as pd

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io
from django.shortcuts import render
import pandas as pd
from .models import PautaProduccion
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
import datetime
from .models import PautaProduccion

from django.db.models import Sum, Count, F
from django.db.models import Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView
from collections import defaultdict
from django.db.models import Sum, Count
from django.shortcuts import render
from django.views.generic import TemplateView
from collections import defaultdict


@method_decorator(login_required, 'dispatch')
class NivelView(TemplateView):
    template_name = 'produccion/lote/nivel/nivel.html'

    def parse_fecha(self, fecha_str):
        if fecha_str:
            try:
                return datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
            except ValueError:
                return None
        return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener filtros de la URL
        fecha_inicio = self.parse_fecha(self.request.GET.get('fecha_inicio'))
        fecha_fin = self.parse_fecha(self.request.GET.get('fecha_fin'))
        lote_filter = self.request.GET.get('lote', '')
        pauta_filter = self.request.GET.get('pauta', '')

        # Obtener las pautas con filtros aplicados
        pautas = PautaProduccion.objects.select_related('plantilla_pauta')

        # Aplicar filtros de fecha
        if fecha_inicio and fecha_fin:
            fecha_fin += datetime.timedelta(days=1)  # Incluir todo el día de 'fecha_fin'
            pautas = pautas.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            pautas = pautas.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            fecha_fin += datetime.timedelta(days=1)
            pautas = pautas.filter(fecha__lte=fecha_fin)

        # Filtrar por lote y pauta
        if lote_filter:
            pautas = pautas.filter(lote__icontains=lote_filter)
        if pauta_filter:
            pautas = pautas.filter(plantilla_pauta__nombre__icontains=pauta_filter)

        # Preparar los datos para los gráficos
        pautas_data = pautas.values('fecha', 'plantilla_pauta__tipo').annotate(
            cantidad_total=Sum('cantidad'),
            lotes_hechos=Count('id')
        ).order_by('fecha')

        # Separar los datos por tipo de pauta
        pauta_info_pip = [pauta for pauta in pautas_data if pauta['plantilla_pauta__tipo'] == 'PIP']
        pauta_info_linea = [pauta for pauta in pautas_data if pauta['plantilla_pauta__tipo'] == 'Linea']

        # Convertir las fechas a cadenas para su uso en los gráficos
        for pauta in pauta_info_pip + pauta_info_linea:
            pauta['fecha'] = pauta['fecha'].strftime('%Y-%m-%d')

        # Pasa los datos filtrados al contexto
        context['pauta_info_pip'] = pauta_info_pip
        context['pauta_info_linea'] = pauta_info_linea

        # Preparar los datos para los gráficos
        context['grafico_lotes_pip'] = pauta_info_pip
        context['grafico_cantidad_pip'] = pauta_info_pip
        context['grafico_lotes_linea'] = pauta_info_linea
        context['grafico_cantidad_linea'] = pauta_info_linea

        # Pautas disponibles para el filtro
        context['pautas_nombres'] = PautaProduccion.objects.values_list('plantilla_pauta__nombre', flat=True).distinct()
        return context
    
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
import datetime
# Vista para generar el PDF
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.views.generic import View
from .models import PautaProduccion


class GenerarPDFView(View):
    def get(self, request, *args, **kwargs):
        # Capturamos los parámetros de la URL
        fecha_inicio = request.GET.get('fecha_inicio', None)
        fecha_fin = request.GET.get('fecha_fin', None)
        pauta = request.GET.get('pauta', None)

        # Obtener las pautas con filtros aplicados
        pautas = PautaProduccion.objects.select_related('plantilla_pauta')

        # Filtrar las pautas por fecha y otros parámetros
        if fecha_inicio and fecha_fin:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d') + datetime.timedelta(days=1)
            pautas = pautas.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            pautas = pautas.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d') + datetime.timedelta(days=1)
            pautas = pautas.filter(fecha__lte=fecha_fin)

        if pauta:
            pautas = pautas.filter(plantilla_pauta__nombre__icontains=pauta)

        # Procesar los datos para los gráficos
        pautas_data = pautas.values('fecha', 'plantilla_pauta__tipo', 'plantilla_pauta__nombre').annotate(
            cantidad_total=Sum('cantidad'),
            lotes_hechos=Count('id')
        ).order_by('fecha')


        # Separar los datos por tipo de pauta
        pauta_info_pip = [pauta for pauta in pautas_data if pauta['plantilla_pauta__tipo'] == 'PIP']
        pauta_info_linea = [pauta for pauta in pautas_data if pauta['plantilla_pauta__tipo'] == 'Linea']

        # Convertir las fechas a cadenas para usarlas en el HTML
        for pauta in pauta_info_pip + pauta_info_linea:
            pauta['fecha'] = pauta['fecha'].strftime('%Y-%m-%d')

        # Preparar el contexto para el template
        context = {
            'fecha_inicio': fecha_inicio or "No especificada",
            'fecha_fin': fecha_fin or "No especificada",
            'pauta': pauta or "No especificada",
            'pauta_info_pip': pauta_info_pip,
            'pauta_info_linea': pauta_info_linea,
        }


        # Renderizar el HTML con el contexto
        html = render_to_string('produccion/lote/nivel/nivel_pdf.html', context)

        # Convertir el HTML a PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_produccion.pdf"'  # Esto fuerza la descarga
        
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF', status=500)
        
        return response
