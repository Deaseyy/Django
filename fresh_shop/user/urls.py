from django.urls import path

from user.views import user_center_info, user_center_order, user_center_site, login, register, logout, edit_site

urlpatterns = [
    path('info/', user_center_info, name='info'),
    path('order/', user_center_order, name='order'),
    path('site/', user_center_site, name='site'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit_site/', edit_site, name='edit_site'),
]

