import json
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from .models import CategoriaProducto, Producto, Factura, LineaFactura
from django.contrib.auth.models import User
# from .forms import PedidoCreateForm

def lista_categorias(request):
    categorias = CategoriaProducto.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'lista_facturas.html', {'facturas': facturas})

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def obtener_factura(request):
    factura = Factura.objects.get(id=1)
    ls = {i:value for i, value in enumerate(map(lambda x: x.to_dict(), list(factura.lineas_factura.all())))}
    return  JsonResponse(ls)
 
def crear_factura(request):
    if(request.method == "POST"):
        body = request.body
        print("\033[44m")
        print(body)
        print("\033[0m")
        return None
    factura = Factura.objects.get(id=1)
    return render(
        request,
        'crear_factura.html',
        {'lineas': factura.lineas_factura.all() }
    )

