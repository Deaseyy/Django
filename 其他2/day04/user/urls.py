from django.contrib.auth.decorators import login_required
from django.urls import path

from user.views import register, login, logout, index

urlpatterns = [
    path('register/', register),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', login_required(index), name='index'),
]