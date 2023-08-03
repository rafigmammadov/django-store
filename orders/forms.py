from django import forms
from django.forms import ModelForm

from orders.models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your '
                                                                                                       'first '
                                                                                                       'name'}),
                                 required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your last '
                                                                                                      'name'}),
                                required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your email '
                                                                                                  'address'}),
                            required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your address'}), required=True)
