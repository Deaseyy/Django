from django.conf.urls import url

from . import views

urlpatterns = [
    # 官方的两个demo教程 url
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
