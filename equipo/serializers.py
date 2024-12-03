from rest_framework import serializers
from .models import AreaEquipo, Equipo

class AreaSerializer(serializers.ModelSerializer):
    lugar_nombre = serializers.SerializerMethodField()
    class Meta:
        model = AreaEquipo
        fields = '__all__'

    def get_lugar_nombre(self,instance):
        return (instance.lugar.nombre if instance.lugar else 'Sin Lugar')

class EquipoSerializer(serializers.ModelSerializer):
    area_nombre = serializers.SerializerMethodField()
    area = AreaSerializer()
    class Meta:
        model = Equipo
        fields = ('id','area','nombre','area_nombre')
    
    def get_area_nombre(self,instance):
        return (instance.area.nombre if instance.area else 'Sin Área')

