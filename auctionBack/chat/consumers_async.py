"""
聊天室
"""
"""
ChatConsumer 只使用 async-native 库 (Channels 和 channel layer), 特别是它不访问同步的 Django models。
因此, 它可以被改写为异步的而不会变得复杂化

注意：
即使 ChatConsumer 访问 Django models 或其他同步的代码, 它仍然可以将其重写为异步的。
像 asgiref.sync.sync_to_async 和 channels.db.database_sync_to_async
这样的实用工具可以用来从异步 consumer 那里调用同步的代码。
但是, 性能增益将小于仅使用 async-native 库的方式。
"""

"""
这些用于 ChatConsumer 的新代码与原始代码非常相似, 它们具有以下差异:
1.现在 ChatConsumer 继承自 AsyncWebsocketConsumer 而不是 WebsocketConsumer
2.所有方法都是 async def, 而不仅仅是 def
3.await 用于调用执行 I/O 的异步函数
4.在 channel layer 上调用方法时, 不再需要 async_to_sync。
"""
"""
await是一个只能在协程函数中使用的关键字，用于遇到IO操作时挂起 当前协程（任务），
当前协程（任务）挂起过程中 事件循环可以去执行其他的协程（任务），
当前协程IO处理完成时，可以再次切换回来执行await之后的代码
"""



from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('text_data1:',text_data)
        text_data_json = json.loads(text_data)
        print('text_data:',text_data)
        print('text_data:',type(text_data))
        # message = text_data_json['message']
        message = text_data_json

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))