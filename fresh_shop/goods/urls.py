from django.urls import path

from goods.views import goods_index, goods_detail, goods_list, search

urlpatterns = [
    path('index/', goods_index, name='index'),
    path('list/', goods_list, name='list'),
    path('detail/<int:id>/', goods_detail, name='detail'),
    path('search/', search, name='search'),

]