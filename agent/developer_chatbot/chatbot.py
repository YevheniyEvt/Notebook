from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from agent.developer_chatbot.utils.state import StateAgent
from agent.developer_chatbot.utils import nodes

load_dotenv("./.env")

router_builder = StateGraph(StateAgent)

router_builder.add_node('meta_data_router', nodes.meta_data_router)
router_builder.add_node('namae_for_chat', nodes.namae_for_chat)

router_builder.add_node('llm_call_router', nodes.llm_call_router)
router_builder.add_node("general_answer", nodes.general_answer)
router_builder.add_node("programming_answer", nodes.programming_answer)

router_builder.add_edge(START, 'meta_data_router')
router_builder.add_conditional_edges(
    'meta_data_router',
    nodes.route_generate_chat_name,
    {
        'namae_for_chat': 'namae_for_chat',
        'llm_call_router': 'llm_call_router'
    }
)
router_builder.add_edge('namae_for_chat', 'llm_call_router')
router_builder.add_conditional_edges(
    'llm_call_router',
    nodes.route_decision,
    {
        'general_answer': 'general_answer',
        'programming_answer': 'programming_answer'
    }
)
router_builder.add_edge('programming_answer', END)
router_builder.add_edge('general_answer', END)

memory = MemorySaver()
graph = router_builder.compile()