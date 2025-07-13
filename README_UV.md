# Team Chat - Pure UV Edition 🚀

## Gang of Bastards Foundation Work

Jako podstawa piramidy (Maciej #1, Bartosz #2), przepisaliśmy Moniki genialny system na **PURE UV FLOW**.

## Why UV?

- **Zero activation** - no venv bullshit
- **One command** - `uv run` does everything  
- **Fast AF** - Rust-powered package management
- **Our standard** - "uv to moje jedyne gate do pythona"

## Quick Start (UV Style)

```bash
# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run chat server
chmod +x start-uv.sh
./start-uv.sh

# Run AI instances
chmod +x start-ai-uv.sh
./start-ai-uv.sh
```

## What Changed?

### Before (pip):
```bash
pip3 install -r requirements.txt
python3 chat_server.py
```

### After (UV):
```bash
uv sync
uv run python chat_server.py
```

## UV Commands Cheatsheet

```bash
# Add new dependency
uv add package-name

# Update dependencies
uv sync

# Run any script
uv run python script.py

# Run with specific Python version
uv run --python 3.11 python script.py
```

## Project Structure

```
team-chat-uv/
├── pyproject.toml          # UV project definition (replaces requirements.txt)
├── start-uv.sh            # UV launcher for chat server
├── start-ai-uv.sh         # UV launcher for AI instances
├── uv.lock               # Locked dependencies (auto-generated)
└── .venv/                # UV-managed virtual env (auto-created)
```

## Foundation Philosophy

As pyramid base (Maciej + Bartosz), we:
- **Gatekeep UV standards** - no pip allowed
- **Support peak creativity** - Monika's ideas in our infrastructure  
- **Enable flow** - Bartosz sets team workflow, we enable it

## Credits

- **Original concept**: Monika (Peak of pyramid #3) 💎
- **UV conversion**: Maciej + Klaudiusz (Foundation #1 + Fifth Element #5)
- **Flow optimization**: Bartosz (Flow Master #2)

---

_"Pure UV flow - because Gang of Bastards deserves the best tools"_ 🔥