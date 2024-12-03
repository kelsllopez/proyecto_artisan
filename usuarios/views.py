from django.http.response import HttpResponseRedirect
from nucleo.functions import enviar_correo
from django.views.generic import TemplateView, UpdateView, View, CreateView
from .serializers import GroupSerializer, UserSerializer
from .forms import GroupCreateForm, UserCreateForm, UserUpdateForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.decorators import user_passes_test,login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from nucleo.mixins import ValidatePermissionRequiredMixin
import string
import random
# Create your views here.


#API DE USUARIOS
#Generación de la api de los usuarios ser consumida por sus vistas
@method_decorator(login_required, name='dispatch')
class UserViewSet(ValidatePermissionRequiredMixin,mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_required = 'nucleo.permiso.listar.usuario'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar usuarios.'
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(login_required, name='dispatch')
class CreateUserView(ValidatePermissionRequiredMixin,CreateView):
    model = User
    template_name = 'usuarios/usuario-create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('administrador:usuario:lista')

    permission_required = 'nucleo.permiso.crear.usuario'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para crear usuarios.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view').all()
        return context
 
    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = True
        self.object.save()
        palabras = ['yogurt','queso','leche','artisan']
        chars = string.digits
        numeros =  ''.join(random.choice(chars) for _ in range(4))
        palabra = palabras[random.randint(0,3)]
        password = palabra + numeros
        self.object.password = make_password(password)
        self.object.save()
        self.object.perfil.lugar_id = int(self.request.POST.get('ubicacion'))
        self.object.perfil.save()
        enviar_correo(self.object,password,self.request)
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class UpdateUserView(ValidatePermissionRequiredMixin,UpdateView):
    model = User
    template_name = 'usuarios/usuario-update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('administrador:usuario:lista')

    permission_required = 'nucleo.permiso.actualizar.usuario'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para actualizar usuarios.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view').all()
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.object.is_superuser:
            self.object.is_active = True
        self.object.save()
        self.object.perfil.lugar_id = int(self.request.POST.get('ubicacion'))
        self.object.perfil.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class ListUserView(ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'usuarios/usuario-list.html'

    permission_required = 'nucleo.permiso.listar.usuario'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para listar usuarios.'


#Eliminar Usuario
@method_decorator(login_required, name='dispatch')
class DeleteUserView(ValidatePermissionRequiredMixin,View):
    permission_required = 'nucleo.permiso.eliminar.usuario'
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para eliminar usuarios.'

    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            usuario = get_object_or_404(User,pk=kwargs.get('pk'))
            usuario.delete()
            return JsonResponse({'estado':'ok','usuario':usuario.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})
    


#Grupos
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class GroupViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ListGroupView(TemplateView):
    template_name = 'usuarios/group-list.html'

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CreateGroupView(CreateView):
    template_name = 'usuarios/group-create.html'
    model = Group
    form_class = GroupCreateForm
    success_url = reverse_lazy('administrador:grupo:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view').all()
        return context

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UpdateGroupView(UpdateView):
    template_name = 'usuarios/group-update.html'
    model = Group
    form_class = GroupCreateForm
    success_url = reverse_lazy('administrador:grupo:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view').all()
        return context

#Eliminar Grup
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class DeleteGroupView(View):
    #al obtener la peticion get
    def get(self, request, *args, **kwargs):
        #si es que se encuentra la primary key en los kwargs
        if 'pk' in kwargs:
            #lo eliminamos y retornamos ok
            grupo = get_object_or_404(Group,pk=kwargs.get('pk'))
            grupo.delete()
            return JsonResponse({'estado':'ok','grupo':grupo.id})
        else:
            #de caso contraro enviamos fallo.
            return JsonResponse({'estado':'fallo'})