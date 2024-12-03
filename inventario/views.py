from logistica.models import LoteEnvio
from produccion.models import EstadoLote
from nucleo.models import Producto
from django.db.models import F, Q
import statistics
from produccion.models import Lote
from nucleo.models import Rama
from django.shortcuts import render
from .models import Bodega, HistorialBodega, InsumoBulto, InventarioInsumo, InventarioProducto
from ordendecompra.models import OrdenDeCompraInsumo
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, View, UpdateView
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import DetailView
from rest_framework.generics import RetrieveAPIView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .serializers import BodegaSerializer, HistorialBodegaSerializer, InsumoBultoSerializer, InventarioProductoSerializer, InventarioSerializer
from .forms import BodegaForm, BodegaHistorialForm, HistorialBodegaForm, InventarioInsumoUpdateForm, InventarioProductoUpdateForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.db.models import Sum, Max
from rest_framework.views import APIView
from django.core import serializers
from .functions import historial_create_bodega, historial_delete_bodega, historial_update_bodega, historial_update_inventarioi
import copy
import collections

# BODEGAS
#Generación de la api de las bodegas para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class BodegaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    
    #permiso necesario
    permission_required = 'inventario.bodega.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las bodegas.'

#Lista de bodegas
@method_decorator(login_required,'dispatch')
class BodegaListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "inventario/bodega-lista.html"

    #permiso necesario
    permission_required = 'inventario.bodega.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las bodegas.'

#Crear bodega
@method_decorator(login_required,'dispatch')
class BodegaCreateView(ValidatePermissionRequiredMixin, CreateView):
    template_name = 'inventario/bodega-crear.html'

    #permiso necesario
    permission_required = 'inventario.bodega.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:bodega:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear bodegas.'
    form_class = BodegaForm
    success_url = reverse_lazy('administrador:bodega:lista')

    #al momento de validar el formulario creamos el registro en la base de datos
    def form_valid(self,form):
        #sacamos el objeto que se guardo en la base de datos
        self.object = form.save()
        #creamos el historial de este
        historial_create_bodega(self.request.user,self.object)
        #retornamos el form_valid
        return HttpResponseRedirect(self.get_success_url())


# API Para Consultar estado de pallet de los bultos al momentos de escanear
@method_decorator(login_required, 'dispatch')
class BultoRetrieveScanApi(ValidatePermissionRequiredMixin, RetrieveAPIView):
    # permiso necesario para ver la lista de ordenes de compra
    permission_required = 'inventario.bodega.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los bultos.'
    serializer_class = InsumoBultoSerializer

    def get_queryset(self):
        bulto = InsumoBulto.objects.filter(bodega=self.request.user.perfil.lugar)
        return bulto

@method_decorator(login_required,'dispatch')
class BultoViewset(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = InsumoBulto.objects.all()
    serializer_class = InsumoBultoSerializer

    #permiso necesario
    permission_required = 'inventario.bodega.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los bultos.'


#Actualizar
@method_decorator(login_required,'dispatch')
class BodegaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    template_name = 'inventario/bodega-actualizar.html'

    #permiso necesario
    permission_required = 'inventario.bodega.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:bodega:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar la bodega.'
    form_class = BodegaForm
    model = Bodega
    success_url = reverse_lazy('administrador:bodega:lista')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def form_valid(self,form):
        obj = Bodega.objects.get(pk=form.instance.pk)
        prev_bodega = copy.copy(obj)
        #obtenemos la bodega desde el formulario
        self.object = form.save()
        # supervisores
        supervisor = [int(x) for x in self.request.POST.getlist('supervisores')]
        supervisores = [s.supervisor.pk for s in self.object.supervisorbodega_set.all()]
        for superv in supervisor:
            if superv not in supervisores:
                print(superv)
                self.object.supervisorbodega_set.create(supervisor_id=superv)
        # eliminamos los antiguos
        [s.delete() for s in self.object.supervisorbodega_set.all() if s.supervisor.pk not in supervisor]
     
        #creamos el historial
        historial_update_bodega(self.request.user,self.object,prev_bodega)
        #retornamos la url de exito
        return HttpResponseRedirect(self.get_success_url())

#Eliminar Bodega
@method_decorator(login_required,'dispatch')
class BodegaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'inventario.bodega.eliminar'
    url_redirect = reverse_lazy('administrador:bodega:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta bodega.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            bodega = get_object_or_404(Bodega,pk=kwargs.get('pk'))
            historial_delete_bodega(self.request.user,bodega)
            bodega.delete()
            return JsonResponse({'estado':'ok','bodega':bodega.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#INVENTARIO INSUMOS
#Generación de la api de los inventarios para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class InventarioViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = InventarioInsumo.objects.all()
    serializer_class = InventarioSerializer
    
    #permiso necesario
    permission_required = 'inventario.inventarioi.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario'

    def dispatch(self, request, *args, **kwargs):
        permiso = 'inventario.inventarioi_{}'
        if 'bodega' in request.GET:
            bodega = get_object_or_404(Bodega,pk=request.GET.get('bodega'))
            nombre = bodega.nombre.lower().replace(' ','-')
            if self.request.user.has_perm(permiso.format(nombre)):
                return super().dispatch(request, *args, **kwargs)
        else:
            if self.request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        raise Http404()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'bodega' in request.GET:
            queryset = queryset.filter(bodega=int(request.GET.get('bodega')))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#Valorizar inventario por bodega
@method_decorator(login_required,'dispatch')
class InventarioInsumoValorizar(ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'inventario/inventarioi-valorizar.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Bodega, nombre=kwargs.get('lugar'))
        inventarioprecio = []
        total = 0
        inventario = InventarioInsumo.objects.filter(bodega=self.object).all()
        for i in inventario:
            check = True
            for p in inventarioprecio:
                if p['inventario'] == i.insumo:
                    p['inventario'].cantidad+= i.cantidad
                    p['precio']+= i.valorizar()
                    p['inventario'].transito+= i.obtener_transito()
                    check = False
                    break
            if check:
                i.insumo.cantidad = i.cantidad
                i.insumo.transito = i.obtener_transito()
                inventarioprecio.append( {'inventario':i.insumo,'precio':i.valorizar()})
        for i in inventarioprecio:
            try:
                i['preciou'] = i['precio']
                i['precio'] = (i['inventario'].cantidad + i['inventario'].transito) * i['precio']
            except Exception as ex:
                print(ex)
                i['preciou'] = 0
            total+=i['precio']
        context = self.get_context_data(object=self.object)
        context['precio'] = total
        context['inventario'] = inventarioprecio
        context['lugar'] = self.object.id
        context['lugarNombre'] = kwargs['lugar']

        return self.render_to_response(context)

#Listar Inventario global
@method_decorator(login_required,'dispatch')
class InventarioGlobalInsumoListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "inventario/inventarioi-valorizar.html"
    #permiso necesario
    permission_required = 'inventario.inventarioi.global'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario.'

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto
        context = super().get_context_data(**kwargs)
        #obtenemos los insumos y su cantidad global de inventario
        inventarioprecio = []
        total = 0
        inventario = InventarioInsumo.objects.all()
        for i in inventario:
            print(i.insumo.nombre)
            print(i.cantidad)
            check = True
            for p in inventarioprecio:
                if p['inventario'] == i.insumo:
                    p['inventario'].cantidad+= i.cantidad
                    p['precio'].append(i.valorizar())
                    p['inventario'].transito = i.obtener_transito()
                    check = False
                    break
            if check:
                i.insumo.cantidad = i.cantidad
                i.insumo.transito = i.obtener_transito()
                inventarioprecio.append({'inventario': i.insumo, 'precio': [i.valorizar()]})
        for i in inventarioprecio:
            i['precio'] = statistics.mean(i['precio'])
            try:
                i['preciou'] = i['precio']
                i['precio'] = (i['inventario'].cantidad + i['inventario'].transito) * i['precio']
            except Exception as ex:
                print(ex)
                i['preciou'] = 0
            total+=i['precio']
        context['precio'] = total
        context['inventario'] = inventarioprecio
        context['precio'] = total
        context['lugarNombre'] = 'Global'
        return context

#Listar inventario por bodega
@method_decorator(login_required,'dispatch')
class InventarioInsumoListView(ValidatePermissionRequiredMixin, DetailView):
    template_name = "inventario/inventarioi-lista.html"
    model = Bodega
    #permiso necesario
    permission_required = 'inventario.inventarioi.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario.'

    def dispatch(self, request, *args, **kwargs):
        permiso = 'inventario.inventarioi_{}'
        bodega = get_object_or_404(Bodega,nombre=kwargs['lugar'])
        nombre = bodega.nombre.lower().replace(' ','-')
        if self.request.user.has_perm(permiso.format(nombre)) or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404()

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Bodega,nombre=kwargs.get('lugar'))
        context = self.get_context_data(object=self.object)
        context['lugar'] = self.object.id
        context['lugarNombre'] = kwargs['lugar']
        return self.render_to_response(context)

@method_decorator(login_required,'dispatch')
class InventarioInsumoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    template_name = "inventario/inventarioi-actualizar.html"
    model = InventarioInsumo
    form_class = InventarioInsumoUpdateForm
    #permiso necesario
    permission_required = 'inventario.inventarioi.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar el inventario.'

    def dispatch(self, request, *args, **kwargs):
        #El permiso que se utiliza para verificar si tiene la posibilidad de actualizar inventario
        permiso = 'inventario.inventarioi_{}'
        #obtenemos el lugar del inventario
        self.object = self.get_object()
        #obtenemos el nombrel de lugar
        nombre = self.object.bodega.nombre.lower().replace(' ','-')
        if self.request.user.has_perm(permiso.format(nombre)) or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404()

    def get_success_url(self):
        self.object = self.get_object()
        lugar = self.object.bodega.nombre
        return reverse_lazy('inventario:insumo', args={lugar})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['lugar'] = self.object.id
        context['lugarNombre'] = kwargs['lugar']
        return self.render_to_response(context)
    
    def form_valid(self,form):
        self.object = form.save()
        historial_update_inventarioi(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())



#INVENTARIO Productos
#Generación de la api de los inventarios de productos para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class InventarioProductoViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = InventarioProducto.objects.all()
    serializer_class = InventarioProductoSerializer
    
    #permiso necesario
    permission_required = 'inventario.inventariop.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario'

    def dispatch(self, request, *args, **kwargs):
        permiso = 'inventario.inventariop_{}'
        if 'bodega' in request.GET:
            bodega = get_object_or_404(Bodega,pk=request.GET.get('bodega'))
            nombre = bodega.nombre.lower().replace(' ','-')
            if self.request.user.has_perm(permiso.format(nombre)):
                return super().dispatch(request, *args, **kwargs)
        else:
            if self.request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        raise Http404()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if 'bodega' in request.GET:
            queryset = queryset.filter(bodega=int(request.GET.get('bodega')))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



#Api para obtener el inventario de productos a partir de una ubicación
@method_decorator(login_required,'dispatch')
class InventarioProductoPorUbicacion(ValidatePermissionRequiredMixin,APIView):
    #permiso necesario para ver la lista de ordenes de compra
    permission_required = 'inventario.inventariop.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario'
    
    def get(self,request,*args,**kwargs):
        #el lugar de donde se obtendra el inventario
        lugar = int(self.kwargs.get('lugar'))
        #rama a investigar
        rama = int(self.kwargs.get('rama'))
        #buscamos sus respectivos objetos
        lugar = get_object_or_404(Bodega,pk=lugar)
        rama = get_object_or_404(Rama,pk=rama)
        #sacamos todos los productos que posean inventario en el lugar
        productos = rama.productos.all()
        productos_f = []
        for p in productos:
            #obtenemos el inventario del producto en caso de no encontrarlo se inicializa en valro 0
            inventario,created = InventarioProducto.objects.get_or_create(bodega=lugar,producto=p,defaults={'cantidad': 0})
            maduracion = 0
            transito = 0
            #obtenemso los productos que estan en maduración
            lotes = Lote.objects.filter(producto=p,pauta_produccion__lugar=lugar).all()
            for l in lotes:
                estado = l.estadolote_set.last()
                if "maduracion" in estado.nombre.lower() or "maduración" in estado.nombre.lower():
                    maduracion+=l.cantidadactual()
            #obtenemos las cajas que se encuentran en transito
            envios_caja = LoteEnvio.objects.filter(envio__lugar_o=lugar,recepcionado=None,cajalote__lote__producto=p).all()
            #recorremos las cajas enviadas, y sumamos al en transito
            for envio_c in envios_caja:
                transito+=envio_c.cajalote.cantidad            
            producto = {'codigo':p.codigo,'updated':p.updated,'nombre':p.nombre,'presentacion':p.presentacion,'id':inventario.id,'maduracion':maduracion,'transito':transito,'inventario':inventario.cantidad,'unidad':p.unidad,'total':inventario.cantidad+transito+maduracion}
            productos_f.append(producto)

        return Response(
                {
                "productos":productos_f,
                "detail": "ok",
                }
        )

#Listar inventario de productos por bodega
@method_decorator(login_required,'dispatch')
class InventarioProductoView(ValidatePermissionRequiredMixin, DetailView):
    template_name = "inventario/inventariop/lista.html"
    #permiso necesario
    permission_required = 'inventario.inventariop.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario.'
    model = Bodega

    def dispatch(self, request, *args, **kwargs):
        permiso = 'inventario.inventariop_{}'
        bodega = get_object_or_404(Bodega,nombre=kwargs['lugar'])
        nombre = bodega.nombre.lower().replace(' ','-')
        if self.request.user.has_perm(permiso.format(nombre)) or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404()
    

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Bodega,nombre=kwargs.get('lugar'))
        context = self.get_context_data(object=self.object)
        context['areas'] = Rama.objects.all()
        context['lugar'] = self.object.id
        context['lugarNombre'] = kwargs['lugar']
        context['lugarnombre'] = 'inventario.inventariop_' + kwargs['lugar'].lower().replace(' ','-')
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        # Obtenemos el contexto
        context = super().get_context_data(**kwargs)
        self.object = context['object']
        #obtenemos los insumos y su cantidad global de inventario
        inventario = InventarioProducto.objects.filter(bodega=self.object).values('producto').annotate(cantidad=Sum('cantidad')).annotate(actualizado=Max('updated'))
        for producto in Producto.objects.all():
            ip,created = InventarioProducto.objects.get_or_create(producto=producto,bodega=self.object,defaults={'cantidad':0})
        #lotes en maduracion
        estadolotesm = EstadoLote.objects.filter(nombre__icontains="maduración",).all()
        estadolotest = EstadoLote.objects.filter(nombre='Empacado',).all()
        maduracion = []
        transito = []
        for estado in estadolotesm:
            #ver si es el ultimo estado
            if estado == estado.lote.estadolote_set.last():
                #si es guardamos su cantidad en la lista de maduracion
                ingresar = {estado.lote.producto.pk:estado.lote.cantidadactual()}
                maduracion.append(ingresar)
         #obtenemos las cajas que se encuentran en transito
        envios_caja = LoteEnvio.objects.filter(recepcionado=None,envio__lugar_o=self.object).all()
        #recorremos las cajas enviadas, y sumamos al en transito
        for envio_c in envios_caja:
            ingresar = {envio_c.cajalote.lote.producto.pk:envio_c.cajalote.cantidad}
            transito.append(ingresar)
        
        #utilizamos la libreria collections, para sumar los distintos en maduración de los productos
        counter = collections.Counter()
        for d in maduracion: 
            counter.update(d) 
        maduracion_f = dict(counter)

        #utilizamos la libreria collections, para sumar los distintos en transito de los productos
        counter = collections.Counter()
        for d in transito: 
            counter.update(d) 
        transito_f = dict(counter)
        #agregamos al inventario la cantidad y las unidades en maduración
        for i in inventario:
            i['producto'] = Producto.objects.get(pk=i['producto'])
            i['id'] = InventarioProducto.objects.filter(producto=i['producto'],bodega=self.object).values('pk')[0]['pk']
            try:
                i['maduracion'] = maduracion_f[i['producto'].pk]
            except:
                i['maduracion'] = 0
            try:
                i['transito'] = transito_f[i['producto'].pk]
            except:
                i['transito'] = 0
            i['total'] = i['maduracion'] + i['cantidad'] + i['transito']
        context['inventario'] = inventario
        context['areas'] = Rama.objects.all()
        context['lugarNombre'] = self.object.nombre
        return context

#Listar Inventario global
@method_decorator(login_required,'dispatch')
class InventarioGlobalProductoListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "inventario/inventariop/global.html"
    #permiso necesario
    permission_required = 'inventario.inventariop.global'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el inventario.'

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto
        context = super().get_context_data(**kwargs)
        context['areas'] = Rama.objects.all()
        context['lugarNombre'] = 'Global'
        #obtenemos los insumos y su cantidad global de inventario
        inventario = InventarioProducto.objects.values('producto').annotate(cantidad=Sum('cantidad')).annotate(actualizado=Max('updated'))
        #lotes en maduracion
        estadolotesm = EstadoLote.objects.filter(nombre__icontains="maduración",).all()
        estadolotest = EstadoLote.objects.filter(nombre='Empacado',).all()
        maduracion = []
        transito = []
        for estado in estadolotesm:
            #ver si es el ultimo estado
            if estado == estado.lote.estadolote_set.last():
                #si es guardamos su cantidad en la lista de maduracion
                ingresar = {estado.lote.producto.pk:estado.lote.cantidadactual()}
                maduracion.append(ingresar)
         #obtenemos las cajas que se encuentran en transito
        envios_caja = LoteEnvio.objects.filter(recepcionado=None,envio__lugar_o__in=[bodega for bodega in Bodega.objects.all()]).all()
        #recorremos las cajas enviadas, y sumamos al en transito
        for envio_c in envios_caja:
            ingresar = {envio_c.cajalote.lote.producto.pk:envio_c.cajalote.cantidad}
            transito.append(ingresar)
        
        #utilizamos la libreria collections, para sumar los distintos en maduración de los productos
        counter = collections.Counter()
        for d in maduracion: 
            counter.update(d) 
        maduracion_f = dict(counter)

        #utilizamos la libreria collections, para sumar los distintos en transito de los productos
        counter = collections.Counter()
        for d in transito: 
            counter.update(d) 
        transito_f = dict(counter)
        #agregamos al inventario la cantidad y las unidades en maduración
        for i in inventario:
            i['producto'] = Producto.objects.get(pk=i['producto'])
            i['id'] = InventarioProducto.objects.filter(producto=i['producto']).values('pk')[0]['pk']
            try:
                i['maduracion'] = maduracion_f[i['producto'].pk]
            except:
                i['maduracion'] = 0
            try:
                i['transito'] = transito_f[i['producto'].pk]
            except:
                i['transito'] = 0
            i['total'] = i['maduracion'] + i['cantidad'] + i['transito']
        context['inventario'] = inventario
        return context


    template_name = "inventario/inventariop/lista.html"
    #permiso necesario
    permission_required = 'inventario.inventariop.global'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    model = Bodega
    mensaje = 'No tienes los permisos necesarios para listar el inventario.'

# ACTUALIZAR INVENTARIO Productos MANUAL
@method_decorator(login_required,'dispatch')
class InventarioProductoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    template_name = "inventario/inventariop/actualizar.html"
    #permiso necesario
    permission_required = 'inventario.inventariop.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar el inventario'
    form_class = InventarioProductoUpdateForm
    model = InventarioProducto
    

    def get_success_url(self):
        self.object = self.get_object()
        lugar = self.object.bodega.nombre
        return reverse_lazy('inventario:producto', args={lugar})

    def dispatch(self, request, *args, **kwargs):
        permiso = 'inventario.inventariop_{}'
        bodega = get_object_or_404(Bodega,nombre=kwargs['lugar'])
        nombre = bodega.nombre.lower().replace(' ','-')
        if self.request.user.has_perm(permiso.format(nombre)) or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cantidad"] = str(round((context["object"].cantidad / context["object"].producto.unidades),2)).replace(',','.')
        print(context)
        return context
    


    def form_valid(self, form):
        self.object = form.save(commit=False)
        cantidad = float(self.request.POST.get('cantidad'))
        self.object.cantidad = cantidad  * self.object.producto.unidades
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



# API Historial de Inventario
@method_decorator(login_required,'dispatch')
class HistorialBodegaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = HistorialBodega.objects.all()
    serializer_class = HistorialBodegaSerializer
    
    #permiso necesario
    permission_required = 'inventario.historia.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar el historial de inventario'

# Crear Historial de Inventario
@method_decorator(login_required,'dispatch')
class BodegaHistorialCreateView(ValidatePermissionRequiredMixin, CreateView):
    template_name = "inventario/historial/create.html"
    #permiso necesario
    permission_required = 'inventario.historial.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    success_url = reverse_lazy('historial:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios crear un historial de inventario'
    form_class = HistorialBodegaForm
    model = HistorialBodega

    def form_valid(self,form):
        self.object = form.save()
        #Obtenemos los insumos que hay en esa bodega
        insumos = InventarioInsumo.objects.filter(bodega=self.object.bodega).all()
        #recorremso los insumos y creamos su valorización a la fecha
        for i in insumos:
            self.object.historialbodegainsumo_set.create(precio=i.valorizar(),insumo=i.insumo,cantidad=i.cantidad)
        return HttpResponseRedirect(self.get_success_url())

# Mostrar Historial de Inventario
@method_decorator(login_required,'dispatch')
class BodegaHistorialDetailView(ValidatePermissionRequiredMixin, DetailView):
    template_name = "inventario/historial/detail.html"
    #permiso necesario
    permission_required = 'inventario.historial.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    success_url = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios crear un historial de inventario'
    model = HistorialBodega

#Lista de historiales de inventario
@method_decorator(login_required,'dispatch')
class BodegaHistorialListView(ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'inventario/historial/list.html'
    #permiso necessario
    permission_required = 'inventario.historial.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    success_url = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios crear un historial de inventario'


#Eliminar Bodega
@method_decorator(login_required,'dispatch')
class HistorialBodegaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'inventario.historial.eliminar'
    url_redirect = reverse_lazy('historial:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este historial.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            bodega = get_object_or_404(HistorialBodega,pk=kwargs.get('pk'))
            #historial_delete_bodega(self.request.user,bodega)
            bodega.delete()
            return JsonResponse({'estado':'ok','bodega':bodega.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Hacer Inventario
@method_decorator(login_required,'dispatch')
class HacerInventarioView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso necessario
    permission_required = 'inventario.historial.'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    success_url = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios crear un historial de inventario'
    #planilla a utilizar
    template_name = 'inventario/hinventario/hinventario.html'
    #modelo
    model = Bodega
    form_class = BodegaHistorialForm
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.lugar.pk != int(kwargs.get('pk')):
            raise Http404('No puedes realizar inventario en una bodega en la cual no te encuentras.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #obtenemos todos los bultos que se encuentra en la bodega seleccionada
        context = super().get_context_data(**kwargs)
        context['bultos'] = InsumoBulto.objects.filter(bodega=context['object']).filter(~Q(cantidadu=F('cantidad'))).all()
        return context