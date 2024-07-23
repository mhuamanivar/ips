# En admin_panel/urls.py

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('profile/', views.profile_list, name='profile'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('supplier/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('supplier/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('profile/<int:pk>/accept/', views.accept_guarantor, name='accept_guarantor'),
    path('profile/<int:pk>/reject/', views.reject_guarantor, name='reject_guarantor'),
    # Agrega más URLs según sea necesario para los otros modelos (productos, proveedores, órdenes, etc.)
]
