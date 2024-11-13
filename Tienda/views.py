from django.shortcuts import render

from django.shortcuts import render
from .models import CategoriaProducto, Producto, Pedido
from django.contrib.auth.models import User

def pagina_principal(request):
    return render(request, 'pagina_principal.html')
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