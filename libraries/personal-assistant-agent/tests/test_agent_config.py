import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from personal_assistant_agent.agent import AgentConfig, AzureOpenAIModelConfig, create_llm_config_from_yaml
from personal_assistant_agent.enums import LLM_PROVIDER


def test_temperature_validation():
    try:
        AgentConfig(
            nickname="test",
            host="http://localhost",
            model="demo-model",
            temperature=1.5,
            provider=LLM_PROVIDER.OPENAI,
        )
    except ValueError:
        assert True
    else:  # pragma: no cover
        assert False, "Expected ValueError for invalid temperature"


def test_create_llm_config_for_lmstudio():
    config = {
        "model": {
            "model": "google/gemma-3-4b",
            "host": "http://127.0.0.1:1234",
            "temperature": 0.2,
            "provider": "LMSTUDIO",
            "apiVersion": "",
            "nickname": "demo",
        }
    }

    llm_config = create_llm_config_from_yaml(config)

    assert llm_config.nickname == "demo"
    assert llm_config.host == "http://127.0.0.1:1234"
    assert llm_config.provider == LLM_PROVIDER.LMSTUDIO


def test_create_llm_config_for_azure(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "secret")

    config = {
        "model": {
            "model": "GPT_4O",
            "temperature": 0.2,
            "provider": "AZURE_OPENAI",
            "apiVersion": "2024-12-01-preview",
        }
    }

    llm_config = create_llm_config_from_yaml(config)

    assert isinstance(llm_config, AzureOpenAIModelConfig)
    assert llm_config.host == "https://example.openai.azure.com"
    assert llm_config.api_key == "secret"


