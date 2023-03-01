from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('register', views.register, name="register"),
 
    path('login', views.loginpage, name="login"),

    path('logout', views.logoutUser, name="logout"),

    path('', views.home, name="home"),

    path('customer/<str:primarykey>/', views.customer, name='customer'),

    path('product', views.product, name="product"),

    path('createorder/<str:pk>/', views.createorder, name="createorder"),

    path('updateorder/<str:pk>/', views.updateorder, name="updateorder"),

    path('deleteorder/<str:pk>/', views.deleteorder, name="deleteorder"),

    path('createcustomer', views.createcustomer, name="createcustomer"),

    path('user', views.userPage, name="user"),

    path('accountsetting', views.accountsetting, name="accountsetting"),

    # passwordrestting
    
    path('reset_password',auth_views.PasswordResetView.as_view(),name="reset_password"),
    
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(), name="reset_password_done" ),

    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),),
   
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),


]
