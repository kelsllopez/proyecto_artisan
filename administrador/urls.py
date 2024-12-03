from clientes.views import ClienteCreateView, ClienteDeleteView, ClienteListView, ClienteLocalCreateView, ClienteLocalDeleteView, ClienteLocalListView, ClienteLocalUpdateView, ClienteUpdateView
from django.urls import path, include
from proveedores.views import ProveedorInsumoUpdateView, ProveedorListaView, ProveedorActualizarView,ProveedorCreateView, ProveedorDetalleView, ProveedorBorrarView,ProveedorInsumoCreateView, ProveedorInsumoDeleteView
from nucleo.views import InsumoDeleteView, InsumoListView, InsumoCreateView, InsumoUpdateView, ProductoCreateView, ProductoListView, ProductoUpdateView, ProductodeleteView, RamaCreateView, RamaDeleteView, RamaListView, RamaUpdateView
from inventario.views import BodegaCreateView, BodegaDeleteView, BodegaListView, BodegaUpdateView
from nucleo.urls import insumo_patterns
from nucleo.urls import productos_patterns
from nucleo.urls import areas_patterns
from pauta.urls import pauta_patterns
from usuarios.urls import usuarios_patterns,grupos_patterns
from nucleo.urls import areas_patterns, productos_patterns, insumo_patterns
from proveedores.urls import proveedor_patterns
from inventario.urls import bodega_patterns
from clientes.urls import cliente_patterns,local_patterns
from equipo.urls import equipo_patterns
from estado.urls import estado_patterns
from costeo.urls import costeo_patterns

administrador_patterns = ([
   #Proveedores
   path('proveedores/', include(proveedor_patterns)),
   #Insumo
    path('insumos/', include((insumo_patterns, 'insumo'), namespace='insumo')),
   #Bodegas
   path('bodegas/', include(bodega_patterns)),
   #Clientes
   path('clientes/', include(cliente_patterns)),
   #Costeo
   path('costeo/', include(costeo_patterns)),
   #Locales
   path('locales/', include(local_patterns)),
   #Áreas del negocio
    path('areas/', include((areas_patterns, 'area'), namespace='area')),
   #Productos
    path('productos/', include((productos_patterns, 'producto'), namespace='producto')),
   #Pautas
   path('pautas/', include(pauta_patterns)),
   #Usuarios
   path('usuarios/', include(usuarios_patterns)),
   #Grupos
   path('grupos/', include(grupos_patterns)),
   #Equipo
   path('equipos/', include(equipo_patterns)),
   #Estados
   path('pva/', include(estado_patterns)),
],'administrador')
