from agent.developer_chatbot.chatbot import graph as chatbot
from agent.models import Message

def llm_response_generator(chat):
    messages = Message.objects.filter(chat=chat)[:8]
    messages_content = [message.content for message in messages]
    llm_answer = chatbot.invoke({"role": "user", "messages": messages_content})
    return llm_answer

    # for message_chunk, metadata in stream:
    #     if metadata["langgraph_node"] == "llm_call_router" or metadata["langgraph_node"] == "categorize_request":
    #         continue
    #     if message_chunk.content:
    #         yield message_chunk.content
