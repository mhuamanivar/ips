# En admin_panel/urls.py

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('proveedores/', views.proveedores_list, name='proveedores_list'),
    # Agrega más URLs según sea necesario para los otros modelos (productos, proveedores, órdenes, etc.)
]
