from typing import AsyncIterator

from asgiref.sync import sync_to_async
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer, JavaLexer, MarkdownLexer
from pygments.formatters import HtmlFormatter

from django.contrib.auth.models import User
from django.db import models

from agent.constants import COUNT_MESSAGES_SEND_TO_LLM
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

    async def generate_stream_response_from_llm(self)  -> AsyncIterator[str]:
        messages_content = await self._get_messages_for_llm()
        llm_stream_answer = chatbot.astream({'messages': messages_content}, stream_mode="messages")

        async for message_chunk, metadata in llm_stream_answer:
            node = metadata.get('langgraph_node')
            if node == "namae_for_chat":
                parsed = message_chunk.additional_kwargs.get('parsed')
                chat_name = getattr(parsed, 'chat_name', None)
                if chat_name:
                    await self._save_chat_name(chat_name)
                continue

            # Skip internal messages
            if node in ('llm_call_router', 'namae_for_chat', 'meta_data_router'):
                continue

            content = getattr(message_chunk, 'content', None)
            if content:
                yield content

    async def generate_and_save_llm_response(self) -> dict:
        llm_response = await self._send_messages_and_get_response_from_llm()
        chat_name_from_llm = llm_response.get('chat_name')
        if chat_name_from_llm:
            await self._save_chat_name(chat_name_from_llm)

        # get last message in list - it is last answer from LLM
        messages = llm_response.get('messages')
        if not messages:
            raise ValueError("LLM returned no messages")
        last_message = messages[-1]
        content = getattr(last_message, 'content', None)
        if not content:
            raise ValueError("Last LLM message has no content")

        await Message.objects.acreate(
            chat=self,
            user_id=self.user_id,
            is_ai_message=True,
            content=content,
        )
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

    async def _save_chat_name(self, chat_name_from_llm):
        if not self.name:
            self.name = chat_name_from_llm
            await self.asave(update_fields=["name"])


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
        if self.content:
            html = highlight(self.content, PythonLexer(), HtmlFormatter(cssclass="highlight p-2"))
            self.html_content = html
        super().save(*args, **kwargs)