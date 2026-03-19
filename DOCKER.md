# Personal Assistant - Docker Compose Guide

This guide helps you run the entire Personal Assistant stack using Docker Compose.

## 🚀 Quick Start

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your credentials:**
   ```bash
   nano .env  # or use your favorite editor
   ```
   Add your Azure OpenAI endpoint and API key.

3. **Start all services:**
   ```bash
   docker compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📦 Services

### Backend (Port 8000)
- FastAPI server with LangChain/LangGraph
- REST and WebSocket endpoints
- Agent-based chat system

### Frontend (Port 8080)
- React + Vite application
- Stunning glassmorphism UI
- Real-time chat interface

## 🛠️ Development Commands

```bash
# Start services
docker compose up

# Start in detached mode
docker compose up -d

# Rebuild containers
docker compose up --build

# Stop services
docker compose down

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart a service
docker compose restart backend
```

## 🧹 Cleanup

```bash
# Stop and remove containers
docker compose down

# Remove containers and volumes
docker compose down -v

# Remove containers, volumes, and images
docker compose down -v --rmi all
```

## 🔧 Configuration

The stack uses:
- `.env` - Environment variables (API keys)
- `config.yaml` - LLM model configuration
- `appsettings.json` - Service settings

## 📝 Notes

- Hot reload is enabled for both frontend and backend in development
- Backend code changes will auto-reload
- Frontend requires rebuild for changes (or run `npm run dev` locally)
- Network: Services communicate via `personal-assistant-network`

## 🐛 Troubleshooting

**Backend won't start:**
- Verify `.env` file exists and has correct API keys
- Check `docker compose logs backend`

**Frontend can't connect to backend:**
- Ensure backend is healthy: `docker compose ps`
- Check nginx proxy configuration

**Port conflicts:**
- Change ports in `docker-compose.yml` if 8000 or 8080 are in use
