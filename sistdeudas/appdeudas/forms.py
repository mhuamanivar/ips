from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, Cliente

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha', 'tipo_pedido', 'metodo_pago', 'total', 'productos', 'estado']
