from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import *


@login_required
def rated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.user.groups.filter(name='SELLER'):
        return render(request, 'rate_unauthorised.html')
    if request.method == 'POST':
        instance.good_rates += 1
        instance.save()
    return redirect('view_product', pk=pk)


@login_required
def unrated(request, pk):
    instance = Product.objects.get(pk=pk)
    if request.user.groups.filter(name='SELLER'):
        return render(request, 'rate_unauthorised.html')
    if request.method == 'POST':
        instance.bad_rates += 1
        instance.save()
    return redirect('view_product', pk=pk)
