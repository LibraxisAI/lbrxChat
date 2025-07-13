#!/bin/bash

echo "🚀 Team Chat - Quick Start"
echo "=========================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany"
    exit 1
fi

# Install dependencies
echo "📦 Instaluję dependencje..."
pip3 install -r requirements.txt

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n1)

echo ""
echo "🔧 Konfiguracja:"
echo "Local IP: $LOCAL_IP"
echo ""

# Start chat server
echo "🏃 Uruchamiam chat server..."
echo "Chat będzie dostępny na:"
echo "  - Lokalnie: http://localhost:8000" 
echo "  - W sieci: http://$LOCAL_IP:8000"
echo ""
echo "Aby zatrzymać server: Ctrl+C"
echo ""

python3 chat_server.py
