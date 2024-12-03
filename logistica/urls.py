from django.urls import path, include
from .views import EnvioCreateView, EnvioDeleteView, EnvioDetailView, EnvioEtiquetasView, EnvioListView, EnvioRecepcionarListView, EnvioRecepcionarView, EnvioRetrocederView, MisRutasView, PalletCodigoView, PalletCreateView, PalletDeleteView, PalletListView, PalletUpdateView, RutaCerrarView, RutaCreateView, RutaDeleteView, RutaDetailView, RutaListView, RutaSeguimientoView, RutaUpdateView

envio_patterns = ([
    path('', EnvioListView.as_view(), name="lista"),
    path('crear', EnvioCreateView.as_view(), name='crear'),
    path('recepcionar', EnvioRecepcionarListView.as_view(), name='recepcion'),
    path('recepcionar/<int:pk>', EnvioRecepcionarView.as_view(), name='recepcionar'),
    path('eliminar/<int:pk>', EnvioDeleteView.as_view(), name='eliminar'),
    path('detalle/<int:pk>', EnvioDetailView.as_view(), name='detalle'),
    path('etiquetas/<int:pk>', EnvioEtiquetasView.as_view(),name='etiquetas'),
    path('retroceder/<int:pk>', EnvioRetrocederView.as_view(),name='retroceder'),
], 'envios')

ruta_patterns = ([
    path('', RutaListView.as_view(), name='lista'),
    path('crear', RutaCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>', RutaUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', RutaDeleteView.as_view(), name='eliminar'),
    path('misrutas/', MisRutasView.as_view(), name='misrutas'),
    path('seguimiento/<int:pk>', RutaSeguimientoView.as_view(), name='seguimiento'),
    path('detalle/<int:pk>', RutaDetailView.as_view(), name='detalle'),
    path('cerrar/<int:pk>', RutaCerrarView.as_view(), name='cerrar'),
], 'rutas')

pallet_patterns = ([
    path('', PalletListView.as_view(), name='lista'),
    path('agregar', PalletCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>', PalletUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', PalletDeleteView.as_view(), name='eliminar'),
    path('codigo/<int:pk>', PalletCodigoView.as_view(), name='codigo')
], 'pallet')

logistica_patterns = ([
    path('envios/', include(envio_patterns)),
    path('pallets/', include(pallet_patterns)),
    path('rutas/', include(ruta_patterns))
], 'logistica')
