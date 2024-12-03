from django.db import models
from inventario.models import Bodega,Insumo
from django.contrib.auth.models import User
from .tasks import enviar_email_remitente


class Solicitud(models.Model):
    lugar_o = models.ForeignKey(Bodega, on_delete=models.CASCADE, verbose_name="Lugar de Origen")
    solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Persona que solicita",null=True)
    estado = models.CharField(max_length=120, verbose_name="Estado solicitud", default="No Completada", choices=(('No Completada', 'No Completada'), ('Completada', 'Completada')))
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = 'solicitudes'
        ordering = ['-created']
        default_permissions = ()
        permissions = (
            ('listar', 'Puede listar las solicitudes'),
            ('crear', 'Puede crear una solicitud'),
            ('eliminar', 'Permite eliminar una solicitud'),
            ('actualizar', 'Permite actualizar una solicitud'),
            ('detalle', 'Permite ver el detalle de la solicitud')
        )
    
    def notificar(self):
        encargados = self.solicitudencargados_set.all()
        insumos = self.solicitudinsumos_set.all()
        for e in encargados:
            html_message = f"Hola {e.encargado.first_name},<br>{self.solicitante.first_name} {self.solicitante.last_name} ha solicitado los siguientes insumos para la planta de {self.lugar_o.nombre}<br><ul>"
            message = f"Hola {e.encargado.first_name},\n {self.solicitante.first_name} {self.solicitante.last_name} ha solicitado los siguientes insumos para la planta de {self.lugar_o.nombre}\n"
            for i in insumos:
                html_message+=f'<li>{i.insumo.nombre} ({i.insumo.unidad}) - {i.cantidad} - Comentario: {i.comentario}</li>'
                message+=f'{i.insumo.nombre} ({i.insumo.unidad}) - {i.cantidad} - Comentario: {i.comentario}\n'
            html_message+='</ul>'
            subject = f"Solicitud Insumos para planta {self.lugar_o.nombre}"
            enviar_email_remitente.delay(subject,html_message,message,e.encargado.email)
        return True


class SolicitudInsumos(models.Model):
    solicitud = models.ForeignKey(Solicitud, verbose_name="Solicitud", on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, verbose_name="Insumo a solicitar", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name="Cantidad a solicitar")
    comentario = models.CharField(verbose_name="Comentario",max_length=255,default="")

    class Meta:
        verbose_name = 'solicitud insumo'
        verbose_name_plural = 'solicitud insumos'
        default_permissions = ()


class SolicitudEncargados(models.Model):
    solicitud = models.ForeignKey(Solicitud, verbose_name="Solicitud", on_delete=models.CASCADE)
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Persona que sera notificada",)

    class Meta:
        verbose_name = 'solicitud encargado'
        unique_together = ['solicitud', 'encargado']
        verbose_name_plural = 'solicitud encargado'
        default_permissions = ()
