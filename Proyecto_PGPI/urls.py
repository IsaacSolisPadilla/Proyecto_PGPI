from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from Tienda import views
from Tienda.Factura import views as viewsFactura
from Tienda.Producto import views as producto_views
from django.contrib.auth.views import LogoutView
from Tienda.Usuario import views as usuario_views

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('admin/', admin.site.urls),

    path('cart/', include('cart.urls', namespace='cart')),
    path('cart-count/', views.cart_count_view),
 
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('editar-perfil/', usuario_views.edit_profile, name='edit_profile'),
    path('lista-usuarios/', usuario_views.user_list, name='user_list'),
    path('editar-usuario/<int:user_id>/', usuario_views.edit_user, name='edit_user'),
    path('crear-usuario/', usuario_views.create_new_user, name='crear_usuario'),
    path('eliminar_usuario/<int:user_id>/', usuario_views.delete_user, name='delete_user'),

    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('factura/<int:factura_id>/', viewsFactura.modificar_factura, name="factura_admin"),
    path('factura/confirmar', viewsFactura.confirmar_factura, name='crear_pedido'),
    path('factura/numero_factura/<str:numero_factura>', viewsFactura.obtener_factura_por_numero_factura, name='buscar_factura_por_numero'),
    
    # path('crear-sesion-pago/', viewsFactura.crear_sesion_pago, name='crear_sesion_pago'),
    path('cancelar_factura', viewsFactura.cancelar_factura, name='cancelar_factura'),
    path('procesar_pago/<str:numero_factura>', viewsFactura.procesar_pago, name="procesar_pago"),
    
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/<int:producto_id>/', producto_views.detalle_producto, name='detalle_producto'),
    path('productos/crear/', producto_views.crear_producto, name='crear_producto'),
    path('producto/<int:producto_id>/editar/', producto_views.actualizar_producto, name='actualizar_producto'),
    path('productos/<int:producto_id>/eliminar/', producto_views.eliminar_producto, name='eliminar_producto'),

    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/', producto_views.lista_productos_de_categoria, name='lista_productos_categoria'),
    path('categorias/crear/', producto_views.crear_categoria_de_producto, name='crear_categoria'),
    path('categorias/<int:categoria_de_producto_id>/editar/', producto_views.ver_actualizar_categoria_de_producto, name='ver_actualizar_categoria'),
    path('categorias/<int:categoria_de_producto_id>/editado/', producto_views.actualizar_categoria_de_producto, name='actualizar_categoria'),
    path('categorias/<int:categoria_de_producto_id>/eliminar/', producto_views.eliminar_categoria_de_producto, name='eliminar_categoria'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
