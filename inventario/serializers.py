from .models import Bodega, HistorialBodega, InsumoBulto, InventarioInsumo, InventarioProducto
from rest_framework import serializers
from nucleo.serializers import InsumoSerializer




class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(read_only=True,source="insumo.nombre")
    stock_critico = serializers.FloatField(read_only=True,source="insumo.stock_critico")
    unidad = serializers.CharField(read_only=True,source="insumo.unidad")
    
    class Meta:
        model = InventarioInsumo
        fields = '__all__'
        datatables_always_serialize = ('stock_critico','estado',)
    
    def get_estado(self, obj):
        stock_critico = obj.insumo.stock_critico
        cantidad = obj.cantidad
        if cantidad <= stock_critico:
            return 'Critico'
        else:
            return 'Ok'

class InventarioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioProducto
        fields = '__all__'
        #datatables_always_serialize = ('stock_critico','estado',)

class InsumoBultoSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    class Meta:
        model = InsumoBulto
        fields = '__all__'

class HistorialBodegaSerializer(serializers.ModelSerializer):
    bodega = BodegaSerializer()
    class Meta:
        model = HistorialBodega
        fields = '__all__'