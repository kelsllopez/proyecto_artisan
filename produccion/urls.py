from .views import *
from .views import LoteDeleteView, LoteList, LoteUpdateView, LoteDetailView, LoteCodigoBarraView, LoteMaduracionView
from .views import EnvioView
from django.urls import path,include

pauta_patterns = ([
    path('listapip/', PautaProduccionList.as_view(), name='listapip'),
    path('listalinea/',PautaProduccionListLinea.as_view(),name='listalinea'),

    path('fabricar_pip/',PautaProduccionCreateView.as_view(),name='crear_pip'),
    path('fabricar_linea/',PautaProduccionCreateViewLinea.as_view(),name='crear_linea'),

    path('eliminar/<int:pk>/',PautaProduccionDeleteView.as_view(),name='eliminar'),
    path('detalle/<int:pk>/', PautaDetailView.as_view(),name='detalle'),
    path('actualizar/<int:pk>/',PautaProduccionUpdateView.as_view(),name='actualizar'),

],'pauta')

envio_patterns = ([
    path('',EnvioView.as_view(),name='lista')
],'envio')

lote_patterns = ([
    path('',LoteList.as_view(),name='lista'),
    path('eliminar/<int:pk>/',LoteDeleteView.as_view(),name='eliminar'),
    path('detalle/<int:pk>/estado',LoteUpdateView.as_view(),name='actualizar'),
    path('detalle/<int:pk>/',LoteDetailView.as_view(),name='detalle'),
    path('detalle/<int:pk>/imprimir',LoteCodigoBarraView.as_view(),name='imprimir'),
    path('estado/<int:pk>/eliminar',EstadoLoteDeleteView.as_view(),name='estado-eliminar'),
    path('maduracion/',LoteMaduracionView.as_view(),name="maduracion"),

    path('nivel/', NivelView.as_view(), name="nivel"),
    path('generar-pdf/', GenerarPDFView.as_view(), name='generar_pdf'),


],'lote')

produccion_patterns = ([
    path('pauta/',include(pauta_patterns)),
    path('lote/',include(lote_patterns)),
    path('envio/',include(envio_patterns))
],'produccion')