# 🤖 Personal Assistant

An intelligent AI-powered personal assistant with a stunning visual interface, built with FastAPI, LangChain, and React.

![Personal Assistant](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed)

## ✨ Features

- 🎨 **Stunning UI** - Glassmorphism design with animated gradients and floating particles
- 🧠 **AI-Powered** - LangChain + LangGraph with Azure OpenAI integration
- ⚡ **Real-time Chat** - REST and WebSocket support
- 🔍 **Document Search** - Elasticsearch integration for indexed document queries
- 🐳 **Docker Ready** - Complete containerization with docker-compose
- 🔄 **Hot Reload** - Development mode with automatic reloading
- 📱 **Responsive** - Beautiful UI that works on all devices

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose V2 installed
- Azure OpenAI API credentials (or compatible OpenAI endpoint)

### Get Running in 30 Seconds

```bash
# Clone and navigate
cd PersonalAssistant

# Set up environment
cp .env.example .env
nano .env  # Add your Azure OpenAI credentials

# Start everything!
./start.sh --build
```

Access at:
- 🌐 Frontend: **http://localhost:8080**
- 🔧 Backend API: **http://localhost:8000**
- 📖 API Docs: **http://localhost:8000/docs**

## 📦 What's Included

### Backend (`/server`)
- FastAPI server with LangChain/LangGraph
- Agent-based conversational AI
- Elasticsearch integration
- REST + WebSocket endpoints
- Comprehensive API documentation

### Frontend (`/frontend`)
- React 18 + Vite
- Tailwind CSS with custom animations
- Glassmorphism UI design
- Real-time chat interface
- Beautiful loading states and micro-interactions

### Infrastructure
- Docker containerization
- Nginx reverse proxy
- Multi-service orchestration
- Development & production configurations

## 🛠️ Development

### Using Docker (Recommended)

```bash
# Start with hot reload
./start.sh

# Rebuild containers
./start.sh --build

# Run in background
./start.sh -b -d

# View logs
docker compose logs -f

# Stop services
./stop.sh
```

### Local Development

**Backend:**
```bash
pip install -r requirements
uvicorn server.chat_api:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started quickly
- [DOCKER.md](DOCKER.md) - Complete Docker guide
- [server/README.md](server/README.md) - Backend documentation
- [frontend/README.md](frontend/README.md) - Frontend documentation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│  Port 8080 | Glassmorphism UI | Real-time Chat      │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────┐
│              Backend (FastAPI)                       │
│  Port 8000 | LangChain | Agent System                │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼─────────┐
│  Azure OpenAI  │        │  Elasticsearch   │
│   LLM Models   │        │ Document Search  │
└────────────────┘        └──────────────────┘
```

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Model Configuration (`config.yaml`)

```yaml
model:
  model: "GPT_4O"
  temperature: 0.7
  provider: "AZURE_OPENAI"
  apiVersion: "2024-12-01-preview"
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "conversation_id": "test"}'
```

## 📊 Project Structure

```
PersonalAssistant/
├── server/              # FastAPI backend
│   ├── chat_api.py      # Main API endpoints
│   ├── Dockerfile       # Backend container
│   └── README.md        # Backend docs
├── frontend/            # React frontend
│   ├── src/             # Source code
│   ├── Dockerfile       # Frontend container
│   └── README.md        # Frontend docs
├── src/                 # Shared Python modules
│   └── agents/          # Agent implementations
├── chatbot/             # Chatbot logic
├── elasticsearch_client/# Search client
├── prompts/             # AI prompts
├── docker-compose.yml   # Multi-service orchestration
├── start.sh             # Quick start script
└── stop.sh              # Stop script
```

## 🎨 UI Highlights

- **Animated Gradients** - Dynamic, shifting background colors
- **Glassmorphism** - Frosted glass aesthetic with backdrop blur
- **Floating Particles** - Ambient animated orbs for depth
- **Smooth Animations** - Entrance effects and micro-interactions
- **Gradient Buttons** - Modern, vibrant interactive elements
- **Custom Shadows** - Multi-layered depth effects

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- AI powered by [LangChain](https://langchain.com/)
- UI with [React](https://react.dev/) + [Tailwind CSS](https://tailwindcss.com/)
- Icons by [Lucide](https://lucide.dev/)

---

Made with ❤️ and ☕ by the Personal Assistant Team
