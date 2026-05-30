from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from products.models import Product, Category


def homepage(request):
    featured_categories = Category.objects.filter(is_active=True)[:4]
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    best_sellers = Product.objects.filter(is_available=True).order_by('-stock')[:8]
    context = {
        'featured_categories': featured_categories,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
    }
    return render(request, 'core/homepage.html', context)


def robots_txt(request):
    site_url = getattr(settings, 'SITE_URL', request.build_absolute_uri('/').rstrip('/'))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /cart/",
        "Disallow: /orders/",
        "Allow: /",
        f"Sitemap: {site_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)
