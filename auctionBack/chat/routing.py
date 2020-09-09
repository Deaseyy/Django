from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/chat/(?P<group_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^push/(?P<username>[0-9a-z]+)/$', consumers.PushConsumer),
]