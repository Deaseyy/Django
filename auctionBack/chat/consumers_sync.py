"""
ChatConsumer 当前是同步的。同步的 consumers 很方便, 因为它们可以调用常规的同步 I/O 函数,
例如访问 Django models 而不用编写特殊的代码。但是, 异步的 consumers 可以提供更高级别的性能,
因为它们在处理请求时不需要创建其他线程
"""
"""
我们建议您在默认情况下编写syncconsumer，并且只在以下情况下使用asyncconsumer:
您知道您正在做的事情可以通过异步处理(可以并行完成的长时间运行的任务)得到改进，并且您只使用异步本机库。
"""

"""
当用户发布消息时, JavaScript 函数将通过 WebSocket 将消息传输到 ChatConsumer。
ChatConsumer 将接收该消息并将其转发到与房间名称对应的 group。
在同一 group 中的每个 ChatConsumer (并因此在同一个房间中) 将接收来自该 group 的消息,
通过 WebSocket 将其转发并返回到 JavaScript, 它将会追加到聊天日志中。
"""
"""
代码解释：
1. self.scope[‘url_route’][‘kwargs’][‘room_name’]
    - 从给 consumer 打开 WebSocket 连接的 chat/routes.py 中的 URL 路由中获取 "room_name" 参数
    - 每个 consumer 都有一个 scope, 其中包含有关其连接的信息, 
        特别是来自 URL 路由和当前经过身份验证的用户 (如果有的话) 中的任何位置或关键字参数
    
2. self.room_group_name = ‘chat_%s’ % self.room_name
    - 直接从用户指定的房间名称构造一个 Channels group 名称, 无需任何引用或转义
    - 组名只能包含字母、数字、连字符和句点。因此, 此示例代码将在具有其他字符的房间名称上发生失败

3. async_to_sync(self.channel_layer.group_add)(…)
    - 加入一个 group
    - async_to_sync(…) wrapper 是必需的, 因为 ChatConsumer 是同步 WebsocketConsumer, 
        但它调用的是异步 channel layer 方法。（所有 channel layer 方法都是异步的）
    - group 名称仅限于 ASCII 字母、连字符和句点。由于此代码直接从房间名称构造 group 名称, 
        因此如果房间名称中包含的其他无效的字符, 代码运行则会失败

4. self.accept()
    - 接收 WebSocket 连接
    - 如果你在 connect() 方法中不调用 accept(), 则连接将被拒绝并关闭。
        例如，您可能希望拒绝连接, 因为请求的用户未被授权执行请求的操作
    - 如果你选择接收连接, 建议 accept() 作为在 connect() 方法中的最后一个操作。
    
5. async_to_sync(self.channel_layer.group_discard)(…)
    - 离开一个 group

6. async_to_sync(self.channel_layer.group_send)
    - 将 event 发送到一个 group
    - event 具有一个特殊的键 'type' 对应接收 event 的 consumers 调用的方法的名称
"""



from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

# 允许一个group内多个consumer相互通讯
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


# 第一步 最简单的连接形式
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         self.send(text_data=json.dumps({
#             'message': message
#         }))