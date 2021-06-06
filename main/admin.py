from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'category',
              'description', 'photo', 'price', 'quantity']

#ajoutant les tables a l'espace admin
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(ProductsRated)

admin.site.register(Order)
admin.site.register(Checkout)
admin.site.register(ContactUs)
admin.site.register(OrderedCart)