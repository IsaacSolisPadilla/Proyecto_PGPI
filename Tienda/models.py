from django.db import models

from django.db import models
from django.contrib.auth.models import User
import uuid

class CustomUser(User):
    direccion = models.CharField(max_length=100)

class DatosEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

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
    numero_pedido = models.CharField(unique=True, max_length=12)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    direccion = models.TextField()
    estado = models.CharField(
        max_length=50,
        choices=[("Pendiente", "Pendiente"), ("Enviado","Enviado") ,("Entregado","Entregado")]
    )
    metodo_de_pago = models.CharField(
        max_length=50,
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")]
    )
    coste_envio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username}"

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            self.numero_pedido = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
class Factura(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)

    def precio_total(self):
        return sum(map(lambda linea: linea.precio_linea() ,LineaFactura.objects.filter(factura=self).all()))
    
    def __str__(self):
        return f"Factura {self.id} para Pedido {self.pedido.id}"

class LineaFactura(models.Model):
    
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="lineas_factura", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def precio_linea(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Pedido {self.factura.pedido.id}"


