from django import forms
from .models import Cliente, ClienteLocal, AcuerdoComercial

# Formulario de creación de cliente


class ClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        selects = ['pago']
        for field_name, field in self.fields.items():
            if field_name in selects:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'comuna': forms.Select(attrs={'class':'form-select'}),
            'rut': forms.TextInput(attrs={'class':'form-control','onkeyup':'vue.formatearRut(event)'}),
            'region': forms.Select(attrs={'class':'form-select','onChange': 'vue.buscarComuna(event)'})
        }

# Formulario de creación de local


class ClienteLocalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente') if 'cliente' in kwargs else None
        super(ClienteLocalForm, self).__init__(*args, **kwargs)
        selects = ['comuna', 'region', 'cliente']
        for field_name, field in self.fields.items():
            if field_name in selects:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        if cliente:
            self.fields['cliente'].initial = cliente

    class Meta:
        model = ClienteLocal
        fields = '__all__'
        widgets = {
            'comuna': forms.Select(),
            'region': forms.Select(attrs={'onChange': 'vue.buscarComuna(event)'})
        }

# Formulario de creación de acuerdos


class ClienteAcuerdoForm(forms.ModelForm):

    class Meta:
        model = AcuerdoComercial
        fields = ('cliente', )
