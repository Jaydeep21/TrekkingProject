from django import forms
from main.models import Customer
from django.contrib.auth.forms import UserChangeForm
from moneyed import list_all_currencies
from django.forms import Select


class InputTextSelect(Select):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input-text', 'onchange': 'update_price()'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class SignupForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ['phone', 'age']


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'placeholder': 'Email',
            "type": "email",
            "name": "email",
        }
    ), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input-text',
            "type": "password",
            'placeholder': 'Password',
            'name': 'password',
        }
    ), label="Password")


class PaymentForm(forms.Form):
    currency = forms.ChoiceField(choices=[(c.code, c.name) for c in list_all_currencies()],
                                 widget=InputTextSelect(), initial=['CAD'])
    price = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'class': 'input-text'
    }))
    card_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'placeholder': 'Enter Card Holder Name',
            "name": "card_name",
            'autocomplete': 'off',  # disable autocomplete for security
            'required': True,
            'maxlength': 50,
            'pattern': "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
        }

    ), error_messages={
        'invalid': 'Please enter a valid Card name',
        'required': 'Card Name is Required',
    })
    card_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'placeholder': 'Enter Card Number',
            "name": "card_number",
            'autocomplete': 'off',
            'required': True,
            'maxlength': 16,
            'pattern': '\d{16}'
        }
    ), error_messages={
        'invalid': 'Please enter a valid Card Number',
        'required': 'Card Number is Required',
    })
    expiry_date = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'autocomplete': 'off',
            'required': True,
            'placeholder': 'MM/YY',
            'name': 'expiry_date',
            'pattern': '(0[1-9]|1[0-2])\/\d{2}',
            'maxlength': '5',
        }
    ), error_messages={
        'invalid': 'Please enter a valid Card Number',
        'required': 'Card Number is Required',
    })
    security_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input-text',
            'placeholder': 'Enter Security Code',
            "name": "security_code",
            'autocomplete': 'off',
            'required': True,
            'pattern': '\d{3,4}',
            'maxlength': 4
        }
    ), error_messages={
        'invalid': 'Please enter a valid security number',
        'required': 'Security Code is Required',
    })