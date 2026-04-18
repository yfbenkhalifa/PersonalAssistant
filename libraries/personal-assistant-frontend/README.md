# Personal Assistant Frontend

Standalone React project extracted from `PersonalAssistant`. It can run as:

- a demo app during development
- a reusable UI library for another React application

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
- a compatible backend exposing `POST /api/chat`, `DELETE /api/chat/:id`, and `GET /health`

## 🚀 Quick Start

### Demo app

1. **Navigate to the project:**
   ```bash
   cd /home/wiz/Dev/PersonalAssistant/libraries/personal-assistant-frontend
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

The demo app will be available at `http://localhost:3000`.

## 📦 Library build

Build the reusable package output:

```bash
npm run build:lib
```

Generated files are written to `dist/`.

## 🧩 Library usage

```jsx
import 'personal-assistant-frontend/styles.css'
import { ChatInterface, setApiBaseUrl } from 'personal-assistant-frontend'

setApiBaseUrl('http://localhost:8000')

export default function App() {
  return <ChatInterface />
}
```

You can also inject your own message transport:

```jsx
import { ChatInterface } from 'personal-assistant-frontend'

async function sendMessageHandler(message, conversationId) {
  const response = await fetch('/my-api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  })

  return response.json()
}

export default function App() {
  return <ChatInterface sendMessageHandler={sendMessageHandler} />
}
```

## 🏗️ Project Structure

```
personal-assistant-frontend/
├── src/
│   ├── components/
│   ├── services/
│   ├── App.jsx              # Demo app shell
│   ├── index.js             # Library entrypoint
│   └── main.jsx             # Demo app bootstrap
├── package.json
└── vite.config.js
```

## 🔌 Expected Backend Contract

- **POST /api/chat** - Send a message and get response
  ```json
  {
    "message": "Hello, assistant!",
    "conversation_id": "optional-id"
  }
  ```

- **DELETE /api/chat/{conversation_id}** - Clear conversation
- **GET /health** - Health check

## 🎨 Customization

### Styling

The app uses Tailwind CSS. Customize colors in `tailwind.config.js`:

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

Update environment variables in `.env`:

```env
VITE_API_URL=http://your-api-url:8000
VITE_WS_URL=ws://your-websocket-url:8000
```

## 📦 Building for Production

### Demo app

```bash
npm run build
```

Build output will be in `dist/`.

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

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check backend CORS settings
- Confirm `.env` file has correct URLs

### Messages not sending
- Check browser console for errors
- Verify API endpoint is accessible
- Test backend directly: `curl http://localhost:8000/health`

## 📝 Notes

This package was extracted from the original monorepo and is intended to be published independently if desired.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

Built with React, Vite, and Tailwind CSS
