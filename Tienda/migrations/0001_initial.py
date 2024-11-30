# Generated by Django 5.1.1 on 2024-11-30 15:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DatosEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('metodo_de_pago', models.CharField(blank=True, choices=[('Contrareembolso', 'Contrareembolso'), ('Pasarela', 'Pasarela de pago')], max_length=50, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellidos', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('fecha_entrega', models.DateTimeField(blank=True, null=True)),
                ('direccion', models.TextField()),
                ('is_draft_mode', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado')], max_length=50)),
                ('forma_entrega', models.CharField(choices=[('Presencialmente', 'Presencialmente'), ('Envío', 'Envío')], max_length=50)),
                ('metodo_de_pago', models.CharField(choices=[('Contrareembolso', 'Contrareembolso'), ('Pasarela', 'Pasarela de pago')], max_length=50, null=True)),
                ('session_id_stripe', models.CharField(blank=True, max_length=255, null=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('descripcion', models.TextField(blank=True)),
                ('fotografia', models.ImageField(upload_to='productos/')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='Tienda.categoriaproducto')),
            ],
        ),
        migrations.CreateModel(
            name='LineaFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('factura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lineas_factura', to='Tienda.factura')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tienda.producto')),
            ],
        ),
    ]
