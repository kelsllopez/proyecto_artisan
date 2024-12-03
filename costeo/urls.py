from django.urls import path
from .views import CosteoProductoDetailView, CosteoProductoListView, MargenDetailView

costeo_patterns = ([
    path('productos/listar/', CosteoProductoListView.as_view(), name='listar'),
    path('margen/', MargenDetailView.as_view(), name='margen'),
    path('detalle/<int:pk>/', CosteoProductoDetailView.as_view(), name='detalle'),
], 'costeo')
