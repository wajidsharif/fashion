from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'product_name', 'price', 'quantity', 'size', 'color', 'subtotal']
    can_delete = False
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'city', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'city', 'created_at']
    search_fields = ['full_name', 'phone', 'id']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['total_amount', 'created_at', 'updated_at']
    fieldsets = [
        ('Customer Information', {'fields': ['full_name', 'phone', 'address', 'city', 'notes']}),
        ('Order Information', {'fields': ['total_amount', 'status']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price', 'subtotal']
    list_filter = ['order']
