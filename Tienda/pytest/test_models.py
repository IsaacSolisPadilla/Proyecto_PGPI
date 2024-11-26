import pytest
from django.contrib.auth.models import User
from Tienda.models import DatosEmpresa, CategoriaProducto, Producto, Factura, LineaFactura, Datos
from decimal import Decimal

@pytest.mark.django_db
def test_datos_empresa_creation():
    # Crear una instancia de DatosEmpresa
    datos_empresa = DatosEmpresa.objects.create(
        nombre="Mi Empresa",
        direccion="Calle Falsa 123",
        telefono="123456789",
        email="contacto@miempresa.com"
    )

    # Verificar que la instancia se crea correctamente
    assert datos_empresa.nombre == "Mi Empresa"
    assert datos_empresa.direccion == "Calle Falsa 123"
    assert datos_empresa.telefono == "123456789"
    assert datos_empresa.email == "contacto@miempresa.com"
    assert str(datos_empresa) == "Mi Empresa"

@pytest.mark.django_db
def test_categoria_producto_creation():
    # Crear una instancia de CategoriaProducto
    categoria = CategoriaProducto.objects.create(
        nombre="Electrónica",
        descripcion="Productos electrónicos"
    )

    # Verificar que la instancia se crea correctamente
    assert categoria.nombre == "Electrónica"
    assert categoria.descripcion == "Productos electrónicos"
    assert str(categoria) == "Electrónica"
    assert categoria.to_dict() == {"nombre": "Electrónica", "descripcion": "Productos electrónicos"}

@pytest.mark.django_db
def test_producto_creation():
    categoria = CategoriaProducto.objects.create(
        nombre="Electrónica", descripcion="Productos electrónicos"
    )

    # Crear una instancia de Producto
    producto = Producto.objects.create(
        nombre="Smartphone",
        categoria=categoria,
        precio=299.99,
        stock=10,
        descripcion="Un smartphone de última generación",
        fotografia="productos/smartphone.jpg"
    )

    # Verificar que la instancia se crea correctamente
    assert producto.nombre == "Smartphone"
    assert producto.categoria == categoria
    assert producto.precio == 299.99
    assert producto.stock == 10
    assert producto.descripcion == "Un smartphone de última generación"
    assert producto.fotografia == "productos/smartphone.jpg"
    assert producto.to_dict()["nombre"] == "Smartphone"

@pytest.mark.django_db
def test_factura_creation():
    user = User.objects.create_user(username="usuario", password="contraseña")

    # Crear una instancia de Factura
    factura = Factura.objects.create(
        usuario=user,
        nombre="Juan",
        apellidos="Pérez",
        email="juanperez@example.com",
        direccion="Calle Falsa 123",
        estado="Pendiente",
        metodo_de_pago="Pasarela",
    )

    # Verificar que la instancia se crea correctamente
    assert factura.usuario == user
    assert factura.nombre == "Juan"
    assert factura.apellidos == "Pérez"
    assert factura.email == "juanperez@example.com"
    assert factura.direccion == "Calle Falsa 123"
    assert factura.estado == "Pendiente"
    assert factura.metodo_de_pago == "Pasarela"
    assert str(factura).startswith("Factura")
    assert factura.to_dict()["estado"] == "Pendiente"
    
    # Verificar que se ha generado un número de factura
    assert len(factura.numero_factura) > 0

@pytest.mark.django_db
def test_factura_precio_total():
    user = User.objects.create_user(username="usuario", password="contraseña")
    categoria = CategoriaProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
    producto = Producto.objects.create(
        nombre="Smartphone",
        categoria=categoria,
        precio=299.99,
        stock=10,
        descripcion="Un smartphone de última generación",
        fotografia="productos/smartphone.jpg"
    )

    factura = Factura.objects.create(
        usuario=user,
        nombre="Juan",
        apellidos="Pérez",
        email="juanperez@example.com",
        direccion="Calle Falsa 123",
        estado="Pendiente",
        metodo_de_pago="Pasarela",
    )

    # Crear una línea de factura
    LineaFactura.objects.create(
        factura=factura,
        producto=producto,
        cantidad=2,
        precio_unitario=producto.precio
    )

    # Verificar que el precio total de la factura es correcto
    assert factura.precio_total() == Decimal('599.98')  # 299.99 * 2

@pytest.mark.django_db
def test_linea_factura_creation():
    categoria = CategoriaProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
    producto = Producto.objects.create(
        nombre="Smartphone",
        categoria=categoria,
        precio=299.99,
        stock=10,
        descripcion="Un smartphone de última generación",
        fotografia="productos/smartphone.jpg"
    )

    factura = Factura.objects.create(
        nombre="Juan",
        apellidos="Pérez",
        email="juanperez@example.com",
        direccion="Calle Falsa 123",
        estado="Pendiente",
        metodo_de_pago="Pasarela",
    )

    # Crear una instancia de LineaFactura
    linea_factura = LineaFactura.objects.create(
        factura=factura,
        producto=producto,
        cantidad=2,
        precio_unitario=producto.precio
    )

    # Verificar que la instancia se crea correctamente
    assert linea_factura.factura == factura
    assert linea_factura.producto == producto
    assert linea_factura.cantidad == 2
    assert linea_factura.precio_unitario == 299.99
    assert linea_factura.precio_linea() == 599.98  # 299.99 * 2
    assert str(linea_factura) == "2 de Smartphone en Factura 1"
    assert linea_factura.to_dict()["cantidad"] == 2

@pytest.mark.django_db
def test_datos_creation():
    user = User.objects.create_user(username="usuario", password="contraseña")

    # Crear una instancia de Datos
    datos = Datos.objects.create(
        user=user,
        direccion="Calle Falsa 123",
        metodo_de_pago="Pasarela"
    )

    # Verificar que la instancia se crea correctamente
    assert datos.user == user
    assert datos.direccion == "Calle Falsa 123"
    assert datos.metodo_de_pago == "Pasarela"
    assert datos.to_dict()["metodo_de_pago"] == "Pasarela"
