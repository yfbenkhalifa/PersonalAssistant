# Personal Assistant Server

FastAPI-based backend server for the Personal Assistant application.

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

2. **Build and run with Docker:**
   ```bash
   # From the server directory
   docker build -t personal-assistant-server:dev .
   docker run -p 8000:8000 --env-file .env personal-assistant-server:dev
   ```

3. **Or use docker-compose from project root:**
   ```bash
   # Run both frontend and backend
   cd ..
   docker-compose up
   ```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export AZURE_OPENAI_ENDPOINT="your-endpoint"
   export AZURE_OPENAI_API_KEY="your-api-key"
   ```

3. **Run the server:**
   ```bash
   uvicorn chat_api:app --reload --port 8000
   ```

## 📡 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/chat` - Send chat message (REST)
- `WebSocket /ws/{conversation_id}` - Real-time chat (WebSocket)

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "conversation_id": "test"}'
```

## 📋 Configuration

The server uses:
- `config.yaml` - LLM model configuration
- `appsettings.json` - Elasticsearch and service settings
- `.env` - Environment variables (API keys, endpoints)

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes (for Azure) |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes (for Azure) |
| `ENVIRONMENT` | Environment (development/production) | No |
| `LOG_LEVEL` | Logging level | No |
