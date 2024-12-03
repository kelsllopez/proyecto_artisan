from django.views.generic.detail import DetailView
from .functions import generar_excel
from proveedores.functions import historial_eliminar_proveedor,historial_actualizar_proveedor,historial_crear_proveedor
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import View
from .forms import ProveedorForm, ProveedorInsumoForm, ProveedorInsumoFormUpdate
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Proveedor, ProveedorInsumo
from rest_framework import viewsets, mixins
from .serializers import ProveedorListaSerializer, ProveedorSerializer
from nucleo.mixins import ValidatePermissionRequiredMixin
from nucleo.models import Moneda,Insumo
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse,HttpResponseRedirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from io import BytesIO
# Create your views here.



@method_decorator(login_required,'dispatch')
class ProveedorInsumoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.insumo.listar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para acceder a los insumos del proveedor'

    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

@method_decorator(login_required,'dispatch')
class ProveedorViewSet( mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.listar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para acceder a los insumos del proveedor'

    queryset = Proveedor.objects.all()
    serializer_class = ProveedorListaSerializer

@method_decorator(login_required,'dispatch')
class ProveedorListaView(ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'proveedores/lista.html'

    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos para acceder a los proveedores.'

@method_decorator(login_required,'dispatch')
class ProveedorDetalleView(ValidatePermissionRequiredMixin, DetailView):
    model = Proveedor
    template_name = 'proveedores/detalle.html'

    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.detalle'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para acceder al detalle del proveedor'

    def get_context_data(self, **kwargs):
        #obtenemos el context actual
        context = super().get_context_data(**kwargs)
        #transformamos al proveedor en diccionario para un facil manejo
        instance = self.object
        context["proveedorq"] = {instance._meta.get_field(key).verbose_name if hasattr(instance._meta.get_field(key), 'verbose_name') else key: getattr(instance, key) for key in model_to_dict(instance).keys()}
        return context

@method_decorator(login_required,'dispatch')
class ProveedorCreateView(ValidatePermissionRequiredMixin, CreateView):
    template_name = 'proveedores/crear.html'
    model = Proveedor
    form_class = ProveedorForm
    #la url donde se redigira luego de crear la orden de compra
    success_url = reverse_lazy('administrador:proveedor:lista')

    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.crear'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para añadir un proveedor'

    def form_valid(self, form):
        proveedor = form.save()
        historial_crear_proveedor(self.request.user,proveedor)
        return super().form_valid(form)

@method_decorator(login_required,'dispatch')
class ProveedorActualizarView(ValidatePermissionRequiredMixin,UpdateView):
    template_name = 'proveedores/actualizar.html'
    model = Proveedor
    form_class = ProveedorForm

    #donde retorna si no hay permiso y mensaje
    permission_required = 'proveedores.actualizar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar el proveedor.'

    def get_success_url(self):
        view_name = 'administrador:proveedor:detalle'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.id})

    def form_valid(self, form):
        proveedor = form.save()
        historial_actualizar_proveedor(self.request.user,proveedor)
        return super().form_valid(form)


@method_decorator(login_required,'dispatch')
class ProveedorBorrarView(ValidatePermissionRequiredMixin,View):
    #PERMISOS
    permission_required = 'proveedores.eliminar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una asociación.'
    #FIN PERMISOS

    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #obtenemos el proveedor
            proveedor = get_object_or_404(Proveedor,pk=kwargs.get('pk'))
            #guardamos en el historial quien la borro
            historial_eliminar_proveedor(self.request.user,proveedor)
            #la borramos
            proveedor.delete()
            return JsonResponse({'estado':'ok','proveedor':proveedor.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

@method_decorator(login_required,'dispatch')
class ProveedorInsumoCreateView(ValidatePermissionRequiredMixin, CreateView):
    #PERMISOS
    permission_required = 'proveedores.insumo.crear'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear una asociación.'
    #FIN PERMISOS

    #modelo de la base de datos
    model = ProveedorInsumo
    #la template a utilizar
    template_name = 'proveedores/pi-crearv2.html'
    #el formulario de creación de asociación
    form_class = ProveedorInsumoForm
    #url de exito
    success_url = reverse_lazy('administrador:proveedor:lista')

    def get_form_kwargs(self):
        #agregamos proveedor / insumo para un manejo más rapido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'proveedor' in self.request.GET:
            kwargs['proveedor'] = self.request.GET.get('proveedor')
        if 'insumo' in self.request.GET:
            kwargs['insumo'] = self.request.GET.get('insumo')
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['monedas'] = Moneda.objects.all()
        context.update(kwargs)
        return context

    # mensaje de exito en la creación
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            return url + "?mensaje=La asociación ha sido creada&tipo_mensaje=info"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        proveedor_id = int(self.request.POST.get('proveedor'))
        insumo = Insumo.objects.filter(pk=int(self.request.POST.get('insumo'))).first()
        lead = int(self.request.POST.get('lead', 0))
        precio = float(self.request.POST.get('precio', 0))
        moneda_id = int(self.request.POST.get('moneda'))
        empaques = self.request.POST.get('empaques', None)
        uempaques = self.request.POST.get('uempaques', None)
        empaquet = self.request.POST.get('empaquet',None)
        uempaquet = self.request.POST.get('uempaquet',None)
        empaquec = self.request.POST.get('empaquec',None)
        uempaquec = self.request.POST.get('uempaquec',None)
        # unidad base
        ProveedorInsumo.objects.create(proveedor_id=proveedor_id,insumo=insumo,formato=1,moneda_id=moneda_id,precio=precio,lead=lead,nombre_insumo=f"{insumo.nombre}")
        if(empaques is not None and uempaques is not None):
            uempaques = float(uempaques)
            ProveedorInsumo.objects.create(proveedor_id=proveedor_id,insumo=insumo,formato=uempaques,moneda_id=moneda_id,precio=precio*uempaques,lead=lead,nombre_insumo="{} {}".format(empaques.capitalize(),insumo.nombre))
        if(empaquet is not None and uempaquet is not None):
            uempaquet = float(uempaquet)
            ProveedorInsumo.objects.create(proveedor_id=proveedor_id, insumo=insumo, formato=uempaquet*uempaques, moneda_id=moneda_id, precio=precio*uempaques*uempaquet, lead=lead, nombre_insumo="{} {}".format(empaquet.capitalize(),insumo.nombre))
        if(empaquec is not None and uempaquec is not None):
            uempaquec = float(uempaquec)
            ProveedorInsumo.objects.create(proveedor_id=proveedor_id, insumo=insumo, formato=uempaquec*uempaquet*uempaques, moneda_id=moneda_id, precio=precio*uempaques*uempaquet*uempaquec, lead=lead, nombre_insumo="{} {}".format(empaquec.capitalize(),insumo.nombre))

        # self.object.moneda_id = int(self.request.POST.get('moneda'))
        # self.object.save()

        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required,'dispatch')
class ProveedorExportarView(ValidatePermissionRequiredMixin,TemplateView):
    #PERMISOS
    permission_required = 'proveedores.insumo.actualizar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar la asociación.'
    template_name = 'proveedores/pi-editar.html'
    
    def get(self, request, *args, **kwargs):
        wb = generar_excel(ProveedorInsumo.objects.all(),request)
        stream = BytesIO()
        wb.save(stream)
        response = HttpResponse(stream.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}'.format('insumos.xlsx')
        return response


@method_decorator(login_required, 'dispatch')
class ProveedorInsumoUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    #PERMISOS
    permission_required = 'proveedores.insumo.actualizar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar la asociación.'
    #FIN PERMISOS
    #formulario a utilizar
    form_class = ProveedorInsumoFormUpdate
    #url de exito
    success_url = reverse_lazy('administrador:proveedor:detalle',args=[1])
    #modelo de la base de datos
    model = ProveedorInsumo
    #template a utilizar
    template_name = 'proveedores/pi-editar.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['monedas'] = Moneda.objects.all()
        context.update(kwargs)
        return context

    #mensaje de exito en la actualización
    def get_success_url(self):
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
            url = url.replace('1',str(self.object.proveedor.id))
            return url + "?mensaje=La asociación ha sido actualizada&tipo_mensaje=info"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.moneda_id = int(self.request.POST.get('moneda'))
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, 'dispatch')
class ProveedorInsumoDeleteView(ValidatePermissionRequiredMixin, View):
    # PERMISOS
    permission_required = 'proveedores.insumo.actualizar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar la asociación.'
    # FIN PERMISOS

    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            asociacion = get_object_or_404(ProveedorInsumo, pk=kwargs.get('pk'))
            asociacion.delete()
            return JsonResponse({'estado': 'ok', 'asociacion': asociacion.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})


@method_decorator(login_required, 'dispatch')
class ProveedorInsumoMostrarView(ValidatePermissionRequiredMixin, View):
    # PERMISOS
    permission_required = 'proveedores.insumo.eliminar'
    url_redirect = reverse_lazy('administrador:proveedor:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar la asociación.'
    # FIN PERMISOS
    # al obtener la peticion get

    def get(self, request, *args, **kwargs):
        # si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            # lo eliminamos y retornamos ok
            asociacion = get_object_or_404(ProveedorInsumo, pk=kwargs.get('pk'))
            asociacion.mostrar = not asociacion.mostrar
            asociacion.save()
            return JsonResponse({'estado': 'ok', 'asociacion': asociacion.id})
        else:
            # de caso contraro enviamos fallo.
            return JsonResponse({'estado': 'fallo'})
