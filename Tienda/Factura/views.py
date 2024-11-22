import json
from typing import List
import stripe
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from Tienda.models import Factura, LineaFactura, Producto
from Tienda.forms import FormFactura

def actualizar_factura(request):
    
    if(request.method == "PUT"):
        body = json.loads(request.body)
        factura = None
        if request.user != None:
            factura = request.user.facturas.filter(estado="Espera").first()
        else:
            factura = request.user.facturas.filter(numero_factura=1).first()
        if factura == None:
            return redirect("/")
        lineas_factura: List[LineaFactura] = factura.lineas_factura.all()
        producto_id_linea = dict()

        # Eliminación de productos
        for ln in lineas_factura:
            if str(ln.producto.id) not in body["lineas_factura"].keys():
                print(1)
                ln.delete()
            else:
                producto_id_linea[str(ln.producto.id)] = ln

        # Se actualizan los demás casos
        lineas_factura_body = body["lineas_factura"]
        for new_id in lineas_factura_body.keys():
            linea_factura = producto_id_linea[str(new_id)]
            if linea_factura.cantidad != lineas_factura_body[new_id]:
                linea_factura.cantidad = lineas_factura_body[new_id]
                linea_factura.save()

        return JsonResponse({"message": "Datos recibidos correctamente"}, status=200)
    
def obtener_factura_por_numero_factura(request, numero_factura):
    print(numero_factura)
    print(Factura.objects.filter(numero_factura=numero_factura).first())
    return JsonResponse({"estado_factura": get_object_or_404(Factura, numero_factura=numero_factura).estado} ,status=200)

def obtener_factura_espera(request):
    print("-"*100)
    print(request.GET.get("num_factura"))
    print("-"*100)
    factura = None
    if request.user != None:
        factura = request.user.facturas.filter(estado="Espera").first()
    else:
        factura = request.user.facturas.filter(numero_factura=1).first()

    if factura is None:
        return JsonResponse({})
    ls = {i:value for i, value in enumerate(map(lambda x: x.to_dict(), list(factura.lineas_factura.all())))}
    return JsonResponse(ls)
 
def confirmar_factura(request):
    form = FormFactura(request.POST)
    if(request.method == "POST" and form.is_valid()):
        print(form.fields)
        return None
    
    factura = None
    if request.user != None:
        factura = request.user.facturas.filter(estado="Espera").first()
    else:
        factura = request.user.facturas.filter(numero_factura=1).first()
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

def crear_sesion_pago(request):
    if request.user != None:
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
        success_url=request.build_absolute_uri('/'),  # URL de éxito
        cancel_url=request.build_absolute_uri('/'),  # URL de cancelación
    )

    # Redirige al usuario a la URL de la sesión de Stripe Checkout
    return HttpResponseRedirect(session.url)