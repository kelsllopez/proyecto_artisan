from django.urls import path, include

from .views import ListaPrecioCreateView, ListaPrecioDeleteView, ListaPrecioFixView, ListaPrecioListView, ListaPrecioUpdateView, OrdenDeVentaAsignarView, OrdenDeVentaDetailView, OrdenDeVentaEliminarArchivo, OrdenDeVentaEntregarView, OrdenDeVentaExcel, OrdenDeVentaFacturaView, OrdenDeVentaGenerarExcel,\
    OrdenDeVentaListView, OrdenDeVentaCreateView, OrdenDeVentaDeleteView, OrdenDeVentaPickView, OrdenDeVentaPickearView, OrdenDeVentaReAsignarView, OrdenDeVentaRetrocederView, OrdenDeVentaUpdateView, OrdenDeVentaUploadView, OrdenDeVentaDeleteAllView, OrdenVentaPdfView

listas_patterns = ([
    path('', ListaPrecioListView.as_view(), name='lista'),
    path('agregar', ListaPrecioCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>/', ListaPrecioUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>/', ListaPrecioDeleteView.as_view(), name='eliminar'),
    path('arreglar/',ListaPrecioFixView.as_view(),name='arreglar'),
], "listap")

ordenes_patterns = ([
    path('', OrdenDeVentaListView.as_view(), name='lista'),
    path('agregar', OrdenDeVentaCreateView.as_view(), name='crear'),
    path('detalle/<int:pk>/', OrdenDeVentaDetailView.as_view(), name='detalle'),
    path('actualizar/<int:pk>/', OrdenDeVentaUpdateView.as_view(), name='actualizar'),
    path('facturar/<int:pk>/', OrdenDeVentaFacturaView.as_view(), name='facturar'),
    path('asignar/<int:pk>/', OrdenDeVentaAsignarView.as_view(), name='asignar'),
    path('pickear/', OrdenDeVentaPickView.as_view(), name='pickear'),
    path('pickear/<int:pk>', OrdenDeVentaPickearView.as_view(), name='pickear-ov'),
    path('retroceder/<int:pk>', OrdenDeVentaRetrocederView.as_view(), name='retroceder'),
    path('reasignar/<int:pk>', OrdenDeVentaReAsignarView.as_view(), name='reasignar'),
    path('eliminar/<int:pk>/', OrdenDeVentaDeleteView.as_view(), name='eliminar'),
    path('eliminar/', OrdenDeVentaDeleteAllView.as_view(), name='eliminar-todo'),
    path('eliminar/archivo/<int:pk>/', OrdenDeVentaEliminarArchivo.as_view(), name='eliminar-archivo'),
    path('entregar/<int:pk>/<str:estado>/', OrdenDeVentaEntregarView.as_view(), name='entregar'),
    path('excel', OrdenDeVentaGenerarExcel.as_view(), name='gexcel'),
    path('pdf/<int:pk>',OrdenVentaPdfView.as_view(),name='pdf'),
    path('excel/<int:pk>/', OrdenDeVentaExcel.as_view(), name='excel'),
    path('cargar/', OrdenDeVentaUploadView.as_view(), name='cargar')
], "orden")


ventas_patterns = ([
    path('listas/', include(listas_patterns)),
    path('ordenes/', include(ordenes_patterns)),
], "ventas")
