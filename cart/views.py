from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from Tienda.models import Producto

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id, llevar_a_carrito):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            producto=product,
            cantidad=cd["cantidad"] if cd["cantidad"] != None else 1,
            sobreescribir_cantidad=cd["sobreescribir"],
        )
    if llevar_a_carrito == 0:
        return redirect('/')
    else:
        return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Producto, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'cantidad': item['cantidad'], 'sobreescribir': True}
        )
        
    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
        },
    )
