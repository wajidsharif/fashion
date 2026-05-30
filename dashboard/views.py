from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Sum, Q
from products.models import Category, Product, Size, Color
from orders.models import Order
from django.contrib.auth.models import User
from accounts.models import UserProfile


@staff_member_required
def dashboard(request):
    tab = request.GET.get('tab', 'overview')

    categories = Category.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('-created_at')
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')
    orders = Order.objects.all().order_by('-created_at')

    context = {
        'tab': tab,
        'categories': categories,
        'products': products,
        'customers': customers,
        'orders': orders,
        'category_count': categories.count(),
        'product_count': products.count(),
        'customer_count': customers.count(),
        'order_count': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'total_revenue': orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('dashboard:category_add')

        category = Category.objects.create(
            name=name,
            description=description,
            is_active=is_active,
            image=image,
        )
        messages.success(request, f'Category "{category.name}" created.')
        return redirect(reverse('dashboard:main') + '?tab=categories')

    return render(request, 'dashboard/category_form.html', {'category': None})


@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', '')
        category.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            category.image = request.FILES['image']
        category.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect(reverse('dashboard:main') + '?tab=categories')

    return render(request, 'dashboard/category_form.html', {'category': category})


@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = category.name
    category.delete()
    messages.success(request, f'Category "{name}" deleted.')
    return redirect(reverse('dashboard:main') + '?tab=categories')


@staff_member_required
def product_add(request):
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or None
        stock = request.POST.get('stock', 0)
        featured = request.POST.get('featured') == 'on'
        is_available = request.POST.get('is_available') == 'on'
        image = request.FILES.get('image')
        selected_sizes = request.POST.getlist('sizes')
        selected_colors = request.POST.getlist('colors')

        if not name or not price:
            messages.error(request, 'Name and price are required.')
            return redirect('dashboard:product_add')

        product = Product.objects.create(
            name=name,
            category_id=category_id,
            description=description,
            price=price,
            discount_price=discount_price,
            stock=stock,
            featured=featured,
            is_available=is_available,
            image=image,
        )
        if selected_sizes:
            product.sizes.set(Size.objects.filter(id__in=selected_sizes))
        if selected_colors:
            product.colors.set(Color.objects.filter(id__in=selected_colors))

        messages.success(request, f'Product "{product.name}" created.')
        return redirect(reverse('dashboard:main') + '?tab=products')

    return render(request, 'dashboard/product_form.html', {
        'product': None,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
    })


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.category_id = request.POST.get('category', product.category_id)
        product.description = request.POST.get('description', '')
        product.price = request.POST.get('price', product.price)
        product.discount_price = request.POST.get('discount_price') or None
        product.stock = request.POST.get('stock', product.stock)
        product.featured = request.POST.get('featured') == 'on'
        product.is_available = request.POST.get('is_available') == 'on'
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()

        selected_sizes = request.POST.getlist('sizes')
        selected_colors = request.POST.getlist('colors')
        if selected_sizes:
            product.sizes.set(Size.objects.filter(id__in=selected_sizes))
        else:
            product.sizes.clear()
        if selected_colors:
            product.colors.set(Color.objects.filter(id__in=selected_colors))
        else:
            product.colors.clear()

        messages.success(request, f'Product "{product.name}" updated.')
        return redirect(reverse('dashboard:main') + '?tab=products')

    return render(request, 'dashboard/product_form.html', {
        'product': product,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
    })


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f'Product "{name}" deleted.')
    return redirect(reverse('dashboard:main') + '?tab=products')


@staff_member_required
def order_detail(request, pk):
    from urllib.parse import quote
    order = get_object_or_404(Order, pk=pk)

    msg = f"🛍️ *Order #{order.id}*\n\n"
    msg += f"👤 *Customer:* {order.full_name}\n📞 *Phone:* {order.phone}\n📍 *Address:* {order.address}, {order.city}\n"
    msg += f"📦 *Status:* {order.get_status_display()}\n\n*Items:*\n"
    for item in order.items.all():
        details = f" ({item.size}" if item.size else ""
        details += f" | {item.color}" if item.color else ""
        details += ")" if (item.size or item.color) else ""
        msg += f"• {item.product_name}{details} x{item.quantity} - Rs.{item.price}\n"
    msg += f"\n💰 *Total:* Rs.{order.total_amount}"

    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'order_whatsapp_message': msg,
    })


@staff_member_required
def order_invoice(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'dashboard/order_invoice.html', {
        'order': order,
    })


@staff_member_required
def order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()

            if new_status == 'delivered':
                for item in order.items.all():
                    if item.product:
                        product = item.product
                        product.stock = max(0, product.stock - item.quantity)
                        product.save()

            messages.success(request, f'Order #{order.id} status updated to "{order.get_status_display()}".')
    return redirect(reverse('dashboard:main') + '?tab=orders')
