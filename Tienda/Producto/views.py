
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
import stripe
def crear_producto(request):
    if request.method == 'POST':
        data = request.POST
        fotografia = request.FILES.get('fotografia')
        producto = ProductoService.crear_producto(data, fotografia)
        return redirect('/')
    else:
        categorias = CategoriaProducto.objects.all()
        return render(request, 'Productos/crear_producto.html', {'categorias': categorias})

def eliminar_producto(request, producto_id):
    ProductoService.eliminar_producto(producto_id)
    return redirect('pagina_principal')

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

def crear_sesion_pago(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    stripe.api_key = 'sk_test_51Q2XBLRr6L8GxbwMtP9iKtu8hChihr12m1xHEGoTlGRQSZYCHR8APCuH2T2vA454IoYMwRBMEit7V9MxfSpOZouT00Re1Yl42n'

    # Crea la sesión de Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': producto.nombre,
                },
                'unit_amount': int(producto.precio * 100),  # Convertir a céntimos
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),  # URL de éxito
        cancel_url=request.build_absolute_uri('/cancel/'),  # URL de cancelación
    )

    # Redirige al usuario a la URL de la sesión de Stripe Checkout
    return HttpResponseRedirect(session.url)

def success_view(request):
    return render(request, 'Productos/success.html', {"mensaje": "Pago realizado con éxito"})

def cancel_view(request):
    return render(request, 'Productos/cancel.html', {"mensaje": "El pago fue cancelado"})
