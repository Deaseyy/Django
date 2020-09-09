"""
点对点聊天，消息推送
聊天室和点对点区别：
聊天室指定一个公用的房间名roomName（group_name）
点对点指定一个专用的房间名：user1.id_user2.id（group_name）
"""
import json

"""
1.采用user_a的id加上下划线_加上user_b的id的方式来命名聊天组名  123_124
2.当用户通过ws/chat/group_name/的方式向服务端请求连接时，
  后端会把这个聊天组的信息放入一个字典里。当连接关闭时，就把聊天组从字典里移除。
3.接着，我们需要判断连接这个聊天组的用户个数。当有两个用户连接这个聊天组时，
  我们就直接向这个聊天组发送信息。当只有一个用户连接这个聊天组时，
  我们就通过push/xxx/把信息发给接收方。
4.chats是一个字典，用来记录每一个group中的连接数目。
  每当一个客户端访问正确的websocket url之后，都会调用connect()函数，
  将该客户端添加入其url中指向的一个group，同时向chats中添加该客户端的信息。
  当该客户端断开连接时，会调用disconnect()函数，将该客户端从group中移除，同时删除它在chats中的记录。
"""

from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    chats = dict()
    async def connect(self):
        # 获取ws请求url中用户传递的组名
        print(self.scope)
        print(self.scope['url_route'])
        print(self.scope['path'])
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        # 新建一个group（使用用户url后的组名:user_a.id_user_b.id）
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # 将用户添加至聊天信息charts中 (key为组名，value为用户(定义为一个集合))
        try:
            ChatConsumer.chats[self.group_name].add(self)  # 向指定组(group已存在于chats)添加当前用户
        except:
            ChatConsumer.chats[self.group_name] = set([self])  # 向指定组(group还不存在)添加当前用户

        # 创建连接时调用, 该语句一般放在最后
        await self.accept()

    async def disconnect(self, close_code):
        """连接关闭时调用"""
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        # 将该客户端移出聊天信息组
        ChatConsumer.chats[self.group_name].remove(self)
        await self.close()

    async def receive_json(self, message, **kwargs):
        """收到信息时调用"""
        print(message, kwargs)
        to_user = message.get('to_user')
        # 信息发送
        length = len(ChatConsumer.chats[self.group_name])
        # 聊天组用户数等于2，直接发送消息到group
        print('组中已连接人数：',length)
        if length == 2:
            # 发送信息到group组
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',  # 自定义事件处理函数
                    'message': message
                }
            )
        # # 否则 使用push推送给指定用户
        # else:
        #     await self.channel_layer.group_send(
        #         to_user,
        #         {
        #             'type': 'push.message',
        #             'event': {'message':message, 'group':self.group_name}
        #         }
        #     )

    async def chat_message(self, event):
        """处理 ‘chat.message’ 事件"""
        # Send message to WebSocket
        print('event:',event)
        await self.send_json({
            'message': event['message']
        })


class PushConsumer(AsyncWebsocketConsumer):
    """消息推送consumer"""
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def push_message(self, event):
        """处理‘push.message’ 事件"""
        print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'event': event['event']
        }))