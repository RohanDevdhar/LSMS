from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home-page"),
    path('login',views.login_page,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('users',views.users,name='user-page'),
    path('manage_user',views.manage_user,name='manage-user'),
    path('manage_user/<int:pk>',views.manage_user,name='manage-user-pk'),
    path('save_user',views.save_user,name='save-user'),
    path('delete_user/<int:pk>',views.delete_user,name='delete-user'),
    path('prices',views.price,name='price-page'),
    path('manage_price',views.manage_price,name='manage-price'),
    path('manage_price/<int:pk>',views.manage_price,name='manage-price-pk'),
    path('view_price/<int:pk>',views.view_price,name='view-price-pk'),
    path('save_price',views.save_price,name='save-price'),
    path('delete_price/<int:pk>',views.delete_price,name='delete-price'),
    path('products',views.products,name='product-page'),
    path('manage_product',views.manage_product,name='manage-product'),
    path('manage_product/<int:pk>',views.manage_product,name='manage-product-pk'),
    path('view_product',views.view_product,name='view-product'),
    path('view_product/<int:pk>',views.view_product,name='view-product-pk'),
    path('save_product',views.save_product,name='save-product'),
    path('delete_product/<int:pk>',views.delete_product,name='delete-product'),
    path('manage_stockin/<int:pid>',views.manage_stockin,name='manage-stockin-pid'),
    path('manage_stockin/<int:pid>/<int:pk>',views.manage_stockin,name='manage-stockin-pid-pk'),
    path('save_stockin',views.save_stockin,name='save-stockin'),
    path('delete_stockin/<int:pk>',views.delete_stockin,name='delete-stockin'),
    path('laundries',views.laundries,name='laundry-page'),
    path('manage_laundry',views.manage_laundry,name='manage-laundry'), 
    path('manage_laundry/<int:pk>',views.manage_laundry,name='manage-laundry-pk'),
    path('view_laundry',views.view_laundry,name='view-laundry'),
    path('view_laundry/<int:pk>',views.view_laundry,name='view-laundry-pk'),
    path('save_laundry',views.save_laundry,name='save-laundry'),
    path('delete_laundry/<int:pk>',views.delete_laundry,name='delete-laundry'),
    path('update_transaction_form/<int:pk>',views.update_transaction_form,name='transacton-update-status'),
    path('update_transaction_status',views.update_transaction_status,name='update-laundry-status'),
    path('daily_report',views.daily_report,name='daily-report'),
    path('daily_report/<str:date>',views.daily_report,name='daily-report-date'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
