from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Proveedor, Producto
from django.shortcuts import get_object_or_404, render

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
