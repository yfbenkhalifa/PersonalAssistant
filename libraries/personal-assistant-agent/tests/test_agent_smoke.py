"""Smoke test for the Agent class against Azure OpenAI.

Skipped automatically when ``AZURE_OPENAI_API_KEY`` is not set so the suite
stays green in CI without credentials.
"""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

from personal_assistant_agent import Agent, AzureOpenAIModelConfig

load_dotenv()

pytestmark = pytest.mark.skipif(
    not os.getenv("AZURE_OPENAI_API_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"),
    reason="AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT not set",
)


@pytest.fixture
def agent() -> Agent:
    config = AzureOpenAIModelConfig(
        nickname="test",
        host=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="gpt-4o",
        temperature=0.1,
        api_version="2024-12-01-preview",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )
    return Agent(config)


def test_agent_initialization(agent: Agent) -> None:
    assert agent is not None
    assert agent.nickname == "test"
