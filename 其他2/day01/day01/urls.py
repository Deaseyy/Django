"""day01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from app.views import hello, add_stu, sel_stu, del_stu, update_stu

urlpatterns = [
    path('admin/', admin.site.urls),
    # 127.0.0.1:8000/hello/
    path('hello/', hello),
    path('add_stu/', add_stu),
    path('sel_stu/', sel_stu),
    path('del_stu/', del_stu),
    path('update_stu/', update_stu),
]
