# En admin_panel/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_panel'

urlpatterns = [
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('proveedores/', views.proveedores_list, name='proveedores_list'),
    path('productos/', views.productos_list, name='productos_list'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('lista_Usuarios/', views.lista_Usuarios, name='lista_Usuarios'),
    path('assign_superuser/<int:user_id>/', views.assign_superuser, name='assign_superuser'),
    
    # Agrega más URLs según sea necesario para los otros modelos (productos, proveedores, órdenes, etc.)
]
