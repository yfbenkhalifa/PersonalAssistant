from fastapi import FastAPI
from global_settings import global_settings
from langchain_core.messages import HumanMessage, AIMessage
from server import startup

graph = startup.graph
elasticsearch_client = startup.elasticsearch_client
document_indexer_settings = startup.appSettings

app = FastAPI(
    title=global_settings.API_TITLE,
    description=global_settings.API_DESCRIPTION,
    version=global_settings.API_VERSION
)

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
        "host": document_indexer_settings.ELASTICSEARCH_HOST
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

    import uvicorn
    uvicorn.run(app, host=global_settings.HOST, port=global_settings.PORT)