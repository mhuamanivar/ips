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
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('products/category/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),  # Cambiar aquí
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/', views.cart_view, name='cart_view'),
    path('order/checkout_payment/', views.order_checkout_payment, name='checkout_payment'),
    path('order/checkout_wallet/', views.checkout_wallet, name='checkout_wallet'),
    path('order/checkout_card/', views.checkout_card, name='checkout_card'),
    path('order/checkout_cash/', views.checkout_cash, name='checkout_cash'),
    path('order/process_wallet_payment/', views.process_wallet_payment, name='process_wallet_payment'),
    path('order/process_card_payment/', views.process_card_payment, name='process_card_payment'),
    path('order/process_cash_payment/', views.process_cash_payment, name='process_cash_payment'),
    path('order/success', views.order_success, name='order_success'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
