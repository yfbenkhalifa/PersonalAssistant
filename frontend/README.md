# Personal Assistant - React + FastAPI Chat UI

A modern, responsive chat interface for the Personal Assistant application, built with React and FastAPI.

## 🌟 Features

- **Modern Chat Interface**: Clean, responsive design with message bubbles
- **Real-time Communication**: Support for both REST API and WebSocket
- **Auto-scrolling**: Automatic scroll to latest messages
- **Loading States**: Visual feedback during message processing
- **Error Handling**: Graceful error messages and recovery
- **Conversation Management**: Maintain conversation context
- **Tailwind CSS**: Beautiful, customizable styling

## 📋 Prerequisites

- Node.js 18+ and npm (for frontend)
- Python 3.12+ (for backend)
- Personal Assistant backend configured

## 🚀 Quick Start

### Backend Setup

1. **Navigate to project root:**
   ```bash
   cd /home/wiz/Dev/PersonalAssistant
   ```

2. **Install Python dependencies:**
   ```bash
   pip install fastapi uvicorn websockets python-dotenv
   ```

3. **Create `.env` file in project root:**
   ```bash
   AZURE_OPENAI_ENDPOINT=your-endpoint-here
   AZURE_OPENAI_API_KEY=your-api-key-here
   ```

4. **Start the FastAPI server:**
   ```bash
   python server/chat_api.py
   ```
   
   Or use uvicorn directly:
   ```bash
   uvicorn server.chat_api:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at: `http://localhost:3000`

## 🏗️ Project Structure

```
PersonalAssistant/
├── server/
│   └── chat_api.py          # FastAPI backend with REST & WebSocket
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── MessageInput.jsx
│   │   │   └── LoadingIndicator.jsx
│   │   ├── services/        # API services
│   │   │   ├── api.js       # REST API client
│   │   │   └── websocket.js # WebSocket client
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
└── config.yaml              # Agent configuration
```

## 🔌 API Endpoints

### REST API

- **POST /api/chat** - Send a message and get response
  ```json
  {
    "message": "Hello, assistant!",
    "conversation_id": "optional-id"
  }
  ```

- **DELETE /api/chat/{conversation_id}** - Clear conversation
- **GET /health** - Health check

### WebSocket

- **WS /ws/{conversation_id}** - Real-time chat connection
  ```json
  {
    "message": "Your message here"
  }
  ```

## 🎨 Customization

### Styling

The app uses Tailwind CSS. Customize colors in `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3b82f6',  // Change primary color
      secondary: '#64748b'
    }
  }
}
```

### API Configuration

Update environment variables in `frontend/.env`:

```env
VITE_API_URL=http://your-api-url:8000
VITE_WS_URL=ws://your-websocket-url:8000
```

## 📦 Building for Production

### Frontend

```bash
cd frontend
npm run build
```

Build output will be in `frontend/dist/`

### Backend

For production deployment:

```bash
uvicorn server.chat_api:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use Docker, Gunicorn, or your preferred deployment method.

## 🧪 Features to Add (Optional)

- [ ] Markdown rendering for assistant responses
- [ ] File upload support
- [ ] Voice input/output
- [ ] Multiple conversation tabs
- [ ] Message editing and regeneration
- [ ] Export conversation history
- [ ] Dark mode toggle
- [ ] User authentication

## 🐛 Troubleshooting

### Backend won't start
- Check that all Python dependencies are installed
- Verify `.env` file has correct API credentials
- Ensure config.yaml exists in project root

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check CORS settings in `server/chat_api.py`
- Confirm `.env` file has correct URLs

### Messages not sending
- Check browser console for errors
- Verify API endpoint is accessible
- Test backend directly: `curl http://localhost:8000/health`

## 📝 License

This project is part of the Personal Assistant application.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

Built with ❤️ using React, FastAPI, and Tailwind CSS
