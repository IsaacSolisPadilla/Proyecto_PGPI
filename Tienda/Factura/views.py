import stripe
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from Tienda.models import Factura, LineaFactura, Producto
from Tienda.forms import AdminFormFactura, FormFactura
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from cart.cart import Cart

# Modificación de facturas para cambiar el estado de la factura por parte de admin
def modificar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        data = request.POST.copy()
        data['metodo_de_pago'] = factura.metodo_de_pago  # Forzar el valor original
        form = AdminFormFactura(data, instance=factura)
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
                factura.save()
                for item in cart:
                    linea_factura = LineaFactura()
                    linea_factura.factura = factura
                    linea_factura.producto = item["producto"]
                    linea_factura.cantidad = item["cantidad"]
                    linea_factura.precio_unitario = item["producto"].precio
                    linea_factura.save()
                
                return enviar_email(factura, factura.email) if factura.metodo_de_pago == "Contrareembolso" else crear_sesion_pago(request, factura)
            return redirect("/factura/confirmar")
        else:
            return redirect("/cart")
    else:
        form = FormFactura(user=request.user)
        return render(request,'crear_factura.html',{'form': form, "cart":cart})

# Cambiar para que se mande un email con los datos de la factura
def enviar_email(factura, email):
    subject = "Factura de tu compra"
    message = message = f"""
                Hola {factura.nombre} {factura.apellidos},

                Gracias por tu compra. El precio total de tu factura es {factura.precio_total()}€.

                Aquí están los detalles de tu pedido:

                - Número de factura: {factura.numero_factura}
                - Fecha del pedido: {factura.fecha_pedido.strftime('%d/%m/%Y %H:%M:%S')}ç
                - Dirección de envío: {factura.direccion}

                Gracias por confiar en nosotros. Si tienes alguna pregunta, no dudes en contactarnos.

                Saludos,
                El equipo de tu tienda
            """
    print("*"*100)
    print(email)
    print("*"*100)
    send_mail(
                subject,
                message,
                'admin@tienda.com',  # Dirección del remitente
                [email],  # Dirección del destinatario
                fail_silently=False,
            )
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
            enviar_email(factura, session.customer_email)
            return redirect("/")
        else:
            return redirect("/")
    
    except stripe.error.StripeError as e:
        return redirect("/")

