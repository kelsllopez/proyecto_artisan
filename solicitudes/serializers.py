from rest_framework import serializers
from nucleo.serializers import InsumoSerializer
from inventario.serializers import BodegaSerializer
from .models import Solicitud, SolicitudEncargados, SolicitudInsumos


# Serializer para los insumos
class SolicitudInsumoSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer()

    class Meta:
        model = SolicitudInsumos
        fields = ('id', 'insumo', 'cantidad', 'comentario')


class SolicitudSerializer(serializers.ModelSerializer):
    lugar_o = BodegaSerializer()
    insumos = SolicitudInsumoSerializer(many=True, source='solicitudinsumos_set')
    solicitante = serializers.SerializerMethodField()
    encargados = serializers.SerializerMethodField()

    class Meta:
        model = Solicitud
        fields = '__all__'

    def get_solicitante(self, instance):
        return {'nombre': f"{instance.solicitante.first_name} {instance.solicitante.last_name}"}

    def get_encargados(self, instance):
        lista = []
        for e in instance.solicitudencargados_set.all():
            lista.append(f"{e.encargado.first_name} {e.encargado.last_name}")
        return lista
