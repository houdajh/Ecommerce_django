from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from accounts.forms import CreateUserForm,SettingsForm

from .forms import CreateUserForm
from main.models import WishlistProduct, Cart
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            userType = form.cleaned_data.get('choice')
            if userType == 'BOTH':
                group1 = Group.objects.get(name='SELLER')
                user.groups.add(group1)
                group2 = Group.objects.get(name='CLIENT')
                user.groups.add(group2)
            else:
                group = Group.objects.get(name=userType)
                user.groups.add(group)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required
def view_account(request):
    userform = User.objects.get(id=request.user.id)
    form = SettingsForm(instance=userform)
    
    if request.method == 'POST':

        form = SettingsForm(request.POST, instance=userform)
        print(form.name)
        if form.is_valid():
            form.save()
            return redirect('general')
    context = {'form': form}
    return render(request, 'accounts/myAccount.html',context)



@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account/profile/')
    return render(request, 'accounts/myAccount.html')


@login_required
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset/password_reset.html", context={"password_reset_form": password_reset_form})

@login_required
def delete_account_client(request):
    user=request.user
    if request.method == "POST":
        user.delete()
        return redirect('home')
    context = {'user': user}
    return render(request, 'accounts/delete_account.html', context)