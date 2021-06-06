from django.db import models
from django.db.models.fields.related import OneToOneField
from django.forms import ChoiceField, RadioSelect
from django.db.models.fields import EmailField, PositiveIntegerField
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import Group
from phone_field import PhoneField

from django import forms

from django.contrib.auth.models import User
# Create your models here

TRADE_ROLE = (
    (0, 'SELLER'),
    (1, 'CLIENT'),
    (2, 'BOTH'),
)

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

COLORS = (
    ('RED', 'RED'),
    ('BLUE', 'BLUE'),
    ('BLACK', 'BLACK'),
    ('ORANGE', 'ORANGE'),
    ('PINK', 'PINK'),
    ('PURPLE', 'PURPLE'),
    ('GREEN', 'GREEN'),
    ('YELLOW', 'YELLOW'),
    ('GRAY', 'GRAY'),
    ('WHITE', 'WHITE'),
)


#table categories 
class Category(models.Model):
  
    category=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.category
#table des feedback users 
class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
#table des produits
class Product(models.Model):
    #definit user comme cle etranger
    user=models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    category=models.ForeignKey(
        Category,on_delete=models.CASCADE,null=True
    )
    description = models.TextField()
    photo = models.ImageField(blank=True,)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(null=True)
    good_rates = models.PositiveIntegerField(default=0)
    bad_rates = models.PositiveIntegerField(default=0)
    rates = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50, choices=COLORS, blank=True)

    def __str__(self):
        return self.name
    #definit des methodes du produit
    def get_display_price(self):
        return "{0:.2f}".format(self.price/10)
    #calculer la moyenne des rates et l'afficher pour chaque produit
    def avg_rate(self):
        self.rates = (self.good_rates-self.bad_rates)/(self.bad_rates +
                                                       self.good_rates) if self.bad_rates+self.good_rates != 0 else 0
        return self.rates
    def old_price(self):
        return self.price+3

class ProductsRated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE)
    rated = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

#table wishlist qui content les produits
class WishlistProduct(models.Model):
    user = models.ForeignKey(
        User, related_name='wishlist', on_delete=models.CASCADE)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_carted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name

    def cart_total_price(self):
        total_cart = self.quantity_carted*self.product.price
        return total_cart

class OrderedCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_carted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name


#table de payment informations
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    adress_1 = models.CharField(max_length=100)
    adress_2 = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100)
#order est creer apres payment
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    OrderedCart = models.ManyToManyField(OrderedCart,blank=True)
    checkout_adress = models.ForeignKey(Checkout , on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=200, null=True)




