# Quickstart

## 1. Prerequisites

- Docker + Docker Compose v2
- (For local dev) Python 3.11+, Node.js 18+

## 2. Configure secrets

```bash
cp .env.example .env
# Edit .env and set AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY
# (or point the agent at LM Studio via libraries/personal-assistant-agent/config.yaml)
```

## 3. Start everything in Docker

```bash
./start.sh --build --detached
```

| Service  | URL                           |
|----------|-------------------------------|
| Frontend | http://localhost:8080         |
| Backend  | http://localhost:8000         |
| API docs | http://localhost:8000/docs    |

Stop: `./stop.sh`

## 4. Run pieces locally (without Docker)

### Agent backend (FastAPI)

```bash
pip install -e "projects/personal-assistant-agent[dev]"
uvicorn personal_assistant_agent.api:app --reload --port 8000
```

Or use the interactive CLI:

```bash
personal-assistant-agent --config libraries/personal-assistant-agent/config.yaml
```

### Elasticsearch API

```bash
pip install -e "projects/personal-assistant-elasticsearch[dev]"
uvicorn personal_assistant_elasticsearch.api:app --reload --port 8100
```

### Frontend (Vite dev server)

```bash
cd libraries/personal-assistant-frontend
npm install
npm run dev
```

### Local Elasticsearch cluster

```bash
cd infra/elasticsearch
cp .env.example .env
docker compose up -d
```

## 5. Run tests

```bash
(cd libraries/personal-assistant-agent && pytest)
(cd libraries/personal-assistant-elasticsearch && pytest)
```

