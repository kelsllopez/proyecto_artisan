from django.contrib import admin
from .models import PautaProduccion
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(PautaProduccion,SimpleHistoryAdmin)