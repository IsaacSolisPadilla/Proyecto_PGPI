from ..models import Producto, CategoriaProducto
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import stripe

class ProductoService:
    @staticmethod
    def listar_productos():
        productos = Producto.objects.all()
        return [producto.to_dict() for producto in productos]

    @staticmethod
    def crear_producto(data, fotografia):
        categoria = CategoriaProducto.objects.get(id=data.get('categoria'))
        producto = Producto(
            nombre=data.get('nombre'),
            categoria=categoria,
            precio=data.get('precio'),
            stock=data.get('stock'),
            descripcion=data.get('descripcion'),
            fotografia=fotografia
        )
        producto.save()
        return producto.to_dict()
    
    @staticmethod
    def actualizar_producto(producto_id, data, fotografia=None):
        # Buscar el producto existente
        producto = get_object_or_404(Producto, id=producto_id)

        # Actualizar los campos del producto
        producto.nombre = data.get('nombre', producto.nombre)
        producto.precio = data.get('precio', producto.precio)
        producto.stock = data.get('stock', producto.stock)
        producto.descripcion = data.get('descripcion', producto.descripcion)

        # Si se proporciona una nueva fotografía, actualizarla
        if fotografia:
            producto.fotografia = fotografia

        # Actualizar la categoría si se proporciona
        if 'categoria' in data:
            categoria = CategoriaProducto.objects.get(id=data.get('categoria'))
            producto.categoria = categoria

        # Guardar los cambios
        producto.save()
        return producto.to_dict()

    @staticmethod
    def eliminar_producto(producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return {"mensaje": "Producto eliminado correctamente"}

