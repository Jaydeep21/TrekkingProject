from django import forms
from main.models import Customer
from django.contrib.auth.forms import UserChangeForm


class SignupForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ['phone', 'age']


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'input-text',
        'placeholder':'Email',
        "type":"email",
        "name": "email",
        }
    ), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'input-text',
        "type" : "password",
        'placeholder':'Password',
        'name': 'password',
        }
    ), label="Password")