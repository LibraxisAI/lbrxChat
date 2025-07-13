# Multi-AI Team Chat - 3 AI Personalities

System chatu dla zespołu z **3 odrębnymi AI**:
- 🔍 **Klaudiusz** (Claude Macieja) - code review, VISTY monitoring  
- 🤖 **Claude** (Moniki) - team coordination, general help
- 🎨 **Mikserka** (GPT) - creative solutions, brainstorming

## 🚀 Quick Start

### 1. Uruchom chat server
```bash
./start.sh
```
Chat dostępny: `http://localhost:8000`

### 2. Uruchom AI (wybierz opcję)
```bash
# Interactive launcher
./start_ai.sh

# Lub bezpośrednio:
python3 multi_ai_integration.py klaudiusz  # Tylko Klaudiusz
python3 multi_ai_integration.py claude     # Tylko Claude  
python3 multi_ai_integration.py mikserka   # Tylko Mikserka
python3 multi_ai_integration.py all        # Wszystkie AI
```

## 🤖 AI Personalities

### 🔍 Klaudiusz (Claude Macieja)
- **Role:** Code review, deployment, VISTY repo monitoring
- **Style:** Techniczny ekspert, konkretny, merytoryczny
- **Triggers:** `code review`, `klaudiusz`, `maciej`, `visty`, `deploy`, `repo`
- **LibraxisAI Model:** `claude-model` (konfigurowalny)

### 🤖 Claude (Moniki)  
- **Role:** Team coordination, general assistance, organization
- **Style:** Pomocny, przyjazny, organizujący zespół
- **Triggers:** `claude`, `monika`, `koordynacja`, `help`, `organize`
- **LibraxisAI Model:** `claude-model` (konfigurowalny)

### 🎨 Mikserka (GPT)
- **Role:** Creative solutions, brainstorming, innovation
- **Style:** Kreatywny, energiczny, inspirujący
- **Triggers:** `mikserka`, `gpt`, `creative`, `brainstorm`, `pomysł`, `idea`
- **LibraxisAI Model:** `gpt-model` (konfigurowalny)

## 📋 Pliki

```
📁 team-chat-libraxis/
├── 🚀 start.sh                    # Chat server launcher
├── 🤖 start_ai.sh                 # AI launcher (interactive)
├── 🌐 chat_server.py              # Main chat server
├── ⭐ multi_ai_integration.py     # Multi-AI system (MAIN)
├── ⚙️ config_multi_ai.py         # AI configuration
├── 📖 README_MULTI_AI.md          # Ta dokumentacja
└── ... (other files)
```

## ⚙️ Konfiguracja

### W `config_multi_ai.py` można dostosować:

```python
# Modele LibraxisAI dla każdego AI
AI_MODEL_MAPPING = {
    "klaudiusz": "claude-model",
    "claude": "claude-model", 
    "mikserka": "gpt-model"
}

# Priorytety odpowiedzi
AI_PRIORITY = {
    "klaudiusz": 1,  # Pierwszy dla code
    "claude": 2,     # Drugi dla general
    "mikserka": 3    # Trzeci dla creative
}

# Czy AI mogą rozmawiać między sobą
ENABLE_AI_TO_AI_CHAT = False  # True = może być zabawne ale chaotyczne :)
```

## 💬 Przykłady użycia

### Testowanie AI w chacie:

**Code review:**
```
User: "klaudiusz sprawdź kod w main.py"
Klaudiusz 🔍: "@User Sprawdzam kod! Analizuję main.py pod kątem jakości i bezpieczeństwa..."
```

**Team coordination:**
```
User: "claude pomóż zorganizować zadania na dziś"
Claude 🤖: "@User Organizuję zadania zespołu! Sprawdzam co mamy do zrobienia..."
```

**Brainstorming:**
```
User: "mikserka jakieś pomysły na nową funkcję?"
Mikserka 🎨: "@User Czas na kreatywne myślenie! Może spróbujemy podejścia z AI automation..."
```

**Status check:**
```
User: "status"
Klaudiusz 🔍: "Klaudiusz aktywny | Role: code_review | Owner: Maciej"
Claude 🤖: "Claude aktywny | Role: coordination | Owner: Monika" 
Mikserka 🎨: "Mikserka aktywna | Role: creative | Owner: Team"
```

## 🔧 Advanced Features

### Multi-AI Response Strategy
- **round_robin:** AI odpowiadają na zmianę
- **priority:** Według ustawionego priorytetu  
- **all_respond:** Wszystkie AI mogą odpowiedzieć

### LibraxisAI Integration
- Każde AI może używać różnych modeli
- Automatic fallback gdy LibraxisAI niedostępny
- Conversation context dla każdego AI osobno

### Conflict Resolution
- Anti-spam: delay między odpowiedziami AI
- Smart triggering: AI odpowiadają tylko na właściwe wiadomości
- Owner context: AI wiedzą do kogo należą

## 🐛 Troubleshooting

**AI nie odpowiadają:**
```bash
# Sprawdź czy właściwy AI jest uruchomiony
ps aux | grep multi_ai_integration

# Sprawdź logi
tail -f multi_ai_chat.log
```

**Konflikt AI (wszystkie odpowiadają):**
```python
# W config_multi_ai.py
MULTI_AI_RESPONSE_STRATEGY = "priority"  # Tylko najwyższy priorytet
```

**LibraxisAI connection issues:**
```python
# Sprawdź modele
AI_MODEL_MAPPING = {
    "klaudiusz": "default",  # Użyj domyślnego modelu
    "claude": "default", 
    "mikserka": "default"
}
```

## 🎯 Best Practices

1. **Uruchamiaj selektywnie:** Nie zawsze wszystkie AI na raz
2. **Testuj triggers:** Każde AI ma swoje słowa kluczowe
3. **Monitoruj response rate:** Może być potrzeba dostrojenia
4. **Customizuj personalities:** Edytuj prompts w config
5. **Używaj właściwych modeli:** Przypisz odpowiednie modele LibraxisAI

---

**🎉 Teraz macie 3 oddzielne AI personalities w teamie!**

- **Klaudiusz** dba o kod i deployment
- **Claude** koordynuje zespół  
- **Mikserka** inspiruje kreatywnością

Każde z unikalną osobowością, rolą i proprietaire! 🚀
