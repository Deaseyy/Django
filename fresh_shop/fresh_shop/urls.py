"""fresh_shop URL Configuration

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
from django.urls import path, include
from django.contrib.staticfiles.urls import static

from fresh_shop.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(('user.urls', 'user'), namespace='user')),
    path('goods/',include(('goods.urls', 'goods'), namespace='goods')),
    path('carts/',include(('carts.urls', 'carts'), namespace='carts')),
    path('order/',include(('order.urls', 'order'), namespace='order')),
]

# media 图片访问  添加能当作静态文件自动访问
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)