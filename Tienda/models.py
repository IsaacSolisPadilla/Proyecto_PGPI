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
            "precio": str(self.precio).replace(",","."),
            "stock": self.stock,
            "descripcion": self.descripcion,
            "fotografia": self.fotografia
        }
    
class Factura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="facturas", null=True)
    numero_factura = models.CharField(unique=True, max_length=12)
    nombre = models.CharField(max_length=50, null=True)
    apellidos = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    direccion = models.TextField()
    is_draft_mode = models.BooleanField(default=True)
    estado = models.CharField(
        max_length=50,
        choices=[("Pendiente", "Pendiente"), ("Enviado","Enviado") ,("Entregado","Entregado")]
    )
    forma_entrega = models.CharField(
        max_length=50,
        choices=[("Presencialmente", "Presencialmente"), ("Envío","Envío")]
    )
    metodo_de_pago = models.CharField(
        max_length=50,
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")],
        null=True
    )
    COSTE_ENVIO = 10
    session_id_stripe = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo para el session_id de Stripe
    
    def save(self, *args, **kwargs):
        if not self.numero_factura:
            self.numero_factura = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def precio_total(self):
        precio_total = sum(map(lambda linea: linea.precio_linea(), self.lineas_factura.all()))
        if precio_total < 50 and self.forma_entrega == "Envío":
            precio_total += Factura.COSTE_ENVIO
        return precio_total

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
            "forma_entrega": self.forma_entrega,
            "precio_total": self.precio_total(),
            "session_id_stripe": self.session_id_stripe,
            "is_draft_mode": self.is_draft_mode
        }


class Datos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datos", null=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    metodo_de_pago = models.CharField(
        max_length=50,
        choices=[("Contrareembolso", "Contrareembolso"), ("Pasarela","Pasarela de pago")],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"User ID: {self.user} - Location: {self.direccion}"
    
    def to_dict(self):
        return {
            "user": self.user,
            "direccion": self.direccion,
            "metodo_de_pago": self.metodo_de_pago
        }

class LineaFactura(models.Model):
    
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="lineas_factura", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # def __init__(self, factura, producto, cantidad, precio_unitario):
    #     self.factura = factura
    #     self.producto = producto
    #     self.cantidad = cantidad
    #     self.precio_unitario = precio_unitario
        
    def precio_linea(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Factura {self.factura.id}"
    
    def to_dict(self):
        return {
            "factura": self.factura.to_dict(), 
            "producto": self.producto.to_dict(),
            "cantidad": self.cantidad
        }


