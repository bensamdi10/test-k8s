import json
from channels.generic.websocket import AsyncWebsocketConsumer
from backend.factory import Factory
from asgiref.sync import sync_to_async

class CliConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.cli = "cli"  #self.scope['url_route']['kwargs']['token']
        self.cli_name = 'cli_%s' % self.cli

        # Join room group
        await self.channel_layer.group_add(
            self.cli_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.cli_name,
            self.channel_name
        )


    # Receive message from WebSocket

    async def receive(self, text_data):
        #text_data_json = json.loads(text_data)
        cli = text_data
        # Send message to room group
        await self.channel_layer.group_send(
            self.cli_name,
            {
                'type': 'cli_message',
                'cli': cli
            }
        )


    # Receive message from room group

    async def cli_message(self, event):
        cli = event['cli']
        # Send message to WebSocket
        cli_data = json.loads(cli)

        await self.send(text_data=json.dumps({
            'uid': cli_data["uid"],
            'action': cli_data["action"],
            "output" : cli_data["output"],
            "input" : cli_data["input"],
            "output_errors" : cli_data["output_errors"],
            "workdir" : cli_data["workdir"],
            "finish_output" : cli_data["finish_output"],
            "context" : cli_data["context"]
        }))