"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',v.Home),
    path('login',v.userLogin ,name='login'),
    path('createAccount', v.createAccount , name='createAccount'),
    path('logout',v.logoutUser),

    path('pricing',v.pricingPage),

    path('payment',v.Payment),
    path('contact',v.Contact),

    # password reset url and auth_views
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/reset.html',email_template_name='password_reset/reset_email.html',),
         name='password_reset'),
    
    # password reset email sent done url and auth_views
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    # password reset create new password url and auth_views
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/reset_confirm.html'),
         name='password_reset_confirm'),

    # password reset new password set done url and auth_views
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/reset_done.html'),
         name='password_reset_complete'),
]
