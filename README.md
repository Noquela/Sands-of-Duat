# Sands of Duat

An innovative roguelike deck-builder set in the ancient Egyptian underworld during the 12 hours of the night. Features the unique **Hour-Glass Initiative** combat system where timing and resource management create tactical depth beyond traditional turn-based mechanics.

## 🎮 Core Innovation: Hour-Glass Initiative System

### Concept
- Each combatant possesses an "Hour-Glass" containing 0-6 grains of sand
- Playing cards costs sand (0-6 cost range)
- Sand regenerates in real-time at 1 grain per second
- Creates strategic tension between quick cheap plays vs powerful expensive cards with downtime
- Enemy sand gauges are visible, enabling tactical timing predictions

### Strategic Implications
- **Stutter-stepping**: Chain cheap (0-1 cost) cards for rapid pressure
- **Power spikes**: Save sand for expensive (4-6 cost) game-changing moves
- **Tempo reading**: Watch enemy sand to predict their next major play
- **Animation timing**: Sand regen pauses during animations to maintain sync

## 🏛️ Project Structure

```
sands_duat/
├── core/                    # Engine systems
│   ├── hourglass.py        # Sand management & timing
│   ├── combat.py           # Combat engine & queue
│   ├── ecs.py              # Entity component system
│   ├── cards.py            # Card system & effects
│   └── engine.py           # Main game loop
├── content/                # YAML definitions
│   ├── cards/              # Card definitions
│   ├── enemies/            # Enemy data
│   ├── events/             # Map events
│   └── decks/              # Starting decks
├── assets/                 # Generated art & audio
│   ├── art_raw/            # AI-generated base images
│   ├── art_clean/          # Upscaled & processed
│   ├── audio/              # Sound effects & music
│   └── fonts/              # Egyptian-themed fonts
├── tools/                  # Development utilities
│   ├── gen_art.py          # ComfyUI batch driver
│   ├── upscale.py          # Real-ESRGAN wrapper
│   ├── lora_train.py       # Style consistency training
│   └── content_validator.py # YAML validation
├── ui/                     # Game interface
│   ├── combat_screen.py    # Main battle UI
│   ├── map_screen.py       # Node progression
│   └── deck_builder.py     # Card collection management
└── tests/                  # Automated testing
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- CUDA-capable GPU (RTX 5070 or equivalent) for AI art generation
- 16GB+ RAM recommended

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd sand-of-duat
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the game:**
```bash
python main.py
```

### Development Mode
```bash
python main.py --dev-mode --debug --windowed
```

## 🎨 Asset Generation Pipeline

The game uses a local AI art generation pipeline optimized for RTX 5070:

### AI Model Stack
1. **Playground v2.5** (12GB VRAM): High-aesthetic concept art generation
2. **Stable Cascade** (14GB VRAM): High-resolution decode and inpainting
3. **Kandinsky 3.0** (Apache-2.0): Style variety and backup generation
4. **Real-ESRGAN** (Minimal VRAM): 4x upscaling with edge enhancement

### Workflow Commands
```bash
# Generate card art from YAML prompts
python tools/gen_art.py --content content/cards/ --output assets/art_raw/

# Upscale and clean
python tools/upscale.py assets/art_raw assets/art_clean --model real-esrgan

# Apply Egyptian papyrus overlay
python tools/add_papyrus_overlay.py assets/art_clean --opacity 0.6

# Train style consistency LoRA (after 30+ images)
python tools/lora_train.py --model playground-v2.5 --images assets/art_clean --output loras/duat_style
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Core system tests
python -m pytest tests/test_hourglass.py tests/test_combat.py tests/test_cards.py -v

# Performance tests
python -m pytest tests/test_performance.py -v

# Content validation
python tests/test_content.py
```

### Validate YAML Content
```bash
python tools/content_validator.py --content-dir content/
```

## 🎯 Card Categories by Sand Cost

- **0-1 Sand**: Cantrips, weak attacks, utility (rapid fire potential)
- **2-3 Sand**: Standard attacks, moderate effects (balanced tempo)
- **4-5 Sand**: Powerful spells, game-changing effects (setup required)
- **6 Sand**: Ultimate abilities, fight-ending moves (maximum commitment)

### Sample Card Progression
```yaml
# Early game tempo card
id: desert_strike
cost: 1
effects: [damage: 6, draw: 1]

# Mid-game value card  
id: solar_flare
cost: 3
effects: [damage: 12, ignite: 2]

# Late game finisher
id: judgment_of_anubis
cost: 6
effects: [damage: 25, execute_if_below: 15]
```

## 🏗️ Development Tools

### Content Hot-Reload
The game supports hot-reloading of YAML content files during development:
```bash
# Start with hot-reload enabled
python main.py --dev-mode
# Edit any YAML file in content/ and see changes immediately
```

### Performance Monitoring
```bash
# Run performance benchmarks
python tests/test_performance.py

# Profile specific systems
python -m cProfile main.py --dev-mode > profile.txt
```

### Asset Processing
```bash
# Optimize images for game use
python tools/asset_processor.py optimize assets/art_raw assets/art_clean

# Create card frames
python tools/asset_processor.py cards assets/art_clean assets/cards

# Generate asset manifest
python tools/asset_processor.py manifest assets/ assets/manifest.json
```

## 🎮 Controls

### Global Controls
- **F11**: Toggle fullscreen
- **Alt+F4**: Exit game
- **ESC**: Exit (dev mode only)

### Combat Controls
- **Mouse**: Select and play cards
- **Spacebar**: End turn
- **Tab**: View detailed card information

## 📊 Performance Targets

### Technical Goals
- Sand regeneration accuracy within 50ms of target timing
- Hot-reload system responds within 200ms of file changes
- Combat engine handles 60fps with smooth animations
- Asset generation produces consistent Egyptian aesthetic

### Gameplay Goals
- Combat decisions every 2-3 seconds maintain engagement
- Sand cost distribution creates meaningful timing choices
- Enemy AI demonstrates varied sand usage patterns
- Player progression feels rewarding and strategic

## 🤝 Contributing

### Development Workflow
1. Create feature branch from main
2. Write tests for new functionality
3. Implement feature with proper documentation
4. Run full test suite: `python -m pytest tests/ -v`
5. Validate content: `python tools/content_validator.py`
6. Submit pull request

### Code Style
- Use Black for code formatting: `black sands_duat/`
- Use flake8 for linting: `flake8 sands_duat/`
- Use mypy for type checking: `mypy sands_duat/`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ancient Egyptian mythology and art for thematic inspiration
- The deck-building and roguelike communities for gameplay inspiration
- Open-source AI model creators for enabling local art generation
- Python game development community for tools and libraries

---

**🏺 "In the depths of the Duat, every grain of sand counts..." 🏺**