# config.py - Centralna konfiguracja dla team chat

# === PODSTAWOWE USTAWIENIA ===
CHAT_SERVER_HOST = "0.0.0.0"  # Dostępny dla wszystkich w sieci
CHAT_SERVER_PORT = 8000

# Claude Code endpoint (ZMIEŃ NA WŁAŚCIWY!)
CLAUDE_CODE_URL = "http://localhost:8001/receive-message"

# === USTAWIENIA CHATU ===
# Ile ostatnich wiadomości pokazać przy ładowaniu
MAX_RECENT_MESSAGES = 50

# Jak często Claude sprawdza nowe wiadomości (sekundy)
CLAUDE_POLLING_INTERVAL = 5

# === USTAWIENIA BAZY DANYCH ===
DATABASE_FILE = "chat.db"

# === TEAM MEMBERS ===
# Lista członków zespołu (opcjonalne, do przyszłych funkcji)
TEAM_MEMBERS = [
    "Human1", "Human2", "Human3",
    "Claude", "AI_Assistant_2", "AI_Assistant_3"
]

# === KEYWORDS DLA CLAUDE ===
# Keywords które wywołują automatyczne odpowiedzi Claude
CLAUDE_TRIGGERS = {
    "code_review": ["code review", "review kod", "sprawdź kod"],
    "deployment": ["deploy", "deployment", "wdrażanie"],
    "bug_report": ["bug", "błąd", "error", "problem"],
    "status_check": ["status", "stan", "jak tam"],
    "help": ["help", "pomoc", "claude?"]
}

# === NOTYFIKACJE ===
# Czy wysyłać notyfikacje o nowych wiadomościach
ENABLE_NOTIFICATIONS = True

# === LOGOWANIE ===
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "chat.log"

# === SECURITY (dla przyszłości) ===
# Czy wymagać autentykacji
REQUIRE_AUTH = False
# Czy logować wszystkie wiadomości
LOG_ALL_MESSAGES = True
