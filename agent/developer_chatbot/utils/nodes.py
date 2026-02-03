from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from agent.developer_chatbot.utils.state import StateAgent, Router
from agent.developer_chatbot.utils.prompt import SYSTEM_PROMPT, PROGRAM_ANSWER_PROMPT, ROUTER_PROMPT


def general_answer(state: StateAgent):
    """Generate answer as usually"""
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    result = llm.invoke(state["messages"])
    return {"messages": result}


def programming_answer(state: StateAgent):
    """Generate answer for developer use"""

    llm = ChatOpenAI(model="o4-mini")
    system = [SystemMessage(content=SYSTEM_PROMPT + PROGRAM_ANSWER_PROMPT)]
    result = llm.invoke(system + state["messages"])
    return {"messages": result}


def llm_call_router(state: StateAgent):
    """Route the input to the appropriate node"""
    
    llm = ChatOpenAI(model="o3-mini")
    router  = llm.with_structured_output(Router)
    sys_msg = [SystemMessage(content=SYSTEM_PROMPT + ROUTER_PROMPT)]
    decision = router.invoke(sys_msg + state["messages"])
    return {"decision": decision.step}

def route_decision(state: StateAgent) -> str:
    if state["decision"] == "general":
        return "general_answer"
    elif state["decision"] == "programming":
        return "programming_answer"
    
    