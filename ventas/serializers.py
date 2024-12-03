from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from nucleo.serializers import ProductoSerializerCliente, ProductoSerializer
from .models import ListaPrecio, ListaPrecioProducto, OrdenDeVenta, OrdenDeVentaProducto

# SERIALIZERS LISTAS DE PRECIOS


class ListaPrecioProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializerCliente()

    class Meta:
        model = ListaPrecioProducto
        fields = ('precio', 'producto')


class ListaPrecioSerializer(serializers.ModelSerializer):
    productos = ListaPrecioProductoSerializer(read_only=True, many=True, source="listaprecioproducto_set")
    total_productos = SerializerMethodField(read_only=True)

    class Meta:
        model = ListaPrecio
        fields = ('id', 'nombre', 'productos', 'total_productos')

    def get_total_productos(self, instance):
        return instance.listaprecioproducto_set.count()

# SERIALIZER ORDEN DE VENTA PRODUCTO


class OrdenDeVentaProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = OrdenDeVentaProducto
        fields = '__all__'

# SERIALIZERS ORDEN DE VENTA


class OrdenDeVentaSerializer(serializers.ModelSerializer):
    total_productos = serializers.SerializerMethodField(read_only=True)
    productos = OrdenDeVentaProductoSerializer(source='ordendeventaproducto_set', many=True)
    total = serializers.SerializerMethodField(read_only=True)
    facturas = serializers.SerializerMethodField(read_only=True)
    boleta = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrdenDeVenta
        depth = 1
        fields = '__all__'
        datatables_always_serialize = ('n_orden_cliente', 'facturas', 'boleta')

    def get_total(self, instance):
        return {'neto': instance.totalNeto(), 'iva': instance.iva(), 'total': instance.total(),'envio':instance.envio,'descuento':instance.totalDescuento()}

    def get_boleta(self, instance):
        facturas = self.get_facturas(instance)
        boleta = False
        for f in facturas:
            if 'BE' in f:
                boleta = True
        return boleta

    def get_facturas(self, instance):
        return instance.get_facturas()

    def get_total_productos(self, instance):
        return instance.ordendeventaproducto_set.count()
