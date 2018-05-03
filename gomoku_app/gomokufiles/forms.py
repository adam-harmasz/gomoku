from django import forms
from django.core.validators import validate_email


class GomokuFileForm(forms.Form):
    files = forms.FileField(widget=forms.FileInput(attrs={'class': 'input-field'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'register-input'}))
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register-input'}))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register-input'}))
    email = forms.EmailField(validators=[validate_email], widget=forms.EmailInput(attrs={'class': 'register-input'}))




