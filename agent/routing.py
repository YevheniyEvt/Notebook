from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<int:pk>/", consumers.ChatConsumer.as_asgi(), name="ws_chat"),
    path("ws/chat/<int:pk>/stream/", consumers.ChatStreamConsumer.as_asgi(), name="ws_chat_stream"),
]