from django import forms
from .models import EquipoUtensilioLimpieza, GrupoEquipos, RegistroLimpiezaEquipo, UtensilioLimpieza
from equipo.models import Equipo
from django.shortcuts import get_object_or_404
import datetime
import rsa

class UtensilioLimpiezaForm(forms.ModelForm):
    class Meta:
        model = UtensilioLimpieza
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':''})
        }

class GruposEquiposForm(forms.ModelForm):
    class Meta:
        model = GrupoEquipos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }

class EquipoUtensilioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        utensilio = kwargs.pop('utensilio') if 'utensilio' in kwargs else None
        super(EquipoUtensilioForm, self).__init__(*args, **kwargs)
        self.fields['utensilio'].initial = utensilio if utensilio else None
        equipos = Equipo.objects.all()
        self.fields['equipo'].choices = [(equipo.pk,"{} - {} - {}".format(equipo.nombre,equipo.area.nombre,equipo.area.lugar.nombre)) if equipo.area != None else (equipo.pk,equipo.nombre) for equipo in equipos]

    class Meta:
        model = EquipoUtensilioLimpieza
        fields = '__all__'
        widgets = {
            'equipo': forms.Select(attrs={'class':''}),
            'utensilio': forms.Select(attrs={'class':''})
        }

class RegistroLimpiezaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        equipo = kwargs.pop('equipo') if 'equipo' in kwargs else None
        super(RegistroLimpiezaForm, self).__init__(*args, **kwargs)
        if equipo:
            with open('privada.PEM', mode='rb') as privatefile:
                keydata = privatefile.read()
            privkey = rsa.PrivateKey.load_pkcs1(keydata)
            pk = rsa.decrypt(bytes.fromhex(equipo),privkey).decode()
            equipo = get_object_or_404(Equipo,pk=pk)
            self.fields['equipo'].choices = [(equipo.pk,"{}".format(equipo.nombre))]
            self.fields['utensilios'].choices = [(utensilio.utensilio.id,utensilio.utensilio.nombre) for utensilio in equipo.equipoutensiliolimpieza_set.all()]
        
    class Meta:
        model = RegistroLimpiezaEquipo
        fields = ('equipo','observacion','utensilios')
        widgets = {
            'equipo': forms.Select(attrs={'class':'form-select'}),
            'observacion': forms.Textarea(attrs={'class':'form-control'}),
            'utensilios': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'utensilios': 'Artículos',
        }
        help_texts = {
            'utensilios': 'Seleccione los artículos de limpieza y desinfección que <strong>utilizó durante</strong> la limpieza.'
        }

class RegistroLimpiezaUpdateSupervisorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroLimpiezaUpdateSupervisorForm, self).__init__(*args, **kwargs)
        deshabilitar = ['equipo','observacion','utensilios']
        self.fields['utensilios'].choices = [(utensilio.utensilio.id,utensilio.utensilio.nombre) for utensilio in kwargs['instance'].equipo.equipoutensiliolimpieza_set.all()]
        for d in deshabilitar:
            self.fields[d].disabled = True
        
        
    class Meta:
        model = RegistroLimpiezaEquipo
        fields = ('equipo','observacion','utensilios','accion_correctiva','estado')
        widgets = {
            'equipo': forms.Select(attrs={'class':'form-select'}),
            'observacion': forms.Textarea(attrs={'class':'form-control'}),
            'accion_correctiva': forms.Textarea(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-select'}),
            'utensilios': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'utensilios': 'Artículos',
        }

class RegistroLimpiezaUpdateOperadorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroLimpiezaUpdateOperadorForm, self).__init__(*args, **kwargs)
        self.fields['utensilios'].choices = [(utensilio.utensilio.id,utensilio.utensilio.nombre) for utensilio in kwargs['instance'].equipo.equipoutensiliolimpieza_set.all()]
        self.fields['estado'].disabled = True
        self.fields['equipo'].disabled = True
        
    class Meta:
        model = RegistroLimpiezaEquipo
        fields = ('equipo','observacion','utensilios','estado')
        widgets = {
            'equipo': forms.Select(attrs={'class':'form-select'}),
            'observacion': forms.Textarea(attrs={'class':'form-control'}),
            'utensilios': forms.CheckboxSelectMultiple(),
            'estado': forms.Select(attrs={'class':'form-select'}),
        }
        labels = {
            'utensilios': 'Artículos',
        }

class RegistroLimpiezaExcelForm(forms.Form):
    fechainicio = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form-control','id':'fechainicio'}),
        label="Fecha de Inicio")
    fechafin = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form-control','id':'fechafin'}),
        label="Fecha de Termino")