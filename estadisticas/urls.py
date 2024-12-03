from django.urls import path, include
from .views import EstadisticasBodegaView

estadisticas_patterns = [
    path('', EstadisticasBodegaView.as_view(), name='estadistica'),
]
