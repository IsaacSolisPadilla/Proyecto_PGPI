import stripe
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from Tienda.models import Factura, LineaFactura, Producto
from Tienda.forms import AdminFormFactura, FormFactura
from django.contrib.auth.decorators import user_passes_test
import requests
from cart.cart import Cart

# Modificación de facturas para cambiar el estado de la factura por parte de admin
@user_passes_test(lambda u: u.is_superuser)
def modificar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        data = request.POST.copy()
        data['metodo_de_pago'] = factura.metodo_de_pago  # Forzar el valor original
        form = AdminFormFactura(request.POST, instance=factura)
        if form.is_valid():
            form.save()
        return redirect('/facturas')
    else:
        form = AdminFormFactura(instance=factura, is_disable=True)
        return render(request, 'factura.html', {"form": form})
    

def obtener_factura_por_numero_factura(request, numero_factura):
    return JsonResponse({"estado_factura": get_object_or_404(Factura, numero_factura=numero_factura).estado} ,status=200)

def confirmar_factura(request):
    cart = Cart(request)
    if(request.method == "POST"):
        if len(cart) > 0:
            form = FormFactura(request.POST)
            if form.is_valid():
                factura = Factura()
                data = request.POST.copy()
                if request.user != None and not request.user.is_anonymous:
                    request.user.facturas.filter(is_draft_mode=True).delete()
                    factura.usuario = request.user
                factura.nombre = data["nombre"]
                factura.apellidos = data["apellidos"]
                factura.direccion = data["direccion"]
                factura.email = data["email"]
                factura.metodo_de_pago = data["metodo_de_pago"]
                factura.estado = "Pendiente"
                factura.forma_entrega = data["forma_entrega"]
                factura.save()
                for item in cart:
                    linea_factura = LineaFactura()
                    linea_factura.factura = factura
                    linea_factura.producto = item["producto"]
                    linea_factura.cantidad = item["cantidad"]
                    linea_factura.precio_unitario = item["producto"].precio
                    linea_factura.save()
                
                return enviar_email(request, factura, factura.email) if factura.metodo_de_pago == "Contrareembolso" else crear_sesion_pago(request, factura)
            return redirect("/factura/confirmar")
        else:
            return redirect("/cart")
    else:
        form = FormFactura(user=request.user)
        return render(request,'crear_factura.html',{'form': form, "cart":cart})

def html_de_factura(factura):
    listado_productos_html = """
    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr style="background-color: #f8f8f8; text-align: left; border-bottom: 2px solid #ddd;">
                <th style="padding: 8px; border-bottom: 1px solid #ddd;">Cantidad</th>
                <th style="padding: 8px; border-bottom: 1px solid #ddd;">Producto</th>
                <th style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">Precio</th>
                <th style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">Total</th>
            </tr>
        </thead>
        <tbody>
    """
    for ln in factura.lineas_factura.all():
        cantidad, producto = ln.cantidad, ln.producto
        listado_productos_html += f"""
        <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{cantidad}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{producto.nombre}</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{producto.precio} €</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">{ln.precio_linea()} €</td>
        </tr>
        """
    listado_productos_html += """
        </tbody>
    </table>
    """
    return listado_productos_html

# Cambiar para que se mande un email con los datos de la factura
def enviar_email(request, factura: Factura, email):
    API_URL = "https://api.mailersend.com/v1/email"
    API_KEY = "mlsn.5064fa8def5d34991649294ce407417438efb5e24978bb8445508bfa1f754369"  # Reemplaza con tu API Key de MailerSend
    factura.is_draft_mode = False
    factura.save()
    listado_productos = ""
    
    for ln in factura.lineas_factura.all():
        cantidad, producto = ln.cantidad, ln.producto
        producto.stock -= cantidad
        listado_productos += f" • {cantidad} {producto.nombre} {producto.precio} {ln.precio_linea()}€\n"
        producto.save()
    
    # Asunto y contenido del correo
    subject = "Factura de tu compra"
    text = f"""
Hola {factura.nombre} {factura.apellidos},

Gracias por tu compra. El precio total de tu factura es {factura.precio_total()}€.

Aquí están los detalles de tu pedido:

- Número de factura: {factura.numero_factura}
- Fecha del pedido: {factura.fecha_pedido.strftime('%d/%m/%Y %H:%M:%S')}
- Dirección de envío: {factura.direccion}

{listado_productos}

Gracias por confiar en nosotros. Si tienes alguna pregunta, no dudes en contactarnos.

Saludos,
El equipo de Aura Arcana
    """
    html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; padding: 20px; background-color: #f9f9f9;">
                <div style="max-width: 600px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <header style="text-align: center; margin-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 20px; color: #333;">Factura de tu compra</h1>
                        <p style="margin: 5px 0; font-size: 16px; color: #333;">Coste Total: {factura.precio_total()} €</p>
                        <p style="margin: 5px 0; font-size: 14px; color: #666;">Número de factura: {factura.numero_factura}</p>
                        <p style="margin: 0; font-size: 14px; color: #666;">Fecha: {factura.fecha_pedido.strftime('%d/%m/%Y %H:%M:%S')}</p>
                    </header>
                    <section>
                        <h2 style="font-size: 18px; color: #333; margin-bottom: 10px;">Detalles del pedido</h2>
                        {html_de_factura(factura)}
                        <p style="margin-top: 10px; font-size: 14px; color: #333;">
                            <strong>Dirección de envío:</strong><br>
                            {factura.direccion}
                        </p>
                        <p style="margin-top: 10px; font-size: 14px; color: #333;">
                            <strong>Nota:</strong> El coste total incluye <strong>10 €</strong> en gastos de envío.
                        </p>
                    </section>
                    <footer style="margin-top: 20px; text-align: center; font-size: 12px; color: #888;">
                        <p>Gracias por confiar en nosotros.</p>
                        <p>El equipo de tu tienda</p>
                    </footer>
                </div>
            </body>
        </html>
        """




    # Configuración del remitente y destinatario
    sender = {
        "email": "mailgun@trial-3zxk54vxdj1gjy6v.mlsender.net",  # Cambia a tu dominio verificado si es necesario
        "name": "Aura Arcana"
    }
    recipients = [{"email": email}]

    # Configuración del correo
    data = {
        "from": sender,
        "to": recipients,
        "subject": subject,
        "text": text,
        "html": html
    }

    # Encabezados de la solicitud
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Enviar la solicitud POST a la API de MailerSend
    try:
        response = requests.post(API_URL, json=data, headers=headers)

        if response.status_code == 202:  # 202 indica que el correo fue aceptado para envío
            print("Correo enviado exitosamente!")
        else:
            print(f"Error al enviar el correo: {response.status_code}")
            print(response.json())  # Detalle del error
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

    # Redirigir a la página principal (opcional)
    cart = Cart(request)
    cart.clear()
    return redirect("/")

# En la vista que genera la sesión de pago de Stripe
def crear_sesion_pago(request, factura: Factura):

    coste = factura.precio_total()
    stripe.api_key = 'sk_test_51Q2XBLRr6L8GxbwMtP9iKtu8hChihr12m1xHEGoTlGRQSZYCHR8APCuH2T2vA454IoYMwRBMEit7V9MxfSpOZouT00Re1Yl42n'

    # Crea la sesión de Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': "Productos",
                },
                'unit_amount': int(coste * 100),  # Convertir a céntimos
            },
            'quantity': 1,
        }],
        mode='payment',
        customer_email=factura.email,
        success_url=request.build_absolute_uri(f'/procesar_pago/{factura.numero_factura}'),  # Redirige a esta URL
        cancel_url=request.build_absolute_uri('/cancelar_factura'),  # URL de cancelación
    )

    factura.session_id_stripe = session.id
    factura.save() 

    # Redirige al usuario a la URL de la sesión de Stripe Checkout
    return HttpResponseRedirect(session.url)

def cancelar_factura(request):
    if request.user.is_anonymous != None and not request.user.is_anonymous:
        request.user.facturas.filter(is_draft_mode=True).delete()
    return redirect("/")
    
def procesar_pago(request, numero_factura):
    factura = Factura.objects.get(numero_factura=numero_factura)
    session_id = factura.session_id_stripe
    stripe.api_key = 'sk_test_51Q2XBLRr6L8GxbwMtP9iKtu8hChihr12m1xHEGoTlGRQSZYCHR8APCuH2T2vA454IoYMwRBMEit7V9MxfSpOZouT00Re1Yl42n'
    try:
        # Obtener los detalles de la sesión de pago desde Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Verifica si el pago fue exitoso
        if session.payment_status == 'paid':
            # Obtener la información del cliente (correo, etc.)
            enviar_email(request, factura, session.customer_email)
        return redirect("/")
    
    except stripe.error.StripeError as e:
        return redirect("/")

