# Personal Assistant

A monorepo for an AI-powered personal assistant with document search, chat,
and a React web UI.

## Repository layout

```
PersonalAssistant/
├── docker-compose.yml          # Orchestrates backend + frontend
├── start.sh / stop.sh          # Convenience wrappers around docker compose
├── .env.example                # Shared runtime environment variables
├── infra/
│   └── elasticsearch/          # 3-node Elasticsearch + Kibana dev stack
├── notebooks/                  # Research / experimentation
└── projects/
    ├── personal-assistant-agent/         # LangChain/LangGraph agent + FastAPI
    ├── personal-assistant-elasticsearch/ # Elasticsearch client + FastAPI
    └── personal-assistant-frontend/      # React + Vite + Tailwind UI
```

Each project under `projects/` is self-contained with its own `pyproject.toml`
or `package.json`, tests, and Dockerfile.

## Quick start

See [`QUICKSTART.md`](./QUICKSTART.md).

## Projects

| Project | Purpose | Docs |
|---|---|---|
| `personal-assistant-agent` | LangChain-based chat agent exposed over REST + WebSocket. | [README](libraries/personal-assistant-agent/README.md) |
| `personal-assistant-elasticsearch` | Elasticsearch-backed document indexing and semantic search API. | [README](libraries/personal-assistant-elasticsearch/README.md) |
| `personal-assistant-frontend` | React web client and reusable component library. | [README](libraries/personal-assistant-frontend/README.md) |
| `infra/elasticsearch` | Local Elasticsearch + Kibana dev cluster. | [README](./infra/elasticsearch/README.md) |

## Development

Install the Python projects in editable mode (order matters because the agent
has an optional dependency on the elasticsearch package):

```bash
pip install -e libraries/personal-assistant-elasticsearch
pip install -e "projects/personal-assistant-agent[elasticsearch,dev]"
```

Run the test suites per-project:

```bash
(cd libraries/personal-assistant-agent && pytest)
(cd libraries/personal-assistant-elasticsearch && pytest)
(cd libraries/personal-assistant-frontend && npm install && npm run build)
```

## Running with Docker

```bash
cp .env.example .env            # fill in credentials
./start.sh --build --detached   # build images and run in background
```

Once running:

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

Stop with `./stop.sh` or `docker compose down`.

