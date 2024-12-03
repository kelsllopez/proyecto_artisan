from django import forms
from .models import Envio, Pallet, Ruta
from inventario.models import Bodega
from django.contrib.auth.models import User

class EnvioCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        lugar = kwargs.pop('lugar') if 'lugar' in kwargs else None
        super(EnvioCreateForm, self).__init__(*args, **kwargs)
        print(self.fields['lugar_d'].choices)
        self.fields["lugar_d"].queryset = Bodega.objects.exclude(pk=lugar.pk).all()
        

    class Meta:
        model = Envio
        fields = ('lugar_d','fecha_envio','medio_transporte','numero_documento')
        widgets = {
            'lugar_d': forms.Select(attrs={'class':'form-select'}),
            'medio_transporte': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_envio': forms.TextInput(attrs={'class':'form-control','id':'fechaenvio'}),
            'numero_documento': forms.TextInput(attrs={'class':'form-control'})
        }

class PalletCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PalletCreateForm, self).__init__(*args, **kwargs)
        self.fields["nombre"].initial = "Pallet {}".format(Pallet.objects.count())

    class Meta:
        model = Pallet
        fields = ('nombre','lugar')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'lugar': forms.Select(attrs={'class':'form-select'})
        }

class PalletUpdateForm(forms.ModelForm):

    class Meta:
        model = Pallet
        fields = ('nombre','lugar')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'lugar': forms.Select(attrs={'class':'form-select'})
        }


class RutaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RutaCreateForm, self).__init__(*args, **kwargs)
        # obtenemos todas las personas con permiso de transportista
        personas = User.objects.filter().all()
        self.fields['persona'].choices = [(persona.id, '{} - {}'.format(persona, persona.perfil.lugar.nombre)) for persona in personas if hasattr(persona, 'perfil')]

    class Meta:
        model = Ruta
        fields = ('nombre','persona','patente')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'persona': forms.Select(attrs={'class': 'form-select'}),
            'patente': forms.TextInput(attrs={'class':'form-control'}),
        }


class RutaCerrarForm(forms.ModelForm):

    class Meta:
        model = Ruta
        fields = ('estado',)


class EnvioRecepcionarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnvioRecepcionarForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'fecha_recepcion':
                field.disabled = True

    class Meta:
        model = Envio
        fields = ('lugar_o', 'lugar_d', 'fecha_envio', 'fecha_recepcion', 'medio_transporte', 'numero_documento')
        widgets = {
            'lugar_d': forms.Select(attrs={'class': 'form-select'}),
            'lugar_o': forms.Select(attrs={'class': 'form-select'}),
            'medio_transporte': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_envio': forms.TextInput(attrs={'class': 'form-control', 'id': 'fechaenvio'}),
            'fecha_recepcion': forms.TextInput(attrs={'class': 'form-control', 'id': 'fecha_recepcion'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'})
        }
