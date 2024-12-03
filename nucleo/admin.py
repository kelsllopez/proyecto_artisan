from django.contrib import admin
from .models import Insumo, InsumoDirectoProducto, Linea, Producto, Moneda, InsumoElaboracionProducto, Rama  # Asegúrate de importar Rama
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User, Permission


class RamaAdmin(admin.ModelAdmin):
    # Campos solo de lectura
    readonly_fields = ('created', 'updated')
    
    # Campos que se mostrarán en la lista del panel administrativo
    list_display = ('nombre', 'created', 'updated')
    
    # Campos que serán aplicados en el buscador
    search_fields = ('nombre',)
    
    # Cantidad de ramas a mostrar en la lista por página
    list_per_page = 50


class MonedaAdmin(admin.ModelAdmin):
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50

#Clase que maneja los insumos en el panel administrativo
class InsumoAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('nombre_insumo','unidad','stock_critico')
    #campos que seran aplicados en el buscador
    search_fields = ('nombre',)
    #posibilidad de filtrar por fecha de creación del insumo
    date_hierarchy = 'created'
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50

    #Funciones personalizadas para obtención de datos extras del producto
    @admin.display(description='Nombre insumo')
    def nombre_insumo(self, obj):
        return obj.nombre.upper()

#Clase que maneja las ramas en el panel administrativo
class LineaAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('nombre','created')
    #campos que seran aplicados en el buscador
    search_fields = ('nombre',)
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50


# Clase para insumos de elaboración en línea de productos
class InsumoElaboracionInLine(admin.TabularInline):
    model = InsumoElaboracionProducto
    extra = 1


#Clase para descriptores inline de los productos
class DescriptorInLine(admin.TabularInline):
    model = InsumoDirectoProducto
    extra = 1

#Clase que maneja los insumos en el panel administrativo
class ProductoAdmin(admin.ModelAdmin):
    #campos que se mostraran en el agregar / modificar producto
    fields = ('nombre', 'linea', 'presentacion', 'unidad', 'duracion', 'maduracion', 'stock_critico', 'id_comercio_net')
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('codigo','linea','nombre','presentacion_producto','duracion_dias','maduracion_dias','stock_unidades')
    #campos que redirigiran a editar
    list_display_links = ('nombre','codigo')
    #campos que seran aplicados en el buscador
    search_fields = ('nombre',)
    #posibilidad de filtrar por fecha de creación del insumo
    date_hierarchy = 'created'
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50
    #aplicamos la visualización del descriptor en linea.
    inlines = (DescriptorInLine,InsumoElaboracionInLine)


    #Funciones personalizadas para obtención de datos extras del producto
    @admin.display(description='Presentación Producto')
    def presentacion_producto(self, obj):
        return ("%s %s" % (obj.presentacion, obj.unidad))
    
    @admin.display(description="Ciclo de vida producción")
    def maduracion_dias(self, obj):
        return str(obj.maduracion) + " días"
    
    @admin.display(description="Ciclo de vida comercial")
    def duracion_dias(self, obj):
        return str(obj.duracion) + " días"
    
    @admin.display(description="Stock crítico de inventario")
    def stock_unidades(self, obj):
        return str(obj.stock_critico) + " unidades"


#registramos los modelos con sus configuraciones del panel administrativo
admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Linea, LineaAdmin)
admin.site.register(Moneda, MonedaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Rama, RamaAdmin)


from django.contrib.admin.models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]


class PermissionFilterMixin(object):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in ('permissions', 'user_permissions'):
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            qs = _filter_permissions(qs)
            kwargs['queryset'] = qs

        return super(PermissionFilterMixin, self).formfield_for_manytomany(db_field, request, **kwargs)


class MyGroupAdmin(PermissionFilterMixin, GroupAdmin):
    pass


class MyUserAdmin(PermissionFilterMixin, UserAdmin):
    pass


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)
admin.site.register(Group, MyGroupAdmin)

modelos_a_ignorar = ['auth','historical','group','permission','user','session','logentry','contenttype']
lista = []
for modelo in modelos_a_ignorar:
    lista.append('add_{}'.format(modelo))
    lista.append('change_{}'.format(modelo))
    lista.append('delete_{}'.format(modelo))
    lista.append('view_{}'.format(modelo))
def _filter_permissions(qs):
    return qs.exclude(codename__in=tuple(lista)) \
    .exclude(codename__endswith='userobjectpermission') \
    .exclude(codename__endswith='groupobjectpermission') \
    .exclude(codename__contains='historical')  # django-guardian

admin.site.register(Permission)