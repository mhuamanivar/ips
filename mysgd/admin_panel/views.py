from django.shortcuts import render
from shop.models import Product, CartItem, Order, Profile, Category, OrderItem, Payment, PaymentMethod, PaymentSchedule, Supplier  # Importa los modelos necesarios
from django.shortcuts import render, get_object_or_404

def profile_list(request):
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
    return render(request, 'admin_panel/profile_detail.html', {'profile': profile})



def product_list(request):
    # Obtén los parámetros de filtro de la solicitud GET
    supplier_id = request.GET.get('supplier')
    category_id = request.GET.get('category')
    
    # Filtra los productos según los parámetros
    products = Product.objects.all()
    if supplier_id:
        products = products.filter(supplier_id=supplier_id)
    if category_id:
        products = products.filter(category_id=category_id)
    
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'admin_panel/product_list.html', {
        'products': products,
        'suppliers': suppliers,
        'categories': categories
    })