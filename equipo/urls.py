from django.urls import path, include
from .views import EquipoDeleteView, EquipoListView,EquipoCreateView, EquipoQRView, EquipoUpdateView
from .views import AreaEquipoListView, AreaEquipoCreateView, AreaEquipoDeleteView, AreaEquipoUpdateView

area_patterns = ([
    path('',AreaEquipoListView.as_view(),name='lista'),
    path('crear',AreaEquipoCreateView.as_view(),name='crear'),
    path('actualizar/<int:pk>',AreaEquipoUpdateView.as_view(),name='actualizar'),
    path('eliminar/<int:pk>',AreaEquipoDeleteView.as_view(),name='eliminar')
],'area')

equipo_patterns = ([
    path('',EquipoListView.as_view(),name='lista'),
    path('crear',EquipoCreateView.as_view(),name='crear'),
    path('actualizar/<int:pk>',EquipoUpdateView.as_view(),name='actualizar'),
    path('eliminar/<int:pk>',EquipoDeleteView.as_view(),name='eliminar'),
    path('qr/<int:pk>',EquipoQRView.as_view(),name='qr'),
    path('area/',include(area_patterns))
],'equipo')

