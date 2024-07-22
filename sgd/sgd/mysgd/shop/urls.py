# shop/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register1, name='register'),
    path('register2/', views.register2, name='register2'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),  # Cambiar aquí
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('order/checkout_payment/', views.order_checkout_payment, name='checkout_payment'),
    path('order/checkout_wallet/', views.checkout_wallet, name='checkout_wallet'),
    path('order/checkout_card/', views.checkout_card, name='checkout_card'),
    path('order/checkout_cash/', views.checkout_cash, name='checkout_cash'),
    path('order/process_wallet_payment/', views.process_wallet_payment, name='process_wallet_payment'),
    path('order/process_card_payment/', views.process_card_payment, name='process_card_payment'),
    path('order/process_cash_payment/', views.process_cash_payment, name='process_cash_payment'),
    path('create-order/', views.create_order, name='create_order'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('select_installments/', views.select_installments, name='select_installments'),
    path('payment_schedule/', views.payment_schedule, name='payment_schedule'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
