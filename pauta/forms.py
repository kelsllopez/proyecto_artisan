from django import forms
from .models import Columna, Pauta
from nucleo.models import Producto


class PautaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PautaForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance') is not None:
            self.fields['productos'].initial = [c.producto.pk for c in kwargs.get('instance').pautaproducto_set.all()]
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False, widget=forms.SelectMultiple(), label="Productos asociados a esta pauta.")

    class Meta:
        model = Pauta
        fields = ['nombre', 'tipo', 'productos', 'rendimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control','onchange':'vue.cambiarTipo(event)'}),
            'rendimiento': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ColumnaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColumnaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Columna
        fields = '__all__'

        help_texts = {
            'nombre': ('Esto es lo que se desea <strong>medir</strong> en las pautas de elaboración, por ejemplo: Temperatura, PH.'),
        }
