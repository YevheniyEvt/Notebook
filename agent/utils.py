from langchain_core.messages import AIMessage, HumanMessage
from agent.developer_chatbot.chatbot import graph as chatbot
from agent.models import Message

def generate_llm_response(chat, stream=False):
    # Get last 8 messages and reverse it for right order for LLM
    messages = list(Message.objects.filter(chat=chat).order_by('-created_at')[:8][::-1])
    messages_content = [
        HumanMessage(content=message.content)
        if message.is_user_message
        else AIMessage(content=message.content)
        for message in messages
    ]
    if stream:
        return stream_answer(messages_content)

    llm_answer = chatbot.invoke({'messages': messages_content})
    return llm_answer

def stream_answer(messages_content):
    llm_stream_answer = chatbot.stream({'messages': messages_content}, stream_mode="messages")
    for message_chunk, metadata in llm_stream_answer:
        if metadata["langgraph_node"] == "llm_call_router" or metadata["langgraph_node"] == "categorize_request":
            continue
        if message_chunk.content:
            yield f"event: message\ndata: {message_chunk.content}\n\n"