from django import forms
from .models import Perfil
from django.core.exceptions import ValidationError



class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('avatar','pin','firma_digital')
        widgets = {
            'pin': forms.NumberInput(attrs={'class':'form-control','onkeydown':'return event.keyCode !== 69','max':'9999'}),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'firma_digital': forms.ClearableFileInput(attrs={'class':'form-control'})
        }
        help_texts = {
            'avatar': 'Para eliminar tu imagen de perfil actual, tickea la casilla <strong>limpiar</strong>.'
        }

class PerfilLoginForm(forms.Form):
    pin = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','onkeydown':'return event.keyCode !== 69','max':'9999'}))

    def clean_pin(self):
        data = self.cleaned_data['pin']
        if len(data) != 4:
            raise ValidationError("Recuerda que el PIN esta compuesto de cuatro números.")