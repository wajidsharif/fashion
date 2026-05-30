from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='main'),

    # Categories
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Products
    path('product/add/', views.product_add, name='product_add'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Orders
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/invoice/', views.order_invoice, name='order_invoice'),
    path('order/<int:pk>/status/', views.order_status, name='order_status'),
]
