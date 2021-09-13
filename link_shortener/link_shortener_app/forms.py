from django import forms
from django.core.validators import URLValidator, EmailValidator
from .models import HASH_LEN


class LongLinkForm(forms.Form):
    long_link = forms.CharField(label="", initial="", max_length=500, validators=[URLValidator()])
    long_link.widget = forms.TextInput(attrs={'class': "form-control",
                                              'placeholder': "http://my_long_link_longlonglonglong.com"})


class ShortLinkForm(forms.Form):
    short_link = forms.CharField(label="", initial="", max_length=20)
    short_link.widget = forms.TextInput(attrs={'class': "form-control"})


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=50, validators=[EmailValidator(allowlist=['\D+\.\D+'])])
    email.widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})

    password = forms.CharField(label="Enter your password", max_length=HASH_LEN)
    password.widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Password"})

    password_confirmation = forms.CharField(label="Confirm your password", max_length=HASH_LEN)
    password_confirmation.widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Confirm"})


class SignInForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=50, validators=[EmailValidator(allowlist=['\D+\.\D+'])])
    email.widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})

    password = forms.CharField(label="Enter your password", max_length=HASH_LEN)
    password.widget = forms.TextInput(attrs={"class": "form-control", "placeholder": "Password"})
