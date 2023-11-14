from django import contrib, forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.forms import fields, widgets
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy as gt
from . models import Customer


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'input'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'input'}))
    phone = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'class': 'input'}))

    # username = forms.CharField(label = "Your Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'class':'input'}))
    # email = forms.EmailField(required=True, label="Your Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'class':'input'}))
    # phone = forms.IntegerField(required=True, label="Phone Numbers", widget=forms.TextInput(attrs={'class': 'form-control','class':'input'}))
    # pass1 = forms.CharField(label="Passwords", widget=forms.PasswordInput(attrs={'class': 'form-control', 'class':'input'}))
    # pass2 = forms.CharField(label="Confirm Passwords", widget=forms.PasswordInput(attrs={'class': 'form-control', 'class':'input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        labels = {'email': 'Email'}
        widget = {'username': forms.TextInput(attrs={'class': 'input'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(label="Name", widget=forms.TextInput(
        attrs={'autofocus': True, 'class':'input'}))
    password = forms.CharField(label=('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class':'input'}))
    

#To add user information to user profile such as name, address, etc.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'house_number',
                  'locality', 'landmark', 'city']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'house_number': forms.TextInput(attrs={'class': 'form-control'}),
                   'locality': forms.TextInput(attrs={'class': 'form-control'}),
                   'landmark': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   }
        



#To change password
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=gt('Old Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=gt('New Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'autofocus': True, 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=gt('Confirm Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}))


#Password reset using forget password functionality.
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=gt('Email'), max_length=200, widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control'}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=gt("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=gt("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))
