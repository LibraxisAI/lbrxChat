#!/bin/bash

echo "🤖 Multi-AI Team Chat - UV Edition"
echo "================================="

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV nie jest zainstalowany"
    echo "Instalacja: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Ensure dependencies are synced
echo "📦 UV sync check..."
uv sync --quiet

echo ""
echo "Wybierz które AI uruchomić:"
echo "1) 🔍 Klaudiusz (Maciej) - Code review, VISTY monitoring"
echo "2) 🤖 Claude (Monika) - Team coordination, general help"
echo "3) 🎨 Mikserka (GPT) - Creative solutions, brainstorming"
echo "4) 🚀 Wszystkie AI jednocześnie"
echo "5) 💬 Tylko chat server (bez AI)"

read -p "Wybierz opcję (1-5): " choice

case $choice in
    1)
        echo "🔍 Uruchamiam Klaudiusza..."
        uv run python multi_ai_integration.py klaudiusz
        ;;
    2)
        echo "🤖 Uruchamiam Claude..."
        uv run python multi_ai_integration.py claude
        ;;
    3)
        echo "🎨 Uruchamiam Mikserka..."
        uv run python multi_ai_integration.py mikserka
        ;;
    4)
        echo "🚀 Uruchamiam wszystkie AI..."
        uv run python multi_ai_integration.py all
        ;;
    5)
        echo "💬 Uruchamiam tylko chat server..."
        uv run python chat_server.py
        ;;
    *)
        echo "❌ Nieprawidłowy wybór"
        exit 1
        ;;
esac