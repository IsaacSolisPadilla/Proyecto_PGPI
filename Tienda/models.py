from django.db import models

from django.db import models
from django.contrib.auth.models import User

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name="productos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    fotografia = models.ImageField(upload_to='productos/')

    def str(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username}"

class LineaFactura(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="lineas_factura")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Pedido {self.pedido.id}"

class Factura(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Factura {self.numero_factura} para Pedido {self.pedido.id}"
