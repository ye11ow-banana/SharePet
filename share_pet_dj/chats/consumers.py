import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer

from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chat_name']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send.sdp',
            },
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send.sdp',
            },
        )

    async def send_sdp(self, event):
        await self.send(text_data=json.dumps({'f': 'f'}))
