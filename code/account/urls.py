"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views





urlpatterns = [
    path('create-profil/', views.CreateProfil.as_view()),
    path('create-profil-user/', views.CreateProfilUser.as_view()),
    path('complete-profil/', views.CompleteProfil.as_view()),
    path('verify-profil/(<str:token>.+)/', views.VerifyProfil.as_view()),
    path('login-profil/', views.LoginProfil.as_view()),
    path('logout-profil/', views.LogoutProfil.as_view()),
    path('password-profil/(<str:token>.+)/', views.PasswordProfil.as_view()),
    path('forget-password/', views.ForgetPassword.as_view()),
    path('forget-password-complete/', views.ForgetpasswordComplete.as_view()),
    path('edit-profil/', views.EditProfil.as_view()),
    path('about-profil/', views.AboutProfil.as_view()),
    path('security-profil/', views.SecurityProfil.as_view()),

]
