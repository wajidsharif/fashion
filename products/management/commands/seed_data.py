from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product, Size, Color, ProductImage


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Sizes
        sizes_data = [
            ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'),
            ('XL', 'XL'), ('XXL', 'XXL'), ('28', '28'), ('30', '30'),
            ('32', '32'), ('34', '34'), ('36', '36'),
        ]
        sizes = {}
        for name, code in sizes_data:
            size, _ = Size.objects.get_or_create(name=name, code=code)
            sizes[code] = size
        self.stdout.write(f'Created {len(sizes_data)} sizes')

        # Colors
        colors_data = [
            ('Black', '#000000'), ('White', '#FFFFFF'), ('Red', '#FF0000'),
            ('Blue', '#0000FF'), ('Green', '#008000'), ('Navy', '#000080'),
            ('Gray', '#808080'), ('Beige', '#F5F5DC'), ('Pink', '#FFC0CB'),
        ]
        colors = {}
        for name, code in colors_data:
            color, _ = Color.objects.get_or_create(name=name, code=code)
            colors[name.lower()] = color
        self.stdout.write(f'Created {len(colors_data)} colors')

        # Categories
        categories_data = [
            ('Casual Wear', 'casual-wear', 'Everyday casual clothing for comfort and style'),
            ('Formal Wear', 'formal-wear', 'Elegant formal attire for special occasions'),
            ('Summer Collection', 'summer-collection', 'Light and breezy summer fashion'),
            ('Winter Collection', 'winter-collection', 'Warm and cozy winter wear'),
            ('Sports & Active', 'sports-active', 'Activewear for your fitness journey'),
            ('Accessories', 'accessories', 'Complete your look with our accessories'),
        ]
        category_objs = {}
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, slug=slug, defaults={'description': desc})
            category_objs[name] = cat
        self.stdout.write(f'Created {len(categories_data)} categories')

        # Products
        products_data = [
            {
                'name': 'Classic White Shirt',
                'category': 'Formal Wear',
                'description': 'Premium quality white cotton shirt. Perfect for formal occasions and office wear. Features a tailored fit with button-down collar.',
                'price': 2999, 'discount_price': 2499, 'stock': 50, 'featured': True,
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'], 'colors': ['White', 'Black'],
            },
            {
                'name': 'Black Denim Jacket',
                'category': 'Casual Wear',
                'description': 'Classic black denim jacket with a modern slim fit. Made from premium quality denim fabric. Features button closure and chest pockets.',
                'price': 4499, 'discount_price': 3799, 'stock': 30, 'featured': True,
                'sizes': ['S', 'M', 'L', 'XL'], 'colors': ['Black', 'Navy'],
            },
            {
                'name': 'Summer Floral Dress',
                'category': 'Summer Collection',
                'description': 'Beautiful floral print dress perfect for summer days. Lightweight and breathable fabric with an elegant A-line cut.',
                'price': 3999, 'discount_price': 3299, 'stock': 25, 'featured': True,
                'sizes': ['XS', 'S', 'M', 'L'], 'colors': ['Pink', 'White', 'Beige'],
            },
            {
                'name': 'Premium Sneakers',
                'category': 'Sports & Active',
                'description': 'Comfortable and stylish sneakers for everyday wear. Features cushioned sole and breathable mesh upper.',
                'price': 5499, 'discount_price': None, 'stock': 40, 'featured': True,
                'sizes': ['28', '30', '32', '34', '36'], 'colors': ['White', 'Black', 'Gray'],
            },
            {
                'name': 'Wool Blend Sweater',
                'category': 'Winter Collection',
                'description': 'Luxurious wool blend sweater for cold winter days. Soft and warm with ribbed cuffs and hem.',
                'price': 4999, 'discount_price': 4299, 'stock': 20, 'featured': True,
                'sizes': ['S', 'M', 'L', 'XL'], 'colors': ['Gray', 'Navy', 'Black'],
            },
            {
                'name': 'Slim Fit Chinos',
                'category': 'Casual Wear',
                'description': 'Modern slim fit chinos in comfortable stretch cotton. Perfect for smart casual occasions.',
                'price': 3499, 'discount_price': 2999, 'stock': 35, 'featured': False,
                'sizes': ['28', '30', '32', '34', '36'], 'colors': ['Beige', 'Navy', 'Black'],
            },
            {
                'name': 'Leather Belt',
                'category': 'Accessories',
                'description': 'Genuine leather belt with polished buckle. A timeless accessory for any wardrobe.',
                'price': 1999, 'discount_price': 1499, 'stock': 60, 'featured': False,
                'sizes': ['S', 'M', 'L', 'XL'], 'colors': ['Black', 'Brown'],
            },
            {
                'name': 'Printed T-Shirt',
                'category': 'Casual Wear',
                'description': 'Comfortable cotton t-shirt with modern print design. Perfect for casual everyday wear.',
                'price': 1499, 'discount_price': 999, 'stock': 100, 'featured': False,
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'], 'colors': ['White', 'Black', 'Gray'],
            },
            {
                'name': 'Blazer - Navy Blue',
                'category': 'Formal Wear',
                'description': 'Elegant navy blue blazer crafted from premium fabric. Single breasted with notch lapel.',
                'price': 8999, 'discount_price': 7499, 'stock': 15, 'featured': False,
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'], 'colors': ['Navy', 'Black'],
            },
            {
                'name': 'Casual Linen Shirt',
                'category': 'Summer Collection',
                'description': 'Breathable linen shirt perfect for hot summer days. Relaxed fit with rolled sleeves.',
                'price': 2799, 'discount_price': 2299, 'stock': 45, 'featured': False,
                'sizes': ['S', 'M', 'L', 'XL'], 'colors': ['White', 'Beige', 'Blue'],
            },
            {
                'name': 'Sports Joggers',
                'category': 'Sports & Active',
                'description': 'High-performance joggers with moisture-wicking fabric. Elastic waistband with drawstring.',
                'price': 2499, 'discount_price': None, 'stock': 55, 'featured': False,
                'sizes': ['S', 'M', 'L', 'XL', 'XXL'], 'colors': ['Black', 'Gray', 'Navy'],
            },
            {
                'name': 'Wool Scarf',
                'category': 'Accessories',
                'description': 'Luxurious wool scarf to keep you warm in style. Soft texture with classic pattern.',
                'price': 1499, 'discount_price': 1199, 'stock': 70, 'featured': False,
                'sizes': [], 'colors': ['Gray', 'Navy', 'Black', 'Red'],
            },
        ]

        for data in products_data:
            cat_name = data.pop('category')
            size_codes = data.pop('sizes', [])
            color_names = data.pop('colors', [])

            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    **data,
                    'category': category_objs[cat_name],
                    'slug': slugify(data['name']),
                }
            )

            for code in size_codes:
                if code in sizes:
                    product.sizes.add(sizes[code])

            for cname in color_names:
                if cname.lower() in colors:
                    product.colors.add(colors[cname.lower()])

        self.stdout.write(self.style.SUCCESS(f'Created {len(products_data)} products'))
        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))
