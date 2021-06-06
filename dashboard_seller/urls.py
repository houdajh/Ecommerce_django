from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

#on cree les vues du dashboard seller 
urlpatterns = [
    path('dashboard_seller/', views.show_dashboard, name='dashboard_seller'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('prod/', views.show_product, name='prod'),
    path('statistics/', views.show_statistics, name='statistics'),
    
    
    path('settings/general/', views.show_general, name='general'),
    path('resultsdata/', views.result_data, name='resultsdata'),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),
    path('delete_account/', views.delete_account, name="delete_account"),
    path('settings/change-password/', auth_views.PasswordChangeView.as_view(
         template_name='dashboard_seller/settings/change_password.html'), name="change_password"),
]
