from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('register/', views.register_view, name='register'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
