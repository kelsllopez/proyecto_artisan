from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from .functions import historial_solicitud

from nucleo.models import Insumo
from .forms import SolicitudForm
from .models import Solicitud
from .serializers import SolicitudSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from rest_framework import viewsets, mixins


# Vista api solicitudes
@method_decorator(login_required, 'dispatch')
class SolicitudViewSet(ValidatePermissionRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    # permiso necesario
    permission_required = 'solicitudes.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las solicitudes.'


# Vista de todas las solicitudes
@method_decorator(login_required, 'dispatch')
class SolicitudListView(ValidatePermissionRequiredMixin, TemplateView):
    # permiso necesario
    permission_required = 'solicitudes.listar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las solicitudes.'
    # template
    template_name = 'solicitudes/list.html'


# actualizar solicitud
@method_decorator(login_required, 'dispatch')
class SolicitudUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    # permiso necesario
    permission_required = 'solicitudes.actualizar'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    success_url = reverse_lazy('solicitudes:lista')
    mensaje = 'No tienes los permisos necesarios para actualizar las solicitudes.'
    # template
    template_name = 'solicitudes/update.html'
    # modelo
    model = Solicitud
    form_class = SolicitudForm

    # le entregamos al formulario la info necesaria
    def get_form_kwargs(self):
        kwargs = super(SolicitudUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        solicitud = super(SolicitudUpdateView, self).get_object()
        kwargs['encargados'] = [se.encargado.pk for se in solicitud.solicitudencargados_set.all()]
        return kwargs

    # verificamos que la solicitud se encuentre en estado no completada.
    def dispatch(self, request, *args, **kwargs):
        solicitud = super(SolicitudUpdateView, self).get_object()
        if solicitud.estado == 'Completada':
            raise Http404('La solicitud no puede ser actualizada, ya que se encuentra en estado completada.')
        return super().dispatch(request, *args, **kwargs)

    # si el formulario es valido
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # le asignamos los encargados
        encargados = [int(x) for x in self.request.POST.getlist('encargados')]
        for e in encargados:
            check = self.object.solicitudencargados_set.filter(encargado_id=e).first()
            if check is None:
                self.object.solicitudencargados_set.create(encargado_id=e)
        # eliminamos los encargados que no estan
        [encargado.delete() for encargado in self.object.solicitudencargados_set.all() if encargado.encargado.pk not in encargados]
        # le asignamos los insumos
        insumos = [int(x) for x in self.request.POST.getlist('insumo')]
        cantidad = [float(x) for x in self.request.POST.getlist('insumocantidad')]
        comentario = self.request.POST.getlist('insumocomentario')
        for i, insumo in enumerate(insumos):
            # verificamos que el insumo exista realmente
            insumo = Insumo.objects.filter(pk=insumo).first()
            check, created = self.object.solicitudinsumos_set.get_or_create(insumo=insumo, defaults={'cantidad': cantidad[i], 'comentario': comentario[i]})
            if created is False:
                check.cantidad = cantidad[i]
                check.comentario = comentario[i]
                check.save()
        # eliminamos los insumos que no estan
        [insumo.delete() for insumo in self.object.solicitudinsumos_set.all() if insumo.insumo.pk not in insumos]
        historial_solicitud(self.request.user, self.object, "cambiado")
        self.object.notificar()
        return HttpResponseRedirect(self.get_success_url())


# Crear solicitud
@method_decorator(login_required, 'dispatch')
class SolicitudCreateView(ValidatePermissionRequiredMixin, CreateView):
    # permiso necesario
    permission_required = 'solicitudes.crear'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    success_url = reverse_lazy('solicitudes:lista')
    mensaje = 'No tienes los permisos necesarios para crear las solicitudes.'
    # template
    template_name = 'solicitudes/create.html'
    # modelo
    model = Solicitud
    form_class = SolicitudForm

    def get_form_kwargs(self):
        kwargs = super(SolicitudCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lugar_o = self.request.user.perfil.lugar
        self.object.solicitante = self.request.user
        self.object.save()
        # le asignamos los encargados
        encargados = [int(x) for x in self.request.POST.getlist('encargados')]
        for e in encargados:
            self.object.solicitudencargados_set.create(encargado_id=e)
        # le asignamos los insumos
        insumos = [int(x) for x in self.request.POST.getlist('insumo')]
        cantidad = [float(x) for x in self.request.POST.getlist('insumocantidad')]
        comentario = self.request.POST.getlist('insumocomentario')
        for i, insumo in enumerate(insumos):
            if cantidad[i] > 0:
                # verificamos que el insumo exista realmente
                insumo = Insumo.objects.filter(pk=insumo).first()
                if insumo:
                    self.object.solicitudinsumos_set.create(insumo=insumo, comentario=comentario[i], cantidad=cantidad[i])
        self.object.notificar()
        historial_solicitud(self.request.user, self.object, "agregado")
        return HttpResponseRedirect(self.get_success_url())


# Completar Solicitud
@method_decorator(login_required, 'dispatch')
class SolicitudCompletarView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'solicitud.completar'

    # al obtener la peticion get
    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            solicitud = get_object_or_404(Solicitud, pk=kwargs.get('pk'))
            if solicitud.estado == 'No Completada':
                solicitud.estado = 'Completada'
                solicitud.save()
                historial_solicitud(self.request.user, solicitud, "cambiado")
            return JsonResponse({'estado': 'ok'})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})


# Eliminar Solicitud
@method_decorator(login_required, 'dispatch')
class SolicitudDeleteView(ValidatePermissionRequiredMixin, View):
    # permiso
    permission_required = 'solicitudes.eliminar'

    # al obtener la peticion get
    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            solicitud = get_object_or_404(Solicitud, pk=kwargs.get('pk'))
            historial_solicitud(self.request.user, solicitud, "borrado")
            solicitud.delete()
            return JsonResponse({'estado': 'ok', 'solicitud': solicitud.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})
