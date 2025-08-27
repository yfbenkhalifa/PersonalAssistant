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
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            yield ("Assistant:", value["messages"][-1].content)

    
@app.get("/health")
async def health_check():
    return {"status": "ok"} if graph is not None else {"status": "error", "message": "Agent not initialized"}

@app.get("/api/v1/invoke")
async def invoke(query: str):
    user_input = query
    result = stream_graph_updates(user_input)
    return {"response": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=global_settings.HOST, port=global_settings.PORT)