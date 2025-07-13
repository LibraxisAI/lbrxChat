# lbrxChat - Multi-AI Team Communication System

First component of the LBRX SDK ecosystem. Replace MD file sharing via Tailscale with real-time multi-AI team chat.

## 🚀 Installation

```bash
curl -LsSf https://raw.githubusercontent.com/LibraxisAI/lbrxChat/main/install.sh | sh
```

This installer will:
- Check system requirements (Python 3, macOS/Linux)
- Install UV package manager if needed (recommended)
- Set up lbrxChat in `~/.lbrxchat`
- Add commands to your PATH

## 🏃 Quick Start

After installation, restart your terminal or run:
```bash
source ~/.zshrc  # or ~/.bashrc
```

Then:
```bash
# Start chat server
lbrx-chat

# In another terminal, start AI instances
lbrx-chat-ai
```

Chat interface available at: `http://localhost:1019`

## 🤖 Multi-AI System

Three AI personalities working together:

- 🔍 **Klaudiusz** - Code review, technical analysis, VISTY monitoring
- 🤖 **Claude** - Team coordination, general assistance  
- 🎨 **Mikserka** - Creative solutions, brainstorming

### Starting specific AI:
```bash
lbrx-chat-ai klaudiusz  # Just Klaudiusz
lbrx-chat-ai claude     # Just Claude
lbrx-chat-ai mikserka   # Just Mikserka
lbrx-chat-ai all        # All AI instances
```

## 🛠️ Manual Installation (for development)

If you prefer manual setup:

```bash
# Clone repository
git clone https://github.com/LibraxisAI/lbrxChat.git
cd lbrxChat

# Install with UV
uv sync

# Run directly
uv run python chat_server.py
uv run python multi_ai_integration.py
```

## 📁 Project Structure

```
lbrxChat/
├── chat_server.py           # Main WebSocket + REST server
├── multi_ai_integration.py  # Multi-AI system 
├── config_multi_ai.py       # AI personalities config
├── pyproject.toml          # UV project definition
├── install.sh              # One-line installer
└── start-uv.sh             # UV launcher scripts
```

## ⚡ How It Works

1. **Chat Server** - FastAPI WebSocket server with web interface
2. **AI Integration** - Each AI polls for messages via HTTP
3. **Team Access** - Real-time chat through browser WebSocket

## 🔧 Configuration

### AI Endpoints
Edit `config_multi_ai.py`:
```python
LIBRAXIS_API_BASE_URL = "https://llm.libraxis.cloud/api/v1"
LIBRAXIS_API_KEY = "your-key-if-needed"
```

### AI Personalities
Each AI has triggers and custom behavior:
```python
AI_PERSONALITIES = {
    "klaudiusz": {
        "triggers": ["code", "review", "klaudiusz", "deploy"],
        "style": "Technical expert, direct and thorough"
    }
}
```

## 💬 AI Commands

AIs respond to specific triggers:
- `@klaudiusz review this` → Code review mode
- `@claude help coordinate` → Team coordination  
- `@mikserka brainstorm ideas` → Creative mode
- `status` → Show all AI status

## 🌟 Features

- ✅ **Multi-AI Support** - 3 distinct AI personalities
- ✅ **Real-time Chat** - WebSocket for instant messaging
- ✅ **Context Awareness** - AIs remember conversation history
- ✅ **Trigger System** - Smart keyword activation
- ✅ **LibraxisAI Integration** - Use your own LLM models
- ✅ **UV Powered** - Modern Python package management

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**AI not responding:**
- Check console output for errors
- Verify LibraxisAI endpoints in config
- Ensure API keys are set if required

**UV not found:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🚀 Future LBRX Components

This is just the beginning:
- `lbrx generate` - AI code generation
- `lbrx sync` - API synchronization
- `lbrx deploy` - Deployment automation

## 🤝 Contributing

This is a Gang of Bastards internal tool. Contributions welcome from team members.

## 📝 License

Private repository - Gang of Bastards exclusive.

---

**Issues?** Check the console output or reach out on the team chat itself! 🔄