"""State definitions for the LangGraph chatbot pipeline."""

from __future__ import annotations

from typing import Annotated

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    """Conversation state. ``messages`` is append-only via ``add_messages``."""

    messages: Annotated[list, add_messages]


def build_graph_builder() -> StateGraph:
    """Return a fresh ``StateGraph`` configured with the chatbot ``State``."""
    return StateGraph(State)

