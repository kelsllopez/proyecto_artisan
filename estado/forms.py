from django import forms
from django.forms import widgets

from nucleo.models import Insumo
from .models import ConjuntoEstado, Estado, Producto


class ConjuntoEstadoForm(forms.ModelForm):

    class Meta:
        model = ConjuntoEstado
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }


class EstadoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EstadoForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance') is not None:
            self.fields['insumos'].initial = [c.insumo.pk for c in kwargs.get('instance').estadoinsumo_set.all()]
            self.fields['productos'].initial = [c.producto.pk for c in kwargs.get('instance').estadoproducto_set.all()]

    insumos = forms.ModelMultipleChoiceField(required=False, queryset=Insumo.objects, help_text='Los insumos que se obtendran a partir de este estado.')
    productos = forms.ModelMultipleChoiceField(required=False, queryset=Producto.objects, help_text='Los productos que se obtendran a partir de este estado.')

    class Meta:
        model = Estado
        fields = ('nombre', 'peso', 'uc', 'uff', 'unc', 'insumos', 'productos')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'unc': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        help_texts = {
            'nombre': 'El nombre que tendra este estado.',
            'peso': 'Si en este estado se registrara el peso en kilogramos.',
            'uc': 'Si en este estado se podra registrar unidades para calidad',
            'uff': 'Si en este estado se podra registrar unidades fuera de formato',
            'unc': 'Si en este estado se podra registrar unidades no consumibles',
        }
