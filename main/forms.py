from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Product, ProductsFeedBacks


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description',
                  'photo', 'price', 'quantity', 'color']


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class ContactUsForm(forms.Form):
    name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter your first name'
                           ,'class': 'input1'}))
    email = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Email'
                           ,'class': 'input1'}))
    subject = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'subject'
                           ,'class': 'input1'}))
    message= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'message'
                           ,'class': 'input1'}))
class CheckoutForm(forms.Form):
    adress_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control '
    }))
    adress_2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control p-0'
    }))
    
    
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = ProductsFeedBacks
        fields = ['message']
