from django import forms
from django.contrib.auth.models import User
from .models import Bodega, HistorialBodega, InsumoBulto, InventarioInsumo, InventarioProducto

class BodegaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BodegaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if kwargs.get('instance') is not None:
            self.fields['supervisores'].initial = [c.supervisor.pk for c in kwargs.get('instance').supervisorbodega_set.all()]


    supervisores = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, widget=forms.SelectMultiple(), label="Supervisores de planta")

    class Meta:
        model = Bodega
        fields = '__all__'

class HistorialBodegaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(HistorialBodegaForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = HistorialBodega
        fields = '__all__'


class InventarioInsumoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InventarioInsumoUpdateForm, self).__init__(*args, **kwargs)
        bloqueados = ['bodega','insumo']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in bloqueados:
                field.disabled = True

    class Meta:
        model = InventarioInsumo
        fields = ['bodega','insumo','cantidad']


class InventarioProductoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InventarioProductoUpdateForm, self).__init__(*args, **kwargs)
        bloqueados = ['producto']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in bloqueados:
                field.disabled = True

    class Meta:
        model = InventarioProducto
        fields = ['producto']
        labels = {
            'cantidad': 'Cajas en inventario'
        }


class InsumoBultoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InsumoBultoUpdateForm, self).__init__(*args, **kwargs)
        bloqueados = ['numero']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in bloqueados:
                field.disabled = True

    class Meta:
        model = InsumoBulto
        fields = ['numero']

class BodegaHistorialForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BodegaHistorialForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.disabled = True

    class Meta:
        model = Bodega
        fields = ('nombre',)