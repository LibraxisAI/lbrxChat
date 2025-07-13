#!/bin/sh
# lbrxChat installer - Multi-AI Team Communication System
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ASCII art header
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                           L B R X   C H A T                              "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                    Multi-AI Team Communication System"
echo ""

# Platform detection
OS="$(uname -s)"
ARCH="$(uname -m)"

# Check OS
if [ "$OS" != "Darwin" ] && [ "$OS" != "Linux" ]; then
    echo "${RED}❌ Error: Unsupported operating system: $OS${NC}"
    echo "Supported: macOS, Linux"
    exit 1
fi

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "${RED}❌ Error: Python 3 is required but not found${NC}"
    echo ""
    echo "Please install Python 3 from: https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION detected"

# Check UV
if ! command -v uv >/dev/null 2>&1; then
    echo ""
    echo "${YELLOW}UV package manager not found${NC}"
    echo ""
    echo "UV is a fast, reliable Python package manager that lbrxChat uses."
    echo "Would you like to install it now? (recommended)"
    echo ""
    printf "Install UV? [Y/n]: "
    read -r response
    case "$response" in
        [nN][oO]|[nN])
            echo ""
            echo "Installation cancelled. To install manually:"
            echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
            exit 0
            ;;
        *)
            echo "Installing UV..."
            curl -LsSf https://astral.sh/uv/install.sh | sh || {
                echo "${RED}❌ UV installation failed${NC}"
                echo "Please install manually and run this installer again"
                exit 1
            }
            # Source shell config to get UV in PATH
            if [ -f "$HOME/.bashrc" ]; then
                . "$HOME/.bashrc"
            elif [ -f "$HOME/.zshrc" ]; then
                . "$HOME/.zshrc"
            fi
            ;;
    esac
fi

echo "✓ UV package manager detected"

# Installation directory
INSTALL_DIR="$HOME/.lbrxchat"
echo ""
echo "📦 Installing lbrxChat to: $INSTALL_DIR"

# Create directory
mkdir -p "$INSTALL_DIR"

# Clone repository
echo "📥 Downloading lbrxChat..."
if command -v git >/dev/null 2>&1; then
    git clone --quiet https://github.com/LibraxisAI/lbrxChat.git "$INSTALL_DIR/repo" 2>/dev/null || {
        echo "${RED}❌ Failed to clone repository${NC}"
        exit 1
    }
else
    # Fallback to curl/wget
    echo "Downloading via HTTPS..."
    curl -L https://github.com/LibraxisAI/lbrxChat/archive/main.tar.gz | tar -xz -C "$INSTALL_DIR" || {
        echo "${RED}❌ Failed to download${NC}"
        exit 1
    }
    mv "$INSTALL_DIR/lbrxChat-main" "$INSTALL_DIR/repo"
fi

# Install with UV
cd "$INSTALL_DIR/repo"
echo "📦 Installing dependencies..."
uv sync --quiet || {
    echo "${RED}❌ Dependency installation failed${NC}"
    exit 1
}

# Create launcher script
cat > "$INSTALL_DIR/lbrx-chat" << 'EOF'
#!/bin/sh
cd "$HOME/.lbrxchat/repo" && uv run python chat_server.py "$@"
EOF
chmod +x "$INSTALL_DIR/lbrx-chat"

# Create AI launcher
cat > "$INSTALL_DIR/lbrx-chat-ai" << 'EOF'
#!/bin/sh
cd "$HOME/.lbrxchat/repo" && uv run python multi_ai_integration.py "$@"
EOF
chmod +x "$INSTALL_DIR/lbrx-chat-ai"

# Configure port
echo ""
echo "🔧 Port Configuration..."
printf "Choose lbrxChat port (default 9310): "
read -r port_choice
PORT=${port_choice:-9310}

# Add to PATH
echo ""
echo "🔧 Setting up shell integration..."

add_to_path() {
    local shell_rc="$1"
    if [ -f "$shell_rc" ]; then
        if ! grep -q "lbrxchat" "$shell_rc"; then
            echo "" >> "$shell_rc"
            echo "# lbrxChat Configuration" >> "$shell_rc"
            echo "export PATH=\"\$HOME/.lbrxchat:\$PATH\"" >> "$shell_rc"
            echo "export LBRX_CHAT_PORT=$PORT" >> "$shell_rc"
            echo "✓ Added to $shell_rc (port: $PORT)"
        fi
    fi
}

# Create symlinks in user's local bin if exists
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$INSTALL_DIR/lbrx-chat" "$HOME/.local/bin/lbrx-chat" 2>/dev/null || true
    ln -sf "$INSTALL_DIR/lbrx-chat-ai" "$HOME/.local/bin/lbrx-chat-ai" 2>/dev/null || true
fi

# Add to shell configs
add_to_path "$HOME/.bashrc"
add_to_path "$HOME/.zshrc"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "${GREEN}✨ lbrxChat installed successfully!${NC}"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "  1. Restart your terminal or run: source ~/.zshrc"
echo "  2. Start chat server: ${GREEN}lbrx-chat${NC}"
echo "  3. Start AI instances: ${GREEN}lbrx-chat-ai${NC}"
echo ""
echo "📖 Documentation: https://github.com/LibraxisAI/lbrxChat"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"