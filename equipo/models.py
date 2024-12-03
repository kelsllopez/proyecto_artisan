from django.db import models
from inventario.models import Bodega

# Create your models here.

class AreaEquipo(models.Model):
    nombre = models.CharField(verbose_name="Nombre Área",max_length=255,unique=True)
    lugar = models.ForeignKey(Bodega,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'área'
        verbose_name_plural = 'áreas'
        permissions = (
                            ('area.listar', 'Puede ver las areas'),
                            ('area.crear', 'Puede añadir un area'),
                            ('area.eliminar', 'Puede eliminar una area'),
                            ('area.actualizar','Puede actualizar un area'),
                        )
    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    nombre = models.CharField(verbose_name="Nombre Equipo",max_length=255)
    area = models.ForeignKey(AreaEquipo,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'equipo'
        verbose_name_plural = 'equipos'
        permissions = (
                        ('listar', 'Puede ver los equipos'),
                        ('crear', 'Puede añadir un equipo'),
                        ('eliminar', 'Puede eliminar un equipo'),
                        ('actualizar','Puede actualizar un equipo'),
                        ('qrlimpieza','Permite generar el qr de limpieza')
                    )
    def __str__(self):
        return "{}".format(self.nombre)


    
