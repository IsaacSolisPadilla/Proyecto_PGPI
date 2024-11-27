import pytest
from django.urls import reverse
from django.core import mail
import stripe
from Tienda.Factura.views import cancelar_factura, crear_sesion_pago, enviar_email, obtener_factura_por_numero_factura, procesar_pago 
from Tienda.models import Factura, Producto, LineaFactura, CategoriaProducto
from cart.cart import Cart
from django.contrib.auth.models import User

@pytest.mark.django_db
@pytest.fixture
def producto():
    categoria = CategoriaProducto.objects.create(nombre="Categoría Test")
    return Producto.objects.create(nombre="Producto Test", precio=100, categoria=categoria)

@pytest.mark.django_db
@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")

@pytest.mark.django_db
@pytest.fixture
def factura(producto):
    # Remove the user argument if the Factura model does not have a user field
    factura = Factura.objects.create(
        nombre="John",
        apellidos="Doe",
        direccion="Calle Falsa 123",
        email="johndoe@example.com",
        metodo_de_pago="Contrareembolso",
        estado="Pendiente"
    )
    # You can create the related user and link it later if necessary.
    return factura
@pytest.mark.django_db
@pytest.fixture
def factura(producto, user=None):
    # Si no se pasa un usuario, creamos una factura sin usuario
    factura = Factura.objects.create(
        nombre="John",
        apellidos="Doe",
        direccion="Calle Falsa 123",
        email="johndoe@example.com",
        metodo_de_pago="Contrareembolso",
        estado="Pendiente",
        user=user  # Si el usuario es None, se creará sin usuario
    )
    return factura

@pytest.mark.django_db
def test_enviar_email_envia_email_correctamente(client):
    # Crear un producto
    categoria = CategoriaProducto.objects.create(nombre="Categoría Test")
    producto = Producto.objects.create(nombre="Producto Test", precio=100, categoria=categoria)

    # Crear una factura sin usuario
    factura = Factura.objects.create(
        nombre="John",
        apellidos="Doe",
        direccion="Calle Falsa 123",
        email="johndoe@example.com",
        metodo_de_pago="Contrareembolso",
        estado="Pendiente"
    )

    # Crear una sesión activa
    client.session.save()  # Crear y guardar la sesión

    # Llamar a la función de envío de correo
    response = enviar_email(client, factura, factura.email)
    response = obtener_factura_por_numero_factura(client, factura.numero_factura)
