from django import forms
from django.core.validators import URLValidator


class LongLinkForm(forms.Form):
    long_link = forms.CharField(label="", initial="", max_length=500, validators=[URLValidator()])
    long_link.widget = forms.TextInput(attrs={'class': "form-control",
                                              'placeholder': "http://my_long_link_longlonglonglong.com"})


class ShortLinkForm(forms.Form):
    short_link = forms.CharField(label="", initial="", max_length=20)
    short_link.widget = forms.TextInput(attrs={'class': "form-control"})