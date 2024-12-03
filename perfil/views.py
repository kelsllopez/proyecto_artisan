from django.http.response import Http404
from .forms import PerfilUpdateForm,PerfilLoginForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView,CreateView,DetailView,View,UpdateView,FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from .models import Perfil
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import rsa
from django.conf import settings
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from PIL import Image, ImageFont, ImageDraw

import string
from random import choice
# Create your views here.

@method_decorator(login_required,'dispatch')
class PerfilUpdateView(UpdateView):
    template_name = 'perfil/perfil.html'
    model = Perfil
    form_class = PerfilUpdateForm
    success_url = reverse_lazy('perfil:perfil')

    def get_object(self, *args, **kwargs):
        chars = string.digits
        random =  ''.join(choice(chars) for _ in range(4))
        Perfil.objects.get_or_create(usuario=self.request.user,defaults={'pin':random})
        return Perfil.objects.filter(usuario=self.request.user).get()

#Generar QR de Inicio de sesión
@method_decorator(login_required,'dispatch')
class PerfilQRView(TemplateView):
    template_name = 'perfil/perfil.html'

    def get(self, request, *args, **kwargs):
        cifrado = rsa.encrypt(str(request.user.pk).encode(),settings.KEYS['publica']).hex()
        qr = qrcode.QRCode(box_size=10,border=3,error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(request.build_absolute_uri(reverse_lazy('loginqr',args=[cifrado])))
        img = qr.make_image(fill_color="black",back_color="white")
        font = ImageFont.truetype("arial.ttf", 15)
        draw = ImageDraw.Draw(img)
        nombre = request.user.first_name + " " + request.user.last_name
        draw.text((img.width*0.8,img.height*0.95),"{}".format(nombre.upper()),font=font)
        stream = BytesIO()
        img.save(stream)
        return HttpResponse(stream.getvalue(),content_type='image/png')

class LoginQRView(FormView):
    template_name = 'perfil/login.html'
    form_class = PerfilLoginForm

    def get(self, request,*args, **kwargs):
        logout(request)
        return self.render_to_response(self.get_context_data())
    
    def form_valid(self, form):
        pin = self.request.POST.get('pin')
        identificador = self.kwargs['identificador']
        try:
            identificador = rsa.decrypt(bytes.fromhex(identificador),settings.KEYS['privada']).decode('utf8')
        except:
            raise Http404
        perfil = Perfil.objects.filter(usuario=int(identificador)).filter(pin=pin).first()
        if perfil:
            login(self.request,user=perfil.usuario)
            return redirect('home')
        context = self.get_context_data()

        context['invalido'] = True
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(LoginQRView, self).get_context_data(**kwargs)
        identificador = self.kwargs['identificador']
        try:
            identificador = rsa.decrypt(bytes.fromhex(identificador),settings.KEYS['privada']).decode('utf8')
        except:
            raise Http404
        usuario = get_object_or_404(User,pk=int(identificador))
        context['usuario'] = usuario
        context['form'] = self.get_form()
        return context
        