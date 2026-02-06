from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from agent.developer_chatbot.utils.state import StateAgent, Router, MetaData
from agent.developer_chatbot.utils import prompt

def general_answer(state: StateAgent):
    """Generate answer as usually"""
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    result = llm.invoke(state["messages"])
    return {"messages": result}

def programming_answer(state: StateAgent):
    """Generate answer for developer use"""

    llm = ChatOpenAI(model="o4-mini")
    system = [SystemMessage(content=prompt.SYSTEM_PROMPT + prompt.PROGRAM_ANSWER_PROMPT)]
    result = llm.invoke(system + state["messages"])
    return {"messages": result}

def llm_call_router(state: StateAgent):
    """Route the input to the appropriate node"""
    
    llm = ChatOpenAI(model="o3-mini")
    router  = llm.with_structured_output(Router)
    sys_msg = [SystemMessage(content=prompt.SYSTEM_PROMPT + prompt.ROUTER_PROMPT)]
    decision = router.invoke(sys_msg + state["messages"])
    return {"decision": decision.step}

def route_decision(state: StateAgent):
    if state["decision"] == "general":
        return "general_answer"
    elif state["decision"] == "programming":
        return "programming_answer"

def meta_data_router(state: StateAgent):
    """Route the input to the appropriate node"""

    llm = ChatOpenAI(model="o3-mini")
    router  = llm.with_structured_output(Router)
    sys_msg = [SystemMessage(content=prompt.SYSTEM_PROMPT + prompt.META_DATA_ROUTER)]
    decision = router.invoke(sys_msg + state["messages"])
    return {"generate_chat_name": decision.generate_chat_name}

def route_generate_chat_name(state: StateAgent):
    if state["generate_chat_name"]:
        return "namae_for_chat"
    else:
        return "llm_call_router"

def namae_for_chat(state: StateAgent):
    """Generate name for current chat"""

    llm = ChatOpenAI(model="o3-mini")
    llm_with_structured = llm.with_structured_output(MetaData)
    sys_msg = [SystemMessage(content=prompt.SYSTEM_PROMPT + prompt.GENERATE_NAME_FOR_CHAT_PROMPT)]
    decision = llm_with_structured.invoke(sys_msg + state["messages"])
    return { "chat_name": decision.chat_name}