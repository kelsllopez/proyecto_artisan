from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from inventario.models import Bodega
import string
from random import choice

# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles", null=True, blank=True)
    pin = models.CharField(verbose_name="Pin", max_length=4)
    lugar = models.ForeignKey(Bodega, verbose_name="Lugar de Trabajo", on_delete=models.SET_NULL, null=True, blank=True)
    firma_digital = models.ImageField(upload_to="firmas", null=True, blank=True)


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        default_permissions = ()


#crear perfil al momento de crear un usuario
@receiver(models.signals.post_save, sender=User)
def crear_perfil(sender, instance, **kwargs):
    if kwargs.get('created', False):
        chars = string.digits
        random = ''.join(choice(chars) for _ in range(4))
        Perfil.objects.get_or_create(usuario=instance, defaults={'pin': random})



