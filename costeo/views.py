from django.db.models.query_utils import Q
from django.shortcuts import render
from ventas.models import OrdenDeVenta
from inventario.models import Bodega
from nucleo.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from nucleo.models import Producto
import datetime
from django.views.generic import TemplateView, CreateView, View, DetailView, ListView

@method_decorator(login_required, 'dispatch')
class CosteoProductoListView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'costeo.listar'
    template_name = 'costeo/list.html'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para el costeo'

    def get_context_data(self, **kwargs):
        context = {}
        context['productos'] = Producto.objects.all()
        context.update(kwargs)
        return context


@method_decorator(login_required, 'dispatch')
class MargenDetailView(ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'costeo.listar'
    template_name = 'costeo/margen.html'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para ver el margen'

    def get_context_data(self, **kwargs):
        context = {}
        # obtenemos las ventas
        ventas = OrdenDeVenta.objects
        fecha = self.request.GET.get('fecha', None)
        ubicacion = self.request.GET.get('ubicacion', '0')
        fechasf = []
        if fecha is None or fecha == "":
            fechasf = [datetime.datetime.now().replace(day=1, month=1), datetime.datetime.now().replace(day=31, month=12)]
        else:
            fechas = fecha.split(' a ')
            if len(fechas) > 1:
                fechai = [int(x) for x in fechas[0].split('-')]
                fechai = datetime.datetime(fechai[2], fechai[1], fechai[0])
                fechasf.append(fechai)
                fechaf = [int(x) for x in fechas[1].split('-')]
                fechaf = datetime.datetime(fechaf[2], fechaf[1], fechaf[0])
                fechasf.append(fechaf)
                ventas = ventas.filter(fecha__gte=fechai).filter(fecha__lte=fechaf)
            elif (len(fechas) == 1):
                fechai = [int(x) for x in fechas[0].split('-')]
                fechai = datetime.datetime(fechai[2], fechai[1], fechai[0])
                fechasf.append(fechai)
                ventas = ventas.filter(fecha__gte=fechai)

        if len(fechasf) == 1:
            fechasf.append(datetime.datetime.now().replace(day=31, month=12))
        ventas = ventas.order_by("-fecha").all()
        # clasificamos las ventas por mes
        ano_i = fechasf[0].year
        ano_f = fechasf[1].year
        diferencia = ano_f - ano_i
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        anos = {}
        if diferencia > 0:
            for i in range(diferencia):
                anos[fechasf[0].year+i] = {}
        else:
            anos[fechasf[1].year] = {}
        for ano in anos:
            for mes in meses:
                anos[ano][mes] = []
        # obtenemos los lotes de las ventas
        lotesingresados = []
        fechas = []
        margen = []
        for venta in ventas:
            cajas = venta.ordendeventacajalote_set.all()
            for c in cajas:
                # obtenemos el lote
                lote = c.caja.lote
                if ubicacion != "0":
                    try:
                        ubicacion = int(ubicacion)
                        context['ubicacion'] = int(ubicacion)
                        if lote.pauta_produccion.lugar.id == ubicacion:
                            if lote.estadolote_set.last().nombre == 'Cerrado' and lote.pk not in lotesingresados:
                                lotesingresados.append(lote.pk)
                                anos[venta.fecha.year][meses[venta.fecha.month-1]].append(lote.margen())
                    except Exception as ex:
                        print("Error" + ex)
                else:
                    if lote.estadolote_set.last().nombre == 'Cerrado' and lote.pk not in lotesingresados:
                        lotesingresados.append(lote.pk)
                        anos[venta.fecha.year][meses[venta.fecha.month-1]].append(lote.margen())
        for ano in anos:
            for mes in anos[ano]:
                if (meses.index(mes) >= (fechasf[0].month-1) and meses.index(mes) <= (fechasf[1].month-1)):
                    margen.append(sum(anos[ano][mes]))
                    fechas.append(f"{mes} {ano}")
        context['fechas'] = fechas
        context['margen'] = margen
        context['bodegas'] = Bodega.objects.all()
        context['fechasi'] = [f"{fecha.day:02d}-{fecha.month:02d}-{fecha.year}" for fecha in fechasf]
        context.update(kwargs)
        return context


@method_decorator(login_required, 'dispatch')
class CosteoProductoDetailView(ValidatePermissionRequiredMixin, DetailView):
    model = Producto
    permission_required = 'costeo.listar'
    template_name = 'costeo/detail.html'
    # donde retorna si no hay permiso y mensaje
    url_redirect = reverse_lazy('home')
    tipo_mensaje = 'error'
    mensaje = 'No tienes los permisos necesarios para el costeo'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            ubicacion = self.request.GET.get('ubicacion', '0')
            fecha = self.request.GET.get('fecha', None)
            context['lotes'] = self.object.lote_set.filter()
            fechasf = []
            if fecha is not None and fecha != "":
                fechas = fecha.split(' a ')
                if len(fechas) > 1:
                    fechai = [int(x) for x in fechas[0].split('-')]
                    fechai = datetime.datetime(fechai[2], fechai[1], fechai[0])
                    fechasf.append(fechai)
                    fechaf = [int(x) for x in fechas[1].split('-')]
                    fechaf = datetime.datetime(fechaf[2], fechaf[1], fechaf[0])
                    fechasf.append(fechaf)
                    context['lotes'] = context['lotes'].filter(pauta_produccion__fecha__gte=fechai).filter(pauta_produccion__fecha__lte=fechaf)
                elif (len(fechas) == 1):
                    fechai = [int(x) for x in fechas[0].split('-')]
                    fechai = datetime.datetime(fechai[2], fechai[1], fechai[0])
                    fechasf.append(fechai)
                    context['lotes'] = context['lotes'].filter(pauta_produccion__fecha__gte=fechai)
            if ubicacion != "0":
                try:
                    context['ubicacion'] = int(ubicacion)
                    context['lotes'] = context['lotes'].filter(pauta_produccion__lugar_id=int(ubicacion))
                except Exception as ex:
                    print(ex)
            if fecha is not None:
                context['lotes'] = context['lotes'].order_by('pk').all()
            else:
                context['lotes'] = context['lotes'].order_by('pk').all()[:30]
            context['fechas'] = [f"{fecha.day:02d}-{fecha.month:02d}-{fecha.year}" for fecha in fechasf]
            context['bodegas'] = Bodega.objects.all()
        context.update(kwargs)
        return context
