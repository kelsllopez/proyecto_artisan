from rest_framework import routers
from ordendecompra.views import OrdenDeCompraViewset, InsumoListViewApi
from logistica.views import EnvioViewSet, PalletViewSet, PalletRetrieveApi, EnvioRecepcionarListApiView, EnvioRetrieveApiView, EnvioResumenApi, PalletRetrieveScanApi, RutaViewSet
from proveedores.views import ProveedorInsumoViewSet, ProveedorViewSet
from nucleo.views import InsumoViewSet, ProductoViewSet, RamaViewSet
from inventario.views import BodegaViewSet, InventarioViewSet, InventarioProductoPorUbicacion, BultoRetrieveScanApi, BultoViewset, HistorialBodegaViewSet
from pauta.views import PautaViewSet, ColumnaViewSet, PautaElaboracionRetrieve
from usuarios.views import UserViewSet, GroupViewSet
from calidad.views import UtensilioLimpiezaViewSet, EquipoRegistroLimpiezaViewSet, GruposEquiposViewSet
from equipo.views import EquipoViewSet, AreaEquipoViewSet
from django.urls import path, include
from clientes.views import ClienteLocalViewSet, ClienteViewSet, ClienteListApiView, ClienteAvanzadoDetailApiView
from produccion.views import PautaProduccionViewSet, PautaProduccionRetrieveApi, LoteViewSet, LoteRetrieveApi, LoteMaduracionPorProducto, LoteRetrieveScanApi, CajaLoteRetrieveScanApi
from ventas.views import ListaPrecioViewSet, OrdenDeVentaViewSet, OrdenDeVentaPorClienteApiView, APIAbrirCaja
from estado.views import EstadoViewSet, ConjuntoEstadoViewset
from solicitudes.views import SolicitudViewSet

router = routers.DefaultRouter()
router.register('ordendecompra', OrdenDeCompraViewset)
router.register('solicitudes', SolicitudViewSet)
router.register('proveedor', ProveedorInsumoViewSet)
router.register('insumo', InsumoViewSet)
router.register('bodega', BodegaViewSet)
router.register('inventarioinsumo', InventarioViewSet)
router.register('cliente', ClienteViewSet)
router.register('local', ClienteLocalViewSet)
router.register('area', RamaViewSet)
router.register('producto', ProductoViewSet)
router.register('pauta', PautaViewSet)
router.register('columna', ColumnaViewSet)
router.register('usuario', UserViewSet)
router.register('grupo', GroupViewSet)
router.register('equipo', EquipoViewSet)
router.register('utensiliolimpieza', UtensilioLimpiezaViewSet)
router.register('equiporegistrolimpieza', EquipoRegistroLimpiezaViewSet)
router.register('areaequipo', AreaEquipoViewSet)
router.register('pautaproduccion', PautaProduccionViewSet)
router.register('lote', LoteViewSet)
router.register('envio', EnvioViewSet)
router.register('pallet', PalletViewSet)
router.register('listap', ListaPrecioViewSet)
router.register('ordendeventa', OrdenDeVentaViewSet)
router.register('ruta', RutaViewSet)
router.register('bulto', BultoViewset)
router.register('gruposequipos', GruposEquiposViewSet)
router.register('estado',EstadoViewSet)
router.register('conjuntoestado',ConjuntoEstadoViewset)
router.register('historialbodega',HistorialBodegaViewSet)

api_patterns = [
    path('', include(router.urls)),
    path('pauta/detalle/<int:pk>/<int:lugar>', PautaElaboracionRetrieve.as_view(), name='api-pauta-detalle'),
    path('cliente/buscar/<str:nombre>', ClienteListApiView.as_view(), name='api-cliente-buscar'),
    path('cliente/avanzado/<int:pk>', ClienteAvanzadoDetailApiView.as_view(), name='api-cliente-avanzado'),
    path('insumo/detalle/<int:pk>', InsumoListViewApi.as_view(), name='api-insumo-detalle'),
    path('inventarioproducto/<int:rama>/<int:lugar>', InventarioProductoPorUbicacion.as_view(), name='api-producto-por-rama'),
    path('inventario/bultos/<int:pk>', BultoRetrieveScanApi.as_view(), name='api-bulto-scan'),
    path('pautaproduccion/detalle/<int:pk>', PautaProduccionRetrieveApi.as_view(), name='api-pautaproduccion-detalle'),
    path('ordendeventa/detalle/cliente/<int:cliente>', OrdenDeVentaPorClienteApiView.as_view(), name='api-ordenventa-cliente'),
    path('envios/recepcionar/', EnvioRecepcionarListApiView.as_view(), name='api-envio-recepcionar'),
    path('envios/detalle/<int:pk>', EnvioRetrieveApiView.as_view(), name='api-envio-detalle'),
    path('envios/detalle/<int:pk>/resumen', EnvioResumenApi.as_view(), name='api-envio-resumen'),
    path('lote/detalle/<int:pk>', LoteRetrieveApi.as_view(), name='api-lote-detalle'),
    path('pallet/detalle/<int:pk>', PalletRetrieveApi.as_view(), name='api-pallet-detalle'),
    path('pallet/scan/<int:pk>', PalletRetrieveScanApi.as_view(), name='api-pallet-scan'),
    path('lote/maduracion/<int:pk>', LoteMaduracionPorProducto.as_view(), name='api-lote-maduracion'),
    path('lote/scan/<int:pk>', LoteRetrieveScanApi.as_view(), name='api-lote-scan'),
    path('lote/caja/abrir/<int:pk>', APIAbrirCaja.as_view(), name='api-abrir-caja'),
    path('lote/caja/scan/<int:pk>', CajaLoteRetrieveScanApi.as_view(), name='api-cajalote-scan')
]
