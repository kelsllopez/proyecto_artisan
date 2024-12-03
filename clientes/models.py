from django.conf import settings
from django.db import models
from django.dispatch import receiver
from nucleo.models import Rama

# Modelos de Clientes


class Cliente(models.Model):
    tipo = models.CharField(max_length=255, choices=(
        ('', '-- Seleccione --'),
        ('HORECA', 'Hotel - Restaurant - Casino'),
        ('Retail', 'Retail'),
        ('Venta Web,', 'Venta Web'),
        ('Persona Natural', 'Persona Natural')
    ), verbose_name="tipo de cliente")
    nombre = models.CharField(max_length=255, verbose_name="nombre comercial")
    razon_social = models.CharField(max_length=255, verbose_name="razón social", blank=True, null=True)
    rut = models.CharField(max_length=50, verbose_name="Rut Cliente", blank=True, null=True)
    giro = models.CharField(max_length=100, verbose_name="Giro Cliente", blank=True, null=True)
    pago = models.CharField(max_length=255, verbose_name="Forma de Pago", blank=True, null=True, choices=(
        ('', '-- Seleccione --'),
        ('Contado', 'Contado'),
        ('Credito 15 días', 'Credito 15 días'),
        ('Credito 30 días', 'Credito 30 días'),
        ('Credito 60 días', 'Credito 60 días')
    ))
    telefono = models.CharField(max_length=255, verbose_name="Teléfono Cliente", null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name="Región", null=True, blank=True, choices=settings.REGIONES)
    comuna = models.CharField(max_length=255, verbose_name="Comuna", null=True, blank=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    contacto = models.CharField(max_length=255, verbose_name="Nombre del Contacto", blank=True, null=True)
    email = models.CharField(max_length=255, verbose_name="Correo Electrónico", null=True, blank=True)
    celular = models.CharField(max_length=255, verbose_name="Celular Contacto", null=True, blank=True)
    listap = models.ForeignKey('ventas.ListaPrecio', on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name="Lista de Precios")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ['-created']
        default_permissions = ()
        permissions = (
            ('cliente.listar', 'Puede ver el listado de los clientes'),
            ('cliente.crear', 'Puede crear un cliente'),
            ('cliente.eliminar', 'Permite eliminar un cliente'),
            ('cliente.actualizar', 'Permite actualizar un cliente'),
            ('cliente.detalle', 'Permite ver el detalle de un cliente')
        )

    def __str__(self):
        return self.nombre


class ClienteLocal(models.Model):
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", on_delete=models.CASCADE)
    local = models.CharField(max_length=255, verbose_name="Nombre del local")
    telefono = models.CharField(max_length=255, verbose_name="Teléfono", null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name="Región", null=True, blank=True, choices=settings.REGIONES)
    comuna = models.CharField(max_length=255, verbose_name="Comuna", null=True, blank=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    contacto = models.CharField(max_length=255, verbose_name="Nombre del Contacto", null=True, blank=True)
    email = models.CharField(max_length=255, verbose_name="Correo Electrónico", null=True, blank=True)
    celular = models.CharField(max_length=255, verbose_name="Celular Contacto", null=True, blank=True)
    id_comercio_electronico = models.CharField(max_length=255, verbose_name="Identificador Comercio Electrónico", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "local"
        verbose_name_plural = "locales"
        ordering = ['-created']
        default_permissions = ()
        permissions = (
            ('local.listar', 'Puede ver el listado de los locales'),
            ('local.crear', 'Puede crear un local'),
            ('local.eliminar', 'Permite eliminar un local'),
            ('local.actualizar', 'Permite actualizar un local'),
            ('local.detalle', 'Permite ver el detalle de un local')
        )

    def __str__(self) -> str:
        return self.local + " " + self.direccion

class AcuerdoComercial(models.Model):
    cliente = models.ForeignKey(Cliente, verbose_name="Cliente", on_delete=models.CASCADE)
    rama = models.ForeignKey(Rama, verbose_name="Rama", on_delete=models.CASCADE)
    porcentaje = models.FloatField(verbose_name="Porcentaje")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'Acuerdo Comercial'
        verbose_name_plural = 'Acuerdos Comerciales'
        ordering = ['-created']
        default_permissions = ()
        unique_together = [['cliente', 'rama']]

# Crear casa matriz para los clientes

@receiver(models.signals.post_save, sender=Cliente)
def crear_casa_matriz(sender, instance, created, **kwargs):
    if created:
        instance.clientelocal_set.create(local='Casa Matriz', direccion=instance.direccion, telefono=instance.telefono, contacto=instance.contacto)
