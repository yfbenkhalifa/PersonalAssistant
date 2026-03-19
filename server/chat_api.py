"""
FastAPI Chat API for Personal Assistant
Provides REST and WebSocket endpoints for the chat interface
"""
import sys
from pathlib import Path

# Add src folder to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from agents.agent import Agent, AzureOpenAiModelConfig, AgentConfig
from agents.enums import LLM_MODEL, LLM_PROVIDER
from langchain_core.messages import HumanMessage, AIMessage
import yaml

# Load environment variables
load_dotenv()


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    conversation_id: str
    timestamp: str


# Initialize FastAPI app
app = FastAPI(
    title="Personal Assistant Chat API",
    description="Chat API with REST and WebSocket support",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_agent() -> Agent:
    """Create and initialize the Agent"""
    config = load_config()
    llm_cfg = config['model']
    provider = LLM_PROVIDER[llm_cfg['provider']]
    
    if provider == LLM_PROVIDER.AZURE_OPENAI:
        agent_config = AzureOpenAiModelConfig(
            host=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model=LLM_MODEL[llm_cfg['model']],
            temperature=llm_cfg['temperature'],
            provider=provider,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=llm_cfg.get('apiVersion', '2024-12-01-preview')
        )
    else:
        agent_config = AgentConfig(
            host=llm_cfg['host'],
            model=LLM_MODEL[llm_cfg['model']],
            temperature=llm_cfg['temperature'],
            provider=provider
        )
    
    return Agent(agent_config)


# Store active agents per session (in production, use Redis or similar)
agents = {}


def get_or_create_agent(conversation_id: str) -> Agent:
    """Get existing agent or create new one for conversation"""
    if conversation_id not in agents:
        agents[conversation_id] = create_agent()
    return agents[conversation_id]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Personal Assistant Chat API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat",
            "websocket": "/ws/{conversation_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for REST API
    Send a message and get a response
    """
    try:
        conversation_id = request.conversation_id or "default"
        agent = get_or_create_agent(conversation_id)
        
        # Create message and invoke agent
        message = HumanMessage(content=request.message)
        response = agent.invoke(message)
        
        return ChatResponse(
            message=response.content,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/chat/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation (delete agent instance)"""
    if conversation_id in agents:
        del agents[conversation_id]
        return {"message": f"Conversation {conversation_id} cleared"}
    return {"message": "Conversation not found"}


@app.websocket("/ws/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: str):
    """
    WebSocket endpoint for real-time chat
    Supports streaming responses
    """
    await websocket.accept()
    agent = get_or_create_agent(conversation_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "ack",
                "message": "Processing...",
                "timestamp": datetime.now().isoformat()
            })
            
            try:
                # Invoke agent
                message = HumanMessage(content=user_message)
                response = agent.invoke(message)
                
                # Send response
                await websocket.send_json({
                    "type": "response",
                    "message": response.content,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        print(f"Client disconnected from conversation: {conversation_id}")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "chat_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
