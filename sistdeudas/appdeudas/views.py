from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Proveedor, Producto, Pedido, Cliente
from .forms import CrearNuevoPedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
            return render(request, 'nuevo_pedido', {
                'form': form
            })

def producto_detalle(request, cod):
    producto = get_object_or_404(Producto, codigo=cod)
    return render(request, 'productos/detalle.html',{
        'producto': producto,
    })

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                Cliente.objects.create(nombre=request.POST['username'],correo=request.POST['username'], contraseña=request.POST['password1'])
                return HttpResponse('Usuario creado satisfactoriamente')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden'
        })
