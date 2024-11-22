from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Tienda import views
from Tienda.Factura import views as viewsFactura
from Tienda.Producto import views as producto_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('factura/confirmar', viewsFactura.confirmar_factura, name='crear_pedido'),
    path('factura/agregar/<int:producto_id>/', viewsFactura.agregar_producto_a_factura, name='agregar_producto_a_factura'),
    path('factura/actualizar', viewsFactura.actualizar_factura, name='actualizar_factura'),
    path('carrito', views.ver_carrito),
    path('factura/espera', viewsFactura.obtener_factura_espera),
    path('', views.pagina_principal, name='pagina_principal'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('productos/<int:producto_id>/', producto_views.detalle_producto, name='detalle_producto'),
    path('crear-sesion-pago/', viewsFactura.crear_sesion_pago, name='crear_sesion_pago'),
    path('productos/crear/', producto_views.crear_producto, name='crear_producto'),
    path('producto/<int:producto_id>/editar/', producto_views.actualizar_producto, name='actualizar_producto'),
    path('productos/<int:producto_id>/eliminar/', producto_views.eliminar_producto, name='eliminar_producto'),

    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', producto_views.crear_categoria_de_producto, name='crear_categoria'),
    path('categorias/<int:categoria_de_producto_id>/editar/', producto_views.actualizar_categoria_de_producto, name='actualizar_categoria'),
    path('categorias/<int:categoria_de_producto_id>/eliminar/', producto_views.eliminar_categoria_de_producto, name='eliminar_categoria'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
