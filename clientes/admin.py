from clientes.models import Cliente, ClienteLocal
from django.contrib import admin

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista de clientes
    list_display = ('nombre', 'razon_social', 'rut', 'telefono', 'contacto', 'email', 'celular')
    #campos que serviran de busqueda
    search_fields = ('nombre','contacto', 'rut')
    #posibilidad de filtrar por fecha de creación del insumo
    date_hierarchy = 'created'
    #clientes por pagina
    list_per_page = 25


class ClienteLocalAdmin(admin.ModelAdmin):
    #campos solo de lectura
    readonly_fields = ('created', 'updated')
    #campos que se mostraran en la lista del panel administrativo
    list_display = ('cliente', 'local', 'direccion', 'contacto', 'email', 'celular')
    #campos que seran aplicados en el buscador
    search_fields = ('cliente__nombre','nombre', 'contacto')
    #proveedores a mostrar por pagina
    list_per_page = 50

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteLocal, ClienteLocalAdmin)