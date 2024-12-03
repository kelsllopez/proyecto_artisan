from django import forms
from .models import Equipo,AreaEquipo

class AreaEquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AreaEquipoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 

    class Meta:
        model = AreaEquipo
        fields = '__all__'

class EquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EquipoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 

    class Meta:
        model = Equipo
        fields = '__all__'