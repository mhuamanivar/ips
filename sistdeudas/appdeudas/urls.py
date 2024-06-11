from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('hello/<str:username>', views.hello),
    path('proveedores/', views.proveedores),
    path('productos/', views.productos),
    path('pedidos/', views.pedidos),
]