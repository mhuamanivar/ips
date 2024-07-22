# En admin_panel/urls.py

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('profile/', views.profile_list, name='profile'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    # Agrega más URLs según sea necesario para los otros modelos (productos, proveedores, órdenes, etc.)
]
