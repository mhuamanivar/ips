from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_of_measure = models.CharField(max_length=10, default='L')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, blank=True, null=True)
    credit_approved = models.BooleanField(default=False)
    credit_guarantor = models.FileField(upload_to='credit_guarantors/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    has_outstanding_debt = models.BooleanField(default=False)  

    def __str__(self):
        return self.user.username
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_credit = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('in_preparation', 'En preparación'),
        ('prepared', 'Preparado'),
        ('delivered', 'Entregado'),
        ('delivered_in_debt', 'Entregado en deuda'),
        ('completed', 'Finalizado'),
        ('cancelled', 'Anulado')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        # Calcular la suma de total_amount de todos los OrderItem asociados a esta Order
        return sum(item.total_amount for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def formatted_created_date(self):
        return self.created_at.astimezone(timezone.get_current_timezone()).strftime("%d-%m-%Y")

    def formatted_created_time(self):
        return self.created_at.astimezone(timezone.get_current_timezone()).strftime("%I:%M %p")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name} ({self.quantity})"

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"

class PaymentSchedule(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_schedules', blank=True, null=True)
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('in_process', 'En proceso'),
            ('paid', 'Pagado'),
            ('overdue', 'Atrasado')
        ],
        default='pending'
    )

    def formatted_due_date(self):
        return self.due_date.strftime("%d-%m-%Y")

    def __str__(self):
        return f"Installment {self.installment_number} for Order {self.order.id}"
    


@receiver(post_save, sender=Order)
def update_user_profile_debt_status(sender, instance, **kwargs):
    if instance.is_credit:
        # Obtener el perfil del usuario asociado
        profile = Profile.objects.get(user=instance.user)
        # Verificar si hay algún pedido con is_credit=True y status diferente de "completed"
        has_outstanding_debt = Order.objects.filter(user=instance.user, is_credit=True).exclude(status='completed').exists()
        # Actualizar el campo en el perfil
        profile.has_outstanding_debt = has_outstanding_debt
        profile.save()


@receiver(post_delete, sender=Order)
def update_user_profile_debt_status_on_delete(sender, instance, **kwargs):
    # Obtener el perfil del usuario asociado
    profile = Profile.objects.get(user=instance.user)
    # Verificar si hay algún pedido con is_credit=True y status diferente de "completed"
    has_outstanding_debt = Order.objects.filter(user=instance.user, is_credit=True).exclude(status='completed').exists()
    # Actualizar el campo en el perfil
    profile.has_outstanding_debt = has_outstanding_debt
    profile.save()