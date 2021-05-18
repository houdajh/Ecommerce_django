from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from math import ceil
from accounts.decorators import allowed_users
from ..models import *
from ..forms import FeedBackForm


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
    product_feedbacks = ProductsFeedBacks.objects.filter(product=product)
    context = {'product': product, 'rate_avg': rate_avg,
               'num_wishes': num_wishes, 'group': group,
               'num_carts': num_carts, 'all_rates': all_rates,
               'real_rate': real_rate, 'num_carts': num_carts,
               'total_price': total_price, 'product_feedbacks': product_feedbacks,
               'form':form}
    return render(request, 'view_product.html', context)

def add_feedback(request,pk):
    product = Product.objects.get(pk=pk)
    form = FeedBackForm()
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            feedback = ProductsFeedBacks.objects.create(
                user=request.user,
                product=product,
                message=message,
            )
            feedback.save()
            return redirect('view_product',pk=pk)
    return redirect('view_product',pk=pk)


@allowed_users(allowed_roles=['ADMIN', 'CLIENT', 'SELLER'])
def search_form(request):
    wishes = WishlistProduct.objects.all()
    num_wishes = wishes.count()
    carts = Cart.objects.filter(user=request.user)
    num_carts = carts.count()
    total_price = 0
    for cart in carts:
        total_price += cart.cart_total_price()
    products = Product.objects.all().order_by('-rates')
    if 'term' in request.GET and request.GET['term']:
        term = request.GET.get('term')
        qs = Product.objects.filter(name__startswith=term)
        sources = []
        for product in qs:
            sources.append(
                {"value": "/view_product/"+str(product.id)+"/", "label": product.name})
        return JsonResponse(sources, safe=False)
    if 'search' in request.GET and request.GET['search']:
        search_query = request.GET.get('search')
        products = Product.objects.filter(
            Q(name__contains=search_query) | Q(category__category__contains=search_query) | Q(description__contains=search_query)).order_by('-rates')
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    return render(request, 'searches.html', {'products': products, 'num_wishes': num_wishes, 'group': group,
                                             'num_carts': num_carts, 'total_price': total_price})


@allowed_users(allowed_roles=['ADMIN', 'CLIENT', 'SELLER'])
def categorie(request, pk):
    total_price = 0
    num_wishes = WishlistProduct.objects.count()
    carts = Cart.objects.all()
    num_carts = carts.count()
    for cart in carts:
        total_price += cart.cart_total_price()
    products = Product.objects.filter(category__pk=pk)
    if products.first():
        cat = products.first().category
    else:
        cat = "Category"
    paginator = Paginator(products, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products_list = paginator.page(page)
    except(Emptypage, InvalidPage):
        products_list = paginator.page(paginator.num_pages)
    group = ""
    if request.user.groups.filter(name='CLIENT'):
        group = 'CLIENT'
    if request.user.groups.filter(name='ADMIN'):
        group = 'ADMIN'
    if request.user.groups.filter(name='SELLER'):
        group = 'SELLER'
    context = {'products': products, 'num_carts': num_carts, 'categorie': cat, 'group': group,
               'num_wishes': num_wishes, 'total_price': total_price, 'products_list': products_list}
    return render(request, 'categorie.html', context)
