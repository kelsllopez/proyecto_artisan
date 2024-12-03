from rest_framework import serializers
from equipo.serializers import EquipoSerializer
from nucleo.serializers import UserSerializer
from .models import EquipoUtensilioLimpieza, GrupoEquipos, RegistroLimpiezaEquipo, UtensilioLimpieza,RegistroLimpiezaEquipoHistorial

class HistorialRegistroEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroLimpiezaEquipoHistorial
        fields = ('__all__')

class EquipoUtensilioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(read_only=True,source="equipo.nombre")
    lugar = serializers.SerializerMethodField()
    class Meta:
        model = EquipoUtensilioLimpieza
        fields = ('equipo','nombre','lugar','id')
    
    def get_lugar(self,instance):
        return (instance.equipo.area.lugar.nombre if instance.equipo.area else 'Sin Lugar')

class UtensilioLimpiezaEquipoSerializer(serializers.ModelSerializer):
    equipos = EquipoUtensilioSerializer(read_only=True,many=True,source='equipoutensiliolimpieza_set')
    class Meta:
        model = UtensilioLimpieza
        fields = '__all__'

class UtensilioLimpiezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtensilioLimpieza
        fields = ('nombre','categoria')

class EquipoRegistroLimpiezaSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer(read_only=True)
    utensilios = UtensilioLimpiezaSerializer(read_only=True,many=True)
    encargado = UserSerializer()
    revisado = UserSerializer()
    historial = HistorialRegistroEquipoSerializer(source="registrolimpiezaequipohistorial_set",many=True)
    class Meta:
        model = RegistroLimpiezaEquipo
        fields = '__all__'
        datatables_always_serialize = ('encargado.last_name',)


class GrupoEquiposSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrupoEquipos
        fields = '__all__'
