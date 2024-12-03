from django import forms
from .models import Solicitud
from django.contrib.auth.models import User


# Formulario para crear la solicitud
class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        encargados = kwargs.pop('encargados') if 'encargados' in kwargs else None
        super(SolicitudForm, self).__init__(*args, **kwargs)
        campos = ['lugar_o']
        for campo in campos:
            self.fields[campo].disabled = True
            self.fields[campo].initial = user.perfil.lugar
        if encargados:
            self.fields['encargados'].initial = encargados

    encargados = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=True, widget=forms.SelectMultiple(), label="Las personas que seran notificadas por esta solicitud.")

    class Meta:
        model = Solicitud
        fields = ("lugar_o", "encargados")
