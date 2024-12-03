from rest_framework import serializers
from .models import Proveedor, ProveedorInsumo


class ProveedorOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('empresa_nombre',)


class ProveedorInsumosSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(read_only=True, source="insumo.nombre")
    unidad = serializers.CharField(read_only=True, source='insumo.unidad')
    insumo_id = serializers.IntegerField(read_only=True, source="insumo.id")
    precio = serializers.SerializerMethodField()

    class Meta:
        model = ProveedorInsumo
        fields = ('precio', 'id', 'insumo_nombre', 'insumo_id', 'nombre_insumo', 'formato', 'unidad', 'lead', 'mostrar')

    def get_precio(self, instance):
        return instance.getValor()


class ProveedorSerializer(serializers.ModelSerializer):
    insumos = ProveedorInsumosSerializer(read_only=True, many=True, source='proveedorinsumo_set')

    class Meta:
        model = Proveedor
        fields = '__all__'


class ProveedorListaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = '__all__'
