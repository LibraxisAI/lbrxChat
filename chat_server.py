from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import sqlite3
import json
import asyncio
from datetime import datetime
from typing import List
import requests
from pydantic import BaseModel

app = FastAPI()

# Model dla wiadomości
class Message(BaseModel):
    sender: str
    content: str
    timestamp: str = None

# Lista aktywnych WebSocket połączeń
active_connections: List[WebSocket] = []

# Inicjalizacja bazy danych
def init_db():
    conn = sqlite3.connect('chat.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# WebSocket manager
async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

def disconnect_websocket(websocket: WebSocket):
    active_connections.remove(websocket)

async def broadcast_message(message: dict):
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            active_connections.remove(connection)

# Zapisz wiadomość do bazy
def save_message(sender: str, content: str):
    conn = sqlite3.connect('chat.db')
    timestamp = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO messages (sender, content, timestamp) VALUES (?, ?, ?)",
        (sender, content, timestamp)
    )
    conn.commit()
    conn.close()
    return timestamp

# Pobierz ostatnie wiadomości
def get_recent_messages(limit: int = 50):
    conn = sqlite3.connect('chat.db')
    cursor = conn.execute(
        "SELECT sender, content, timestamp FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    messages = cursor.fetchall()
    conn.close()
    return [{"sender": m[0], "content": m[1], "timestamp": m[2]} for m in reversed(messages)]

# ENDPOINTS

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect_websocket(websocket)
    try:
        while True:
            # Czekaj na wiadomości od frontendu
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Zapisz i broadcast
            timestamp = save_message(message_data["sender"], message_data["content"])
            message_data["timestamp"] = timestamp
            
            await broadcast_message(message_data)
            
            # Wyślij do Claude Code jeśli wiadomość nie jest od niego
            if message_data["sender"] != "Claude":
                await send_to_claude(message_data)
                
    except WebSocketDisconnect:
        disconnect_websocket(websocket)

# API endpoint dla Claude Code do wysyłania wiadomości
@app.post("/api/send")
async def send_message(message: Message):
    timestamp = save_message(message.sender, message.content)
    
    message_dict = {
        "sender": message.sender,
        "content": message.content,
        "timestamp": timestamp
    }
    
    await broadcast_message(message_dict)
    return {"status": "sent", "timestamp": timestamp}

# API endpoint dla Claude Code do pobierania nowych wiadomości
@app.get("/api/messages")
async def get_messages(since: str = None):
    if since:
        conn = sqlite3.connect('chat.db')
        cursor = conn.execute(
            "SELECT sender, content, timestamp FROM messages WHERE timestamp > ? ORDER BY id",
            (since,)
        )
        messages = cursor.fetchall()
        conn.close()
        return [{"sender": m[0], "content": m[1], "timestamp": m[2]} for m in messages]
    else:
        return get_recent_messages()

# Funkcja do wysyłania wiadomości do Claude Code
async def send_to_claude(message: dict):
    try:
        # Tu wstawcie URL waszego Claude Code endpoint
        claude_url = "http://localhost:8001/receive-message"  # ZMIENIĆ NA WŁAŚCIWY
        
        response = requests.post(claude_url, json=message, timeout=5)
        print(f"Sent to Claude: {response.status_code}")
    except Exception as e:
        print(f"Failed to send to Claude: {e}")

# Serwuj frontend
@app.get("/")
async def get_chat():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>Team Chat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .chat-container { max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chat-header { background: #4a90e2; color: white; padding: 15px; text-align: center; }
        .messages { height: 400px; overflow-y: auto; padding: 15px; border-bottom: 1px solid #eee; }
        .message { margin-bottom: 10px; padding: 10px; border-radius: 8px; }
        .message.claude { background: #e3f2fd; border-left: 4px solid #2196f3; }
        .message.human { background: #f3e5f5; border-left: 4px solid #9c27b0; }
        .message .sender { font-weight: bold; margin-bottom: 5px; }
        .message .timestamp { font-size: 0.8em; color: #666; margin-left: 10px; }
        .message .content { margin-top: 5px; }
        .input-area { display: flex; padding: 15px; }
        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-right: 10px; }
        .input-area button { padding: 10px 20px; background: #4a90e2; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .input-area button:hover { background: #357abd; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>Team Chat - 3 Humans + 3 AI</h2>
        </div>
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Napisz wiadomość..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Wyślij</button>
        </div>
    </div>

    <script>
        const ws = new WebSocket('ws://localhost:8000/ws');
        const messages = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        
        // Prompt for username on load
        const username = prompt("Podaj swoje imię:") || "Anonim";
        
        ws.onmessage = function(event) {
            const message = JSON.parse(event.data);
            displayMessage(message);
        };
        
        function displayMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message.sender === 'Claude' ? 'claude' : 'human'}`;
            
            const time = new Date(message.timestamp).toLocaleTimeString();
            
            messageDiv.innerHTML = `
                <div class="sender">
                    ${message.sender}
                    <span class="timestamp">${time}</span>
                </div>
                <div class="content">${message.content}</div>
            `;
            
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
        }
        
        function sendMessage() {
            const content = messageInput.value.trim();
            if (content) {
                const message = {
                    sender: username,
                    content: content
                };
                
                ws.send(JSON.stringify(message));
                messageInput.value = '';
            }
        }
        
        // Load recent messages on connect
        fetch('/api/messages')
            .then(response => response.json())
            .then(messages => {
                messages.forEach(displayMessage);
            });
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
