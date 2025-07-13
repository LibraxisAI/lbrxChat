# config_libraxis.py - Enhanced config z integracją LibraxisAI

# === LIBRAXIS AI SETTINGS ===
LIBRAXIS_API_BASE_URL = "https://llm.libraxis.cloud/api/v1"
LIBRAXIS_API_KEY = ""  # Jeśli używacie API keys
LIBRAXIS_DEFAULT_MODEL = "default"  # Zmieńcie na właściwy model
LIBRAXIS_MAX_TOKENS = 150
LIBRAXIS_TEMPERATURE = 0.7

# Backup gdy LibraxisAI nie działa
ENABLE_FALLBACK_RESPONSES = True

# === PODSTAWOWE USTAWIENIA CHATU ===
CHAT_SERVER_HOST = "0.0.0.0"
CHAT_SERVER_PORT = 8000

# === INTELIGENTNE ODPOWIEDZI ===
# Czy Claude ma odpowiadać automatycznie
ENABLE_AI_RESPONSES = True

# Słowa kluczowe które uruchamiają AI response
AI_TRIGGER_KEYWORDS = [
    "claude", "?", "help", "pomoc", 
    "code review", "sprawdź kod",
    "bug", "błąd", "error", "problem",
    "deploy", "deployment", "wdrażanie",
    "status", "stan", "jak tam"
]

# Maksymalny kontekst konwersacji dla AI (liczba wiadomości)
MAX_CONVERSATION_CONTEXT = 10

# === USTAWIENIA CHATU ===
MAX_RECENT_MESSAGES = 50
CLAUDE_POLLING_INTERVAL = 5
DATABASE_FILE = "chat.db"

# === TEAM MEMBERS ===
TEAM_MEMBERS = [
    "Human1", "Human2", "Human3",
    "Claude-LibraxisAI", "AI_Assistant_2", "AI_Assistant_3"
]

# === ADVANCED AI FEATURES ===
# Czy używać kontekstu konwersacji w AI responses
USE_CONVERSATION_CONTEXT = True

# Czy logować AI interactions
LOG_AI_INTERACTIONS = True

# Timeout dla AI API calls (sekundy)
AI_API_TIMEOUT = 30

# === STT/TTS INTEGRATION (opcjonalne) ===
# Jeśli macie własne STT/TTS endpoints
STT_ENDPOINT = "https://stt.libraxis.cloud/api/v1/transcribe"  # Przykład
TTS_ENDPOINT = "https://tts.libraxis.cloud/api/v1/synthesize"  # Przykład

# Czy włączyć voice features
ENABLE_VOICE_FEATURES = False

# === NOTYFIKACJE I LOGOWANIE ===
ENABLE_NOTIFICATIONS = True
LOG_LEVEL = "INFO"
LOG_FILE = "claude_libraxis.log"

# === SECURITY ===
REQUIRE_AUTH = False
LOG_ALL_MESSAGES = True

# === MONITORING ===
# Health check URL dla LibraxisAI
LIBRAXIS_HEALTH_CHECK = "https://status.libraxis.cloud"

# Sprawdzaj health co X sekund
HEALTH_CHECK_INTERVAL = 60

# === PRZYKŁADY CUSTOMIZACJI ===
# Custom prompts dla różnych scenariuszy
CUSTOM_PROMPTS = {
    "code_review": "Analizuję kod pod kątem jakości, bezpieczeństwa i best practices.",
    "deployment": "Sprawdzam status deployment, logi i potencjalne problemy.",
    "debugging": "Pomagam znaleźć i rozwiązać bugi. Podaj szczegóły problemu.",
    "general": "Jestem Claude Code, członek zespołu. Czym mogę pomóc?"
}

# AI Personality settings
AI_PERSONALITY = {
    "style": "helpful_technical",  # helpful_technical, casual, formal
    "use_emojis": True,
    "mention_users": True,  # @username w odpowiedziach
    "max_response_length": 200
}
