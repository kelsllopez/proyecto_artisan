from django.contrib import admin
from django.db.models import query
from .models import InventarioProducto, InventarioInsumo, Bodega
from django.utils import safestring
from django.db.models import F
# Register your models here.

#Clase que maneja las bodegas en el panel administrativo
class bodegaAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('nombre','created')
    #campos que seran aplicados en el buscador
    search_fields = ('nombre',)
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50


#filtros personalizado para filtrar
class InventarioProductoStockFilter(admin.SimpleListFilter):
    title = 'Estado Stock'
    parameter_name = 'producto'

    def lookups(self, request, model_admin):
        return (
            ('peligro',safestring.mark_safe('<b style=\'color:red\'>Peligro</b>')),
            ('bien',safestring.mark_safe('<b style=\'color:green\'>Bien</b>')),
            )

    def queryset(self, request, queryset):
        if self.value() == 'peligro':
            return queryset.filter(producto__stock_critico__gte = F('cantidad'))
        elif self.value() == 'bien':
            return queryset.filter(producto__stock_critico__lte = F('cantidad'))

#filtro personalizado
class InventarioInsumoStockFilter(admin.SimpleListFilter):
    title = 'Estado Stock'
    parameter_name = 'insumo'

    def lookups(self, request, model_admin):
        return (
            ('peligro',safestring.mark_safe('<b style=\'color:red\'>Peligro</b>')),
            ('bien',safestring.mark_safe('<b style=\'color:green\'>Bien</b>')),
            )

    def queryset(self, request, queryset):
        if self.value() == 'peligro':
            return queryset.filter(insumo__stock_critico__gte = F('cantidad'))
        elif self.value() == 'bien':
            return queryset.filter(insumo__stock_critico__lte = F('cantidad'))
        

class InventarioInsumoAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('insumo','bodega','cantidad', 'estado','created', 'updated')
    #campos que seran aplicados en el buscador
    search_fields = ('insumo__nombre',)
    #filtros de lista
    list_filter = ('bodega',InventarioInsumoStockFilter)
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50

    #Funciones personalizadas para obtención de datos extras del producto
    @admin.display(description='Estado')
    def estado(self, obj):
        insumo= obj.insumo
        if insumo.stock_critico > obj.cantidad:
            return safestring.mark_safe('<b style="color:red">Peligro (-{})</b>'.format(abs(insumo.stock_critico - obj.cantidad)))
        else:
            return safestring.mark_safe('<b style="color:green">Bien (+{})</b>'.format(abs(insumo.stock_critico - obj.cantidad)))

class InventarioProductoAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('producto','bodega','cantidad','estado')
    #campos que seran aplicados en el buscador
    search_fields = ('producto__nombre',)
    #filtros de lista
    list_filter = ('bodega', InventarioProductoStockFilter)
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50

    #Funciones personalizadas para obtención de datos extras del producto
    @admin.display(description='Estado')
    def estado(self, obj):
        producto = obj.producto
        if producto.stock_critico > obj.cantidad:
            return safestring.mark_safe('<b style="color:red">Peligro (-{})</b>'.format(abs(producto.stock_critico - obj.cantidad)))
        else:
            return safestring.mark_safe('<b style="color:green">Bien (+{})</b>'.format(abs(producto.stock_critico - obj.cantidad)))



admin.site.register(InventarioInsumo, InventarioInsumoAdmin)
admin.site.register(InventarioProducto, InventarioProductoAdmin)
admin.site.register(Bodega, bodegaAdmin)