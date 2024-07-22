from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class UserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)

    class Meta:
        model = Profile
        fields = ['dni', 'phone_number', 'address']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Campos del modelo User que quieres incluir

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.instance.email:
            raise forms.ValidationError("No puedes cambiar tu correo electrónico.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dni', 'phone_number', 'address', 'credit_approved', 'credit_guarantor']  # Campos del modelo Profile que quieres incluir
