
from django.urls import path

from home.home_page import views

urlpatterns = [
  # 获取临时密钥
    path('getNum', views.get_num),
]
