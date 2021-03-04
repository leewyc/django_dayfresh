from django.contrib import admin
from django.urls import include, path
from .views import *
urlpatterns = [
    path('',index),
    path(r'register',register),
    path(r'register_handle',register_handle),
    path(r'register_exist/',register_exist),
    path(r'login',login),
    path(r'user_center_info',center_info),
    path(r'login_handle',login_handle),
    path(r'user_center_order',order),
    path(r'user_center_site',site),
    path(r'info',info),
    path(r'site',site)
]