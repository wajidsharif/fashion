from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min, Max
from django.conf import settings
from .models import Product, Category, Size, Color


def shop_view(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    selected_category = request.GET.get('category')
    selected_size = request.GET.get('size')
    selected_color = request.GET.get('color')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '-created_at')
    search_query = request.GET.get('q', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if selected_size:
        products = products.filter(sizes__code=selected_size)

    if selected_color:
        products = products.filter(colors__code=selected_color)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    valid_sorts = {
        'price': 'price',
        '-price': '-price',
        'name': 'name',
        '-name': '-name',
        '-created_at': '-created_at',
        'created_at': 'created_at',
    }
    sort_field = valid_sorts.get(sort_by, '-created_at')
    products = products.order_by(sort_field)

    price_range = Product.objects.filter(is_available=True).aggregate(
        min_price=Min('price'), max_price=Max('price')
    )

    context = {
        'products': products,
        'categories': categories,
        'sizes': sizes,
        'colors': colors,
        'selected_category': selected_category,
        'selected_size': selected_size,
        'selected_color': selected_color,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'sort_by': sort_by,
        'search_query': search_query,
        'price_range': price_range,
    }
    return render(request, 'products/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
        'whatsapp_number': settings.WHATSAPP_NUMBER,
    }
    return render(request, 'products/product_detail.html', context)
