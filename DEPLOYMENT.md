# lbrxChat Deployment Guide

## Team Central Server Setup

### Prerequisites
- Git installed
- UV package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Network access (port 9310)

### Central Server Deployment

```bash
# 1. Clone repository
git clone https://github.com/LibraxisAI/lbrxChat.git
cd lbrxChat

# 2. Install dependencies  
uv sync

# 3. Start central server
uv run python chat_server.py
```

### Server will start on:
- **Local access:** http://localhost:9310
- **Network access:** http://YOUR-IP:9310
- **Tailscale access:** http://YOUR-TAILSCALE-IP:9310

### Team Member Access

Team members just need to:
1. Open browser
2. Navigate to: `http://SERVER-IP:9310` 
3. Enter their name
4. Start chatting!

**No installation required for team members!**

### Adding AI Assistants

```bash
# In separate terminal on server machine:
uv run python multi_ai_integration.py

# AIs will join the chat automatically:
# - Klaudiusz 🔍 (Code review, technical analysis)
# - Claude 🤖 (Team coordination, general assistance)  
# - Mikserka 🎨 (Creative solutions, brainstorming)
```

### Configuration

Port and host can be configured via environment variables:

```bash
export LBRX_CHAT_PORT=9310      # Custom port
export LBRX_CHAT_HOST=0.0.0.0   # Bind to all interfaces
```

### Troubleshooting

**Port already in use:**
```bash
lsof -i :9310
kill -9 <PID>
```

**Network access issues:**
- Check firewall settings
- Verify port 9310 is open
- Confirm server binding to 0.0.0.0

**AI not responding:**
- Check LibraxisAI endpoint configuration in `config_multi_ai.py`
- Verify network connectivity
- Check console logs for errors