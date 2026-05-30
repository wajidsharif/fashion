from products.models import Category
from cart.utils import get_cart_count


def categories_processor(request):
    return {'all_categories': Category.objects.filter(is_active=True)}


def cart_count(request):
    count = get_cart_count(request)
    return {'cart_item_count': count}
