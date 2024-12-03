from nucleo.functions import comparar_palabra, historial_actualizar_insumo, historial_actualizar_producto, historial_actualizar_rama, historial_crear_insumo, historial_crear_producto, historial_crear_rama, historial_eliminar_insumo, historial_eliminar_producto, historial_eliminar_rama
from inventario.models import InventarioInsumo
from django.shortcuts import render
from django.views.generic import TemplateView,CreateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.static import serve
from django.urls import reverse_lazy,reverse
from django.conf import settings
from django.http import HttpResponseForbidden
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import InsumoOrdenSerializer, ProductoSerializer,ProveedorInsumoSerializer, RamaSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from .models import Insumo, InsumoDirectoProducto, Producto, Rama
from proveedores.models import ProveedorInsumo
from .forms import InsumoForm, ProductoForm, RamaForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse,HttpResponseRedirect

# Create your views here.
#solo usuarios logeados pueden acceder al home
@method_decorator(login_required,'dispatch')
#clase home
class HomeView(TemplateView):
    #la template que usaremos para el home
    template_name = "nucleo/home.html"


# -- INSUMOS -- #

#Generación de la api de los insumos para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class InsumoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoOrdenSerializer

    def list(self,request):
        permisos = ['nucleo.insumo.listar','nucleo.producto.crear','nucleo.producto.actualizar','pauta.actualizar','pauta.crear']
        check = False
        for p in permisos:
            if self.request.user.has_perm(p):
                check = True
        if check:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("[]")

    @action(detail=True, methods=['get'])
    def proveedores(self,request,pk=None):
        queryset = ProveedorInsumo.objects.filter(insumo=pk).all()
        serializer = ProveedorInsumoSerializer(queryset,many=True)
        return Response(serializer.data);




@method_decorator(login_required,'dispatch')
class InsumoListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "nucleo/insumo-lista.html"

    #permiso necesario
    permission_required = 'nucleo.insumo.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los insumos.'

@method_decorator(login_required, 'dispatch')
class InsumoCreateView(ValidatePermissionRequiredMixin, CreateView):
    template_name = "nucleo/insumo-crear.html"
    model = Insumo
    form_class = InsumoForm
    success_url = reverse_lazy('administrador:insumo:lista')

    # permiso necesario
    permission_required = 'nucleo.insumo.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:insumo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un insumo.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        check = self.request.POST.get('forzar')
        if check is None:
            nombre = form.cleaned_data.get('nombre')
            insumo_ids = [insumo.id for insumo in Insumo.objects.all() if comparar_palabra(nombre, insumo.nombre) > 0.80]
            if len(insumo_ids) > 0:
                insumos = [insumo.nombre for insumo in Insumo.objects.filter(id__in=insumo_ids).all()]
                form.add_error('nombre', "El nombre ya es muy similar a otros ({})".format(' ,'.join(insumos)))
                return super(InsumoCreateView, self).form_invalid(form)
        self.object.save()
        historial_crear_insumo(self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, 'dispatch')
class InsumoUpdateView(UpdateView):
    template_name = "nucleo/insumo-actualizar.html"
    model = Insumo
    form_class = InsumoForm
    success_url = reverse_lazy('administrador:insumo:lista')

    # permiso necesario
    permission_required = 'nucleo.insumo.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:insumo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un insumo.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        check = self.request.POST.get('forzar')
        if check is None:
            nombre = form.cleaned_data.get('nombre')
            insumo_ids = [insumo.id for insumo in Insumo.objects.exclude(pk=self.object.pk).all() if comparar_palabra(nombre, insumo.nombre) > 0.80]
            if len(insumo_ids) > 0:
                insumos = [insumo.nombre for insumo in Insumo.objects.filter(id__in=insumo_ids).all()]
                form.add_error('nombre', "El nombre ya es muy similar a otros ({})".format(' ,'.join(insumos)))
                return super(InsumoUpdateView, self).form_invalid(form)
        #actualizar todos los insumos asociados (para el stock)
        self.object.save()
        insumos = InventarioInsumo.objects.filter(insumo=self.object.id).all()
        for i in insumos:
            i.save()
        historial_actualizar_insumo(self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required,'dispatch')
class InsumoDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'nucleo.insumo.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            insumo = get_object_or_404(Insumo,pk=kwargs.get('pk'))
            historial_eliminar_insumo(self.request.user,insumo)
            insumo.delete()
            return JsonResponse({'estado':'ok','insumo':insumo.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})


# -- FIN INSUMOS -- #

# -- INICIO Areas de Negocio -- #
#Generación de la api de las areas de negocio para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class RamaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Rama.objects.all()
    serializer_class = RamaSerializer
    
    #permiso necesario
    permission_required = 'nucleo.rama.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las áreas del negocio.'

    @action(detail=True, methods=['get'])
    def productos(self,request,pk=None):
        queryset = Producto.objects.filter(rama=pk).all()
        serializer = ProductoSerializer(queryset,many=True)
        rama = Rama.objects.filter(pk=pk).first()
        serializer_rama = RamaSerializer(rama)
        return Response({"productos":serializer.data,"rama":serializer_rama.data});

#Lista de las distintas Áreas del negocio
@method_decorator(login_required,'dispatch')
class RamaListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "nucleo/rama-lista.html"

    #permiso necesario
    permission_required = 'nucleo.rama.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las áreas del negocio.'

@method_decorator(login_required,'dispatch')
class RamaCreateView(ValidatePermissionRequiredMixin, CreateView):
    #INFO
    template_name = 'nucleo/rama-crear.html'
    model = Rama
    form_class = RamaForm
    success_url = reverse_lazy('administrador:area:lista')

    # PERMISOS #
    permission_required = 'nucleo.rama.crear'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una área de negocio'

    def form_valid(self, form):
        self.object = form.save()
        historial_crear_rama(self.request.user,self.object)
        return super().form_valid(form)

@method_decorator(login_required,'dispatch')
class RamaUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    #INFO
    template_name = 'nucleo/rama-actualizar.html'
    model = Rama
    form_class = RamaForm
    success_url = reverse_lazy('administrador:area:lista')

    # PERMISOS #
    permission_required = 'nucleo.rama.actualizar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un área de negocio'

    def form_valid(self, form):
        self.object = form.save()
        historial_actualizar_rama(self.request.user,self.object)
        return super().form_valid(form)

@method_decorator(login_required,'dispatch')
class RamaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'nucleo.rama.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            rama = get_object_or_404(Rama,pk=kwargs.get('pk'))
            historial_eliminar_rama(self.request.user,rama)
            rama.delete()
            return JsonResponse({'estado':'ok','rama':rama.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

# FIN AREAS DE NEGOCIO #

# PRODUCTOS #
#Generación de la api de los productos para ser consumida por sus vistas
@method_decorator(login_required,'dispatch')
class ProductoViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    #permiso necesario
    permission_required = 'nucleo.producto.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los productos.'


#Lista de los productos del negocio
@method_decorator(login_required,'dispatch')
class ProductoListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "nucleo/producto-lista.html"

    #permiso necesario
    permission_required = 'nucleo.producto.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los productos.'

#Crear un producto
@method_decorator(login_required,'dispatch')
class ProductoCreateView(ValidatePermissionRequiredMixin, CreateView):
    #OPCIONES
    template_name = "nucleo/producto-crear.html"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('administrador:producto:lista')

    #permiso necesario
    permission_required = 'nucleo.producto.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:producto:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un productos.'

    def get_form_kwargs(self):
        #agregamos rama para un manejo más rapido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'rama' in self.request.GET:
            kwargs['rama'] = self.request.GET.get('rama')
        return kwargs

    def form_valid(self, form):
        #obtenemos el producto a partir del formulario
        self.object = form.save()
        descriptores = self.request.POST.getlist('descriptores[]')
        descriptores_c = self.request.POST.getlist('descriptores_c[]')
        descriptores_d = self.request.POST.getlist('descriptores_d[]')
        listaf = []
        for i in range(len(descriptores)):
            insumo = {'producto_id':self.object.id,'insumo_id': descriptores[i:i+1][0],'cantidad':descriptores_c[i:i+1][0],'detalle':descriptores_d[i:i+1][0]}
            if insumo['insumo_id'] not in listaf:
                listaf.append(insumo['insumo_id'])
                insumo = InsumoDirectoProducto(**insumo)
                insumo.save()
                self.object.descriptores.add(insumo.insumo)
        historial_crear_producto(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())

#Actualizar un producto
@method_decorator(login_required,'dispatch')
class ProductoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    #OPCIONES
    template_name = "nucleo/producto-actualizar.html"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('administrador:producto:lista')

    #permiso necesario
    permission_required = 'nucleo.producto.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:producto:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar el producto.'

    def form_valid(self, form):
        #obtenemos el producto a partir del formulario
        self.object = form.save()
        descriptores = self.request.POST.getlist('descriptores[]')
        descriptores_c = self.request.POST.getlist('descriptores_c[]')
        descriptores_d = self.request.POST.getlist('descriptores_d[]')
        listaf = []
        self.object.descriptores.clear()
        for i in range(len(descriptores)):
            insumo = {'producto_id':self.object.id,'insumo_id': descriptores[i:i+1][0],'cantidad':descriptores_c[i:i+1][0],'detalle':descriptores_d[i:i+1][0]}
            if insumo['insumo_id'] not in listaf:
                listaf.append(insumo['insumo_id'])
                insumo = InsumoDirectoProducto(**insumo)
                insumo.save()
                self.object.descriptores.add(insumo.insumo)
        historial_actualizar_producto(self.request.user,self.object)
        return HttpResponseRedirect(self.get_success_url())


#Eliminar un producto
@method_decorator(login_required,'dispatch')
class ProductodeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'nucleo.producto.eliminar'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            producto = get_object_or_404(Producto,pk=kwargs.get('pk'))
            historial_eliminar_producto(self.request.user,producto)
            producto.delete()
            return JsonResponse({'estado':'ok','producto':producto.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})



#vista protegida para los archivos adjuntos
def protected_media(request, path):

    user = request.user
    if user.is_authenticated:
        if path[0:7] == 'firmas/':
            if user.has_perm('calidad.registrolimpiezaequipo.excel'):
                return serve(request, path, settings.MEDIA_ROOT)
            else:
                if user.perfil:
                    if path == user.perfil.firma_digital.name:
                        return serve(request,user.perfil.firma_digital.name,settings.MEDIA_ROOT)
                    else:
                        return HttpResponseForbidden('No tienes acceso para ver este archivo.')
                else:
                    return HttpResponseForbidden('No tienes acceso para ver este archivo.')
        return serve(request, path, settings.MEDIA_ROOT)
    else:
        return HttpResponseForbidden('No tienes acceso para ver este archivo.')