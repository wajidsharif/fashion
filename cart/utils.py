from decimal import Decimal
from products.models import Product


def get_cart(request):
    cart = request.session.get('cart', {})
    return cart


def set_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def get_cart_count(request):
    cart = get_cart(request)
    return sum(item['quantity'] for item in cart.values())


def get_cart_items(request):
    cart = get_cart(request)
    items = []
    total = Decimal('0.00')

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_available=True)
            price = Decimal(str(item_data['price']))
            subtotal = price * item_data['quantity']
            total += subtotal
            items.append({
                'product': product,
                'size': item_data.get('size', ''),
                'color': item_data.get('color', ''),
                'quantity': item_data['quantity'],
                'price': price,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    return items, total


def add_to_cart(request, product_id, quantity=1, size='', color=''):
    cart = get_cart(request)
    product = Product.objects.get(id=product_id)

    price = float(product.discount_price) if product.has_discount else float(product.price)
    cart_key = str(product_id)

    if cart_key in cart:
        cart[cart_key]['quantity'] += quantity
    else:
        cart[cart_key] = {
            'quantity': quantity,
            'price': price,
            'size': size,
            'color': color,
        }

    set_cart(request, cart)
    return get_cart_count(request)


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart_key = str(product_id)
    if cart_key in cart:
        del cart[cart_key]
    set_cart(request, cart)
    return get_cart_count(request)


def update_cart_quantity(request, product_id, quantity):
    cart = get_cart(request)
    cart_key = str(product_id)

    if cart_key in cart:
        if quantity > 0:
            cart[cart_key]['quantity'] = quantity
        else:
            del cart[cart_key]

    set_cart(request, cart)
    return get_cart_count(request)
