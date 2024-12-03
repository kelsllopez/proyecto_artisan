from django.urls import *
from .views import *
nucleo_patterns = [
    path('', HomeView.as_view(), name='home'),
    re_path(r'^media/', protected_media, name='media'),  # Cambiado a re_path
    path('acliente/', direccion_cliente, name='actualizarclientex'),  # Cambiado a path
    path('generar/', generate_pdf, name='generate_pdf'),


]

areas_patterns = [
    path('', RamaListView.as_view(), name='lista'),
    path('crear/', RamaCreateView.as_view(), name='crear'),
    path('modificar/<int:pk>/', RamaUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>/', RamaDeleteView.as_view(), name='eliminar'),
]

productos_patterns = [
    path('', ProductoListView.as_view(), name='lista'),
    path('crear/', ProductoCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>/', ProductoUpdateView.as_view(), name='actualizar'),
    path('delete/<int:pk>/', ProductodeleteView.as_view(), name='eliminar'),

]

insumo_patterns = [
    path('', InsumoListView.as_view(), name='lista'),
    path('crear/', InsumoCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>/', InsumoUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>/', InsumoDeleteView.as_view(), name='eliminar'),
]
