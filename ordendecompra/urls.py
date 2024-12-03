from ordendecompra.models import OrdenDeCompra
from django.urls import path, include
from .views import InsumoListViewApi, OrdenCompraDetalleView, OrdenCompraTemplateView, OrdenCompraCreateView, OrdenCompraPdfView, OrdenDeCompraEditarView, OrdenDeCompraEliminar, OrdenDeCompraEliminarArchivo, OrdenDeCompraEtiquetarView, OrdenDeCompraInsumoCodigoView, OrdenDeCompraPagar, OrdenDeCompraRetroceder, OrdenDeCompraValidarView, paso, OrdenDeCompraRecepcionarView, OrdenDeCompraRechazar
from .views import OrdenCompraDividirBultoView

ordencompra_patterns = ([
    path('', OrdenCompraTemplateView.as_view(), name='lista'),
    path('crear', OrdenCompraCreateView.as_view(), name='create'),
    path('pdf/<int:pk>', OrdenCompraPdfView.as_view(), name='pdf'),
    path('paso/<int:pk>', paso, name='paso'),
    path('detalle/<int:pk>', OrdenCompraDetalleView.as_view(), name='detalle'),
    path('etiquetar/<int:pk>', OrdenDeCompraEtiquetarView.as_view(), name='etiquetar'),
    path('etiquetas/<int:pk>', OrdenDeCompraInsumoCodigoView.as_view(), name='etiquetas'),
    path('validar/<int:pk>', OrdenDeCompraValidarView.as_view(), name='validar'),
    path('recepcionar/<int:pk>', OrdenDeCompraRecepcionarView.as_view(), name='recepcionar'),
    path('eliminar/<int:pk>', OrdenDeCompraEliminar.as_view(), name='eliminar'),
    path('eliminara/<int:pk>', OrdenDeCompraEliminarArchivo.as_view(), name='eliminara'),
    path('rechazar/<int:pk>', OrdenDeCompraRechazar.as_view(), name='rechazar'),
    path('pagar/<int:pk>', OrdenDeCompraPagar.as_view(), name='pagar'),
    path('editar/<int:pk>', OrdenDeCompraEditarView.as_view(), name='editar'),
    path('retroceder/<int:pk>', OrdenDeCompraRetroceder.as_view(), name='retroceder'),
    path('insumo/<int:pk>', InsumoListViewApi.as_view(), name='insumoapi'),
    path('dividirbulto/<int:pk>', OrdenCompraDividirBultoView.as_view(), name='dividirbulto'),
], 'ordendecompra')
