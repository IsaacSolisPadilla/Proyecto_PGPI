"""
URL configuration for Proyecto_PGPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('facturas/crear', views.crear_factura, name='crear_pedido'),
    path('factura', views.obtener_factura),
    path('', views.pagina_principal, name='pagina_principal'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register')
]
