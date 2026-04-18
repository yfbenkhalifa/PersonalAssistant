from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from personal_assistant_agent.agent import Agent, create_llm_config_from_yaml, load_config

load_dotenv()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: str


class ChatRuntime:
    def __init__(self, config_path: str | Path):
        self.config_path = str(config_path)
        self.agents: dict[str, Agent] = {}

    def create_agent(self) -> Agent:
        config = load_config(self.config_path)
        agent_config = create_llm_config_from_yaml(config)
        return Agent(agent_config)

    def get_or_create_agent(self, conversation_id: str) -> Agent:
        agent = self.agents.get(conversation_id)
        if agent is None:
            agent = self.create_agent()
            self.agents[conversation_id] = agent
        return agent


DEFAULT_CONFIG_PATH = Path(
    os.getenv(
        "PERSONAL_ASSISTANT_AGENT_CONFIG",
        str(Path(__file__).resolve().parents[2] / "config.yaml"),
    )
)
runtime = ChatRuntime(DEFAULT_CONFIG_PATH)


def create_app(chat_runtime: ChatRuntime | None = None) -> FastAPI:
    app = FastAPI(
        title="Personal Assistant Chat API",
        description="Chat API with REST and WebSocket support",
        version="1.0.0",
    )
    local_runtime = chat_runtime or runtime

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "message": "Personal Assistant Chat API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "chat": "/api/chat",
                "websocket": "/ws/{conversation_id}",
            },
        }

    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "active_agents": {
                "count": len(local_runtime.agents),
                "conversation_ids": list(local_runtime.agents.keys()),
            },
        }

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        try:
            conversation_id = request.conversation_id or "default"
            agent = local_runtime.get_or_create_agent(conversation_id)
            response = agent.invoke(HumanMessage(content=request.message))
            return ChatResponse(
                message=str(response.content),
                conversation_id=conversation_id,
                timestamp=datetime.now().isoformat(),
            )
        except Exception as exc:  # pragma: no cover - runtime boundary
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.delete("/api/chat/{conversation_id}")
    async def clear_conversation(conversation_id: str):
        if conversation_id in local_runtime.agents:
            del local_runtime.agents[conversation_id]
            return {"message": f"Conversation {conversation_id} cleared"}
        return {"message": "Conversation not found"}

    @app.websocket("/ws/{conversation_id}")
    async def websocket_chat(websocket: WebSocket, conversation_id: str):
        await websocket.accept()
        agent = local_runtime.get_or_create_agent(conversation_id)
        try:
            while True:
                payload = await websocket.receive_json()
                user_message = payload.get("message", "")
                if not user_message:
                    continue

                await websocket.send_json(
                    {
                        "type": "ack",
                        "message": "Processing...",
                        "timestamp": datetime.now().isoformat(),
                    }
                )
                response = agent.invoke(HumanMessage(content=user_message))
                await websocket.send_json(
                    {
                        "type": "response",
                        "message": str(response.content),
                        "timestamp": datetime.now().isoformat(),
                    }
                )
        except WebSocketDisconnect:
            return
        except Exception as exc:  # pragma: no cover - runtime boundary
            await websocket.send_json(
                {
                    "type": "error",
                    "message": f"Error: {exc}",
                    "timestamp": datetime.now().isoformat(),
                }
            )
            await websocket.close()

    return app


app = create_app()


