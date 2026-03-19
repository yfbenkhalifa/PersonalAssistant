from sys import api_version
from dotenv import load_dotenv
import pytest
from agents.agent import Agent, AgentConfig, AzureOpenAiModelConfig
from agents.enums import LLM_MODEL, LLM_PROVIDER
import os
load_dotenv()

@pytest.fixture
def agent():
    """Fixture to create an Agent instance for testing."""
    agent_config = AzureOpenAiModelConfig(
        host="https://yf-personal-swedencentral.services.ai.azure.com/api/projects/Personal",
        model="gpt-4o",
        provider=LLM_PROVIDER.AZURE_OPENAI,
        temperature=0.1,
        api_version="2024-12-01-preview",
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
    return Agent(agent_config)


def test_agent_initialization(agent):
    assert agent is not None
