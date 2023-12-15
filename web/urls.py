from django.contrib import admin
from django.urls import path, include

from web.views import index, register_view, login_view, logout_view

urlpatterns = [
    path('', index, name="main"),
    path('register/', register_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]