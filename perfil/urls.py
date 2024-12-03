from django.urls import path, include
from .views import PerfilQRView, PerfilUpdateView

perfil_patterns = ([
    path("",PerfilUpdateView.as_view(),name='perfil'),
    path("qr",PerfilQRView.as_view(),name='qr'),
],'perfil')