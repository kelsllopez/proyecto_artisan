"""artisan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from nucleo.urls import nucleo_patterns
from ordendecompra.urls import ordencompra_patterns
from administrador.urls import administrador_patterns
from inventario.urls import inventario_patterns,historial_patterns
from estadisticas.urls import estadisticas_patterns
from produccion.urls import produccion_patterns
from logistica.urls import logistica_patterns
from ventas.urls import ventas_patterns
from perfil.views import LoginQRView
from calidad.urls import calidad_patterns
from perfil.urls import perfil_patterns
from costeo.urls import costeo_patterns
from solicitudes.urls import solicitudes_patterns
from .api import api_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    # Path de auth
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    # Urls del nucleo
    path('', include(nucleo_patterns)),
    # Urls orden de compra
    path('ordendecompra/', include(ordencompra_patterns)),
    path('administrador/', include(administrador_patterns)),
    path('inventario/', include(inventario_patterns)),
    path('estadisticas/', include(estadisticas_patterns)),
    path('calidad/', include(calidad_patterns)),
    path('perfil/', include(perfil_patterns)),
    path('login/<str:identificador>', LoginQRView.as_view(), name='loginqr'),
    path('api/', include(api_patterns)),
    path('produccion/', include(produccion_patterns)),
    path('logistica/', include(logistica_patterns)),
    path('ventas/', include(ventas_patterns)),
    path('historial/',include(historial_patterns)),
    path('costeo/', include(costeo_patterns)),
    path('solicitudes/', include(solicitudes_patterns))
]
