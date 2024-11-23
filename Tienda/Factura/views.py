import json
from typing import List
import stripe
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from Tienda.models import Factura, LineaFactura, Producto
from Tienda.forms import AdminFormFactura, FormFactura
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail

def agregar_producto_a_factura(request, producto_id):
    if request.method == "POST":
        cantidad = 1
        if not producto_id:
            return JsonResponse({"error": "No se especificó el producto"}, status=400)
        print(producto_id)
        producto = get_object_or_404(Producto, id=producto_id)

        if producto.stock < cantidad:
            return JsonResponse({"error": "Stock insuficiente para este producto"}, status=400)

        # Busca una factura pendiente asociada al usuario
        factura, creada = Factura.objects.get_or_create(
            usuario=request.user,
            estado="Espera",
            defaults={
                "direccion": "",  # Puedes definir valores predeterminados
                "metodo_de_pago": "Contrareembolso",  # O cambiarlo según corresponda
            },
        )

        # Intenta obtener una línea de factura existente para el producto
        linea_factura, creada_linea = LineaFactura.objects.get_or_create(
            factura=factura,
            producto=producto,
            defaults={"cantidad": cantidad},
        )

        if not creada_linea:
            # Si la línea ya existe, actualiza la cantidad
            nueva_cantidad = linea_factura.cantidad + cantidad
            if producto.stock < nueva_cantidad:
                return JsonResponse({"error": "Stock insuficiente para la cantidad solicitada"}, status=400)
            linea_factura.cantidad = nueva_cantidad
            linea_factura.save()

        # Actualiza el stock del producto
        producto.stock -= cantidad
        producto.save()

        return JsonResponse({"message": "Producto añadido a la factura correctamente"}, status=200)

    return JsonResponse({"error": "Método no permitido"}, status=405)

# def actualizar_factura(request):
    
#     if(request.method == "PUT"):
#         body = json.loads(request.body)
#         factura = None
#         if request.user != None:
#             factura = request.user.facturas.filter(estado="Espera").first()
#         else:
#             factura = request.user.facturas.filter(numero_factura=1).first()
#         if factura == None:
#             return redirect("/")
#         lineas_factura: List[LineaFactura] = factura.lineas_factura.all()
#         producto_id_linea = dict()

#         # Eliminación de productos
#         for ln in lineas_factura:
#             if str(ln.producto.id) not in body["lineas_factura"].keys():
#                 print(1)
#                 ln.delete()
#             else:
#                 producto_id_linea[str(ln.producto.id)] = ln

#         # Se actualizan los demás casos
#         lineas_factura_body = body["lineas_factura"]
#         for new_id in lineas_factura_body.keys():
#             linea_factura = producto_id_linea[str(new_id)]
#             if linea_factura.cantidad != lineas_factura_body[new_id]:
#                 linea_factura.cantidad = lineas_factura_body[new_id]
#                 linea_factura.save()

#         return JsonResponse({"message": "Datos recibidos correctamente"}, status=200)
    
def obtener_factura_por_numero_factura(request, numero_factura):
    print(numero_factura)
    print(Factura.objects.filter(numero_factura=numero_factura).first())
    return JsonResponse({"estado_factura": get_object_or_404(Factura, numero_factura=numero_factura).estado} ,status=200)

# def obtener_factura_espera(request):
#     print("-"*100)
#     print(request.GET.get("num_factura"))
#     print("-"*100)
#     factura = None
#     if request.user != None:
#         factura = request.user.facturas.filter(estado="Espera").first()
#     else:
#         factura = request.user.facturas.filter(numero_factura=1).first()

#     if factura is None:
#         return JsonResponse({})
#     ls = {i:value for i, value in enumerate(map(lambda x: x.to_dict(), list(factura.lineas_factura.all())))}
#     return JsonResponse(ls)
 
def confirmar_factura(request):
    form = FormFactura(request.POST)
    if(request.method == "POST" and form.is_valid()):
        print(form.fields)
        return None
    
    factura = None
    # TODO: ahora se debe coger el carrito
    # if request.user != None:
    #     factura = request.user.facturas.filter(estado="Espera").first()
    # else:
    #     factura = request.user.facturas.filter(numero_factura=1).first()
    if factura == None:
        return redirect("/")
    
    return render(
        request,
        'crear_factura.html',
        {
            'lineas': factura.lineas_factura.all() if factura != None else [], 
            'precio_total': factura.precio_total(),
            'form': FormFactura()
        }
    )

# En la vista que genera la sesión de pago de Stripe

def crear_sesion_pago(request):
    # TODO: mirar que modificar aquí
    if request.user is not None:
        factura = request.user.facturas.filter(estado="Espera").first()
    else:
        factura = request.user.facturas.filter(numero_factura=1).first()

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
        success_url=request.build_absolute_uri('/procesar_pago/?session_id={CHECKOUT_SESSION_ID}'),  # Redirige a esta URL
        cancel_url=request.build_absolute_uri('/'),  # URL de cancelación
    )

    # Redirige al usuario a la URL de la sesión de Stripe Checkout
    return HttpResponseRedirect(session.url)

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
    
def procesar_pago(request):
    session_id = request.GET.get('session_id')
    stripe.api_key = 'sk_test_51Q2XBLRr6L8GxbwMtP9iKtu8hChihr12m1xHEGoTlGRQSZYCHR8APCuH2T2vA454IoYMwRBMEit7V9MxfSpOZouT00Re1Yl42n'
    try:
        # Obtener los detalles de la sesión de pago desde Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Verifica si el pago fue exitoso
        if session.payment_status == 'paid':
            # Obtener la información del cliente (correo, etc.)
            customer_email = session.customer_email
            
            # Aquí debes buscar la factura del usuario que ha sido pagada
            # TODO: Mirar que hacer aquí
            # if request.user is not None:
            #     factura = request.user.facturas.filter(estado="Espera").first()
            # else:
            #     factura = request.user.facturas.filter(numero_factura=1).first()

            # Contenido del correo
            subject = "Factura de tu compra"
            message = message = f"""
                Hola {factura.nombre} {factura.apellidos},

                Gracias por tu compra. El precio total de tu factura es {factura.precio_total()} EUR.

                Aquí están los detalles de tu pedido:

                - Número de factura: {factura.numero_factura}
                - Fecha del pedido: {factura.fecha_pedido.strftime('%d/%m/%Y %H:%M:%S')}
                - Fecha de salida: {factura.fecha_salida.strftime('%d/%m/%Y %H:%M:%S') if factura.fecha_salida else 'No disponible'}
                - Fecha de entrega: {factura.fecha_entrega.strftime('%d/%m/%Y %H:%M:%S') if factura.fecha_entrega else 'No disponible'}
                - Dirección de envío: {factura.direccion}

                Gracias por confiar en nosotros. Si tienes alguna pregunta, no dudes en contactarnos.

                Saludos,
                El equipo de tu tienda
            """

            # Enviar el correo
            send_mail(
                subject,
                message,
                'eduroblesrusso82@gmail.com',  # Dirección del remitente
                [customer_email],  # Dirección del destinatario
                fail_silently=False,
            )

            return HttpResponse("Pago completado y correo enviado.")
        else:
            return HttpResponse("El pago no se completó correctamente.")
    
    except stripe.error.StripeError as e:
        return HttpResponse(f"Hubo un error al procesar el pago: {str(e)}")

