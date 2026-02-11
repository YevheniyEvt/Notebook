import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from agent.models import Message,Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = await sync_to_async(Chat.objects.get)(
            pk=self.chat_pk, user = self.scope["user"]
        )
        self.chat_group_name = f"chat_{self.chat.id}"

        # Join room group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope["user"]
        message = await sync_to_async(Message.objects.create)(
            chat=self.chat,
            user=user,
            is_user_message=True,
            content=text_data_json["message"],
        )
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat.message",
                "message_id": message.id,
            }
        )
        logging.info(f"Send user message to group. ID: {message.id}")
        asyncio.create_task(self.handle_ai_response())

    # Receive message from room group
    async def chat_message(self, event):
        message_id = event["message_id"]
        message = await sync_to_async(Message.objects.select_related("user").get)(
            id=message_id
        )

        html = render_to_string(
            "agent/partials/message.html",
            {"message": message}
        )
        log_msg = 'Send ai message' if message.is_ai_message else 'Send user message'
        logging.info(f"{log_msg}. Message: {message.content[:20]}")
        await self.send(text_data=html)


    async def handle_ai_response(self):
        logging.info("Start generate and save llm_response")
        await self.chat.generate_and_save_llm_response()
        ai_message = await self.chat.get_last_ai_message()

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat.message",
                "message_id": ai_message.id,
            }
        )
        logging.info(f"Send ai message to group. ID: {ai_message.id}")