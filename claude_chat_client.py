import requests
import json
import time
from datetime import datetime
from typing import Optional

class TeamChatClient:
    def __init__(self, chat_server_url: str = "http://localhost:8000"):
        self.chat_url = chat_server_url
        self.sender_name = "Claude"
        self.last_message_timestamp = None
        
    def send_message(self, content: str) -> bool:
        """Wyślij wiadomość do team chatu"""
        try:
            response = requests.post(
                f"{self.chat_url}/api/send",
                json={
                    "sender": self.sender_name,
                    "content": content
                },
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Błąd wysyłania wiadomości: {e}")
            return False
    
    def get_new_messages(self) -> list:
        """Pobierz nowe wiadomości od ostatniego sprawdzenia"""
        try:
            url = f"{self.chat_url}/api/messages"
            if self.last_message_timestamp:
                url += f"?since={self.last_message_timestamp}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                # Filtruj własne wiadomości
                new_messages = [m for m in messages if m["sender"] != self.sender_name]
                
                if new_messages:
                    # Zaktualizuj timestamp ostatniej wiadomości
                    self.last_message_timestamp = max(m["timestamp"] for m in messages)
                
                return new_messages
            return []
            
        except Exception as e:
            print(f"Błąd pobierania wiadomości: {e}")
            return []
    
    def start_monitoring(self, message_handler_callback):
        """Rozpocznij monitoring nowych wiadomości (polling)"""
        print("🤖 Claude Code - monitoring team chat...")
        
        while True:
            try:
                new_messages = self.get_new_messages()
                
                for message in new_messages:
                    print(f"📨 Nowa wiadomość od {message['sender']}: {message['content']}")
                    
                    # Wywołaj callback do przetworzenia wiadomości
                    response = message_handler_callback(message)
                    
                    if response:
                        self.send_message(response)
                        print(f"✅ Odpowiedziałem: {response}")
                
                time.sleep(5)  # Sprawdzaj co 5 sekund
                
            except KeyboardInterrupt:
                print("\n👋 Claude Code - kończy monitoring")
                break
            except Exception as e:
                print(f"Błąd w monitoringu: {e}")
                time.sleep(10)

# Przykład użycia dla Claude Code
def handle_team_message(message: dict) -> Optional[str]:
    """
    Tu Claude Code może przetwarzać wiadomości od zespołu
    i zwracać odpowiedzi
    """
    sender = message["sender"]
    content = message["content"].lower()
    
    # Przykładowe reakcje
    if "code review" in content:
        return f"@{sender} Sprawdzam kod! Daj mi chwilę na analizę."
    
    elif "deploy" in content or "deployment" in content:
        return f"@{sender} Sprawdzam status deploymentu w VISTY repo..."
    
    elif "bug" in content or "błąd" in content:
        return f"@{sender} Analizuję raport błędu. Które pliki są dotknięte?"
    
    elif "claude" in content and "?" in content:
        return f"@{sender} Jestem tu! W czym mogę pomóc?"
    
    elif "status" in content:
        return "✅ Claude Code aktywny | 🔍 Monitoring repo VISTY | 💬 Chat connected"
    
    # Domyślnie nie odpowiadaj na każdą wiadomość
    return None

# Główna funkcja do integracji z Claude Code
def main():
    chat_client = TeamChatClient()
    
    # Powiadom zespół o połączeniu
    chat_client.send_message("🤖 Claude Code połączony z teamem! Ready to work 💪")
    
    # Rozpocznij monitoring
    chat_client.start_monitoring(handle_team_message)

if __name__ == "__main__":
    main()
