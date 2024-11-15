from ..models import Producto, CategoriaProducto
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class ProductoService:
    @staticmethod
    def listar_productos():
        productos = Producto.objects.all()
        return [producto.to_dict() for producto in productos]

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
    def eliminar_producto(producto_id):
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return {"mensaje": "Producto eliminado correctamente"}
