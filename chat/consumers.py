import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import Chat, Message

class ChatConsumer(WebsocketConsumer):

    def can_comunicate(self):
        return self.chat.user_is_part_of(self.user)

    def connect(self):
        self.user = self.scope['user']
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = Chat.objects.get(pk=chat_id)
        if not self.can_comunicate():
            return
        self.room_group_name = str(self.chat.id)


        # print(self.chat)
        # print(type(self.user), self.user)
        # print('path =', self.scope['path'])
        # print('url_route =', self.scope['url_route'])
        print(self.channel_layer)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        m = Message.objects.create(text=message, sender=self.user, chat=self.chat)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'sender': m.sender.username
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message,
            'sender': sender
        }))