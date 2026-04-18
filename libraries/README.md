# Extracted Projects

This folder contains the three standalone projects split out of the original `PersonalAssistant` workspace.

## Projects

### 1. `personal-assistant-agent`
Reusable Python package for the conversational agent and its FastAPI wrapper.

**Derived from:**
- `src/agents/`
- `server/chat_api.py`
- `config.yaml`

**Key outputs:**
- `personal_assistant_agent.agent.Agent`
- `personal_assistant_agent.api:create_app`
- installable Python package via `pyproject.toml`

### 2. `personal-assistant-elasticsearch`
Reusable Python package for document indexing/search and its FastAPI wrapper.

**Derived from:**
- `elasticsearch_client/`
- selected document chunking logic
- Elasticsearch settings concepts from `elasticsearch_client/settings.yaml`

**Key outputs:**
- `personal_assistant_elasticsearch.clients.ElasticSearchClient`
- `personal_assistant_elasticsearch.api:create_app`
- installable Python package via `pyproject.toml`

### 3. `personal-assistant-frontend`
Standalone React/Vite frontend that can run as a demo app or be built as a reusable UI library.

**Derived from:**
- `frontend/`

**Key outputs:**
- reusable `ChatInterface` component
- configurable REST/WebSocket services
- library build via `npm run build:lib`

## Suggested next step for publishing

If you want these as fully independent repositories/libraries, move each folder below into its own repository:

- `projects/personal-assistant-agent`
- `projects/personal-assistant-elasticsearch`
- `projects/personal-assistant-frontend`

## Validation commands

### Agent
```bash
cd /home/wiz/Dev/PersonalAssistant/libraries/personal-assistant-agent
pytest
```

### Elasticsearch
```bash
cd /home/wiz/Dev/PersonalAssistant/libraries/personal-assistant-elasticsearch
pytest
```

### Frontend demo build
```bash
cd /home/wiz/Dev/PersonalAssistant/libraries/personal-assistant-frontend
npm install
npm run build
```

### Frontend library build
```bash
cd /home/wiz/Dev/PersonalAssistant/libraries/personal-assistant-frontend
npm run build:lib
```

