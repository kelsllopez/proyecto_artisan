from rest_framework import serializers
import logging

from produccion.models import PautaProduccion
from .models import (Etapa, Ingrediente, Instruccion, InstruccionColumna, InsumoProceso, Pauta, Columna, PautaProducto)  
from perfil.models import Perfil
from inventario.models import InventarioInsumo,Bodega
from nucleo.models import Rama
from nucleo.serializers import ProductoSerializer
logger = logging.getLogger(__name__)

class PautaSerializer(serializers.ModelSerializer):
    rama_nombre = serializers.CharField(read_only=True,source='rama.nombre',allow_blank=True,default="Sin Área")
    class Meta:
        model = Pauta
        fields = '__all__'
        datatables_always_serialize = ('rama_nombre',)

class ColumnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columna
        fields = '__all__'

class InstruccionColumnaSerializer(serializers.ModelSerializer):
    columna = ColumnaSerializer()
    class Meta:
        model = InstruccionColumna
        fields = '__all__'

#PARA LA PAUTA DE ELABORACIÓN


class IngredienteSerializer(serializers.ModelSerializer):
    inventario = serializers.SerializerMethodField()

    class Meta:
        model = Ingrediente
        depth = 1
        fields = ('id', 'cantidad', 'unidad', 'insumo', 'inventario', 'opcional', 'original')

    def get_inventario(self, instance):
        # Obtener el perfil del usuario
        user = self.context['request'].user
        perfil = Perfil.objects.filter(usuario=user).first()
        
        if not perfil or not perfil.lugar:
            logger.warning(f"Perfil no encontrado o lugar no asignado para el usuario: {user.username}")
            return 0
        
        lugar = perfil.lugar.nombre  # Asumiendo que 'lugar' es una ForeignKey a Bodega

        # Buscar la bodega por nombre
        bodega = Bodega.objects.filter(nombre__iexact=lugar).first()
        if not bodega:
            logger.warning(f"Bodega no encontrada para nombre: {lugar}")
            return 0

        # Obtener o crear el inventario
        try:
            inventario, created = InventarioInsumo.objects.get_or_create(
                bodega=bodega,
                insumo=instance.insumo,
                defaults={'cantidad': 0}
            )
            return inventario.cantidad
        except Exception as e:
            logger.error(f"Error al obtener o crear inventario: {e}")
            return 0

class InsumoProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsumoProceso
        depth = 1
        fields = ('id','insumo')


class InstruccionSerializer(serializers.ModelSerializer):
    columnas = InstruccionColumnaSerializer(source='instruccioncolumna_set',many=True)
    maximop = serializers.SerializerMethodField()
    class Meta:
        model = Instruccion
        fields = ('id', 'orden', 'descripcion', 'columnas', 'maximop')
    def get_maximop(self, instance):
        # obtenemos los parametros
        return len(instance.instruccioncolumna_set.all())
    
class EtapaSerializer(serializers.ModelSerializer):
    instrucciones = InstruccionSerializer(source="instruccion_set",many=True)
    class Meta:
        model = Etapa
        depth = 1
        fields = ('id','orden','nombre','instrucciones')

class RamaSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True)
    class Meta:
        model = Rama
        fields = ('id','nombre','productos')

class PautaProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model = PautaProducto
        fields = '__all__'

class PautaElaboracionSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(source='ingrediente_set', many=True)
    insumosproceso = InsumoProcesoSerializer(source='insumoproceso_set', many=True)
    etapas = EtapaSerializer(source="etapa_set", many=True)
    productos = PautaProductoSerializer(source="pautaproducto_set", many=True)
    lider = serializers.SerializerMethodField()
    rendimiento = serializers.SerializerMethodField()

    class Meta:
        model = Pauta
        fields = ('id', 'nombre', 'rendimiento', 'productos', 'ingredientes', 'etapas', 'insumosproceso','lider')
        depth = 1

    def get_rendimiento(self, instance):
        # obtener el promedio de rendimiento
        lugar = self.context.get('request').user.perfil.lugar
        # obtenemos las pautas de elaboración que se han desarrollado en ese lugar
        pautas = PautaProduccion.objects.filter(lugar=lugar, plantilla_pauta=instance).all()
        promedio = 0
        masas = 0
        for p in pautas:
            if p.rendimiento and p.rendimiento > 0:
                promedio += p.rendimiento * (p.masa_final if p.masa_final != None else 0)
                masas += p.masa_final if p.masa_final != None else 0
        if promedio > 0:
            return promedio / masas
        return instance.rendimiento

    def get_lider(self, instance):
        #obtenemos los ingredientes
        lider = instance.ingrediente_set.filter(lider=True).first()
        if lider:
            return lider.cantidad
        else:
            return 100



    # pasamos el contexto a los ingredientes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredientes'].context.update(self.context)

