"""LangGraph tool nodes and built-in tools for the Personal Assistant agent.

The Elasticsearch-backed ``search_indexed_documents`` tool is only functional
when the ``personal-assistant-elasticsearch`` package is installed (optional
``elasticsearch`` extra) and a client is attached via
:func:`set_elasticsearch_client`.
"""

from __future__ import annotations

import json
from typing import Any, Callable, List, Optional

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.graph import END

from personal_assistant_agent.graph.state import State

_es_client: Optional[Any] = None


def set_elasticsearch_client(client: Any) -> None:
    """Register a module-level Elasticsearch client for use by the tool."""
    global _es_client
    _es_client = client


class BasicToolNode:
    """A node that runs the tools requested in the last ``AIMessage``."""

    def __init__(self, tools: List[Callable[..., Any]]) -> None:
        self.tools_by_name = {t.name: t for t in tools}

    def __call__(self, inputs: dict) -> dict:
        messages = inputs.get("messages", [])
        if not messages:
            raise ValueError("No message found in input")

        message = messages[-1]
        outputs = []
        for tool_call in getattr(message, "tool_calls", []):
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


def route_tools(state: State):
    """Conditional edge: route to ``tools`` if the last AI message has tool calls."""
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


@tool("query_length")
def query_length(query: str) -> int:
    """Return the character length of the user's query."""
    return len(query)


@tool("search_indexed_documents")
def search_indexed_documents(query: str) -> list | None:
    """Search indexed documents, WhatsApp conversations, and personal information.

    A client must be registered via :func:`set_elasticsearch_client` before
    invocation; otherwise the tool returns ``None``.
    """
    if _es_client is None:
        return None
    try:
        response = _es_client.client.search(
            index="whatsapp_chats",
            body={"query": {"match": {"content": query}}},
        )
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception as exc:  # pragma: no cover - runtime boundary
        print(f"Error searching indexed documents: {exc}")
        return None

