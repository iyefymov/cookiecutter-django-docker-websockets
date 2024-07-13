import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Represents a WebSocket consumer for handling chat functionality.

    Attributes:
        room_group_name (str): The name of the room group associated with the consumer.

    Methods:
        connect: Called when the websocket is handshaking as part of the connection process.
        disconnect: Called when the WebSocket closes for any reason.
        receive: Called when a message is received from the WebSocket.
        chat_message: Handles the 'chat_message' event.
    """

    async def connect(self):
        """
        Called when the websocket is handshaking as part of the connection process.
        Adds the channel to the specified room group and accepts the connection.
        """
        self.room_group_name = 'chat_public'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.

        Removes the consumer from the group associated with the room.

        Args:
            close_code (int): The close code sent by the WebSocket client.

        Returns:
            None
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.

        Args:
            text_data (str): The received message data.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        """
        Handles the 'chat_message' event.

        Args:
            event (dict): The event data containing the message.

        Returns:
            None
        """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
