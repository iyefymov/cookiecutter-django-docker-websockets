import os
from unittest.mock import patch

import pytest
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


@pytest.mark.asyncio
class TestChatConsumer:
    async def asyncSetUp(self):
        self.consumer = ChatConsumer()
        self.communicator = await self.create_communicator()

    async def create_communicator(self):
        communicator = WebsocketCommunicator(self.consumer, "/ws/chat/")
        communicator.scope["url_route"] = {"kwargs": {"room_name": "chat_public"}}
        return communicator

    @patch('channels_redis.core.RedisChannelLayer.group_add')
    @patch('channels_redis.core.RedisChannelLayer.group_discard')
    async def test_connect(self, mock_group_discard, mock_group_add):
        await self.asyncSetUp()
        connected, _ = await self.communicator.connect()
        assert connected

        # Verify that the connection is added to the group
        group_name = "chat_public"
        channel_layer = self.consumer.channel_layer
        await channel_layer.group_add(group_name, self.consumer.channel_name)
        mock_group_add.assert_called_with(group_name, self.consumer.channel_name)

        await self.communicator.disconnect()

        # Verify that the connection is removed from the group
        await channel_layer.group_discard(group_name, self.consumer.channel_name)
        mock_group_discard.assert_called_with(group_name, self.consumer.channel_name)

    async def test_receive(self):
        await self.asyncSetUp()
        await self.communicator.connect()
        message = {"message": "Hello, world!"}
        await self.communicator.send_json_to(message)
        response = await self.communicator.receive_json_from()
        assert response == message

    async def test_chat_message(self):
        await self.asyncSetUp()
        await self.communicator.connect()
        message = {"message": "Hello, world!"}
        await self.consumer.chat_message(message)
        response = await self.communicator.receive_json_from()
        assert response == message
