# Personal Assistant - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Start the Backend

```bash
# From project root
cd /home/wiz/Dev/PersonalAssistant

# Set up environment
cp .env.example .env
# Edit .env and add your API credentials

# Start the API server
python server/chat_api.py
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

Frontend will run on: http://localhost:3000

### 3. Open Your Browser

Navigate to: http://localhost:3000

Start chatting with your Personal Assistant! 🎉

## 📚 Full Documentation

See [frontend/README.md](frontend/README.md) for complete documentation.

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
