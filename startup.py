import os
from langchain.chat_models import init_chat_model
import chatbot.state_graph as state_graph
from langgraph.graph import StateGraph, START, END


llm = init_chat_model(
    model="qwen/qwen3-coder-30b",
    model_provider="openai",
    base_url="http://10.5.0.2:25000/v1",  # Your local server URL
    api_key="not-needed"  # Local servers often don't require real API keys
)

graph_builder = state_graph.graph_builder

def chatbot(state: state_graph.State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()