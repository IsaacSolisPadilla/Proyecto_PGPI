from django.db import migrations
from datetime import datetime

def agregar_datos_prueba(apps, schema_editor):
    CategoriaProducto = apps.get_model("Tienda", "CategoriaProducto")
    Producto = apps.get_model("Tienda", "Producto")
    Pedido = apps.get_model("Tienda", "Pedido")
    LineaFactura = apps.get_model("Tienda", "LineaFactura")
    Factura = apps.get_model("Tienda", "Factura")
    User = apps.get_model("auth", "User")

    # Crear categorías de productos
    categoria_velas = CategoriaProducto.objects.create(nombre="Velas", descripcion="Velas aromáticas")
    categoria_cristales = CategoriaProducto.objects.create(nombre="Cristales", descripcion="Cristales de sanación")

    # Crear productos
    producto1 = Producto.objects.create(nombre="Vela de Lavanda", descripcion="Relajante", precio=5.99, categoria=categoria_velas, stock=100)
    producto2 = Producto.objects.create(nombre="Cristal de Cuarzo", descripcion="Cristal de sanación", precio=15.99, categoria=categoria_cristales, stock=50)

    # Crear un usuario de prueba
    usuario = User.objects.create_user(username="cliente1", password="password123")

    # Crear un pedido
    pedido = Pedido.objects.create(usuario=usuario, fecha=datetime.now(), total=27.97)

    # Crear líneas de factura (agregando productos al pedido)
    linea1 = LineaFactura.objects.create(pedido=pedido, producto=producto1, cantidad=2, precio_unitario=producto1.precio)
    linea2 = LineaFactura.objects.create(pedido=pedido, producto=producto2, cantidad=1, precio_unitario=producto2.precio)

    # Actualizar el total del pedido basado en las líneas de factura
    pedido.total = linea1.cantidad * linea1.precio_unitario + linea2.cantidad * linea2.precio_unitario
    pedido.save()

    # Crear una factura asociada al pedido
    factura = Factura.objects.create(pedido=pedido, fecha_emision=datetime.now(), numero_factura="F12345")

class Migration(migrations.Migration):

    dependencies = [
        ("Tienda", "0001_initial"),  # Asegúrate de que esta dependencia apunta a la migración inicial
    ]

    operations = [
        migrations.RunPython(agregar_datos_prueba),
    ]
