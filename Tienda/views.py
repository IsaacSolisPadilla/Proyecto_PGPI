import json
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from .models import CategoriaProducto, Producto, Factura, LineaFactura
from django.contrib.auth.models import User
# from .forms import PedidoCreateForm

def pagina_principal(request):
    return render(request, 'pagina_principal.html')
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirige a la página principal o la que prefieras
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'login/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)

        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('/')

    return render(request, 'login/register.html')  # Ruta de la plantilla
