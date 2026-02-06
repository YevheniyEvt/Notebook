from typing_extensions import Literal
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState


class Router(BaseModel):
    step: Literal["general", "programming"] = Field(
        None, description="The next step in the routing process"
    )
    generate_chat_name: bool = Field(default=False, description="Generate a chat name or not")


class MetaData(BaseModel):
    chat_name: str = Field(description="The name of the chat")

class StateAgent(MessagesState):
    decision: str
    chat_name: str
    generate_chat_name: bool
