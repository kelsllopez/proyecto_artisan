from django.urls import path, include
from .views import ConjuntoEstadoCreateView, ConjuntoEstadoDeleteView, ConjuntoEstadoTemplateView, ConjuntoEstadoUpdateView, EstadoCreateView, EstadoDeleteView, EstadoTemplateView, EstadoUpdateView

estado_patterns = ([
    path('conjunto', ConjuntoEstadoTemplateView.as_view(), name='lista_conjunto'),
    path('', EstadoTemplateView.as_view(), name='lista_estado'),
    path('conjunto/crear', ConjuntoEstadoCreateView.as_view(), name='crear-conjunto'),
    path('conjunto/actualizar/<int:pk>', ConjuntoEstadoUpdateView.as_view(), name='actualizar-conjunto'),
    path('conjunto/eliminar/<int:pk>', ConjuntoEstadoDeleteView.as_view(), name='eliminar-conjunto'),
    path('eliminar/<int:pk>', EstadoDeleteView.as_view(), name="eliminar-estado"),
    path('crear', EstadoCreateView.as_view(), name='crear-estado'),
    path('actualizar/<int:pk>', EstadoUpdateView.as_view(), name='actualizar-estado'),
], 'estados')
