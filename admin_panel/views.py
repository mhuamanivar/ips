from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from shop.models import Profile, Supplier, Product # Importa los modelos necesarios
from django.contrib import messages
from .models import Business
from .forms import BusinessForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminPermissionForm

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

def proveedores_list(request):
    proveedores = Supplier.objects.all()
    return render(request, 'productores.html', {'proveedores': proveedores})

def productos_list(request):
    productos = Product.objects.all()
    proveedores = Supplier.objects.all()
    return render(request, 'productos.html', {'productos': productos, 'proveedores': proveedores})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'admin_panel/profile_detail.html', {'profile': profile})

@login_required
def nosotros(request):
    try:
        business = Business.objects.get()
    except Business.DoesNotExist:
        messages.error(request, 'El negocio solicitado no existe.')
        return redirect('some_fallback_view')

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'La información de la empresa ha sido actualizada correctamente.')
            return redirect('/')  # Ajusta la redirección según sea necesario
    else:
        form = BusinessForm(instance=business)
    
    context = {
        'form': form
    }
    return render(request, 'empresa.html', context)

@login_required
def lista_Usuarios(request):
    profiles = Profile.objects.all()
    return render(request, 'permisos.html', {'profiles': profiles})

@login_required
def assign_superuser(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    if request.method == 'POST':
        profile.is_admin = not profile.is_admin
        profile.save()
        messages.success(request, f'Permiso de administrador {"asignado" if profile.is_admin else "revocado"} correctamente.')
        return redirect('/')
    return render(request, 'assign_superuser.html', {'profile': profile})