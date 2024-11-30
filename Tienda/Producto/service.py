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
        if fotografia == None:
            fotografia = 'productos/defaultImage.jpeg'
        categoria = CategoriaProducto.objects.get(id=data.get('categoria'))
        producto = Producto(
            nombre=data.get('nombre'),
            categoria=categoria,
            precio=float(data.get('precio')),
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

    @staticmethod
    def crear_categoria_de_producto(data):
        categoriaproducto = CategoriaProducto(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
        )
        categoriaproducto.save()
        return categoriaproducto.to_dict()
    

    @staticmethod
    def actualizar_categoria_de_producto(cateogira_producto_id, data):
        cateogriaDeProducto = get_object_or_404(CategoriaProducto, id=cateogira_producto_id)
        cateogriaDeProducto.nombre = data.get('nombre', cateogriaDeProducto.nombre)
        cateogriaDeProducto.descripcion = data.get('descripcion', cateogriaDeProducto.descripcion)
        cateogriaDeProducto.save()
        return cateogriaDeProducto.to_dict()


    @staticmethod
    def eliminar__categoria_de_producto(categoria_de_producto_id):
        producto = get_object_or_404(CategoriaProducto, id=categoria_de_producto_id)
        producto.delete()
        return {"mensaje": "Categoría de producto eliminada correctamente"}


    @staticmethod
    def listar_categorias_de_productos():
        categorias = CategoriaProducto.objects.all()
        return [categoria.to_dict() for categoria in categorias]



