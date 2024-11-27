import pytest
from django.urls import reverse
from Tienda.models import CategoriaProducto, Producto
from django.contrib.auth.models import User

@pytest.fixture
def superuser(db):
    """Crea un usuario superusuario para pruebas."""
    return User.objects.create_superuser(username='admin', password='password', email='admin@test.com')

@pytest.fixture
def categoria(db):
    """Crea una categoría de producto para pruebas."""
    return CategoriaProducto.objects.create(nombre='Electrónica')

@pytest.fixture
def producto(db, categoria):
    """Crea un producto de prueba."""
    return Producto.objects.create(nombre='Laptop', precio=1000, categoria=categoria)

@pytest.fixture
def client_logged_as_superuser(client, superuser):
    """Cliente autenticado como superusuario."""
    client.force_login(superuser)
    return client

# ==== Tests para vistas de productos ====

@pytest.mark.django_db
def test_crear_producto_get(client_logged_as_superuser, categoria):
    """Prueba el acceso GET a la vista crear_producto."""
    url = reverse('crear_producto')  # Asegúrate de que el nombre coincida con tu configuración en urls.py
    response = client_logged_as_superuser.get(url)
    assert response.status_code == 200
    assert 'Productos/crear_producto.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_crear_producto_post(client_logged_as_superuser, monkeypatch):
    """Prueba la creación de un producto mediante POST."""
    def mock_crear_producto(data, fotografia):
        return True  # Simula que el servicio realiza su trabajo correctamente
    
    # Parchea el método `crear_producto` del servicio
    monkeypatch.setattr('Tienda.Producto.service.ProductoService.crear_producto', mock_crear_producto)
    
    url = reverse('crear_producto')
    data = {
        'nombre': 'Nuevo Producto',
        'precio': 2000,
        'categoria': 1,
    }
    response = client_logged_as_superuser.post(url, data=data)
    assert response.status_code == 302  # Redirección tras creación

@pytest.mark.django_db
def test_eliminar_producto(client_logged_as_superuser, producto, mocker):
    """Prueba la eliminación de un producto."""
    mock_eliminar_producto = mocker.patch('Tienda.Producto.service.ProductoService.eliminar_producto')
    url = reverse('eliminar_producto', args=[producto.id])
    response = client_logged_as_superuser.post(url)
    assert response.status_code == 302  # Redirección tras eliminación
    mock_eliminar_producto.assert_called_once_with(producto.id)

@pytest.mark.django_db
def test_actualizar_producto_get(client_logged_as_superuser, producto):
    """Prueba el acceso GET a la vista actualizar_producto."""
    url = reverse('actualizar_producto', args=[producto.id])
    response = client_logged_as_superuser.get(url)
    assert response.status_code == 200
    assert 'Productos/actualizar_producto.html' in [template.name for template in response.templates]
    assert response.context['producto']['id'] == producto.id
