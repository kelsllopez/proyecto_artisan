from django.urls import path
from .views import *

inventario_patterns = ([
    path('<str:lugar>/insumos', InventarioInsumoListView.as_view(), name='insumo'),
    path('<str:lugar>/productos', InventarioProductoView.as_view(), name='producto'),
    path('<str:lugar>/insumos/<int:pk>/actualizar', InventarioInsumoUpdateView.as_view(), name='insumo-actualizar'),
    path('<str:lugar>/insumos/valorizar', InventarioInsumoValorizar.as_view(), name='insumo-valorizar'),
    path('insumos', InventarioGlobalInsumoListView.as_view(), name='insumo-global'),
    path('productos', InventarioGlobalProductoListView.as_view(), name='producto-global'),
    path('<str:lugar>/productos/<int:pk>/actualizar', InventarioProductoUpdateView.as_view(), name='producto-actualizar'),
], 'inventario')

bodega_patterns = ([
    path('', BodegaListView.as_view(), name='lista'),
    path('crear', BodegaCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>', BodegaUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', BodegaDeleteView.as_view(), name='eliminar'),
], 'bodega')

historial_patterns = ([
    path('crear', BodegaHistorialCreateView.as_view(), name='crear'),
    path('crear/<int:pk>', HacerInventarioView.as_view(), name='crearmanual'),
    path('detalle/<int:pk>', BodegaHistorialDetailView.as_view(), name='detalle'),
    path('', BodegaHistorialListView.as_view(), name='lista'),
    path('eliminar/<int:pk>', HistorialBodegaDeleteView.as_view(), name='eliminar'),
], 'historial')
