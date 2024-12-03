from .views import ClienteAcuerdoCreateView, ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .views import ClienteLocalListView, ClienteLocalUpdateView, ClienteLocalCreateView, ClienteLocalDeleteView
from django.urls import path, include

cliente_patterns = ([
    path('', ClienteListView.as_view(), name='lista'),
    path('crear', ClienteCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>', ClienteUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', ClienteDeleteView.as_view(), name='eliminar'),
    path('acuerdo/<int:cliente>', ClienteAcuerdoCreateView.as_view(), name='acuerdo')
], 'cliente')

local_patterns = ([
    path('', ClienteLocalListView.as_view(), name='lista'),
    path('crear', ClienteLocalCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>', ClienteLocalUpdateView.as_view(), name='actualizar'),
    path('eliminar/<int:pk>', ClienteLocalDeleteView.as_view(), name='eliminar'),
], 'local')
