from django.shortcuts import render

from django.shortcuts import render
from .models import CategoriaProducto, Producto, Pedido
from django.contrib.auth.models import User

def lista_categorias(request):
    categorias = CategoriaProducto.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

