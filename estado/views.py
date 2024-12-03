from django.shortcuts import render
from django.http.response import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, View, DetailView
from .serializers import ConjuntoEstadoSerializer, EstadoSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from nucleo.models import Producto, Insumo
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .models import ConjuntoEstado, Estado
from .forms import ConjuntoEstadoForm, EstadoForm
from rest_framework import viewsets, mixins
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.

@method_decorator(login_required,'dispatch')
class ConjuntoEstadoCreateView(ValidatePermissionRequiredMixin,CreateView):
    #template a utilizar
    template_name = 'estado/conjunto/create.html'
    #permiso necesario
    permission_required = 'estado.conjunto.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje
    mensaje = 'No tienes los permisos necesarios para crear un envio'
    #modelo a utilizar
    model = ConjuntoEstado
    form_class = ConjuntoEstadoForm
    #url de redirección si todo sale bien
    success_url = reverse_lazy('administrador:estados:lista-conjunto')

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['estados'] = Estado.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        estados = [int(id) for id in self.request.POST.getlist('estados')]
        contador = 0
        for i in estados:
            existe = Estado.objects.filter(pk=i).first()
            if existe:
                self.object.estadoconjunto_set.create(estado=existe, pos=contador)
                contador += 1
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, 'dispatch')
class ConjuntoEstadoTemplateView(ValidatePermissionRequiredMixin, TemplateView):
    # template a utilizar
    template_name = 'estado/conjunto/list.html'
    # permiso necesario
    permission_required = 'estado.conjunto.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para listar los estados'

@method_decorator(login_required, 'dispatch')
class EstadoTemplateView(ValidatePermissionRequiredMixin, TemplateView):
    # template a utilizar
    template_name = 'estado/estado/list.html'
    # permiso necesario
    permission_required = 'estado.conjunto.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para listar los estados'

@method_decorator(login_required, 'dispatch')
class ConjuntoEstadoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # template a utilizar
    template_name = 'estado/conjunto/update.html'
    # permiso necesario
    permission_required = 'estado.conjunto.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para actualizar un conjunto de estados'
    # modelo a utilizar
    model = ConjuntoEstado
    form_class = ConjuntoEstadoForm
    # url de redirección si todo sale bien
    success_url = reverse_lazy('administrador:estados:lista-conjunto')

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['estados'] = Estado.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        estados = [int(id) for id in self.request.POST.getlist('estados')]
        contador = 0
        for i in estados:
            existe = Estado.objects.filter(pk=i).first()
            if existe:
                # vemos si ya existe
                check2 = self.object.estadoconjunto_set.filter(estado=existe).first()
                if check2:
                    check2.pos = contador
                    check2.save()
                else:
                    self.object.estadoconjunto_set.create(estado=existe, pos=contador)
                contador += 1
        # eliminamos los que ya no existan
        eliminar = [conjuntoestado for conjuntoestado in self.object.estadoconjunto_set.all() if conjuntoestado.estado.id not in estados]
        for e in eliminar:
            e.delete()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required,'dispatch')
class EstadoCreateView(ValidatePermissionRequiredMixin,CreateView):
    # template a utilizar
    template_name = 'estado/estado/create.html'
    # permiso necesario
    permission_required = 'estado.conjunto.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para crear un estado'
    # modelo a utilizar
    model = Estado
    form_class = EstadoForm
    # url de redirección si todo sale bien
    success_url = reverse_lazy('administrador:estados:lista-estado')

    def form_valid(self, form):
        self.object = form.save()
        insumos = [int(id) for id in self.request.POST.getlist('insumos')]
        productos = [int(id) for id in self.request.POST.getlist('productos')]
        for i in insumos:
            existe = Insumo.objects.filter(pk=i).first()
            if existe:
                self.object.estadoinsumo_set.create(insumo=existe)
        for i in productos:
            existe = Producto.objects.filter(pk=i).first()
            if existe:
                self.object.estadoproducto_set.create(producto=existe)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required,'dispatch')
class EstadoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # template a utilizar
    template_name = 'estado/estado/update.html'
    # permiso necesario
    permission_required = 'estado.conjunto.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para actualizar un estado'
    # modelo a utilizar
    model = Estado
    form_class = EstadoForm
    # url de redirección si todo sale bien
    success_url = reverse_lazy('administrador:estados:lista-estado')

    def form_valid(self, form):
        self.object = form.save()
        insumos = [int(id) for id in self.request.POST.getlist('insumos')]
        productos = [int(id) for id in self.request.POST.getlist('productos')]
        for i in insumos:
            existe = Insumo.objects.filter(pk=i).first()
            if existe:
                #vemos si existe la relacion
                check2 = self.object.estadoinsumo_set.filter(insumo__id=i).first()
                if check2 is None:
                    self.object.estadoinsumo_set.create(insumo=existe)
        #eliminamos los insumos
        eliminar = [insumo for insumo in self.object.estadoinsumo_set.all() if insumo.insumo.id not in insumos]
        for e in eliminar:
            e.delete()
        for i in productos:
            existe = Producto.objects.filter(pk=i).first()
            if existe is None:
                #vemos si existe la relacion
                check2 = self.object.estadoproducto_set.filter(producto__id=i).first()
                if check2 is None:
                    self.object.estadoproducto_set.create(producto=existe)
        #eliminamos los productos
        eliminar = [producto for producto in self.object.estadoproducto_set.all() if producto.producto.id not in productos]
        for e in eliminar:
            e.delete()
        return HttpResponseRedirect(self.get_success_url())

#Api para obtener el listado de los pallets
@method_decorator(login_required,'dispatch')
class EstadoViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #objetos a serializar
    queryset = Estado.objects.all()
    #serializer utilizado
    serializer_class = EstadoSerializer
    #permiso necesario
    permission_required = 'estado.conjunto.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar los estados.'

#Api para obtener el listado de los pallets
@method_decorator(login_required,'dispatch')
class ConjuntoEstadoViewset(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #objetos a serializar
    queryset = ConjuntoEstado.objects.all()
    #serializer utilizado
    serializer_class = ConjuntoEstadoSerializer
    #permiso necesario
    permission_required = 'estado.conjunto.listar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    #tipo de mensaje
    tipo_mensaje = 'error'
    #mensaje a mostrar
    mensaje = 'No tienes los permisos necesarios para listar los estados.'


# Eliminar Conjunto
@method_decorator(login_required, 'dispatch')
class ConjuntoEstadoDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'estado.conjunto.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            conjunto = get_object_or_404(ConjuntoEstado, pk=kwargs.get('pk'))
            conjunto.delete()
            return JsonResponse({'estado': 'ok'})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})


# Eliminar Estado
@method_decorator(login_required, 'dispatch')
class EstadoDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'estado.conjunto.eliminar'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            estado = get_object_or_404(Estado, pk=kwargs.get('pk'))
            estado.delete()
            return JsonResponse({'estado': 'ok'})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})
