from django.shortcuts import render
from django.views.generic import TemplateView
from ordendecompra.models import OrdenDeCompraInsumo
# Create your views here.


class EstadisticasBodegaView(TemplateView):
    template_name = 'estadisticas/simple.html'
