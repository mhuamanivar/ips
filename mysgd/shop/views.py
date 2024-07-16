from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Product, CartItem, Order, Profile, Category, OrderItem, Payment, PaymentMethod
from django.contrib import messages
from django.db import IntegrityError, transaction
from .forms import UserRegisterForm, UserDetailsForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from django.template.defaultfilters import register

def home(request):
    return render(request, 'home.html')

def register1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            request.session['user_id'] = user.id  # Save user ID in session
            return redirect('register2')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def register2(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
            except IntegrityError:
                profile = Profile.objects.get(user=user)
                profile.dni = form.cleaned_data['dni']
                profile.phone_number = form.cleaned_data['phone_number']
                profile.address = form.cleaned_data['address']
                profile.save()

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserDetailsForm()
    return render(request, 'register2.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Manejo de la búsqueda
    query = request.POST.get('q')
    if query:
        # Filtrar productos por nombre o descripción que contengan el query
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Verificar si no se encontraron resultados
    no_results = False
    if query and len(products) == 0:
        no_results = True

    context = {
        'products': products,
        'categories': categories,
        'no_results': no_results,  # Variable para indicar que no se encontraron resultados
    }
    return render(request, 'product_list.html', context)

def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir a una página de éxito o a otra parte del sitio
            return redirect('home')  # Redirige a la página 'home' después del login
        else:
            # Mostrar un mensaje de error de login
            return render(request, 'login.html', {'error_message': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html')
    
@login_required
def orders(request):
    # Retrieve all orders for the current user, ordenados por fecha descendente
    orders_contado = Order.objects.filter(user=request.user, is_credit=False).order_by('-created_at')
    orders_credito = Order.objects.filter(user=request.user, is_credit=True).order_by('-created_at')

    context = {
        'orders_contado': orders_contado,
        'orders_credito': orders_credito,
    }
    return render(request, 'orders.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()  # Obtener todos los OrderItem asociados a esta Order

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'order_detail.html', context)



@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def total_price(cart_items):
    return sum(item.product.price * item.quantity for item in cart_items)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart_view')

@login_required
def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'El producto se eliminó del carrito correctamente.')
        return redirect('cart_view') 
    
    return redirect('cart_view')


from django.db import transaction

@login_required
def cart_view(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        payment_type = request.POST.get('paymentType')

        # Crear el pedido
        with transaction.atomic():
            order = Order.objects.create(user=request.user, is_credit=(payment_type == 'credit'))

            # Crear los OrderItems basados en los elementos del carrito
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_amount=cart_item.product.price * cart_item.quantity
                )

            # Almacenar el ID del pedido en la sesión para usarlo en el pago
            request.session['order_id'] = order.id

        # Redirigir a la página de checkout_payment
        return redirect('checkout_payment')

    cart = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def order_checkout_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    cart_items = CartItem.objects.filter(user=request.user)
    methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        payment_method_id = request.POST.get('paymentMethod')
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Crear la transacción de pago
        with transaction.atomic():
            payment = Payment.objects.create(
                order=order,
                amount=total_amount,
                payment_method=payment_method
            )

        # Almacenar cart_items en la sesión
        request.session['cart_items'] = [
            {'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items
        ]

        # Redirigir a la página correspondiente según el método de pago
        if payment_method_id == '1':
            return redirect('checkout_wallet')
        elif payment_method_id == '2':
            return redirect('checkout_card')
        elif payment_method_id == '3':
            return redirect('checkout_cash')

    return render(request, 'checkout_payment.html', {'methods': methods, 'cart': cart_items})

@login_required
def checkout_wallet(request):
    cart_items_data = request.session.get('cart_items')
    cart_items = [CartItem(product=get_object_or_404(Product, id=item['product_id']), quantity=item['quantity']) for item in cart_items_data]
    return render(request, 'checkout_wallet.html', {'cart': cart_items})

@login_required
def checkout_card(request):
    cart_items_data = request.session.get('cart_items')
    cart_items = [CartItem(product=get_object_or_404(Product, id=item['product_id']), quantity=item['quantity']) for item in cart_items_data]
    return render(request, 'checkout_card.html', {'cart': cart_items})

@login_required
def checkout_cash(request):
    cart_items_data = request.session.get('cart_items')
    cart_items = [CartItem(product=get_object_or_404(Product, id=item['product_id']), quantity=item['quantity']) for item in cart_items_data]
    return render(request, 'checkout_cash.html', {'cart': cart_items})

@login_required
def process_wallet_payment(request):
    if request.method == 'POST':
        # Lógica para procesar el pago con billetera
        wallet_id = request.POST.get('walletId')
        wallet_pin = request.POST.get('walletPin')

        with transaction.atomic():
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            if not order.is_credit:
                order.status = 'completed'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('order_success')
    return redirect('checkout_payment')

@login_required
def process_card_payment(request):
    if request.method == 'POST':
        # Lógica para procesar el pago con tarjeta
        card_number = request.POST.get('cardNumber')
        card_expiry = request.POST.get('cardExpiry')
        card_cvc = request.POST.get('cardCVC')

        with transaction.atomic():
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            if not order.is_credit:
                order.status = 'completed'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('order_success')
    return redirect('checkout_payment')

@login_required
def process_cash_payment(request):
    if request.method == 'POST':
        # Lógica para procesar el pago en efectivo
        delivery_address = request.POST.get('deliveryAddress')
        contact_number = request.POST.get('contactNumber')

        with transaction.atomic():
            order_id = request.session.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            if not order.is_credit:
                order.status = 'completed'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('order_success')
    return redirect('checkout_payment')

@login_required
def order_success(request):
    return render(request, 'order_success.html')

@login_required
def cancel_order(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    # Delete the order and related cart items
    order.delete()
    CartItem.objects.filter(user=request.user).delete()

    # Delete related session variables
    del request.session['order_id']

    messages.success(request, 'The order has been cancelled successfully.')
    return redirect('cart_view')