import asyncio
import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from agent.models import Message,Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = await Chat.objects.aget(
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
        message = await Message.objects.acreate(
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
        message = await Message.objects.aget(id=message_id)

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
        ai_message = await Message.objects.filter(
            chat=self.chat,
            is_ai_message=True
        ).alast()

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat.message",
                "message_id": ai_message.id,
            }
        )
        logging.info(f"Send ai message to group. ID: {ai_message.id}")


class ChatStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = await Chat.objects.aget(
            pk=self.chat_pk, user = self.scope["user"]
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.user = self.scope["user"]
        message = await Message.objects.acreate(
            chat=self.chat,
            user=self.user,
            is_user_message=True,
            content=text_data_json["message"],
        )
        asyncio.create_task(self.handle_ai_response())
        logging.info(f"Send user message. ID: {message.id}")

        html = render_to_string(
            "agent/partials/user_message.html",
            {"message": message}
        )
        await self.send(text_data=html)


    async def handle_ai_response(self):
        logging.info("Start generate and save llm_response")
        llm_stream_answer = self.chat.generate_stream_response_from_llm()
        message = await Message.objects.acreate(
            chat=self.chat,
            user=self.user,
            is_ai_message=True,
        )
        ai_message_html_container = render_to_string(
            "agent/partials/ai_message_container.html",
            {"message_id": message.id}
        )

        send_container = False
        accumulate_message_content = ''
        async for content in llm_stream_answer:
            if not send_container:
                await self.send(text_data=ai_message_html_container)
                send_container = True

            html = render_to_string(
                "agent/partials/ai_message_chunk.html",
                {"content": content, "message_id": message.id}
            )
            await self.send(text_data=html)
            accumulate_message_content += content
        logging.info(f"Streaming message finished.")

        message.content = accumulate_message_content
        await message.asave()

