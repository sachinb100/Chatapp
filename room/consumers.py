import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Room,Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self,text_data):
        data = json.loads(text_data)
        
        message = data["message"]
        username = data["user"]
        room = data["room"]
        #message = (username + ':' + message)
        await self.save_message(username,room,message)
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'username':username,
                'message':message
            }
        )

    async def chat_message(self,event):
        username = event["user"]
        message = event['message']
        
        
        await self.send(text_data=json.dumps(
            {
                'username':username,
                'message':message
                
            }))
        
    @database_sync_to_async
    def save_message(self,username,room,message):
        user=User.objects.get(username=username)
        room=Room.objects.get(slug=room)

        return   Message.objects.create(user=user,room=room,content=message)