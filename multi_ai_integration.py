import requests
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
import random

# Import konfiguracji
from config_multi_ai import (
    AI_MEMBERS, AI_PERSONALITIES, AI_MODEL_MAPPING, 
    MULTI_AI_RESPONSE_STRATEGY, AI_PRIORITY, CUSTOM_PROMPTS,
    LIBRAXIS_API_BASE_URL, LIBRAXIS_API_KEY, ENABLE_AI_TO_AI_CHAT,
    CHAT_SERVER_HOST, CHAT_SERVER_PORT
)

class LibraxisAIClient:
    """Client dla integracji z LibraxisAI - wspiera różne modele"""
    
    def __init__(self, base_url: str = LIBRAXIS_API_BASE_URL):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
        }
        if LIBRAXIS_API_KEY:
            self.headers["Authorization"] = f"Bearer {LIBRAXIS_API_KEY}"
    
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
    
    async def generate_response(self, message: str, ai_name: str, context: list = None) -> str:
        """Wygeneruj odpowiedź dla konkretnego AI"""
        try:
            # Wybierz model dla danego AI
            model = AI_MODEL_MAPPING.get(ai_name, "default")
            
            payload = {
                "model": model,
                "messages": context or [{"role": "user", "content": message}],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                return f"Błąd API: {response.status_code}"
                
        except Exception as e:
            print(f"Błąd generowania odpowiedzi dla {ai_name}: {e}")
            return "Przepraszam, mam problem z połączeniem."

class MultiAITeamChatClient:
    """Enhanced client dla 3 AI w zespole"""
    
    def __init__(self, ai_name: str, chat_server_url: str = None):
        self.ai_name = ai_name
        self.ai_config = AI_MEMBERS[ai_name]
        self.chat_url = chat_server_url or f"http://{CHAT_SERVER_HOST}:{CHAT_SERVER_PORT}"
        self.last_message_timestamp = None
        self.libraxis_client = LibraxisAIClient()
        self.conversation_context = []
        
        # Unique sender name z emoji
        self.sender_name = f"{self.ai_config['name']} {self.ai_config['emoji']}"
        
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
                new_messages = [m for m in messages if not m["sender"].startswith(self.ai_config['name'])]
                
                if new_messages:
                    self.last_message_timestamp = max(m["timestamp"] for m in messages)
                
                return new_messages
            return []
            
        except Exception as e:
            print(f"Błąd pobierania wiadomości: {e}")
            return []
    
    def should_respond(self, message: dict) -> bool:
        """Sprawdź czy to AI powinno odpowiedzieć na wiadomość"""
        content = message["content"].lower()
        sender = message["sender"]
        
        # Nie odpowiadaj na wiadomości od innych AI (chyba że włączone AI-to-AI)
        if any(ai_name in sender for ai_name in AI_MEMBERS.keys()) and not ENABLE_AI_TO_AI_CHAT:
            return False
        
        # Sprawdź triggery specyficzne dla tego AI
        ai_triggers = self.ai_config.get('triggers', [])
        if any(trigger in content for trigger in ai_triggers):
            return True
        
        # Sprawdź ogólne triggery
        general_triggers = ["?", "help", "pomoc", "status"]
        if any(trigger in content for trigger in general_triggers):
            return True
            
        return False
    
    def update_conversation_context(self, message: dict):
        """Aktualizuj kontekst konwersacji"""
        self.conversation_context.append({
            "role": "user",
            "content": f"{message['sender']}: {message['content']}"
        })
        
        # Zachowaj tylko ostatnie 10 wiadomości
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
    
    async def generate_smart_response(self, message: dict) -> Optional[str]:
        """Wygeneruj inteligentną odpowiedź używając LibraxisAI"""
        content = message["content"].lower()
        sender = message["sender"]
        
        self.update_conversation_context(message)
        
        if not self.should_respond(message):
            return None
        
        # Przygotuj prompt specyficzny dla tego AI
        ai_prompts = CUSTOM_PROMPTS[self.ai_name]
        system_prompt = ai_prompts["system"]
        
        # Dodaj kontekst roli
        role_context = f"""
        Twoja rola w zespole: {self.ai_config['description']}
        Owner: {self.ai_config['owner']}
        Primary role: {self.ai_config['primary_role']}
        
        Odpowiadaj zgodnie ze swoją personalności i używaj emoji {self.ai_config['emoji']}.
        Zwracaj się do użytkownika: @{sender}
        """
        
        full_context = [
            {"role": "system", "content": system_prompt + role_context},
            *self.conversation_context[-5:],
        ]
        
        try:
            response = await self.libraxis_client.generate_response(
                message=content,
                ai_name=self.ai_name,
                context=full_context
            )
            
            return response if response and len(response.strip()) > 0 else None
            
        except Exception as e:
            print(f"Błąd generowania smart response dla {self.ai_name}: {e}")
            return self.get_fallback_response(content, sender)
    
    def get_fallback_response(self, content: str, sender: str) -> Optional[str]:
        """Fallback responses gdy LibraxisAI nie działa"""
        emoji = self.ai_config['emoji']
        
        # Responses specyficzne dla każdego AI
        if self.ai_name == "klaudiusz":
            if "code review" in content:
                return f"@{sender} Sprawdzam kod! {emoji} Analizuję VISTY repo..."
            elif "deploy" in content:
                return f"@{sender} Monitoruję deployment {emoji} Sprawdzam logi..."
            elif "visty" in content:
                return f"@{sender} Repo VISTY status: aktywny {emoji}"
                
        elif self.ai_name == "claude":
            if "help" in content or "pomoc" in content:
                return f"@{sender} Jestem tu żeby pomóc! {emoji} Czym się zajmiemy?"
            elif "organize" in content or "koordynacja" in content:
                return f"@{sender} Organizuję zadania zespołu {emoji}"
                
        elif self.ai_name == "mikserka":
            if "brainstorm" in content or "pomysł" in content:
                return f"@{sender} Czas na kreatywne myślenie! {emoji} Jakie mamy wyzwanie?"
            elif "creative" in content or "idea" in content:
                return f"@{sender} Generuję innowacyjne rozwiązania {emoji}"
        
        # Ogólne responses
        if "status" in content:
            return f"{emoji} {self.ai_config['name']} aktywny | Role: {self.ai_config['primary_role']} | Owner: {self.ai_config['owner']}"
        elif self.ai_config['name'].lower() in content:
            return f"@{sender} Jestem tu! {emoji} Specjalizuję się w: {self.ai_config['primary_role']}"
            
        return None
    
    async def start_monitoring(self):
        """Rozpocznij monitoring z AI-specific behavior"""
        print(f"{self.ai_config['emoji']} {self.ai_config['name']} (Owner: {self.ai_config['owner']}) - monitoring team chat...")
        
        # Sprawdź dostępne modele
        models = await self.libraxis_client.get_available_models()
        if models:
            print(f"📊 LibraxisAI modele dostępne: {len(models)}")
            self.send_message(f"{self.ai_config['emoji']} {self.ai_config['name']} połączony! Role: {self.ai_config['primary_role']} (Owner: {self.ai_config['owner']}) 💪")
        else:
            print("⚠️ LibraxisAI niedostępny, używam fallback")
            self.send_message(f"{self.ai_config['emoji']} {self.ai_config['name']} connected! (Fallback mode)")
        
        while True:
            try:
                new_messages = self.get_new_messages()
                
                for message in new_messages:
                    print(f"📨 [{self.ai_name}] Nowa wiadomość od {message['sender']}: {message['content']}")
                    
                    response = await self.generate_smart_response(message)
                    
                    if response:
                        # Dodaj delay żeby AI nie odpowiadały jednocześnie
                        await asyncio.sleep(random.uniform(0.5, 2.0))
                        
                        self.send_message(response)
                        print(f"✅ [{self.ai_name}] Odpowiedziałem: {response}")
                
                await asyncio.sleep(5)
                
            except KeyboardInterrupt:
                print(f"\n👋 {self.ai_config['name']} - kończy monitoring")
                break
            except Exception as e:
                print(f"Błąd w monitoringu {self.ai_name}: {e}")
                await asyncio.sleep(10)

# Funkcje do uruchamiania konkretnych AI
async def start_klaudiusz():
    """Uruchom Klaudiusza (Claude Macieja)"""
    client = MultiAITeamChatClient("klaudiusz")
    await client.start_monitoring()

async def start_claude():
    """Uruchom Claude (Moniki)"""
    client = MultiAITeamChatClient("claude") 
    await client.start_monitoring()

async def start_mikserka():
    """Uruchom Mikserka (GPT)"""
    client = MultiAITeamChatClient("mikserka")
    await client.start_monitoring()

async def start_all_ai():
    """Uruchom wszystkie AI jednocześnie"""
    await asyncio.gather(
        start_klaudiusz(),
        start_claude(), 
        start_mikserka()
    )

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        ai_name = sys.argv[1].lower()
        if ai_name == "klaudiusz":
            asyncio.run(start_klaudiusz())
        elif ai_name == "claude":
            asyncio.run(start_claude())
        elif ai_name == "mikserka":
            asyncio.run(start_mikserka())
        elif ai_name == "all":
            asyncio.run(start_all_ai())
        else:
            print("Dostępne AI: klaudiusz, claude, mikserka, all")
    else:
        print("Użyj: python multi_ai_integration.py [klaudiusz|claude|mikserka|all]")
        print("\nPrzykłady:")
        print("python multi_ai_integration.py klaudiusz  # Tylko Klaudiusz")
        print("python multi_ai_integration.py claude     # Tylko Claude") 
        print("python multi_ai_integration.py mikserka   # Tylko Mikserka")
        print("python multi_ai_integration.py all        # Wszystkie AI")
