# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
**Sands of Duat** is a roguelike action hack-&-slash game inspired by Hades but with Egyptian mythology themes. Built with Python 3.13 and Pygame 2.6, targeting PC (16:9 + ultrawide 3440×1440 UWQHD).

## Core Game Architecture
- **ECS Pattern**: Entity-Component-System using `@dataclass` components
- **Scene System**: Hub (lobby) and procedural arenas with portal transitions
- **Combat System**: Light/heavy attacks, divine boons (fire/ice/poison effects), artifact deck management
- **Progression**: Permanent upgrades (Mirror of Nyx style), sacred checkpoints between floors

## Development Environment Setup
```bash
# Windows setup
python -m venv .venv313
.venv313\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# PyTorch with CUDA 12.8 (nightly)
pip install --index-url https://download.pytorch.org/whl/nightly/cu128 --extra-index-url https://pypi.org/simple torch torchvision torchaudio
```

## Project Structure
```
SandsOfDuat/
├─ assets/
│  ├─ generated/        # SDXL output
│  └─ raw/              # original artwork
├─ src/
│  ├─ ecs/              # systems & components
│  ├─ scenes/
│  ├─ ui/
│  └─ game.py           # entry-point
├─ tools/
│  ├─ pygame_mcp.py     # game execution MCP
│  └─ sdxl_mcp.py       # asset generation MCP
├─ tests/
├─ requirements.txt
└─ Instructions.txt     # master project prompt
```

## Key Dependencies
- **Core**: pygame==2.6.1, mcp>=0.5
- **AI/Graphics**: diffusers>=0.29.0, torch (nightly cu128), transformers>=4.43.0
- **Development**: mypy (strict mode), ruff, black (100 col), conventional commits

## Development Commands
```bash
# Run game
python src/game.py

# Code quality
ruff src/
black src/ --line-length 100
mypy --strict src/

# Testing
pytest tests/
```

## MCP Tools Available
- **pygame_mcp.py**: `run_game(entry)`, `profile_fps(seconds)`, file operations
- **sdxl_mcp.py**: `text2img()`, `img2img()`, `sprite_sheet()`, `palette_reduce()`

## Art Generation Workflow
1. **Base Prompt**: "Egyptian warrior Anubis, golden armor, Hades style..."
2. **Generation**: Use `sprite_sheet()` for 4×4 frames, 512px
3. **Processing**: `palette_reduce()` for optimization
4. **Integration**: Verify hitboxes in Pygame

## Code Conventions
- ECS components as `@dataclass`
- Type hints with mypy strict mode
- 100 character line limit
- Conventional commit messages
- Performance profiling with `profile_fps(10)` for <60 FPS optimizations

## Sprint Development Phases
1. **Sprint 0**: Setup (venv, MCP tools, CI/CD)
2. **Sprint 1**: Base character (Transform, SpriteRenderer, InputController)
3. **Sprint 2**: Combat & enemies (AttackSystem, HealthComponent, AI)
4. **Sprint 3**: Deck & items (ArtifactComponent, UI, StatSystem)
5. **Sprint 4**: Boss & progression (BossSystem, permanent upgrades)
6. **Sprint 5**: Polish (menus, audio, optimization)

## Performance Targets
- Maintain 60+ FPS (use `profile_fps()` to verify)
- PyTorch autocast + `enable_vae_slicing` for GPU efficiency
- Batch operations and object pooling for optimization

## Agent Roles (When Using Specialized Prompts)
- **AssetGenAgent**: Spritesheet generation via SDXL-MCP
- **CodeRefactorAgent**: ECS optimization with FPS profiling  
- **QAAgent**: pytest & mypy validation
- **LevelGenAgent**: Procedural arena generation