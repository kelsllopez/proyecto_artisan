from inventario.models import InsumoBulto
from ventas.serializers import OrdenDeVentaSerializer
from nucleo.serializers import UserSerializer
import requests
from django.conf import settings
from inventario.serializers import BodegaSerializer, InsumoBultoSerializer
from rest_framework import serializers
from .models import Envio, InsumoEnvio, Pallet,LoteEnvio, Ruta, RutaOv
from produccion.serializers import LoteSerializer

class EnvioSerializer(serializers.ModelSerializer):
    estadot = serializers.SerializerMethodField()
    encargado_recepcion = serializers.SerializerMethodField()
    encargado_envio = serializers.SerializerMethodField()
    class Meta:
        model = Envio
        fields = '__all__'
        depth = 1
        datatables_always_serialize = ('estadot',)
    
    def get_estadot(self, instance):
        if instance.estado:
            return "Recepcionado"
        else:
            return "En Transito"
    
    def get_encargado_recepcion(self, instance):
        if instance.encargado_recepcion:
            return instance.encargado_recepcion.first_name + " " + instance.encargado_recepcion.last_name
        else:
            return None
        
    def get_encargado_envio(self, instance):
        if instance.encargado_envio:
            return instance.encargado_envio.first_name + " " + instance.encargado_envio.last_name
        else:
            return None
    
class LoteEnvioSerializer(serializers.ModelSerializer):
    lote = LoteSerializer(source="cajalote.lote")
    class Meta:
        model = LoteEnvio
        fields = '__all__'

class InsumoEnvioSerializer(serializers.ModelSerializer):
    insumobulto = InsumoBultoSerializer()
    class Meta:
        model = InsumoEnvio
        fields = '__all__'

class PalletSerializerDetalle(serializers.ModelSerializer):
    class Meta:
        model = Pallet
        fields = ('id','nombre')
    
class EnvioSerializerDetalle(serializers.ModelSerializer):
    pallets = PalletSerializerDetalle(source="pallet_set.all",many=True)
    lotes = LoteEnvioSerializer(source="loteenvio_set.all",many=True)
    insumos = InsumoEnvioSerializer(source="insumoenvio_set.all",many=True)
    resumen = serializers.SerializerMethodField()
    encargado_recepcion = serializers.SerializerMethodField()
    encargado_envio = serializers.SerializerMethodField()

    class Meta:
        model = Envio
        fields = '__all__'

    def get_resumen(self, instance):
        lotes = instance.loteenvio_set.all()
        insumos = instance.insumoenvio_set.all()
        final = {'lotes': [], 'insumos': []}
        for lote in lotes:
            diccionario = {'id': lote.cajalote.lote.producto.id, 'producto': lote.cajalote.lote.producto.nombre, 'unidad': lote.cajalote.lote.producto.unidad, 'presentacion': lote.cajalote.lote.producto.presentacion, 'cajas': 1, 'cantidad': lote.cajalote.cantidad}
            encontrado = False
            for f in final['lotes']:
                if f['id'] == lote.cajalote.lote.producto.id:
                    f['cantidad'] += lote.cajalote.cantidad
                    f['cajas']+=1
                    encontrado = True
            if encontrado == False:
                final['lotes'].append(diccionario)
        for insumo in insumos:
            encontrado = False
            diccionario = {'insumo': insumo.insumobulto.insumo.id,'bultos':1, 'nombre': insumo.insumobulto.insumo.nombre, 'unidad': insumo.insumobulto.insumo.unidad, 'cantidad': insumo.insumobulto.formato * insumo.insumobulto.cantidad}
            for i in final['insumos']:
                if i['insumo'] == insumo.insumobulto.insumo.id:
                    i['bultos']+=1
                    i['cantidad'] += insumo.insumobulto.formato * insumo.insumobulto.cantidad
                    encontrado = True
            if encontrado == False:
                final['insumos'].append(diccionario)    
        return final
    
    def get_encargado_recepcion(self, instance):
        if instance.encargado_recepcion:
            return instance.encargado_recepcion.first_name + " " + instance.encargado_recepcion.last_name
        else:
            return None
        
    def get_encargado_envio(self, instance):
        if instance.encargado_envio:
            return instance.encargado_envio.first_name + " " + instance.encargado_envio.last_name
        else:
            return None


class PalletSerializer(serializers.ModelSerializer):
    lugar = serializers.SerializerMethodField()

    class Meta:
        model = Pallet
        fields = '__all__'
        depth = 1

    def get_lugar(self, instance):
        if instance.lugar is None:
            return {"nombre": "Desconocido"}
        else:
            return BodegaSerializer(instance.lugar).data


class RutaOVSerializer(serializers.ModelSerializer):
    orden = OrdenDeVentaSerializer()
    class Meta:
        model = RutaOv
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    persona = UserSerializer()
    ordenes = RutaOVSerializer(source='rutaov_set', many=True)
    total_ordenes = serializers.SerializerMethodField()
    locacion = serializers.SerializerMethodField()


    class Meta:
        model = Ruta
        fields = '__all__'
    
    def to_representation(self, instance):
        extra = self.context.get('request').GET.get('extra')
        locacion = self.context.get('request').GET.get('locacion')
        representation = super().to_representation(instance)
        if extra != '1':
            representation.pop('ordenes')
            representation.pop('total_ordenes')
        if locacion != '1':
            representation.pop('locacion')
        return representation
    
    def get_locacion(self, instance):
        locacion = self.context.get('request').GET.get('locacion')
        if locacion == '1' and instance.patente != "":
            endpoint = 'https://drivetech.pro/api/v1/'
            token = settings.DRIVETECH_KEY
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Token {token}'
            }
            url = endpoint + f'get_vehicle_status/?plate={instance.patente}'
            r = requests.get(url, headers=headers)
            return r.json()
        return None

    def get_total_ordenes(self, instance):
        extra = self.context.get('request').GET.get('extra')
        if extra == '1':
            return instance.rutaov_set.count()
        return None

