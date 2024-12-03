from rest_framework import serializers
from django.urls import reverse, reverse_lazy
from ordendecompra.models import OrdenDeCompraInsumo
from ventas.models import OrdenDeVentaProducto
from .models import Insumo, InsumoDirectoProducto, InsumoElaboracionProducto, Producto, Linea, Rama
from inventario.models import InventarioProducto, InventarioInsumo
from django.contrib.auth.models import User
from proveedores.models import ProveedorInsumo
from django.core.exceptions import ObjectDoesNotExist

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rama
        fields = '__all__'

class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('nombre', 'first_name', 'last_name', 'email', 'id',)

    def get_nombre(self, instance):
        return f"{instance.first_name} {instance.last_name}"

class ProveedorInsumoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(read_only=True, source="proveedor.empresa_nombre")
    class Meta:
        model = ProveedorInsumo
        fields = '__all__'

class InsumoOrdenSerializer(serializers.ModelSerializer):
    proveedores = ProveedorInsumoSerializer(read_only=True, many=True, source='proveedorinsumo_set')
    precio_oc = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Insumo
        fields = '__all__'

    def get_precio_oc(self, instance):
        request = self.context.get('request')
        cantidad = int(request.GET.get('cantidad', 1))

        if request.GET.get('precio') is not None:
            if instance.pip:
                lugar = request.user.perfil.lugar
                bodega = InventarioInsumo.objects.filter(bodega=lugar, insumo=instance).first()
                if bodega:
                    return round(bodega.valorizar() * cantidad, 3)
            else:
                try:
                    ordendecomprainsumo = OrdenDeCompraInsumo.objects.filter(insumo__insumo=instance).first()
                    if ordendecomprainsumo:
                        return round((ordendecomprainsumo.neto / ordendecomprainsumo.insumo.formato) * cantidad, 10)
                except Exception as ex:
                    print(f"Error al calcular el precio de la orden de compra: {ex}")
        return 0

class InsumoSerializer(serializers.ModelSerializer):
    inventario = serializers.SerializerMethodField(read_only=True)
    cantidad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Insumo
        fields = ('nombre', 'unidad', 'inventario', 'id', 'cantidad')

    def to_representation(self, instance):
        request = self.context.get('request', None)
        representation = super().to_representation(instance)

        lista = ['/api/pauta/detalle/', '/api/grupoproducto/']
        if not self.context.get('cantidad'):
            representation.pop('cantidad')

        if not any(palabra in request.get_full_path() for palabra in lista):
            representation.pop('inventario')
            representation['stock_critico'] = instance.stock_critico

        return representation

    def get_inventario(self, instance):
        try:
            request = self.context.get('request', None)
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                lugar = request.user.perfil.lugar
                inventario, created = InventarioInsumo.objects.get_or_create(
                    bodega=lugar,
                    insumo=instance,
                    defaults={'cantidad': 0}
                )
                return inventario.cantidad
            return 0
        except ObjectDoesNotExist as e:
            print(f"Error al obtener el inventario: {e}")
            return 0  # Valor por defecto
        except Exception as e:
            print(f"Error inesperado: {e}")
            return 0  # Valor por defecto

    def get_cantidad(self, instance):
        return self.context.get('cantidad', None)
    
    
class DescriptorSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(source='insumo.nombre')
    
    class Meta:
        model = InsumoDirectoProducto
        fields = '__all__'

class InsumoElaboracionProductoSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    
    class Meta:
        model = InsumoElaboracionProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    rama_nombre = serializers.SerializerMethodField()
    rama = AreaSerializer(source='linea.rama', read_only=True)
    linea = LineaSerializer()
    descriptores = DescriptorSerializer(read_only=True, many=True, source='insumodirectoproducto_set')
    insumose = InsumoElaboracionProductoSerializer(read_only=True, many=True, source="insumoelaboracionproducto_set")

    class Meta:
        model = Producto
        fields = '__all__'

    def get_rama_nombre(self, instance):
        return instance.linea.rama.nombre if instance.linea else "Sin Rama"

class ProductoSerializerCliente(serializers.ModelSerializer):
    inventario = serializers.SerializerMethodField(read_only=True)
    rama = AreaSerializer(source='linea.rama', read_only=True)

    class Meta:
        model = Producto
        fields = ('nombre', 'codigo', 'presentacion', 'unidad', 'inventario', 'id', 'rama')

    def to_representation(self, instance):
        request = self.context.get('request', None)
        representation = super().to_representation(instance)

        lista = ['/api/cliente/avanzado/', '?id=true']
        if not any(palabra in request.get_full_path() for palabra in lista):
            representation.pop('inventario')

        return representation

    def get_inventario(self, instance):
        lugar = self.context.get('request').user.perfil.lugar
        oc = self.context.get('request').GET.get('oc')
        try:
            if oc is not None:
                pendientes = OrdenDeVentaProducto.objects.filter(orden__pk__lte=int(oc), orden__lugar=lugar, producto=instance, orden__estado='Pendiente').exclude(orden__pk=int(oc)).all()
            else:
                pendientes = OrdenDeVentaProducto.objects.filter(orden__lugar=lugar, producto=instance, orden__estado='Pendiente').all()
            inventario, created = InventarioProducto.objects.get_or_create(bodega=lugar, producto=instance, defaults={'cantidad': 0})

            for p in pendientes:
                inventario.cantidad -= p.cantidad
            return inventario.cantidad
        except Exception as e:
            print(f"Error al obtener el inventario: {e}")
            return 0  # O un valor predeterminado

class RamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = '__all__'
