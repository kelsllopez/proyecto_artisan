from django.contrib.auth.models import User
from inventario.serializers import BodegaSerializer
from rest_framework import serializers
from .models import CajaLote, EstadoLote, InsumoProcesoProduccion, PautaProduccion,IngredienteProduccion,InstruccionProduccion,Lote
from pauta.serializers import PautaElaboracionSerializer
from nucleo.serializers import LineaSerializer
from datetime import datetime, timedelta

class PautaProduccionSerializer(serializers.ModelSerializer):
    pauta_nombre = serializers.CharField(read_only=True,source='plantilla_pauta.nombre',allow_blank=True,default="Sin Pauta")
    class Meta:
        model = PautaProduccion
        fields = '__all__'
        datatables_always_serialize = ('estado',)


class IngredienteProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredienteProduccion
        fields = ('id','cantidad','plantilla_ingrediente')

class InsumoProcesoProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoProcesoProduccion
        depth=1
        fields = ('id','cantidad','plantilla_ip')

class InstruccionProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstruccionProduccion
        fields = '__all__'

class EstadoLoteSerializer(serializers.ModelSerializer):
    lugar = BodegaSerializer()
    encargado = serializers.SerializerMethodField()
    class Meta:
        model = EstadoLote
        fields = '__all__'
    
    def get_encargado(self,instance):
        try:
            encargado = instance.encargado
            if encargado:
                nombre = encargado.first_name + " " + encargado.last_name
                return nombre
            else:
                return "Sin Encargado"
        except User.DoesNotExist:
            return "Sin Encargado"


class LoteSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    proximo_estado = serializers.SerializerMethodField()
    cantidad_actual = serializers.SerializerMethodField(read_only=True)
    pauta_produccion = serializers.SerializerMethodField(read_only=True)
    linea = LineaSerializer(read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'
        datatables_always_serialize = ('cantidad_actual', 'linea', 'producto', 'proximo_estado')
        depth = 1

    def get_estado(self, instance):
        estado = instance.estadolote_set.last()
        serializer = EstadoLoteSerializer(estado, read_only=True, many=False)
        return serializer.data

    def get_proximo_estado(self, instance):
        return instance.proximo_estado().nombre if instance.proximo_estado() is not None else 'No'

    def get_cantidad_actual(self, instance):
        return instance.cantidadactual()

    def get_pauta_produccion(self, instance):
        try:
            pauta = instance.pauta_produccion
            serializer = PautaProduccionSerializer(pauta, many=False)
            return serializer.data
        except PautaProduccion.DoesNotExist:
            return {"nombre": "Nulo", "id": 0}



class PautaProduccionDetalleSerializer(serializers.ModelSerializer):
    plantilla_pauta = PautaElaboracionSerializer()
    ingredientes_produccion = IngredienteProduccionSerializer(source='ingredienteproduccion_set',many=True)
    instruccion_produccion = InstruccionProduccionSerializer(source='instruccionproduccion_set',many=True)
    insumoproceso_produccion = InsumoProcesoProduccionSerializer(source='insumoprocesoproduccion_set',many=True)
    lotes = LoteSerializer(source="lote_set",many=True)
    class Meta:
        model = PautaProduccion
        fields = '__all__'
    #pasamos el contexto a la plantilla_pauta
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plantilla_pauta'].context.update(self.context)

class LoteDetalleSerializer(serializers.ModelSerializer):
    estados  = EstadoLoteSerializer(many=True,source="estadolote_set")
    cantidad_actual = serializers.SerializerMethodField(read_only=True)
    pauta_produccion = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Lote
        fields = '__all__'
        datatables_always_serialize = ('cantidad_actual',)
        depth = 1
    
    def get_cantidad_actual(self,instance):
        return instance.cantidadactual()
    def get_pauta_produccion(self,instance):
        try:
            pauta = instance.pauta_produccion
            serializer = PautaProduccionSerializer(pauta,many=False)
            return serializer.data
        except PautaProduccion.DoesNotExist:
            return {"nombre":"Nulo","id":0}

class LoteMaduracionSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField(read_only=True)
    fechas  = serializers.SerializerMethodField(read_only=True)


    def get_id(self,instance):
        return 'Hola'
    
    def get_fechas(self,instance):
        dt = datetime.now()
        start = dt - timedelta(days=dt.weekday())
        print(instance)
        lista = [-28,-21,-14,-7,0,7,14,21,28]
        return [start + timedelta(days=i) for i in lista]

class LoteSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = Lote
        fields = ('id','producto')
        depth = 1

class CajaLoteSerializer(serializers.ModelSerializer):
    lote = LoteSerializerSimple()
    class Meta:
        model = CajaLote
        fields = '__all__'