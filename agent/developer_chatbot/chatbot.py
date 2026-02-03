from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from agent.developer_chatbot.utils.state import StateAgent
from agent.developer_chatbot.utils.nodes import llm_call_router, general_answer, programming_answer, route_decision

load_dotenv("./.env")

router_builder = StateGraph(StateAgent)

router_builder.add_node('llm_call_router', llm_call_router)
router_builder.add_node("general_answer", general_answer)
router_builder.add_node("programming_answer", programming_answer)

router_builder.add_edge(START, 'llm_call_router')
router_builder.add_conditional_edges(
    'llm_call_router',
    route_decision,
    {
        'general_answer': 'general_answer',
        'programming_answer': 'programming_answer'
    }
)
router_builder.add_edge('programming_answer', END)
router_builder.add_edge('general_answer', END)

memory = MemorySaver()
graph = router_builder.compile()