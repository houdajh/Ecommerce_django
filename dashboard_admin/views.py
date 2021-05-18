from django.shortcuts import render, redirect, reverse
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from main.models import *
from main.forms import *
from main.filters import ProductFilter

from accounts.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['ADMIN'])
def admin_dashboard_view(request):
    # for cards on dashboard
    group = Group.objects.get(name='CLIENT')
    customercount = group.user_set.count()
    productcount = Product.objects.count()
    ordercount = Order.objects.count()
    group = Group.objects.get(name='SELLER')
    seller_count = group.user_set.count()

    # for recent order tables
    orders = Order.objects.all()
    ordered_products = []
    ordered_bys = []
    for order in orders:
        ordered_product = Product.objects.filter(id=order.id)
        #ordered_by = Customer.objects.filter(id=order.customer.id)
        ordered_products.append(ordered_product)
        #ordered_bys.append(ordered_by)

    mydict = {
        'customercount': customercount,
        'productcount': productcount,
        'ordercount': ordercount,
        'seller_count': seller_count,
        'data': orders,
    }
    return render(request, 'dashboard_admin/admin_dashboard.html', context=mydict)


# admin view customer table
# @login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def view_customer_view(request):
    group = Group.objects.get(name='CLIENT')
    customers = group.user_set.all()
    return render(request, 'dashboard_admin/view_customer.html', {'customers': customers})




# admin view the product
# @login_required(login_url='login')

@allowed_users(allowed_roles=['ADMIN'])
def admin_products_view(request):
    products =Product.objects.all()
    return render(request, 'dashboard_admin/admin_products.html', {'products': products})



# @login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def admin_view_booking_view(request):
    orders = Order.objects.all()
    return render(request, 'dashboard_admin/admin_view_booking.html', {'data': orders})



# admin view the Seller
# @login_required(login_url='login')
def admin_sellers_view(request):
    group = Group.objects.get(name='SELLER')
    sellers = group.user_set.all()
    return render(request, 'dashboard_admin/admin_sellers.html', {'sellers': sellers})


# @login_required(login_url='login')
def delete_seller_view(request, pk):
    group = Group.objects.get(name='SELLER')
    seller = group.user_set.get(id=pk)
    seller.delete()
    return redirect('admin_sellers')



# admin view the feedback
#@login_required(login_url='login')
def view_feedback_view(request):
    feedbacks=Feedback.objects.all().order_by('-id')
    return render(request,'dashboard_admin/view_feedback.html',{'feedbacks':feedbacks})