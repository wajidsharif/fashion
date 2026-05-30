from django.contrib import admin
from .models import Category, Product, ProductImage, Size, Color


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ['name']}
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'featured', 'is_available', 'created_at']
    list_filter = ['featured', 'is_available', 'category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
    list_editable = ['featured', 'is_available', 'stock', 'price', 'discount_price']
    inlines = [ProductImageInline]
    filter_horizontal = ['sizes', 'colors']
    fieldsets = [
        ('Basic Information', {'fields': ['category', 'name', 'slug', 'description']}),
        ('Pricing', {'fields': ['price', 'discount_price']}),
        ('Inventory', {'fields': ['stock', 'sizes', 'colors', 'image']}),
        ('Status', {'fields': ['featured', 'is_available']}),
    ]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary']
    list_filter = ['is_primary']
