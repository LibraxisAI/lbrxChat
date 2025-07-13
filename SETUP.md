# Team Chat Setup - Szczegółowe instrukcje

## 1. Instalacja dependencji

```bash
pip install fastapi uvicorn websockets requests sqlite3
```

Lub użyj `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 2. Uruchomienie chat servera

### Opcja A: Quick start
```bash
chmod +x start.sh
./start.sh
```

### Opcja B: Ręcznie
```bash
python3 chat_server.py
```

Server będzie dostępny na: `http://localhost:8000`

## 3. Dostęp dla zespołu

Każda osoba z zespołu otwiera w przeglądarce:
```
http://localhost:8000
```

Pojawi się chat interface - każdy wpisuje swoje imię i może pisać.

## 4. Integracja Claude Code - Basic Version

```bash
# Zapisz kod jako claude_chat_client.py
python3 claude_chat_client.py
```

Claude automatycznie:
- Połączy się z chatem
- Będzie monitorować nowe wiadomości co 5 sekund  
- Odpowie na określone keywords (code review, deploy, bug, itp.)

## 5. Integracja Claude Code - Enhanced z LibraxisAI ⭐

```bash
# Użyj enhanced version zamiast basic
python3 libraxis_integration.py
```

### Korzyści Enhanced version:
- 🧠 **Smart AI responses** używając waszych modeli LibraxisAI
- 💭 **Conversation context** - pamięta poprzednie wiadomości
- 🔄 **Automatic fallback** gdy LibraxisAI nie działa
- ⚙️ **Custom prompts** dla różnych scenariuszy
- 🏠 **Private infrastructure** - wszystko w waszej sieci

## 6. Konfiguracja

### W chat_server.py zmień:
```python
claude_url = "http://localhost:8001/receive-message"  # URL do Claude Code API
```

### W claude_chat_client.py (basic) zmień:
```python
chat_server_url = "http://TWÓJ_IP:8000"  # IP servera chatu
```

### W libraxis_integration.py (enhanced) zmień w config_libraxis.py:
```python
LIBRAXIS_API_BASE_URL = "https://llm.libraxis.cloud/api/v1"
LIBRAXIS_API_KEY = ""  # Jeśli używacie API keys
LIBRAXIS_DEFAULT_MODEL = "your-model-name"  # Nazwa waszego modelu
```

## 7. Customizacja dla Claude Code

### Basic version - edytuj `handle_team_message()`:
```python
def handle_team_message(message: dict) -> Optional[str]:
    content = message["content"]
    sender = message["sender"]
    
    if "analyze repo" in content:
        return f"Analizuję repo... znalazłem {count} issues"
    
    if "create PR" in content:
        return f"Tworzę PR dla {feature_name}"
    
    return None
```

### Enhanced version - edytuj prompts w `config_libraxis.py`:
```python
CUSTOM_PROMPTS = {
    "code_review": "Analizuję kod pod kątem jakości, bezpieczeństwa i best practices.",
    "deployment": "Sprawdzam status deployment, logi i potencjalne problemy.",
    "debugging": "Pomagam znaleźć i rozwiązać bugi. Podaj szczegóły problemu.",
    "general": "Jestem Claude Code, członek zespołu. Czym mogę pomóc?"
}
```

## 8. LibraxisAI Configuration Details

### API Format adaptacja
W `libraxis_integration.py` dostosuj format request do waszego API:

```python
async def generate_response(self, message: str, model: str = None, context: list = None) -> str:
    payload = {
        "model": model or "default",
        "messages": context or [{"role": "user", "content": message}],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    # Sprawdźcie właściwy endpoint - może być inny!
    response = requests.post(
        f"{self.base_url}/chat/completions",  # lub /generate, /complete itp.
        headers=self.headers,
        json=payload,
        timeout=30
    )
```

### Response format adaptacja
```python
if response.status_code == 200:
    result = response.json()
    # Adaptuj do formatu odpowiedzi z waszego API
    # Może być result["response"], result["text"], itp.
    return result.get("choices", [{}])[0].get("message", {}).get("content", "")
```

## 9. Production hints

### Dla stabilności:
- Użyj nginx jako reverse proxy
- Dodaj SSL certificates  
- Backup bazy SQLite co godzinę
- Logi do pliku

### Dla skalowania:
- Redis zamiast SQLite
- WebSocket clustering
- Rate limiting na API

### Dla security:
- Authentication tokens
- CORS configuration
- Input validation

## 10. Voice Integration (opcjonalne)

Jeśli macie STT/TTS endpointy:

### W config_libraxis.py:
```python
STT_ENDPOINT = "https://stt.libraxis.cloud/api/v1/transcribe"
TTS_ENDPOINT = "https://tts.libraxis.cloud/api/v1/synthesize"
ENABLE_VOICE_FEATURES = True
```

### Dodaj do chat_server.py:
```python
@app.post("/api/voice")
async def voice_message(audio_file):
    # Wyślij do waszego STT
    text = requests.post(STT_ENDPOINT, files={"audio": audio_file}).json()["text"]
    
    # Przetwórz jako normalną wiadomość
    message = {"sender": "Voice User", "content": text}
    timestamp = save_message(message["sender"], message["content"])
    await broadcast_message({**message, "timestamp": timestamp})
```

## 11. Troubleshooting

**Claude nie odpowiada:**
- Sprawdź czy `libraxis_integration.py` lub `claude_chat_client.py` działa
- Czy URL w `config.py`/`config_libraxis.py` jest poprawny
- Czy Claude Code ma dostęp do internetu

**Wiadomości się gubią:**
- Sprawdź logi serwera
- Czy WebSocket connection jest stabilny
- Restart `chat_server.py`

**LibraxisAI API errors:**
- Sprawdź `https://status.libraxis.cloud`
- Zweryfikuj API endpoint URL
- Sprawdź czy potrzebujecie API key
- Claude automatycznie użyje fallback responses

**Slow performance:**
- Zmniejsz polling interval (z 5s na 2s)
- Dodaj indexy do SQLite
- Cache recent messages

## 12. Testing LibraxisAI Integration

### Test połączenia:
```bash
curl -X GET https://llm.libraxis.cloud/api/v1/models
```

### Test chat endpoint:
```bash
curl -X POST https://llm.libraxis.cloud/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "default",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

## 13. Monitoring i Logs

### Chat server logs:
```bash
# Uruchom z logami
python3 chat_server.py > chat_server.log 2>&1
```

### Claude client logs:
```bash
# Enhanced version loguje do pliku
tail -f claude_libraxis.log
```

### LibraxisAI health monitoring:
```bash
# Sprawdź status
curl https://status.libraxis.cloud
```

---

**To wszystko!** Mając ten setup, Claude Code może normalnie gadać z zespołem jak na Slacku, używając waszych własnych modeli AI, bez męczenia z plikami przez Tailscale.

**Recommended flow:**
1. Start z basic version (`claude_chat_client.py`)
2. Jak działa - przełącz na enhanced (`libraxis_integration.py`)
3. Skonfiguruj LibraxisAI endpoints
4. Dostosuj prompts w `config_libraxis.py`
5. Ciesz się inteligentnym Claude Code! 🎉
