# Sands of Duat

A roguelike action hack-&-slash game inspired by *Hades*, set in Egyptian mythology. Built with Python and Pygame.

## 🏺 Game Overview

**Sands of Duat** is a roguelike action game where you play as a warrior navigating the Egyptian underworld. Features include:

- **Egyptian Mythology Theme**: Anubis warriors, scarab enemies, mummy guardians
- **Roguelike Mechanics**: Procedural arenas, divine boons, permanent progression
- **Hub System**: Central lobby similar to Hades' Hall of Styx
- **Combat System**: Light/heavy attacks, elemental effects (fire, ice, poison)
- **Artifact Deck**: Collectible items that modify gameplay

## 🛠️ Development Setup

### Prerequisites
- Python 3.13
- CUDA 12.8 (for AI asset generation)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Noquela/Sands-of-Duat.git
cd Sands-of-Duat
```

2. **Set up virtual environment:**
```bash
python -m venv .venv313
# Windows:
.venv313\Scripts\activate
# Linux/Mac:
source .venv313/bin/activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt

# For PyTorch with CUDA 12.8 (Windows):
pip install --index-url https://download.pytorch.org/whl/nightly/cu128 --extra-index-url https://pypi.org/simple torch torchvision torchaudio
```

## 🎮 Running the Game

```bash
python src/game.py
```

## 🏗️ Project Structure

```
SandsOfDuat/
├── assets/
│   ├── generated/        # AI-generated game assets
│   └── raw/              # Original artwork
├── src/
│   ├── ecs/              # Entity-Component-System
│   ├── scenes/           # Game scenes (Hub, Arena)
│   ├── ui/               # User interface
│   └── game.py           # Main entry point
├── tools/
│   ├── pygame_mcp.py     # Game execution MCP server
│   └── sdxl_mcp.py       # Asset generation MCP server
├── tests/                # Unit tests
└── requirements.txt      # Python dependencies
```

## 🤖 MCP Tools

This project includes custom MCP (Model Context Protocol) servers for development:

- **pygame_mcp.py**: Game execution, FPS profiling, file operations
- **sdxl_mcp.py**: AI asset generation using Stable Diffusion XL

## 🎨 Art Generation Workflow

1. **Generate sprites**: Use `sprite_sheet()` tool for character animations
2. **Optimize colors**: Apply `palette_reduce()` for pixel art style
3. **Egyptian themes**: Prompts focus on golden armor, hieroglyphs, desert aesthetics

## 🔧 Development Commands

```bash
# Code quality
ruff src/                 # Linting
black src/                # Formatting
mypy --strict src/        # Type checking

# Testing
pytest tests/             # Run tests
```

## 📋 Development Phases

- **Sprint 0**: Project setup and tooling
- **Sprint 1**: Basic character movement and rendering
- **Sprint 2**: Combat system and enemy AI
- **Sprint 3**: Item/artifact deck system
- **Sprint 4**: Boss battles and progression
- **Sprint 5**: Polish and optimization

## 🎯 Technical Goals

- **Performance**: Maintain 60+ FPS on target hardware
- **Code Quality**: Strict typing with mypy, consistent formatting
- **Architecture**: Clean ECS pattern with modular systems
- **Art Pipeline**: Automated asset generation with AI tools

## 📄 License

This project is developed for educational and portfolio purposes.

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome!

---

*May the gods favor your code!* 🏺⚡