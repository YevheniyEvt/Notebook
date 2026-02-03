from typing_extensions import Literal
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState


class Router(BaseModel):
    step: Literal["general", "programming"] = Field(
        None, description="The next step in the routing process"
    )


class StateAgent(MessagesState):
    decision: str
