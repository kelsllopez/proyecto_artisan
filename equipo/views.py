from .functions import historial_create_area, historial_delete_area, historial_delete_equipo,historial_create_equipo, historial_update_area,historial_update_equipo
from .forms import AreaEquipoForm, EquipoForm
from .serializers import AreaSerializer, EquipoSerializer
from .models import AreaEquipo, Equipo
from django.views.generic import TemplateView,CreateView,View,DetailView,UpdateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from django.urls import reverse_lazy
from django.conf import settings
from PIL import Image, ImageFont, ImageDraw, ImageOps
import math

#qr
import qrcode
from io import BytesIO
from django.http import HttpResponse
import rsa

# Create your views here.
@method_decorator(login_required,'dispatch')
class EquipoViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de maquinas
    permission_required = 'equipo.listar'
    #las maquinas compras que seran mostradas en la api rest
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

@method_decorator(login_required,'dispatch')
class EquipoListView(ValidatePermissionRequiredMixin,TemplateView):
    permission_required = 'equipo.listar'
    template_name = 'equipo/equipo-list.html'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para administrar las máquinas.'

@method_decorator(login_required,'dispatch')
class EquipoCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso requerido para la vista
    permission_required = 'equipo.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:equipo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para añadir una máquina.'
    #modelo
    model = Equipo
    form_class = EquipoForm
    #template
    template_name = 'equipo/equipo-create.html'
    success_url = reverse_lazy('administrador:equipo:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_create_equipo(self.request.user,self.object)
        return super().form_valid(form)

@method_decorator(login_required,'dispatch')
class EquipoUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso requerido para la vista
    permission_required = 'equipo.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:equipo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar una máquina.'
    #modelo
    model = Equipo
    form_class = EquipoForm
    #template
    template_name = 'equipo/equipo-update.html'
    success_url = reverse_lazy('administrador:equipo:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_update_equipo(self.request.user,self.object)
        return super().form_valid(form)

#Eliminar Máquina
@method_decorator(login_required,'dispatch')
class EquipoDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'equipo.eliminar'
    url_redirect = reverse_lazy('administrador:equipo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta máquina.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            equipo = get_object_or_404(Equipo,pk=kwargs.get('pk'))
            historial_delete_equipo(self.request.user,equipo)
            equipo.delete()
            return JsonResponse({'estado':'ok','equipo':equipo.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})

#Generar QR Limpieza
@method_decorator(login_required,'dispatch')
class EquipoQRView(ValidatePermissionRequiredMixin,DetailView):
    #permiso requerido para la vista
    permission_required = 'equipo.qrlimpieza'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:equipo:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el qr de limpieza asociado a la maquina.'
    template_name = 'equipo/equipo-qr.html'
    model = Equipo

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cifrado = rsa.encrypt(str(self.object.pk).encode(),settings.KEYS['publica']).hex()
        qr = qrcode.QRCode(box_size=10,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(request.build_absolute_uri(reverse_lazy('calidad:limpiezaequipo:seleccionar', args=[cifrado])))
        img = qr.make_image(fill="black")
        font = ImageFont.truetype("arial.ttf", 15)
        draw = ImageDraw.Draw(img)
        nombre = self.object.nombre
        
        draw.text((img.width*0.8,img.height*0.022),"{}".format(nombre.upper()),font=font)
        if self.object.area:
            draw.text((img.width*0.8,img.height*0.95),"{}".format(self.object.area.lugar.nombre.upper()),font=font)
            img = img.rotate(90)
            draw = ImageDraw.Draw(img)
            draw.text((img.width*0.07,img.height*0.022),"{}".format(self.object.area.nombre.upper()),font=font)
            img = img.rotate(270)
        
        stream = BytesIO()
        img.save(stream,format='PNG')
        return HttpResponse(stream.getvalue(),content_type='image/png')


#API PARA LISTAR LAS AREAS
@method_decorator(login_required,'dispatch')
class AreaEquipoViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    #permiso necesario para ver la lista de maquinas
    permission_required = 'equipo.area.listar'
    #las maquinas compras que seran mostradas en la api rest
    queryset = AreaEquipo.objects.all()
    serializer_class = AreaSerializer

#LISTAR LAS ÁREAS DE EQUIPO
@method_decorator(login_required,'dispatch')
class AreaEquipoListView(ValidatePermissionRequiredMixin,TemplateView):
    permission_required = 'equipo.area.listar'
    template_name = 'equipo/area/list.html'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver las áreas de equipo.'

#CREAR UN ÁREA DE EQUIPOS
@method_decorator(login_required,'dispatch')
class AreaEquipoCreateView(ValidatePermissionRequiredMixin,CreateView):
    #permiso requerido para la vista
    permission_required = 'equipo.area.crear'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:equipo:area:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para añadir un área de equipo.'
    #modelo
    model = AreaEquipo
    form_class = AreaEquipoForm
    #template
    template_name = 'equipo/area/create.html'
    success_url = reverse_lazy('administrador:equipo:area:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_create_area(self.request.user,self.object)
        return super().form_valid(form)
    
    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje= se ha creado el Área correctamente."

#ACTUALIZAR UN ÁREA DE EQUIPOS
@method_decorator(login_required,'dispatch')
class AreaEquipoUpdateView(ValidatePermissionRequiredMixin,UpdateView):
    #permiso requerido para la vista
    permission_required = 'equipo.area.actualizar'
    #donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('administrador:equipo:area:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar un área de equipo.'
    #modelo
    model = AreaEquipo
    form_class = AreaEquipoForm
    #template
    template_name = 'equipo/area/update.html'
    success_url = reverse_lazy('administrador:equipo:area:lista')

    def form_valid(self, form):
        self.object = form.save()
        historial_update_area(self.request.user,self.object)
        return super().form_valid(form)
    
    def get_success_url(self):
        return super().get_success_url() + "?tipo=info&mensaje= se ha actualizado el Área correctamente."

#ELIMINAR UN ÁREA DE EQUIPOS
@method_decorator(login_required,'dispatch')
class AreaEquipoDeleteView(ValidatePermissionRequiredMixin,View):
    #permiso
    permission_required = 'equipo.area.eliminar'
    url_redirect = reverse_lazy('administrador:equipo:area:lista')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar esta área.'
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            area = get_object_or_404(AreaEquipo,pk=kwargs.get('pk'))
            historial_delete_area(self.request.user,area)
            area.delete()
            return JsonResponse({'estado':'ok','area':area.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})