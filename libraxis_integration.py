import requests
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

class LibraxisAIClient:
    """Client dla integracji z waszymi endpointami LibraxisAI"""
    
    def __init__(self, base_url: str = "https://llm.libraxis.cloud/api/v1"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            # Dodajcie API key jeśli używacie
            # "Authorization": "Bearer YOUR_API_KEY"
        }
    
    async def get_available_models(self) -> list:
        """Pobierz listę dostępnych modeli"""
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Błąd pobierania modeli: {e}")
            return []
    
    async def generate_response(self, message: str, model: str = None, context: list = None) -> str:
        """Wygeneruj odpowiedź używając waszego LLM API"""
        try:
            # Adaptuj format do waszego API
            payload = {
                "model": model or "default",  # Użyjcie domyślnego modelu
                "messages": context or [{"role": "user", "content": message}],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",  # Sprawdźcie właściwy endpoint
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Adaptuj do formatu odpowiedzi z waszego API
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return f"Błąd API: {response.status_code}"
                
        except Exception as e:
            print(f"Błąd generowania odpowiedzi: {e}")
            return "Przepraszam, mam problem z połączeniem."

class EnhancedTeamChatClient:
    """Rozszerzony client chatu z integracją LibraxisAI"""
    
    def __init__(self, chat_server_url: str = "http://localhost:8000"):
        self.chat_url = chat_server_url
        self.sender_name = "Claude-LibraxisAI"
        self.last_message_timestamp = None
        self.libraxis_client = LibraxisAIClient()
        self.conversation_context = []  # Historia konwersacji dla kontekstu
        
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
                    self.last_message_timestamp = max(m["timestamp"] for m in messages)
                
                return new_messages
            return []
            
        except Exception as e:
            print(f"Błąd pobierania wiadomości: {e}")
            return []
    
    def update_conversation_context(self, message: dict):
        """Aktualizuj kontekst konwersacji"""
        self.conversation_context.append({
            "role": "user",
            "content": f"{message['sender']}: {message['content']}"
        })
        
        # Zachowaj tylko ostatnie 10 wiadomości dla kontekstu
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
    
    async def generate_smart_response(self, message: dict) -> Optional[str]:
        """Wygeneruj inteligentną odpowiedź używając LibraxisAI"""
        content = message["content"].lower()
        sender = message["sender"]
        
        # Dodaj wiadomość do kontekstu
        self.update_conversation_context(message)
        
        # Sprawdź czy Claude powinien odpowiedzieć
        should_respond = any([
            "claude" in content,
            "?" in content and len(content.split()) < 15,  # Krótkie pytania
            "code review" in content,
            "bug" in content or "błąd" in content,
            "deploy" in content,
            "help" in content or "pomoc" in content,
            "status" in content
        ])
        
        if not should_respond:
            return None
        
        # Przygotuj prompt z kontekstem
        system_prompt = f"""Jesteś Claude Code, członek zespołu 3 humans + 3 AI. 
        Pomagasz w:
        - Code review i analiza kodu
        - Monitorowanie repo VISTY 
        - Debugging i rozwiązywanie problemów
        - Deployment i DevOps
        
        Odpowiadaj krótko, konkretnie i pomocnie. Używaj emoji tam gdzie pasuje.
        Zwracaj się do użytkownika po imieniu: @{sender}"""
        
        # Przygotuj pełny kontekst dla LLM
        full_context = [
            {"role": "system", "content": system_prompt},
            *self.conversation_context[-5:],  # Ostatnie 5 wiadomości kontekstu
        ]
        
        try:
            response = await self.libraxis_client.generate_response(
                message=content,
                context=full_context
            )
            
            return response if response and len(response.strip()) > 0 else None
            
        except Exception as e:
            print(f"Błąd generowania smart response: {e}")
            # Fallback do prostych odpowiedzi
            return self.get_fallback_response(content, sender)
    
    def get_fallback_response(self, content: str, sender: str) -> Optional[str]:
        """Proste odpowiedzi fallback gdy LibraxisAI nie działa"""
        if "code review" in content:
            return f"@{sender} Sprawdzam kod! 🔍 Daj mi chwilę na analizę."
        elif "deploy" in content:
            return f"@{sender} Monitoruję deployment... 🚀"
        elif "bug" in content or "błąd" in content:
            return f"@{sender} Analizuję problem 🐛 Które pliki są dotknięte?"
        elif "status" in content:
            return "✅ Claude Code aktywny | 🔍 Monitoring VISTY | 💬 LibraxisAI connected"
        elif "claude" in content and "?" in content:
            return f"@{sender} Jestem tu! W czym mogę pomóc? 🤖"
        return None
    
    async def start_monitoring(self):
        """Rozpocznij monitoring z AI-powered responses"""
        print("🤖 Claude Code + LibraxisAI - monitoring team chat...")
        
        # Sprawdź dostępne modele przy starcie
        models = await self.libraxis_client.get_available_models()
        if models:
            print(f"📊 Dostępne modele LibraxisAI: {len(models)}")
            self.send_message(f"🤖 Claude Code połączony! Using LibraxisAI models: {len(models)} dostępnych 💪")
        else:
            print("⚠️ Nie udało się pobrać listy modeli, używam fallback responses")
            self.send_message("🤖 Claude Code połączony! (Fallback mode) 💪")
        
        while True:
            try:
                new_messages = self.get_new_messages()
                
                for message in new_messages:
                    print(f"📨 Nowa wiadomość od {message['sender']}: {message['content']}")
                    
                    # Wygeneruj smart response
                    response = await self.generate_smart_response(message)
                    
                    if response:
                        self.send_message(response)
                        print(f"✅ Odpowiedziałem: {response}")
                
                await asyncio.sleep(5)  # Sprawdzaj co 5 sekund
                
            except KeyboardInterrupt:
                print("\n👋 Claude Code - kończy monitoring")
                break
            except Exception as e:
                print(f"Błąd w monitoringu: {e}")
                await asyncio.sleep(10)

# Główna funkcja z integracją LibraxisAI
async def main():
    chat_client = EnhancedTeamChatClient()
    await chat_client.start_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
