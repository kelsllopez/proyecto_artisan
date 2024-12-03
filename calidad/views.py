from django import http
from .functions import generar_excel
from django.http.response import Http404
from django.views.generic import TemplateView, CreateView, View, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.urls import reverse_lazy
from .serializers import EquipoRegistroLimpiezaSerializer, GrupoEquiposSerializer, UtensilioLimpiezaEquipoSerializer
from .models import EquipoUtensilioLimpieza, GrupoEquipos, RegistroLimpiezaEquipo, UtensilioLimpieza
from equipo.models import Equipo
from .forms import EquipoUtensilioForm, GruposEquiposForm, RegistroLimpiezaExcelForm, RegistroLimpiezaForm, RegistroLimpiezaUpdateOperadorForm, RegistroLimpiezaUpdateSupervisorForm, UtensilioLimpiezaForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from io import BytesIO
from datetime import datetime
# from django.utils.http import urlquote  # Eliminar esta línea o reemplazar si es necesario


#TEST
import rsa

# Create your views here.
@method_decorator(login_required,'dispatch')
class UtensilioLimpiezaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de maquinas
    permission_required = 'calidad.utensiliolimpieza.listar'
    #las maquinas compras que seran mostradas en la api rest
    queryset = UtensilioLimpieza.objects.all()
    serializer_class = UtensilioLimpiezaEquipoSerializer

#Listar los Utensilios de Limpieza
@method_decorator(login_required,'dispatch')
class UtensilioLimpiezaListView(ValidatePermissionRequiredMixin,TemplateView):
    permission_required = 'calidad.utensiliolimpieza.listar'
    template_name = 'calidad/utensiliolimpieza/list.html'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para administrar los utensilios de limpieza.'

@method_decorator(login_required,'dispatch')
class UtensilioLimpiezaCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso requerido para la vista
    permission_required = 'calidad.utensiliolimpieza.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para añadir un utensilio de limpieza.'
    #modelo
    model = UtensilioLimpieza
    form_class = UtensilioLimpiezaForm
    #template
    template_name = 'calidad/utensiliolimpieza/create.html'
    success_url = reverse_lazy('calidad:utensiliolimpieza:lista')

@method_decorator(login_required,'dispatch')
class UtensilioLimpiezaUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso requerido para la vista
    permission_required = 'calidad.utensiliolimpieza.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un utensilio de limpieza.'
    #modelo
    model = UtensilioLimpieza
    form_class = UtensilioLimpiezaForm
    #template
    template_name = 'calidad/utensiliolimpieza/update.html'
    success_url = reverse_lazy('calidad:utensiliolimpieza:lista')

#Eliminar Utensilio
@method_decorator(login_required,'dispatch')
class UtensilioLimpiezaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'calidad.utensiliolimpieza.eliminar'
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este utensilio.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            utensilio = get_object_or_404(UtensilioLimpieza,pk=kwargs.get('pk'))
            #historial_delete_bodega(self.request.user,bodega)
            utensilio.delete()
            return JsonResponse({'estado':'ok','utensilio':utensilio.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Añadir Asociación
@method_decorator(login_required,'dispatch')
class EquipoUtensilioCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso requerido para la vista
    permission_required = 'calidad.utensiliolimpieza.asociar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para asociar un utensilio de limpieza.'
    #modelo
    model = EquipoUtensilioLimpieza
    form_class = EquipoUtensilioForm
    #template
    template_name = 'calidad/equipoutensilio/create.html'
    success_url = reverse_lazy('calidad:utensiliolimpieza:lista')

    def get_form_kwargs(self):
        #agregamos proveedor / insumo para un manejo más rapido de las asociaciones.
        kwargs = super().get_form_kwargs()
        if 'utensilio' in self.request.GET:
            kwargs['utensilio'] = self.request.GET.get('utensilio')
        return kwargs

#Eliminar Asociación
@method_decorator(login_required,'dispatch')
class EquipoUtensilioLimpiezaDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'calidad.utensiliolimpieza.easociar'
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta asociación.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            utensilio = get_object_or_404(EquipoUtensilioLimpieza,pk=kwargs.get('pk'))
            #historial_delete_bodega(self.request.user,bodega)
            utensilio.delete()
            return JsonResponse({'estado':'ok','utensilio':utensilio.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Seleccionador de Registro de Limpieza
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoSeleccionView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso requerido para la vista
    permission_required = 'calidad.registrolimpiezaequipo.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para registrar una limpieza.'
    template_name = 'calidad/registrolimpiezaequipo/seleccion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        try:
            descifrar = rsa.decrypt(bytes.fromhex(pk),settings.KEYS['privada']).decode('utf8')
        except:
            raise Http404
        equipo = get_object_or_404(Equipo,pk=int(descifrar))
        if self.request.user.groups.filter(name__in=['Supervisor']).exists():
            supervisar = RegistroLimpiezaEquipo.objects.filter(equipo=equipo).exclude(estado="Aprobado").exclude(estado='Pendiente').all()
        else:
            supervisar = []
        registros = RegistroLimpiezaEquipo.objects.filter(equipo=equipo,encargado=self.request.user).exclude(estado='Aprobado')
        context['registros'] = registros.all()
        context['personales'] = supervisar
        context['equipo'] = equipo
        context['identificador'] = pk
        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            descifrar = rsa.decrypt(bytes.fromhex(pk),settings.KEYS['privada']).decode('utf8')
        except:
            raise Http404
        equipo = get_object_or_404(Equipo,pk=int(descifrar))
        #ver si el usuario tiene tareas pendientes con este equipo
        registros = RegistroLimpiezaEquipo.objects.filter(equipo=equipo,encargado=self.request.user).exclude(estado='Aprobado')
        if len(registros) == 0 and not self.request.user.groups.filter(name__in=['Supervisor']).exists():
            return redirect(reverse_lazy('calidad:limpiezaequipo:crear') + "?equipo={}".format(pk))
        return super().get(request, *args, **kwargs)

#Agregar Registro de Limpieza
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso requerido para la vista
    permission_required = 'calidad.registrolimpiezaequipo.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para registrar una limpieza.'
    #modelo
    model = RegistroLimpiezaEquipo
    form_class = RegistroLimpiezaForm
    #template
    template_name = 'calidad/registrolimpiezaequipo/create.html'
    success_url = reverse_lazy('calidad:limpiezaequipo:lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'equipo' in self.request.GET:
            kwargs['equipo'] = self.request.GET.get('equipo')
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.encargado = self.request.user
        #creamos el historial
        self.object.registrolimpiezaequipohistorial_set.create(observacion=self.object.observacion,estado=self.object.estado,accion_correctiva=self.object.accion_correctiva)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get(self, request, *args, **kwargs):
        if 'equipo' in self.request.GET:
            pk = self.request.GET.get('equipo')
            try:
                descifrar = rsa.decrypt(bytes.fromhex(pk),settings.KEYS['privada']).decode('utf8')
            except:
                raise Http404
            equipo = get_object_or_404(Equipo,pk=int(descifrar))
            if equipo:
                return super().get(request, *args, **kwargs)
        raise Http404


#Actualizar Registro de Limpieza
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso requerido para la vista
    permission_required = 'calidad.registrolimpiezaequipo.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una limpieza.'
    #modelo
    model = RegistroLimpiezaEquipo
    #template
    template_name = 'calidad/registrolimpiezaequipo/update.html'
    success_url = reverse_lazy('calidad:limpiezaequipo:lista')

    def get_form_class(self):
        if self.request.user.has_perm('calidad.registrolimpiezaequipo.administrador'):
            return RegistroLimpiezaUpdateSupervisorForm
        else:
            return RegistroLimpiezaUpdateOperadorForm
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            if not self.request.user.has_perm('calidad.registrolimpiezaequipo.administrador'):
                if obj.encargado != self.request.user:
                    raise Http404("Página no encontrada")
                else:
                    if obj.estado == 'Aprobado':
                        raise Http404("Página no encontrada")
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                        {'verbose_name': queryset.model._meta.verbose_name})
        return obj
    
    def form_valid(self, form):
        self.object = form.save()
        if self.request.user.has_perm('calidad.registrolimpiezaequipo.administrador'):
            self.object.revisado = self.request.user
        else:
            self.object.estado = 'Ejecutado'
        #creamos el historial
        self.object.registrolimpiezaequipohistorial_set.create(observacion=self.object.observacion,estado=self.object.estado,accion_correctiva=self.object.accion_correctiva)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

#Listar los Registros de Limpieza de Equipo
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoListView(ValidatePermissionRequiredMixin,TemplateView):
    permission_required = 'calidad.registrolimpiezaequipo.listar'
    template_name = 'calidad/registrolimpiezaequipo/list.html'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver los registros de limpieza.'

#Eliminar Registro
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'calidad.registrolimpiezaequipo.eliminar'
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta asociación.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            registro = get_object_or_404(RegistroLimpiezaEquipo,pk=kwargs.get('pk'))
            #historial_delete_bodega(self.request.user,bodega)
            registro.delete()
            return JsonResponse({'estado':'ok','registro':registro.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Generar Excel
@method_decorator(login_required,'dispatch')
class RegistroLimpiezaEquipoExcel(ValidatePermissionRequiredMixin,FormView):
    #permiso
    permission_required = 'calidad.registrolimpiezaequipo.excel'
    url_redirect = reverse_lazy('calidad:utensiliolimpieza:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para exportar los registros.'

    form_class = RegistroLimpiezaExcelForm
    template_name = 'calidad/registrolimpiezaequipo/excel.html'

    def form_valid(self, form):
        #obtenemos las fechas para las cuales queremos generar el excel
        fecha_inicio = form.cleaned_data.get('fechainicio')
        fecha_fin = form.cleaned_data.get('fechafin')
        fecha_fin_m = datetime(year=fecha_fin.year,month=fecha_fin.month,day=fecha_fin.day).replace(hour = 23,minute=59)
        registros = RegistroLimpiezaEquipo.objects.filter(created__range=[fecha_inicio,fecha_fin_m])
        excel = generar_excel(fecha_inicio,fecha_fin,registros,self.request)
        stream = BytesIO()
        excel.save(stream)
        response = HttpResponse(stream.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}'.format('registroequipo-{}.xlsx'.format(fecha_inicio))
        return response

#La Llamada a la api de los registros de limpieza
@method_decorator(login_required,'dispatch')
class EquipoRegistroLimpiezaViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de maquinas
    permission_required = 'calidad.registrolimpiezaequipo.listar'
    #los registros que seran mostrados en la api
    queryset = RegistroLimpiezaEquipo.objects.all()
    serializer_class = EquipoRegistroLimpiezaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        permiso = 'calidad.registrolimpiezaequipo.administrador'
        #logica para solo mostrar los registros correspondientes a ese usuario.
        if 'envia' in request.GET:
            envia = request.GET.get('envia')
            try:
                descifrar = rsa.decrypt(bytes.fromhex(envia),settings.KEYS['privada']).decode('utf8')
            except:
                raise Http404
            if self.request.user.has_perm(permiso):
                queryset = queryset
            else:
                queryset = queryset.filter(encargado=int(descifrar))
        else:
            raise Http404
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = {'data':'No'}
        permiso = 'calidad.registrolimpiezaequipo.administrador'
        #logica para solo mostrar los registros correspondientes a ese usuario.
        if self.request.user.has_perm(permiso):
            serializer = self.get_serializer(instance)
        else:
            if instance.encargado.pk == self.request.user.pk:
                serializer = self.get_serializer(instance)
            else:
                raise Http404
        return Response(serializer.data)

#Lista de grupos de equipos y utensilios
@method_decorator(login_required,'dispatch')
class GrupoListView(ValidatePermissionRequiredMixin,TemplateView):
    #permiso
    permission_required = 'calidad.grupos.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar los grupos'
    template_name = 'calidad/grupo/list.html'

#Api para ver los grupos de equipos y utensilos
@method_decorator(login_required,'dispatch')
class GruposEquiposViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de maquinas
    permission_required = 'calidad.grupos.listar'
    #las maquinas compras que seran mostradas en la api rest
    queryset = GrupoEquipos.objects.all()
    serializer_class = GrupoEquiposSerializer

#Crear Grupo
@method_decorator(login_required,'dispatch')
class GrupoCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso
    permission_required = 'calidad.grupos.crear'
    url_redirect = reverse_lazy('calidad:grupo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear un grupo'
    template_name = 'calidad/grupo/create.html'
    success_url = reverse_lazy('calidad:grupo:lista')
    model = GrupoEquipos
    form_class = GruposEquiposForm

#Actualizar Grupo
@method_decorator(login_required,'dispatch')
class GrupoUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso
    permission_required = 'calidad.grupos.actualizar'
    url_redirect = reverse_lazy('calidad:grupo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un grupo'
    template_name = 'calidad/grupo/create.html'
    success_url = reverse_lazy('calidad:grupo:lista')
    model = GrupoEquipos
    form_class = GruposEquiposForm

#Eliminar Grupo
@method_decorator(login_required,'dispatch')
class GrupoDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'calidad.grupos.eliminar'
    url_redirect = reverse_lazy('calidad:grupo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar este grupo.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            grupo = get_object_or_404(GrupoEquipos,pk=kwargs.get('pk'))
            #historial_delete_bodega(self.request.user,bodega)
            grupo.delete()
            return JsonResponse({'estado':'ok'})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

@login_required
def probando(request,string):
    if len(string) > 5:
        decifrado = rsa.decrypt(bytes.fromhex(string),settings.KEYS['privada']).decode('utf8')
        return HttpResponse(f"tu string es: {decifrado}")
    cifrado = rsa.encrypt(string.encode(),settings.KEYS['publica']).hex()
    descifrar = rsa.decrypt(bytes.fromhex(cifrado),settings.KEYS['privada']).decode('utf8')
    return HttpResponse("tu string {} cifrado es {} y decifrado es {}.".format(string,cifrado,descifrar))

#   ------------------------------- PRODUCCION Y CALIDAD -------------------------------------------------------------#
from produccion.models import * 

from django.shortcuts import render
from django.views.generic import TemplateView
from produccion.models import PautaProduccion
from produccion.forms import CalidadProduccionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, 'dispatch')
class produccionlista(TemplateView):
    permission_required = 'calidad.produccion.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las producciones'
    template_name = 'calidad/produccion/lista_calidad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los objetos de PautaProduccion y CalidadProduccion
        producciones = PautaProduccion.objects.all()
        calidad_producciones = CalidadProduccion.objects.all()

        # Pasa ambos objetos al contexto
        context['producciones'] = producciones
        context['calidad_producciones'] = calidad_producciones
        return context
        
from django.contrib import messages

@method_decorator(login_required, 'dispatch')
class produccionagregar(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'calidad.produccion.agregar'
    url_redirect = reverse_lazy('calidad:elaboraciones:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las producciones'
    template_name = 'calidad/produccion/detalle.html'
    success_url = reverse_lazy('calidad:elaboraciones:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)

        # Obtener los detalles relacionados
        instrucciones = InstruccionProduccion.objects.filter(pauta_produccion=pauta_produccion)
        # Obtener o crear la calidad de producción
        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()

        # Si no existe una calidad de producción para esta pauta, la creamos vacía
        if not calidad_produccion:
            calidad_produccion = CalidadProduccion(pauta_produccion=pauta_produccion)

        context.update({
            'pauta_produccion': pauta_produccion,
            'instrucciones': instrucciones,
            'calidad_form': CalidadProduccionForm(instance=calidad_produccion),
            'calidad_produccion': calidad_produccion  # Si necesitas acceder al objeto en el template
        })

        return context

    def post(self, request, *args, **kwargs):
        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)

        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()
        if not calidad_produccion:
            calidad_produccion = CalidadProduccion(pauta_produccion=pauta_produccion)

        # Crear el formulario a partir de los datos de la solicitud POST
        form = CalidadProduccionForm(request.POST, instance=calidad_produccion)

        if form.is_valid():
            form.save()  # Guarda el objeto en la base de datos

            # Asegúrate de que el mensaje de éxito se vea
            messages.success(request, 'Estado de aprobación actualizado correctamente.')

            return redirect(self.success_url)

        # Si el formulario no es válido, renderizamos nuevamente con errores
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)



@method_decorator(login_required,'dispatch')
class producciondetalle(ValidatePermissionRequiredMixin,TemplateView):
    #permiso
    permission_required = 'calidad.produccion.listar'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar las producciones'
    template_name = 'calidad/produccion/agregar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el ID de la pauta de producción desde la URL
        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)
        instrucciones = InstruccionProduccion.objects.filter(pauta_produccion=pauta_produccion)
        # Obtener la calidad de producción asociada a esta pauta
        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()

        # Crear el formulario para actualizar el estado de aprobación
        form = CalidadProduccionForm(instance=calidad_produccion)

        # Pasar todos los datos al contexto para el template
        context.update({
            'pauta_produccion': pauta_produccion,
            'instrucciones': instrucciones,
            'calidad_produccion': calidad_produccion,
            'form': form,
        })

        return context

    def post(self, request, *args, **kwargs):
        # Obtener el ID de la pauta de producción desde la URL
        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)

        # Obtener la calidad de producción asociada a esta pauta
        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()

        # Crear el formulario para actualizar el estado de aprobación
        form = CalidadProduccionForm(request.POST, instance=calidad_produccion)

        if form.is_valid():
            form.save()
            messages.success(request, 'Estado de aprobación actualizado correctamente.')
            return redirect('detalle_produccion', pauta_id=pauta_produccion.id)

        # Si el formulario no es válido, renderizar de nuevo la página con los errores
        context = self.get_context_data(pauta_id=pauta_produccion.id)
        context['form'] = form
        return self.render_to_response(context)
    

@method_decorator(login_required, 'dispatch')
class ProduccionModificarView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'calidad.produccion.modificar'
    url_redirect = reverse_lazy('calidad:elaboraciones:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para modificar esta producción'
    template_name = 'calidad/produccion/modificar.html'  # Asegúrate de tener esta plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)

        # Obtener las instrucciones de producción
        instrucciones = InstruccionProduccion.objects.filter(pauta_produccion=pauta_produccion)

        # Obtener o crear la calidad de producción
        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()

        if not calidad_produccion:
            calidad_produccion = CalidadProduccion(pauta_produccion=pauta_produccion)

        # Agregar el formulario al contexto para que se renderice
        context.update({
            'pauta_produccion': pauta_produccion,
            'instrucciones': instrucciones,
            'calidad_form': CalidadProduccionForm(instance=calidad_produccion),
            'calidad_produccion': calidad_produccion
        })

        return context

    def post(self, request, *args, **kwargs):
        pauta_produccion_id = kwargs.get('pauta_id')
        pauta_produccion = get_object_or_404(PautaProduccion, id=pauta_produccion_id)

        calidad_produccion = CalidadProduccion.objects.filter(pauta_produccion=pauta_produccion).first()
        if not calidad_produccion:
            calidad_produccion = CalidadProduccion(pauta_produccion=pauta_produccion)

        # Crear el formulario con los datos del POST
        form = CalidadProduccionForm(request.POST, instance=calidad_produccion)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producción actualizada correctamente.')
            return redirect(reverse_lazy('calidad:elaboraciones:lista'))  # Redirige a la lista de producciones

        # Si el formulario no es válido, renderizamos de nuevo el formulario con errores
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)