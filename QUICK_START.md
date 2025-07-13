# Quick Start Guide

## 🚀 2-minutowy setup

### 1. Rozpakuj i uruchom
```bash
cd team-chat-libraxis/
chmod +x start.sh
./start.sh
```

### 2. Otwórz chat w przeglądarce
```
http://localhost:8000
```

### 3. Uruchom Claude Code
```bash
# Basic version
python3 claude_chat_client.py

# LUB Enhanced z LibraxisAI (RECOMMENDED)
python3 libraxis_integration.py
```

## ⚙️ Szybka konfiguracja

### Dla Enhanced version (z LibraxisAI):
Edytuj `config_libraxis.py`:
```python
LIBRAXIS_API_BASE_URL = "https://llm.libraxis.cloud/api/v1"
LIBRAXIS_DEFAULT_MODEL = "your-model-name"  # ZMIEŃ
```

### Dla zespołu:
- Server IP: znajdź w output `start.sh`
- Chat URL: `http://IP:8000` 
- Każdy wpisuje swoje imię i może pisać

## 💬 Test Claude

Napisz w chacie:
- `claude?` → Claude odpowie
- `code review` → automatyczna reakcja
- `status` → pokaże status

## 📋 Struktura plików

```
📁 team-chat-libraxis/
├── 🚀 start.sh                  # URUCHOM TO
├── 🌐 chat_server.py            # Chat server  
├── 🤖 claude_chat_client.py     # Basic Claude
├── ⭐ libraxis_integration.py   # Enhanced Claude (USE THIS)
├── ⚙️ config_libraxis.py       # Konfiguracja LibraxisAI
├── 📖 README.md                # Pełna dokumentacja
└── 🔧 SETUP.md                 # Szczegółowe instrukcje
```

## 🆘 Problemy?

1. **Port zajęty?** Zmień port w `config.py`
2. **Claude nie odpowiada?** Sprawdź URL w config
3. **LibraxisAI nie działa?** Claude użyje fallback responses

---
**That's it!** Macie Slack-like chat z AI Claude używającym waszych własnych modeli! 🎉
