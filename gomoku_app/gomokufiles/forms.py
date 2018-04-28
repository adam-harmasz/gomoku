from django import forms
from django.core.validators import validate_email


class GomokuFileForm(forms.Form):
    files = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64)
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(validators=[validate_email])




