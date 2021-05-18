from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from ..models import *
from ..forms import CheckoutForm
from django.contrib.auth.models import Group
from main.forms import CreateProductForm

@login_required
def checkout(request):
    form = CheckoutForm()
    num_wishes = WishlistProduct.objects.count()
    num_carts = Cart.objects.count()
    total_price = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            total_price += cart.cart_total_price()
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            
            if form.is_valid():
                adress1 = form.cleaned_data.get('adress_1')
                adress2 = form.cleaned_data.get('adress_2')
                zipcode = form.cleaned_data.get('zip_code')
                countryy = form.cleaned_data.get('country') 
                checkoutadress = Checkout.objects.create(
                    user = request.user,
                    adress_1 = adress1,
                    adress_2 = adress2,
                    zip_code = zipcode,
                    country = countryy
                )
                order = Order.objects.create(user= request.user, checkout_adress= checkoutadress,status= 'Payed')
                order.save()
                products=Product.objects.all()
                for cart in carts:
                    cart.product.quantity=cart.product.quantity-cart.quantity_carted
                    if cart.product.quantity <=0:
                        Product.objects.filter(pk=cart.product.id).delete()
                    else:
                        Product.objects.filter(pk=cart.product.id).update(quantity=cart.product.quantity)
                        print(cart.product.quantity)
                    order.cart.add(cart)
                    
                    
                carts.delete()
                       
                    
                return redirect('home')

            redirect('checkout')
            
  
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    context = {'form': form, 'group': group,
               'num_carts': num_carts, 'num_wishes': num_wishes, 'total_price': total_price}
    return render(request, 'checkout.html', context)
