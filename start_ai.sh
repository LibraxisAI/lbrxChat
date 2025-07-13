#!/bin/bash

echo "🤖 Multi-AI Team Chat Launcher"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany"
    exit 1
fi

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
        python3 multi_ai_integration.py klaudiusz
        ;;
    2)
        echo "🤖 Uruchamiam Claude..."
        python3 multi_ai_integration.py claude
        ;;
    3)
        echo "🎨 Uruchamiam Mikserka..."
        python3 multi_ai_integration.py mikserka
        ;;
    4)
        echo "🚀 Uruchamiam wszystkie AI..."
        python3 multi_ai_integration.py all
        ;;
    5)
        echo "💬 Uruchamiam tylko chat server..."
        python3 chat_server.py
        ;;
    *)
        echo "❌ Nieprawidłowy wybór"
        exit 1
        ;;
esac
