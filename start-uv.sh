#!/bin/bash

echo "🚀 Team Chat UV Edition - Pure UV Flow"
echo "====================================="

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV nie jest zainstalowany"
    echo "Instalacja: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n1)

echo ""
echo "🔧 UV Pure Flow:"
echo "Local IP: $LOCAL_IP"
echo ""

# UV sync dependencies
echo "📦 UV sync dependencies..."
uv sync

echo ""
echo "🏃 Uruchamiam chat server..."
echo "Chat będzie dostępny na:"
echo "  - Lokalnie: http://localhost:8000" 
echo "  - W sieci: http://$LOCAL_IP:8000"
echo ""
echo "Aby zatrzymać server: Ctrl+C"
echo ""

# Run with UV - no activation needed!
uv run python chat_server.py