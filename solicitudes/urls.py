from django.urls import path
from .views import SolicitudCompletarView, SolicitudCreateView, SolicitudDeleteView, SolicitudListView, SolicitudUpdateView

solicitudes_patterns = (
    [
        path('', SolicitudListView.as_view(), name='lista'),
        path('crear', SolicitudCreateView.as_view(), name='crear'),
        path('eliminar/<int:pk>', SolicitudDeleteView.as_view(), name='eliminar'),
        path('actualizar/<int:pk>', SolicitudUpdateView.as_view(), name='actualizar'),
        path('completar/<int:pk>', SolicitudCompletarView.as_view(), name='completar')
    ], 'solicitudes'
)
