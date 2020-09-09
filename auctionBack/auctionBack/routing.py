"""
这个根路由配置指定: 当与 Channels 开发服务器建立连接的时候,
ProtocolTypeRouter 将首先检查连接的类型。
如果是 WebSocket 连接 (ws://或 wss://), 则连接会交给 AuthMiddlewareStack。

AuthMiddlewareStack 将使用对当前经过身份验证的用户的引用来填充连接的 scope,
类似于 Django 的 AuthenticationMiddleware 用当前经过身份验证的用户填充视图函数的请求对象。
（Scopes 将在本教程后面讨论。）然后连接将被给到 URLRouter。

"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns   # 指向chat.routing
        )
    ),
})