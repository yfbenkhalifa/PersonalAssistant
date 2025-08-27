import os
from langchain.chat_models import init_chat_model
import chatbot.state_graph as state_graph
from langgraph.graph import StateGraph, START, END

from chatbot.tools import BasicToolNode, route_tools, query_lenght

# Initialize your local LLM
llm = init_chat_model(
    model="qwen/qwen3-coder-30b",
    model_provider="openai",
    base_url="http://localhost:25000/v1/",
    api_key="lm-studio"
)

# Bind tools to the LLM
llm_with_tools = llm.bind_tools([query_lenght])

graph_builder = state_graph.graph_builder

def chatbot(state: state_graph.State):
    # Use the LLM with tools instead of the base LLM
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Set up tool node
tool_node = BasicToolNode(tools=[query_lenght])
graph_builder.add_node("tools", tool_node)

# Add conditional edges for tool routing
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)

# Build the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()