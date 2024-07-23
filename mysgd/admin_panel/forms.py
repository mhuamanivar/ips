# forms.py
from django import forms
from shop.models import Product, RecordStatus, Supplier, Profile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'supplier', 'category', 'quantity', 'price', 'image', 'record_status']
        labels = {
            'name': 'Nombre',
            'supplier': 'Proveedor',
            'category': 'Categoría',
            'quantity': 'Cantidad',
            'price': 'Precio',
            'image': 'Imagen',
            'record_status': 'Estado del Registro',
        }
        widgets = {
            'record_status': forms.Select(choices=RecordStatus.objects.all().values_list('status', 'status')),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['record_status'].widget.attrs.update({'class': 'form-control'})
        # Add help texts for the fields
        self.fields['name'].help_text = "Ingrese el nombre del producto."
        self.fields['supplier'].help_text = "Seleccione el proveedor del producto."
        self.fields['category'].help_text = "Seleccione la categoría del producto."
        self.fields['quantity'].help_text = "Ingrese la cantidad del producto."
        self.fields['price'].help_text = "Ingrese el precio del producto."
        self.fields['image'].help_text = "Suba una imagen del producto."
        self.fields['record_status'].help_text = "Seleccione el estado del registro del producto."


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info', 'record_status']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dni', 'address', 'phone_number', 'credit_guarantor']