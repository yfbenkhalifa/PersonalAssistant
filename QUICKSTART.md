# Personal Assistant - Quick Start Guide

## 🚀 Getting Started (Docker - Recommended)

### The Fastest Way - Docker Compose

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your Azure OpenAI credentials

# 2. Start everything with one command
./start.sh --build
```

That's it! Access at:
- 🌐 **Frontend:** http://localhost:8080
- 🔧 **Backend API:** http://localhost:8000
- 📖 **API Docs:** http://localhost:8000/docs

To stop: `./stop.sh` or `docker compose down`

---

## 🐳 Docker Options

### Start services
```bash
./start.sh              # Start normally
./start.sh --build      # Rebuild and start
./start.sh -b -d        # Rebuild and run in background
```

### Manual Docker commands
```bash
# Build both images
docker compose build

# Start all services
docker compose up

# View logs
docker compose logs -f
```

See [DOCKER.md](DOCKER.md) for comprehensive Docker documentation.

---

## 💻 Local Development (Without Docker)

### 1. Start the Backend

```bash
# From project root
cd /home/wiz/Dev/PersonalAssistant

# Set up environment
cp .env.example .env
# Edit .env and add your API credentials

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn server.chat_api:app --reload --port 8000
```

Backend will run on: http://localhost:8000

### 2. Start the Frontend

```bash
# Open new terminal
cd /home/wiz/Dev/PersonalAssistant/frontend

# Install dependencies (first time only)
npm install

# Copy environment file
cp .env.example .env

# Start dev server
npm run dev
```

Frontend will run on: http://localhost:5173

### 3. Open Your Browser

Navigate to: http://localhost:5173

Start chatting with your Personal Assistant! 🎉

---

## 📚 Additional Documentation

- [DOCKER.md](DOCKER.md) - Complete Docker guide
- [frontend/README.md](frontend/README.md) - Frontend documentation
- [server/README.md](server/README.md) - Backend documentation

## 🔧 Configuration

### Backend (`.env` in project root)
```env
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-key
```

### Frontend (`.env` in frontend/)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🐛 Issues?

- **Backend not starting?** Check Python dependencies and .env file
- **Frontend can't connect?** Ensure backend is running on port 8000
- **Other issues?** Check the browser console for errors

---

Need help? Check the full README in the frontend folder!
