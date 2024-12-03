from django import forms
from django.forms import widgets
from django.forms.fields import ChoiceField, FileField
from .models import ListaPrecio, OrdenDeVenta
from django.core.exceptions import ValidationError
from clientes.models import Cliente
from django.contrib.auth.models import User

class ListaPrecioForm(forms.ModelForm):
    class Meta:
        model = ListaPrecio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nombre de Lista de Precios"})
        }
        text_helpers = {
            'nombre': 'El nombre que recibira la lista de precios.'
        }

class OrdenDeVentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaForm, self).__init__(*args, **kwargs)
        self.fields['archivos'].required = False
        self.fields['archivos'].label = 'Archivos Adjuntos'

    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeVenta
        fields = ('cliente', 'fecha', 'n_orden_cliente', 'envio', 'condiciones', 'archivos')
        widgets = {
            'condiciones': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'id': 'fecha'}),
            'envio': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'envio', 'onkeyup': 'vue.actualizarTotal()'}),
            'n_orden_cliente': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrdenDeVentaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaUpdateForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].disabled = True
        ov = kwargs.get('instance')
        locales = [(local.id, "{} {}".format(local.local, local.direccion)) for local in ov.cliente.clientelocal_set.all()]
        if len(locales) == 0:
            locales = [('matriz', 'Casa Matriz {}'.format(ov.cliente.direccion))]
        self.fields['local'].choices = locales
        self.fields['archivos'].required = False
        self.fields['archivos'].label = 'Archivos Adjuntos'

    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeVenta
        fields = ('cliente', 'local', 'fecha', 'n_orden_cliente', 'envio', 'condiciones', 'archivos')
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-control'}),
            'envio': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'envio', 'onkeyup': 'vue.actualizarTotal()'}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'id': 'fecha'}),
            'n_orden_cliente': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrdenDeVentaFacturarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaFacturarForm, self).__init__(*args, **kwargs)
        disabled = ['fecha']
        for d in disabled:
            self.fields[d].disabled = True
        self.fields['archivos'].required = False
        self.fields['archivos'].label = 'Archivos Adjuntos'

    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeVenta
        fields = ('fecha', 'fecha_f', 'archivos')
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control', 'id': 'fecha'}),
            'fecha_f': forms.TextInput(attrs={'class': 'form-control'})
        }

class OrdenDeVentaCargarForm(forms.Form):
    archivos = forms.FileField(required=False)

    jump = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'jump'}), label="Código Jump Seller", required=False
    )


class OrdenDeVentaPickearForm(forms.Form):
    cliente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'cliente'}), label='Cliente', required=True)
    ov = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'ov'}), label='Orden de Venta', required=True)

    def clean_cliente(self):
        cliente_id = self.cleaned_data['cliente']
        cliente = Cliente.objects.filter(pk=int(cliente_id)).first()
        if cliente:
            return cliente_id
        else:
            raise ValidationError('El cliente seleccionado no es valido!')

    def clean_ov(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.get("cliente"):
            raise forms.ValidationError("El Cliente seleccionado no es valido")
        ov = self.cleaned_data['ov']
        orden = OrdenDeVenta.objects.filter(pk=int(ov), estado='Pendiente').first()
        if orden:
            return ov
        else:
            raise ValidationError('La Orden de Venta no ha sido encontrada!')


class OrdenDeVentaAsignarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaAsignarForm, self).__init__(*args, **kwargs)
        self.fields['archivos'].required = False
        self.fields['archivos'].label = 'Archivos Adjuntos'
        # obtenemos todas las personas con permiso de transportista
        personas = User.objects.filter().all()
        personas_f = []
        for p in personas:
            if p.ruta_set.count() > 0:
                personas_f.append(p)
        self.fields['personas'].choices = [('', '-- Seleciona un Repartidor --')] + [(persona.id, '{} - {}'.format(persona, persona.perfil.lugar.nombre)) for persona in personas_f if hasattr(persona, 'perfil')]

    archivos = forms.FileField(required=False)
    personas = ChoiceField(widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'vue.obtenerRutas(event)'}))

    class Meta:
        model = OrdenDeVenta
        fields = ('personas', 'archivos')

class OrdenDeVentaReAsignarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaReAsignarForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].disabled = True

    class Meta:
        model = OrdenDeVenta
        fields = ('cliente',)

class OrdenDeVentaPickearOVForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeVentaPickearOVForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].disabled = True
        self.fields['archivos'].required = False
        self.fields['archivos'].label = 'Archivos Adjuntos'

    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeVenta
        fields = ('cliente', 'archivos')

class OrdenDeVentaExcelForm(forms.Form):
    fechainicio = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form-control','id':'fechainicio'}),
        label="Fecha de Inicio")
    fechafin = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form-control','id':'fechafin'}),
        label="Fecha de Termino")