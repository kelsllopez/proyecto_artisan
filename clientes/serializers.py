from ventas.serializers import ListaPrecioSerializer
from nucleo.serializers import ProductoSerializerCliente
from .models import AcuerdoComercial, Cliente, ClienteLocal
from rest_framework import serializers

# Serializer utilizado para obtener los locales


class ClienteLocalSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(read_only=True, source="cliente.nombre")

    class Meta:
        model = ClienteLocal
        fields = '__all__'

# Serializer utilizado para obtener los datos de los locales a partir del cliente


class ClienteLocalClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteLocal
        fields = ['id', 'local', 'telefono', 'region', 'comuna', 'direccion', 'contacto', 'email', 'celular']


# Serializer para acuerdos comerciales
class ClienteAcuerdoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcuerdoComercial
        depth = 1
        fields = ('rama', 'porcentaje')


# Serializer utilizado para obtener los datos del cliente
class ClienteSerializer(serializers.ModelSerializer):
    locales = ClienteLocalClienteSerializer(read_only=True, many=True, source='clientelocal_set')
    listap = ListaPrecioSerializer()
    acuerdos = ClienteAcuerdoSerializer(many=True, source='acuerdocomercial_set')

    class Meta:
        model = Cliente
        fields = '__all__'

# Serializer cliente sencillo
class ClienteSerializerSencillo(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = '__all__'
        
        
