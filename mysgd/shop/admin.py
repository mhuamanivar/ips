from django.contrib import admin
from .models import Product, Order, Supplier, Category, Profile, Order, CartItem, OrderItem, Payment, PaymentMethod, PaymentSchedule  # Asegúrate de que el nombre del modelo sea correcto

admin.site.register(Product)  # Registrar el modelo en el panel de administración
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(PaymentSchedule)
