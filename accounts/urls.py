from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', login, name='login'),
    path('accounts/profile/', view_account, name='view_account'),
    path('accounts/profile/edit', edit_account, name='edit_account'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html'), name="change_passwordClient"),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html'), name="change_password_done"),
    
    path('delete_account_client/',delete_account_client, name='delete_account_client'),
]
