from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('admin_dashboard/', admin_dashboard_view, name='dashboard_admin'),
    path('view_customer/', view_customer_view, name='view_customer'),
    path('admin_products/', admin_products_view, name='admin_products'),

    
    path('admin_view_booking/', admin_view_booking_view, name='admin_view_booking'),
    path('view_feedback/', view_feedback_view, name='view_feedback'),
    path('delete_feedback/<int:pk>', delete_feedback_view, name='delete_feedback'),
    

    path('admin_sellers/', admin_sellers_view, name='admin_sellers'),
    path('delete_seller/<int:pk>', delete_seller_view, name='delete_seller'),
    
]
