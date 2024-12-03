from rest_framework.response import Response
from nucleo.models import Rama
from .forms import ClienteAcuerdoForm, ClienteForm, ClienteLocalForm
from .serializers import ClienteLocalSerializer, ClienteSerializer, ClienteSerializerSencillo
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView, RetrieveAPIView
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Cliente, ClienteLocal
from rest_framework.pagination import PageNumberPagination
from .functions import historial_create_cliente, historial_create_cliente_local, historial_delete_cliente, historial_delete_cliente_local, historial_update_cliente, historial_update_cliente_local
# Create your views here.

# API CLIENTES #
# Generación de la api de los clientes para ser consumidos por sus vistas


@method_decorator(login_required, 'dispatch')
class ClienteViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializerSencillo
    # permiso necesario
    permission_required = 'clientes.cliente.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los clientes.'

# API CLIENTES #
# Generación de la api de los clientes para ser consumidos por sus vistas


@method_decorator(login_required, 'dispatch')
class ClienteAvanzadoDetailApiView(ValidatePermissionRequiredMixin, RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # permiso necesario
    permission_required = 'clientes.cliente.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los clientes.'

# API PARA EL BUSCADOR DE CLIENTES #

@method_decorator(login_required, 'dispatch')
class ClienteListApiView(ValidatePermissionRequiredMixin, ListAPIView):
    # permiso necesario
    permission_required = 'clientes.cliente.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    # tipo de mensaje
    tipo_mensaje = 'error'
    # mensaje
    mensaje = 'No tienes los permisos necesarios para listar los envios.'
    # serializer
    serializer_class = ClienteSerializerSencillo

    def get_queryset(self):
        return Cliente.objects.filter(nombre__icontains=self.kwargs['nombre']).all().order_by('-pk')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


# Listar Clientes


@method_decorator(login_required, 'dispatch')
class ClienteListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "clientes/listar.html"
    # permiso necesario
    permission_required = 'clientes.cliente.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los clientes.'

# Crear Clientes


@method_decorator(login_required, 'dispatch')
class ClienteCreateView(ValidatePermissionRequiredMixin, CreateView):
    # template a utilizar
    template_name = 'clientes/crear.html'
    # formulario a utilizar
    form_class = ClienteForm
    # permiso necesario
    permission_required = 'clientes.cliente.crear'
    # donde retornar si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:cliente:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un cliente'
    success_url = reverse_lazy('administrador:cliente:lista')

    def form_valid(self, form):
        historial_create_cliente(self.request.user, form.save())
        return super().form_valid(form)

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=El cliente ha sido creado&tipo_mensaje=info"

# Actualizar Clientes


@method_decorator(login_required, 'dispatch')
class ClienteUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # template a utilizar
    template_name = 'clientes/actualizar.html'
    # formulario a utilizar
    form_class = ClienteForm
    # modelo a utilizar
    model = Cliente
    # permiso necesario
    permission_required = 'clientes.cliente.actualizar'
    # donde retornar si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:cliente:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar los clientes'
    success_url = reverse_lazy('administrador:cliente:lista')

    def form_valid(self, form):
        historial_update_cliente(self.request.user, form.save())
        return super().form_valid(form)

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=El cliente ha sido actualizado&tipo_mensaje=info"

# Eliminar Cliente


@method_decorator(login_required, 'dispatch')
class ClienteDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'clientes.cliente.eliminar'
    url_redirect = reverse_lazy('administrador:cliente:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este cliente.'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            cliente = get_object_or_404(Cliente, pk=kwargs.get('pk'))
            historial_delete_cliente(self.request.user, cliente)
            cliente.delete()
            return JsonResponse({'estado': 'ok', 'cliente': cliente.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

# API CLIENTES #
# Generación de la api de los clientes para ser consumidos por sus vistas


@method_decorator(login_required, 'dispatch')
class ClienteLocalViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ClienteLocal.objects.all()
    serializer_class = ClienteLocalSerializer

    # permiso necesario
    permission_required = 'clientes.local.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los locales.'

# Listar Locales


@method_decorator(login_required, 'dispatch')
class ClienteLocalListView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = "clientes/local-listar.html"
    # permiso necesario
    permission_required = 'clientes.local.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los locales.'


# Crear Local
@method_decorator(login_required, 'dispatch')
class ClienteLocalCreateView(ValidatePermissionRequiredMixin, CreateView):
    # template a utilizar
    template_name = 'clientes/local-crear.html'
    # formulario a utilizar
    form_class = ClienteLocalForm
    # permiso necesario
    permission_required = 'clientes.local.crear'
    # donde retornar si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:local:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un local'
    success_url = reverse_lazy('administrador:cliente:lista')

    def get_form_kwargs(self):
        # agregamos proveedor / insumo para un manejo más rapido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'cliente' in self.request.GET:
            kwargs['cliente'] = self.request.GET.get('cliente')
        return kwargs

    def form_valid(self, form):
        historial_create_cliente_local(self.request.user, form.save())
        return super().form_valid(form)

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=El local ha sido creado&tipo_mensaje=info"

# Actualizar Local


@method_decorator(login_required, 'dispatch')
class ClienteLocalUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # template a utilizar
    template_name = 'clientes/local-actualizar.html'
    # formulario a utilizar
    form_class = ClienteLocalForm
    # modelo a utilizar
    model = ClienteLocal
    # permiso necesario
    permission_required = 'clientes.local.actualizar'
    # donde retornar si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:local:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar los locales'
    success_url = reverse_lazy('administrador:local:lista')

    def form_valid(self, form):
        historial_update_cliente_local(self.request.user, form.save())
        return super().form_valid(form)

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=El local ha sido actualizado&tipo_mensaje=info"

# Eliminar Local


@method_decorator(login_required, 'dispatch')
class ClienteLocalDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'clientes.local.eliminar'
    url_redirect = reverse_lazy('administrador:local:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este local.'
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            local = get_object_or_404(ClienteLocal, pk=kwargs.get('pk'))
            historial_delete_cliente_local(self.request.user, local)
            local.delete()
            return JsonResponse({'estado': 'ok', 'cliente': local.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})

# Manejar Acuerdos Comerciales


@method_decorator(login_required, 'dispatch')
class ClienteAcuerdoCreateView(ValidatePermissionRequiredMixin, CreateView):
    # template a utilizar
    template_name = 'clientes/acuerdos/create.html'
    # formulario a utilizar
    form_class = ClienteAcuerdoForm
    # permiso necesario
    permission_required = 'clientes.cliente.crear'
    # donde retornar si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:cliente:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un cliente'
    success_url = reverse_lazy('administrador:cliente:lista')

    def get_context_data(self, **kwargs):
        context = super(ClienteAcuerdoCreateView, self).get_context_data(**kwargs)
        cliente_id = self.kwargs.get('cliente', None)
        if cliente_id:
            # si existe el cliente
            cliente = Cliente.objects.filter(pk=int(cliente_id)).first()
            if cliente:
                # agregamos el cliente al contexto
                context['cliente'] = cliente
                # obtenemos las ramas
                ramas = Rama.objects.all()
                # obtenemos los acuerdos actuales
                actuales = cliente.acuerdocomercial_set.all()
                # combinamos las ramas y los acuerdos actuales
                for rama in ramas:
                    actual = [actual for actual in actuales if actual.rama.id == rama.id]
                    if len(actual) > 0:
                        rama.porcentaje = str(actual[0].porcentaje).replace(',', '.')
                    else:
                        rama.porcentaje = 0
                # agregamos las ramas al contexto
                context['ramas'] = ramas
        return context
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        cliente = Cliente.objects.filter(pk=int(form.data['cliente'])).first()
        if cliente:
            identificadores = [int(identificador) for identificador in self.request.POST.getlist('identificadores[]')]
            porcentajes = [float(porcentaje) for porcentaje in self.request.POST.getlist('porcentajes[]')]
            for i in range(len(identificadores)):
                # verificamos si el identificador de la rama existe
                rama = Rama.objects.filter(pk=int(identificadores[i])).first()
                if rama:
                    porcentaje = porcentajes[i]
                    # vemos si existe el porcentaje
                    if porcentaje > 0:
                        # obtenemos el acuerdo y si no existe se crea
                        acuerdo, created = cliente.acuerdocomercial_set.get_or_create(rama=rama, defaults={'porcentaje': porcentaje})
                        # si el acuerdo existe, actualizamos el porcentaje
                        if created is False:
                            acuerdo.porcentaje = porcentaje
                            acuerdo.save()
                    # de no existir, se elimina este acuerdo
                    else:
                        acuerdo = cliente.acuerdocomercial_set.filter(rama=rama).first()
                        if acuerdo:
                            acuerdo.delete()
        return HttpResponseRedirect(self.get_success_url())

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=El local ha sido creado&tipo_mensaje=info"