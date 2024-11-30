import json
import re
from typing import List
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.shortcuts import render

from cart.cart import Cart
from .models import CategoriaProducto, Datos, Producto, Factura, LineaFactura
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .Producto.service import ProductoService
# from .forms import PedidoCreateForm

def pagina_principal(request):
    return render(request, 'pagina_principal.html')

def ver_carrito(request):
    return render(request, 'carrito.html')

def lista_categorias(request):
    categorias = CategoriaProducto.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def lista_productos(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    return render(request, 'Productos/lista_productos.html', {'productos': productos, 'categorias': categorias})

def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'lista_facturas.html', {'facturas': facturas})

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Buscar usuario por correo electrónico
            user = User.objects.get(email=email)
            username = user.username  # Obtenemos el username asociado al email
        except User.DoesNotExist:
            messages.error(request, 'El correo electrónico no está registrado.')
            return redirect('login')

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.facturas.filter(is_draft_mode=True).delete()
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('/')  # Redirige a la página principal
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')

    return render(request, 'login/login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validar campos vacíos
        if not first_name or not last_name or not email or not username or not password or not confirm_password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('register')

        if not re.match(r"^[\w.@+-]+\Z", username):
            messages.error(request, 'El nombre de usuario puede contener únicamente letras, números y los caracteres @/./+/-/_') 
            return redirect('register')
        
        # Validar si el correo electrónico ya existe
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está en uso.')
            return redirect('register')

        # Validar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')

        # Validar contraseñas
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        user.save()
        Datos.objects.create(user=user)
        # Iniciar sesión automáticamente después del registro
        login(request, user)

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('/')

    return render(request, 'login/register.html')

def pagina_principal(request):
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    return render(request, 'pagina_principal.html', {'productos': productos, 'categorias': categorias})
 # O donde sea que esté implementada la lógica del carrito

def cart_count_view(request):
    cart = Cart(request)
    return JsonResponse({"cart_count": len(cart)})
