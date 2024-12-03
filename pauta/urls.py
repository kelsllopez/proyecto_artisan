from .models import Pauta
from django.urls import path, include
from .views import ColumnaCreateView, ColumnaDeleteView, ColumnaListView, ColumnaUpdateView, PautaCreateView, PautaElaboracionRetrieve, PautaTemplateView, PautaDeleteView, PautaUpdateView, PautaDetailView

pauta_patterns = ([
    path('',PautaTemplateView.as_view(),name='lista'),
    path('eliminar/<int:pk>',PautaDeleteView.as_view(),name='eliminar'),
    path('crear',PautaCreateView.as_view(),name='crear'),
    path('actualizar/<int:pk>',PautaUpdateView.as_view(),name='actualizar'),
    path('detalle/<int:pk>',PautaDetailView.as_view(),name='detalle'),
    path('columnas',ColumnaListView.as_view(),name='columna'),
    path('columnas/crear',ColumnaCreateView.as_view(),name='columna-crear'),
    path('columnas/actualizar/<int:pk>',ColumnaUpdateView.as_view(),name='columna-actualizar'),
    path('columnas/eliminar/<int:pk>',ColumnaDeleteView.as_view(),name='columna-eliminar')
],'pauta')
