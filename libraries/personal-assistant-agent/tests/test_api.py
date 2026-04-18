import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from personal_assistant_agent.api import ChatRuntime, create_app


class StubAgent:
    def __init__(self):
        self.received = []

    def invoke(self, message):
        self.received.append(message.content)
        return AIMessage(content=f"echo:{message.content}")


class StubRuntime(ChatRuntime):
    def __init__(self):
        super().__init__(config_path="unused.yaml")
        self.created = 0

    def create_agent(self):
        self.created += 1
        return StubAgent()


def test_chat_route_creates_and_reuses_agent():
    runtime = StubRuntime()
    client = TestClient(create_app(runtime))

    first = client.post("/api/chat", json={"message": "hello", "conversation_id": "abc"})
    second = client.post("/api/chat", json={"message": "again", "conversation_id": "abc"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["message"] == "echo:hello"
    assert second.json()["message"] == "echo:again"
    assert runtime.created == 1


def test_clear_conversation_removes_cached_agent():
    runtime = StubRuntime()
    client = TestClient(create_app(runtime))

    client.post("/api/chat", json={"message": "hello", "conversation_id": "to-clear"})
    response = client.delete("/api/chat/to-clear")

    assert response.status_code == 200
    assert response.json()["message"] == "Conversation to-clear cleared"
    assert "to-clear" not in runtime.agents


def test_health_route_reports_agent_count():
    runtime = StubRuntime()
    runtime.agents["one"] = StubAgent()
    runtime.agents["two"] = StubAgent()
    client = TestClient(create_app(runtime))

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["active_agents"]["count"] == 2
    assert set(payload["active_agents"]["conversation_ids"]) == {"one", "two"}


