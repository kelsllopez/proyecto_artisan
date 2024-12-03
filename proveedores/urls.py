from django.urls import path, include
from .views import ProveedorActualizarView,ProveedorCreateView, ProveedorExportarView, ProveedorInsumoMostrarView,ProveedorListaView,ProveedorDetalleView,ProveedorBorrarView
from .views import ProveedorInsumoCreateView, ProveedorInsumoUpdateView, ProveedorInsumoDeleteView

proveedorinsumo_patterns = ([
   path('asociar/',ProveedorInsumoCreateView.as_view(),name='asociar'),
   path('asociar/actualizar/<int:pk>',ProveedorInsumoUpdateView.as_view(),name='actualizar'),
   path('asociar/eliminar/<int:pk>',ProveedorInsumoDeleteView.as_view(),name='eliminar'),
   path('asociar/mostrar/<int:pk>',ProveedorInsumoMostrarView.as_view(),name='mostrar'),
],'insumo')

proveedor_patterns = ([
   path('', ProveedorListaView.as_view(),name='lista'),
   path('crear', ProveedorCreateView.as_view(),name='crear'),
   path('actualizar/<int:pk>', ProveedorActualizarView.as_view(),name='actualizar'),
   path('detalle/<int:pk>', ProveedorDetalleView.as_view(),name='detalle'),
   path('eliminar/<int:pk>', ProveedorBorrarView.as_view(),name='eliminar'),
   path('exportar', ProveedorExportarView.as_view(),name='exportar'),
   path('', include(proveedorinsumo_patterns))
],'proveedor')
