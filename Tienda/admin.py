from django.contrib import admin
from .models import CategoriaProducto, Producto, LineaFactura, Factura

admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(LineaFactura)
admin.site.register(Factura)
