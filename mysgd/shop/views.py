from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Product, CartItem, Order, Profile, Category, OrderItem, Payment, PaymentMethod, PaymentSchedule
from django.contrib import messages
from django.db import IntegrityError, transaction
from .forms import UserRegisterForm, UserDetailsForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from django.template.defaultfilters import register
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta

from django.db import transaction

def home(request):
    return render(request, 'home.html')


def not_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print(f"User authenticated: {request.user.is_authenticated}")
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@not_login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html')

@not_login_required
def register1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            request.session['user_id'] = user.id
            return redirect('register2')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@not_login_required
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
    products = Product.objects.all().order_by('name')
    categories = Category.objects.all()

    query = request.POST.get('q')
    if query:
        products = products.filter(Q(name__icontains=query))

    no_results = False
    if query and len(products) == 0:
        no_results = True

    context = {
        'products': products,
        'categories': categories,
        'no_results': no_results,
        'active_category': None,  # Indicador para la categoría activa
    }
    return render(request, 'product_list.html', context)


def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('name')
    categories = Category.objects.all()

    # Obtener la categoría activa para marcarla en la plantilla
    active_category = category_id

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
    })



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
    
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
def clear_cart(request):
    if request.method == 'POST':
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, 'El carrito ha sido vaciado.')
    return redirect('cart_view')


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
        if action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif action == 'increase':
            cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view') 

# Función para eliminar del carrito
@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


@login_required
def cart_view(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        payment_type = request.POST.get('paymentType')

        with transaction.atomic():
            order = Order.objects.create(user=request.user, is_credit=(payment_type == 'credit'))

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    total_amount=cart_item.product.price * cart_item.quantity
                )

            request.session['order_id'] = order.id
            request.session['from_cart_view'] = True

        if payment_type == 'credit':
            return redirect('select_installments')
        else:
            return redirect('checkout_payment')

    cart = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def order_checkout_payment(request):
    # Verificar si el usuario vino desde cart_view
    if request.method == 'GET':
        if not request.session.get('from_cart_view'):
            return redirect('cart_view')
        else:
            del request.session['from_cart_view']
    
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        payment_method_id = request.POST.get('paymentMethod')
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        total_amount = sum(item.total_amount for item in order_items)

        # Crear la transacción de pago
        with transaction.atomic():
            payment = Payment.objects.create(
                order=order,
                amount=total_amount,
                payment_method=payment_method
            )

        # Almacenar order_items en la sesión
        request.session['order_items'] = [
            {'product_id': item.product.id, 'quantity': item.quantity} for item in order_items
        ]

        
        request.session['from_checkout_payment'] = True

        # Redirigir a la página correspondiente según el método de pago
        if payment_method_id == '1':
            return redirect('checkout_wallet')
        elif payment_method_id == '2':
            return redirect('checkout_card')
        elif payment_method_id == '3':
            return redirect('checkout_cash')

    return render(request, 'checkout_payment.html', {'methods': methods, 'order_items': order_items})



@login_required
def checkout_wallet(request):
    if not request.session.get('from_checkout_payment'):
        return redirect('cart_view')
    else:
        del request.session['from_checkout_payment']

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'checkout_wallet.html', {'order_items': order_items})


@login_required
def checkout_card(request):
    if not request.session.get('from_checkout_payment'):
        return redirect('cart_view')
    else:
        del request.session['from_checkout_payment']

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'checkout_card.html', {'order_items': order_items})

@login_required
def checkout_cash(request):
    if not request.session.get('from_checkout_payment'):
        return redirect('cart_view')
    else:
        del request.session['from_checkout_payment']
        
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'checkout_cash.html', {'order_items': order_items})

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
                order.status = 'in_preparation'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('orders')
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
                order.status = 'in_preparation'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('orders')
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
                order.status = 'in_preparation'
                order.save()

        CartItem.objects.filter(user=request.user).delete()

        # Procesar el pago aquí
        return redirect('orders')
    return redirect('checkout_payment')

@login_required
def cancel_order(request):
    if 'order_id' in request.session:
        order_id = request.session['order_id']
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        del request.session['order_id']

    # Eliminar la bandera de la sesión
    if 'from_cart_view' in request.session:
        del request.session['from_cart_view']

    return redirect('cart_view')

from datetime import date, timedelta

@login_required
def select_installments(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        installments = int(request.POST.get('installments'))

        # Limitar el número de plazos a un máximo de 4 (2 meses)
        if installments < 1 or installments > 4:
            messages.error(request, 'El número de plazos debe ser entre 1 y 4.')
            return redirect('select_installments')

        # Calcular el monto de cada cuota
        total_amount = order.total_amount
        installment_amount = total_amount / installments

        # Generar las fechas de vencimiento para cada plazo
        def get_next_payment_date(start_date):
            if start_date.day <= 9:
                return date(start_date.year, start_date.month, 9)
            elif start_date.day <= 24:
                return date(start_date.year, start_date.month, 24)
            else:
                next_month = start_date.month + 1 if start_date.month < 12 else 1
                next_year = start_date.year if start_date.month < 12 else start_date.year + 1
                return date(next_year, next_month, 9)

        due_dates = []
        next_payment_date = get_next_payment_date(order.created_at.date())
        for _ in range(installments):
            due_dates.append(next_payment_date)
            if next_payment_date.day == 9:
                if next_payment_date.month == 12:
                    next_payment_date = date(next_payment_date.year + 1, 1, 24)
                else:
                    next_payment_date = date(next_payment_date.year, next_payment_date.month + 1, 24)
            else:  # next_payment_date.day == 24
                next_payment_date = date(next_payment_date.year, next_payment_date.month + 1, 9)

        # Guardar cronograma de pagos en la base de datos
        with transaction.atomic():
            PaymentSchedule.objects.filter(order=order).delete()  # Eliminar cronograma anterior si existe
            for i, due_date in enumerate(due_dates):
                PaymentSchedule.objects.create(
                    order=order,
                    installment_number=i + 1,
                    amount=installment_amount,
                    due_date=due_date
                )

        return redirect('payment_schedule')

    return render(request, 'select_installments.html', {'order_items': order_items})


@login_required
def payment_schedule(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    payment_schedule = order.payment_schedules.all()
    
    return render(request, 'payment_schedule.html', {'payment_schedule': payment_schedule})

@login_required
def create_order(request):
    if request.method == 'POST':
        order_id = request.session.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order.save()

            # Clear the cart items
            CartItem.objects.filter(user=request.user).delete()
            # Optionally, clear the session data if needed
            del request.session['order_id']

            return redirect('orders')

    return redirect('payment_schedule')
