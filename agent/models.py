from collections.abc import Generator

import markdown
import bleach
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User
from django.db import models

from agent.constants import ALLOWED_TAGS, ALLOWED_ATTRS, COUNT_MESSAGES_SEND_TO_LLM
from langchain_core.messages import AIMessage, HumanMessage
from agent.developer_chatbot.chatbot import graph as chatbot


class Chat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name or f'Chat #{self.id}'

    def generate_stream_response_from_llm(self) -> Generator[str, None, None]:
        messages_content = self._get_messages_for_llm()
        llm_stream_answer = chatbot.stream({'messages': messages_content}, stream_mode="messages")
        for message_chunk, metadata in llm_stream_answer:

            # Skip system messages
            if metadata["langgraph_node"] == "llm_call_router" or metadata["langgraph_node"] == "categorize_request":
                continue
            if message_chunk.content:
                yield message_chunk.content

    async def generate_and_save_llm_response(self) -> dict:
        llm_response = await self._send_messages_and_get_response_from_llm()
        # get last message in list - it is last answer from LLM
        llm_message_content = llm_response['messages'][-1].content
        await self._save_ai_message(llm_message_content)
        return llm_response

    async def _send_messages_and_get_response_from_llm(self) -> dict:
        messages_content = await self._get_messages_for_llm()
        llm_response = await chatbot.ainvoke({'messages': messages_content})
        return llm_response

    @sync_to_async
    def _get_messages_for_llm(self) -> list[AIMessage | HumanMessage]:
        """Get last `count_messages` messages and reverse it for right order for LLM"""

        # Need reverse to have correct order for LLM
        messages = list(self.messages.order_by('-created_at')[:COUNT_MESSAGES_SEND_TO_LLM][::-1])
        messages_content = [
            HumanMessage(content=message.content)
            if message.is_user_message
            else AIMessage(content=message.content)
            for message in messages
        ]
        return messages_content

    @sync_to_async
    def _save_ai_message(self, content: str):
        Message.objects.create(
            chat=self,
            user=self.user,
            is_ai_message=True,
            content=content,
        )

    @sync_to_async
    def get_last_ai_message(self):
        return Message.objects.filter(
            chat=self,
            is_ai_message=True
        ).last()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ai_message = models.BooleanField(default=False)
    is_user_message = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:10]

    def save(self, *args, **kwargs):
        # render markdown → HTML
        html = markdown.markdown(
            self.content,
            extensions=['fenced_code', 'codehilite']
        )
        clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
        self.html_content = clean_html
        super().save(*args, **kwargs)