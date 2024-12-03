from rest_framework.fields import ChoiceField
from nucleo.serializers import InsumoOrdenSerializer
from .models import OrdenDeCompra, OrdenDeCompraInsumo
from rest_framework import serializers
from proveedores.serializers import ProveedorInsumosSerializer
from django.contrib.auth.models import User
from proveedores.serializers import ProveedorSerializer


class HistorialInsumoSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(read_only=True,source='insumo.insumo.nombre')
    proveedor_nombre = serializers.CharField(source="insumo.proveedor.empresa_nombre")
    cantidad = serializers.IntegerField()
    neto = serializers.FloatField()
    fecha = serializers.DateTimeField(read_only=True,source='orden.created')
    class Meta:
        model = OrdenDeCompraInsumo
        fields = ('insumo_nombre','proveedor_nombre','cantidad','neto','insumo','fecha')



class OrdenDeCompraInsumoSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(read_only=True,source='insumo.insumo.nombre')
    insumo_descriptor = serializers.CharField(read_only=True,source='insumo.nombre_insumo')
    formato = serializers.FloatField(read_only=True,source='insumo.formato')
    unidad = serializers.CharField(read_only=True,source='insumo.insumo.unidad')
    neto = serializers.FloatField(read_only=True)
    class Meta:
        model = OrdenDeCompraInsumo
        fields = '__all__'
    


class OrdenDeCompraSerializer(serializers.ModelSerializer):
    nombre_proveedor = serializers.CharField(read_only=True, source='proveedor.empresa_nombre')
    nombre_lugar = serializers.CharField(read_only=True, source='bodega.nombre')
    insumos = OrdenDeCompraInsumoSerializer(read_only=True,many=True,source='ordendecomprainsumo_set')
    solicita = serializers.SerializerMethodField()
    class Meta:
        model = OrdenDeCompra
        fields = '__all__'
        datatables_always_serialize = ('pagada',)
    
    def get_solicita(self,instance):
        registro = instance.registro_set.first()
        if registro:
            return f"{registro.empleado.first_name} {registro.empleado.last_name}"
        return "Sin Empleado"

