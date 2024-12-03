from django import forms
from django.contrib.auth.models import User, Permission, Group
from django.forms import widgets
from inventario.models import Bodega


class GroupCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Group
        fields = '__all__'


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'ubicacion':
                field.widget.attrs['class'] = 'form-control'
        requeridos = ['first_name', 'last_name', 'email']
        for r in requeridos:
            self.fields[r].required = True
        # self.fields['user_permissions'].queryset = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view')
    ubicacion = forms.ModelChoiceField(queryset=Bodega.objects, required=True, widget=forms.Select(attrs={'class': 'form-select'}), help_text="Selecciona la planta donde el empleado realiza sus labores.", label="Planta")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'groups', 'ubicacion']


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        requeridos = ['first_name', 'last_name']
        for r in requeridos:
            self.fields[r].required = True
        checks = []
        for check in checks:
            self.fields[check].widget.attrs['class'] = 'form-check-input'
        self.fields['ubicacion'].initial = [kwargs.get('instance').perfil.lugar.pk]
        # self.fields['user_permissions'].queryset = Permission.objects.exclude(codename__contains='add').exclude(codename__contains='change').exclude(codename__contains='delete').exclude(codename__contains='view')
    ubicacion = forms.ModelChoiceField(queryset=Bodega.objects, required=True, widget=forms.Select(attrs={'class': 'form-select'}), help_text="Selecciona la planta donde el empleado realiza sus labores.", label="Planta")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'groups', 'ubicacion', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-select'})
        }
        help_texts = {
            'is_active': ' Si el usuario es actualmente un empleado de la empresa.'
        }
