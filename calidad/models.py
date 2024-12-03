from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from equipo.models import Equipo

# Create your models here.

class UtensilioLimpieza(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre Artículo")
    categoria = models.CharField(max_length=255, choices=settings.CATEGORIAS_UTENSILIOS)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'utensilio'
        verbose_name_plural = 'utensilio'
        permissions = (
            ('utensiliolimpieza.listar', 'Puede ver los utensilios'),
            ('utensiliolimpieza.crear', 'Puede añadir un utensilio'),
            ('utensiliolimpieza.eliminar', 'Puede eliminar un utensilio'),
            ('utensiliolimpieza.actualizar', 'Puede actualizar un utensilio'),
            ('utensiliolimpieza.asociar', 'Puede asociar un equipo al utensilio')
        )

    def __str__(self):
        return self.nombre


class GrupoEquipos(models.Model):
    nombre = models.CharField(verbose_name="Nombre del grupo", max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'Grupo Equipos'
        permissions = (
            ('grupos.listar', 'Puede listar los grupos'),
            ('grupos.crear', 'Puede crear un grupo'),
            ('grupos.eliminar', 'Puede eliminar un grupo'),
            ('grupos.actualizar', 'Puede actualizar un utensilio'),
            ('grupos.asociar', 'Puede asociar un equipo al utensilio')
        )

class GrupoEquipo(models.Model):
    grupo = models.ForeignKey(GrupoEquipos, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()

class GrupoUtensilio(models.Model):
    grupo = models.ForeignKey(GrupoEquipos, on_delete=models.CASCADE)
    utensilio = models.ForeignKey(UtensilioLimpieza, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()

class EquipoUtensilioLimpieza(models.Model):
    equipo = models.ForeignKey(Equipo, verbose_name="Equipo", on_delete=models.CASCADE)
    utensilio = models.ForeignKey(UtensilioLimpieza, verbose_name="Utensilio", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'Equipo - Utensilio'
        unique_together = ('equipo', 'utensilio',)
        verbose_name_plural = 'Equipo - Utensilio'


class RegistroLimpiezaEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, verbose_name="Equipo", on_delete=models.CASCADE)
    encargado = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.SET_NULL, null=True, related_name="encargado")
    observacion = models.TextField(verbose_name="Observación", blank=True, null=True)
    estado = models.TextField(max_length=50, choices=(('Ejecutado', 'Ejecutado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')), default="Ejecutado")
    accion_correctiva = models.TextField(verbose_name="Acción Correctiva", db_column='observacion_correctiva', blank=True, null=True)
    revisado = models.ForeignKey(User, verbose_name="Revisado", on_delete=models.SET_NULL, null=True, related_name="revisado")
    utensilios = models.ManyToManyField(UtensilioLimpieza, verbose_name="Utensilios")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        default_permissions = ()
        verbose_name = 'Registro Limpieza Equipo'
        verbose_name_plural = 'Registro Limpieza Equipos'
        permissions = (
            ('registrolimpiezaequipo.listar', 'Puede ver los registros'),
            ('registrolimpiezaequipo.administrador', 'Puede ver todos los registros'),
            ('registrolimpiezaequipo.crear', 'Puede añadir un registro'),
            ('registrolimpiezaequipo.eliminar', 'Puede eliminar un registro'),
            ('registrolimpiezaequipo.actualizar', 'Puede actualizar un registro'),
            ('registrolimpiezaequipo.excel', 'Puede generar un excel'),
        )


class RegistroLimpiezaEquipoHistorial(models.Model):
    registrolimpiezequipo = models.ForeignKey(RegistroLimpiezaEquipo, verbose_name="Registro Equipo",on_delete=models.CASCADE)
    observacion = models.TextField(verbose_name="Observación", blank=True, null=True)
    estado = models.TextField(max_length=50, choices=(('Ejecutado', 'Ejecutado'), ('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado')), default="Ejecutado")
    accion_correctiva = models.TextField(verbose_name="Acción Correctiva", db_column='observacion_correctiva', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        default_permissions = ()
        verbose_name = 'Historial Registro Limpiez Equipo'
        verbose_name_plural = 'Historial Registro Limpieza Equipos'
