from django.urls import path, include
from .views import GrupoCreateView, GrupoDeleteView, GrupoListView, GrupoUpdateView, RegistroLimpiezaEquipoDeleteView, RegistroLimpiezaEquipoExcel, RegistroLimpiezaEquipoListView, EquipoUtensilioCreateView, EquipoUtensilioLimpiezaDeleteView, RegistroLimpiezaEquipoSeleccionView, RegistroLimpiezaEquipoUpdateView
from .views import *
from .views import RegistroLimpiezaEquipoCreateView,probando


utensilioLimpieza_patterns = ([
    path('',UtensilioLimpiezaListView.as_view(),name='lista'),
    path('crear',UtensilioLimpiezaCreateView.as_view(),name='crear'),
    path('actualizar/<int:pk>',UtensilioLimpiezaUpdateView.as_view(),name='actualizar'),
    path('eliminar/<int:pk>',UtensilioLimpiezaDeleteView.as_view(),name='eliminar'),
    path('asociar',EquipoUtensilioCreateView.as_view(),name='asociar'),
    path('eliminar/asociacion/<int:pk>',EquipoUtensilioLimpiezaDeleteView.as_view(),name='easociar')
], 'utensiliolimpieza')

grupo_patterns = ([
    path('', GrupoListView.as_view(), name='lista'),
    path('crear',GrupoCreateView.as_view(),name='crear'),
    path('actualizar/<int:pk>',GrupoUpdateView.as_view(),name='actualizar'),
    path('eliminar/<int:pk>',GrupoDeleteView.as_view(),name='eliminar'),
], 'grupo')

limpiezaEquipo_patterns = ([
    path('crear',RegistroLimpiezaEquipoCreateView.as_view(),name='crear'),
    path('',RegistroLimpiezaEquipoListView.as_view(),name='lista'),
    path('actualizar/<int:pk>',RegistroLimpiezaEquipoUpdateView.as_view(),name='actualizar'),
    path('seleccionar/<str:pk>',RegistroLimpiezaEquipoSeleccionView.as_view(),name='seleccionar'),
    path('eliminar/<int:pk>',RegistroLimpiezaEquipoDeleteView.as_view(),name='eliminar'),
    path('excel',RegistroLimpiezaEquipoExcel.as_view(),name='excel'),
    path('probar/<str:string>',probando,name='probar'),
],'limpiezaequipo')

produccion_patterns = ([
    path('', produccionlista.as_view(), name='lista'),
    path('agregar/<int:pauta_id>', produccionagregar.as_view(), name='agregar'),
    path('detalle/<int:pauta_id>',producciondetalle.as_view(),name='detalle'),
    path('modificar/<int:pauta_id>',ProduccionModificarView.as_view(),name='modificar'),

], 'elaboraciones')

calidad_patterns = ([
    path('utensiliolimpieza/',include(utensilioLimpieza_patterns)),
    path('limpiezaequipo/',include(limpiezaEquipo_patterns)),
    path('grupos/',include(grupo_patterns)),
    path('elaboraciones/',include(produccion_patterns)),

],'calidad')

