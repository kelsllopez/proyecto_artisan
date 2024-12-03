from django import forms
from .models import *


class EstadoLoteCreateForm(forms.ModelForm):

    class Meta:
        model = EstadoLote
        fields = ('nombre', 'peso', 'unidadesNC', 'unidadesFF', 'unidadesC', 'observacion')
        labels = {
            "nombre": "Próximo Estado",
        }

class PautaProduccionCreateForm(forms.ModelForm):
    class Meta:
        model = PautaProduccion
        fields = ('plantilla_pauta', 'fecha', 'cantidad', 'masa_final')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'masa_final': forms.TextInput(attrs={'class': 'form-control'}),
            'plantilla_pauta': forms.Select(attrs={'class': '', 'onchange': 'vue.seleccionarPauta(event)'}),
        }

class PautaProduccionUpdateForm(forms.ModelForm):
    class Meta:
        model = PautaProduccion
        fields = ('fecha', 'cantidad', 'masa_final')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}),
            'masa_final': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CalidadProduccionForm(forms.ModelForm):
    class Meta:
        model = CalidadProduccion
        fields = [
            'filtro_instalado',
            'filtro_integrado',
            'inicio_envasado',
            'fin_envasado',
            'unidades_botellas_lt',
            'unidades_360gr',
            'unidades_150gr',
            'merma_kg',
            'ph',
            'textura',
            'sabor',
            'color',
            'olor',
            'aspecto',
            'elaboracion',
            'envasado',
            'verificacion',
            'observaciones',
            'estado_aprobacion',  # Asegúrate de incluirlo aquí
        ]
