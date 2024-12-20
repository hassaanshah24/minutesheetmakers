# apps/users/forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling and better error messages.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
        error_messages={'required': "Username cannot be empty."}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
        error_messages={'required': "Password cannot be empty."}
    )

    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data.get('username'):
            self.add_error('username', "Please enter your username.")
        if not self.cleaned_data.get('password'):
            self.add_error('password', "Please enter your password.")
        return cleaned_data

class CustomUserForm(forms.ModelForm):
    """
    Form for creating or updating a user with proper password handling.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,  # Password is optional when editing
        label="Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):  # Hash password if provided
            user.set_password(self.cleaned_data['password'])
        elif user.pk:  # Retain existing password if no new password is provided
            user.password = CustomUser.objects.get(pk=user.pk).password
        if commit:
            user.save()
        return user
