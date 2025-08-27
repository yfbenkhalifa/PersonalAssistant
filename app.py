from fastapi import FastAPI
from chatbot.state_graph import State
from global_settings import global_settings
from langgraph.prebuilt import create_react_agent
import chatbot.state_graph as state_graph
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
import startup

graph = startup.graph

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
    return {"status": "ok"} if graph is not None else {"status": "error", "message": "Agent not initialized"}

@app.get("/api/v1/invoke")
async def invoke(query: str):
    user_input = query
    result = stream_graph_updates(user_input)
    last_message = result[-1] if result else ""
    return {"response": last_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=global_settings.HOST, port=global_settings.PORT)