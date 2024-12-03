from django.contrib import admin
from .models import OrdenDeCompra, OrdenDeCompraInsumo
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(OrdenDeCompra,SimpleHistoryAdmin)
admin.site.register(OrdenDeCompraInsumo)