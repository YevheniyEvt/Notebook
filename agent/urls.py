from django.urls import path

from agent.views import (
    ChatCreateView,
    ChatDetailView,
    MessageCreateView,
    ChatListView,
    ChatDeleteView,
    get_ws_message_form,
)

app_name = "chatbot"

urlpatterns = [
    path("chats/", ChatListView.as_view(), name="chat_list"),
    path("chat/create/", ChatCreateView.as_view(), name="chat_create"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="chat_detail"),
    path("chat/<int:pk>/delete", ChatDeleteView.as_view(), name="chat_delete"),

    # path('chat/<int:pk>/stream/', chat_stream, name='chat_stream'),

    # path("chat/<int:pk>/message/create/", MessageCreateView.as_view(), name="messages_create"),
    # path("chat/<int:pk>/message/create/", get_ws_message_form, name="messages_create"),
]