from django.contrib import admin
from .models import ConjuntoEstado, Estado, EstadoConjunto, EstadoInsumo, EstadoProducto

# Registrar ConjuntoEstado
@admin.register(ConjuntoEstado)
class ConjuntoEstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created', 'updated')
    search_fields = ('nombre',)

# Registrar Estado
@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created', 'updated', 'peso', 'uc', 'uff', 'unc')
    search_fields = ('nombre',)

# Registrar EstadoConjunto
@admin.register(EstadoConjunto)
class EstadoConjuntoAdmin(admin.ModelAdmin):
    list_display = ('conjunto', 'estado', 'pos')
    list_filter = ('conjunto', 'estado')
    search_fields = ('conjunto__nombre', 'estado__nombre')
    ordering = ['pos']

# Registrar EstadoInsumo
@admin.register(EstadoInsumo)
class EstadoInsumoAdmin(admin.ModelAdmin):
    list_display = ('estado', 'insumo', 'created', 'updated')
    search_fields = ('estado__nombre', 'insumo__nombre')

# Registrar EstadoProducto
@admin.register(EstadoProducto)
class EstadoProductoAdmin(admin.ModelAdmin):
    list_display = ('estado', 'producto', 'created', 'updated')
    search_fields = ('estado__nombre', 'producto__nombre')
