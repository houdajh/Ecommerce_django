from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Product

#on cree la formulaire du produit pour l'afficher dans l'interface
class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description',
                  'photo', 'price', 'quantity', 'color']


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)
#on cree la formulaire du de contactUs pour l'afficher dans l'interface
class ContactUsForm(forms.Form):
    name = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter your first name'
                           ,'class': 'input1'}))
    email = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Email'
                           ,'class': 'input1'}))
                           #specifier css de chauqe champs 
    subject = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'subject'
                           ,'class': 'input1'}))
    message= forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'message'
                           ,'class': 'input1'}))

#on cree la formulaire du checkout pour l'afficher dans l'interface
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


