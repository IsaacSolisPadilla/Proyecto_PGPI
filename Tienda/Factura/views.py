import json
from typing import List

from django.http import JsonResponse
from django.shortcuts import redirect, render

from Tienda.models import LineaFactura


def actualizar_factura(request):
    if(request.method == "PUT"):
        body = json.loads(request.body)
        factura = request.user.facturas.filter(estado="Pendiente").first()
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
    
def obtener_factura_pendiente(request):
    print(request.user)
    factura = request.user.facturas.filter(estado="Pendiente").first()
    ls = {i:value for i, value in enumerate(map(lambda x: x.to_dict(), list(factura.lineas_factura.all())))}
    return JsonResponse(ls)
 
def confirmar_factura(request):
    if(request.method == "POST"):
        body = json.loads(request.body)
        print("\033[44m")
        print(body)
        print("\033[0m")
        return None
    
    factura = request.user.facturas.filter(estado="Pendiente").first()
    if factura == None:
        return redirect("/")
    return render(
        request,
        'crear_factura.html',
        {'lineas': factura.lineas_factura.all() if factura != None else [], "precio_total": factura.precio_total() }
    )