from django.db import models

from django.db import models
from django.contrib.auth.models import User
import uuid


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
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name="productos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    fotografia = models.ImageField(upload_to='productos/')

    def str(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre, 
            "categoria": self.categoria.to_dict(),
            "precio": self.precio,
            "stock": self.stock,
            "descripcion": self.descripcion,
            "fotografia": str(self.fotografia)
        }
    
class Factura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="facturas")
    numero_factura = models.CharField(unique=True, max_length=12)
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
    
    def save(self, *args, **kwargs):
        if not self.numero_factura:
            self.numero_factura = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def precio_total(self):
        return sum(map(lambda linea: linea.precio_linea() ,self.lineas_factura.all()))
    
    def __str__(self):
        return f"Factura {self.id}"
    
    def to_dict(self):
        return {
            "numero_factura": self.numero_factura, 
            "fecha_pedido": self.fecha_pedido,
            "fecha_salida": self.fecha_salida,
            "fecha_entrega": self.fecha_entrega,
            "direccion": self.direccion,
            "estado": self.estado,
            "metodo_de_pago": self.metodo_de_pago,
            "coste_envio": self.coste_envio,
            "precio_total": self.precio_total()
        }


class LineaFactura(models.Model):
    
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="lineas_factura", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __ini__(self, factura, producto, cantidad):
        self.factura = factura
        self.producto = producto
        self.cantidad = cantidad
        
    def precio_linea(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Factura {self.factura.id}"
    
    def to_dict(self):
        return {
            "factura": self.factura.to_dict(), 
            "producto": self.producto.to_dict(),
            "cantidad": self.cantidad
        }


