from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Proveedor, Producto, Pedido, Cliente
from django.shortcuts import get_object_or_404, render
from .forms import PedidoForm
from django.contrib.auth import login

# Create your views here.
def index(request):
    title = 'Django Course!!'
    return render(request, 'index.html', {
        'title': title,
    })

def hello(request, username):
    return HttpResponse("<h1>Hola %s</h1>" % username)

def about(request):
    username = 'mel'
    return render(request, 'about.html', {
        'username': username,
    })

def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores.html', {
        'proveedores': proveedores,
    })

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {
        'productos': productos,
    })


def pedidos(request):
    pedidos = Pedido.objects.filter(tipo_pedido="C")
    deudas = Pedido.objects.filter(tipo_pedido="D")
    
    print("Pedidos Contado:", pedidos)
    print("Pedidos A crédito:", deudas)
    
    context = {
        'pedidos': pedidos,
        'deudas': deudas,
    }
    return render(request, 'pedidos.html', context)

def nuevo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm()
    return render(request, 'nuevo_pedido.html', {'form': form})