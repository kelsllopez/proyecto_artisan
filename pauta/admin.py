from django.contrib import admin
from .models import Etapa, Pauta,Ingrediente,Columna,Instruccion
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

class IngredienteInline(admin.TabularInline):                                                                                               
    model = Ingrediente
    min_num = 2

class EtapaInline(admin.TabularInline):
    model = Etapa
    min_num = 1

class PautaAdmin(SimpleHistoryAdmin):
    readonly_fields = ('created', 'updated')
    #cantidad de insumos a mostrar en la lista por pagina.
    list_per_page = 50
    inlines = (IngredienteInline,EtapaInline)

admin.site.register(Pauta,PautaAdmin)
admin.site.register(Etapa)
admin.site.register(Ingrediente)
admin.site.register(Columna)