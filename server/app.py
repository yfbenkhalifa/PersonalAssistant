from fastapi import FastAPI
from langchain_core.messages import HumanMessage, AIMessage
from loguru import logger
from langchain.chat_models import init_chat_model
import chatbot.state_graph as state_graph
from langgraph.graph import START, END
from langgraph.prebuilt import ToolNode

from chatbot.tools import (
    query_lenght,
    route_tools,
    search_indexed_documents
)
from langchain_core.messages import SystemMessage

from prompts.agent_prompts import AgentPrompts
from elasticsearch_client.clients.elasticsearch_client import ElasticSearchClient
from exceptions.serverExceptions import ServerException
from elasticsearch_client.appSettings import AppSettings

llm = init_chat_model(
    model="qwen/qwen3-coder-30b",
    model_provider="openai",
    base_url="http://localhost:25000/v1/",
    api_key="lm-studio"
)

tools = [
    query_lenght,
    search_indexed_documents
]

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

graph_builder = state_graph.graph_builder

def chatbot(state: state_graph.State):
    """Chatbot node with structured prompt template"""
    messages = state["messages"]

    # Use the prompt template to format messages with system instructions
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        # Add system message if not present
        system_msg = AgentPrompts.get_system_message()
        messages = [system_msg] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Add conditional edges for tool routing
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools
)

# Build the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


APPSETTINGS = AppSettings()

try:
    elasticsearch_client = ElasticSearchClient(
        host=APPSETTINGS.ELASTICSEARCH_HOST,
        port=APPSETTINGS.ELASTICSEARCH_PORT,
        user=APPSETTINGS.ELASTICSEARCH_USERNAME,
        password=APPSETTINGS.ELASTICSEARCH_PASSWORD,
        api_key=APPSETTINGS.ELASTICSEARCH_API_KEY
    )
except ServerException as e:
    print(f"Error initializing Elasticsearch client: {e}")

app = FastAPI(
    title=APPSETTINGS.API_TITLE,
    description=APPSETTINGS.API_DESCRIPTION,
    version=APPSETTINGS.API_VERSION
)

app_logger = logger.bind(app=app)

def stream_graph_updates(user_input: str):
    try:
        response = []
        # Create the input in the correct format for the graph
        input_data = {"messages": [HumanMessage(content=user_input)]}
        
        # Stream the graph execution
        for event in graph.stream(input_data):
            for value in event.values():
                if "messages" in value and value["messages"]:
                    last_message = value["messages"][-1]
                    if isinstance(last_message, AIMessage):
                        response.append(last_message.content)
        
        return response
    except Exception as e:
        return [f"Error processing request: {str(e)}"]


    
@app.get("/health")
async def health_check():
    """Check the health of the API and Elasticsearch connection"""
    es_healthy = elasticsearch_client.health_check()
    return {
        "status": "healthy" if es_healthy else "unhealthy",
        "elasticsearch": "connected" if es_healthy else "disconnected",
        "host": APPSETTINGS.ELASTICSEARCH_HOST
    }

@app.get("/api/v1/invoke")
async def invoke(query: str):
    user_input = query
    result = stream_graph_updates(user_input)
    last_message = result[-1] if result else ""
    return {"response": last_message}

@app.get("/api/v1/documents/{index_id}")
async def get_document(index_id: str):
    result = elasticsearch_client.client.search(index=index_id, body={"query": {"match_all": {}}})
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APPSETTINGS.HOST, port=APPSETTINGS.PORT)