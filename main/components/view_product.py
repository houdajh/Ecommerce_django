from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from math import ceil
from accounts.decorators import allowed_users
from ..models import *



def view_product(request, pk):
    product = Product.objects.get(pk=pk)
    rate_avg = ceil(product.avg_rate()*5) if product.avg_rate() >= 0 else 0
    real_rate = int(product.avg_rate()*100) if product.avg_rate() >= 0 else 0
    wishes = WishlistProduct.objects.all()
    num_wishes = wishes.count()
    carts = Cart.objects.filter(user=request.user)
    num_carts = carts.count()
    total_price = 0
    for cart in carts:
        total_price += cart.cart_total_price()
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    form = FeedBackForm()
    all_rates = product.good_rates + product.bad_rates
    
    context = {'product': product, 'rate_avg': rate_avg,
               'num_wishes': num_wishes, 'group': group,
               'num_carts': num_carts, 'all_rates': all_rates,
               'real_rate': real_rate, 'num_carts': num_carts,
               'total_price': total_price,
               'form':form}
    return render(request, 'view_product.html', context)








    