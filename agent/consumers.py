import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.template.loader import render_to_string

from agent.models import Message,Chat
from notebook import settings

class ChatConsumer(AsyncWebsocketConsumer):
    """Generate connection with group.
    From LLM returned one piece of full html
    Messages to frontend send as HTML
    """

    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = await Chat.objects.aget(
            pk=self.chat_pk, user = self.scope["user"]
        )
        self.chat_group_name = f"chat_{self.chat.id}"
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = self.scope["user"]
        message = await Message.objects.acreate(
            chat=self.chat,
            user=user,
            is_user_message=True,
            content=text_data_json["message"],
        )

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat.message",
                "message_id": message.id,

            }
        )
        logging.info(f"Send user message to group. ID: {message.id}")
        asyncio.create_task(self.handle_ai_response())

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


class ChatStreamConsumer(AsyncJsonWebsocketConsumer):
    """Generate connection with one socket.
    From LLM returned chunks with HTML marked answer
    Messages to frontend send as a JSON
    """

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

        html_content = await sync_to_async(render_to_string)(
            "agent/partials/user_message.html",
            {"message": message}
        )
        data = {
            "type": "user_message",
            "html_content": html_content,
            "message_id": message.id,
        }
        await self.send_json(data)

    async def handle_ai_response(self):
        logging.info("Start generate and save llm_response")
        message = await Message.objects.acreate(
            chat=self.chat,
            user=self.user,
            is_ai_message=True,
        )
        ai_message_html_container = await sync_to_async(render_to_string)(
            "agent/partials/ai_message_container.html",
            {"message_id": message.id}
        )

        accumulate_message_content = ''
        send_container = False

        try:
            llm_stream_answer = self.chat.generate_stream_response_from_llm()
        except Exception as exc:
            logging.error(f"AI streaming failed: {exc}", exc_info=True)
            if settings.DEBUG:
                await self.send(text_data=json.dumps({"type": "ai_error", "error": str(exc)}))
        else:
            async for content in llm_stream_answer:
                if not send_container:
                    await self.send(text_data=ai_message_html_container)
                    send_container = True

                data = {
                    "type": "ai_chunk",
                    "chunk": content,
                    "message_id": message.id,
                }
                await self.send_json(data)
                accumulate_message_content += content

            done = {
                "type": "ai_done"
            }
            await self.send_json(done)
            logging.info(f"Streaming message finished.")

            message.html_content = accumulate_message_content
            await message.asave()


