from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from app.views import *

urlpatterns = [
    path('index/', index),
    # 跳转，无参情况
    path('redirect_no_params/', redirect1, name='no_params'),
    # 跳转，有参情况
    path('redirect_params/<int:id>/', redirect2, name='params'),
    re_path('redirect_params2/(\d+)/', redirect2, name='params2'),
    # 请求
    path('index2/', index2),

    # 权限
    # path('add_permission/', login_required(add_permission)),
    path('add_permission/', add_permission),
    path('menu/', menu),

]
