from rest_framework import serializers
from .models import Estado, ConjuntoEstado, EstadoConjunto
import re

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class EstadoConjuntoSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = EstadoConjunto
        fields = ('estado','pos')

class ConjuntoEstadoSerializer(serializers.ModelSerializer):
    estados = EstadoConjuntoSerializer(source="estadoconjunto_set",many=True)

    class Meta:
        model = ConjuntoEstado
        fields = '__all__'
    
    # metodo to_representation para
    def to_representation(self, instance):
        # obtenemos el contexto
        self._context["request"] = self.context["request"]
        # obtenemos la representation actual
        representation = super().to_representation(instance)
        # si es que estamos en detalle
        patron = '\/\d*\/'
        check = len(re.findall(patron,self.context.get('request').get_full_path()))
        if check <= 0:
            representation.pop('estados')
        return representation
