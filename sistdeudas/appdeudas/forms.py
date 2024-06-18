from django import forms
from .models import Pedido

class CrearNuevoPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'tipo_pedido', 'metodo_pago', 'total', 'productos']
        widgets = {
            'tipo_pedido': forms.Select(),
            'productos': forms.CheckboxSelectMultiple(),
            'metodo_pago': forms.Select(),
        }
        labels = {
            'cliente': 'Cliente',
            'tipo_pedido': 'Tipo de Pedido',
            'metodo_pago': 'Método de Pago',
            'productos': 'Productos',
            'total': 'Total',
        }
