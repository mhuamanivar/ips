from django.shortcuts import render
from shop.models import Product, CartItem, Order, Profile, Category, OrderItem, Payment, PaymentMethod, PaymentSchedule, Supplier, RecordStatus  # Importa los modelos necesarios
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from admin_panel.forms import ProductForm, SupplierForm, ProfileForm
from django.db.models import Q
from django.shortcuts import render

def profile_list(request):
    status = request.GET.get('status')

    if status == 'pending':
        profiles = Profile.objects.filter(
            credit_approved=False,
            credit_guarantor__isnull=False
        ).exclude(credit_guarantor='')
    elif status == 'not_accepted':
        profiles = Profile.objects.filter(
            credit_approved=False,
            credit_guarantor__exact=''
        )
    elif status == 'accepted':
        profiles = Profile.objects.filter(
            credit_approved=True
        )
    else:
        profiles = Profile.objects.all()

    return render(request, 'admin_panel/profile_list.html', {'profiles': profiles})



def supplier_list(request):
    # Obtén el parámetro de filtro de la solicitud GET
    category_id = request.GET.get('category')
    
    # Filtra proveedores según la categoría
    suppliers = Supplier.objects.all()
    if category_id:
        suppliers = suppliers.filter(product__category_id=category_id).distinct()
        
    categories = Category.objects.all()
    
    return render(request, 'admin_panel/suppliers.html', {
        'suppliers': suppliers,
        'categories': categories
    })

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if 'edit' in request.GET:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('admin_panel:profile_detail', pk=profile.pk)
        else:
            form = ProfileForm(instance=profile)
        return render(request, 'admin_panel/profile_detail.html', {'profile': profile, 'form': form, 'edit_mode': True})
    
    return render(request, 'admin_panel/profile_detail.html', {'profile': profile, 'edit_mode': False})




def product_list(request):
    active_status = RecordStatus.objects.get(status='A')
    inactive_status = RecordStatus.objects.get(status='I')
    products = Product.objects.filter(record_status__in=[active_status, inactive_status])

    supplier_id = request.GET.get('supplier')
    if supplier_id:
        products = products.filter(supplier__id=supplier_id)

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category__id=category_id)

    suppliers = Supplier.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'suppliers': suppliers,
        'categories': categories
    }
    return render(request, 'admin_panel/product_list.html', context)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    deleted_status = get_object_or_404(RecordStatus, status='*')
    product.record_status = deleted_status
    product.save()
    return redirect(reverse('admin_panel:product_list'))

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/edit_product.html', {'form': form, 'product': product})

def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'admin_panel/edit_supplier.html', {'form': form, 'supplier': supplier})

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    deleted_status = get_object_or_404(RecordStatus, status='*')
    supplier.record_status = deleted_status
    supplier.save()
    return redirect('admin_panel:suppliers')

def accept_guarantor(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile.credit_approved = True
    profile.save()
    return redirect(reverse('admin_panel:profile_detail', args=[pk]))

def reject_guarantor(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile.credit_approved = False
    profile.credit_guarantor.delete()  # Elimina el archivo del perfil
    profile.credit_guarantor = None
    profile.save()
    return redirect(reverse('admin_panel:profile_detail', args=[pk]))