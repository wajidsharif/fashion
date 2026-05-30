from urllib.parse import quote
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderItem
from cart.utils import get_cart_items, get_cart


def checkout(request):
    items, total = get_cart_items(request)

    if not items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = total
            order.save()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item.get('size', ''),
                    color=item.get('color', ''),
                    subtotal=item['subtotal'],
                )

            whatsapp_url = generate_whatsapp_url(order)

            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, 'Order placed successfully!')
            return render(request, 'orders/order_success.html', {
                'order': order,
                'whatsapp_url': whatsapp_url,
            })
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name()
            if hasattr(request.user, 'profile'):
                initial['phone'] = request.user.profile.mobile
                initial['address'] = request.user.profile.address
                initial['city'] = request.user.profile.city
        form = OrderForm(initial=initial)

    context = {
        'form': form,
        'cart_items': items,
        'cart_total': total,
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    return render(request, 'orders/checkout.html', context)


def generate_whatsapp_url(order):
    number = settings.WHATSAPP_NUMBER
    message = f"🛍️ *New Order #{order.id}*\n\n"
    message += f"👤 *Customer:* {order.full_name}\n"
    message += f"📞 *Phone:* {order.phone}\n"
    message += f"📍 *Address:* {order.address}, {order.city}\n\n"
    message += "*📦 Order Details:*\n"

    for item in order.items.all():
        message += f"• {item.product_name}"
        if item.size:
            message += f" (Size: {item.size})"
        if item.color:
            message += f" (Color: {item.color})"
        message += f" x{item.quantity} - Rs.{item.price}\n"

    message += f"\n💰 *Total Amount:* Rs.{order.total_amount}\n"
    message += f"📝 *Notes:* {order.notes or 'N/A'}\n\n"
    message += "Thank you for your order! 🙏"

    encoded_message = quote(message)
    return f"https://wa.me/{number}?text={encoded_message}"
