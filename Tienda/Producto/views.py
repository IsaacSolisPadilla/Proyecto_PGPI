
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.shortcuts import render
from Tienda.models import CategoriaProducto, Producto, Factura, LineaFactura
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from Tienda.Producto.service import ProductoService
from django.contrib.auth.decorators import user_passes_test
import stripe

@user_passes_test(lambda u: u.is_superuser)
def crear_producto(request):
    if request.method == 'POST':
        data = request.POST
        fotografia = request.FILES.get('fotografia')
        producto = ProductoService.crear_producto(data, fotografia)
        return redirect('/')
    else:
        categorias = CategoriaProducto.objects.all()
        return render(request, 'Productos/crear_producto.html', {'categorias': categorias})

@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    ProductoService.eliminar_producto(producto_id)
    return redirect('pagina_principal')

@user_passes_test(lambda u: u.is_superuser)
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = CategoriaProducto.objects.all()

    if request.method == 'POST':
        data = request.POST
        fotografia = request.FILES.get('fotografia')
        ProductoService.actualizar_producto(producto_id, data, fotografia)
        return redirect('detalle_producto', producto_id=producto.id)  # Cambia la redirección según tu necesidad

    return render(request, 'Productos/actualizar_producto.html', {'producto': producto, 'categorias': categorias})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'Productos/detalle_producto.html', {'producto': producto})

def detalle_carro_pago(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'Productos/carro.html', {'producto': producto})

#=====

@user_passes_test(lambda u: u.is_superuser)
def crear_categoria_de_producto(request):
    if request.method == 'POST':
        data = request.POST
        categoriaProducto = ProductoService.crear_categoria_de_producto(data)
        return redirect('lista_categorias')
    else:
        return render(request, 'Productos/crear_categoria_producto.html')

@user_passes_test(lambda u: u.is_superuser)
def eliminar_categoria_de_producto(request, categoria_de_producto_id):
    ProductoService.eliminar__categoria_de_producto(categoria_de_producto_id)
    return redirect('lista_categorias')

@user_passes_test(lambda u: u.is_superuser)
def actualizar_categoria_de_producto(request, categoria_de_producto_id):
    categoria = get_object_or_404(CategoriaProducto, id=categoria_de_producto_id)

    if request.method == 'POST':
        data = request.POST
        ProductoService.actualizar_categoria_de_producto(categoria_de_producto_id, data)
        return redirect('lista_categorias') 
    else:
        return render(request, 'Productos/actualizar_categoria.html', {'categoria': categoria})

def lista_productos_de_categoria(request, categoria_id):
    # Obtener la categoría o retornar error 404 si no se encuentra
    categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
    # Obtener los productos que pertenecen a esta categoría
    productos = Producto.objects.filter(categoria=categoria)
    # Renderizar la plantilla pasando la categorías
    categorias = CategoriaProducto.objects.all()
    # Renderizar la plantilla pasando la categoría y los productos
    return render(request, 'Productos/lista_productos_categoria.html', {'categorias': categorias, 'categoria': categoria, 'productos': productos})
