from django.contrib.auth.decorators import login_required
from django.urls import path

from user.views import register, login, logout, index, \
    my_register, my_login, my_index, my_session_login, my_session_logout, \
    register_icon, list_user

urlpatterns = [
    # 使用django自带的User模型实现登录注册注销
    path('register/', register),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', index, name='index'),
    # 自定义User模型，并实现登录注册注销（采用cookie+token的形式）
    path('my_register/', my_register),
    path('my_login/', my_login, name='my_login'),
    path('my_index/', my_index, name='my_index'),
    # 使用session实现登录
    path('my_session_login/', my_session_login, name='my_session_login'),
    path('my_session_logout/', my_session_logout, name='my_session_logout'),
    # 头像上传ImageFiled使用
    path('register_icon/', register_icon),
    # 分页
    path('list/', list_user, name='list'),

]