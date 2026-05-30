from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .utils import (
    get_cart_items, add_to_cart, remove_from_cart,
    update_cart_quantity, get_cart_count
)
from products.models import Product


def cart_view(request):
    items, total = get_cart_items(request)
    context = {
        'cart_items': items,
        'cart_total': total,
        'cart_count': get_cart_count(request),
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', '')
    color = request.POST.get('color', '')

    product = get_object_or_404(Product, id=product_id, is_available=True)
    count = add_to_cart(request, product_id, quantity, size, color)

    _, total = get_cart_items(request)

    return JsonResponse({
        'success': True,
        'cart_count': count,
        'cart_total': str(total),
        'message': f'{product.name} added to cart!',
    })


@require_POST
def cart_remove(request):
    product_id = request.POST.get('product_id')
    count = remove_from_cart(request, product_id)
    items, total = get_cart_items(request)

    return JsonResponse({
        'success': True,
        'cart_count': count,
        'cart_total': str(total),
    })


@require_POST
def cart_update(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))
    count = update_cart_quantity(request, product_id, quantity)
    items, total = get_cart_items(request)

    item_subtotal = '0.00'
    for item in items:
        if str(item['product'].id) == product_id:
            item_subtotal = str(item['subtotal'])
            break

    return JsonResponse({
        'success': True,
        'cart_count': count,
        'cart_total': str(total),
        'item_subtotal': item_subtotal,
    })
