from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('proveedores/', views.proveedores, name="proveedores"),
    path('productos/', views.productos, name="productos"),
    path('productos/<str:cod>', views.producto_detalle, name="producto_detalle"),
    path('pedidos/', views.pedidos, name="pedidos"),
    path('nuevo_pedido/', views.nuevo_pedido, name="nuevo_pedido"),
]