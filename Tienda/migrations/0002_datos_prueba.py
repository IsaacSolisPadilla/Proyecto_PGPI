from django.db import migrations

def crear_datos_prueba(apps, schema_editor):
    CategoriaProducto = apps.get_model("Tienda", "CategoriaProducto")
    Producto = apps.get_model("Tienda", "Producto")
    
    # Crear categorías de productos
    categoria1 = CategoriaProducto.objects.create(nombre="Velas", descripcion="Velas aromáticas")
    categoria2 = CategoriaProducto.objects.create(nombre="Cristales", descripcion="Cristales de sanación")

    # Crear productos
    Producto.objects.create(nombre="Vela de Lavanda", descripcion="Relajante", precio=5.99, categoria=categoria1, stock=100)
    Producto.objects.create(nombre="Cristal de Cuarzo", descripcion="Cristal de sanación", precio=15.99, categoria=categoria2, stock=50)

class Migration(migrations.Migration):

    dependencies = [
        ("Tienda", "0001_initial"),  # Ajusta al nombre de tu migración inicial
    ]

    operations = [
        migrations.RunPython(crear_datos_prueba),
    ]
