import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BackendConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.env = self.scope['url_route']['kwargs']['env']
        self.env_name= 'env_%s' % self.env

        # Join room group
        await self.channel_layer.group_add(
            self.env_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.env_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.env_name,
            {
                'type': 'env_message',
                'message': message
            }
        )

    # Receive message from room group
    async def env_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


