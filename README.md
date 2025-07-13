# Team Chat - Claude Code Integration

Prosty chat system dla zespołu 3 humans + 3 AI, żeby zastąpić komunikację przez pliki .md w Tailscale.

## 🚀 Quick Start (2 minuty)

```bash
# Rozpakuj pliki
cd team-chat-libraxis/

# Uruchom (automatycznie zainstaluje dependencje)
chmod +x start.sh
./start.sh
```

Chat będzie dostępny w przeglądarce na `http://localhost:8000`

## 📁 Struktura plików

```
team-chat-libraxis/
├── chat_server.py           # Główny server (WebSocket + REST API)
├── claude_chat_client.py    # Podstawowa integracja (single AI)  
├── libraxis_integration.py  # Enhanced version (single AI)
├── 🌟 multi_ai_integration.py # Multi-AI system (3 AI personalities)
├── config.py               # Podstawowa konfiguracja
├── config_libraxis.py      # Konfiguracja LibraxisAI (single)
├── 🌟 config_multi_ai.py   # Konfiguracja Multi-AI
├── requirements.txt        # Python dependencies
├── start.sh               # Chat server launcher
├── 🌟 start_ai.sh         # AI launcher (interactive)
├── README.md              # Podstawowa dokumentacja
├── 🌟 README_MULTI_AI.md  # Multi-AI dokumentacja
└── SETUP.md              # Szczegółowe instrukcje
```

## ⚡ Jak to działa

1. **Chat Server** - WebSocket server z prostym web interface
2. **Claude Code** - łączy się przez HTTP API, polling co 5s
3. **Zespół** - używa przeglądarki, real-time przez WebSocket

## 🔧 Podstawowa konfiguracja

### Zmień w `config.py`:
```python
CLAUDE_CODE_URL = "http://IP_CLAUDE:PORT/receive-message"
```

### Dla Claude Code:
```python
# W claude_chat_client.py
chat_server_url = "http://IP_SERVERA:8000"
```

## 🌟 Multi-AI System (RECOMMENDED)

Zamiast pojedynczego AI, użyjcie **Multi-AI system** z 3 personality:

```bash
# Interactive launcher
./start_ai.sh

# Lub bezpośrednio:
python3 multi_ai_integration.py all        # Wszystkie AI
python3 multi_ai_integration.py klaudiusz  # Tylko Klaudiusz (Maciej)
python3 multi_ai_integration.py claude     # Tylko Claude (Monika)  
python3 multi_ai_integration.py mikserka   # Tylko Mikserka (GPT)
```

### 🤖 AI Personalities:
- 🔍 **Klaudiusz** (Claude Macieja) - code review, VISTY monitoring
- 🤖 **Claude** (Moniki) - team coordination, general help  
- 🎨 **Mikserka** (GPT) - creative solutions, brainstorming

**Więcej info:** `README_MULTI_AI.md`

## 🌟 Single AI Integration (alternatywa)

Jeśli chcecie tylko 1 AI:

```bash
python3 libraxis_integration.py
```

### Konfiguracja LibraxisAI w `config_libraxis.py`:
```python
LIBRAXIS_API_BASE_URL = "https://llm.libraxis.cloud/api/v1"
LIBRAXIS_API_KEY = ""  # Jeśli używacie
LIBRAXIS_DEFAULT_MODEL = "your-model-name"
```

## 💬 Komendy dla Claude

Claude automatycznie reaguje na:
- `code review` → "Sprawdzam kod!"
- `deploy` → "Sprawdzam deployment..."  
- `bug` / `błąd` → "Analizuję raport błędu"
- `claude?` → "Jestem tu!"
- `status` → Pokazuje status Claude Code

## 🤖 LibraxisAI Features

- ✅ **Smart AI Responses** - używa waszych modeli LLM
- ✅ **Conversation Context** - pamięta poprzednie wiadomości
- ✅ **Fallback System** - działa nawet gdy LibraxisAI nie odpowiada
- ✅ **Custom Prompts** - dostosowane do teamowych potrzeb
- ✅ **Private Infrastructure** - wszystko zostaje w waszej sieci

## 🔍 Monitoring

Claude Code wyświetla w konsoli:
```
🤖 Claude Code + LibraxisAI - monitoring team chat...
📊 Dostępne modele LibraxisAI: 5
📨 Nowa wiadomość od Human1: sprawdź deployment
✅ Odpowiedziałem: @Human1 Monitoruję deployment... 🚀
```

## 🐛 Troubleshooting

**Chat nie działa:**
```bash
# Sprawdź czy port 8000 jest wolny
lsof -i :8000

# Uruchom ręcznie z logami
python3 chat_server.py
```

**Claude nie odpowiada:**
```bash
# Podstawowa wersja
python3 claude_chat_client.py

# Enhanced z LibraxisAI
python3 libraxis_integration.py

# Sprawdź URL w config files
```

**LibraxisAI nie działa:**
- Sprawdź `https://status.libraxis.cloud`
- Zweryfikuj URL w `config_libraxis.py`
- Claude automatycznie przełączy się na fallback responses

## 🚀 Rozszerzenia

### Dodaj nowe reakcje Claude:
```python
# W libraxis_integration.py, funkcja get_fallback_response()
if "git status" in content:
    return "📊 Checking git status..."
```

### Voice integration (z waszymi STT/TTS):
```python
# W config_libraxis.py
STT_ENDPOINT = "https://stt.libraxis.cloud/api/v1/transcribe"
TTS_ENDPOINT = "https://tts.libraxis.cloud/api/v1/synthesize"
ENABLE_VOICE_FEATURES = True
```

## 📊 Versions

### Basic Version:
- `claude_chat_client.py` - proste odpowiedzi, keyword matching
- `config.py` - podstawowe ustawienia

### Enhanced Version (Recommended):
- `libraxis_integration.py` - AI-powered responses z waszymi modelami
- `config_libraxis.py` - advanced configuration
- Smart context awareness
- Conversation memory
- Custom prompts

## 🔗 Przydatne linki

- WebSocket test: `ws://localhost:8000/ws`
- API docs: `http://localhost:8000/docs` (FastAPI auto-docs)
- Messages API: `http://localhost:8000/api/messages`
- LibraxisAI Status: `https://status.libraxis.cloud`

---

**Problemy?** Sprawdź SETUP.md dla szczegółowych instrukcji lub napisz na chacie! 😉

**Pro tip:** Użyjcie `libraxis_integration.py` zamiast podstawowego client'a - Claude będzie znacznie inteligentniejszy używając waszych własnych modeli LLM! 🧠✨
