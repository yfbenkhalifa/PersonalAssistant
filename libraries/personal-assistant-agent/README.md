# Personal Assistant Agent

Standalone Python project for the reusable agent layer extracted from `PersonalAssistant`.

## Included

- `personal_assistant_agent.agent.Agent`
- `personal_assistant_agent.agent.AgentConfig`
- `personal_assistant_agent.agent.AzureOpenAIModelConfig`
- `personal_assistant_agent.api.create_app()` for the FastAPI chat API wrapper

## Install

```bash
pip install -e .
```

## Run the API locally

```bash
uvicorn personal_assistant_agent.api:app --reload --port 8000
```

## Minimal usage

```python
from langchain_core.messages import HumanMessage
from personal_assistant_agent.agent import Agent, AgentConfig
from personal_assistant_agent.enums import LLM_PROVIDER

config = AgentConfig(
    nickname="assistant",
    host="http://127.0.0.1:1234",
    model="google/gemma-3-4b",
    temperature=0.2,
    provider=LLM_PROVIDER.LMSTUDIO,
)

agent = Agent(config)
response = agent.invoke(HumanMessage(content="Hello"))
print(response.content)
```

## Test

```bash
pytest
```

