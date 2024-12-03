from django.contrib import admin
from .models import Proveedor, ProveedorInsumo
# Register your models here.


class ProveedorAdmin(admin.ModelAdmin):
    # campos solo de lectura
    readonly_fields = ('created', 'updated')
    # campos que se mostraran en la lista del panel administrativo
    list_display = ('empresa_nombre', 'empresa_rut', 'ventas_nombre', 'ventas_email', 'ventas_celular')
    # secciones para el formulario de agregar un proveedor
    fieldsets = (
        ('Información General', {
            'fields': ('empresa_nombre', 'empresa_rut', 'empresa_giro', 'empresa_region', 'empresa_comuna', 'empresa_direccion')
        }),
        ('Contacto Comercial', {
            'fields': ('ventas_nombre', 'ventas_email', 'ventas_celular')
        }),
    )
    # posibilidad de filtrar por fecha de creación del insumo
    date_hierarchy = 'created'
    # campos que seran aplicados en el buscador
    search_fields = ('empresa_nombre',)
    # proveedores a mostrar por pagina
    list_per_page = 50


class ProveedorInsumoAdmin(admin.ModelAdmin):
    # campos solo de lectura
    readonly_fields = ('created', 'updated')
    # campos que se mostraran en la lista del panel administrativo
    list_display = ('insumo', 'proveedor', 'precio')
    # campos que seran aplicados en el buscador
    search_fields = ('insumo__nombre', 'proveedor__empresa_nombre')
    # posibilidad de filtrar por fecha de creación del insumo
    date_hierarchy = 'created'
    # proveedores a mostrar por pagina
    list_per_page = 50


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(ProveedorInsumo, ProveedorInsumoAdmin)
