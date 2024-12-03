from django import forms
from django.forms import widgets
from nucleo.models import Insumo
from .models import Proveedor,ProveedorInsumo

class ProveedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'empresa_rut': forms.TextInput(attrs={'onkeyup':'vue.formatearRut(event)','class':'form-control'}),
            'empresa_comuna': forms.Select(),
            'empresa_region': forms.Select(attrs={'onChange':'vue.buscarComuna(event)'})
        }
class ProveedorInsumoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        proveedor = kwargs.pop('proveedor') if 'proveedor' in kwargs else None
        insumo = kwargs.pop('insumo') if 'insumo' in kwargs else None
        super(ProveedorInsumoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['proveedor','insumo']:
                field.widget.attrs['class'] = ''
            if field_name == 'insumo':
                field.widget.attrs['onchange'] = 'vue.actualizarUnidad()'
        self.fields['proveedor'].initial = proveedor if proveedor else None
        self.fields['insumo'].initial = insumo if insumo else None


    class Meta:
        model = ProveedorInsumo
        fields = ['proveedor','insumo','nombre_insumo','formato','precio','lead']
        help_texts = {
            'proveedor': ('Este es el proveedor que vendera el insumo.'),
            'insumo': ('El insumo que el proveedor suministrara a la empresa.'),
            'nombre_insumo': ('Este es el nombre que maneja el proveedor para su insumo. Ej: Maltodextrina 14'),
            'formato': ('Esta es el formato con el cual el proveedor vende el insumo. Ej: Azucar saco 25 kilos, crema 1 litro'),
            'precio': ('Es el precio neto por formato. Ej: Cuanto cuesta el saco de 25 kilos.'),
            'lead': ('Es el tiempo que el proveedor se demora en entregar los insumos, medido en días')
        }
        labels = {
            'lead': ('Lead Time (Días)')
        }

class ProveedorInsumoFormUpdate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProveedorInsumoFormUpdate, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['proveedor'].disabled = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['proveedor','insumo']:
                field.widget.attrs['class'] = ''
            if field_name == 'insumo':
                field.widget.attrs['onchange'] = 'vue.actualizarUnidad()'

    class Meta:
        model = ProveedorInsumo
        fields = ['proveedor','insumo','nombre_insumo','formato','precio','lead']
        help_texts = {
            'proveedor': ('Este es el proveedor que vendera el insumo.'),
            'insumo': ('El insumo que el proveedor suministrara a la empresa.'),
            'nombre_insumo': ('Este es el nombre que maneja el proveedor para su insumo. Ej: Maltodextrina 14'),
            'formato': ('Esta es el formato con el cual el proveedor vende el insumo. Ej: Azucar saco 25 kilos, crema 1 litro'),
            'precio': ('Es el precio por formato. Ej: Cuanto cuesta el saco de 25 kilos.'),
            'lead': ('Es el tiempo que el proveedor se demora en entregar los insumos, medido en días')
        }
        labels = {
            'lead': ('Lead Time (Días)')
        }
