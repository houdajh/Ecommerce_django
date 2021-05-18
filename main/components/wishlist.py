from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from django.http import JsonResponse
from ..models import *


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def wishlist(request):
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
    context = {'products': wishes, 'num_wishes': num_wishes, 'group': group,
               'num_carts': num_carts, 'total_price': total_price}
    return render(request, 'wishlist.html', context)


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def add_wishlist(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        produit = Product.objects.get(pk=product_id)
        total_price = 0
        num_wishes = WishlistProduct.objects.count()
        carts = Cart.objects.all()
        num_carts = carts.count()
        if request.user.is_authenticated:
            owner = request.user
            m = WishlistProduct.objects.create(user=owner, product=produit)
            m.save()
            num_wishes = WishlistProduct.objects.filter(user=owner).count()
            carts = Cart.objects.filter(user=owner)
            num_carts = carts.count()
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['num_wishes'] = '<div id="num_wishes" class="wishlist_count">' + \
            str(num_wishes)+'</div>'
        return JsonResponse(data)
    return render(request, 'wishlist.html')


@login_required
@allowed_users(allowed_roles=['ADMIN', 'CLIENT'])
def eliminate_wish(request, pk):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        wish = WishlistProduct.objects.get(pk=pk)
        wish.delete()
        carts = Cart.objects.all()
        num_carts = carts.count()
        num_wishes = WishlistProduct.objects.count()
        total_price = 0
        for cart in carts:
            total_price += cart.cart_total_price()
        data = {}
        data['num_wishes'] = '<div id="num_wishes" class="wishlist_count">' + \
            str(num_wishes)+'</div>'
        return JsonResponse(data)
    return redirect('wishlist')
