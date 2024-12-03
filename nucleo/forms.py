from django import forms
from django.forms import widgets
import math
import numpy as np
from .models import Insumo, Producto, Rama, InsumoElaboracionProducto
from django.core.exceptions import ValidationError


class InsumoForm(forms.ModelForm):

    class Meta:
        model = Insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-select'}),
            'stock_critico': forms.NumberInput(attrs={'class': 'form-control'})

        }
        help_texts = {
            'nombre': ('Este es el nombre <b>génerico</b> del insumo, el cual se controlara en inventario, por ejemplo: Maltodextrina.'),
            'unidad': ('Esta es la unidad de medida en la cual se medira el insumo a <b>nivel de inventario</b>, por ejemplo la Leche se mide en Litros.'),
            'stock_critico': ('Este es el stock minimo que debe haber en el inventario, bajo este numero se <b>leventaran alertas</b>.')
        }


class RamaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RamaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Rama
        fields = '__all__'

class ProductoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        selects = ['linea', 'unidad']
        rama = kwargs.pop('linea') if 'linea' in kwargs else None
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in selects:
                field.widget.attrs['class'] = ''
            else:
                field.widget.attrs['class'] = 'form-control'
        self.fields['linea'].initial = rama if rama else None

    class Meta:
        model = Producto
        fields = ['nombre', 'linea', 'descripcion', 'presentacion', 'unidad', 'duracion', 'unidades', 'dun14', 'stock_critico', 'sap', 'conjunto',  'maduracion',]

    def clean_dun14(self):
        data = self.cleaned_data['dun14']
        largo = len(data)
        if largo == 0:
            return data
        # verificamos que el largo sea 12 o 13
        if ((largo > 14) or (largo < 13)):
            raise ValidationError("El código DUN14 se compone de 13 dígitos más el dígito verificador.")
        else:
            # verificamos el digito verificador
            redondeo = 0
            suma = 0
            pares = 0
            impares = 0
            try:
                if largo == 14:
                    pares = [int(data[digito]) for digito in range(len(data)) if (digito+1) % 2 == 0][:-1]
                else:
                    pares = [int(data[digito]) for digito in range(len(data)) if (digito+1) % 2 == 0]
                impares = [int(data[digito]) for digito in range(len(data)) if (digito+1) % 2 != 0]
                sumapares = np.sum(pares)
                sumaimpares = np.sum(impares) * 3
                suma = sumapares + sumaimpares
                redondeo = int(math.ceil(suma / 10.0)) * 10
            except Exception as ex:
                raise ValidationError("El código DUN14 solo puede contener números.")
            digito = redondeo - suma
            if largo == 14:
                if digito != int(data[-1]):
                    raise ValidationError("El dígito verificador ingresado no es el correcto. debería ser ({})".format(digito))
                else:
                    return data
            else:
                data += str(digito)
                return data