from django import forms
from .models import Business
from shop.models import Profile

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'image', 'description', 'ruc']

class AdminPermissionForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['is_admin']