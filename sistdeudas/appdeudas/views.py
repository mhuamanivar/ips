from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Proveedor, Producto, Pedido
from .forms import CrearNuevoPedido

# Create your views here.
def index(request):
    title = 'Django Course!!'
    return render(request, 'index.html')

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
    return render(request, 'productos/productos.html', {
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
    return render(request, 'pedidos/pedidos.html', context)

def nuevo_pedido(request):
    if request.method == 'GET':
        return render(request, 'pedidos/nuevo_pedido.html', {
            'form': CrearNuevoPedido()
        })
    else:
        form = CrearNuevoPedido(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            pedido.productos.set(form.cleaned_data['productos'])
            pedido.save()
            return redirect('pedidos')
        else:
            return render(request, 'nuevo_pedido.html', {
                'form': form
            })

def producto_detalle(request, cod):
    producto = get_object_or_404(Producto, codigo=cod)
    return render(request, 'productos/detalle.html',{
        'producto': producto,
    })
