from django import forms
from .models import OrdenDeCompra

class OrdenDeCompraCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeCompraCreateForm, self).__init__(*args, **kwargs)
        self.fields['archivos'].required = False
        self.fields['bodega'].required = True
        campos = ['numero', 'estado']
        for campo in campos:
            self.fields[campo].disabled = True

    archivos = forms.FileField(required=False)


    class Meta:
        model = OrdenDeCompra
        fields = ['fecha', 'proveedor', 'bodega', 'numero', 'estado', 'condiciones', 'archivos']
        widgets = {
            'proveedor': forms.Select(attrs={'class': '', 'onchange': 'vue.obtenerInsumos()'}),
            'bodega': forms.Select(attrs={'class': ''}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height:50px;height:50px;'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'id': 'pickadate', 'class': 'form-control'}),
        }

class OrdenDeCompraValidarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeCompraValidarForm, self).__init__(*args, **kwargs)
        campos = ['numero', 'estado', 'proveedor', 'bodega']
        for campo in campos:
            self.fields[campo].disabled = True
        self.fields['archivos'].required = False

    archivos = forms.FileField(required=False)


    class Meta:
        model = OrdenDeCompra
        fields = ['fecha', 'proveedor', 'bodega', 'numero', 'estado', 'pagada', 'condiciones', 'archivos']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'pagada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height:50px;height:50px;'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'id': 'pickadate', 'class': 'form-control'}),
        }

class OrdenDeCompraRecepcionarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeCompraRecepcionarForm, self).__init__(*args, **kwargs)
        campos = ['numero', 'estado', 'proveedor', 'bodega', 'fecha']
        for campo in campos:
            self.fields[campo].disabled = True
        self.fields['fecha_facturacion'].required = True
        self.fields['archivos'].required = False

    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeCompra
        fields = ['fecha', 'proveedor', 'bodega', 'numero', 'estado', 'pagada', 'condiciones', 'fecha_recepcion', 'numero_factura', 'fecha_facturacion', 'guia_despacho', 'archivos']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height:50px;height:50px;'}),
            'pagada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'id': 'pickadate', 'class': 'form-control'}),
            'fecha_recepcion': forms.DateInput(attrs={'id': 'fecha_recepcion', 'class': 'form-control'}),
            'fecha_facturacion': forms.DateInput(attrs={'id': 'fecha_facturacion', 'class': 'form-control'}),
            'guia_despacho': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('numero_factura') and not cleaned_data.get('guia_despacho'):
            raise forms.ValidationError({'numero_factura': 'Debes introducir el número de factura ó la guía de despacho.'})

class OrdenDeCompraEtiquetarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeCompraEtiquetarForm, self).__init__(*args, **kwargs)
        campos = ['proveedor', 'bodega', 'numero', 'estado']
        for campo in campos:
            self.fields[campo].disabled = True

    class Meta:
        model = OrdenDeCompra
        fields = ['proveedor', 'bodega', 'numero', 'estado']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class OrdenDeCompraPagarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrdenDeCompraPagarForm, self).__init__(*args, **kwargs)
        campos = ['numero', 'estado', 'proveedor', 'bodega', 'fecha', 'condiciones', 'fecha_recepcion', 'guia_despacho']
        for campo in campos:
            self.fields[campo].disabled = True
        obligatorios = ['numero_factura', 'fecha_facturacion', 'fecha_pago', 'pago']
        for campo in obligatorios:
            self.fields[campo].required = True
        self.fields['archivos'].required = False
    
    archivos = forms.FileField(required=False)

    class Meta:
        model = OrdenDeCompra
        fields = ['fecha', 'proveedor', 'bodega', 'numero', 'estado', 'condiciones', 'fecha_recepcion', 'guia_despacho', 'fecha_facturacion', 'numero_factura', 'fecha_pago', 'pago', 'archivos']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'bodega': forms.Select(attrs={'class': 'form-select'}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'style': 'min-height:50px;height:50px;'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'id': 'pickadate', 'class': 'form-control'}),
            'fecha_recepcion': forms.DateInput(attrs={'id': 'fecha_recepcion', 'class': 'form-control'}),
            'fecha_facturacion': forms.DateInput(attrs={'id': 'fecha_facturacion', 'class': 'form-control'}),
            'guia_despacho': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateInput(attrs={'id': 'fecha_pago', 'class': 'form-control'}),
            'pago': forms.Select(attrs={'class': 'form-select'})
        }
