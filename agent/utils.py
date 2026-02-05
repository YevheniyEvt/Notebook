from langchain_core.messages import AIMessage, HumanMessage
from agent.developer_chatbot.chatbot import graph as chatbot
from agent.models import Message

def llm_response_generator(chat):
    # Get last 8 messages and reverse it for right order for LLM
    messages = list(Message.objects.filter(chat=chat).order_by('-created_at')[:8][::-1])
    messages_content = [
        HumanMessage(content=message.content)
        if message.is_user_message
        else AIMessage(content=message.content)
        for message in messages
    ]

    llm_answer = chatbot.invoke({'messages': messages_content})
    return llm_answer

    # for message_chunk, metadata in stream:
    #     if metadata["langgraph_node"] == "llm_call_router" or metadata["langgraph_node"] == "categorize_request":
    #         continue
    #     if message_chunk.content:
    #         yield message_chunk.content
