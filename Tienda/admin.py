from django.contrib import admin
from .models import CategoriaProducto, Producto, Pedido, LineaFactura, Factura

admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(LineaFactura)
admin.site.register(Factura)
