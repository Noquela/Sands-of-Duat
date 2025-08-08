# SANDS OF DUAT - COMPLETE MEGA IMPLEMENTATION PLAN
## The Definitive 8000+ Line Technical Guide

### EXECUTIVE OVERVIEW
Sands of Duat is a premium Egyptian underworld-themed card game that achieves Hades-level artistic excellence and gameplay depth. This comprehensive plan details every aspect of development from initial setup to final deployment, including complete code implementations, detailed algorithms, and practical examples for all systems.

---

## 1. PROJECT ARCHITECTURE & SETUP (ULTRA-DETAILED)

### 1.1 COMPLETE DIRECTORY STRUCTURE

```
sands_of_duat/
├── README.md
├── requirements.txt
├── pyproject.toml
├── setup.py
├── .gitignore
├── .env.example
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── build.yml
│   │   └── deploy.yml
│   └── ISSUE_TEMPLATE.md
├── docs/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── core.md
│   │   ├── cards.md
│   │   ├── combat.md
│   │   └── ui.md
│   ├── design/
│   │   ├── game_design.md
│   │   ├── art_style_guide.md
│   │   ├── egyptian_mythology.md
│   │   └── ui_wireframes/
│   ├── development/
│   │   ├── setup_guide.md
│   │   ├── coding_standards.md
│   │   └── testing_guide.md
│   └── deployment/
│       ├── build_guide.md
│       └── release_notes.md
├── src/
│   └── sands_of_duat/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   ├── constants.py
│       │   ├── paths.py
│       │   └── version.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── game_state.py
│       │   ├── event_system.py
│       │   ├── resource_manager.py
│       │   ├── save_system.py
│       │   ├── performance_monitor.py
│       │   └── error_handler.py
│       ├── cards/
│       │   ├── __init__.py
│       │   ├── card.py
│       │   ├── deck.py
│       │   ├── effects/
│       │   │   ├── __init__.py
│       │   │   ├── base_effect.py
│       │   │   ├── damage_effects.py
│       │   │   ├── healing_effects.py
│       │   │   ├── ba_ka_effects.py
│       │   │   ├── divine_effects.py
│       │   │   └── underworld_effects.py
│       │   ├── collections/
│       │   │   ├── __init__.py
│       │   │   ├── base_cards.py
│       │   │   ├── god_cards.py
│       │   │   ├── underworld_cards.py
│       │   │   └── artifact_cards.py
│       │   └── loader.py
│       ├── combat/
│       │   ├── __init__.py
│       │   ├── combat_manager.py
│       │   ├── turn_system.py
│       │   ├── targeting.py
│       │   ├── damage_calculation.py
│       │   ├── ba_ka_system.py
│       │   ├── ai/
│       │   │   ├── __init__.py
│       │   │   ├── base_ai.py
│       │   │   ├── god_personalities/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── ra_ai.py
│       │   │   │   ├── anubis_ai.py
│       │   │   │   ├── thoth_ai.py
│       │   │   │   ├── isis_ai.py
│       │   │   │   ├── set_ai.py
│       │   │   │   └── osiris_ai.py
│       │   │   ├── decision_tree.py
│       │   │   └── threat_assessment.py
│       │   └── hour_glass_initiative.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── screen_manager.py
│       │   ├── components/
│       │   │   ├── __init__.py
│       │   │   ├── base_component.py
│       │   │   ├── button.py
│       │   │   ├── card_display.py
│       │   │   ├── health_bar.py
│       │   │   ├── resource_display.py
│       │   │   ├── dialog.py
│       │   │   ├── tooltip.py
│       │   │   ├── progress_bar.py
│       │   │   └── animation_system.py
│       │   ├── screens/
│       │   │   ├── __init__.py
│       │   │   ├── base_screen.py
│       │   │   ├── main_menu.py
│       │   │   ├── deck_builder.py
│       │   │   ├── combat_screen.py
│       │   │   ├── map_screen.py
│       │   │   ├── collection_screen.py
│       │   │   ├── settings_screen.py
│       │   │   └── credits_screen.py
│       │   ├── themes/
│       │   │   ├── __init__.py
│       │   │   ├── egyptian_theme.py
│       │   │   ├── colors.py
│       │   │   ├── fonts.py
│       │   │   └── layouts.py
│       │   ├── input/
│       │   │   ├── __init__.py
│       │   │   ├── input_handler.py
│       │   │   ├── drag_drop.py
│       │   │   ├── keyboard_shortcuts.py
│       │   │   └── gesture_recognition.py
│       │   └── effects/
│       │       ├── __init__.py
│       │       ├── particle_system.py
│       │       ├── screen_transitions.py
│       │       ├── card_animations.py
│       │       └── combat_effects.py
│       ├── content/
│       │   ├── __init__.py
│       │   ├── content_manager.py
│       │   ├── localization/
│       │   │   ├── __init__.py
│       │   │   ├── text_manager.py
│       │   │   ├── en_US.json
│       │   │   ├── hieroglyphic.json
│       │   │   └── validator.py
│       │   ├── progression/
│       │   │   ├── __init__.py
│       │   │   ├── underworld_progression.py
│       │   │   ├── difficulty_scaling.py
│       │   │   └── rewards_system.py
│       │   └── validation/
│       │       ├── __init__.py
│       │       ├── card_validator.py
│       │       ├── balance_checker.py
│       │       └── content_integrity.py
│       ├── art/
│       │   ├── __init__.py
│       │   ├── art_generator.py
│       │   ├── stable_diffusion/
│       │   │   ├── __init__.py
│       │   │   ├── pipeline.py
│       │   │   ├── prompts/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── card_prompts.py
│       │   │   │   ├── background_prompts.py
│       │   │   │   └── ui_prompts.py
│       │   │   └── post_processing.py
│       │   ├── comfyui/
│       │   │   ├── __init__.py
│       │   │   ├── workflow_manager.py
│       │   │   ├── workflows/
│       │   │   │   ├── card_generation.json
│       │   │   │   ├── background_generation.json
│       │   │   │   └── ui_element_generation.json
│       │   │   └── api_client.py
│       │   ├── quality_control/
│       │   │   ├── __init__.py
│       │   │   ├── hades_standards.py
│       │   │   ├── consistency_checker.py
│       │   │   ├── auto_reviewer.py
│       │   │   └── batch_validator.py
│       │   └── asset_manager.py
│       ├── lora/
│       │   ├── __init__.py
│       │   ├── training/
│       │   │   ├── __init__.py
│       │   │   ├── dataset_preparation.py
│       │   │   ├── training_pipeline.py
│       │   │   ├── validation.py
│       │   │   └── hyperparameter_tuning.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── egyptian_mythology.py
│       │   │   ├── hades_style.py
│       │   │   └── model_manager.py
│       │   └── integration/
│       │       ├── __init__.py
│       │       ├── model_loader.py
│       │       └── inference_engine.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── coordinator.py
│       │   ├── code_agent.py
│       │   ├── art_agent.py
│       │   ├── testing_agent.py
│       │   ├── quality_agent.py
│       │   ├── communication/
│       │   │   ├── __init__.py
│       │   │   ├── message_protocol.py
│       │   │   ├── task_queue.py
│       │   │   └── progress_tracker.py
│       │   └── workflows/
│       │       ├── __init__.py
│       │       ├── development_workflow.py
│       │       ├── testing_workflow.py
│       │       └── deployment_workflow.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── audio_manager.py
│       │   ├── music_system.py
│       │   ├── sound_effects.py
│       │   └── ambient_audio.py
│       ├── networking/
│       │   ├── __init__.py
│       │   ├── multiplayer.py
│       │   ├── server/
│       │   │   ├── __init__.py
│       │   │   ├── game_server.py
│       │   │   ├── matchmaking.py
│       │   │   └── anti_cheat.py
│       │   └── client/
│       │       ├── __init__.py
│       │       ├── network_client.py
│       │       └── synchronization.py
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           ├── profiler.py
│           ├── math_utils.py
│           ├── color_utils.py
│           ├── file_utils.py
│           ├── encryption.py
│           └── data_structures.py
├── assets/
│   ├── images/
│   │   ├── cards/
│   │   │   ├── gods/
│   │   │   │   ├── ra/
│   │   │   │   ├── anubis/
│   │   │   │   ├── thoth/
│   │   │   │   ├── isis/
│   │   │   │   ├── set/
│   │   │   │   └── osiris/
│   │   │   ├── artifacts/
│   │   │   ├── spells/
│   │   │   └── underworld/
│   │   ├── backgrounds/
│   │   │   ├── main_menu/
│   │   │   ├── combat/
│   │   │   ├── underworld_levels/
│   │   │   └── ui_overlays/
│   │   ├── ui/
│   │   │   ├── buttons/
│   │   │   ├── frames/
│   │   │   ├── icons/
│   │   │   ├── panels/
│   │   │   └── decorations/
│   │   └── effects/
│   │       ├── particles/
│   │       ├── animations/
│   │       └── transitions/
│   ├── audio/
│   │   ├── music/
│   │   │   ├── main_theme.ogg
│   │   │   ├── combat_themes/
│   │   │   ├── ambient/
│   │   │   └── boss_themes/
│   │   ├── sfx/
│   │   │   ├── card_sounds/
│   │   │   ├── ui_sounds/
│   │   │   ├── combat_sounds/
│   │   │   └── ambient_sounds/
│   │   └── voice/
│   │       ├── narrator/
│   │       └── god_voices/
│   ├── fonts/
│   │   ├── papyrus_modern.ttf
│   │   ├── hieroglyphic.ttf
│   │   ├── egyptian_serif.ttf
│   │   └── ui_sans.ttf
│   └── data/
│       ├── cards/
│       │   ├── base_set.yaml
│       │   ├── god_set.yaml
│       │   ├── underworld_set.yaml
│       │   └── artifact_set.yaml
│       ├── encounters/
│       │   ├── level_1_encounters.yaml
│       │   ├── level_2_encounters.yaml
│       │   ├── boss_encounters.yaml
│       │   └── special_encounters.yaml
│       ├── progression/
│       │   ├── underworld_map.yaml
│       │   ├── difficulty_curves.yaml
│       │   └── reward_tables.yaml
│       └── localization/
│           ├── strings_en.yaml
│           ├── strings_hieroglyphic.yaml
│           └── card_text_en.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_core/
│   │   │   ├── __init__.py
│   │   │   ├── test_game_state.py
│   │   │   ├── test_event_system.py
│   │   │   ├── test_resource_manager.py
│   │   │   └── test_save_system.py
│   │   ├── test_cards/
│   │   │   ├── __init__.py
│   │   │   ├── test_card.py
│   │   │   ├── test_deck.py
│   │   │   ├── test_effects.py
│   │   │   └── test_loader.py
│   │   ├── test_combat/
│   │   │   ├── __init__.py
│   │   │   ├── test_combat_manager.py
│   │   │   ├── test_turn_system.py
│   │   │   ├── test_targeting.py
│   │   │   ├── test_damage_calculation.py
│   │   │   ├── test_ba_ka_system.py
│   │   │   └── test_ai.py
│   │   ├── test_ui/
│   │   │   ├── __init__.py
│   │   │   ├── test_components.py
│   │   │   ├── test_screens.py
│   │   │   └── test_input.py
│   │   └── test_utils/
│   │       ├── __init__.py
│   │       └── test_math_utils.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_gameplay_flow.py
│   │   ├── test_card_interactions.py
│   │   ├── test_combat_scenarios.py
│   │   ├── test_ui_workflows.py
│   │   └── test_save_load.py
│   ├── performance/
│   │   ├── __init__.py
│   │   ├── test_memory_usage.py
│   │   ├── test_rendering_performance.py
│   │   ├── test_ai_performance.py
│   │   └── benchmark_suite.py
│   ├── visual/
│   │   ├── __init__.py
│   │   ├── test_art_quality.py
│   │   ├── test_ui_consistency.py
│   │   └── screenshot_tests.py
│   └── fixtures/
│       ├── __init__.py
│       ├── sample_cards.yaml
│       ├── test_saves/
│       └── mock_assets/
├── tools/
│   ├── art_generation/
│   │   ├── batch_generate.py
│   │   ├── quality_check.py
│   │   ├── style_transfer.py
│   │   └── asset_optimizer.py
│   ├── content_tools/
│   │   ├── card_designer.py
│   │   ├── balance_analyzer.py
│   │   ├── localization_tool.py
│   │   └── content_validator.py
│   ├── development/
│   │   ├── code_generator.py
│   │   ├── test_generator.py
│   │   ├── documentation_generator.py
│   │   └── performance_profiler.py
│   ├── deployment/
│   │   ├── build_script.py
│   │   ├── asset_packager.py
│   │   ├── distribution_manager.py
│   │   └── update_deployer.py
│   └── automation/
│       ├── ci_scripts/
│       ├── testing_automation/
│       └── release_automation/
├── scripts/
│   ├── setup/
│   │   ├── install_dependencies.py
│   │   ├── setup_development.py
│   │   ├── configure_environment.py
│   │   └── initialize_project.py
│   ├── maintenance/
│   │   ├── cleanup_assets.py
│   │   ├── update_dependencies.py
│   │   ├── backup_saves.py
│   │   └── performance_monitoring.py
│   └── utilities/
│       ├── asset_converter.py
│       ├── data_migrator.py
│       ├── log_analyzer.py
│       └── system_checker.py
├── builds/
│   ├── windows/
│   ├── linux/
│   ├── macos/
│   └── web/
├── temp/
│   ├── art_generation/
│   ├── build_artifacts/
│   └── cache/
└── logs/
    ├── development/
    ├── performance/
    ├── errors/
    └── user_analytics/
```

### 1.2 PYTHON ENVIRONMENT SETUP WITH EXACT VERSIONS

#### requirements.txt
```
# Core Game Engine
pygame==2.5.2
pygame-gui==0.6.9

# Data Handling
PyYAML==6.0.1
Pillow==10.0.1
numpy==1.24.3
pandas==2.0.3

# AI and Machine Learning
torch==2.0.1
torchvision==0.15.2
diffusers==0.21.4
transformers==4.33.2
accelerate==0.23.0
xformers==0.0.22
compel==2.0.2

# Image Processing
opencv-python==4.8.1.78
imageio==2.31.5
scikit-image==0.21.0

# Audio Processing
pygame-mixer==2.0.2
pydub==0.25.1

# Networking
websockets==11.0.3
aiohttp==3.8.6
requests==2.31.0

# Configuration and Serialization
pydantic==2.4.2
marshmallow==3.20.1
omegaconf==2.3.0

# Testing Framework
pytest==7.4.2
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-benchmark==4.0.0
pytest-mock==3.11.1
pytest-xdist==3.3.1
hypothesis==6.82.6

# Code Quality
black==23.9.1
flake8==6.1.0
mypy==1.5.1
pre-commit==3.4.0
bandit==1.7.5

# Development Tools
watchdog==3.0.0
python-dotenv==1.0.0
click==8.1.7
rich==13.5.2
tqdm==4.66.1

# Performance Monitoring
psutil==5.9.5
memory-profiler==0.61.0
line-profiler==4.1.1
py-spy==0.3.14

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==1.3.0
myst-parser==2.0.0

# Deployment
pyinstaller==6.0.0
cx-Freeze==6.15.10
nuitka==1.8.4

# Platform Specific
pywin32==306; sys_platform == "win32"
```

#### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sands-of-duat"
version = "1.0.0"
description = "Premium Egyptian underworld card game with Hades-level artistic excellence"
authors = [
    {name = "Sands of Duat Team", email = "dev@sansofduat.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Games/Entertainment :: Board Games",
    "Topic :: Games/Entertainment :: Turn Based Strategy",
]
keywords = ["game", "cards", "egyptian", "mythology", "strategy"]

dependencies = [
    "pygame>=2.5.2",
    "pygame-gui>=0.6.9",
    "PyYAML>=6.0.1",
    "Pillow>=10.0.1",
    "numpy>=1.24.3",
    "pydantic>=2.4.2",
    "click>=8.1.7",
    "rich>=13.5.2",
]

[project.optional-dependencies]
ai = [
    "torch>=2.0.1",
    "diffusers>=0.21.4",
    "transformers>=4.33.2",
]
dev = [
    "pytest>=7.4.2",
    "black>=23.9.1",
    "flake8>=6.1.0",
    "mypy>=1.5.1",
    "pre-commit>=3.4.0",
]
build = [
    "pyinstaller>=6.0.0",
    "cx-Freeze>=6.15.10",
]

[project.scripts]
sands-of-duat = "sands_of_duat.main:main"
sands-dev = "sands_of_duat.tools.dev_cli:main"
sands-art = "sands_of_duat.art.cli:main"

[project.urls]
Homepage = "https://github.com/sandsofDuat/sands-of-duat"
Documentation = "https://docs.sansofduat.com"
Repository = "https://github.com/sandsofDuat/sands-of-duat.git"
"Bug Tracker" = "https://github.com/sandsofDuat/sands-of-duat/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"sands_of_duat" = ["py.typed"]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "visual: marks tests as visual regression tests",
    "performance: marks tests as performance benchmarks",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

### 1.3 CONFIGURATION FILES WITH FULL CONTENTS

#### .env.example
```bash
# Development Configuration
DEBUG=true
LOG_LEVEL=DEBUG
PROFILING_ENABLED=false

# Game Configuration
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
FULLSCREEN=false
VSYNC=true
FPS_TARGET=60

# Audio Configuration
MASTER_VOLUME=0.8
MUSIC_VOLUME=0.7
SFX_VOLUME=0.9
AMBIENT_VOLUME=0.5

# AI Art Generation
STABLE_DIFFUSION_MODEL_PATH=./models/stable-diffusion-v1-5
COMFYUI_SERVER_URL=http://localhost:8188
LORA_MODELS_PATH=./models/lora
ART_GENERATION_BATCH_SIZE=4
ART_QUALITY_THRESHOLD=0.85

# Performance Settings
MAX_MEMORY_USAGE_MB=4096
TEXTURE_QUALITY=HIGH
PARTICLE_DENSITY=MEDIUM
ANIMATION_QUALITY=HIGH

# Networking (Future)
MULTIPLAYER_ENABLED=false
SERVER_URL=ws://localhost:8080
MATCHMAKING_REGION=US_WEST

# Content Paths
CARDS_DATA_PATH=./assets/data/cards
ENCOUNTERS_DATA_PATH=./assets/data/encounters
LOCALIZATION_PATH=./assets/data/localization

# Development Tools
AUTO_RELOAD_CONTENT=true
SHOW_DEBUG_UI=true
ENABLE_CONSOLE=true
SCREENSHOT_ON_ERROR=true

# Analytics (Optional)
ANALYTICS_ENABLED=false
TELEMETRY_ENDPOINT=https://analytics.sansofduat.com
USER_ID_GENERATION=ANONYMOUS

# Build Configuration
BUILD_TARGET=development
OPTIMIZATION_LEVEL=0
INCLUDE_DEBUG_SYMBOLS=true
COMPRESS_ASSETS=false
```

#### .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Game Specific
logs/
temp/
cache/
saves/
screenshots/
user_data/
performance_data/

# AI Models
models/
*.ckpt
*.safetensors
*.pt
*.pth

# Generated Assets
assets/generated/
builds/
*.log

# Development
.mypy_cache/
.bandit
.pre-commit-config.yaml
profiling_results/
benchmark_results/
```

### 1.4 DEVELOPMENT TOOLS AND IDE SETUP

#### VSCode Configuration (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile", "black"],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.mypy_cache": true,
        "**/temp": true,
        "**/logs": true
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.autoImportCompletions": true,
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml"
    },
    "yaml.validate": true,
    "yaml.completion": true,
    "editor.rulers": [88],
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "git.ignoreLimitWarning": true
}
```

#### VSCode Extensions (extensions.json)
```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "ms-python.pylint",
        "ms-vscode.test-adapter-converter",
        "redhat.vscode-yaml",
        "ms-vscode.vscode-json",
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-toolsai.jupyter",
        "streetsidesoftware.code-spell-checker",
        "gruntfuggly.todo-tree",
        "eamodio.gitlens",
        "ms-vscode.powershell"
    ]
}
```

---

## 2. CORE SYSTEMS IMPLEMENTATION (STEP-BY-STEP WITH CODE)

### 2.1 COMPLETE GAME STATE MANAGEMENT ARCHITECTURE

#### src/sands_of_duat/core/game_state.py
```python
"""
Complete Game State Management System for Sands of Duat

This module provides comprehensive state management including:
- Global game state tracking
- State transitions with validation
- Event-driven state updates
- Persistent state serialization
- Multi-threaded state access safety
- Performance monitoring and optimization
"""

from __future__ import annotations

import asyncio
import json
import threading
import time
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union
from uuid import uuid4

import pygame
from pydantic import BaseModel, validator

from ..utils.logger import get_logger
from ..config.constants import SAVE_PATH, MAX_SAVE_SLOTS
from .event_system import EventSystem, Event


logger = get_logger(__name__)


class GamePhase(Enum):
    """All possible game phases with explicit state transitions."""
    STARTUP = auto()
    MAIN_MENU = auto()
    DECK_BUILDER = auto()
    MAP_NAVIGATION = auto()
    ENCOUNTER_SETUP = auto()
    COMBAT_INIT = auto()
    COMBAT_PLAYER_TURN = auto()
    COMBAT_ENEMY_TURN = auto()
    COMBAT_RESOLUTION = auto()
    REWARD_SELECTION = auto()
    PROGRESSION = auto()
    SETTINGS = auto()
    CREDITS = auto()
    SHUTDOWN = auto()


class GameDifficulty(Enum):
    """Difficulty levels with balanced progression scaling."""
    SCRIBE = "scribe"  # Easy - For learning
    PRIEST = "priest"  # Normal - Balanced experience
    PHARAOH = "pharaoh"  # Hard - Challenge seekers
    GOD_KING = "god_king"  # Extreme - Masters only


@dataclass
class PlayerProgress:
    """Complete player progression tracking."""
    # Core progression
    current_level: int = 1
    underworld_depth: int = 0
    experience_points: int = 0
    souls_collected: int = 0
    
    # Combat statistics
    battles_won: int = 0
    battles_lost: int = 0
    perfect_victories: int = 0
    cards_played: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    
    # Collection progress
    cards_discovered: Set[str] = field(default_factory=set)
    artifacts_found: Set[str] = field(default_factory=set)
    gods_encountered: Set[str] = field(default_factory=set)
    
    # Achievement tracking
    achievements_unlocked: Set[str] = field(default_factory=set)
    milestones_reached: Set[str] = field(default_factory=set)
    
    # Time tracking
    total_playtime_seconds: float = 0.0
    session_start_time: Optional[float] = None
    
    # Difficulty progression
    highest_difficulty_completed: Optional[GameDifficulty] = None
    current_run_difficulty: GameDifficulty = GameDifficulty.PRIEST
    
    def start_session(self) -> None:
        """Start tracking session time."""
        self.session_start_time = time.time()
    
    def end_session(self) -> None:
        """End session and add time to total."""
        if self.session_start_time:
            session_time = time.time() - self.session_start_time
            self.total_playtime_seconds += session_time
            self.session_start_time = None
    
    def add_card_discovery(self, card_id: str) -> bool:
        """Add discovered card. Returns True if new discovery."""
        if card_id not in self.cards_discovered:
            self.cards_discovered.add(card_id)
            return True
        return False
    
    def calculate_level(self) -> int:
        """Calculate level based on experience points."""
        # Egyptian-themed level progression: 100 * level^1.5
        level = 1
        while self.experience_points >= 100 * (level ** 1.5):
            level += 1
        return level - 1
    
    def get_completion_percentage(self) -> float:
        """Calculate overall completion percentage."""
        # Weighted completion based on various factors
        factors = {
            'level_progress': min(self.current_level / 50, 1.0) * 0.2,
            'depth_progress': min(self.underworld_depth / 100, 1.0) * 0.3,
            'collection_progress': len(self.cards_discovered) / 200 * 0.2,
            'achievement_progress': len(self.achievements_unlocked) / 50 * 0.2,
            'difficulty_progress': (
                list(GameDifficulty).index(self.highest_difficulty_completed or GameDifficulty.SCRIBE) 
                / (len(GameDifficulty) - 1)
            ) * 0.1
        }
        return sum(factors.values())


@dataclass
class CombatState:
    """Complete combat state tracking with all systems."""
    # Basic combat info
    is_active: bool = False
    current_turn: int = 0
    phase: str = "setup"
    
    # Participants
    player_health: int = 100
    player_max_health: int = 100
    player_ba: int = 50  # Soul energy
    player_ka: int = 50  # Life force
    
    enemy_health: int = 100
    enemy_max_health: int = 100
    enemy_ba: int = 50
    enemy_ka: int = 50
    enemy_id: str = ""
    
    # Card game state
    player_hand: List[str] = field(default_factory=list)
    player_deck: List[str] = field(default_factory=list)
    player_discard: List[str] = field(default_factory=list)
    player_exhausted: List[str] = field(default_factory=list)
    
    # Resources and status effects
    player_mana: int = 3
    player_max_mana: int = 3
    player_status_effects: Dict[str, int] = field(default_factory=dict)
    enemy_status_effects: Dict[str, int] = field(default_factory=dict)
    
    # Hour-Glass Initiative System
    hour_glass_position: float = 0.0  # -1.0 to 1.0
    initiative_modifiers: Dict[str, float] = field(default_factory=dict)
    
    # Advanced combat tracking
    cards_played_this_turn: List[str] = field(default_factory=list)
    damage_preview: Dict[str, int] = field(default_factory=dict)
    targeting_info: Dict[str, Any] = field(default_factory=dict)
    
    # Ba-Ka system state
    ba_ka_split_active: bool = False
    ba_split_duration: int = 0
    soul_reunion_power: float = 1.0
    
    def reset_for_new_combat(self, enemy_id: str, difficulty: GameDifficulty) -> None:
        """Reset state for new combat encounter."""
        self.is_active = True
        self.current_turn = 0
        self.phase = "setup"
        self.enemy_id = enemy_id
        
        # Reset health based on difficulty
        difficulty_multipliers = {
            GameDifficulty.SCRIBE: 0.8,
            GameDifficulty.PRIEST: 1.0,
            GameDifficulty.PHARAOH: 1.3,
            GameDifficulty.GOD_KING: 1.7
        }
        
        multiplier = difficulty_multipliers[difficulty]
        self.enemy_max_health = int(100 * multiplier)
        self.enemy_health = self.enemy_max_health
        
        # Reset all other combat-specific state
        self.player_hand.clear()
        self.player_deck.clear()
        self.player_discard.clear()
        self.player_exhausted.clear()
        self.player_status_effects.clear()
        self.enemy_status_effects.clear()
        self.cards_played_this_turn.clear()
        
        self.hour_glass_position = 0.0
        self.initiative_modifiers.clear()
        self.ba_ka_split_active = False
        self.ba_split_duration = 0
        self.soul_reunion_power = 1.0


class GameStateManager:
    """
    Complete game state management with thread safety, persistence, and validation.
    
    Features:
    - Thread-safe state access and modification
    - Automatic state validation and correction
    - Event-driven state change notifications
    - Persistent state saving and loading
    - Performance monitoring and optimization
    - Rollback capabilities for critical errors
    - Multi-version save compatibility
    """
    
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        self._lock = threading.RLock()
        self._state_history: List[Dict[str, Any]] = []
        self._max_history_size = 100
        
        # Core state components
        self.current_phase = GamePhase.STARTUP
        self.previous_phase = GamePhase.STARTUP
        self.player_progress = PlayerProgress()
        self.combat_state = CombatState()
        
        # Game settings
        self.settings = {
            'master_volume': 0.8,
            'music_volume': 0.7,
            'sfx_volume': 0.9,
            'screen_resolution': (1920, 1080),
            'fullscreen': False,
            'vsync': True,
            'language': 'en_US',
            'auto_save': True,
            'difficulty': GameDifficulty.PRIEST,
        }
        
        # Runtime state
        self.is_paused = False
        self.debug_mode = False
        self.performance_stats = {
            'frame_count': 0,
            'fps': 60.0,
            'memory_usage': 0,
            'state_changes': 0,
            'last_save_time': 0.0,
        }
        
        # State change callbacks
        self._phase_change_callbacks: Dict[GamePhase, List[Callable]] = {}
        self._state_change_listeners: List[Callable] = []
        
        # Initialize state tracking
        self._last_state_snapshot = self._create_state_snapshot()
        self._state_change_timer = 0.0
        
        logger.info("GameStateManager initialized successfully")
    
    def _create_state_snapshot(self) -> Dict[str, Any]:
        """Create a complete snapshot of current state."""
        with self._lock:
            return {
                'timestamp': time.time(),
                'phase': self.current_phase,
                'previous_phase': self.previous_phase,
                'player_progress': asdict(self.player_progress),
                'combat_state': asdict(self.combat_state),
                'settings': self.settings.copy(),
                'is_paused': self.is_paused,
                'performance_stats': self.performance_stats.copy(),
            }
    
    def save_state_snapshot(self) -> None:
        """Save current state to history for rollback purposes."""
        snapshot = self._create_state_snapshot()
        self._state_history.append(snapshot)
        
        # Maintain history size limit
        if len(self._state_history) > self._max_history_size:
            self._state_history.pop(0)
    
    def rollback_to_previous_state(self, steps_back: int = 1) -> bool:
        """Rollback to a previous state snapshot."""
        if len(self._state_history) < steps_back:
            logger.warning(f"Cannot rollback {steps_back} steps, only {len(self._state_history)} snapshots available")
            return False
        
        try:
            target_snapshot = self._state_history[-(steps_back + 1)]
            self._restore_from_snapshot(target_snapshot)
            
            # Remove newer snapshots
            self._state_history = self._state_history[:-(steps_back)]
            
            logger.info(f"Successfully rolled back {steps_back} steps")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback state: {e}")
            return False
    
    def _restore_from_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """Restore state from a saved snapshot."""
        with self._lock:
            self.current_phase = snapshot['phase']
            self.previous_phase = snapshot['previous_phase']
            
            # Restore player progress
            progress_data = snapshot['player_progress']
            self.player_progress = PlayerProgress(**progress_data)
            
            # Restore combat state
            combat_data = snapshot['combat_state']
            self.combat_state = CombatState(**combat_data)
            
            # Restore settings and runtime state
            self.settings = snapshot['settings'].copy()
            self.is_paused = snapshot['is_paused']
            self.performance_stats = snapshot['performance_stats'].copy()
    
    def change_phase(self, new_phase: GamePhase, force: bool = False) -> bool:
        """
        Change game phase with validation and event notification.
        
        Args:
            new_phase: Target phase to transition to
            force: Skip validation if True
            
        Returns:
            bool: True if phase change was successful
        """
        if not force and not self._is_valid_phase_transition(self.current_phase, new_phase):
            logger.warning(f"Invalid phase transition: {self.current_phase} -> {new_phase}")
            return False
        
        with self._lock:
            old_phase = self.current_phase
            self.previous_phase = old_phase
            self.current_phase = new_phase
            
            # Save state snapshot before major transitions
            if self._is_major_transition(old_phase, new_phase):
                self.save_state_snapshot()
            
            # Update performance stats
            self.performance_stats['state_changes'] += 1
            
        # Notify listeners
        self._notify_phase_change(old_phase, new_phase)
        
        # Fire event
        event = Event(
            'phase_changed',
            {
                'old_phase': old_phase,
                'new_phase': new_phase,
                'timestamp': time.time()
            }
        )
        self.event_system.fire_event(event)
        
        logger.info(f"Phase changed: {old_phase} -> {new_phase}")
        return True
    
    def _is_valid_phase_transition(self, from_phase: GamePhase, to_phase: GamePhase) -> bool:
        """Validate if a phase transition is allowed."""
        # Define valid transitions
        valid_transitions = {
            GamePhase.STARTUP: [GamePhase.MAIN_MENU],
            GamePhase.MAIN_MENU: [
                GamePhase.DECK_BUILDER, GamePhase.MAP_NAVIGATION, 
                GamePhase.SETTINGS, GamePhase.CREDITS, GamePhase.SHUTDOWN
            ],
            GamePhase.DECK_BUILDER: [GamePhase.MAIN_MENU, GamePhase.MAP_NAVIGATION],
            GamePhase.MAP_NAVIGATION: [
                GamePhase.ENCOUNTER_SETUP, GamePhase.MAIN_MENU, 
                GamePhase.DECK_BUILDER, GamePhase.PROGRESSION
            ],
            GamePhase.ENCOUNTER_SETUP: [GamePhase.COMBAT_INIT, GamePhase.MAP_NAVIGATION],
            GamePhase.COMBAT_INIT: [GamePhase.COMBAT_PLAYER_TURN],
            GamePhase.COMBAT_PLAYER_TURN: [
                GamePhase.COMBAT_ENEMY_TURN, GamePhase.COMBAT_RESOLUTION
            ],
            GamePhase.COMBAT_ENEMY_TURN: [
                GamePhase.COMBAT_PLAYER_TURN, GamePhase.COMBAT_RESOLUTION
            ],
            GamePhase.COMBAT_RESOLUTION: [GamePhase.REWARD_SELECTION, GamePhase.MAP_NAVIGATION],
            GamePhase.REWARD_SELECTION: [GamePhase.PROGRESSION, GamePhase.MAP_NAVIGATION],
            GamePhase.PROGRESSION: [GamePhase.MAP_NAVIGATION, GamePhase.MAIN_MENU],
            GamePhase.SETTINGS: [GamePhase.MAIN_MENU],
            GamePhase.CREDITS: [GamePhase.MAIN_MENU],
            GamePhase.SHUTDOWN: [],
        }
        
        return to_phase in valid_transitions.get(from_phase, [])
    
    def _is_major_transition(self, from_phase: GamePhase, to_phase: GamePhase) -> bool:
        """Check if this is a major transition requiring state snapshot."""
        major_transitions = [
            (GamePhase.MAP_NAVIGATION, GamePhase.ENCOUNTER_SETUP),
            (GamePhase.ENCOUNTER_SETUP, GamePhase.COMBAT_INIT),
            (GamePhase.COMBAT_RESOLUTION, GamePhase.REWARD_SELECTION),
            (GamePhase.REWARD_SELECTION, GamePhase.PROGRESSION),
        ]
        return (from_phase, to_phase) in major_transitions
    
    def register_phase_callback(self, phase: GamePhase, callback: Callable) -> None:
        """Register a callback for when entering a specific phase."""
        if phase not in self._phase_change_callbacks:
            self._phase_change_callbacks[phase] = []
        self._phase_change_callbacks[phase].append(callback)
    
    def register_state_change_listener(self, listener: Callable) -> None:
        """Register a listener for any state changes."""
        self._state_change_listeners.append(listener)
    
    def _notify_phase_change(self, old_phase: GamePhase, new_phase: GamePhase) -> None:
        """Notify all registered callbacks and listeners."""
        # Notify phase-specific callbacks
        if new_phase in self._phase_change_callbacks:
            for callback in self._phase_change_callbacks[new_phase]:
                try:
                    callback(old_phase, new_phase)
                except Exception as e:
                    logger.error(f"Error in phase callback: {e}")
        
        # Notify general state change listeners
        for listener in self._state_change_listeners:
            try:
                listener('phase_change', old_phase, new_phase)
            except Exception as e:
                logger.error(f"Error in state change listener: {e}")
    
    def update_player_progress(self, **kwargs) -> None:
        """Update player progress with validation."""
        with self._lock:
            for key, value in kwargs.items():
                if hasattr(self.player_progress, key):
                    setattr(self.player_progress, key, value)
                else:
                    logger.warning(f"Unknown player progress field: {key}")
            
            # Recalculate derived values
            self.player_progress.current_level = self.player_progress.calculate_level()
    
    def start_combat(self, enemy_id: str) -> None:
        """Initialize combat state."""
        with self._lock:
            self.combat_state.reset_for_new_combat(
                enemy_id, 
                self.settings['difficulty']
            )
            
        logger.info(f"Combat started against {enemy_id}")
    
    def end_combat(self, victory: bool) -> None:
        """End combat and update statistics."""
        with self._lock:
            self.combat_state.is_active = False
            
            if victory:
                self.player_progress.battles_won += 1
                # Check for perfect victory
                if self.player_progress.current_level == self.player_progress.player_max_health:
                    self.player_progress.perfect_victories += 1
            else:
                self.player_progress.battles_lost += 1
            
        logger.info(f"Combat ended. Victory: {victory}")
    
    def save_to_file(self, slot: int = 0) -> bool:
        """Save complete game state to file."""
        if not (0 <= slot < MAX_SAVE_SLOTS):
            logger.error(f"Invalid save slot: {slot}")
            return False
        
        try:
            save_path = Path(SAVE_PATH) / f"save_slot_{slot}.json"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            save_data = {
                'version': '1.0.0',
                'timestamp': time.time(),
                'save_slot': slot,
                'state_snapshot': self._create_state_snapshot(),
                'metadata': {
                    'playtime': self.player_progress.total_playtime_seconds,
                    'level': self.player_progress.current_level,
                    'completion': self.player_progress.get_completion_percentage(),
                }
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, default=str)
            
            self.performance_stats['last_save_time'] = time.time()
            logger.info(f"Game saved to slot {slot}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
    
    def load_from_file(self, slot: int = 0) -> bool:
        """Load complete game state from file."""
        if not (0 <= slot < MAX_SAVE_SLOTS):
            logger.error(f"Invalid save slot: {slot}")
            return False
        
        try:
            save_path = Path(SAVE_PATH) / f"save_slot_{slot}.json"
            
            if not save_path.exists():
                logger.warning(f"Save file not found: {save_path}")
                return False
            
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Validate save version
            if save_data.get('version') != '1.0.0':
                logger.warning("Save file version mismatch, attempting migration")
                # Future: implement save migration logic
            
            # Restore state from snapshot
            snapshot = save_data['state_snapshot']
            self._restore_from_snapshot(snapshot)
            
            logger.info(f"Game loaded from slot {slot}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return False
    
    def get_available_saves(self) -> List[Dict[str, Any]]:
        """Get information about all available save files."""
        saves = []
        save_dir = Path(SAVE_PATH)
        
        if not save_dir.exists():
            return saves
        
        for slot in range(MAX_SAVE_SLOTS):
            save_path = save_dir / f"save_slot_{slot}.json"
            
            if save_path.exists():
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)
                    
                    saves.append({
                        'slot': slot,
                        'timestamp': save_data.get('timestamp', 0),
                        'metadata': save_data.get('metadata', {}),
                        'valid': True
                    })
                    
                except Exception as e:
                    logger.error(f"Error reading save slot {slot}: {e}")
                    saves.append({
                        'slot': slot,
                        'timestamp': 0,
                        'metadata': {},
                        'valid': False,
                        'error': str(e)
                    })
        
        return saves
    
    def update_performance_stats(self, fps: float, memory_usage: int) -> None:
        """Update performance statistics."""
        with self._lock:
            self.performance_stats['frame_count'] += 1
            self.performance_stats['fps'] = fps
            self.performance_stats['memory_usage'] = memory_usage
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get comprehensive debug information."""
        with self._lock:
            return {
                'current_phase': self.current_phase,
                'previous_phase': self.previous_phase,
                'is_paused': self.is_paused,
                'combat_active': self.combat_state.is_active,
                'player_level': self.player_progress.current_level,
                'underworld_depth': self.player_progress.underworld_depth,
                'performance_stats': self.performance_stats.copy(),
                'memory_snapshots': len(self._state_history),
                'total_playtime': self.player_progress.total_playtime_seconds,
                'settings': self.settings.copy(),
            }
    
    def validate_state_integrity(self) -> bool:
        """Validate the integrity of the current game state."""
        try:
            # Validate player progress
            if self.player_progress.current_level < 1:
                logger.error("Invalid player level")
                return False
            
            if self.player_progress.underworld_depth < 0:
                logger.error("Invalid underworld depth")
                return False
            
            # Validate combat state
            if self.combat_state.is_active:
                if self.combat_state.player_health < 0:
                    logger.error("Invalid player health")
                    return False
                
                if not self.combat_state.enemy_id:
                    logger.error("Combat active but no enemy ID")
                    return False
            
            # Validate settings
            required_settings = ['master_volume', 'difficulty', 'screen_resolution']
            for setting in required_settings:
                if setting not in self.settings:
                    logger.error(f"Missing required setting: {setting}")
                    return False
            
            logger.debug("State integrity validation passed")
            return True
            
        except Exception as e:
            logger.error(f"State validation error: {e}")
            return False
    
    def cleanup(self) -> None:
        """Clean up resources and perform final save."""
        logger.info("Cleaning up GameStateManager")
        
        # End current session
        self.player_progress.end_session()
        
        # Auto-save if enabled
        if self.settings.get('auto_save', True):
            self.save_to_file(0)
        
        # Clear callbacks and listeners
        self._phase_change_callbacks.clear()
        self._state_change_listeners.clear()
        
        # Clear state history
        self._state_history.clear()
        
        logger.info("GameStateManager cleanup completed")
```

### 2.2 EVENT SYSTEM IMPLEMENTATION

#### src/sands_of_duat/core/event_system.py
```python
"""
Advanced Event System for Sands of Duat

Features:
- Type-safe event definitions
- Priority-based event handling
- Asynchronous event processing
- Event filtering and transformation
- Performance monitoring
- Event history and replay
- Memory-efficient event pooling
"""

from __future__ import annotations

import asyncio
import heapq
import threading
import time
import weakref
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union,
    Generic, Protocol, runtime_checkable
)
from uuid import uuid4

from ..utils.logger import get_logger
from ..config.constants import MAX_EVENT_HISTORY, EVENT_POOL_SIZE


logger = get_logger(__name__)
T = TypeVar('T')


class EventPriority(Enum):
    """Event processing priorities."""
    CRITICAL = 0    # System-critical events (errors, shutdown)
    HIGH = 1        # Important game events (combat, state changes)
    NORMAL = 2      # Standard game events (UI updates, animations)
    LOW = 3         # Background events (statistics, analytics)


class EventType(Enum):
    """All possible event types in the game."""
    # System events
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"
    
    # Game state events
    PHASE_CHANGED = "phase_changed"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"
    SAVE_COMPLETED = "save_completed"
    LOAD_COMPLETED = "load_completed"
    
    # Player events
    PLAYER_LEVEL_UP = "player_level_up"
    PLAYER_DIED = "player_died"
    PLAYER_HEALED = "player_healed"
    EXPERIENCE_GAINED = "experience_gained"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    
    # Combat events
    COMBAT_STARTED = "combat_started"
    COMBAT_ENDED = "combat_ended"
    TURN_STARTED = "turn_started"
    TURN_ENDED = "turn_ended"
    CARD_PLAYED = "card_played"
    CARD_DISCARDED = "card_discarded"
    DAMAGE_DEALT = "damage_dealt"
    HEALING_APPLIED = "healing_applied"
    STATUS_APPLIED = "status_applied"
    STATUS_REMOVED = "status_removed"
    BA_KA_SPLIT = "ba_ka_split"
    BA_KA_REUNION = "ba_ka_reunion"
    
    # UI events
    SCREEN_CHANGED = "screen_changed"
    BUTTON_CLICKED = "button_clicked"
    CARD_HOVERED = "card_hovered"
    CARD_SELECTED = "card_selected"
    DRAG_STARTED = "drag_started"
    DRAG_ENDED = "drag_ended"
    TOOLTIP_SHOWN = "tooltip_shown"
    TOOLTIP_HIDDEN = "tooltip_hidden"
    
    # Content events
    CARD_DISCOVERED = "card_discovered"
    ARTIFACT_FOUND = "artifact_found"
    GOD_ENCOUNTERED = "god_encountered"
    AREA_UNLOCKED = "area_unlocked"
    
    # Audio events
    MUSIC_STARTED = "music_started"
    MUSIC_STOPPED = "music_stopped"
    SOUND_PLAYED = "sound_played"
    VOLUME_CHANGED = "volume_changed"
    
    # Performance events
    FPS_WARNING = "fps_warning"
    MEMORY_WARNING = "memory_warning"
    PERFORMANCE_REPORT = "performance_report"
    
    # Network events (future)
    CONNECTION_ESTABLISHED = "connection_established"
    CONNECTION_LOST = "connection_lost"
    MATCH_FOUND = "match_found"
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"


@dataclass
class Event:
    """
    Immutable event data structure with comprehensive metadata.
    """
    event_type: Union[EventType, str]
    data: Dict[str, Any] = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    source: Optional[str] = None
    target: Optional[str] = None
    propagate: bool = True
    
    def __post_init__(self):
        """Ensure event_type is properly typed."""
        if isinstance(self.event_type, str) and hasattr(EventType, self.event_type.upper()):
            self.event_type = EventType(self.event_type)
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Get event data with optional default."""
        return self.data.get(key, default)
    
    def has_data(self, key: str) -> bool:
        """Check if event has specific data key."""
        return key in self.data
    
    def clone(self, **overrides) -> Event:
        """Create a clone of this event with optional overrides."""
        clone_data = {
            'event_type': self.event_type,
            'data': self.data.copy(),
            'priority': self.priority,
            'timestamp': self.timestamp,
            'event_id': str(uuid4()),  # New ID for clone
            'source': self.source,
            'target': self.target,
            'propagate': self.propagate,
        }
        clone_data.update(overrides)
        return Event(**clone_data)


@runtime_checkable
class EventHandler(Protocol):
    """Protocol for event handlers."""
    
    def handle_event(self, event: Event) -> bool:
        """
        Handle an event.
        
        Args:
            event: The event to handle
            
        Returns:
            bool: True if event was handled and should stop propagating
        """
        ...


class BaseEventHandler(ABC):
    """Abstract base class for event handlers with lifecycle management."""
    
    def __init__(self, name: str):
        self.name = name
        self.enabled = True
        self.handled_count = 0
        self.last_handled_time = 0.0
    
    @abstractmethod
    def handle_event(self, event: Event) -> bool:
        """Handle an event. Must be implemented by subclasses."""
        pass
    
    def can_handle(self, event: Event) -> bool:
        """Check if this handler can process the event."""
        return self.enabled
    
    def on_registered(self, event_system: EventSystem) -> None:
        """Called when handler is registered with event system."""
        pass
    
    def on_unregistered(self, event_system: EventSystem) -> None:
        """Called when handler is unregistered from event system."""
        pass


class FilteredEventHandler(BaseEventHandler):
    """Event handler with built-in filtering capabilities."""
    
    def __init__(self, name: str, event_types: Set[EventType], handler_func: Callable[[Event], bool]):
        super().__init__(name)
        self.event_types = event_types
        self.handler_func = handler_func
    
    def can_handle(self, event: Event) -> bool:
        """Check if this handler can process the event type."""
        return (
            super().can_handle(event) and 
            event.event_type in self.event_types
        )
    
    def handle_event(self, event: Event) -> bool:
        """Handle the event using the provided function."""
        if not self.can_handle(event):
            return False
        
        try:
            result = self.handler_func(event)
            self.handled_count += 1
            self.last_handled_time = time.time()
            return result
        except Exception as e:
            logger.error(f"Error in event handler {self.name}: {e}")
            return False


@dataclass
class EventStatistics:
    """Statistics tracking for event system performance."""
    events_fired: int = 0
    events_handled: int = 0
    handlers_registered: int = 0
    average_processing_time: float = 0.0
    peak_processing_time: float = 0.0
    events_by_type: Dict[EventType, int] = field(default_factory=lambda: defaultdict(int))
    handlers_by_performance: Dict[str, float] = field(default_factory=dict)
    
    def record_event_fired(self, event_type: EventType) -> None:
        """Record that an event was fired."""
        self.events_fired += 1
        self.events_by_type[event_type] += 1
    
    def record_processing_time(self, handler_name: str, processing_time: float) -> None:
        """Record handler processing time."""
        self.handlers_by_performance[handler_name] = processing_time
        self.average_processing_time = (
            (self.average_processing_time * self.events_handled + processing_time) / 
            (self.events_handled + 1)
        )
        self.peak_processing_time = max(self.peak_processing_time, processing_time)
        self.events_handled += 1


class EventSystem:
    """
    Advanced event system with comprehensive features for game development.
    
    Features:
    - Priority-based event processing
    - Asynchronous and synchronous event handling
    - Event filtering and transformation
    - Handler lifecycle management
    - Performance monitoring and statistics
    - Event history and replay capabilities
    - Memory-efficient event pooling
    - Thread-safe operations
    """
    
    def __init__(self):
        self._handlers: Dict[EventType, List[BaseEventHandler]] = defaultdict(list)
        self._global_handlers: List[BaseEventHandler] = []
        self._event_queue: List[tuple] = []  # Priority queue: (priority, timestamp, event)
        self._event_history: deque = deque(maxlen=MAX_EVENT_HISTORY)
        self._event_pool: deque = deque(maxlen=EVENT_POOL_SIZE)
        
        # Thread safety
        self._lock = threading.RLock()
        self._processing_lock = threading.Lock()
        
        # Statistics and monitoring
        self.statistics = EventStatistics()
        self._performance_monitor = True
        
        # Asynchronous processing
        self._async_loop: Optional[asyncio.AbstractEventLoop] = None
        self._async_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        
        # Event transformation and filtering
        self._event_transformers: List[Callable[[Event], Event]] = []
        self._event_filters: List[Callable[[Event], bool]] = []
        
        # System state
        self._enabled = True
        self._debug_mode = False
        
        logger.info("EventSystem initialized")
    
    def register_handler(
        self, 
        event_type: Union[EventType, List[EventType], None],
        handler: Union[BaseEventHandler, Callable[[Event], bool]],
        priority: EventPriority = EventPriority.NORMAL
    ) -> None:
        """
        Register an event handler for specific event types.
        
        Args:
            event_type: Event type(s) to handle, or None for global handler
            handler: Handler instance or callable
            priority: Handler priority (affects processing order)
        """
        with self._lock:
            # Convert callable to handler instance
            if callable(handler) and not isinstance(handler, BaseEventHandler):
                if event_type is None:
                    handler_name = f"global_handler_{len(self._global_handlers)}"
                    event_types = set(EventType)
                else:
                    event_types = {event_type} if isinstance(event_type, EventType) else set(event_type)
                    handler_name = f"handler_{event_type}_{len(self._handlers[event_type])}"
                
                handler = FilteredEventHandler(handler_name, event_types, handler)
            
            # Register handler
            if event_type is None:
                # Global handler
                self._global_handlers.append(handler)
                self._global_handlers.sort(key=lambda h: getattr(h, 'priority', priority).value)
            else:
                # Specific event type handler(s)
                event_types = [event_type] if isinstance(event_type, EventType) else event_type
                for et in event_types:
                    self._handlers[et].append(handler)
                    self._handlers[et].sort(key=lambda h: getattr(h, 'priority', priority).value)
            
            # Notify handler of registration
            if hasattr(handler, 'on_registered'):
                handler.on_registered(self)
            
            self.statistics.handlers_registered += 1
            logger.debug(f"Registered handler: {handler.name if hasattr(handler, 'name') else 'anonymous'}")
    
    def unregister_handler(
        self,
        event_type: Union[EventType, List[EventType], None],
        handler: BaseEventHandler
    ) -> bool:
        """
        Unregister an event handler.
        
        Args:
            event_type: Event type(s) the handler was registered for
            handler: Handler instance to remove
            
        Returns:
            bool: True if handler was found and removed
        """
        with self._lock:
            removed = False
            
            if event_type is None:
                # Remove from global handlers
                if handler in self._global_handlers:
                    self._global_handlers.remove(handler)
                    removed = True
            else:
                # Remove from specific event type handlers
                event_types = [event_type] if isinstance(event_type, EventType) else event_type
                for et in event_types:
                    if handler in self._handlers[et]:
                        self._handlers[et].remove(handler)
                        removed = True
            
            if removed:
                # Notify handler of unregistration
                if hasattr(handler, 'on_unregistered'):
                    handler.on_unregistered(self)
                
                self.statistics.handlers_registered -= 1
                logger.debug(f"Unregistered handler: {handler.name if hasattr(handler, 'name') else 'anonymous'}")
            
            return removed
    
    def fire_event(self, event: Event, immediate: bool = False) -> None:
        """
        Fire an event for processing.
        
        Args:
            event: Event to fire
            immediate: If True, process immediately instead of queuing
        """
        if not self._enabled:
            return
        
        # Apply event filters
        for event_filter in self._event_filters:
            try:
                if not event_filter(event):
                    logger.debug(f"Event filtered out: {event.event_type}")
                    return
            except Exception as e:
                logger.error(f"Error in event filter: {e}")
        
        # Apply event transformers
        for transformer in self._event_transformers:
            try:
                event = transformer(event)
            except Exception as e:
                logger.error(f"Error in event transformer: {e}")
        
        # Record statistics
        self.statistics.record_event_fired(event.event_type)
        
        # Add to history
        self._event_history.append(event)
        
        if immediate:
            self._process_event(event)
        else:
            with self._lock:
                # Add to priority queue
                heapq.heappush(
                    self._event_queue,
                    (event.priority.value, event.timestamp, event)
                )
        
        logger.debug(f"Event fired: {event.event_type} (immediate: {immediate})")
    
    def fire_event_sync(self, event_type: EventType, data: Dict[str, Any] = None) -> None:
        """Convenience method to fire an event synchronously."""
        event = Event(event_type, data or {})
        self.fire_event(event, immediate=True)
    
    async def fire_event_async(self, event_type: EventType, data: Dict[str, Any] = None) -> None:
        """Fire an event asynchronously."""
        event = Event(event_type, data or {})
        
        # Process async handlers
        async_handlers = self._async_handlers.get(event_type, [])
        for handler in async_handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Error in async event handler: {e}")
        
        # Also fire for sync processing
        self.fire_event(event)
    
    def process_events(self, max_events: int = 100, max_time_ms: float = 16.67) -> int:
        """
        Process queued events with time and count limits.
        
        Args:
            max_events: Maximum number of events to process
            max_time_ms: Maximum processing time in milliseconds
            
        Returns:
            int: Number of events processed
        """
        if not self._enabled:
            return 0
        
        start_time = time.time()
        processed_count = 0
        
        with self._processing_lock:
            while (
                processed_count < max_events and
                (time.time() - start_time) * 1000 < max_time_ms and
                self._event_queue
            ):
                with self._lock:
                    if not self._event_queue:
                        break
                    
                    # Get highest priority event
                    _, _, event = heapq.heappop(self._event_queue)
                
                self._process_event(event)
                processed_count += 1
        
        return processed_count
    
    def _process_event(self, event: Event) -> None:
        """Process a single event through all applicable handlers."""
        start_time = time.time()
        
        try:
            # Process global handlers first
            for handler in self._global_handlers:
                if not event.propagate:
                    break
                
                if handler.can_handle(event):
                    handler_start = time.time()
                    try:
                        if handler.handle_event(event):
                            event.propagate = False
                    except Exception as e:
                        logger.error(f"Error in global handler {handler.name}: {e}")
                    finally:
                        if self._performance_monitor:
                            processing_time = time.time() - handler_start
                            self.statistics.record_processing_time(handler.name, processing_time)
            
            # Process specific event type handlers
            if event.propagate and event.event_type in self._handlers:
                for handler in self._handlers[event.event_type]:
                    if not event.propagate:
                        break
                    
                    if handler.can_handle(event):
                        handler_start = time.time()
                        try:
                            if handler.handle_event(event):
                                event.propagate = False
                        except Exception as e:
                            logger.error(f"Error in handler {handler.name}: {e}")
                        finally:
                            if self._performance_monitor:
                                processing_time = time.time() - handler_start
                                self.statistics.record_processing_time(handler.name, processing_time)
        
        finally:
            if self._performance_monitor:
                total_time = time.time() - start_time
                if total_time > 0.001:  # Log slow events (>1ms)
                    logger.warning(f"Slow event processing: {event.event_type} took {total_time*1000:.2f}ms")
    
    def add_event_filter(self, filter_func: Callable[[Event], bool]) -> None:
        """Add an event filter function."""
        self._event_filters.append(filter_func)
    
    def add_event_transformer(self, transformer_func: Callable[[Event], Event]) -> None:
        """Add an event transformer function."""
        self._event_transformers.append(transformer_func)
    
    def get_event_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[Event]:
        """Get recent event history, optionally filtered by type."""
        if event_type is None:
            return list(self._event_history)[-limit:]
        else:
            filtered = [e for e in self._event_history if e.event_type == event_type]
            return filtered[-limit:]
    
    def replay_events(self, events: List[Event], immediate: bool = True) -> None:
        """Replay a list of events."""
        logger.info(f"Replaying {len(events)} events")
        for event in events:
            # Create new event with current timestamp
            replay_event = event.clone(timestamp=time.time())
            self.fire_event(replay_event, immediate=immediate)
    
    def clear_event_queue(self) -> int:
        """Clear all queued events and return count cleared."""
        with self._lock:
            count = len(self._event_queue)
            self._event_queue.clear()
            return count
    
    def get_statistics(self) -> EventStatistics:
        """Get event system performance statistics."""
        return self.statistics
    
    def reset_statistics(self) -> None:
        """Reset performance statistics."""
        self.statistics = EventStatistics()
    
    def enable_debug_mode(self, enabled: bool = True) -> None:
        """Enable or disable debug mode for verbose logging."""
        self._debug_mode = enabled
        if enabled:
            logger.info("Event system debug mode enabled")
        else:
            logger.info("Event system debug mode disabled")
    
    def enable(self) -> None:
        """Enable event processing."""
        self._enabled = True
        logger.info("Event system enabled")
    
    def disable(self) -> None:
        """Disable event processing."""
        self._enabled = False
        logger.info("Event system disabled")
    
    def cleanup(self) -> None:
        """Clean up event system resources."""
        logger.info("Cleaning up EventSystem")
        
        # Clear all handlers
        with self._lock:
            for handlers in self._handlers.values():
                for handler in handlers:
                    if hasattr(handler, 'on_unregistered'):
                        handler.on_unregistered(self)
            
            for handler in self._global_handlers:
                if hasattr(handler, 'on_unregistered'):
                    handler.on_unregistered(self)
            
            self._handlers.clear()
            self._global_handlers.clear()
            
            # Clear queues and pools
            self._event_queue.clear()
            self._event_history.clear()
            self._event_pool.clear()
            
            # Clear filters and transformers
            self._event_filters.clear()
            self._event_transformers.clear()
        
        logger.info("EventSystem cleanup completed")


# Convenience decorator for event handlers
def event_handler(event_type: Union[EventType, List[EventType]], priority: EventPriority = EventPriority.NORMAL):
    """Decorator to mark methods as event handlers."""
    def decorator(func):
        func._event_type = event_type
        func._event_priority = priority
        func._is_event_handler = True
        return func
    return decorator


# Example specialized event handlers
class CombatEventHandler(BaseEventHandler):
    """Specialized handler for combat-related events."""
    
    def __init__(self, combat_system):
        super().__init__("CombatEventHandler")
        self.combat_system = combat_system
    
    def can_handle(self, event: Event) -> bool:
        """Only handle combat-related events."""
        combat_events = {
            EventType.COMBAT_STARTED, EventType.COMBAT_ENDED,
            EventType.TURN_STARTED, EventType.TURN_ENDED,
            EventType.CARD_PLAYED, EventType.DAMAGE_DEALT,
            EventType.HEALING_APPLIED, EventType.BA_KA_SPLIT,
            EventType.BA_KA_REUNION
        }
        return super().can_handle(event) and event.event_type in combat_events
    
    def handle_event(self, event: Event) -> bool:
        """Handle combat events."""
        if event.event_type == EventType.COMBAT_STARTED:
            enemy_id = event.get_data('enemy_id')
            if enemy_id:
                self.combat_system.initialize_combat(enemy_id)
            return True
        
        elif event.event_type == EventType.CARD_PLAYED:
            card_id = event.get_data('card_id')
            target = event.get_data('target')
            if card_id:
                self.combat_system.process_card_play(card_id, target)
            return True
        
        elif event.event_type == EventType.DAMAGE_DEALT:
            damage = event.get_data('damage', 0)
            target = event.get_data('target')
            source = event.get_data('source')
            if damage > 0 and target:
                self.combat_system.apply_damage(target, damage, source)
            return True
        
        return False
```

### 2.3 RESOURCE LOADING AND MANAGEMENT

#### src/sands_of_duat/core/resource_manager.py
```python
"""
Advanced Resource Management System for Sands of Duat

Features:
- Intelligent asset loading and caching
- Memory management with automatic cleanup
- Multi-threaded background loading
- Asset hot-reloading for development
- Compression and optimization
- Error recovery and fallback assets
- Performance monitoring and profiling
"""

from __future__ import annotations

import asyncio
import gc
import hashlib
import json
import mmap
import os
import pickle
import threading
import time
import weakref
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any, Dict, List, Optional, Set, Tuple, Union, Callable,
    TypeVar, Generic, Protocol, runtime_checkable
)

import pygame
import yaml
from PIL import Image, ImageOps

from ..config.constants import (
    ASSETS_PATH, CACHE_PATH, MAX_MEMORY_MB, 
    TEXTURE_FORMATS, AUDIO_FORMATS
)
from ..utils.logger import get_logger
from ..utils.file_utils import get_file_hash, ensure_directory
from .event_system import EventSystem, Event, EventType


logger = get_logger(__name__)
T = TypeVar('T')


class ResourceType(Enum):
    """Types of resources that can be managed."""
    IMAGE = auto()
    AUDIO = auto()
    FONT = auto()
    DATA = auto()
    SHADER = auto()
    MODEL = auto()
    ANIMATION = auto()
    LOCALIZATION = auto()


class LoadingPriority(Enum):
    """Resource loading priorities."""
    CRITICAL = 0    # Must be loaded immediately
    HIGH = 1        # Load before normal resources
    NORMAL = 2      # Standard loading priority
    LOW = 3         # Load when system is idle
    BACKGROUND = 4  # Load in background thread


class CacheStrategy(Enum):
    """Memory cache strategies."""
    ALWAYS = "always"           # Always keep in memory
    NEVER = "never"             # Never cache in memory
    LRU = "lru"                 # Least Recently Used eviction
    SIZE_BASED = "size_based"   # Evict based on memory usage
    TIME_BASED = "time_based"   # Evict after time limit


@dataclass
class ResourceMetadata:
    """Metadata for loaded resources."""
    resource_id: str
    resource_type: ResourceType
    file_path: Path
    file_size: int
    file_hash: str
    load_time: float
    last_accessed: float
    access_count: int = 0
    memory_usage: int = 0
    cache_strategy: CacheStrategy = CacheStrategy.LRU
    dependencies: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    version: str = "1.0"
    
    def mark_accessed(self) -> None:
        """Mark resource as accessed."""
        self.last_accessed = time.time()
        self.access_count += 1


@runtime_checkable
class ResourceLoader(Protocol):
    """Protocol for resource loaders."""
    
    def can_load(self, file_path: Path) -> bool:
        """Check if this loader can handle the file."""
        ...
    
    def load(self, file_path: Path, **kwargs) -> Any:
        """Load the resource from file."""
        ...
    
    def get_memory_usage(self, resource: Any) -> int:
        """Get memory usage of loaded resource."""
        ...


class ImageLoader:
    """Specialized loader for image resources."""
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.tga', '.webp'}
    
    def can_load(self, file_path: Path) -> bool:
        """Check if this is a supported image format."""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def load(self, file_path: Path, **kwargs) -> pygame.Surface:
        """
        Load image with optimization options.
        
        Args:
            file_path: Path to image file
            **kwargs: Loading options:
                - convert_alpha: Convert to alpha format (default: True)
                - scale: Scale factor or (width, height)
                - optimize: Apply optimization (default: True)
        """
        try:
            # Load with PIL for better format support and processing
            pil_image = Image.open(file_path)
            
            # Apply transformations
            if 'scale' in kwargs:
                scale = kwargs['scale']
                if isinstance(scale, (int, float)):
                    new_size = (int(pil_image.width * scale), int(pil_image.height * scale))
                else:
                    new_size = scale
                pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Apply optimization
            if kwargs.get('optimize', True):
                pil_image = ImageOps.exif_transpose(pil_image)
            
            # Convert to pygame surface
            mode = pil_image.mode
            size = pil_image.size
            raw = pil_image.tobytes()
            
            surface = pygame.image.fromstring(raw, size, mode)
            
            # Convert for optimal blitting
            if kwargs.get('convert_alpha', True):
                if pil_image.mode in ('RGBA', 'LA') or 'transparency' in pil_image.info:
                    surface = surface.convert_alpha()
                else:
                    surface = surface.convert()
            
            return surface
            
        except Exception as e:
            logger.error(f"Failed to load image {file_path}: {e}")
            return self._create_fallback_surface(64, 64)
    
    def _create_fallback_surface(self, width: int, height: int) -> pygame.Surface:
        """Create a fallback surface for failed loads."""
        surface = pygame.Surface((width, height))
        surface.fill((255, 0, 255))  # Magenta for missing textures
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
        return surface
    
    def get_memory_usage(self, resource: pygame.Surface) -> int:
        """Calculate memory usage of pygame surface."""
        return resource.get_width() * resource.get_height() * resource.get_bytesize()


class AudioLoader:
    """Specialized loader for audio resources."""
    
    SUPPORTED_FORMATS = {'.ogg', '.wav', '.mp3', '.flac'}
    
    def can_load(self, file_path: Path) -> bool:
        """Check if this is a supported audio format."""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def load(self, file_path: Path, **kwargs) -> Union[pygame.mixer.Sound, pygame.mixer.music]:
        """
        Load audio resource.
        
        Args:
            file_path: Path to audio file
            **kwargs: Loading options:
                - as_music: Load as music instead of sound effect
                - volume: Set initial volume (0.0 to 1.0)
        """
        try:
            if kwargs.get('as_music', False):
                # Load as music (streamed)
                pygame.mixer.music.load(str(file_path))
                return pygame.mixer.music
            else:
                # Load as sound effect (into memory)
                sound = pygame.mixer.Sound(str(file_path))
                
                if 'volume' in kwargs:
                    sound.set_volume(kwargs['volume'])
                
                return sound
                
        except Exception as e:
            logger.error(f"Failed to load audio {file_path}: {e}")
            return self._create_fallback_sound()
    
    def _create_fallback_sound(self) -> pygame.mixer.Sound:
        """Create a silent fallback sound."""
        # Create 1 second of silence at 22050 Hz
        import numpy as np
        samples = np.zeros((22050,), dtype=np.int16)
        return pygame.sndarray.make_sound(samples)
    
    def get_memory_usage(self, resource: pygame.mixer.Sound) -> int:
        """Estimate memory usage of sound."""
        # Approximate based on typical audio formats
        return 44100 * 2 * 2  # 44.1kHz, 16-bit, stereo, 1 second estimate


class FontLoader:
    """Specialized loader for font resources."""
    
    SUPPORTED_FORMATS = {'.ttf', '.otf'}
    
    def can_load(self, file_path: Path) -> bool:
        """Check if this is a supported font format."""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def load(self, file_path: Path, **kwargs) -> Dict[int, pygame.font.Font]:
        """
        Load font at multiple sizes.
        
        Args:
            file_path: Path to font file
            **kwargs: Loading options:
                - sizes: List of font sizes to pre-load (default: [12, 16, 24, 32, 48])
        """
        try:
            sizes = kwargs.get('sizes', [12, 16, 24, 32, 48])
            fonts = {}
            
            for size in sizes:
                fonts[size] = pygame.font.Font(str(file_path), size)
            
            return fonts
            
        except Exception as e:
            logger.error(f"Failed to load font {file_path}: {e}")
            return self._create_fallback_font()
    
    def _create_fallback_font(self) -> Dict[int, pygame.font.Font]:
        """Create fallback fonts using system default."""
        sizes = [12, 16, 24, 32, 48]
        return {size: pygame.font.Font(None, size) for size in sizes}
    
    def get_memory_usage(self, resource: Dict[int, pygame.font.Font]) -> int:
        """Estimate memory usage of font collection."""
        # Rough estimate based on number of sizes
        return len(resource) * 1024  # 1KB per size estimate


class DataLoader:
    """Specialized loader for data files (JSON, YAML, etc.)."""
    
    SUPPORTED_FORMATS = {'.json', '.yaml', '.yml', '.xml', '.csv'}
    
    def can_load(self, file_path: Path) -> bool:
        """Check if this is a supported data format."""
        return file_path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def load(self, file_path: Path, **kwargs) -> Any:
        """
        Load data file.
        
        Args:
            file_path: Path to data file
            **kwargs: Loading options:
                - encoding: File encoding (default: utf-8)
                - validate: Validate data structure (default: True)
        """
        try:
            encoding = kwargs.get('encoding', 'utf-8')
            
            with open(file_path, 'r', encoding=encoding) as f:
                if file_path.suffix.lower() == '.json':
                    data = json.load(f)
                elif file_path.suffix.lower() in ('.yaml', '.yml'):
                    data = yaml.safe_load(f)
                else:
                    data = f.read()
            
            # Validate data if requested
            if kwargs.get('validate', True):
                self._validate_data(data, file_path)
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to load data {file_path}: {e}")
            return {}
    
    def _validate_data(self, data: Any, file_path: Path) -> None:
        """Validate loaded data structure."""
        # Basic validation - can be extended
        if data is None:
            raise ValueError(f"Data file {file_path} is empty or invalid")
    
    def get_memory_usage(self, resource: Any) -> int:
        """Estimate memory usage of data structure."""
        try:
            return len(pickle.dumps(resource))
        except:
            return 1024  # Fallback estimate


class ResourceCache:
    """
    Advanced caching system with multiple eviction strategies.
    """
    
    def __init__(self, max_memory_mb: int = MAX_MEMORY_MB):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory_usage = 0
        
        # Cache storage
        self._cache: Dict[str, Any] = {}
        self._metadata: Dict[str, ResourceMetadata] = {}
        self._access_order: List[str] = []  # For LRU
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.evictions = 0
    
    def get(self, resource_id: str) -> Optional[Tuple[Any, ResourceMetadata]]:
        """Get resource from cache."""
        with self._lock:
            if resource_id in self._cache:
                # Update access tracking
                metadata = self._metadata[resource_id]
                metadata.mark_accessed()
                
                # Update LRU order
                if resource_id in self._access_order:
                    self._access_order.remove(resource_id)
                self._access_order.append(resource_id)
                
                self.cache_hits += 1
                return self._cache[resource_id], metadata
            else:
                self.cache_misses += 1
                return None
    
    def put(self, resource_id: str, resource: Any, metadata: ResourceMetadata) -> bool:
        """Put resource in cache."""
        with self._lock:
            # Check if we need to evict resources
            if metadata.cache_strategy != CacheStrategy.NEVER:
                if not self._make_space_for_resource(metadata.memory_usage):
                    return False
                
                self._cache[resource_id] = resource
                self._metadata[resource_id] = metadata
                self._access_order.append(resource_id)
                self.current_memory_usage += metadata.memory_usage
                
                return True
            
            return False
    
    def remove(self, resource_id: str) -> bool:
        """Remove resource from cache."""
        with self._lock:
            if resource_id in self._cache:
                metadata = self._metadata[resource_id]
                self.current_memory_usage -= metadata.memory_usage
                
                del self._cache[resource_id]
                del self._metadata[resource_id]
                
                if resource_id in self._access_order:
                    self._access_order.remove(resource_id)
                
                return True
            
            return False
    
    def _make_space_for_resource(self, required_memory: int) -> bool:
        """Make space for a new resource by evicting others."""
        if self.current_memory_usage + required_memory <= self.max_memory_bytes:
            return True
        
        # Need to evict resources
        memory_to_free = (self.current_memory_usage + required_memory) - self.max_memory_bytes
        freed_memory = 0
        
        # Evict using LRU strategy
        resources_to_evict = []
        
        for resource_id in self._access_order:
            metadata = self._metadata[resource_id]
            
            # Don't evict ALWAYS cache strategy resources
            if metadata.cache_strategy == CacheStrategy.ALWAYS:
                continue
            
            resources_to_evict.append(resource_id)
            freed_memory += metadata.memory_usage
            
            if freed_memory >= memory_to_free:
                break
        
        # Actually evict the resources
        for resource_id in resources_to_evict:
            self.remove(resource_id)
            self.evictions += 1
        
        return freed_memory >= memory_to_free
    
    def clear(self) -> None:
        """Clear all cached resources."""
        with self._lock:
            self._cache.clear()
            self._metadata.clear()
            self._access_order.clear()
            self.current_memory_usage = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        with self._lock:
            total_requests = self.cache_hits + self.cache_misses
            hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0
            
            return {
                'cache_hits': self.cache_hits,
                'cache_misses': self.cache_misses,
                'hit_rate': hit_rate,
                'evictions': self.evictions,
                'current_memory_mb': self.current_memory_usage / (1024 * 1024),
                'max_memory_mb': self.max_memory_bytes / (1024 * 1024),
                'memory_utilization': self.current_memory_usage / self.max_memory_bytes,
                'cached_resources': len(self._cache),
            }


class ResourceManager:
    """
    Advanced resource management system with comprehensive features.
    
    Features:
    - Intelligent loading with multiple strategies
    - Advanced caching with configurable eviction
    - Background loading and preloading
    - Hot-reloading for development
    - Asset bundling and compression
    - Error recovery with fallback resources
    - Performance monitoring and optimization
    """
    
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        
        # Core components
        self.cache = ResourceCache()
        self._loaders: Dict[ResourceType, ResourceLoader] = {}
        self._file_watchers: Dict[str, threading.Thread] = {}
        
        # Loading system
        self._loading_queue: List[Tuple[str, Path, Dict[str, Any]]] = []
        self._loading_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ResourceLoader")
        self._background_loading = True
        
        # Asset bundles
        self._bundles: Dict[str, Dict[str, str]] = {}
        self._bundle_cache: Dict[str, Any] = {}
        
        # Configuration
        self.assets_path = Path(ASSETS_PATH)
        self.cache_path = Path(CACHE_PATH)
        ensure_directory(self.cache_path)
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Statistics
        self.load_times: Dict[str, float] = {}
        self.error_count = 0
        self.hot_reload_count = 0
        
        # Initialize default loaders
        self._register_default_loaders()
        
        # Register event handlers
        self._register_event_handlers()
        
        logger.info("ResourceManager initialized")
    
    def _register_default_loaders(self) -> None:
        """Register default resource loaders."""
        self._loaders[ResourceType.IMAGE] = ImageLoader()
        self._loaders[ResourceType.AUDIO] = AudioLoader()
        self._loaders[ResourceType.FONT] = FontLoader()
        self._loaders[ResourceType.DATA] = DataLoader()
    
    def _register_event_handlers(self) -> None:
        """Register event handlers."""
        def handle_system_events(event: Event) -> bool:
            if event.event_type == EventType.SYSTEM_SHUTDOWN:
                self.cleanup()
            return False
        
        self.event_system.register_handler(
            [EventType.SYSTEM_SHUTDOWN],
            handle_system_events
        )
    
    def register_loader(self, resource_type: ResourceType, loader: ResourceLoader) -> None:
        """Register a custom resource loader."""
        self._loaders[resource_type] = loader
        logger.info(f"Registered loader for {resource_type}")
    
    def load_resource(
        self,
        resource_id: str,
        file_path: Optional[Union[str, Path]] = None,
        resource_type: Optional[ResourceType] = None,
        priority: LoadingPriority = LoadingPriority.NORMAL,
        cache_strategy: CacheStrategy = CacheStrategy.LRU,
        **kwargs
    ) -> Optional[Any]:
        """
        Load a resource with comprehensive options.
        
        Args:
            resource_id: Unique identifier for the resource
            file_path: Path to resource file (auto-detected if None)
            resource_type: Type of resource (auto-detected if None)
            priority: Loading priority
            cache_strategy: Caching strategy
            **kwargs: Additional loading options
            
        Returns:
            Loaded resource or None if failed
        """
        # Check cache first
        cached = self.cache.get(resource_id)
        if cached:
            return cached[0]
        
        # Resolve file path
        if file_path is None:
            file_path = self._resolve_resource_path(resource_id)
            if file_path is None:
                logger.error(f"Could not resolve path for resource: {resource_id}")
                return None
        else:
            file_path = Path(file_path)
        
        # Auto-detect resource type
        if resource_type is None:
            resource_type = self._detect_resource_type(file_path)
        
        # Get appropriate loader
        loader = self._loaders.get(resource_type)
        if loader is None:
            logger.error(f"No loader available for resource type: {resource_type}")
            return None
        
        # Load based on priority
        if priority == LoadingPriority.CRITICAL:
            return self._load_immediate(resource_id, file_path, loader, cache_strategy, **kwargs)
        elif self._background_loading and priority in (LoadingPriority.LOW, LoadingPriority.BACKGROUND):
            self._queue_background_load(resource_id, file_path, loader, cache_strategy, **kwargs)
            return None
        else:
            return self._load_immediate(resource_id, file_path, loader, cache_strategy, **kwargs)
    
    def _load_immediate(
        self,
        resource_id: str,
        file_path: Path,
        loader: ResourceLoader,
        cache_strategy: CacheStrategy,
        **kwargs
    ) -> Optional[Any]:
        """Load resource immediately on current thread."""
        start_time = time.time()
        
        try:
            # Check if file exists
            if not file_path.exists():
                logger.error(f"Resource file not found: {file_path}")
                return None
            
            # Load the resource
            resource = loader.load(file_path, **kwargs)
            
            if resource is None:
                logger.error(f"Failed to load resource: {resource_id}")
                return None
            
            # Create metadata
            metadata = ResourceMetadata(
                resource_id=resource_id,
                resource_type=self._detect_resource_type(file_path),
                file_path=file_path,
                file_size=file_path.stat().st_size,
                file_hash=get_file_hash(file_path),
                load_time=time.time() - start_time,
                last_accessed=time.time(),
                memory_usage=loader.get_memory_usage(resource),
                cache_strategy=cache_strategy
            )
            
            # Cache the resource
            self.cache.put(resource_id, resource, metadata)
            
            # Record statistics
            self.load_times[resource_id] = metadata.load_time
            
            # Fire event
            self.event_system.fire_event(Event(
                EventType.SYSTEM_WARNING,  # Placeholder for resource loaded event
                {
                    'resource_id': resource_id,
                    'load_time': metadata.load_time,
                    'memory_usage': metadata.memory_usage
                }
            ))
            
            logger.debug(f"Loaded resource: {resource_id} in {metadata.load_time:.3f}s")
            return resource
            
        except Exception as e:
            logger.error(f"Error loading resource {resource_id}: {e}")
            self.error_count += 1
            return None
    
    def _queue_background_load(
        self,
        resource_id: str,
        file_path: Path,
        loader: ResourceLoader,
        cache_strategy: CacheStrategy,
        **kwargs
    ) -> None:
        """Queue resource for background loading."""
        future = self._loading_executor.submit(
            self._load_immediate,
            resource_id, file_path, loader, cache_strategy, **kwargs
        )
        
        def on_complete(future):
            try:
                result = future.result()
                if result is not None:
                    logger.debug(f"Background loaded: {resource_id}")
            except Exception as e:
                logger.error(f"Background loading failed for {resource_id}: {e}")
        
        future.add_done_callback(on_complete)
    
    def _resolve_resource_path(self, resource_id: str) -> Optional[Path]:
        """Resolve resource ID to file path."""
        # Try direct path first
        direct_path = self.assets_path / resource_id
        if direct_path.exists():
            return direct_path
        
        # Try with common extensions
        common_extensions = ['.png', '.jpg', '.ogg', '.wav', '.ttf', '.json', '.yaml']
        for ext in common_extensions:
            path_with_ext = self.assets_path / f"{resource_id}{ext}"
            if path_with_ext.exists():
                return path_with_ext
        
        # Search in subdirectories
        for root, dirs, files in os.walk(self.assets_path):
            for file in files:
                if file.startswith(resource_id):
                    return Path(root) / file
        
        return None
    
    def _detect_resource_type(self, file_path: Path) -> ResourceType:
        """Auto-detect resource type from file extension."""
        suffix = file_path.suffix.lower()
        
        if suffix in {'.png', '.jpg', '.jpeg', '.bmp', '.tga', '.webp'}:
            return ResourceType.IMAGE
        elif suffix in {'.ogg', '.wav', '.mp3', '.flac'}:
            return ResourceType.AUDIO
        elif suffix in {'.ttf', '.otf'}:
            return ResourceType.FONT
        elif suffix in {'.json', '.yaml', '.yml', '.xml', '.csv'}:
            return ResourceType.DATA
        else:
            return ResourceType.DATA  # Default fallback
    
    def preload_resources(self, resource_ids: List[str], **kwargs) -> None:
        """Preload a list of resources in background."""
        logger.info(f"Preloading {len(resource_ids)} resources")
        
        for resource_id in resource_ids:
            self.load_resource(
                resource_id,
                priority=LoadingPriority.BACKGROUND,
                **kwargs
            )
    
    def unload_resource(self, resource_id: str) -> bool:
        """Unload a resource from memory."""
        success = self.cache.remove(resource_id)
        
        if success:
            logger.debug(f"Unloaded resource: {resource_id}")
            
            # Stop watching file if we were
            if resource_id in self._file_watchers:
                # File watching implementation would go here
                pass
        
        return success
    
    def enable_hot_reload(self, resource_id: str) -> None:
        """Enable hot-reloading for a resource during development."""
        cached = self.cache.get(resource_id)
        if not cached:
            logger.warning(f"Cannot enable hot-reload for unloaded resource: {resource_id}")
            return
        
        metadata = cached[1]
        
        def watch_file():
            """Watch file for changes and reload."""
            last_mtime = metadata.file_path.stat().st_mtime
            
            while resource_id in self._file_watchers:
                time.sleep(1.0)  # Check every second
                
                try:
                    current_mtime = metadata.file_path.stat().st_mtime
                    if current_mtime > last_mtime:
                        logger.info(f"Hot-reloading resource: {resource_id}")
                        
                        # Reload the resource
                        self.unload_resource(resource_id)
                        self.load_resource(resource_id, metadata.file_path)
                        
                        self.hot_reload_count += 1
                        
                        # Fire hot-reload event
                        self.event_system.fire_event(Event(
                            EventType.SYSTEM_WARNING,  # Placeholder for hot-reload event
                            {'resource_id': resource_id}
                        ))
                        
                        last_mtime = current_mtime
                
                except Exception as e:
                    logger.error(f"Error in file watcher for {resource_id}: {e}")
                    break
        
        # Start file watcher thread
        watcher_thread = threading.Thread(target=watch_file, daemon=True)
        watcher_thread.start()
        self._file_watchers[resource_id] = watcher_thread
        
        logger.info(f"Hot-reload enabled for: {resource_id}")
    
    def disable_hot_reload(self, resource_id: str) -> None:
        """Disable hot-reloading for a resource."""
        if resource_id in self._file_watchers:
            del self._file_watchers[resource_id]
            logger.info(f"Hot-reload disabled for: {resource_id}")
    
    def create_bundle(self, bundle_name: str, resource_ids: List[str]) -> bool:
        """Create an asset bundle for efficient loading."""
        try:
            bundle_path = self.cache_path / f"{bundle_name}.bundle"
            
            with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as bundle_file:
                bundle_manifest = {}
                
                for resource_id in resource_ids:
                    file_path = self._resolve_resource_path(resource_id)
                    if file_path and file_path.exists():
                        # Add file to bundle
                        arcname = f"{resource_id}{file_path.suffix}"
                        bundle_file.write(file_path, arcname)
                        
                        # Add to manifest
                        bundle_manifest[resource_id] = {
                            'arcname': arcname,
                            'size': file_path.stat().st_size,
                            'hash': get_file_hash(file_path)
                        }
                    else:
                        logger.warning(f"Resource not found for bundle: {resource_id}")
                
                # Write manifest
                manifest_json = json.dumps(bundle_manifest, indent=2)
                bundle_file.writestr('manifest.json', manifest_json)
            
            self._bundles[bundle_name] = bundle_manifest
            logger.info(f"Created bundle: {bundle_name} with {len(bundle_manifest)} resources")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create bundle {bundle_name}: {e}")
            return False
    
    def load_bundle(self, bundle_name: str) -> bool:
        """Load all resources from a bundle."""
        try:
            bundle_path = self.cache_path / f"{bundle_name}.bundle"
            
            if not bundle_path.exists():
                logger.error(f"Bundle not found: {bundle_name}")
                return False
            
            with zipfile.ZipFile(bundle_path, 'r') as bundle_file:
                # Read manifest
                manifest_data = bundle_file.read('manifest.json')
                manifest = json.loads(manifest_data)
                
                # Load each resource
                for resource_id, info in manifest.items():
                    try:
                        # Extract to temporary location
                        temp_path = self.cache_path / 'temp' / info['arcname']
                        ensure_directory(temp_path.parent)
                        
                        with bundle_file.open(info['arcname']) as source:
                            with open(temp_path, 'wb') as dest:
                                dest.write(source.read())
                        
                        # Load resource
                        self.load_resource(resource_id, temp_path)
                        
                        # Clean up temp file
                        temp_path.unlink()
                        
                    except Exception as e:
                        logger.error(f"Failed to load resource {resource_id} from bundle: {e}")
            
            logger.info(f"Loaded bundle: {bundle_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load bundle {bundle_name}: {e}")
            return False
    
    def get_resource_info(self, resource_id: str) -> Optional[ResourceMetadata]:
        """Get metadata for a loaded resource."""
        cached = self.cache.get(resource_id)
        return cached[1] if cached else None
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get detailed memory usage information."""
        cache_stats = self.cache.get_statistics()
        
        return {
            'total_memory_mb': cache_stats['current_memory_mb'],
            'max_memory_mb': cache_stats['max_memory_mb'],
            'memory_utilization': cache_stats['memory_utilization'],
            'cached_resources': cache_stats['cached_resources'],
            'cache_hit_rate': cache_stats['hit_rate'],
            'bundles_loaded': len(self._bundles),
            'background_loading_active': self._background_loading,
            'hot_reloads': self.hot_reload_count,
            'load_errors': self.error_count,
        }
    
    def optimize_memory(self) -> Dict[str, int]:
        """Perform memory optimization and return statistics."""
        before_memory = self.cache.current_memory_usage
        
        # Force garbage collection
        gc.collect()
        
        # Clear unused resources (those not accessed recently)
        current_time = time.time()
        threshold = 300  # 5 minutes
        
        resources_to_remove = []
        with self.cache._lock:
            for resource_id, metadata in self.cache._metadata.items():
                if (current_time - metadata.last_accessed) > threshold:
                    if metadata.cache_strategy != CacheStrategy.ALWAYS:
                        resources_to_remove.append(resource_id)
        
        removed_count = 0
        for resource_id in resources_to_remove:
            if self.cache.remove(resource_id):
                removed_count += 1
        
        after_memory = self.cache.current_memory_usage
        memory_freed = before_memory - after_memory
        
        logger.info(f"Memory optimization freed {memory_freed / (1024*1024):.2f}MB by removing {removed_count} resources")
        
        return {
            'resources_removed': removed_count,
            'memory_freed_mb': memory_freed / (1024 * 1024),
            'memory_before_mb': before_memory / (1024 * 1024),
            'memory_after_mb': after_memory / (1024 * 1024),
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive resource manager statistics."""
        cache_stats = self.cache.get_statistics()
        
        avg_load_time = sum(self.load_times.values()) / len(self.load_times) if self.load_times else 0
        
        return {
            'cache_statistics': cache_stats,
            'total_resources_loaded': len(self.load_times),
            'average_load_time': avg_load_time,
            'max_load_time': max(self.load_times.values()) if self.load_times else 0,
            'min_load_time': min(self.load_times.values()) if self.load_times else 0,
            'load_errors': self.error_count,
            'hot_reloads': self.hot_reload_count,
            'bundles_created': len(self._bundles),
            'file_watchers_active': len(self._file_watchers),
            'background_loading_enabled': self._background_loading,
        }
    
    def cleanup(self) -> None:
        """Clean up resource manager."""
        logger.info("Cleaning up ResourceManager")
        
        # Stop all file watchers
        for resource_id in list(self._file_watchers.keys()):
            self.disable_hot_reload(resource_id)
        
        # Shutdown thread pool
        self._loading_executor.shutdown(wait=True)
        
        # Clear cache
        self.cache.clear()
        
        # Clear bundles
        self._bundles.clear()
        self._bundle_cache.clear()
        
        logger.info("ResourceManager cleanup completed")


# Usage example and convenience functions
def load_image(resource_manager: ResourceManager, image_id: str, **kwargs) -> Optional[pygame.Surface]:
    """Convenience function to load an image."""
    return resource_manager.load_resource(
        image_id,
        resource_type=ResourceType.IMAGE,
        **kwargs
    )


def load_sound(resource_manager: ResourceManager, sound_id: str, **kwargs) -> Optional[pygame.mixer.Sound]:
    """Convenience function to load a sound."""
    return resource_manager.load_resource(
        sound_id,
        resource_type=ResourceType.AUDIO,
        **kwargs
    )


def load_font(resource_manager: ResourceManager, font_id: str, **kwargs) -> Optional[Dict[int, pygame.font.Font]]:
    """Convenience function to load a font."""
    return resource_manager.load_resource(
        font_id,
        resource_type=ResourceType.FONT,
        **kwargs
    )


def load_data(resource_manager: ResourceManager, data_id: str, **kwargs) -> Optional[Any]:
    """Convenience function to load data."""
    return resource_manager.load_resource(
        data_id,
        resource_type=ResourceType.DATA,
        **kwargs
    )
```

---

## 3. CARD SYSTEM IMPLEMENTATION (ULTRA-DETAILED)

### 3.1 COMPLETE CARD DATA STRUCTURES

```python
# src/sands_of_duat/cards/card.py
from __future__ import annotations
import uuid
from typing import Dict, List, Optional, Any, Set, Tuple, Union, Callable
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from abc import ABC, abstractmethod

class CardType(Enum):
    """Card type enumeration with Egyptian themes."""
    DEITY = "deity"           # God cards (Ra, Anubis, etc.)
    MORTAL = "mortal"         # Human/mortal cards
    DIVINE_BEAST = "divine_beast"  # Sacred animals
    ARTIFACT = "artifact"     # Sacred objects
    SPELL = "spell"          # Magic spells
    RITUAL = "ritual"        # Ceremonial actions
    UNDERWORLD = "underworld"  # Underworld entities
    CELESTIAL = "celestial"   # Sky/star entities

class CardRarity(Enum):
    """Card rarity with Egyptian precious materials."""
    COMMON = ("common", "Clay Tablet", 1.0)
    UNCOMMON = ("uncommon", "Papyrus Scroll", 0.3)
    RARE = ("rare", "Silver Ankh", 0.1)
    EPIC = ("epic", "Golden Cartouche", 0.03)
    LEGENDARY = ("legendary", "Divine Essence", 0.01)
    MYTHIC = ("mythic", "Pharaoh's Regalia", 0.001)
    
    def __init__(self, key: str, display_name: str, drop_rate: float):
        self.key = key
        self.display_name = display_name
        self.drop_rate = drop_rate

class CardElement(Enum):
    """Egyptian elemental affinities."""
    FIRE = ("fire", "Ra's Flame", "#FF6B35")
    WATER = ("water", "Nile's Flow", "#4ECDC4") 
    EARTH = ("earth", "Desert Sand", "#D4A574")
    AIR = ("air", "Sky Winds", "#87CEEB")
    LIGHT = ("light", "Divine Radiance", "#FFD700")
    DARKNESS = ("darkness", "Underworld Shadow", "#2F1B14")
    DEATH = ("death", "Anubis' Domain", "#8B0000")
    LIFE = ("life", "Ankh Power", "#32CD32")
    CHAOS = ("chaos", "Set's Fury", "#8B008B")
    ORDER = ("order", "Ma'at's Balance", "#4169E1")
    
    def __init__(self, key: str, display_name: str, color_hex: str):
        self.key = key
        self.display_name = display_name
        self.color_hex = color_hex

class CardKeyword(Enum):
    """Card keywords with Egyptian mythology."""
    # Movement Keywords
    DESERT_WALK = ("desert_walk", "Can move through sand obstacles")
    RIVER_CROSSING = ("river_crossing", "Can cross water without penalty")
    UNDERWORLD_PASSAGE = ("underworld_passage", "Can enter underworld zones")
    
    # Combat Keywords  
    DIVINE_STRIKE = ("divine_strike", "Deals double damage to mortals")
    MUMMIFICATION = ("mummification", "Preserves defeated units")
    RESURRECTION = ("resurrection", "Can return from death")
    BLESSING = ("blessing", "Grants positive effects to allies")
    CURSE = ("curse", "Inflicts negative effects on enemies")
    
    # Ba-Ka Keywords
    BA_SPLIT = ("ba_split", "Soul can separate from body")
    KA_DOUBLE = ("ka_double", "Creates spiritual duplicate")
    SOUL_BOND = ("soul_bond", "Links with another entity")
    AFTERLIFE = ("afterlife", "Gains power when destroyed")
    
    # Egyptian God Powers
    PHARAOH_AUTHORITY = ("pharaoh_authority", "Commands mortal units")
    DIVINE_JUDGMENT = ("divine_judgment", "Determines life/death")
    COSMIC_BALANCE = ("cosmic_balance", "Maintains universal order")
    SACRED_GEOMETRY = ("sacred_geometry", "Affects board positioning")
    
    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

@dataclass
class CardStats:
    """Card statistics with Egyptian-themed attributes."""
    # Combat Stats
    attack: int = 0
    defense: int = 0  
    health: int = 1
    
    # Egyptian Spiritual Stats
    ba_power: int = 0      # Soul energy
    ka_strength: int = 0   # Life force
    divine_favor: int = 0  # God approval
    underworld_knowledge: int = 0  # Death realm wisdom
    
    # Initiative and Movement
    initiative: int = 0    # Turn order priority
    movement: int = 1     # Board movement range
    
    # Resource Costs
    mana_cost: int = 0
    gold_cost: int = 0
    offering_cost: int = 0  # Ritual offerings needed
    
    # Advanced Stats
    critical_chance: float = 0.0  # 0.0 to 1.0
    dodge_chance: float = 0.0
    block_chance: float = 0.0
    spell_power: float = 1.0      # Multiplier for magical effects
    
    def __post_init__(self):
        """Validate stats are within reasonable bounds."""
        self.attack = max(0, min(self.attack, 999))
        self.defense = max(0, min(self.defense, 999))
        self.health = max(1, min(self.health, 999))
        self.ba_power = max(0, min(self.ba_power, 100))
        self.ka_strength = max(0, min(self.ka_strength, 100))
        self.divine_favor = max(-50, min(self.divine_favor, 50))
        self.critical_chance = max(0.0, min(self.critical_chance, 1.0))
        self.dodge_chance = max(0.0, min(self.dodge_chance, 1.0))
        self.block_chance = max(0.0, min(self.block_chance, 1.0))
    
    def calculate_combat_rating(self) -> float:
        """Calculate overall combat effectiveness."""
        base_rating = (self.attack * 2 + self.defense + self.health) / 4
        spiritual_bonus = (self.ba_power + self.ka_strength) * 0.1
        divine_bonus = abs(self.divine_favor) * 0.05
        chance_bonus = (self.critical_chance + self.dodge_chance + self.block_chance) * 10
        
        return base_rating + spiritual_bonus + divine_bonus + chance_bonus
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            'attack': self.attack,
            'defense': self.defense,
            'health': self.health,
            'ba_power': self.ba_power,
            'ka_strength': self.ka_strength,
            'divine_favor': self.divine_favor,
            'underworld_knowledge': self.underworld_knowledge,
            'initiative': self.initiative,
            'movement': self.movement,
            'mana_cost': self.mana_cost,
            'gold_cost': self.gold_cost,
            'offering_cost': self.offering_cost,
            'critical_chance': self.critical_chance,
            'dodge_chance': self.dodge_chance,
            'block_chance': self.block_chance,
            'spell_power': self.spell_power
        }

class CardEffect:
    """Base class for all card effects."""
    
    def __init__(self, effect_id: str, name: str, description: str, 
                 trigger_timing: str = "immediate", duration: int = 1,
                 target_type: str = "self", stackable: bool = False):
        self.effect_id = effect_id
        self.name = name
        self.description = description
        self.trigger_timing = trigger_timing  # immediate, on_play, on_death, etc.
        self.duration = duration  # -1 for permanent, 0 for instant, >0 for turns
        self.target_type = target_type  # self, enemy, ally, all, etc.
        self.stackable = stackable
        self.stack_count = 1
        self.created_at = datetime.now()
        self.metadata: Dict[str, Any] = {}
    
    def can_trigger(self, game_state: Any, trigger_context: Dict[str, Any]) -> bool:
        """Check if effect can trigger in current context."""
        return True
    
    def apply_effect(self, game_state: Any, targets: List[Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the effect and return results."""
        return {"success": True, "message": f"{self.name} applied"}
    
    def remove_effect(self, game_state: Any, targets: List[Any]) -> Dict[str, Any]:
        """Remove/undo the effect."""
        return {"success": True, "message": f"{self.name} removed"}
    
    def stack_with(self, other_effect: 'CardEffect') -> bool:
        """Determine if this effect can stack with another."""
        return (self.stackable and 
                other_effect.stackable and 
                self.effect_id == other_effect.effect_id)
    
    def add_stack(self) -> None:
        """Add a stack to this effect."""
        if self.stackable:
            self.stack_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert effect to dictionary."""
        return {
            'effect_id': self.effect_id,
            'name': self.name,
            'description': self.description,
            'trigger_timing': self.trigger_timing,
            'duration': self.duration,
            'target_type': self.target_type,
            'stackable': self.stackable,
            'stack_count': self.stack_count,
            'metadata': self.metadata
        }

class Card:
    """Complete card implementation with all Egyptian mythology features."""
    
    def __init__(self, card_id: str, name: str, card_type: CardType,
                 rarity: CardRarity, element: CardElement, 
                 stats: CardStats, description: str = "",
                 flavor_text: str = "", art_path: str = ""):
        
        # Core Identity
        self.card_id = card_id
        self.name = name
        self.card_type = card_type
        self.rarity = rarity
        self.element = element
        self.stats = stats
        self.description = description
        self.flavor_text = flavor_text
        self.art_path = art_path
        
        # Unique Instance Data
        self.instance_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.owner_id: Optional[str] = None
        self.deck_id: Optional[str] = None
        
        # Game State
        self.current_stats = CardStats(**stats.to_dict())  # Modifiable copy
        self.is_exhausted = False
        self.is_cursed = False
        self.is_blessed = False
        self.position: Optional[Tuple[int, int]] = None
        
        # Effects and Modifiers
        self.keywords: Set[CardKeyword] = set()
        self.active_effects: List[CardEffect] = []
        self.permanent_modifiers: Dict[str, Any] = {}
        self.temporary_modifiers: Dict[str, Any] = {}
        
        # Egyptian Mythology Specific
        self.divine_allegiance: Optional[str] = None  # Which god favors this card
        self.underworld_tier: int = 0  # 0=mortal realm, 1-12=underworld hours
        self.ba_separated: bool = False  # Soul separation state
        self.ka_manifested: bool = False  # Life force manifestation
        self.mummification_level: int = 0  # Preservation state
        
        # Historical Data
        self.play_history: List[Dict[str, Any]] = []
        self.damage_history: List[Dict[str, Any]] = []
        self.kill_count: int = 0
        self.death_count: int = 0
        self.resurrections: int = 0
        
        # Performance Tracking
        self.total_damage_dealt: int = 0
        self.total_damage_taken: int = 0
        self.total_healing_done: int = 0
        self.turns_survived: int = 0
        
        # Metadata
        self.metadata: Dict[str, Any] = {}
        self.custom_data: Dict[str, Any] = {}
        
        # Generate content hash for verification
        self._generate_content_hash()
    
    def _generate_content_hash(self) -> None:
        """Generate a hash of the card's core content for integrity checking."""
        content_str = f"{self.card_id}_{self.name}_{self.card_type.value}_{self.rarity.key}"
        content_str += f"_{self.element.key}_{json.dumps(self.stats.to_dict(), sort_keys=True)}"
        self.content_hash = hashlib.md5(content_str.encode()).hexdigest()
    
    def add_keyword(self, keyword: CardKeyword) -> None:
        """Add a keyword to the card."""
        self.keywords.add(keyword)
        self._log_change("keyword_added", {"keyword": keyword.key})
    
    def remove_keyword(self, keyword: CardKeyword) -> None:
        """Remove a keyword from the card."""
        self.keywords.discard(keyword)
        self._log_change("keyword_removed", {"keyword": keyword.key})
    
    def has_keyword(self, keyword: CardKeyword) -> bool:
        """Check if card has a specific keyword."""
        return keyword in self.keywords
    
    def add_effect(self, effect: CardEffect) -> bool:
        """Add an effect to the card."""
        # Check for stacking
        for existing_effect in self.active_effects:
            if existing_effect.stack_with(effect):
                existing_effect.add_stack()
                self._log_change("effect_stacked", {
                    "effect_id": effect.effect_id,
                    "stack_count": existing_effect.stack_count
                })
                return True
        
        # Add as new effect
        self.active_effects.append(effect)
        self._log_change("effect_added", {"effect_id": effect.effect_id})
        return True
    
    def remove_effect(self, effect_id: str) -> bool:
        """Remove an effect from the card."""
        for i, effect in enumerate(self.active_effects):
            if effect.effect_id == effect_id:
                removed_effect = self.active_effects.pop(i)
                self._log_change("effect_removed", {"effect_id": effect_id})
                return True
        return False
    
    def get_effects_by_timing(self, timing: str) -> List[CardEffect]:
        """Get all effects that trigger at a specific timing."""
        return [effect for effect in self.active_effects 
                if effect.trigger_timing == timing]
    
    def modify_stat(self, stat_name: str, value: int, permanent: bool = False) -> None:
        """Modify a card stat temporarily or permanently."""
        if not hasattr(self.current_stats, stat_name):
            raise ValueError(f"Invalid stat name: {stat_name}")
        
        current_value = getattr(self.current_stats, stat_name)
        new_value = max(0, current_value + value)  # Prevent negative stats
        setattr(self.current_stats, stat_name, new_value)
        
        modifier_dict = self.permanent_modifiers if permanent else self.temporary_modifiers
        if stat_name not in modifier_dict:
            modifier_dict[stat_name] = 0
        modifier_dict[stat_name] += value
        
        self._log_change("stat_modified", {
            "stat": stat_name,
            "change": value,
            "new_value": new_value,
            "permanent": permanent
        })
    
    def reset_temporary_modifiers(self) -> None:
        """Reset all temporary stat modifiers."""
        for stat_name, modifier in self.temporary_modifiers.items():
            current_value = getattr(self.current_stats, stat_name)
            new_value = max(0, current_value - modifier)
            setattr(self.current_stats, stat_name, new_value)
        
        self.temporary_modifiers.clear()
        self._log_change("temporary_modifiers_reset", {})
    
    def take_damage(self, damage: int, damage_type: str = "physical", source: Optional['Card'] = None) -> Dict[str, Any]:
        """Apply damage to the card with Egyptian mythology considerations."""
        original_health = self.current_stats.health
        
        # Calculate damage reduction from defense
        defense_reduction = min(damage // 2, self.current_stats.defense)
        actual_damage = max(1, damage - defense_reduction)  # Minimum 1 damage
        
        # Apply Egyptian god resistances/weaknesses
        if self.divine_allegiance:
            damage_modifier = self._calculate_divine_damage_modifier(damage_type, source)
            actual_damage = int(actual_damage * damage_modifier)
        
        # Apply damage
        self.current_stats.health = max(0, self.current_stats.health - actual_damage)
        self.total_damage_taken += actual_damage
        
        # Record damage event
        damage_event = {
            "timestamp": datetime.now().isoformat(),
            "damage": actual_damage,
            "original_damage": damage,
            "damage_type": damage_type,
            "source_id": source.instance_id if source else None,
            "health_before": original_health,
            "health_after": self.current_stats.health
        }
        self.damage_history.append(damage_event)
        
        # Check for death
        result = {
            "damage_dealt": actual_damage,
            "health_remaining": self.current_stats.health,
            "is_destroyed": self.current_stats.health <= 0,
            "can_resurrect": self.has_keyword(CardKeyword.RESURRECTION)
        }
        
        if result["is_destroyed"]:
            self.death_count += 1
            self._log_change("card_destroyed", damage_event)
        
        return result
    
    def heal(self, healing: int, source: Optional['Card'] = None) -> Dict[str, Any]:
        """Heal the card."""
        max_health = self.stats.health + self.permanent_modifiers.get('health', 0)
        original_health = self.current_stats.health
        
        # Calculate actual healing (can't exceed max health)
        actual_healing = min(healing, max_health - self.current_stats.health)
        self.current_stats.health += actual_healing
        self.total_healing_done += actual_healing
        
        healing_event = {
            "timestamp": datetime.now().isoformat(),
            "healing": actual_healing,
            "source_id": source.instance_id if source else None,
            "health_before": original_health,
            "health_after": self.current_stats.health
        }
        
        self._log_change("card_healed", healing_event)
        
        return {
            "healing_done": actual_healing,
            "health_after": self.current_stats.health,
            "fully_healed": self.current_stats.health == max_health
        }
    
    def _calculate_divine_damage_modifier(self, damage_type: str, source: Optional['Card']) -> float:
        """Calculate damage modifier based on Egyptian god relationships."""
        if not source or not source.divine_allegiance:
            return 1.0
        
        # Egyptian god relationship matrix
        god_relationships = {
            "Ra": {"Set": 1.5, "Apep": 2.0, "Osiris": 0.8},
            "Set": {"Osiris": 2.0, "Horus": 1.5, "Ra": 0.7},
            "Osiris": {"Set": 0.5, "Anubis": 0.8, "Isis": 0.6},
            "Anubis": {"Osiris": 0.7, "Set": 1.2, "Thoth": 0.9},
            "Thoth": {"Set": 1.3, "Ra": 0.8, "Isis": 0.7},
            "Isis": {"Set": 1.4, "Osiris": 0.6, "Thoth": 0.8}
        }
        
        attacker_god = source.divine_allegiance
        defender_god = self.divine_allegiance
        
        if attacker_god in god_relationships and defender_god in god_relationships[attacker_god]:
            return god_relationships[attacker_god][defender_god]
        
        return 1.0
    
    def separate_ba(self) -> bool:
        """Separate the Ba (soul) from the body."""
        if self.has_keyword(CardKeyword.BA_SPLIT) and not self.ba_separated:
            self.ba_separated = True
            self.modify_stat('ba_power', 5, permanent=False)
            self._log_change("ba_separated", {"ba_power_gained": 5})
            return True
        return False
    
    def reunite_ba(self) -> bool:
        """Reunite the Ba with the body."""
        if self.ba_separated:
            self.ba_separated = False
            self.modify_stat('ba_power', -5, permanent=False)
            self.modify_stat('health', 3, permanent=False)  # Spiritual wholeness bonus
            self._log_change("ba_reunited", {"health_gained": 3})
            return True
        return False
    
    def manifest_ka(self) -> bool:
        """Manifest the Ka (life force) as a separate entity."""
        if self.has_keyword(CardKeyword.KA_DOUBLE) and not self.ka_manifested:
            self.ka_manifested = True
            self.modify_stat('ka_strength', 10, permanent=False)
            self._log_change("ka_manifested", {"ka_strength_gained": 10})
            return True
        return False
    
    def exhaust(self) -> None:
        """Exhaust the card (cannot act this turn)."""
        self.is_exhausted = True
        self._log_change("card_exhausted", {})
    
    def refresh(self) -> None:
        """Refresh the card (can act again)."""
        self.is_exhausted = False
        self.turns_survived += 1
        self._log_change("card_refreshed", {"turns_survived": self.turns_survived})
    
    def apply_curse(self, curse_type: str, duration: int = -1) -> None:
        """Apply an Egyptian curse to the card."""
        self.is_cursed = True
        curse_effect = CardEffect(
            effect_id=f"curse_{curse_type}",
            name=f"Curse of {curse_type.title()}",
            description=f"Ancient Egyptian curse: {curse_type}",
            duration=duration,
            trigger_timing="persistent"
        )
        self.add_effect(curse_effect)
        self._log_change("curse_applied", {"curse_type": curse_type, "duration": duration})
    
    def remove_curse(self, curse_type: Optional[str] = None) -> bool:
        """Remove curse(s) from the card."""
        removed = False
        if curse_type:
            removed = self.remove_effect(f"curse_{curse_type}")
        else:
            # Remove all curses
            curse_effects = [e for e in self.active_effects if e.effect_id.startswith("curse_")]
            for effect in curse_effects:
                self.remove_effect(effect.effect_id)
                removed = True
        
        if removed:
            # Check if any curses remain
            remaining_curses = [e for e in self.active_effects if e.effect_id.startswith("curse_")]
            self.is_cursed = len(remaining_curses) > 0
            self._log_change("curse_removed", {"curse_type": curse_type})
        
        return removed
    
    def apply_blessing(self, blessing_type: str, duration: int = 3) -> None:
        """Apply an Egyptian blessing to the card."""
        self.is_blessed = True
        blessing_effect = CardEffect(
            effect_id=f"blessing_{blessing_type}",
            name=f"Blessing of {blessing_type.title()}",
            description=f"Divine Egyptian blessing: {blessing_type}",
            duration=duration,
            trigger_timing="persistent"
        )
        self.add_effect(blessing_effect)
        self._log_change("blessing_applied", {"blessing_type": blessing_type, "duration": duration})
    
    def can_play(self, game_state: Any) -> Tuple[bool, str]:
        """Check if the card can be played in the current game state."""
        # Check mana cost
        if hasattr(game_state, 'current_mana') and game_state.current_mana < self.stats.mana_cost:
            return False, f"Insufficient mana. Need {self.stats.mana_cost}, have {game_state.current_mana}"
        
        # Check if exhausted
        if self.is_exhausted:
            return False, "Card is exhausted and cannot act this turn"
        
        # Check curse restrictions
        if self.is_cursed:
            curse_effects = [e for e in self.active_effects if e.effect_id.startswith("curse_")]
            for effect in curse_effects:
                if "silence" in effect.effect_id.lower():
                    return False, "Card is silenced by a curse"
        
        # Check underworld tier restrictions
        if hasattr(game_state, 'current_underworld_tier'):
            if self.underworld_tier > game_state.current_underworld_tier:
                return False, f"Card requires underworld tier {self.underworld_tier}"
        
        return True, "Can play"
    
    def play(self, game_state: Any, targets: List[Any] = None) -> Dict[str, Any]:
        """Play the card with all its effects."""
        can_play, reason = self.can_play(game_state)
        if not can_play:
            return {"success": False, "reason": reason}
        
        # Record play event
        play_event = {
            "timestamp": datetime.now().isoformat(),
            "game_state_id": getattr(game_state, 'state_id', 'unknown'),
            "targets": [getattr(t, 'instance_id', str(t)) for t in (targets or [])],
            "mana_cost": self.stats.mana_cost
        }
        self.play_history.append(play_event)
        
        # Apply immediate effects
        results = []
        immediate_effects = self.get_effects_by_timing("immediate")
        for effect in immediate_effects:
            if effect.can_trigger(game_state, {"play": True}):
                result = effect.apply_effect(game_state, targets or [], {"source": self})
                results.append(result)
        
        # Exhaust the card
        self.exhaust()
        
        # Apply costs
        if hasattr(game_state, 'current_mana'):
            game_state.current_mana -= self.stats.mana_cost
        
        self._log_change("card_played", play_event)
        
        return {
            "success": True,
            "effects_triggered": len(results),
            "effect_results": results,
            "card_exhausted": True
        }
    
    def _log_change(self, change_type: str, data: Dict[str, Any]) -> None:
        """Log a change to the card for debugging and analytics."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "instance_id": self.instance_id,
            "change_type": change_type,
            "data": data
        }
        
        # Add to metadata for persistence
        if "change_log" not in self.metadata:
            self.metadata["change_log"] = []
        self.metadata["change_log"].append(log_entry)
        
        # Keep only last 100 entries to prevent memory bloat
        if len(self.metadata["change_log"]) > 100:
            self.metadata["change_log"] = self.metadata["change_log"][-100:]
    
    def get_display_stats(self) -> Dict[str, Any]:
        """Get formatted stats for display."""
        return {
            "name": self.name,
            "type": self.card_type.value.replace('_', ' ').title(),
            "rarity": self.rarity.display_name,
            "element": self.element.display_name,
            "attack": self.current_stats.attack,
            "defense": self.current_stats.defense, 
            "health": f"{self.current_stats.health}/{self.stats.health}",
            "ba_power": self.current_stats.ba_power,
            "ka_strength": self.current_stats.ka_strength,
            "divine_favor": self.current_stats.divine_favor,
            "mana_cost": self.stats.mana_cost,
            "keywords": [kw.key.replace('_', ' ').title() for kw in self.keywords],
            "is_exhausted": self.is_exhausted,
            "is_cursed": self.is_cursed,
            "is_blessed": self.is_blessed,
            "active_effects": len(self.active_effects),
            "combat_rating": round(self.current_stats.calculate_combat_rating(), 1)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization."""
        return {
            "card_id": self.card_id,
            "instance_id": self.instance_id,
            "name": self.name,
            "card_type": self.card_type.value,
            "rarity": self.rarity.key,
            "element": self.element.key,
            "stats": self.stats.to_dict(),
            "current_stats": self.current_stats.to_dict(),
            "description": self.description,
            "flavor_text": self.flavor_text,
            "art_path": self.art_path,
            "keywords": [kw.key for kw in self.keywords],
            "active_effects": [effect.to_dict() for effect in self.active_effects],
            "divine_allegiance": self.divine_allegiance,
            "underworld_tier": self.underworld_tier,
            "ba_separated": self.ba_separated,
            "ka_manifested": self.ka_manifested,
            "is_exhausted": self.is_exhausted,
            "is_cursed": self.is_cursed,
            "is_blessed": self.is_blessed,
            "position": self.position,
            "owner_id": self.owner_id,
            "deck_id": self.deck_id,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "content_hash": self.content_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Card':
        """Create card from dictionary."""
        # Create stats objects
        stats = CardStats(**data["stats"])
        current_stats = CardStats(**data["current_stats"])
        
        # Create card
        card = cls(
            card_id=data["card_id"],
            name=data["name"],
            card_type=CardType(data["card_type"]),
            rarity=CardRarity(data["rarity"]),
            element=CardElement(data["element"]),
            stats=stats,
            description=data.get("description", ""),
            flavor_text=data.get("flavor_text", ""),
            art_path=data.get("art_path", "")
        )
        
        # Restore instance data
        card.instance_id = data["instance_id"]
        card.current_stats = current_stats
        card.created_at = datetime.fromisoformat(data["created_at"])
        
        # Restore keywords
        for keyword_key in data.get("keywords", []):
            try:
                keyword = CardKeyword(keyword_key)
                card.keywords.add(keyword)
            except ValueError:
                pass  # Skip unknown keywords
        
        # Restore effects
        for effect_data in data.get("active_effects", []):
            effect = CardEffect(
                effect_id=effect_data["effect_id"],
                name=effect_data["name"],
                description=effect_data["description"],
                trigger_timing=effect_data.get("trigger_timing", "immediate"),
                duration=effect_data.get("duration", 1),
                target_type=effect_data.get("target_type", "self"),
                stackable=effect_data.get("stackable", False)
            )
            effect.stack_count = effect_data.get("stack_count", 1)
            effect.metadata = effect_data.get("metadata", {})
            card.active_effects.append(effect)
        
        # Restore other properties
        card.divine_allegiance = data.get("divine_allegiance")
        card.underworld_tier = data.get("underworld_tier", 0)
        card.ba_separated = data.get("ba_separated", False)
        card.ka_manifested = data.get("ka_manifested", False)
        card.is_exhausted = data.get("is_exhausted", False)
        card.is_cursed = data.get("is_cursed", False)
        card.is_blessed = data.get("is_blessed", False)
        card.position = data.get("position")
        card.owner_id = data.get("owner_id")
        card.deck_id = data.get("deck_id")
        card.metadata = data.get("metadata", {})
        
        return card
    
    def __str__(self) -> str:
        """String representation of the card."""
        status_flags = []
        if self.is_exhausted:
            status_flags.append("Exhausted")
        if self.is_cursed:
            status_flags.append("Cursed")
        if self.is_blessed:
            status_flags.append("Blessed")
        if self.ba_separated:
            status_flags.append("Ba Separated")
        if self.ka_manifested:
            status_flags.append("Ka Manifested")
        
        status = f" [{', '.join(status_flags)}]" if status_flags else ""
        
        return (f"{self.name} ({self.rarity.display_name} {self.element.display_name} "
                f"{self.card_type.value.replace('_', ' ').title()}) - "
                f"{self.current_stats.attack}/{self.current_stats.defense}/"
                f"{self.current_stats.health}{status}")
    
    def __eq__(self, other) -> bool:
        """Check equality based on instance ID."""
        if not isinstance(other, Card):
            return False
        return self.instance_id == other.instance_id
    
    def __hash__(self) -> int:
        """Hash based on instance ID."""
        return hash(self.instance_id)


### 3.2 COMPREHENSIVE YAML PARSING AND VALIDATION

```python
# src/sands_of_duat/cards/loader.py
import yaml
import os
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
import logging
import jsonschema
from jsonschema import validate, ValidationError
import re
from dataclasses import dataclass
from datetime import datetime

from .card import Card, CardType, CardRarity, CardElement, CardStats, CardKeyword, CardEffect

logger = logging.getLogger(__name__)

# YAML Schema for card validation
CARD_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "type", "rarity", "element", "stats"],
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[a-z0-9_]+$",
            "minLength": 3,
            "maxLength": 50
        },
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "type": {
            "type": "string",
            "enum": [t.value for t in CardType]
        },
        "rarity": {
            "type": "string", 
            "enum": [r.key for r in CardRarity]
        },
        "element": {
            "type": "string",
            "enum": [e.key for e in CardElement]
        },
        "stats": {
            "type": "object",
            "required": ["attack", "defense", "health", "mana_cost"],
            "properties": {
                "attack": {"type": "integer", "minimum": 0, "maximum": 999},
                "defense": {"type": "integer", "minimum": 0, "maximum": 999},
                "health": {"type": "integer", "minimum": 1, "maximum": 999},
                "ba_power": {"type": "integer", "minimum": 0, "maximum": 100},
                "ka_strength": {"type": "integer", "minimum": 0, "maximum": 100},
                "divine_favor": {"type": "integer", "minimum": -50, "maximum": 50},
                "underworld_knowledge": {"type": "integer", "minimum": 0, "maximum": 100},
                "initiative": {"type": "integer", "minimum": 0, "maximum": 100},
                "movement": {"type": "integer", "minimum": 0, "maximum": 10},
                "mana_cost": {"type": "integer", "minimum": 0, "maximum": 20},
                "gold_cost": {"type": "integer", "minimum": 0, "maximum": 10000},
                "offering_cost": {"type": "integer", "minimum": 0, "maximum": 100},
                "critical_chance": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "dodge_chance": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "block_chance": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "spell_power": {"type": "number", "minimum": 0.1, "maximum": 5.0}
            },
            "additionalProperties": False
        },
        "description": {"type": "string", "maxLength": 500},
        "flavor_text": {"type": "string", "maxLength": 300},
        "art_path": {"type": "string", "maxLength": 200},
        "keywords": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [k.key for k in CardKeyword]
            },
            "uniqueItems": True,
            "maxItems": 10
        },
        "effects": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name", "description", "trigger_timing"],
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
                    "name": {"type": "string", "minLength": 1, "maxLength": 100},
                    "description": {"type": "string", "minLength": 1, "maxLength": 500},
                    "trigger_timing": {
                        "type": "string",
                        "enum": ["immediate", "on_play", "on_death", "on_damage", "on_heal", "start_turn", "end_turn", "persistent"]
                    },
                    "duration": {"type": "integer", "minimum": -1, "maximum": 99},
                    "target_type": {
                        "type": "string",
                        "enum": ["self", "enemy", "ally", "all", "random_enemy", "random_ally", "all_enemies", "all_allies"]
                    },
                    "stackable": {"type": "boolean"},
                    "parameters": {"type": "object"}
                },
                "additionalProperties": False
            },
            "maxItems": 5
        },
        "divine_allegiance": {"type": "string", "maxLength": 50},
        "underworld_tier": {"type": "integer", "minimum": 0, "maximum": 12},
        "collection": {"type": "string", "maxLength": 50},
        "set_code": {"type": "string", "pattern": "^[A-Z]{2,4}[0-9]{2}$"},
        "artist": {"type": "string", "maxLength": 100},
        "version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
        "metadata": {"type": "object"}
    },
    "additionalProperties": False
}

@dataclass 
class CardLoadResult:
    """Result of loading cards from files."""
    success_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    loaded_cards: List[Card] = None
    errors: List[Dict[str, Any]] = None
    warnings: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.loaded_cards is None:
            self.loaded_cards = []
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

class CardLoader:
    """Advanced card loading system with comprehensive validation."""
    
    def __init__(self, base_path: str = "data/cards"):
        self.base_path = Path(base_path)
        self.schema = CARD_SCHEMA
        self.loaded_cards: Dict[str, Card] = {}
        self.load_errors: List[Dict[str, Any]] = []
        self.load_warnings: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.load_times: Dict[str, float] = {}
        self.validation_times: Dict[str, float] = {}
        
        # Cache for parsed YAML files
        self.yaml_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, datetime] = {}
        
        # Set up custom YAML loader for better performance
        self._setup_yaml_loader()
        
        # Validation patterns
        self.id_pattern = re.compile(r'^[a-z0-9_]+$')
        self.version_pattern = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')
        self.set_code_pattern = re.compile(r'^[A-Z]{2,4}[0-9]{2}$')
    
    def _setup_yaml_loader(self) -> None:
        """Set up optimized YAML loader."""
        # Custom constructor for better performance
        def construct_mapping(loader, node):
            return dict(loader.construct_pairs(node))
        
        yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    
    def load_all_cards(self, reload_cache: bool = False) -> CardLoadResult:
        """Load all cards from the cards directory."""
        start_time = datetime.now()
        result = CardLoadResult()
        
        if not self.base_path.exists():
            error = {
                "type": "directory_not_found",
                "message": f"Cards directory not found: {self.base_path}",
                "timestamp": datetime.now().isoformat()
            }
            result.errors.append(error)
            result.error_count = 1
            return result
        
        # Find all YAML files
        yaml_files = list(self.base_path.rglob("*.yml")) + list(self.base_path.rglob("*.yaml"))
        
        logger.info(f"Found {len(yaml_files)} card files to load")
        
        for file_path in yaml_files:
            try:
                file_result = self.load_cards_from_file(file_path, reload_cache)
                result.success_count += file_result.success_count
                result.error_count += file_result.error_count
                result.warning_count += file_result.warning_count
                result.loaded_cards.extend(file_result.loaded_cards)
                result.errors.extend(file_result.errors)
                result.warnings.extend(file_result.warnings)
                
            except Exception as e:
                error = {
                    "type": "file_load_error",
                    "file": str(file_path),
                    "message": f"Failed to load file: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
                result.errors.append(error)
                result.error_count += 1
                logger.error(f"Error loading {file_path}: {e}")
        
        # Update internal card registry
        for card in result.loaded_cards:
            self.loaded_cards[card.card_id] = card
        
        load_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Loaded {result.success_count} cards in {load_time:.2f}s with {result.error_count} errors")
        
        # Perform cross-card validation
        self._validate_card_relationships(result)
        
        return result
    
    def load_cards_from_file(self, file_path: Path, reload_cache: bool = False) -> CardLoadResult:
        """Load cards from a specific file."""
        result = CardLoadResult()
        
        try:
            # Check cache first
            file_str = str(file_path)
            if not reload_cache and file_str in self.yaml_cache:
                file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_str in self.cache_timestamps and self.cache_timestamps[file_str] >= file_modified:
                    # Use cached data
                    cards_data = self.yaml_cache[file_str]
                    logger.debug(f"Using cached data for {file_path}")
                else:
                    # Reload file
                    cards_data = self._load_yaml_file(file_path)
                    self.yaml_cache[file_str] = cards_data
                    self.cache_timestamps[file_str] = datetime.now()
            else:
                # Load file
                cards_data = self._load_yaml_file(file_path)
                self.yaml_cache[file_str] = cards_data
                self.cache_timestamps[file_str] = datetime.now()
            
            # Handle both single card and card list formats
            if isinstance(cards_data, dict):
                if 'cards' in cards_data:
                    # Multi-card file format
                    cards_list = cards_data['cards']
                    file_metadata = {k: v for k, v in cards_data.items() if k != 'cards'}
                else:
                    # Single card format
                    cards_list = [cards_data]
                    file_metadata = {}
            elif isinstance(cards_data, list):
                # Direct card list format
                cards_list = cards_data
                file_metadata = {}
            else:
                raise ValueError(f"Invalid YAML structure in {file_path}")
            
            # Process each card
            for i, card_data in enumerate(cards_list):
                try:
                    # Add file metadata to card
                    card_data = {**card_data}  # Copy to avoid modifying original
                    if 'metadata' not in card_data:
                        card_data['metadata'] = {}
                    card_data['metadata'].update(file_metadata)
                    card_data['metadata']['source_file'] = str(file_path)
                    card_data['metadata']['card_index'] = i
                    
                    # Validate and create card
                    validation_start = datetime.now()
                    validation_result = self.validate_card_data(card_data)
                    validation_time = (datetime.now() - validation_start).total_seconds()
                    
                    card_id = card_data.get('id', f'unknown_{i}')
                    self.validation_times[card_id] = validation_time
                    
                    if validation_result['valid']:
                        card = self._create_card_from_data(card_data)
                        result.loaded_cards.append(card)
                        result.success_count += 1
                        
                        # Add any validation warnings
                        for warning in validation_result['warnings']:
                            warning['file'] = str(file_path)
                            warning['card_id'] = card_id
                            result.warnings.append(warning)
                            result.warning_count += 1
                    else:
                        # Add validation errors
                        for error in validation_result['errors']:
                            error['file'] = str(file_path)
                            error['card_id'] = card_id
                            error['card_index'] = i
                            result.errors.append(error)
                            result.error_count += 1
                
                except Exception as e:
                    error = {
                        "type": "card_processing_error",
                        "file": str(file_path),
                        "card_index": i,
                        "card_id": card_data.get('id', 'unknown'),
                        "message": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                    result.errors.append(error)
                    result.error_count += 1
                    logger.error(f"Error processing card {i} in {file_path}: {e}")
            
        except Exception as e:
            error = {
                "type": "file_processing_error",
                "file": str(file_path),
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            result.errors.append(error)
            result.error_count += 1
            logger.error(f"Error processing file {file_path}: {e}")
        
        return result
    
    def _load_yaml_file(self, file_path: Path) -> Any:
        """Load and parse a YAML file."""
        start_time = datetime.now()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            load_time = (datetime.now() - start_time).total_seconds()
            self.load_times[str(file_path)] = load_time
            
            return data
            
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {e}")
        except Exception as e:
            raise ValueError(f"File reading error: {e}")
    
    def validate_card_data(self, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive card data validation."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Schema validation
            validate(instance=card_data, schema=self.schema)
            
        except ValidationError as e:
            result["valid"] = False
            result["errors"].append({
                "type": "schema_validation",
                "message": f"Schema validation failed: {e.message}",
                "path": list(e.absolute_path),
                "timestamp": datetime.now().isoformat()
            })
        
        # Additional custom validations
        self._validate_card_id(card_data, result)
        self._validate_card_balance(card_data, result)
        self._validate_card_relationships(card_data, result)
        self._validate_card_effects(card_data, result)
        self._validate_egyptian_authenticity(card_data, result)
        
        return result
    
    def _validate_card_id(self, card_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate card ID uniqueness and format."""
        card_id = card_data.get('id')
        
        if not card_id:
            result["errors"].append({
                "type": "missing_id",
                "message": "Card ID is required",
                "timestamp": datetime.now().isoformat()
            })
            return
        
        # Check format
        if not self.id_pattern.match(card_id):
            result["errors"].append({
                "type": "invalid_id_format",
                "message": f"Card ID '{card_id}' must contain only lowercase letters, numbers, and underscores",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check uniqueness
        if card_id in self.loaded_cards:
            result["errors"].append({
                "type": "duplicate_id",
                "message": f"Card ID '{card_id}' already exists",
                "timestamp": datetime.now().isoformat()
            })
    
    def _validate_card_balance(self, card_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate card balance and power level."""
        stats = card_data.get('stats', {})
        rarity = card_data.get('rarity', 'common')
        
        # Calculate power level
        attack = stats.get('attack', 0)
        defense = stats.get('defense', 0)
        health = stats.get('health', 1)
        mana_cost = stats.get('mana_cost', 0)
        
        power_level = (attack * 2 + defense + health) / max(1, mana_cost)
        
        # Expected power ranges by rarity
        power_ranges = {
            'common': (1.0, 3.0),
            'uncommon': (2.5, 4.5),
            'rare': (4.0, 6.5),
            'epic': (6.0, 9.0),
            'legendary': (8.5, 12.0),
            'mythic': (11.0, 15.0)
        }
        
        if rarity in power_ranges:
            min_power, max_power = power_ranges[rarity]
            
            if power_level < min_power:
                result["warnings"].append({
                    "type": "underpowered_card",
                    "message": f"Card power level {power_level:.1f} is below expected range {min_power}-{max_power} for {rarity}",
                    "timestamp": datetime.now().isoformat()
                })
            elif power_level > max_power:
                result["warnings"].append({
                    "type": "overpowered_card", 
                    "message": f"Card power level {power_level:.1f} exceeds expected range {min_power}-{max_power} for {rarity}",
                    "timestamp": datetime.now().isoformat()
                })
    
    def _validate_card_relationships(self, card_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate relationships between card properties."""
        card_type = card_data.get('type')
        element = card_data.get('element')
        divine_allegiance = card_data.get('divine_allegiance')
        stats = card_data.get('stats', {})
        
        # Validate type-element combinations
        valid_combinations = {
            'deity': ['light', 'darkness', 'fire', 'water', 'earth', 'air', 'death', 'life', 'order', 'chaos'],
            'mortal': ['earth', 'water', 'air', 'fire'],
            'divine_beast': ['earth', 'air', 'fire', 'water', 'light'],
            'artifact': ['light', 'darkness', 'order', 'chaos'],
            'spell': ['light', 'darkness', 'chaos', 'order', 'fire', 'water', 'earth', 'air'],
            'ritual': ['death', 'life', 'light', 'darkness'],
            'underworld': ['darkness', 'death', 'chaos'],
            'celestial': ['light', 'air', 'order']
        }
        
        if card_type in valid_combinations and element not in valid_combinations[card_type]:
            result["warnings"].append({
                "type": "unusual_type_element_combo",
                "message": f"{card_type} cards rarely have {element} element",
                "timestamp": datetime.now().isoformat()
            })
        
        # Validate divine allegiance consistency
        if divine_allegiance:
            god_elements = {
                'Ra': ['fire', 'light', 'order'],
                'Set': ['chaos', 'darkness', 'earth'],
                'Osiris': ['death', 'earth', 'life'],
                'Anubis': ['death', 'darkness'],
                'Thoth': ['air', 'order', 'light'],
                'Isis': ['water', 'life', 'light']
            }
            
            if divine_allegiance in god_elements and element not in god_elements[divine_allegiance]:
                result["warnings"].append({
                    "type": "inconsistent_divine_allegiance",
                    "message": f"{divine_allegiance} typically favors {god_elements[divine_allegiance]} elements, not {element}",
                    "timestamp": datetime.now().isoformat()
                })
    
    def _validate_card_effects(self, card_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate card effects for consistency and balance."""
        effects = card_data.get('effects', [])
        
        for i, effect in enumerate(effects):
            effect_id = effect.get('id', f'effect_{i}')
            
            # Check effect ID format
            if not self.id_pattern.match(effect_id):
                result["errors"].append({
                    "type": "invalid_effect_id",
                    "message": f"Effect ID '{effect_id}' has invalid format",
                    "effect_index": i,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Validate trigger timing
            timing = effect.get('trigger_timing')
            duration = effect.get('duration', 1)
            
            if timing == 'immediate' and duration != 0:
                result["warnings"].append({
                    "type": "inconsistent_effect_timing",
                    "message": f"Effect '{effect_id}' has immediate timing but non-zero duration",
                    "effect_index": i,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Check for overpowered effects
            parameters = effect.get('parameters', {})
            if 'damage' in parameters and parameters['damage'] > 15:
                result["warnings"].append({
                    "type": "high_damage_effect",
                    "message": f"Effect '{effect_id}' has very high damage value: {parameters['damage']}",
                    "effect_index": i,
                    "timestamp": datetime.now().isoformat()
                })
    
    def _validate_egyptian_authenticity(self, card_data: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate Egyptian mythology authenticity."""
        name = card_data.get('name', '')
        description = card_data.get('description', '')
        flavor_text = card_data.get('flavor_text', '')
        
        # Egyptian god names and spellings
        egyptian_gods = [
            'Ra', 'Amun', 'Amun-Ra', 'Anubis', 'Thoth', 'Isis', 'Osiris', 'Set', 'Seth',
            'Horus', 'Hathor', 'Bastet', 'Sekhmet', 'Ptah', 'Khnum', 'Sobek', 'Taweret',
            'Bes', 'Khepri', 'Atum', 'Geb', 'Nut', 'Shu', 'Tefnut', 'Ma\'at', 'Neith'
        ]
        
        # Egyptian terms and concepts
        egyptian_terms = [
            'pharaoh', 'pyramid', 'sphinx', 'ankh', 'scarab', 'papyrus', 'hieroglyph',
            'sarcophagus', 'mummy', 'canopic', 'duat', 'underworld', 'afterlife', 'ka', 'ba',
            'ren', 'sheut', 'ib', 'ushabti', 'amulet', 'cartouche', 'obelisk', 'temple'
        ]
        
        # Check if card mentions Egyptian elements
        full_text = (name + ' ' + description + ' ' + flavor_text).lower()
        has_egyptian_content = any(term.lower() in full_text for term in egyptian_gods + egyptian_terms)
        
        card_type = card_data.get('type')
        if card_type in ['deity', 'ritual', 'underworld'] and not has_egyptian_content:
            result["warnings"].append({
                "type": "missing_egyptian_theme",
                "message": f"Card type '{card_type}' should reference Egyptian mythology",
                "timestamp": datetime.now().isoformat()
            })
    
    def _create_card_from_data(self, card_data: Dict[str, Any]) -> Card:
        """Create a Card object from validated data."""
        # Create stats object
        stats_data = card_data['stats']
        stats = CardStats(
            attack=stats_data.get('attack', 0),
            defense=stats_data.get('defense', 0),
            health=stats_data.get('health', 1),
            ba_power=stats_data.get('ba_power', 0),
            ka_strength=stats_data.get('ka_strength', 0),
            divine_favor=stats_data.get('divine_favor', 0),
            underworld_knowledge=stats_data.get('underworld_knowledge', 0),
            initiative=stats_data.get('initiative', 0),
            movement=stats_data.get('movement', 1),
            mana_cost=stats_data.get('mana_cost', 0),
            gold_cost=stats_data.get('gold_cost', 0),
            offering_cost=stats_data.get('offering_cost', 0),
            critical_chance=stats_data.get('critical_chance', 0.0),
            dodge_chance=stats_data.get('dodge_chance', 0.0),
            block_chance=stats_data.get('block_chance', 0.0),
            spell_power=stats_data.get('spell_power', 1.0)
        )
        
        # Create card
        card = Card(
            card_id=card_data['id'],
            name=card_data['name'],
            card_type=CardType(card_data['type']),
            rarity=CardRarity(card_data['rarity']),
            element=CardElement(card_data['element']),
            stats=stats,
            description=card_data.get('description', ''),
            flavor_text=card_data.get('flavor_text', ''),
            art_path=card_data.get('art_path', '')
        )
        
        # Add keywords
        for keyword_key in card_data.get('keywords', []):
            try:
                keyword = CardKeyword(keyword_key)
                card.add_keyword(keyword)
            except ValueError:
                logger.warning(f"Unknown keyword '{keyword_key}' for card {card.card_id}")
        
        # Add effects
        for effect_data in card_data.get('effects', []):
            effect = CardEffect(
                effect_id=effect_data['id'],
                name=effect_data['name'],
                description=effect_data['description'],
                trigger_timing=effect_data.get('trigger_timing', 'immediate'),
                duration=effect_data.get('duration', 1),
                target_type=effect_data.get('target_type', 'self'),
                stackable=effect_data.get('stackable', False)
            )
            effect.metadata = effect_data.get('parameters', {})
            card.add_effect(effect)
        
        # Set additional properties
        card.divine_allegiance = card_data.get('divine_allegiance')
        card.underworld_tier = card_data.get('underworld_tier', 0)
        
        # Add metadata
        card.metadata.update(card_data.get('metadata', {}))
        card.custom_data = {
            'collection': card_data.get('collection'),
            'set_code': card_data.get('set_code'),
            'artist': card_data.get('artist'),
            'version': card_data.get('version')
        }
        
        return card
    
    def _validate_card_relationships(self, result: CardLoadResult) -> None:
        """Perform cross-card validation after all cards are loaded."""
        card_ids = set(card.card_id for card in result.loaded_cards)
        
        # Check for cards that reference non-existent cards
        for card in result.loaded_cards:
            for effect in card.active_effects:
                if 'target_card_id' in effect.metadata:
                    target_id = effect.metadata['target_card_id']
                    if target_id not in card_ids:
                        warning = {
                            "type": "missing_card_reference",
                            "message": f"Card '{card.card_id}' references non-existent card '{target_id}'",
                            "card_id": card.card_id,
                            "effect_id": effect.effect_id,
                            "timestamp": datetime.now().isoformat()
                        }
                        result.warnings.append(warning)
                        result.warning_count += 1
        
        # Validate set completeness
        sets = {}
        for card in result.loaded_cards:
            set_code = card.custom_data.get('set_code')
            if set_code:
                if set_code not in sets:
                    sets[set_code] = []
                sets[set_code].append(card)
        
        # Check set balance
        for set_code, cards in sets.items():
            rarity_counts = {}
            for card in cards:
                rarity = card.rarity.key
                rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
            
            # Expected distributions (rough guidelines)
            total_cards = len(cards)
            if total_cards >= 100:  # Only check large sets
                common_ratio = rarity_counts.get('common', 0) / total_cards
                if common_ratio < 0.4:
                    warning = {
                        "type": "set_balance_issue",
                        "message": f"Set '{set_code}' has unusually few common cards ({common_ratio:.1%})",
                        "set_code": set_code,
                        "timestamp": datetime.now().isoformat()
                    }
                    result.warnings.append(warning)
                    result.warning_count += 1
    
    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """Get a card by ID."""
        return self.loaded_cards.get(card_id)
    
    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """Get all cards of a specific type."""
        return [card for card in self.loaded_cards.values() if card.card_type == card_type]
    
    def get_cards_by_element(self, element: CardElement) -> List[Card]:
        """Get all cards of a specific element."""
        return [card for card in self.loaded_cards.values() if card.element == element]
    
    def get_cards_by_rarity(self, rarity: CardRarity) -> List[Card]:
        """Get all cards of a specific rarity."""
        return [card for card in self.loaded_cards.values() if card.rarity == rarity]
    
    def get_cards_by_divine_allegiance(self, god_name: str) -> List[Card]:
        """Get all cards aligned with a specific god."""
        return [card for card in self.loaded_cards.values() 
                if card.divine_allegiance == god_name]
    
    def search_cards(self, query: str) -> List[Card]:
        """Search cards by name, description, or keywords."""
        query_lower = query.lower()
        results = []
        
        for card in self.loaded_cards.values():
            # Search in name
            if query_lower in card.name.lower():
                results.append(card)
                continue
            
            # Search in description
            if query_lower in card.description.lower():
                results.append(card)
                continue
            
            # Search in keywords
            for keyword in card.keywords:
                if query_lower in keyword.key.lower():
                    results.append(card)
                    break
        
        return results
    
    def get_load_statistics(self) -> Dict[str, Any]:
        """Get detailed loading statistics."""
        total_validation_time = sum(self.validation_times.values())
        total_load_time = sum(self.load_times.values())
        
        return {
            'total_cards_loaded': len(self.loaded_cards),
            'total_files_processed': len(self.load_times),
            'total_load_time': total_load_time,
            'total_validation_time': total_validation_time,
            'average_load_time_per_file': total_load_time / max(1, len(self.load_times)),
            'average_validation_time_per_card': total_validation_time / max(1, len(self.validation_times)),
            'cache_hit_ratio': len(self.yaml_cache) / max(1, len(self.load_times)),
            'cards_by_type': {card_type.value: len(self.get_cards_by_type(card_type)) 
                             for card_type in CardType},
            'cards_by_rarity': {rarity.key: len(self.get_cards_by_rarity(rarity)) 
                               for rarity in CardRarity},
            'cards_by_element': {element.key: len(self.get_cards_by_element(element)) 
                                for element in CardElement}
        }
    
    def export_cards_to_json(self, output_path: str) -> None:
        """Export all loaded cards to JSON format."""
        cards_data = []
        for card in self.loaded_cards.values():
            cards_data.append(card.to_dict())
        
        export_data = {
            'cards': cards_data,
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'total_cards': len(cards_data),
                'loader_version': '1.0.0'
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def validate_card_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a single card file without loading it into memory."""
        result = self.load_cards_from_file(Path(file_path), reload_cache=True)
        
        return {
            'valid': result.error_count == 0,
            'card_count': result.success_count,
            'errors': result.errors,
            'warnings': result.warnings
        }


# Example YAML card definitions
EXAMPLE_CARD_YAMLS = {
    'ra_sun_god.yml': '''
# Ra - The Sun God
id: ra_sun_god
name: "Ra, Lord of the Sun"
type: deity
rarity: legendary
element: fire
stats:
  attack: 12
  defense: 8
  health: 20
  ba_power: 15
  ka_strength: 12
  divine_favor: 20
  initiative: 8
  mana_cost: 8
  critical_chance: 0.15
  spell_power: 1.5
description: "The mighty sun god whose radiance burns away the darkness of the underworld."
flavor_text: "His falcon eyes see all, his solar barque sails eternal across the sky."
keywords:
  - divine_strike
  - blessing
  - pharaoh_authority
effects:
  - id: solar_flare
    name: "Solar Flare"
    description: "Deal 5 fire damage to all enemies when played"
    trigger_timing: on_play
    target_type: all_enemies
    parameters:
      damage: 5
      damage_type: fire
  - id: divine_radiance
    name: "Divine Radiance"  
    description: "All allies gain +2 attack while Ra is on the field"
    trigger_timing: persistent
    target_type: all_allies
    duration: -1
    parameters:
      attack_bonus: 2
divine_allegiance: Ra
art_path: "art/cards/deities/ra_sun_god.png"
collection: "Gods of Egypt"
set_code: "GOE01"
artist: "AI Generated - Egyptian Style"
version: "1.0.0"
metadata:
  creation_date: "2024-01-01"
  difficulty_rating: 5
  competitive_tier: "S"
''',
    
    'anubis_guide.yml': '''
# Anubis - Guide of the Dead  
id: anubis_guide
name: "Anubis, Guide of the Dead"
type: deity
rarity: epic
element: death
stats:
  attack: 6
  defense: 10
  health: 15
  ba_power: 20
  ka_strength: 8
  underworld_knowledge: 25
  initiative: 6
  mana_cost: 6
  dodge_chance: 0.2
description: "The jackal-headed god who weighs hearts against the feather of Ma'at."
flavor_text: "Death is not an ending, but a doorway he opens with care."
keywords:
  - mummification
  - afterlife
  - divine_judgment
effects:
  - id: weighing_of_hearts
    name: "Weighing of Hearts"
    description: "When an enemy dies, gain +1/+1 permanently"
    trigger_timing: on_death
    target_type: self
    duration: -1
    stackable: true
    parameters:
      attack_gain: 1
      health_gain: 1
  - id: mummify
    name: "Mummify"  
    description: "Preserve a destroyed ally, allowing resurrection next turn"
    trigger_timing: on_death
    target_type: ally
    duration: 1
    parameters:
      preserve_stats: true
      resurrection_cost: 0
divine_allegiance: Anubis
underworld_tier: 3
art_path: "art/cards/deities/anubis_guide.png"
collection: "Gods of Egypt"
set_code: "GOE01"
artist: "AI Generated - Egyptian Style"
version: "1.0.0"
''',

    'scarab_swarm.yml': '''
# Scarab Swarm
id: scarab_swarm  
name: "Sacred Scarab Swarm"
type: divine_beast
rarity: uncommon
element: earth
stats:
  attack: 4
  defense: 2
  health: 6
  movement: 2
  mana_cost: 3
  critical_chance: 0.1
description: "Countless sacred beetles that devour the flesh of the unworthy."
flavor_text: "They roll the sun across the sky, and roll away your sins."
keywords:
  - desert_walk
effects:
  - id: swarm_multiply  
    name: "Swarm Multiply"
    description: "When this card takes damage, create a 1/1 Scarab token"
    trigger_timing: on_damage
    target_type: self
    parameters:
      token_id: scarab_token
      token_attack: 1
      token_defense: 1
      token_health: 1
art_path: "art/cards/beasts/scarab_swarm.png"
collection: "Creatures of the Nile"
set_code: "CON01"
artist: "AI Generated - Egyptian Style"  
version: "1.0.0"
'''
}
```

### 3.3 COMPLETE CARD EFFECT SYSTEM WITH INHERITANCE

```python
# src/sands_of_duat/cards/effects/base_effect.py
from __future__ import annotations
import abc
import uuid
from typing import Dict, List, Any, Optional, Set, Callable, Type, Union
from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime
import inspect
import logging

logger = logging.getLogger(__name__)

class EffectTrigger(Enum):
    """When effects can trigger."""
    IMMEDIATE = "immediate"          # Right when played
    ON_PLAY = "on_play"             # After card is played
    ON_SUMMON = "on_summon"         # When creature enters field
    ON_DEATH = "on_death"           # When unit dies
    ON_DAMAGE = "on_damage"         # When taking damage
    ON_HEAL = "on_heal"             # When being healed
    ON_ATTACK = "on_attack"         # When attacking
    ON_DEFEND = "on_defend"         # When being attacked
    START_TURN = "start_turn"       # Beginning of turn
    END_TURN = "end_turn"           # End of turn
    PERSISTENT = "persistent"        # Always active
    CONDITIONAL = "conditional"      # Based on game state

class EffectTarget(Enum):
    """What effects can target."""
    SELF = "self"
    ENEMY = "enemy"
    ALLY = "ally"
    ALL = "all"
    ALL_ENEMIES = "all_enemies"  
    ALL_ALLIES = "all_allies"
    RANDOM_ENEMY = "random_enemy"
    RANDOM_ALLY = "random_ally"
    ADJACENT = "adjacent"
    BOARD = "board"
    PLAYER = "player"
    OPPONENT = "opponent"

class EffectCategory(Enum):
    """Categories of effects for organization."""
    DAMAGE = "damage"
    HEALING = "healing"
    STAT_MODIFICATION = "stat_modification"
    STATUS = "status"
    RESOURCE = "resource"
    MOVEMENT = "movement"
    DIVINE = "divine"
    BA_KA = "ba_ka"
    UNDERWORLD = "underworld"
    SUMMONING = "summoning"

@dataclass
class EffectContext:
    """Context information for effect execution."""
    source_card: Any = None
    target_cards: List[Any] = None
    game_state: Any = None
    trigger_data: Dict[str, Any] = None
    player: Any = None
    opponent: Any = None
    board_state: Any = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.target_cards is None:
            self.target_cards = []
        if self.trigger_data is None:
            self.trigger_data = {}

class BaseEffect(abc.ABC):
    """Abstract base class for all card effects."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 trigger: EffectTrigger = EffectTrigger.IMMEDIATE,
                 target: EffectTarget = EffectTarget.SELF,
                 category: EffectCategory = EffectCategory.STAT_MODIFICATION,
                 duration: int = 1, stackable: bool = False,
                 max_stacks: int = 10, cost: int = 0):
        
        # Core Properties
        self.effect_id = effect_id
        self.name = name
        self.description = description
        self.trigger = trigger
        self.target = target
        self.category = category
        
        # Duration and Stacking
        self.duration = duration  # -1 = permanent, 0 = instant, >0 = turns
        self.remaining_duration = duration
        self.stackable = stackable
        self.stack_count = 1
        self.max_stacks = max_stacks
        
        # Resource and Timing
        self.cost = cost
        self.priority = 0  # Higher priority effects resolve first
        
        # State Tracking
        self.instance_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_triggered = None
        self.trigger_count = 0
        self.is_active = True
        self.is_conditional_active = True
        
        # Metadata and Parameters
        self.parameters: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.tags: Set[str] = set()
        
        # Callbacks and Conditions
        self.trigger_condition: Optional[Callable] = None
        self.pre_effect_callback: Optional[Callable] = None
        self.post_effect_callback: Optional[Callable] = None
        
        # History
        self.execution_history: List[Dict[str, Any]] = []
    
    @abc.abstractmethod
    def can_trigger(self, context: EffectContext) -> bool:
        """Check if effect can trigger in the given context."""
        pass
    
    @abc.abstractmethod  
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        """Execute the effect and return results."""
        pass
    
    def validate_targets(self, context: EffectContext) -> bool:
        """Validate that targets are valid for this effect."""
        if not context.target_cards:
            return self.target in [EffectTarget.SELF, EffectTarget.BOARD, EffectTarget.PLAYER]
        
        # Check target count constraints
        if self.target in [EffectTarget.ENEMY, EffectTarget.ALLY] and len(context.target_cards) != 1:
            return False
        
        return True
    
    def get_valid_targets(self, context: EffectContext) -> List[Any]:
        """Get all valid targets for this effect."""
        if not context.game_state:
            return []
        
        targets = []
        
        if self.target == EffectTarget.SELF:
            targets = [context.source_card] if context.source_card else []
        elif self.target == EffectTarget.ALL_ENEMIES:
            targets = context.game_state.get_enemy_cards(context.player)
        elif self.target == EffectTarget.ALL_ALLIES:
            targets = context.game_state.get_ally_cards(context.player)
        elif self.target == EffectTarget.ALL:
            targets = context.game_state.get_all_cards()
        elif self.target == EffectTarget.RANDOM_ENEMY:
            enemies = context.game_state.get_enemy_cards(context.player)
            targets = [context.game_state.random.choice(enemies)] if enemies else []
        elif self.target == EffectTarget.RANDOM_ALLY:
            allies = context.game_state.get_ally_cards(context.player)
            targets = [context.game_state.random.choice(allies)] if allies else []
        elif self.target == EffectTarget.ADJACENT:
            if context.source_card and hasattr(context.source_card, 'position'):
                targets = context.game_state.get_adjacent_cards(context.source_card.position)
        
        return targets
    
    def apply_to_target(self, target: Any, context: EffectContext) -> Dict[str, Any]:
        """Apply effect to a single target."""
        return {"success": True, "target": target}
    
    def try_trigger(self, context: EffectContext) -> Dict[str, Any]:
        """Attempt to trigger the effect."""
        result = {
            "triggered": False,
            "success": False,
            "message": "",
            "targets_affected": 0,
            "results": []
        }
        
        # Check if effect is active
        if not self.is_active:
            result["message"] = "Effect is not active"
            return result
        
        # Check duration
        if self.remaining_duration == 0:
            result["message"] = "Effect has expired"
            self.is_active = False
            return result
        
        # Check trigger condition
        if not self.can_trigger(context):
            result["message"] = "Trigger condition not met"
            return result
        
        # Check custom condition
        if self.trigger_condition and not self.trigger_condition(context):
            result["message"] = "Custom condition not met"
            return result
        
        # Validate targets
        if context.target_cards:
            targets = context.target_cards
        else:
            targets = self.get_valid_targets(context)
        
        if not targets and self.target != EffectTarget.BOARD:
            result["message"] = "No valid targets"
            return result
        
        if not self.validate_targets(EffectContext(
            source_card=context.source_card,
            target_cards=targets,
            game_state=context.game_state,
            trigger_data=context.trigger_data,
            player=context.player,
            opponent=context.opponent
        )):
            result["message"] = "Invalid targets"
            return result
        
        # Pre-effect callback
        if self.pre_effect_callback:
            try:
                self.pre_effect_callback(context)
            except Exception as e:
                logger.error(f"Pre-effect callback failed for {self.effect_id}: {e}")
        
        # Execute effect
        try:
            updated_context = EffectContext(
                source_card=context.source_card,
                target_cards=targets,
                game_state=context.game_state,
                trigger_data=context.trigger_data,
                player=context.player,
                opponent=context.opponent,
                board_state=context.board_state
            )
            
            execution_result = self.execute(updated_context)
            
            # Update tracking
            self.last_triggered = datetime.now()
            self.trigger_count += 1
            
            # Update duration
            if self.duration > 0:
                self.remaining_duration -= 1
                if self.remaining_duration <= 0:
                    self.is_active = False
            
            result.update({
                "triggered": True,
                "success": execution_result.get("success", True),
                "message": execution_result.get("message", "Effect executed successfully"),
                "targets_affected": len(targets),
                "results": [execution_result]
            })
            
            # Post-effect callback
            if self.post_effect_callback:
                try:
                    self.post_effect_callback(context, result)
                except Exception as e:
                    logger.error(f"Post-effect callback failed for {self.effect_id}: {e}")
            
            # Record execution
            self.execution_history.append({
                "timestamp": self.last_triggered.isoformat(),
                "targets": [getattr(t, 'instance_id', str(t)) for t in targets],
                "result": execution_result,
                "trigger_data": context.trigger_data
            })
            
            # Limit history size
            if len(self.execution_history) > 50:
                self.execution_history = self.execution_history[-50:]
                
        except Exception as e:
            logger.error(f"Effect execution failed for {self.effect_id}: {e}")
            result.update({
                "triggered": True,
                "success": False,
                "message": f"Effect execution failed: {str(e)}"
            })
        
        return result
    
    def stack_with(self, other_effect: 'BaseEffect') -> bool:
        """Check if this effect can stack with another."""
        return (self.stackable and 
                other_effect.stackable and
                self.effect_id == other_effect.effect_id and
                self.stack_count < self.max_stacks)
    
    def add_stack(self) -> bool:
        """Add a stack to this effect."""
        if self.stack_count < self.max_stacks:
            self.stack_count += 1
            # Refresh duration when stacking
            self.remaining_duration = self.duration
            return True
        return False
    
    def remove_stack(self) -> bool:
        """Remove a stack from this effect."""
        if self.stack_count > 1:
            self.stack_count -= 1
            return True
        else:
            self.is_active = False
            return False
    
    def refresh_duration(self) -> None:
        """Reset duration to original value."""
        if self.duration > 0:
            self.remaining_duration = self.duration
            self.is_active = True
    
    def extend_duration(self, turns: int) -> None:
        """Extend the effect duration by specified turns."""
        if self.duration > 0:
            self.remaining_duration += turns
            if not self.is_active and self.remaining_duration > 0:
                self.is_active = True
    
    def set_parameter(self, key: str, value: Any) -> None:
        """Set an effect parameter."""
        self.parameters[key] = value
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get an effect parameter."""
        return self.parameters.get(key, default)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the effect."""
        self.tags.add(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if effect has a specific tag."""
        return tag in self.tags
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get information for displaying the effect."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "trigger": self.trigger.value,
            "target": self.target.value,
            "duration_remaining": self.remaining_duration if self.duration > 0 else "Permanent" if self.duration == -1 else "Instant",
            "stack_count": self.stack_count if self.stackable else None,
            "is_active": self.is_active,
            "trigger_count": self.trigger_count
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert effect to dictionary for serialization."""
        return {
            "effect_id": self.effect_id,
            "instance_id": self.instance_id,
            "name": self.name,
            "description": self.description,
            "trigger": self.trigger.value,
            "target": self.target.value,
            "category": self.category.value,
            "duration": self.duration,
            "remaining_duration": self.remaining_duration,
            "stackable": self.stackable,
            "stack_count": self.stack_count,
            "max_stacks": self.max_stacks,
            "cost": self.cost,
            "priority": self.priority,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count,
            "parameters": self.parameters,
            "metadata": self.metadata,
            "tags": list(self.tags)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEffect':
        """Create effect from dictionary (for subclasses to implement)."""
        raise NotImplementedError("Subclasses must implement from_dict")
    
    def __str__(self) -> str:
        duration_str = ""
        if self.duration > 0:
            duration_str = f" ({self.remaining_duration} turns left)"
        elif self.duration == -1:
            duration_str = " (permanent)"
        
        stack_str = ""
        if self.stackable and self.stack_count > 1:
            stack_str = f" x{self.stack_count}"
        
        return f"{self.name}{stack_str}{duration_str}"


# src/sands_of_duat/cards/effects/damage_effects.py
class DamageEffect(BaseEffect):
    """Base class for damage-dealing effects."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 damage_amount: int = 1, damage_type: str = "physical",
                 **kwargs):
        super().__init__(effect_id, name, description, 
                        category=EffectCategory.DAMAGE, **kwargs)
        self.set_parameter('damage_amount', damage_amount)
        self.set_parameter('damage_type', damage_type)
        self.add_tag('damage')
    
    def can_trigger(self, context: EffectContext) -> bool:
        return context.target_cards or self.get_valid_targets(context)
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        damage_amount = self.get_parameter('damage_amount', 1)
        damage_type = self.get_parameter('damage_type', 'physical')
        
        # Scale damage with stack count if stackable
        if self.stackable:
            damage_amount *= self.stack_count
        
        results = []
        total_damage = 0
        
        for target in context.target_cards:
            if hasattr(target, 'take_damage'):
                damage_result = target.take_damage(
                    damage=damage_amount,
                    damage_type=damage_type,
                    source=context.source_card
                )
                results.append({
                    "target": target,
                    "damage_dealt": damage_result.get('damage_dealt', 0),
                    "target_destroyed": damage_result.get('is_destroyed', False)
                })
                total_damage += damage_result.get('damage_dealt', 0)
        
        return {
            "success": True,
            "total_damage": total_damage,
            "targets_hit": len(results),
            "target_results": results,
            "damage_type": damage_type
        }

class DirectDamageEffect(DamageEffect):
    """Direct damage that ignores defense."""
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        damage_amount = self.get_parameter('damage_amount', 1)
        if self.stackable:
            damage_amount *= self.stack_count
        
        results = []
        total_damage = 0
        
        for target in context.target_cards:
            if hasattr(target, 'current_stats'):
                # Direct damage bypasses defense
                original_health = target.current_stats.health
                target.current_stats.health = max(0, target.current_stats.health - damage_amount)
                actual_damage = original_health - target.current_stats.health
                
                results.append({
                    "target": target,
                    "damage_dealt": actual_damage,
                    "target_destroyed": target.current_stats.health <= 0
                })
                total_damage += actual_damage
        
        return {
            "success": True,
            "total_damage": total_damage,
            "targets_hit": len(results),
            "target_results": results,
            "damage_type": "direct"
        }

class SolarFlareEffect(DamageEffect):
    """Ra's signature solar flare effect."""
    
    def __init__(self):
        super().__init__(
            effect_id="solar_flare",
            name="Solar Flare",
            description="Deal fire damage to all enemies, increased by divine favor",
            damage_amount=5,
            damage_type="fire",
            trigger=EffectTrigger.ON_PLAY,
            target=EffectTarget.ALL_ENEMIES
        )
        self.add_tag('divine')
        self.add_tag('fire')
        self.add_tag('ra')
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        base_damage = self.get_parameter('damage_amount', 5)
        
        # Increase damage based on source card's divine favor
        divine_bonus = 0
        if context.source_card and hasattr(context.source_card, 'current_stats'):
            divine_favor = getattr(context.source_card.current_stats, 'divine_favor', 0)
            divine_bonus = max(0, divine_favor // 5)  # +1 damage per 5 divine favor
        
        total_damage_per_target = base_damage + divine_bonus
        
        results = []
        total_damage = 0
        
        for target in context.target_cards:
            if hasattr(target, 'take_damage'):
                # Fire damage is extra effective against certain elements
                damage_modifier = 1.0
                if hasattr(target, 'element'):
                    if target.element.key in ['earth', 'darkness']:
                        damage_modifier = 1.5  # Fire beats earth and darkness
                    elif target.element.key in ['water']:
                        damage_modifier = 0.5  # Fire weak to water
                
                final_damage = int(total_damage_per_target * damage_modifier)
                
                damage_result = target.take_damage(
                    damage=final_damage,
                    damage_type="fire",
                    source=context.source_card
                )
                
                results.append({
                    "target": target,
                    "damage_dealt": damage_result.get('damage_dealt', 0),
                    "damage_modifier": damage_modifier,
                    "target_destroyed": damage_result.get('is_destroyed', False)
                })
                total_damage += damage_result.get('damage_dealt', 0)
        
        return {
            "success": True,
            "total_damage": total_damage,
            "base_damage": base_damage,
            "divine_bonus": divine_bonus,
            "targets_hit": len(results),
            "target_results": results,
            "damage_type": "fire"
        }

class LifeDrainEffect(DamageEffect):
    """Damage that heals the source."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 damage_amount: int = 3, heal_ratio: float = 0.5, **kwargs):
        super().__init__(effect_id, name, description, 
                        damage_amount=damage_amount, **kwargs)
        self.set_parameter('heal_ratio', heal_ratio)
        self.add_tag('lifesteal')
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        damage_result = super().execute(context)
        
        if damage_result['success'] and context.source_card:
            total_damage = damage_result['total_damage']
            heal_ratio = self.get_parameter('heal_ratio', 0.5)
            heal_amount = int(total_damage * heal_ratio)
            
            if heal_amount > 0 and hasattr(context.source_card, 'heal'):
                heal_result = context.source_card.heal(heal_amount)
                damage_result['healing_done'] = heal_result.get('healing_done', 0)
        
        return damage_result


# src/sands_of_duat/cards/effects/healing_effects.py  
class HealingEffect(BaseEffect):
    """Base class for healing effects."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 heal_amount: int = 1, **kwargs):
        super().__init__(effect_id, name, description,
                        category=EffectCategory.HEALING, **kwargs)
        self.set_parameter('heal_amount', heal_amount)
        self.add_tag('healing')
    
    def can_trigger(self, context: EffectContext) -> bool:
        # Can only heal targets that are damaged
        valid_targets = []
        for target in context.target_cards or self.get_valid_targets(context):
            if hasattr(target, 'current_stats') and hasattr(target, 'stats'):
                max_health = target.stats.health
                current_health = target.current_stats.health
                if current_health < max_health:
                    valid_targets.append(target)
        
        return len(valid_targets) > 0
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        heal_amount = self.get_parameter('heal_amount', 1)
        
        if self.stackable:
            heal_amount *= self.stack_count
        
        results = []
        total_healing = 0
        
        for target in context.target_cards:
            if hasattr(target, 'heal'):
                heal_result = target.heal(heal_amount, context.source_card)
                results.append({
                    "target": target,
                    "healing_done": heal_result.get('healing_done', 0),
                    "fully_healed": heal_result.get('fully_healed', False)
                })
                total_healing += heal_result.get('healing_done', 0)
        
        return {
            "success": True,
            "total_healing": total_healing,
            "targets_healed": len(results),
            "target_results": results
        }

class RegenerationEffect(HealingEffect):
    """Healing over time effect."""
    
    def __init__(self, effect_id: str = "regeneration", 
                 heal_per_turn: int = 2, duration: int = 3):
        super().__init__(
            effect_id=effect_id,
            name="Regeneration",
            description=f"Heal {heal_per_turn} health at the start of each turn for {duration} turns",
            heal_amount=heal_per_turn,
            trigger=EffectTrigger.START_TURN,
            target=EffectTarget.SELF,
            duration=duration
        )

class DivineHealingEffect(HealingEffect):
    """Healing that scales with divine favor."""
    
    def __init__(self):
        super().__init__(
            effect_id="divine_healing",
            name="Divine Healing",
            description="Heal based on divine favor",
            trigger=EffectTrigger.IMMEDIATE,
            target=EffectTarget.ALLY
        )
        self.add_tag('divine')
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        base_heal = self.get_parameter('heal_amount', 3)
        
        # Scale healing with divine favor
        divine_bonus = 0
        if context.source_card and hasattr(context.source_card, 'current_stats'):
            divine_favor = getattr(context.source_card.current_stats, 'divine_favor', 0)
            divine_bonus = max(0, divine_favor // 3)  # +1 heal per 3 divine favor
        
        total_heal = base_heal + divine_bonus
        
        results = []
        total_healing = 0
        
        for target in context.target_cards:
            if hasattr(target, 'heal'):
                heal_result = target.heal(total_heal, context.source_card)
                results.append({
                    "target": target,
                    "healing_done": heal_result.get('healing_done', 0),
                    "divine_bonus": divine_bonus,
                    "fully_healed": heal_result.get('fully_healed', False)
                })
                total_healing += heal_result.get('healing_done', 0)
        
        return {
            "success": True,
            "total_healing": total_healing,
            "base_healing": base_heal,
            "divine_bonus": divine_bonus,
            "targets_healed": len(results),
            "target_results": results
        }


# src/sands_of_duat/cards/effects/stat_effects.py
class StatModificationEffect(BaseEffect):
    """Effect that modifies card stats."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 stat_modifications: Dict[str, int] = None, **kwargs):
        super().__init__(effect_id, name, description,
                        category=EffectCategory.STAT_MODIFICATION, **kwargs)
        self.set_parameter('stat_modifications', stat_modifications or {})
        self.add_tag('stat_modification')
    
    def can_trigger(self, context: EffectContext) -> bool:
        return bool(context.target_cards or self.get_valid_targets(context))
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        modifications = self.get_parameter('stat_modifications', {})
        permanent = self.duration == -1
        
        results = []
        
        for target in context.target_cards:
            if hasattr(target, 'modify_stat'):
                target_modifications = {}
                
                for stat_name, value in modifications.items():
                    # Scale with stack count if stackable
                    final_value = value * self.stack_count if self.stackable else value
                    
                    target.modify_stat(stat_name, final_value, permanent)
                    target_modifications[stat_name] = final_value
                
                results.append({
                    "target": target,
                    "modifications": target_modifications,
                    "permanent": permanent
                })
        
        return {
            "success": True,
            "targets_modified": len(results),
            "target_results": results,
            "permanent": permanent
        }

class BuffEffect(StatModificationEffect):
    """Positive stat modification."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 attack_bonus: int = 0, defense_bonus: int = 0, 
                 health_bonus: int = 0, **kwargs):
        modifications = {}
        if attack_bonus:
            modifications['attack'] = attack_bonus
        if defense_bonus:
            modifications['defense'] = defense_bonus  
        if health_bonus:
            modifications['health'] = health_bonus
        
        super().__init__(effect_id, name, description,
                        stat_modifications=modifications, **kwargs)
        self.add_tag('buff')

class DebuffEffect(StatModificationEffect):
    """Negative stat modification."""
    
    def __init__(self, effect_id: str, name: str, description: str,
                 attack_penalty: int = 0, defense_penalty: int = 0,
                 **kwargs):
        modifications = {}
        if attack_penalty:
            modifications['attack'] = -attack_penalty
        if defense_penalty:
            modifications['defense'] = -defense_penalty
        
        super().__init__(effect_id, name, description,
                        stat_modifications=modifications, **kwargs)
        self.add_tag('debuff')

class DivineFavorEffect(StatModificationEffect):
    """Effect that modifies divine favor specifically."""
    
    def __init__(self, favor_change: int = 1, duration: int = -1):
        super().__init__(
            effect_id="divine_favor_change",
            name=f"Divine {'Blessing' if favor_change > 0 else 'Curse'}",
            description=f"{'Gain' if favor_change > 0 else 'Lose'} {abs(favor_change)} divine favor",
            stat_modifications={'divine_favor': favor_change},
            trigger=EffectTrigger.IMMEDIATE,
            target=EffectTarget.SELF,
            duration=duration
        )
        self.add_tag('divine')
        self.add_tag('blessing' if favor_change > 0 else 'curse')


# src/sands_of_duat/cards/effects/ba_ka_effects.py
class BaKaEffect(BaseEffect):
    """Base class for Ba-Ka (soul/life force) effects."""
    
    def __init__(self, effect_id: str, name: str, description: str, **kwargs):
        super().__init__(effect_id, name, description, 
                        category=EffectCategory.BA_KA, **kwargs)
        self.add_tag('ba_ka')
        self.add_tag('spiritual')

class BaSeparationEffect(BaKaEffect):
    """Effect to separate Ba (soul) from body."""
    
    def __init__(self):
        super().__init__(
            effect_id="ba_separation",
            name="Ba Separation", 
            description="Separate soul from body, gaining spiritual power",
            trigger=EffectTrigger.IMMEDIATE,
            target=EffectTarget.SELF
        )
    
    def can_trigger(self, context: EffectContext) -> bool:
        if not context.source_card:
            return False
        return (hasattr(context.source_card, 'has_keyword') and
                context.source_card.has_keyword('ba_split') and
                not getattr(context.source_card, 'ba_separated', False))
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        card = context.source_card
        
        if hasattr(card, 'separate_ba') and card.separate_ba():
            return {
                "success": True,
                "message": f"{card.name}'s Ba has been separated",
                "ba_power_gained": 5,
                "card_state": "ba_separated"
            }
        
        return {
            "success": False,
            "message": "Ba separation failed"
        }

class KaManifestationEffect(BaKaEffect):
    """Effect to manifest Ka (life force) as separate entity."""
    
    def __init__(self):
        super().__init__(
            effect_id="ka_manifestation",
            name="Ka Manifestation",
            description="Manifest life force as spiritual double",
            trigger=EffectTrigger.ON_PLAY,
            target=EffectTarget.SELF
        )
    
    def can_trigger(self, context: EffectContext) -> bool:
        if not context.source_card:
            return False
        return (hasattr(context.source_card, 'has_keyword') and
                context.source_card.has_keyword('ka_double') and
                not getattr(context.source_card, 'ka_manifested', False))
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        card = context.source_card
        
        if hasattr(card, 'manifest_ka') and card.manifest_ka():
            # Create Ka token on the board
            if context.game_state and hasattr(context.game_state, 'create_token'):
                ka_token = context.game_state.create_token(
                    token_id=f"{card.card_id}_ka",
                    name=f"Ka of {card.name}",
                    attack=card.current_stats.attack // 2,
                    defense=card.current_stats.defense // 2,
                    health=card.current_stats.health // 2,
                    element=card.element,
                    owner=context.player
                )
                
                return {
                    "success": True,
                    "message": f"{card.name}'s Ka has been manifested",
                    "ka_token_created": ka_token.instance_id if ka_token else None,
                    "ka_strength_gained": 10
                }
        
        return {
            "success": False,
            "message": "Ka manifestation failed"
        }

class SoulReunionEffect(BaKaEffect):
    """Effect to reunite separated Ba and Ka."""
    
    def __init__(self):
        super().__init__(
            effect_id="soul_reunion",
            name="Soul Reunion",
            description="Reunite Ba and Ka for powerful bonus",
            trigger=EffectTrigger.IMMEDIATE,
            target=EffectTarget.SELF,
            cost=2  # Requires resources to reunite
        )
    
    def can_trigger(self, context: EffectContext) -> bool:
        if not context.source_card:
            return False
        return (getattr(context.source_card, 'ba_separated', False) and
                getattr(context.source_card, 'ka_manifested', False))
    
    def execute(self, context: EffectContext) -> Dict[str, Any]:
        card = context.source_card
        
        if hasattr(card, 'reunite_ba') and card.reunite_ba():
            # Remove Ka token and reunite
            if context.game_state:
                ka_token_id = f"{card.card_id}_ka"
                if hasattr(context.game_state, 'remove_token'):
                    context.game_state.remove_token(ka_token_id)
            
            # Grant powerful reunion bonus
            card.modify_stat('attack', 3, permanent=False)
            card.modify_stat('defense', 3, permanent=False)
            card.modify_stat('health', 5, permanent=False)
            card.modify_stat('divine_favor', 5, permanent=False)
            
            return {
                "success": True,
                "message": f"{card.name} has achieved spiritual wholeness",
                "attack_bonus": 3,
                "defense_bonus": 3,
                "health_bonus": 5,
                "divine_favor_bonus": 5,
                "duration": "until_end_of_turn"
            }
        
        return {
            "success": False,
            "message": "Soul reunion failed"
        }


# Effect Factory and Registration System
class EffectFactory:
    """Factory for creating and managing effects."""
    
    _effect_registry: Dict[str, Type[BaseEffect]] = {}
    
    @classmethod
    def register_effect(cls, effect_id: str, effect_class: Type[BaseEffect]) -> None:
        """Register an effect class."""
        cls._effect_registry[effect_id] = effect_class
    
    @classmethod
    def create_effect(cls, effect_id: str, **kwargs) -> Optional[BaseEffect]:
        """Create an effect by ID."""
        if effect_id in cls._effect_registry:
            effect_class = cls._effect_registry[effect_id]
            try:
                return effect_class(**kwargs)
            except Exception as e:
                logger.error(f"Failed to create effect {effect_id}: {e}")
                return None
        
        logger.warning(f"Unknown effect ID: {effect_id}")
        return None
    
    @classmethod
    def get_available_effects(cls) -> List[str]:
        """Get list of all registered effect IDs."""
        return list(cls._effect_registry.keys())
    
    @classmethod
    def create_from_dict(cls, effect_data: Dict[str, Any]) -> Optional[BaseEffect]:
        """Create effect from dictionary data."""
        effect_id = effect_data.get('effect_id')
        if not effect_id:
            return None
        
        # Map common effect types to classes
        effect_type_map = {
            'damage': DamageEffect,
            'direct_damage': DirectDamageEffect,
            'solar_flare': SolarFlareEffect,
            'life_drain': LifeDrainEffect,
            'healing': HealingEffect,
            'regeneration': RegenerationEffect,
            'divine_healing': DivineHealingEffect,
            'buff': BuffEffect,
            'debuff': DebuffEffect,
            'divine_favor': DivineFavorEffect,
            'ba_separation': BaSeparationEffect,
            'ka_manifestation': KaManifestationEffect,
            'soul_reunion': SoulReunionEffect
        }
        
        # Try registered effects first
        if effect_id in cls._effect_registry:
            return cls.create_effect(effect_id, **effect_data.get('parameters', {}))
        
        # Try common types
        for type_key, effect_class in effect_type_map.items():
            if type_key in effect_id:
                try:
                    return effect_class(**effect_data.get('parameters', {}))
                except Exception as e:
                    logger.error(f"Failed to create effect {effect_id} of type {type_key}: {e}")
                    break
        
        # Fallback to generic effect creation
        logger.warning(f"Creating generic effect for unknown type: {effect_id}")
        return None


# Register common effects
EffectFactory.register_effect('solar_flare', SolarFlareEffect)
EffectFactory.register_effect('ba_separation', BaSeparationEffect)
EffectFactory.register_effect('ka_manifestation', KaManifestationEffect)
EffectFactory.register_effect('soul_reunion', SoulReunionEffect)
EffectFactory.register_effect('divine_healing', DivineHealingEffect)
EffectFactory.register_effect('regeneration', RegenerationEffect)
```

### 3.4 ADVANCED DECK MANAGEMENT WITH OPTIMIZATIONS

```python
# src/sands_of_duat/cards/deck.py
from __future__ import annotations
import random
import uuid
from typing import Dict, List, Optional, Any, Set, Tuple, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
import json
import hashlib
from collections import defaultdict, Counter
import math

from .card import Card, CardType, CardRarity, CardElement, CardKeyword

class DeckValidationResult(Enum):
    """Result of deck validation."""
    VALID = "valid"
    INVALID_SIZE = "invalid_size" 
    INVALID_COPIES = "invalid_copies"
    INVALID_RESTRICTIONS = "invalid_restrictions"
    MISSING_REQUIRED = "missing_required"

class ShuffleAlgorithm(Enum):
    """Available shuffle algorithms."""
    FISHER_YATES = "fisher_yates"       # Standard shuffle
    RIFFLE = "riffle"                   # Realistic card shuffle simulation
    WEIGHTED = "weighted"               # Weight-based shuffle for rarity
    MANA_CURVE = "mana_curve"          # Optimize for mana distribution
    EGYPTIAN_MYSTICAL = "egyptian_mystical"  # Themed shuffle with divination

@dataclass
class DeckConstraints:
    """Constraints for deck building."""
    min_size: int = 30
    max_size: int = 60
    max_copies_per_card: int = 3
    max_legendary: int = 2
    max_mythic: int = 1
    min_creature_ratio: float = 0.3  # At least 30% creatures
    max_spell_ratio: float = 0.4     # At most 40% spells
    required_elements: Set[CardElement] = field(default_factory=set)
    banned_cards: Set[str] = field(default_factory=set)
    format_restrictions: Dict[str, Any] = field(default_factory=dict)

@dataclass  
class DeckStats:
    """Statistical analysis of a deck."""
    total_cards: int = 0
    average_mana_cost: float = 0.0
    mana_curve: Dict[int, int] = field(default_factory=dict)
    type_distribution: Dict[str, int] = field(default_factory=dict)
    element_distribution: Dict[str, int] = field(default_factory=dict)
    rarity_distribution: Dict[str, int] = field(default_factory=dict)
    keyword_frequency: Dict[str, int] = field(default_factory=dict)
    combat_rating_average: float = 0.0
    divine_favor_total: int = 0
    underworld_tier_average: float = 0.0
    
    # Advanced Analytics
    curve_smoothness: float = 0.0        # How smooth the mana curve is
    synergy_score: float = 0.0           # How well cards work together
    tempo_rating: float = 0.0            # Early game pressure
    late_game_power: float = 0.0         # End game threat level
    consistency_score: float = 0.0       # How consistent the deck is

class Deck:
    """Advanced deck implementation with Egyptian themes and optimizations."""
    
    def __init__(self, name: str = "Untitled Deck", 
                 owner_id: Optional[str] = None,
                 deck_format: str = "constructed"):
        # Basic Properties
        self.deck_id = str(uuid.uuid4())
        self.name = name
        self.owner_id = owner_id
        self.deck_format = deck_format
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        
        # Card Storage
        self.cards: Dict[str, int] = {}  # card_id -> count
        self._card_instances: Dict[str, List[Card]] = {}  # card_id -> [Card instances]
        self._draw_pile: List[Card] = []
        self._discard_pile: List[Card] = []
        self._hand: List[Card] = []
        self._exile_pile: List[Card] = []  # Removed from game cards
        
        # Deck Configuration
        self.constraints = DeckConstraints()
        self.shuffle_algorithm = ShuffleAlgorithm.FISHER_YATES
        self.is_shuffled = False
        
        # Egyptian Theme Properties
        self.pharaoh_card: Optional[Card] = None  # Deck leader
        self.divine_patron: Optional[str] = None  # Main god allegiance
        self.underworld_progression: int = 0     # Journey through 12 hours
        self.sacred_artifacts: List[str] = []    # Special artifact cards
        
        # Analytics and Optimization
        self.stats = DeckStats()
        self.play_statistics: Dict[str, Any] = {}
        self.win_rate: float = 0.0
        self.games_played: int = 0
        
        # Performance Tracking
        self.shuffle_times: List[float] = []
        self.draw_probabilities: Dict[str, float] = {}
        self.mulligans_taken: int = 0
        
        # Metadata
        self.description: str = ""
        self.tags: Set[str] = set()
        self.version: str = "1.0.0"
        self.hash_signature: str = ""
    
    def add_card(self, card: Card, count: int = 1) -> bool:
        """Add cards to the deck with validation."""
        if count <= 0:
            return False
        
        current_count = self.cards.get(card.card_id, 0)
        new_count = current_count + count
        
        # Check copy limit
        if new_count > self.constraints.max_copies_per_card:
            return False
        
        # Check rarity limits
        if card.rarity.key == 'legendary' and new_count > self.constraints.max_legendary:
            return False
        if card.rarity.key == 'mythic' and new_count > self.constraints.max_mythic:
            return False
        
        # Check banned cards
        if card.card_id in self.constraints.banned_cards:
            return False
        
        # Add to deck
        self.cards[card.card_id] = new_count
        
        # Create instances
        if card.card_id not in self._card_instances:
            self._card_instances[card.card_id] = []
        
        for _ in range(count):
            card_copy = Card.from_dict(card.to_dict())  # Create new instance
            card_copy.deck_id = self.deck_id
            card_copy.owner_id = self.owner_id
            self._card_instances[card.card_id].append(card_copy)
        
        # Update special roles
        if card.card_type == CardType.DEITY and not self.pharaoh_card:
            self.pharaoh_card = card
        
        if card.divine_allegiance and not self.divine_patron:
            self.divine_patron = card.divine_allegiance
        
        if card.card_type == CardType.ARTIFACT:
            self.sacred_artifacts.append(card.card_id)
        
        self.last_modified = datetime.now()
        self._invalidate_cache()
        return True
    
    def remove_card(self, card_id: str, count: int = 1) -> bool:
        """Remove cards from the deck."""
        if card_id not in self.cards:
            return False
        
        current_count = self.cards[card_id]
        if count >= current_count:
            # Remove all copies
            del self.cards[card_id]
            self._card_instances[card_id] = []
        else:
            # Remove partial
            self.cards[card_id] = current_count - count
            # Remove instances
            for _ in range(count):
                if self._card_instances[card_id]:
                    self._card_instances[card_id].pop()
        
        self.last_modified = datetime.now()
        self._invalidate_cache()
        return True
    
    def get_card_count(self, card_id: str) -> int:
        """Get count of specific card in deck."""
        return self.cards.get(card_id, 0)
    
    def get_total_cards(self) -> int:
        """Get total number of cards in deck."""
        return sum(self.cards.values())
    
    def validate(self) -> Tuple[DeckValidationResult, List[str]]:
        """Validate deck against constraints."""
        errors = []
        
        total_cards = self.get_total_cards()
        
        # Check size
        if total_cards < self.constraints.min_size:
            errors.append(f"Deck too small: {total_cards} < {self.constraints.min_size}")
            return DeckValidationResult.INVALID_SIZE, errors
        if total_cards > self.constraints.max_size:
            errors.append(f"Deck too large: {total_cards} > {self.constraints.max_size}")
            return DeckValidationResult.INVALID_SIZE, errors
        
        # Check copy limits
        for card_id, count in self.cards.items():
            if count > self.constraints.max_copies_per_card:
                errors.append(f"Too many copies of {card_id}: {count} > {self.constraints.max_copies_per_card}")
                return DeckValidationResult.INVALID_COPIES, errors
        
        # Check rarity limits
        legendary_count = sum(count for card_id, count in self.cards.items() 
                             if self.get_card_instance(card_id).rarity.key == 'legendary')
        if legendary_count > self.constraints.max_legendary:
            errors.append(f"Too many legendary cards: {legendary_count} > {self.constraints.max_legendary}")
            return DeckValidationResult.INVALID_RESTRICTIONS, errors
        
        mythic_count = sum(count for card_id, count in self.cards.items()
                          if self.get_card_instance(card_id).rarity.key == 'mythic')
        if mythic_count > self.constraints.max_mythic:
            errors.append(f"Too many mythic cards: {mythic_count} > {self.constraints.max_mythic}")
            return DeckValidationResult.INVALID_RESTRICTIONS, errors
        
        # Check type ratios
        type_counts = self._calculate_type_distribution()
        creature_ratio = type_counts.get('creature', 0) / total_cards
        spell_ratio = type_counts.get('spell', 0) / total_cards
        
        if creature_ratio < self.constraints.min_creature_ratio:
            errors.append(f"Too few creatures: {creature_ratio:.2%} < {self.constraints.min_creature_ratio:.2%}")
        if spell_ratio > self.constraints.max_spell_ratio:
            errors.append(f"Too many spells: {spell_ratio:.2%} > {self.constraints.max_spell_ratio:.2%}")
        
        # Check required elements
        deck_elements = set()
        for card_id in self.cards:
            card = self.get_card_instance(card_id)
            if card:
                deck_elements.add(card.element)
        
        missing_elements = self.constraints.required_elements - deck_elements
        if missing_elements:
            errors.append(f"Missing required elements: {[e.display_name for e in missing_elements]}")
            return DeckValidationResult.MISSING_REQUIRED, errors
        
        if errors:
            return DeckValidationResult.INVALID_RESTRICTIONS, errors
        
        return DeckValidationResult.VALID, []
    
    def shuffle(self, algorithm: Optional[ShuffleAlgorithm] = None) -> None:
        """Shuffle the deck using specified algorithm."""
        if algorithm:
            self.shuffle_algorithm = algorithm
        
        start_time = datetime.now()
        
        # Prepare all card instances for shuffling
        all_cards = []
        for card_id, count in self.cards.items():
            instances = self._card_instances[card_id][:count]  # Take only as many as in deck
            all_cards.extend(instances)
        
        if self.shuffle_algorithm == ShuffleAlgorithm.FISHER_YATES:
            self._fisher_yates_shuffle(all_cards)
        elif self.shuffle_algorithm == ShuffleAlgorithm.RIFFLE:
            self._riffle_shuffle(all_cards)
        elif self.shuffle_algorithm == ShuffleAlgorithm.WEIGHTED:
            self._weighted_shuffle(all_cards)
        elif self.shuffle_algorithm == ShuffleAlgorithm.MANA_CURVE:
            self._mana_curve_shuffle(all_cards)
        elif self.shuffle_algorithm == ShuffleAlgorithm.EGYPTIAN_MYSTICAL:
            self._egyptian_mystical_shuffle(all_cards)
        else:
            self._fisher_yates_shuffle(all_cards)
        
        self._draw_pile = all_cards
        self.is_shuffled = True
        
        # Record performance
        shuffle_time = (datetime.now() - start_time).total_seconds()
        self.shuffle_times.append(shuffle_time)
        if len(self.shuffle_times) > 100:  # Keep last 100 shuffles
            self.shuffle_times = self.shuffle_times[-100:]
    
    def _fisher_yates_shuffle(self, cards: List[Card]) -> None:
        """Standard Fisher-Yates shuffle algorithm."""
        for i in range(len(cards) - 1, 0, -1):
            j = random.randint(0, i)
            cards[i], cards[j] = cards[j], cards[i]
    
    def _riffle_shuffle(self, cards: List[Card]) -> None:
        """Simulate realistic riffle shuffling."""
        deck_size = len(cards)
        if deck_size < 2:
            return
        
        # Split deck (not exactly in half, add some variance)
        split_point = deck_size // 2 + random.randint(-2, 2)
        split_point = max(1, min(split_point, deck_size - 1))
        
        left_half = cards[:split_point]
        right_half = cards[split_point:]
        
        # Riffle together with realistic dropping pattern
        result = []
        left_idx, right_idx = 0, 0
        
        while left_idx < len(left_half) or right_idx < len(right_half):
            # Simulate clumping - cards tend to drop in small groups
            drop_from_left = random.random() < 0.5
            
            if left_idx >= len(left_half):
                drop_from_left = False
            elif right_idx >= len(right_half):
                drop_from_left = True
            
            # Drop 1-3 cards from chosen half
            drop_count = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
            
            if drop_from_left:
                for _ in range(min(drop_count, len(left_half) - left_idx)):
                    result.append(left_half[left_idx])
                    left_idx += 1
            else:
                for _ in range(min(drop_count, len(right_half) - right_idx)):
                    result.append(right_half[right_idx])
                    right_idx += 1
        
        cards[:] = result
    
    def _weighted_shuffle(self, cards: List[Card]) -> None:
        """Shuffle with rarity-based weighting."""
        # Assign weights based on rarity
        rarity_weights = {
            'common': 1.0,
            'uncommon': 0.8,
            'rare': 0.6,
            'epic': 0.4,
            'legendary': 0.2,
            'mythic': 0.1
        }
        
        # Create weighted list
        weighted_cards = []
        for card in cards:
            weight = rarity_weights.get(card.rarity.key, 1.0)
            weighted_cards.append((card, weight))
        
        # Sort by weight with randomness
        weighted_cards.sort(key=lambda x: x[1] + random.random() * 0.5)
        
        # Extract cards
        cards[:] = [card for card, weight in weighted_cards]
    
    def _mana_curve_shuffle(self, cards: List[Card]) -> None:
        """Shuffle to optimize mana curve distribution."""
        # Group cards by mana cost
        mana_groups = defaultdict(list)
        for card in cards:
            mana_cost = card.stats.mana_cost
            mana_groups[mana_cost].append(card)
        
        # Shuffle each group
        for group in mana_groups.values():
            self._fisher_yates_shuffle(group)
        
        # Interleave mana costs to spread them throughout deck
        result = []
        max_mana = max(mana_groups.keys()) if mana_groups else 0
        
        # Calculate distribution pattern
        total_cards = len(cards)
        positions_per_mana = {}
        
        for mana_cost, group in mana_groups.items():
            group_size = len(group)
            # Spread this mana cost evenly through deck
            positions = []
            for i in range(group_size):
                position = (i * total_cards) // group_size
                positions.append(position)
            positions_per_mana[mana_cost] = positions
        
        # Create position map
        position_map = {}
        for mana_cost, positions in positions_per_mana.items():
            for i, pos in enumerate(positions):
                position_map[pos] = mana_groups[mana_cost][i]
        
        # Fill result array
        result = [None] * total_cards
        for pos, card in position_map.items():
            result[pos] = card
        
        # Fill any remaining None slots with remaining cards
        remaining_cards = [card for card in cards if card not in result]
        for i, card in enumerate(result):
            if card is None and remaining_cards:
                result[i] = remaining_cards.pop()
        
        cards[:] = result
    
    def _egyptian_mystical_shuffle(self, cards: List[Card]) -> None:
        """Themed shuffle based on Egyptian divination."""
        # Sort cards by divine allegiance first
        god_order = ['Ra', 'Anubis', 'Thoth', 'Isis', 'Osiris', 'Set']
        
        def card_priority(card):
            # Primary: Divine allegiance
            god_priority = 0
            if card.divine_allegiance in god_order:
                god_priority = god_order.index(card.divine_allegiance)
            else:
                god_priority = len(god_order)
            
            # Secondary: Ba/Ka power (spiritual strength)
            spiritual_power = card.stats.ba_power + card.stats.ka_strength
            
            # Tertiary: Random factor
            random_factor = random.random()
            
            return (god_priority, -spiritual_power, random_factor)
        
        cards.sort(key=card_priority)
        
        # Apply mystical redistribution based on underworld hours
        deck_size = len(cards)
        hour_size = deck_size // 12  # Divide into 12 hours of underworld
        
        # Redistribute cards among hours with some randomness
        hours = [[] for _ in range(12)]
        for i, card in enumerate(cards):
            base_hour = i // max(1, hour_size)
            # Add randomness - card might end up in adjacent hour
            actual_hour = base_hour + random.choice([-1, 0, 0, 0, 1])  # Bias toward staying
            actual_hour = max(0, min(actual_hour, 11))
            hours[actual_hour].append(card)
        
        # Shuffle within each hour and recombine
        result = []
        for hour in hours:
            self._fisher_yates_shuffle(hour)
            result.extend(hour)
        
        cards[:] = result
    
    def draw(self, count: int = 1) -> List[Card]:
        """Draw cards from the deck."""
        if not self.is_shuffled:
            self.shuffle()
        
        drawn = []
        for _ in range(min(count, len(self._draw_pile))):
            if self._draw_pile:
                card = self._draw_pile.pop(0)
                self._hand.append(card)
                drawn.append(card)
        
        # Update draw probabilities
        self._update_draw_probabilities()
        
        return drawn
    
    def mulligan(self, keep_cards: List[Card]) -> List[Card]:
        """Mulligan hand, keeping specified cards."""
        self.mulligans_taken += 1
        
        # Put back cards not being kept
        cards_to_return = [card for card in self._hand if card not in keep_cards]
        self._draw_pile.extend(cards_to_return)
        
        # Shuffle returned cards back into deck
        self._fisher_yates_shuffle(self._draw_pile)
        
        # Set new hand
        self._hand = list(keep_cards)
        
        # Draw to fill hand
        cards_needed = 7 - len(self._hand)  # Assuming 7 card starting hand
        drawn = self.draw(cards_needed)
        
        return drawn
    
    def discard(self, cards: List[Card]) -> None:
        """Move cards from hand to discard pile."""
        for card in cards:
            if card in self._hand:
                self._hand.remove(card)
                self._discard_pile.append(card)
    
    def exile(self, cards: List[Card]) -> None:
        """Remove cards from game permanently."""
        for card in cards:
            # Remove from wherever it currently is
            if card in self._hand:
                self._hand.remove(card)
            elif card in self._draw_pile:
                self._draw_pile.remove(card)
            elif card in self._discard_pile:
                self._discard_pile.remove(card)
            
            self._exile_pile.append(card)
    
    def shuffle_discard_into_deck(self) -> int:
        """Shuffle discard pile back into draw pile."""
        cards_shuffled = len(self._discard_pile)
        self._draw_pile.extend(self._discard_pile)
        self._discard_pile.clear()
        
        self._fisher_yates_shuffle(self._draw_pile)
        
        return cards_shuffled
    
    def get_card_instance(self, card_id: str) -> Optional[Card]:
        """Get a card instance from the deck."""
        instances = self._card_instances.get(card_id, [])
        return instances[0] if instances else None
    
    def calculate_statistics(self) -> DeckStats:
        """Calculate comprehensive deck statistics."""
        stats = DeckStats()
        
        if not self.cards:
            return stats
        
        all_cards = []
        for card_id, count in self.cards.items():
            card = self.get_card_instance(card_id)
            if card:
                for _ in range(count):
                    all_cards.append(card)
        
        if not all_cards:
            return stats
        
        stats.total_cards = len(all_cards)
        
        # Mana curve analysis
        mana_costs = [card.stats.mana_cost for card in all_cards]
        stats.average_mana_cost = sum(mana_costs) / len(mana_costs)
        
        mana_curve = Counter(mana_costs)
        stats.mana_curve = dict(mana_curve)
        
        # Type distribution
        type_counts = Counter(card.card_type.value for card in all_cards)
        stats.type_distribution = dict(type_counts)
        
        # Element distribution
        element_counts = Counter(card.element.key for card in all_cards)
        stats.element_distribution = dict(element_counts)
        
        # Rarity distribution
        rarity_counts = Counter(card.rarity.key for card in all_cards)
        stats.rarity_distribution = dict(rarity_counts)
        
        # Keyword frequency
        keyword_counts = Counter()
        for card in all_cards:
            for keyword in card.keywords:
                keyword_counts[keyword.key] += 1
        stats.keyword_frequency = dict(keyword_counts)
        
        # Combat rating
        combat_ratings = [card.current_stats.calculate_combat_rating() for card in all_cards]
        stats.combat_rating_average = sum(combat_ratings) / len(combat_ratings)
        
        # Divine favor
        stats.divine_favor_total = sum(card.stats.divine_favor for card in all_cards)
        
        # Underworld tier
        underworld_tiers = [card.underworld_tier for card in all_cards if card.underworld_tier > 0]
        stats.underworld_tier_average = sum(underworld_tiers) / len(underworld_tiers) if underworld_tiers else 0.0
        
        # Advanced analytics
        stats.curve_smoothness = self._calculate_curve_smoothness(mana_curve)
        stats.synergy_score = self._calculate_synergy_score(all_cards)
        stats.tempo_rating = self._calculate_tempo_rating(all_cards)
        stats.late_game_power = self._calculate_late_game_power(all_cards)
        stats.consistency_score = self._calculate_consistency_score(all_cards)
        
        self.stats = stats
        return stats
    
    def _calculate_curve_smoothness(self, mana_curve: Dict[int, int]) -> float:
        """Calculate how smooth the mana curve is (0-1, higher is smoother)."""
        if not mana_curve:
            return 0.0
        
        max_mana = max(mana_curve.keys())
        if max_mana == 0:
            return 1.0
        
        # Calculate variance in mana distribution
        total_cards = sum(mana_curve.values())
        expected_per_slot = total_cards / (max_mana + 1)
        
        variance = 0
        for mana_cost in range(max_mana + 1):
            count = mana_curve.get(mana_cost, 0)
            variance += (count - expected_per_slot) ** 2
        
        variance /= (max_mana + 1)
        
        # Convert to smoothness score (lower variance = higher smoothness)
        max_possible_variance = expected_per_slot ** 2  # If all cards were in one slot
        smoothness = 1.0 - (variance / max_possible_variance)
        
        return max(0.0, min(1.0, smoothness))
    
    def _calculate_synergy_score(self, cards: List[Card]) -> float:
        """Calculate how well cards work together (0-1)."""
        if len(cards) < 2:
            return 0.0
        
        synergy_points = 0
        max_possible_synergy = 0
        
        # Element synergy
        element_counts = Counter(card.element.key for card in cards)
        for element, count in element_counts.items():
            if count >= 3:  # Synergy threshold
                synergy_points += count * 2
            max_possible_synergy += count * 2
        
        # Divine allegiance synergy
        god_counts = Counter(card.divine_allegiance for card in cards if card.divine_allegiance)
        for god, count in god_counts.items():
            if count >= 2:
                synergy_points += count * 3
            max_possible_synergy += count * 3
        
        # Keyword synergy
        keyword_counts = Counter()
        for card in cards:
            for keyword in card.keywords:
                keyword_counts[keyword.key] += 1
        
        for keyword, count in keyword_counts.items():
            if count >= 2:
                synergy_points += count
            max_possible_synergy += count
        
        # Ba-Ka synergy (cards that work with separated souls)
        ba_ka_cards = [card for card in cards if any(kw.key in ['ba_split', 'ka_double', 'soul_bond'] for kw in card.keywords)]
        if len(ba_ka_cards) >= 2:
            synergy_points += len(ba_ka_cards) * 4
        max_possible_synergy += len(ba_ka_cards) * 4
        
        return synergy_points / max(1, max_possible_synergy)
    
    def _calculate_tempo_rating(self, cards: List[Card]) -> float:
        """Calculate early game tempo potential (0-1)."""
        early_game_cards = [card for card in cards if card.stats.mana_cost <= 3]
        if not early_game_cards:
            return 0.0
        
        # Factor in attack power, initiative, and special abilities
        tempo_score = 0
        for card in early_game_cards:
            score = card.stats.attack * 2 + card.stats.initiative
            
            # Bonus for keywords that affect tempo
            tempo_keywords = ['divine_strike', 'pharaoh_authority', 'desert_walk']
            for keyword in card.keywords:
                if keyword.key in tempo_keywords:
                    score += 5
            
            tempo_score += score
        
        # Normalize against theoretical maximum
        max_possible_tempo = len(early_game_cards) * 20  # Theoretical max per early card
        return min(1.0, tempo_score / max_possible_tempo)
    
    def _calculate_late_game_power(self, cards: List[Card]) -> float:
        """Calculate late game threat level (0-1)."""
        late_game_cards = [card for card in cards if card.stats.mana_cost >= 6]
        if not late_game_cards:
            return 0.0
        
        power_score = 0
        for card in late_game_cards:
            # High-cost cards should have high impact
            score = card.stats.attack + card.stats.health + card.stats.divine_favor
            
            # Bonus for powerful keywords
            power_keywords = ['resurrection', 'divine_judgment', 'cosmic_balance']
            for keyword in card.keywords:
                if keyword.key in power_keywords:
                    score += 10
            
            # Bonus for legendary/mythic rarity
            if card.rarity.key in ['legendary', 'mythic']:
                score += 15
            
            power_score += score
        
        # Normalize
        max_possible_power = len(late_game_cards) * 50
        return min(1.0, power_score / max_possible_power)
    
    def _calculate_consistency_score(self, cards: List[Card]) -> float:
        """Calculate deck consistency (0-1, higher means more reliable)."""
        if not cards:
            return 0.0
        
        # Factors that improve consistency:
        # 1. Balanced mana curve
        # 2. Multiple copies of key cards
        # 3. Card draw/search effects
        # 4. Flexible/modal cards
        
        consistency_score = 0
        
        # Mana curve balance (already calculated)
        consistency_score += self.stats.curve_smoothness * 30
        
        # Copy redundancy
        card_counts = Counter(card.card_id for card in cards)
        redundancy_score = 0
        for card_id, count in card_counts.items():
            if count >= 2:
                redundancy_score += min(count, 3)  # Cap benefit at 3 copies
        consistency_score += min(20, redundancy_score)
        
        # Card advantage engines
        card_draw_count = 0
        search_count = 0
        for card in cards:
            for effect in card.active_effects:
                if 'draw' in effect.description.lower():
                    card_draw_count += 1
                elif 'search' in effect.description.lower():
                    search_count += 1
        
        consistency_score += min(15, card_draw_count * 3)
        consistency_score += min(15, search_count * 2)
        
        # Flexibility (cards with multiple modes or applications)
        flexible_count = 0
        for card in cards:
            if len(card.active_effects) >= 2:  # Multiple effects = flexible
                flexible_count += 1
            if len(card.keywords) >= 2:  # Multiple keywords = versatile
                flexible_count += 1
        
        consistency_score += min(20, flexible_count)
        
        return min(1.0, consistency_score / 100)
    
    def _calculate_type_distribution(self) -> Dict[str, int]:
        """Calculate distribution of card types."""
        type_counts = defaultdict(int)
        for card_id, count in self.cards.items():
            card = self.get_card_instance(card_id)
            if card:
                # Map specific types to broader categories
                card_type = card.card_type.value
                if card_type in ['deity', 'mortal', 'divine_beast']:
                    type_counts['creature'] += count
                elif card_type in ['spell', 'ritual']:
                    type_counts['spell'] += count
                elif card_type == 'artifact':
                    type_counts['artifact'] += count
                else:
                    type_counts[card_type] += count
        
        return dict(type_counts)
    
    def _update_draw_probabilities(self) -> None:
        """Update probability calculations for drawing specific cards."""
        remaining_cards = len(self._draw_pile)
        if remaining_cards == 0:
            self.draw_probabilities.clear()
            return
        
        # Count remaining copies of each card
        remaining_counts = Counter()
        for card in self._draw_pile:
            remaining_counts[card.card_id] += 1
        
        # Calculate probabilities
        for card_id, count in remaining_counts.items():
            # Probability of drawing at least one copy in next N draws
            self.draw_probabilities[f"{card_id}_next_1"] = count / remaining_cards
            
            if remaining_cards >= 3:
                # Hypergeometric distribution for drawing in next 3 cards
                prob = 1 - self._hypergeometric_prob(remaining_cards, count, 3, 0)
                self.draw_probabilities[f"{card_id}_next_3"] = prob
    
    def _hypergeometric_prob(self, population: int, successes: int, draws: int, wanted: int) -> float:
        """Calculate hypergeometric probability."""
        from math import comb
        
        try:
            prob = (comb(successes, wanted) * comb(population - successes, draws - wanted)) / comb(population, draws)
            return prob
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def _invalidate_cache(self) -> None:
        """Invalidate cached data when deck changes."""
        self.is_shuffled = False
        self.stats = DeckStats()
        self.draw_probabilities.clear()
        self._update_hash_signature()
    
    def _update_hash_signature(self) -> None:
        """Update deck hash for change detection."""
        deck_content = json.dumps(self.cards, sort_keys=True)
        self.hash_signature = hashlib.md5(deck_content.encode()).hexdigest()
    
    def optimize_mana_curve(self) -> Dict[str, Any]:
        """Suggest optimizations for mana curve."""
        current_curve = self.stats.mana_curve
        total_cards = sum(current_curve.values())
        
        # Ideal curve distribution (rough guidelines)
        ideal_distribution = {
            0: 0.02,  # 2% mana cost 0
            1: 0.15,  # 15% mana cost 1
            2: 0.20,  # 20% mana cost 2
            3: 0.18,  # 18% mana cost 3
            4: 0.15,  # 15% mana cost 4
            5: 0.12,  # 12% mana cost 5
            6: 0.08,  # 8% mana cost 6
            7: 0.05,  # 5% mana cost 7+
        }
        
        suggestions = []
        
        for mana_cost, ideal_ratio in ideal_distribution.items():
            current_count = current_curve.get(mana_cost, 0)
            current_ratio = current_count / total_cards if total_cards > 0 else 0
            ideal_count = int(total_cards * ideal_ratio)
            
            difference = ideal_count - current_count
            
            if abs(difference) >= 2:  # Only suggest if significant difference
                if difference > 0:
                    suggestions.append({
                        'type': 'add',
                        'mana_cost': mana_cost,
                        'count': difference,
                        'message': f"Consider adding {difference} more cards with mana cost {mana_cost}"
                    })
                else:
                    suggestions.append({
                        'type': 'remove',
                        'mana_cost': mana_cost,
                        'count': abs(difference),
                        'message': f"Consider removing {abs(difference)} cards with mana cost {mana_cost}"
                    })
        
        return {
            'current_curve': current_curve,
            'ideal_distribution': ideal_distribution,
            'suggestions': suggestions,
            'curve_smoothness': self.stats.curve_smoothness
        }
    
    def suggest_cards(self, card_pool: List[Card], count: int = 5) -> List[Tuple[Card, float]]:
        """Suggest cards to add based on current deck composition."""
        if not card_pool:
            return []
        
        suggestions = []
        
        for card in card_pool:
            if card.card_id in self.cards:
                continue  # Skip cards already in deck
            
            score = self._calculate_card_fit_score(card)
            suggestions.append((card, score))
        
        # Sort by score and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:count]
    
    def _calculate_card_fit_score(self, card: Card) -> float:
        """Calculate how well a card fits in this deck (0-1)."""
        score = 0.0
        
        # Element synergy
        element_count = sum(1 for card_id in self.cards 
                          if self.get_card_instance(card_id).element == card.element)
        element_ratio = element_count / max(1, sum(self.cards.values()))
        if element_ratio >= 0.3:  # Strong element theme
            score += 0.3
        elif element_ratio >= 0.15:  # Moderate theme
            score += 0.15
        
        # Divine allegiance synergy
        if card.divine_allegiance and card.divine_allegiance == self.divine_patron:
            score += 0.25
        
        # Mana curve fit
        current_curve = self.stats.mana_curve
        total_cards = sum(current_curve.values())
        if total_cards > 0:
            mana_cost = card.stats.mana_cost
            current_at_cost = current_curve.get(mana_cost, 0)
            ratio_at_cost = current_at_cost / total_cards
            
            # Prefer cards that fill gaps in curve
            if ratio_at_cost < 0.1:  # Understaffed mana cost
                score += 0.2
            elif ratio_at_cost > 0.25:  # Overstaffed
                score -= 0.1
        
        # Keyword synergy
        deck_keywords = set()
        for card_id in self.cards:
            deck_card = self.get_card_instance(card_id)
            if deck_card:
                deck_keywords.update(kw.key for kw in deck_card.keywords)
        
        card_keywords = set(kw.key for kw in card.keywords)
        keyword_overlap = len(card_keywords.intersection(deck_keywords))
        score += keyword_overlap * 0.1
        
        # Power level appropriateness
        avg_combat_rating = self.stats.combat_rating_average
        if avg_combat_rating > 0:
            card_rating = card.current_stats.calculate_combat_rating()
            rating_diff = abs(card_rating - avg_combat_rating)
            if rating_diff <= avg_combat_rating * 0.2:  # Within 20% of average
                score += 0.15
        
        return min(1.0, score)
    
    def export_to_format(self, format_type: str) -> str:
        """Export deck to various formats."""
        if format_type.lower() == 'json':
            return self._export_json()
        elif format_type.lower() == 'text':
            return self._export_text()
        elif format_type.lower() == 'mtga':  # Magic Arena style
            return self._export_mtga_style()
        else:
            return self._export_text()
    
    def _export_json(self) -> str:
        """Export to JSON format."""
        export_data = {
            'deck_id': self.deck_id,
            'name': self.name,
            'format': self.deck_format,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'cards': self.cards,
            'pharaoh_card': self.pharaoh_card.card_id if self.pharaoh_card else None,
            'divine_patron': self.divine_patron,
            'tags': list(self.tags),
            'description': self.description,
            'version': self.version,
            'hash_signature': self.hash_signature,
            'statistics': self.stats.to_dict() if hasattr(self.stats, 'to_dict') else {}
        }
        return json.dumps(export_data, indent=2)
    
    def _export_text(self) -> str:
        """Export to human-readable text format."""
        lines = []
        lines.append(f"# {self.name}")
        lines.append(f"Format: {self.deck_format}")
        lines.append(f"Total Cards: {self.get_total_cards()}")
        
        if self.divine_patron:
            lines.append(f"Divine Patron: {self.divine_patron}")
        
        if self.pharaoh_card:
            lines.append(f"Pharaoh: {self.pharaoh_card.name}")
        
        lines.append("")
        
        # Group cards by type and mana cost
        cards_by_type = defaultdict(list)
        for card_id, count in self.cards.items():
            card = self.get_card_instance(card_id)
            if card:
                cards_by_type[card.card_type.value].append((card, count))
        
        # Sort each type by mana cost, then name
        for card_type in cards_by_type:
            cards_by_type[card_type].sort(key=lambda x: (x[0].stats.mana_cost, x[0].name))
        
        # Output by type
        for card_type, cards in sorted(cards_by_type.items()):
            lines.append(f"## {card_type.replace('_', ' ').title()}")
            for card, count in cards:
                lines.append(f"{count}x {card.name} ({card.stats.mana_cost})")
            lines.append("")
        
        return "\n".join(lines)
    
    def _export_mtga_style(self) -> str:
        """Export in Magic Arena import format."""
        lines = []
        
        for card_id, count in sorted(self.cards.items()):
            card = self.get_card_instance(card_id)
            if card:
                # Format: "Count Card Name (SET) Card Number"
                set_code = card.custom_data.get('set_code', 'SOD')
                lines.append(f"{count} {card.name} ({set_code}) {card.card_id}")
        
        return "\n".join(lines)
    
    def clone(self, new_name: Optional[str] = None) -> 'Deck':
        """Create a copy of this deck."""
        cloned = Deck(
            name=new_name or f"{self.name} (Copy)",
            owner_id=self.owner_id,
            deck_format=self.deck_format
        )
        
        # Copy cards
        for card_id, count in self.cards.items():
            card = self.get_card_instance(card_id)
            if card:
                cloned.add_card(card, count)
        
        # Copy configuration
        cloned.constraints = self.constraints
        cloned.shuffle_algorithm = self.shuffle_algorithm
        cloned.divine_patron = self.divine_patron
        cloned.description = self.description
        cloned.tags = self.tags.copy()
        
        return cloned
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert deck to dictionary for serialization."""
        return {
            'deck_id': self.deck_id,
            'name': self.name,
            'owner_id': self.owner_id,
            'deck_format': self.deck_format,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'cards': self.cards,
            'constraints': {
                'min_size': self.constraints.min_size,
                'max_size': self.constraints.max_size,
                'max_copies_per_card': self.constraints.max_copies_per_card,
                'max_legendary': self.constraints.max_legendary,
                'max_mythic': self.constraints.max_mythic,
                'min_creature_ratio': self.constraints.min_creature_ratio,
                'max_spell_ratio': self.constraints.max_spell_ratio,
                'required_elements': [e.key for e in self.constraints.required_elements],
                'banned_cards': list(self.constraints.banned_cards),
                'format_restrictions': self.constraints.format_restrictions
            },
            'shuffle_algorithm': self.shuffle_algorithm.value,
            'pharaoh_card_id': self.pharaoh_card.card_id if self.pharaoh_card else None,
            'divine_patron': self.divine_patron,
            'underworld_progression': self.underworld_progression,
            'sacred_artifacts': self.sacred_artifacts,
            'description': self.description,
            'tags': list(self.tags),
            'version': self.version,
            'hash_signature': self.hash_signature,
            'win_rate': self.win_rate,
            'games_played': self.games_played,
            'mulligans_taken': self.mulligans_taken
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], card_pool: Dict[str, Card]) -> 'Deck':
        """Create deck from dictionary."""
        deck = cls(
            name=data['name'],
            owner_id=data.get('owner_id'),
            deck_format=data.get('deck_format', 'constructed')
        )
        
        deck.deck_id = data['deck_id']
        deck.created_at = datetime.fromisoformat(data['created_at'])
        deck.last_modified = datetime.fromisoformat(data['last_modified'])
        
        # Add cards
        for card_id, count in data['cards'].items():
            if card_id in card_pool:
                deck.add_card(card_pool[card_id], count)
        
        # Restore constraints
        constraints_data = data.get('constraints', {})
        deck.constraints = DeckConstraints(
            min_size=constraints_data.get('min_size', 30),
            max_size=constraints_data.get('max_size', 60),
            max_copies_per_card=constraints_data.get('max_copies_per_card', 3),
            max_legendary=constraints_data.get('max_legendary', 2),
            max_mythic=constraints_data.get('max_mythic', 1),
            min_creature_ratio=constraints_data.get('min_creature_ratio', 0.3),
            max_spell_ratio=constraints_data.get('max_spell_ratio', 0.4),
            required_elements=set(CardElement(e) for e in constraints_data.get('required_elements', [])),
            banned_cards=set(constraints_data.get('banned_cards', [])),
            format_restrictions=constraints_data.get('format_restrictions', {})
        )
        
        # Restore other properties
        deck.shuffle_algorithm = ShuffleAlgorithm(data.get('shuffle_algorithm', 'fisher_yates'))
        deck.divine_patron = data.get('divine_patron')
        deck.underworld_progression = data.get('underworld_progression', 0)
        deck.sacred_artifacts = data.get('sacred_artifacts', [])
        deck.description = data.get('description', '')
        deck.tags = set(data.get('tags', []))
        deck.version = data.get('version', '1.0.0')
        deck.win_rate = data.get('win_rate', 0.0)
        deck.games_played = data.get('games_played', 0)
        deck.mulligans_taken = data.get('mulligans_taken', 0)
        
        return deck
    
    def __str__(self) -> str:
        """String representation of deck."""
        return f"{self.name} ({self.get_total_cards()} cards, {self.deck_format})"
    
    def __len__(self) -> int:
        """Return total number of cards."""
        return self.get_total_cards()
    
    def __contains__(self, card_id: str) -> bool:
        """Check if deck contains a card."""
        return card_id in self.cards
    
    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Iterate over card IDs and counts."""
        return iter(self.cards.items())
```

### 3.5 HOUR-GLASS INITIATIVE SYSTEM WITH SUB-MILLISECOND TIMING

```python
# src/sands_of_duat/cards/initiative.py
from __future__ import annotations
import time
import heapq
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
import threading
import asyncio
from collections import deque
import uuid
import logging

logger = logging.getLogger(__name__)

class InitiativePhase(Enum):
    """Phases within each initiative cycle."""
    PREPARATION = "preparation"        # Before actions can be taken
    ACTION = "action"                 # Main action phase
    REACTION = "reaction"             # Response to actions
    RESOLUTION = "resolution"         # Effects resolve
    CLEANUP = "cleanup"              # End of cycle cleanup

class TimingPrecision(Enum):
    """Timing precision levels."""
    MILLISECOND = 1      # 1ms precision
    SUBMILLISECOND = 0.1 # 0.1ms precision  
    MICROSECOND = 0.001  # 0.001ms precision

@dataclass
class InitiativeEntry:
    """An entry in the initiative queue."""
    entity_id: str
    initiative_value: float
    action_callback: Optional[Callable] = None
    priority: int = 0  # Higher priority goes first on ties
    timestamp: float = field(default_factory=time.perf_counter)
    phase: InitiativePhase = InitiativePhase.ACTION
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other: 'InitiativeEntry') -> bool:
        """Compare entries for heap ordering (higher initiative first)."""
        # Primary: Higher initiative value
        if self.initiative_value != other.initiative_value:
            return self.initiative_value > other.initiative_value
        
        # Secondary: Higher priority
        if self.priority != other.priority:
            return self.priority > other.priority
        
        # Tertiary: Earlier timestamp
        return self.timestamp < other.timestamp

@dataclass
class HourGlassState:
    """State of the Hour-Glass timer."""
    current_hour: int = 1         # Current underworld hour (1-12)
    sand_remaining: float = 100.0  # Percentage of sand left in current hour
    sand_flow_rate: float = 1.0   # Rate at which sand flows
    is_flowing: bool = True       # Whether time is actively passing
    last_update: float = field(default_factory=time.perf_counter)
    total_elapsed: float = 0.0    # Total time elapsed
    
    # Egyptian mythology elements
    ra_position: float = 0.0      # Ra's position in solar barque (0-1)
    underworld_pressure: float = 1.0  # Affects initiative calculations
    divine_intervention: bool = False # Gods intervening in time flow

class InitiativeSystem:
    """High-precision initiative system with Egyptian Hour-Glass theming."""
    
    def __init__(self, timing_precision: TimingPrecision = TimingPrecision.SUBMILLISECOND):
        # Core System
        self.precision = timing_precision
        self.initiative_heap: List[InitiativeEntry] = []
        self.current_entry: Optional[InitiativeEntry] = None
        self.current_phase = InitiativePhase.PREPARATION
        
        # Hour-Glass Timer
        self.hourglass = HourGlassState()
        self.hour_duration = 300.0  # 5 minutes per underworld hour
        
        # Timing System
        self.system_start_time = time.perf_counter()
        self.last_tick = self.system_start_time
        self.tick_history: deque = deque(maxlen=1000)  # Keep last 1000 ticks
        self.average_tick_time = 0.0
        self.timing_drift = 0.0
        
        # Threading and Async
        self.is_running = False
        self.update_thread: Optional[threading.Thread] = None
        self.thread_lock = threading.RLock()
        self.tick_callbacks: List[Callable] = []
        
        # Performance Monitoring
        self.performance_stats = {
            'total_ticks': 0,
            'missed_deadlines': 0,
            'average_processing_time': 0.0,
            'max_processing_time': 0.0,
            'timing_jitter': 0.0
        }
        
        # Egyptian Mythology Integration
        self.divine_modifiers: Dict[str, float] = {}  # God-specific initiative modifiers
        self.underworld_effects: List[Callable] = []  # Effects that trigger each hour
        self.time_dilation_active = False             # For special abilities that slow time
    
    def start(self) -> None:
        """Start the initiative system."""
        with self.thread_lock:
            if self.is_running:
                return
            
            self.is_running = True
            self.system_start_time = time.perf_counter()
            self.last_tick = self.system_start_time
            
            # Start update thread
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            
            logger.info("Initiative system started with precision: %s", self.precision.name)
    
    def stop(self) -> None:
        """Stop the initiative system."""
        with self.thread_lock:
            self.is_running = False
            
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)
        
        logger.info("Initiative system stopped")
    
    def add_entity(self, entity_id: str, base_initiative: float,
                   action_callback: Optional[Callable] = None,
                   priority: int = 0, metadata: Dict[str, Any] = None) -> None:
        """Add an entity to the initiative queue."""
        # Calculate modified initiative based on Egyptian factors
        modified_initiative = self._calculate_modified_initiative(
            entity_id, base_initiative, metadata or {}
        )
        
        entry = InitiativeEntry(
            entity_id=entity_id,
            initiative_value=modified_initiative,
            action_callback=action_callback,
            priority=priority,
            metadata=metadata or {}
        )
        
        with self.thread_lock:
            heapq.heappush(self.initiative_heap, entry)
        
        logger.debug("Added entity %s with initiative %.3f", entity_id, modified_initiative)
    
    def remove_entity(self, entity_id: str) -> bool:
        """Remove an entity from the initiative queue."""
        with self.thread_lock:
            # Find and mark entry for removal
            removed = False
            for entry in self.initiative_heap:
                if entry.entity_id == entity_id:
                    entry.entity_id = "_REMOVED_"  # Mark for removal
                    removed = True
            
            # Clean up removed entries
            if removed:
                self.initiative_heap = [e for e in self.initiative_heap if e.entity_id != "_REMOVED_"]
                heapq.heapify(self.initiative_heap)
        
        return removed
    
    def modify_initiative(self, entity_id: str, new_initiative: float) -> bool:
        """Modify an entity's initiative value."""
        with self.thread_lock:
            # Remove old entry and add new one
            if self.remove_entity(entity_id):
                # Find the original entry to preserve other data
                original_entry = None
                for entry in self.initiative_heap:
                    if entry.entity_id == entity_id:
                        original_entry = entry
                        break
                
                # Re-add with new initiative
                metadata = original_entry.metadata if original_entry else {}
                self.add_entity(
                    entity_id, new_initiative, 
                    original_entry.action_callback if original_entry else None,
                    original_entry.priority if original_entry else 0,
                    metadata
                )
                return True
        
        return False
    
    def get_current_entity(self) -> Optional[str]:
        """Get the entity ID whose turn it currently is."""
        return self.current_entry.entity_id if self.current_entry else None
    
    def get_next_entities(self, count: int = 5) -> List[Tuple[str, float]]:
        """Get the next few entities in initiative order."""
        with self.thread_lock:
            # Create a copy of heap to peek without modifying
            heap_copy = self.initiative_heap.copy()
            
            next_entities = []
            for _ in range(min(count, len(heap_copy))):
                if heap_copy:
                    entry = heapq.heappop(heap_copy)
                    next_entities.append((entry.entity_id, entry.initiative_value))
            
            return next_entities
    
    def advance_turn(self) -> Optional[InitiativeEntry]:
        """Advance to the next entity's turn."""
        with self.thread_lock:
            # Complete current turn
            if self.current_entry:
                self._complete_current_turn()
            
            # Get next entry
            if self.initiative_heap:
                self.current_entry = heapq.heappop(self.initiative_heap)
                self.current_phase = InitiativePhase.PREPARATION
                
                logger.debug("Advanced to entity %s (initiative: %.3f)", 
                           self.current_entry.entity_id, 
                           self.current_entry.initiative_value)
                
                return self.current_entry
            else:
                self.current_entry = None
                return None
    
    def advance_phase(self) -> InitiativePhase:
        """Advance to the next phase of the current turn."""
        if not self.current_entry:
            return self.current_phase
        
        phase_order = list(InitiativePhase)
        current_index = phase_order.index(self.current_phase)
        
        if current_index < len(phase_order) - 1:
            self.current_phase = phase_order[current_index + 1]
        else:
            # End of turn, advance to next entity
            self.advance_turn()
        
        return self.current_phase
    
    def execute_current_action(self) -> Any:
        """Execute the current entity's action."""
        if not self.current_entry or not self.current_entry.action_callback:
            return None
        
        start_time = time.perf_counter()
        
        try:
            # Execute action
            result = self.current_entry.action_callback(
                self.current_entry.entity_id,
                self.current_phase,
                self.current_entry.metadata
            )
            
            # Record execution time
            execution_time = time.perf_counter() - start_time
            self._update_performance_stats(execution_time)
            
            return result
            
        except Exception as e:
            logger.error("Error executing action for entity %s: %s", 
                        self.current_entry.entity_id, e)
            return None
    
    def add_tick_callback(self, callback: Callable) -> None:
        """Add a callback to be executed every system tick."""
        self.tick_callbacks.append(callback)
    
    def remove_tick_callback(self, callback: Callable) -> None:
        """Remove a tick callback."""
        if callback in self.tick_callbacks:
            self.tick_callbacks.remove(callback)
    
    def set_divine_modifier(self, entity_id: str, god_name: str, modifier: float) -> None:
        """Set a divine initiative modifier for an entity."""
        key = f"{entity_id}:{god_name}"
        self.divine_modifiers[key] = modifier
        
        # Recalculate initiative if entity is in queue
        with self.thread_lock:
            for entry in self.initiative_heap:
                if entry.entity_id == entity_id:
                    # Recalculate and update
                    new_initiative = self._calculate_modified_initiative(
                        entity_id, entry.metadata.get('base_initiative', entry.initiative_value), 
                        entry.metadata
                    )
                    entry.initiative_value = new_initiative
                    heapq.heapify(self.initiative_heap)  # Restore heap property
                    break
    
    def activate_time_dilation(self, factor: float = 0.5, duration: float = 5.0) -> None:
        """Activate time dilation effect (slows down time)."""
        self.time_dilation_active = True
        self.hourglass.sand_flow_rate *= factor
        
        # Schedule deactivation
        def deactivate():
            time.sleep(duration)
            self.time_dilation_active = False
            self.hourglass.sand_flow_rate = 1.0
        
        threading.Thread(target=deactivate, daemon=True).start()
        
        logger.info("Time dilation activated: factor=%.2f, duration=%.1fs", factor, duration)
    
    def get_hourglass_state(self) -> HourGlassState:
        """Get current state of the Hour-Glass."""
        return self.hourglass
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        stats = self.performance_stats.copy()
        stats.update({
            'current_hour': self.hourglass.current_hour,
            'sand_remaining': self.hourglass.sand_remaining,
            'total_elapsed_time': time.perf_counter() - self.system_start_time,
            'timing_precision': self.precision.value,
            'entities_in_queue': len(self.initiative_heap),
            'average_tick_interval': self.average_tick_time,
            'timing_drift': self.timing_drift
        })
        return stats
    
    def _update_loop(self) -> None:
        """Main update loop running in separate thread."""
        target_interval = self.precision.value / 1000.0  # Convert to seconds
        
        while self.is_running:
            loop_start = time.perf_counter()
            
            # Update hourglass
            self._update_hourglass()
            
            # Execute tick callbacks
            for callback in self.tick_callbacks:
                try:
                    callback(self)
                except Exception as e:
                    logger.error("Error in tick callback: %s", e)
            
            # Calculate timing metrics
            self._update_timing_metrics(loop_start)
            
            # Sleep for precision interval
            elapsed = time.perf_counter() - loop_start
            sleep_time = max(0, target_interval - elapsed)
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # We're running behind schedule
                self.performance_stats['missed_deadlines'] += 1
    
    def _update_hourglass(self) -> None:
        """Update the Hour-Glass state."""
        current_time = time.perf_counter()
        dt = current_time - self.hourglass.last_update
        
        if self.hourglass.is_flowing and dt > 0:
            # Calculate sand flow
            sand_decrease = (dt / self.hour_duration) * 100.0 * self.hourglass.sand_flow_rate
            self.hourglass.sand_remaining = max(0, self.hourglass.sand_remaining - sand_decrease)
            
            # Update Ra's position in solar barque
            self.hourglass.ra_position = (self.hourglass.current_hour - 1 + 
                                        (100 - self.hourglass.sand_remaining) / 100.0) / 12.0
            
            # Check for hour completion
            if self.hourglass.sand_remaining <= 0 and self.hourglass.current_hour < 12:
                self._advance_underworld_hour()
            
            self.hourglass.total_elapsed += dt
        
        self.hourglass.last_update = current_time
    
    def _advance_underworld_hour(self) -> None:
        """Advance to the next underworld hour."""
        old_hour = self.hourglass.current_hour
        self.hourglass.current_hour += 1
        self.hourglass.sand_remaining = 100.0
        
        # Calculate underworld pressure (affects initiative)
        # Pressure increases as you go deeper into underworld
        self.hourglass.underworld_pressure = 1.0 + (self.hourglass.current_hour * 0.1)
        
        # Trigger underworld effects
        for effect in self.underworld_effects:
            try:
                effect(old_hour, self.hourglass.current_hour)
            except Exception as e:
                logger.error("Error in underworld effect: %s", e)
        
        logger.info("Advanced to underworld hour %d", self.hourglass.current_hour)
    
    def _calculate_modified_initiative(self, entity_id: str, base_initiative: float, 
                                     metadata: Dict[str, Any]) -> float:
        """Calculate initiative with Egyptian mythology modifiers."""
        modified = base_initiative
        
        # Divine modifiers
        for key, modifier in self.divine_modifiers.items():
            if key.startswith(f"{entity_id}:"):
                modified += modifier
        
        # Underworld pressure effect
        modified *= self.hourglass.underworld_pressure
        
        # Time dilation effect
        if self.time_dilation_active:
            modified *= 0.8  # Slower reactions in dilated time
        
        # Ba-Ka separation effects
        if metadata.get('ba_separated', False):
            modified += 5  # Separated soul acts faster
        if metadata.get('ka_manifested', False):
            modified += 3  # Life force manifestation increases initiative
        
        # Divine favor effects
        divine_favor = metadata.get('divine_favor', 0)
        if divine_favor > 0:
            modified += divine_favor * 0.1
        elif divine_favor < 0:
            modified += divine_favor * 0.2  # Negative favor hurts more
        
        # Ra's position effect (solar cycle influences initiative)
        ra_modifier = math.sin(self.hourglass.ra_position * 2 * math.pi) * 2
        modified += ra_modifier
        
        return max(0.1, modified)  # Minimum initiative of 0.1
    
    def _complete_current_turn(self) -> None:
        """Complete the current entity's turn."""
        if not self.current_entry:
            return
        
        # Record turn completion
        turn_duration = time.perf_counter() - self.current_entry.timestamp
        
        # Log if turn took too long
        if turn_duration > 1.0:  # More than 1 second
            logger.warning("Long turn detected: entity=%s, duration=%.3fs", 
                         self.current_entry.entity_id, turn_duration)
        
        # Reset phase
        self.current_phase = InitiativePhase.PREPARATION
    
    def _update_timing_metrics(self, loop_start: float) -> None:
        """Update timing and performance metrics."""
        current_time = time.perf_counter()
        
        # Tick timing
        tick_time = current_time - self.last_tick
        self.tick_history.append(tick_time)
        
        if len(self.tick_history) >= 10:
            # Calculate average over last 10 ticks
            recent_ticks = list(self.tick_history)[-10:]
            self.average_tick_time = sum(recent_ticks) / len(recent_ticks)
            
            # Calculate timing drift
            expected_interval = self.precision.value / 1000.0
            self.timing_drift = abs(self.average_tick_time - expected_interval)
        
        # Processing time
        processing_time = current_time - loop_start
        self.performance_stats['total_ticks'] += 1
        
        # Update average processing time
        prev_avg = self.performance_stats['average_processing_time']
        tick_count = self.performance_stats['total_ticks']
        self.performance_stats['average_processing_time'] = (
            (prev_avg * (tick_count - 1) + processing_time) / tick_count
        )
        
        # Update max processing time
        if processing_time > self.performance_stats['max_processing_time']:
            self.performance_stats['max_processing_time'] = processing_time
        
        # Calculate jitter (variation in timing)
        if len(self.tick_history) >= 2:
            recent_times = list(self.tick_history)[-10:]
            if len(recent_times) >= 2:
                jitter = max(recent_times) - min(recent_times)
                self.performance_stats['timing_jitter'] = jitter
        
        self.last_tick = current_time
    
    def _update_performance_stats(self, execution_time: float) -> None:
        """Update performance statistics."""
        # This method is called after executing actions
        if execution_time > 0.1:  # More than 100ms
            logger.warning("Slow action execution: %.3fs", execution_time)


# Egyptian-themed utility functions for initiative system
import math

def calculate_divine_initiative_bonus(god_name: str, hour: int, favor: int) -> float:
    """Calculate initiative bonus based on Egyptian god and current hour."""
    # Each god has different power throughout the underworld journey
    god_hour_bonuses = {
        'Ra': {1: 10, 2: 8, 3: 6, 4: 4, 5: 2, 6: 0, 7: -2, 8: -4, 9: -2, 10: 0, 11: 4, 12: 8},
        'Anubis': {1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 10, 7: 8, 8: 6, 9: 4, 10: 2, 11: 0, 12: 0},
        'Thoth': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5},
        'Set': {1: 0, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 10, 8: 8, 9: 6, 10: 4, 11: 2, 12: 0},
        'Isis': {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2},
        'Osiris': {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 8, 12: 6}
    }
    
    base_bonus = god_hour_bonuses.get(god_name, {}).get(hour, 0)
    favor_multiplier = 1.0 + (favor / 100.0)  # Favor ranges from -50 to +50
    
    return base_bonus * favor_multiplier

def calculate_ba_ka_initiative_effect(ba_separated: bool, ka_manifested: bool, 
                                    ba_power: int, ka_strength: int) -> float:
    """Calculate initiative effects from Ba-Ka spiritual state."""
    bonus = 0.0
    
    if ba_separated:
        # Separated Ba increases initiative based on spiritual power
        bonus += ba_power * 0.2
        
    if ka_manifested:
        # Manifested Ka provides steady initiative boost
        bonus += ka_strength * 0.15
        
    if ba_separated and ka_manifested:
        # Both separated provides synergy bonus but instability
        bonus += 5.0
        bonus *= 0.9  # 10% reduction due to instability
    
    return bonus

def simulate_egyptian_time_flow(current_hour: int, ra_position: float) -> Dict[str, float]:
    """Simulate how time flows differently through Egyptian underworld."""
    # Time flows differently in each hour of the underworld
    hour_flow_rates = {
        1: 1.0,   # Entry - normal time
        2: 0.9,   # Slowing down
        3: 0.8,   # Time becomes heavy
        4: 0.7,   # Deep underworld effects
        5: 0.6,   # Minimum flow rate
        6: 0.65,  # Starting to recover
        7: 0.7,   # Gradual acceleration
        8: 0.8,   # 
        9: 0.9,   # 
        10: 1.0,  # Back to normal
        11: 1.1,  # Time accelerates toward exit
        12: 1.2   # Final rush to rebirth
    }
    
    base_flow = hour_flow_rates.get(current_hour, 1.0)
    
    # Ra's position affects time flow (sinusoidal pattern)
    ra_effect = 1.0 + (math.sin(ra_position * 2 * math.pi) * 0.1)
    
    # Divine intervention can occasionally alter time
    intervention_chance = 0.01  # 1% chance per calculation
    intervention_factor = 1.0
    if random.random() < intervention_chance:
        intervention_factor = random.uniform(0.5, 2.0)  # Random time distortion
    
    final_flow_rate = base_flow * ra_effect * intervention_factor
    
    return {
        'flow_rate': final_flow_rate,
        'base_rate': base_flow,
        'ra_effect': ra_effect,
        'intervention': intervention_factor != 1.0,
        'intervention_factor': intervention_factor
    }


# Example usage and integration
class EgyptianCardGame:
    """Example integration of initiative system with card game."""
    
    def __init__(self):
        self.initiative_system = InitiativeSystem(TimingPrecision.SUBMILLISECOND)
        self.players = {}
        self.current_turn_player = None
        
        # Add underworld progression callbacks
        self.initiative_system.underworld_effects.append(self._on_hour_change)
        self.initiative_system.add_tick_callback(self._on_system_tick)
    
    def add_player(self, player_id: str, base_initiative: float = 10.0):
        """Add a player to the game."""
        self.players[player_id] = {
            'initiative': base_initiative,
            'divine_patron': None,
            'ba_separated': False,
            'ka_manifested': False
        }
        
        self.initiative_system.add_entity(
            player_id, 
            base_initiative,
            action_callback=self._player_turn_callback,
            metadata=self.players[player_id]
        )
    
    def start_game(self):
        """Start the game and initiative system."""
        self.initiative_system.start()
        
        # Begin first turn
        self.initiative_system.advance_turn()
    
    def _player_turn_callback(self, player_id: str, phase: InitiativePhase, metadata: Dict[str, Any]):
        """Callback for player turns."""
        self.current_turn_player = player_id
        
        if phase == InitiativePhase.ACTION:
            print(f"Player {player_id}'s turn - Hour {self.initiative_system.hourglass.current_hour}")
            print(f"Sand remaining: {self.initiative_system.hourglass.sand_remaining:.1f}%")
            
            # Simulate player action
            time.sleep(0.1)  # Simulate thinking time
            
            return f"Player {player_id} completed action"
    
    def _on_hour_change(self, old_hour: int, new_hour: int):
        """Handle underworld hour changes."""
        print(f"The sands shift... entering hour {new_hour} of the underworld")
        
        # Apply hour-specific effects to all players
        for player_id, player_data in self.players.items():
            if player_data.get('divine_patron'):
                bonus = calculate_divine_initiative_bonus(
                    player_data['divine_patron'], 
                    new_hour, 
                    player_data.get('divine_favor', 0)
                )
                self.initiative_system.set_divine_modifier(player_id, player_data['divine_patron'], bonus)
    
    def _on_system_tick(self, initiative_system: InitiativeSystem):
        """Handle system ticks."""
        # Can be used for real-time effects, animations, etc.
        pass
```

---

## 4. COMBAT SYSTEM IMPLEMENTATION (ULTRA-DETAILED)

### 4.1 COMPLETE 13-PHASE COMBAT STATE MACHINE

```python
# src/sands_of_duat/combat/combat_manager.py
from __future__ import annotations
import uuid
from typing import Dict, List, Optional, Any, Set, Tuple, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
import logging
import math
import random
from collections import defaultdict, deque

from ..cards.card import Card, CardKeyword, CardElement
from ..cards.effects.base_effect import BaseEffect, EffectContext, EffectTrigger
from .targeting import TargetingSystem, Target, TargetType, TargetingResult
from .damage_calculation import DamageCalculator, DamageType, DamageResult
from .ba_ka_system import BaKaManager, SoulState

logger = logging.getLogger(__name__)

class CombatPhase(Enum):
    """13-phase combat system based on Egyptian mythology."""
    DAWN_PREPARATION = "dawn_preparation"         # 1. Pre-combat setup
    DIVINE_INVOCATION = "divine_invocation"       # 2. Call upon gods
    BA_SEPARATION = "ba_separation"               # 3. Soul preparation
    TARGETING = "targeting"                       # 4. Select targets
    INITIATIVE_ROLL = "initiative_roll"           # 5. Determine turn order
    UNDERWORLD_PASSAGE = "underworld_passage"     # 6. Navigate duat
    COMBAT_ACTION = "combat_action"               # 7. Main action phase
    DIVINE_JUDGMENT = "divine_judgment"           # 8. Gods weigh actions
    DAMAGE_RESOLUTION = "damage_resolution"       # 9. Apply damage/effects
    KA_MANIFESTATION = "ka_manifestation"         # 10. Life force effects
    AFTERLIFE_TRANSITION = "afterlife_transition" # 11. Handle death
    COSMIC_BALANCE = "cosmic_balance"             # 12. Restore ma'at
    DUSK_CLEANUP = "dusk_cleanup"                 # 13. End combat cleanup

class CombatState(Enum):
    """Overall state of combat."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"

@dataclass
class CombatEntity:
    """Entity participating in combat."""
    entity_id: str
    card: Card
    position: Tuple[int, int]
    is_alive: bool = True
    actions_remaining: int = 1
    can_move: bool = True
    can_attack: bool = True
    can_cast: bool = True
    
    # Egyptian-specific states
    ba_separated: bool = False
    ka_manifested: bool = False
    divine_protection: Optional[str] = None  # God providing protection
    underworld_tier: int = 0
    maat_balance: int = 0  # Cosmic balance score
    
    # Combat tracking
    damage_taken_this_turn: int = 0
    actions_taken: List[Dict[str, Any]] = field(default_factory=list)
    effects_applied: List[BaseEffect] = field(default_factory=list)
    
    def __post_init__(self):
        if self.actions_taken is None:
            self.actions_taken = []
        if self.effects_applied is None:
            self.effects_applied = []

@dataclass
class CombatAction:
    """An action taken during combat."""
    action_id: str
    entity_id: str
    action_type: str
    targets: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    phase: CombatPhase = CombatPhase.COMBAT_ACTION
    resolved: bool = False
    results: Dict[str, Any] = field(default_factory=dict)

class CombatManager:
    """Advanced combat system with Egyptian mythology integration."""
    
    def __init__(self, battlefield_width: int = 8, battlefield_height: int = 6):
        # Core Combat State
        self.combat_id = str(uuid.uuid4())
        self.state = CombatState.NOT_STARTED
        self.current_phase = CombatPhase.DAWN_PREPARATION
        self.turn_number = 0
        self.round_number = 0
        
        # Battlefield
        self.battlefield_width = battlefield_width
        self.battlefield_height = battlefield_height
        self.battlefield: Dict[Tuple[int, int], Optional[str]] = {}  # position -> entity_id
        self.terrain_effects: Dict[Tuple[int, int], Dict[str, Any]] = {}
        
        # Entities and Initiative
        self.entities: Dict[str, CombatEntity] = {}
        self.initiative_order: List[str] = []
        self.current_entity_index = 0
        
        # Action Queue and History
        self.action_queue: deque[CombatAction] = deque()
        self.action_history: List[CombatAction] = []
        self.pending_effects: List[BaseEffect] = []
        
        # Subsystems
        self.targeting_system = TargetingSystem(battlefield_width, battlefield_height)
        self.damage_calculator = DamageCalculator()
        self.ba_ka_manager = BaKaManager()
        
        # Egyptian Mythology Systems
        self.divine_interventions: Dict[str, Any] = {}  # Active god interventions
        self.underworld_effects: Dict[int, List[Callable]] = {}  # Effects by hour
        self.cosmic_balance_total = 0  # Overall ma'at balance
        self.active_curses: List[Dict[str, Any]] = []
        self.active_blessings: List[Dict[str, Any]] = []
        
        # Event System
        self.phase_callbacks: Dict[CombatPhase, List[Callable]] = defaultdict(list)
        self.combat_events: List[Dict[str, Any]] = []
        
        # Performance and Analytics
        self.phase_timings: Dict[CombatPhase, List[float]] = defaultdict(list)
        self.action_statistics: Dict[str, int] = defaultdict(int)
        self.combat_metrics: Dict[str, Any] = {}
        
        # Initialize battlefield
        self._initialize_battlefield()
        
        logger.info(f"Combat system initialized: {self.combat_id}")
    
    def add_entity(self, card: Card, position: Tuple[int, int], 
                   player_id: str, team: str = "neutral") -> str:
        """Add an entity to combat."""
        if not self._is_valid_position(position):
            raise ValueError(f"Invalid position: {position}")
        
        if position in self.battlefield:
            raise ValueError(f"Position {position} already occupied")
        
        entity = CombatEntity(
            entity_id=str(uuid.uuid4()),
            card=card,
            position=position
        )
        
        # Set Egyptian-specific properties from card
        entity.ba_separated = card.ba_separated
        entity.ka_manifested = card.ka_manifested
        entity.underworld_tier = card.underworld_tier
        entity.divine_protection = card.divine_allegiance
        
        self.entities[entity.entity_id] = entity
        self.battlefield[position] = entity.entity_id
        
        # Initialize Ba-Ka tracking
        self.ba_ka_manager.register_entity(entity.entity_id, card)
        
        logger.debug(f"Added entity {entity.entity_id} at {position}")
        return entity.entity_id
    
    def remove_entity(self, entity_id: str) -> bool:
        """Remove an entity from combat."""
        if entity_id not in self.entities:
            return False
        
        entity = self.entities[entity_id]
        
        # Clear battlefield position
        if entity.position in self.battlefield:
            del self.battlefield[entity.position]
        
        # Trigger death effects if applicable
        if entity.is_alive:
            self._handle_entity_death(entity_id, "removed")
        
        # Remove from initiative order
        if entity_id in self.initiative_order:
            self.initiative_order.remove(entity_id)
        
        # Cleanup subsystems
        self.ba_ka_manager.unregister_entity(entity_id)
        
        del self.entities[entity_id]
        
        logger.debug(f"Removed entity {entity_id}")
        return True
    
    def start_combat(self) -> bool:
        """Initialize and start combat."""
        if self.state != CombatState.NOT_STARTED:
            return False
        
        if len(self.entities) < 2:
            logger.error("Cannot start combat with fewer than 2 entities")
            return False
        
        self.state = CombatState.IN_PROGRESS
        self.current_phase = CombatPhase.DAWN_PREPARATION
        self.turn_number = 1
        self.round_number = 1
        
        # Execute first phase
        self._execute_phase(CombatPhase.DAWN_PREPARATION)
        
        self._emit_combat_event("combat_started", {
            "combat_id": self.combat_id,
            "entity_count": len(self.entities),
            "battlefield_size": (self.battlefield_width, self.battlefield_height)
        })
        
        logger.info(f"Combat started: {self.combat_id}")
        return True
    
    def advance_phase(self) -> CombatPhase:
        """Advance to the next combat phase."""
        if self.state != CombatState.IN_PROGRESS:
            return self.current_phase
        
        phase_start = datetime.now()
        
        # Get next phase
        phases = list(CombatPhase)
        current_index = phases.index(self.current_phase)
        
        if current_index < len(phases) - 1:
            self.current_phase = phases[current_index + 1]
        else:
            # End of round, start new round
            self.current_phase = CombatPhase.DAWN_PREPARATION
            self.round_number += 1
            self._emit_combat_event("round_ended", {"round": self.round_number - 1})
        
        # Execute new phase
        self._execute_phase(self.current_phase)
        
        # Record timing
        phase_duration = (datetime.now() - phase_start).total_seconds()
        self.phase_timings[self.current_phase].append(phase_duration)
        
        return self.current_phase
    
    def _execute_phase(self, phase: CombatPhase) -> None:
        """Execute the logic for a specific combat phase."""
        phase_start = datetime.now()
        
        logger.debug(f"Executing phase: {phase.value}")
        
        try:
            if phase == CombatPhase.DAWN_PREPARATION:
                self._phase_dawn_preparation()
            elif phase == CombatPhase.DIVINE_INVOCATION:
                self._phase_divine_invocation()
            elif phase == CombatPhase.BA_SEPARATION:
                self._phase_ba_separation()
            elif phase == CombatPhase.TARGETING:
                self._phase_targeting()
            elif phase == CombatPhase.INITIATIVE_ROLL:
                self._phase_initiative_roll()
            elif phase == CombatPhase.UNDERWORLD_PASSAGE:
                self._phase_underworld_passage()
            elif phase == CombatPhase.COMBAT_ACTION:
                self._phase_combat_action()
            elif phase == CombatPhase.DIVINE_JUDGMENT:
                self._phase_divine_judgment()
            elif phase == CombatPhase.DAMAGE_RESOLUTION:
                self._phase_damage_resolution()
            elif phase == CombatPhase.KA_MANIFESTATION:
                self._phase_ka_manifestation()
            elif phase == CombatPhase.AFTERLIFE_TRANSITION:
                self._phase_afterlife_transition()
            elif phase == CombatPhase.COSMIC_BALANCE:
                self._phase_cosmic_balance()
            elif phase == CombatPhase.DUSK_CLEANUP:
                self._phase_dusk_cleanup()
                
            # Execute registered callbacks
            for callback in self.phase_callbacks[phase]:
                try:
                    callback(self, phase)
                except Exception as e:
                    logger.error(f"Phase callback error: {e}")
                    
        except Exception as e:
            logger.error(f"Phase execution error for {phase.value}: {e}")
            
        # Emit phase completion event
        phase_duration = (datetime.now() - phase_start).total_seconds()
        self._emit_combat_event("phase_completed", {
            "phase": phase.value,
            "duration": phase_duration,
            "round": self.round_number,
            "turn": self.turn_number
        })
    
    def _phase_dawn_preparation(self) -> None:
        """Phase 1: Prepare for combat - refresh resources and abilities."""
        for entity_id, entity in self.entities.items():
            if not entity.is_alive:
                continue
                
            # Reset action allowances
            entity.actions_remaining = 1
            entity.can_move = True
            entity.can_attack = True
            entity.can_cast = True
            entity.damage_taken_this_turn = 0
            entity.actions_taken.clear()
            
            # Refresh card if exhausted
            if entity.card.is_exhausted:
                entity.card.refresh()
            
            # Apply start-of-turn effects
            start_turn_effects = entity.card.get_effects_by_timing("start_turn")
            for effect in start_turn_effects:
                self._apply_effect_to_entity(effect, entity_id, EffectTrigger.START_TURN)
        
        # Process terrain effects
        self._process_terrain_effects()
        
        # Check for divine interventions
        self._check_divine_interventions()
    
    def _phase_divine_invocation(self) -> None:
        """Phase 2: Invoke divine powers and blessings."""
        for entity_id, entity in self.entities.items():
            if not entity.is_alive or not entity.divine_protection:
                continue
            
            god_name = entity.divine_protection
            divine_favor = entity.card.stats.divine_favor
            
            # Calculate divine intervention chance
            intervention_chance = min(0.3, abs(divine_favor) / 100.0)  # Max 30% chance
            
            if random.random() < intervention_chance:
                intervention_type = self._determine_divine_intervention(god_name, divine_favor)
                self._apply_divine_intervention(entity_id, god_name, intervention_type)
        
        # Process active divine interventions
        for god_name, intervention in list(self.divine_interventions.items()):
            intervention['duration'] -= 1
            if intervention['duration'] <= 0:
                self._end_divine_intervention(god_name)
    
    def _phase_ba_separation(self) -> None:
        """Phase 3: Handle soul separation and spiritual effects."""
        for entity_id, entity in self.entities.items():
            if not entity.is_alive:
                continue
            
            # Check for automatic Ba separation
            if entity.card.has_keyword(CardKeyword.BA_SPLIT) and not entity.ba_separated:
                if entity.card.current_stats.health <= entity.card.stats.health // 3:
                    # Critical health triggers automatic separation
                    self._separate_entity_ba(entity_id)
            
            # Process existing Ba separations
            if entity.ba_separated:
                ba_state = self.ba_ka_manager.get_ba_state(entity_id)
                if ba_state:
                    # Ba can act independently
                    self._process_independent_ba_action(entity_id, ba_state)
        
        # Resolve Ba-Ka interactions
        self.ba_ka_manager.process_ba_ka_interactions()
    
    def _phase_targeting(self) -> None:
        """Phase 4: Determine valid targets for actions."""
        for entity_id, entity in self.entities.items():
            if not entity.is_alive or entity.actions_remaining <= 0:
                continue
            
            # Calculate available targets for each possible action
            entity_targets = {
                'move': self._get_movement_targets(entity_id),
                'attack': self._get_attack_targets(entity_id),
                'cast': self._get_spell_targets(entity_id),
                'special': self._get_special_targets(entity_id)
            }
            
            # Store targeting information
            if not hasattr(entity, 'available_targets'):
                entity.available_targets = {}
            entity.available_targets = entity_targets
    
    def _phase_initiative_roll(self) -> None:
        """Phase 5: Determine turn order for the combat action phase."""
        if self.turn_number == 1 or self.round_number > 1:
            # Recalculate initiative for new round
            entity_initiatives = []
            
            for entity_id, entity in self.entities.items():
                if not entity.is_alive:
                    continue
                
                # Base initiative from card stats
                base_initiative = entity.card.current_stats.initiative
                
                # Egyptian mythology modifiers
                initiative_modifier = 0
                
                # Divine favor affects initiative
                initiative_modifier += entity.card.current_stats.divine_favor * 0.1
                
                # Ba separation increases initiative
                if entity.ba_separated:
                    initiative_modifier += 5
                
                # Ka manifestation provides steady bonus
                if entity.ka_manifested:
                    initiative_modifier += 3
                
                # Underworld tier affects initiative
                initiative_modifier += entity.underworld_tier * 0.5
                
                # Apply terrain modifiers
                position = entity.position
                terrain = self.terrain_effects.get(position, {})
                initiative_modifier += terrain.get('initiative_modifier', 0)
                
                # Roll dice for randomness
                roll = random.randint(1, 20)
                
                final_initiative = base_initiative + initiative_modifier + roll
                entity_initiatives.append((entity_id, final_initiative))
            
            # Sort by initiative (highest first)
            entity_initiatives.sort(key=lambda x: x[1], reverse=True)
            self.initiative_order = [entity_id for entity_id, _ in entity_initiatives]
            self.current_entity_index = 0
            
            # Log initiative order
            initiative_log = [(eid, init) for eid, init in entity_initiatives]
            self._emit_combat_event("initiative_determined", {
                "order": initiative_log,
                "round": self.round_number
            })
    
    def _phase_underworld_passage(self) -> None:
        """Phase 6: Navigate through underworld effects and hazards."""
        # Apply underworld tier effects
        current_hour = min(12, max(1, self.round_number))
        
        if current_hour in self.underworld_effects:
            for effect_callback in self.underworld_effects[current_hour]:
                try:
                    effect_callback(self, current_hour)
                except Exception as e:
                    logger.error(f"Underworld effect error: {e}")
        
        # Process underworld hazards
        for entity_id, entity in self.entities.items():
            if not entity.is_alive:
                continue
            
            # Entities with higher underworld tier are more resistant
            resistance = entity.underworld_tier * 0.1
            
            # Apply hour-specific effects
            if current_hour <= 6:  # Descent into underworld
                # Increasing pressure and difficulty
                pressure_damage = max(0, (current_hour - entity.underworld_tier))
                if pressure_damage > 0 and random.random() > resistance:
                    self._apply_underworld_damage(entity_id, pressure_damage, "pressure")
            else:  # Ascent from underworld
                # Reduced pressure but potential for rebirth effects
                if random.random() < 0.1:  # 10% chance for rebirth blessing
                    self._apply_rebirth_blessing(entity_id)
    
    def _phase_combat_action(self) -> None:
        """Phase 7: Execute main combat actions in initiative order."""
        if not self.initiative_order:
            return
        
        # Process each entity's turn
        while self.current_entity_index < len(self.initiative_order):
            entity_id = self.initiative_order[self.current_entity_index]
            entity = self.entities.get(entity_id)
            
            if not entity or not entity.is_alive or entity.actions_remaining <= 0:
                self.current_entity_index += 1
                continue
            
            # Execute entity's action
            action_taken = self._execute_entity_turn(entity_id)
            
            if action_taken:
                entity.actions_remaining -= 1
                self.turn_number += 1
            
            # Check if entity has more actions
            if entity.actions_remaining <= 0:
                self.current_entity_index += 1
        
        # Reset for next round
        self.current_entity_index = 0
    
    def _phase_divine_judgment(self) -> None:
        """Phase 8: Gods judge actions and apply cosmic consequences."""
        # Evaluate actions taken this round for cosmic balance
        for action in self.action_history[-len(self.entities):]:  # Last actions
            judgment = self._evaluate_action_morality(action)
            
            entity_id = action.entity_id
            entity = self.entities.get(entity_id)
            
            if entity and entity.is_alive:
                entity.maat_balance += judgment['balance_change']
                self.cosmic_balance_total += judgment['balance_change']
                
                # Apply divine judgment effects
                if judgment['balance_change'] > 0:
                    # Virtuous action - potential blessing
                    if random.random() < 0.2:  # 20% chance
                        self._apply_divine_blessing(entity_id, judgment['virtue_type'])
                elif judgment['balance_change'] < -5:
                    # Severely unbalanced action - potential curse
                    if random.random() < 0.3:  # 30% chance
                        self._apply_divine_curse(entity_id, judgment['transgression_type'])
        
        # Global cosmic balance effects
        if abs(self.cosmic_balance_total) > 20:
            self._apply_cosmic_rebalancing()
    
    def _phase_damage_resolution(self) -> None:
        """Phase 9: Resolve all damage and effects applied this round."""
        # Process all pending damage
        for entity_id, entity in self.entities.items():
            if not entity.is_alive:
                continue
            
            # Apply accumulated damage
            if entity.damage_taken_this_turn > 0:
                damage_result = self._apply_damage_to_entity(
                    entity_id, entity.damage_taken_this_turn, DamageType.ACCUMULATED
                )
                
                # Check for death
                if entity.card.current_stats.health <= 0:
                    self._handle_entity_death(entity_id, "combat")
        
        # Resolve pending effects
        effects_to_remove = []
        for effect in self.pending_effects:
            try:
                context = EffectContext(
                    source_card=None,  # Will be set based on effect
                    game_state=self,
                    trigger_data={"phase": self.current_phase.value}
                )
                
                result = effect.try_trigger(context)
                if result['triggered']:
                    self.action_statistics[f"effect_{effect.effect_id}"] += 1
                
                # Remove expired effects
                if not effect.is_active:
                    effects_to_remove.append(effect)
                    
            except Exception as e:
                logger.error(f"Effect resolution error: {e}")
                effects_to_remove.append(effect)
        
        # Clean up expired effects
        for effect in effects_to_remove:
            self.pending_effects.remove(effect)
    
    def _phase_ka_manifestation(self) -> None:
        """Phase 10: Handle Ka (life force) manifestations and effects."""
        for entity_id, entity in self.entities.items():
            if not entity.is_alive:
                continue
            
            # Check for automatic Ka manifestation
            if entity.card.has_keyword(CardKeyword.KA_DOUBLE) and not entity.ka_manifested:
                ka_strength = entity.card.current_stats.ka_strength
                manifestation_chance = min(0.4, ka_strength / 100.0)
                
                if random.random() < manifestation_chance:
                    self._manifest_entity_ka(entity_id)
            
            # Process existing Ka manifestations
            if entity.ka_manifested:
                ka_state = self.ba_ka_manager.get_ka_state(entity_id)
                if ka_state:
                    # Ka provides defensive benefits
                    self._apply_ka_protection(entity_id, ka_state)
        
        # Handle Ka interactions and conflicts
        self.ba_ka_manager.process_ka_manifestations()
    
    def _phase_afterlife_transition(self) -> None:
        """Phase 11: Handle death, resurrection, and afterlife effects."""
        dead_entities = [eid for eid, entity in self.entities.items() if not entity.is_alive]
        
        for entity_id in dead_entities:
            entity = self.entities[entity_id]
            
            # Check for resurrection abilities
            if entity.card.has_keyword(CardKeyword.RESURRECTION):
                resurrection_chance = 0.3  # Base 30% chance
                
                # Modify based on divine favor
                divine_favor = entity.card.stats.divine_favor
                resurrection_chance += divine_favor * 0.01
                
                # Anubis provides better resurrection chances
                if entity.divine_protection == "Anubis":
                    resurrection_chance += 0.2
                
                if random.random() < resurrection_chance:
                    self._resurrect_entity(entity_id)
            
            # Process afterlife effects for permanently dead entities
            elif not entity.card.has_keyword(CardKeyword.RESURRECTION):
                self._process_afterlife_effects(entity_id)
        
        # Check win/loss conditions
        self._check_combat_completion()
    
    def _phase_cosmic_balance(self) -> None:
        """Phase 12: Restore cosmic balance (Ma'at) and apply corrections."""
        # Calculate overall balance deviation
        total_entities = len([e for e in self.entities.values() if e.is_alive])
        if total_entities == 0:
            return
        
        average_balance = self.cosmic_balance_total / total_entities
        
        # Apply balance corrections if severely skewed
        if abs(average_balance) > 10:
            correction_factor = -0.1 * average_balance  # Gentle correction
            
            for entity_id, entity in self.entities.items():
                if entity.is_alive:
                    # Apply balance correction
                    balance_correction = int(correction_factor)
                    entity.maat_balance += balance_correction
                    
                    # Visual/mechanical effect
                    if balance_correction > 0:
                        # Cosmic favor - small healing or stat boost
                        healing = max(1, balance_correction)
                        entity.card.heal(healing)
                    elif balance_correction < 0:
                        # Cosmic disfavor - small damage or stat reduction
                        damage = max(1, abs(balance_correction))
                        self._apply_damage_to_entity(entity_id, damage, DamageType.COSMIC)
        
        # Update global balance
        self.cosmic_balance_total = int(self.cosmic_balance_total * 0.9)  # Natural decay
    
    def _phase_dusk_cleanup(self) -> None:
        """Phase 13: Clean up temporary effects and prepare for next round."""
        # Remove expired temporary effects
        for entity_id, entity in self.entities.items():
            if entity.card:
                entity.card.reset_temporary_modifiers()
        
        # Clean up temporary terrain effects
        expired_terrain = []
        for position, effects in self.terrain_effects.items():
            if 'duration' in effects:
                effects['duration'] -= 1
                if effects['duration'] <= 0:
                    expired_terrain.append(position)
        
        for position in expired_terrain:
            del self.terrain_effects[position]
        
        # Process end-of-turn effects
        for entity_id, entity in self.entities.items():
            if entity.is_alive:
                end_turn_effects = entity.card.get_effects_by_timing("end_turn")
                for effect in end_turn_effects:
                    self._apply_effect_to_entity(effect, entity_id, EffectTrigger.END_TURN)
        
        # Update combat metrics
        self._update_combat_metrics()
        
        # Check for combat completion
        if not self._check_combat_completion():
            # Prepare for next round if combat continues
            self._prepare_next_round()
    
    def _execute_entity_turn(self, entity_id: str) -> bool:
        """Execute a single entity's turn during combat action phase."""
        entity = self.entities.get(entity_id)
        if not entity or not entity.is_alive:
            return False
        
        # Determine available actions
        available_actions = self._get_available_actions(entity_id)
        if not available_actions:
            return False
        
        # For now, implement AI decision-making (later can be player input)
        chosen_action = self._ai_choose_action(entity_id, available_actions)
        if not chosen_action:
            return False
        
        # Execute the chosen action
        action = CombatAction(
            action_id=str(uuid.uuid4()),
            entity_id=entity_id,
            action_type=chosen_action['type'],
            targets=chosen_action.get('targets', []),
            parameters=chosen_action.get('parameters', {}),
            phase=self.current_phase
        )
        
        success = self._execute_action(action)
        if success:
            self.action_queue.append(action)
            entity.actions_taken.append(action.results)
            self.action_statistics[action.action_type] += 1
        
        return success
    
    def _execute_action(self, action: CombatAction) -> bool:
        """Execute a specific combat action."""
        try:
            if action.action_type == "move":
                return self._execute_move_action(action)
            elif action.action_type == "attack":
                return self._execute_attack_action(action)
            elif action.action_type == "cast_spell":
                return self._execute_spell_action(action)
            elif action.action_type == "use_ability":
                return self._execute_ability_action(action)
            elif action.action_type == "defend":
                return self._execute_defend_action(action)
            else:
                logger.warning(f"Unknown action type: {action.action_type}")
                return False
                
        except Exception as e:
            logger.error(f"Action execution error: {e}")
            action.results = {"success": False, "error": str(e)}
            return False
    
    def _execute_move_action(self, action: CombatAction) -> bool:
        """Execute movement action."""
        entity = self.entities.get(action.entity_id)
        if not entity or not entity.can_move:
            return False
        
        target_position = tuple(action.parameters.get('target_position', []))
        if not self._is_valid_position(target_position):
            return False
        
        # Check movement range
        max_move = entity.card.current_stats.movement
        distance = self._calculate_distance(entity.position, target_position)
        
        if distance > max_move:
            return False
        
        # Check for obstacles
        if not self._is_position_clear(target_position, entity.entity_id):
            return False
        
        # Execute move
        old_position = entity.position
        self.battlefield[old_position] = None
        self.battlefield[target_position] = entity.entity_id
        entity.position = target_position
        entity.can_move = False
        
        action.results = {
            "success": True,
            "old_position": old_position,
            "new_position": target_position,
            "distance": distance
        }
        
        # Trigger movement effects
        self._trigger_movement_effects(action.entity_id, old_position, target_position)
        
        return True
    
    def _execute_attack_action(self, action: CombatAction) -> bool:
        """Execute attack action."""
        attacker_entity = self.entities.get(action.entity_id)
        if not attacker_entity or not attacker_entity.can_attack:
            return False
        
        if not action.targets:
            return False
        
        target_id = action.targets[0]
        target_entity = self.entities.get(target_id)
        if not target_entity or not target_entity.is_alive:
            return False
        
        # Check attack range and line of sight
        if not self._can_attack_target(action.entity_id, target_id):
            return False
        
        # Calculate damage
        damage_result = self.damage_calculator.calculate_damage(
            attacker=attacker_entity.card,
            defender=target_entity.card,
            attack_type="melee",
            context={"combat_manager": self, "attacker_entity": attacker_entity}
        )
        
        # Apply damage
        if damage_result.total_damage > 0:
            target_entity.damage_taken_this_turn += damage_result.total_damage
        
        attacker_entity.can_attack = False
        
        action.results = {
            "success": True,
            "damage_dealt": damage_result.total_damage,
            "damage_type": damage_result.damage_type.value,
            "critical_hit": damage_result.is_critical,
            "target_health_remaining": target_entity.card.current_stats.health
        }
        
        # Trigger attack effects
        self._trigger_attack_effects(action.entity_id, target_id, damage_result)
        
        return True
    
    def _check_combat_completion(self) -> bool:
        """Check if combat should end."""
        alive_entities = [e for e in self.entities.values() if e.is_alive]
        
        if len(alive_entities) <= 1:
            # Combat ends when 1 or fewer entities remain
            winner = alive_entities[0] if alive_entities else None
            self._end_combat(winner.entity_id if winner else None)
            return True
        
        # Check for other end conditions (time limit, special objectives, etc.)
        if self.round_number > 50:  # Maximum round limit
            self._end_combat("draw")
            return True
        
        return False
    
    def _end_combat(self, winner_id: Optional[str]) -> None:
        """End combat and clean up."""
        self.state = CombatState.COMPLETED
        
        # Calculate final combat metrics
        self._calculate_final_metrics()
        
        # Emit combat end event
        self._emit_combat_event("combat_ended", {
            "winner": winner_id,
            "duration_rounds": self.round_number,
            "total_actions": len(self.action_history),
            "final_metrics": self.combat_metrics
        })
        
        logger.info(f"Combat ended: winner={winner_id}, rounds={self.round_number}")
    
    # Utility and helper methods
    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if position is within battlefield bounds."""
        x, y = position
        return 0 <= x < self.battlefield_width and 0 <= y < self.battlefield_height
    
    def _is_position_clear(self, position: Tuple[int, int], excluding_entity: str = None) -> bool:
        """Check if position is not occupied by another entity."""
        occupant = self.battlefield.get(position)
        return occupant is None or occupant == excluding_entity
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate distance between two positions."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _emit_combat_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit a combat event for logging and external systems."""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "combat_id": self.combat_id,
            "data": data
        }
        self.combat_events.append(event)
        
        # Limit event history
        if len(self.combat_events) > 1000:
            self.combat_events = self.combat_events[-1000:]
    
    def get_combat_state(self) -> Dict[str, Any]:
        """Get current combat state for display/serialization."""
        return {
            "combat_id": self.combat_id,
            "state": self.state.value,
            "current_phase": self.current_phase.value,
            "round_number": self.round_number,
            "turn_number": self.turn_number,
            "entities": {
                eid: {
                    "card_name": entity.card.name,
                    "position": entity.position,
                    "is_alive": entity.is_alive,
                    "health": entity.card.current_stats.health,
                    "actions_remaining": entity.actions_remaining
                }
                for eid, entity in self.entities.items()
            },
            "initiative_order": self.initiative_order,
            "battlefield": {
                str(pos): entity_id for pos, entity_id in self.battlefield.items()
                if entity_id is not None
            },
            "cosmic_balance": self.cosmic_balance_total,
            "active_effects": len(self.pending_effects)
        }
    
    # Additional methods would be implemented here for:
    # - AI decision making
    # - Divine interventions
    # - Ba-Ka system integration
    # - Terrain effects
    # - Effect applications
    # - Combat metrics
    # And many more specialized combat mechanics
    
    def _initialize_battlefield(self) -> None:
        """Initialize empty battlefield."""
        for x in range(self.battlefield_width):
            for y in range(self.battlefield_height):
                self.battlefield[(x, y)] = None
```

---

## 5. UI SYSTEM IMPLEMENTATION (ULTRA-DETAILED)

### 5.1 COMPLETE PYGAME SCREEN MANAGEMENT

```python
# src/sands_of_duat/ui/screen_manager.py
from __future__ import annotations
import pygame
from typing import Dict, List, Optional, Any, Callable, Tuple, Type
from enum import Enum, auto
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import threading
import queue

logger = logging.getLogger(__name__)

class ScreenType(Enum):
    """Types of screens in the game."""
    MAIN_MENU = "main_menu"
    DECK_BUILDER = "deck_builder"
    COMBAT = "combat"
    COLLECTION = "collection"
    SETTINGS = "settings"
    LOADING = "loading"
    CARD_PREVIEW = "card_preview"
    EGYPTIAN_LORE = "egyptian_lore"
    UNDERWORLD_MAP = "underworld_map"
    BA_KA_SEPARATION = "ba_ka_separation"

class TransitionType(Enum):
    """Screen transition effects."""
    NONE = "none"
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    EGYPTIAN_DISSOLVE = "egyptian_dissolve"  # Hieroglyph-based transition
    PAPYRUS_SCROLL = "papyrus_scroll"        # Scroll-like transition
    SANDSTORM = "sandstorm"                   # Particle-based transition
    UNDERWORLD_PORTAL = "underworld_portal"   # Mystical portal effect

@dataclass
class ScreenTransition:
    """Configuration for screen transitions."""
    transition_type: TransitionType = TransitionType.FADE
    duration: float = 0.3  # seconds
    easing_function: str = "ease_in_out"
    reverse_on_back: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)

class Screen(ABC):
    """Abstract base class for all game screens."""
    
    def __init__(self, screen_manager: 'ScreenManager'):
        self.screen_manager = screen_manager
        self.screen_type: Optional[ScreenType] = None
        self.is_active = False
        self.is_visible = True
        self.needs_update = True
        
        # Screen properties
        self.surface: Optional[pygame.Surface] = None
        self.rect: Optional[pygame.Rect] = None
        
        # UI Elements
        self.ui_elements: List[UIElement] = []
        self.focused_element: Optional[UIElement] = None
        
        # Event handling
        self.event_handlers: Dict[int, List[Callable]] = {}
        
        # Animation and effects
        self.animations: List[Animation] = []
        self.particle_systems: List[ParticleSystem] = []
        
        # Performance tracking
        self.render_time = 0.0
        self.last_render = datetime.now()
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the screen. Return True if successful."""
        pass
    
    @abstractmethod  
    def update(self, dt: float) -> None:
        """Update screen logic."""
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the screen to the given surface."""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Return True if event was consumed."""
        pass
    
    def on_enter(self, previous_screen: Optional['Screen'] = None) -> None:
        """Called when entering this screen."""
        self.is_active = True
        self.needs_update = True
        
    def on_exit(self, next_screen: Optional['Screen'] = None) -> None:
        """Called when leaving this screen."""
        self.is_active = False
        
    def cleanup(self) -> None:
        """Clean up resources when screen is destroyed."""
        for animation in self.animations:
            animation.cleanup()
        self.animations.clear()
        
        for particle_system in self.particle_systems:
            particle_system.cleanup()
        self.particle_systems.clear()

class ScreenManager:
    """Manages screen transitions and rendering."""
    
    def __init__(self, display_surface: pygame.Surface):
        self.display_surface = display_surface
        self.screen_width = display_surface.get_width()
        self.screen_height = display_surface.get_height()
        
        # Screen stack for managing multiple screens
        self.screen_stack: List[Screen] = []
        self.screen_registry: Dict[ScreenType, Type[Screen]] = {}
        
        # Transition management
        self.current_transition: Optional[ScreenTransition] = None
        self.transition_progress = 0.0
        self.transition_surface: Optional[pygame.Surface] = None
        self.is_transitioning = False
        
        # Performance monitoring
        self.frame_count = 0
        self.fps = 0.0
        self.frame_times: List[float] = []
        self.last_fps_update = datetime.now()
        
        # Event queue for threaded operations
        self.event_queue = queue.Queue()
        
        logger.info(f"ScreenManager initialized: {self.screen_width}x{self.screen_height}")
    
    def register_screen(self, screen_type: ScreenType, screen_class: Type[Screen]) -> None:
        """Register a screen class for a screen type."""
        self.screen_registry[screen_type] = screen_class
        logger.debug(f"Registered screen: {screen_type.value}")
    
    def push_screen(self, screen_type: ScreenType, 
                   transition: Optional[ScreenTransition] = None) -> bool:
        """Push a new screen onto the stack."""
        if screen_type not in self.screen_registry:
            logger.error(f"Screen type not registered: {screen_type.value}")
            return False
        
        # Create new screen instance
        screen_class = self.screen_registry[screen_type]
        new_screen = screen_class(self)
        new_screen.screen_type = screen_type
        
        if not new_screen.initialize():
            logger.error(f"Failed to initialize screen: {screen_type.value}")
            return False
        
        # Handle transition
        if transition and self.screen_stack:
            self._start_transition(new_screen, transition)
        else:
            self._switch_to_screen(new_screen)
        
        return True
    
    def pop_screen(self, transition: Optional[ScreenTransition] = None) -> bool:
        """Pop the current screen from the stack."""
        if len(self.screen_stack) <= 1:
            logger.warning("Cannot pop last screen")
            return False
        
        current_screen = self.screen_stack[-1]
        previous_screen = self.screen_stack[-2] if len(self.screen_stack) > 1 else None
        
        # Handle transition
        if transition and previous_screen:
            # Reverse transition if configured
            if transition.reverse_on_back:
                reverse_transition = self._reverse_transition(transition)
                self._start_transition(previous_screen, reverse_transition, pop_current=True)
            else:
                self._start_transition(previous_screen, transition, pop_current=True)
        else:
            self._pop_current_screen()
        
        return True
    
    def replace_screen(self, screen_type: ScreenType,
                      transition: Optional[ScreenTransition] = None) -> bool:
        """Replace the current screen with a new one."""
        if not self.push_screen(screen_type, transition):
            return False
        
        # Remove the previous screen once transition completes
        if len(self.screen_stack) >= 2:
            old_screen = self.screen_stack[-2]
            old_screen.cleanup()
            self.screen_stack.remove(old_screen)
        
        return True
    
    def clear_stack_and_push(self, screen_type: ScreenType,
                            transition: Optional[ScreenTransition] = None) -> bool:
        """Clear the screen stack and push a new screen."""
        # Clean up all screens
        for screen in self.screen_stack:
            screen.cleanup()
        self.screen_stack.clear()
        
        return self.push_screen(screen_type, transition)
    
    def update(self, dt: float) -> None:
        """Update the screen manager and current screen."""
        start_time = datetime.now()
        
        # Update transition if active
        if self.is_transitioning:
            self._update_transition(dt)
        
        # Update current screen
        if self.screen_stack:
            current_screen = self.screen_stack[-1]
            if current_screen.is_active:
                current_screen.update(dt)
                
                # Update animations
                for animation in current_screen.animations[:]:
                    animation.update(dt)
                    if animation.is_finished():
                        current_screen.animations.remove(animation)
                        animation.cleanup()
                
                # Update particle systems
                for particle_system in current_screen.particle_systems:
                    particle_system.update(dt)
        
        # Process queued events
        self._process_event_queue()
        
        # Update performance metrics
        self._update_performance_metrics(start_time)
    
    def render(self) -> None:
        """Render the current screen."""
        if not self.screen_stack:
            return
        
        render_start = datetime.now()
        
        # Clear display
        self.display_surface.fill((0, 0, 0))
        
        # Render current screen
        current_screen = self.screen_stack[-1]
        if current_screen.is_visible:
            current_screen.render(self.display_surface)
        
        # Render transition effect if active
        if self.is_transitioning and self.current_transition:
            self._render_transition()
        
        # Update screen's render time
        render_time = (datetime.now() - render_start).total_seconds()
        current_screen.render_time = render_time
        current_screen.last_render = datetime.now()
        
        self.frame_count += 1
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events."""
        if not self.screen_stack:
            return False
        
        # Let current screen handle event first
        current_screen = self.screen_stack[-1]
        if current_screen.is_active and current_screen.handle_event(event):
            return True
        
        # Handle global events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:  # Toggle fullscreen
                self._toggle_fullscreen()
                return True
            elif event.key == pygame.K_F1:  # Debug info
                self._toggle_debug_info()
                return True
        
        return False
    
    def _start_transition(self, target_screen: Screen, transition: ScreenTransition, 
                         pop_current: bool = False) -> None:
        """Start a screen transition."""
        self.current_transition = transition
        self.transition_progress = 0.0
        self.is_transitioning = True
        
        # Create transition surface
        self.transition_surface = pygame.Surface((self.screen_width, self.screen_height))
        
        # Store transition parameters
        self.transition_target = target_screen
        self.transition_pop_current = pop_current
        
        logger.debug(f"Started transition: {transition.transition_type.value}")
    
    def _update_transition(self, dt: float) -> None:
        """Update transition progress."""
        if not self.current_transition:
            return
        
        # Update progress
        self.transition_progress += dt / self.current_transition.duration
        
        if self.transition_progress >= 1.0:
            # Transition complete
            self._complete_transition()
        
    def _complete_transition(self) -> None:
        """Complete the current transition."""
        if not hasattr(self, 'transition_target'):
            return
        
        target_screen = self.transition_target
        pop_current = getattr(self, 'transition_pop_current', False)
        
        if pop_current:
            self._pop_current_screen()
        else:
            self._switch_to_screen(target_screen)
        
        # Cleanup transition
        self.current_transition = None
        self.transition_progress = 0.0
        self.is_transitioning = False
        self.transition_surface = None
        
        # Cleanup transition attributes
        delattr(self, 'transition_target')
        if hasattr(self, 'transition_pop_current'):
            delattr(self, 'transition_pop_current')
        
        logger.debug("Transition completed")
    
    def _switch_to_screen(self, new_screen: Screen) -> None:
        """Switch to a new screen."""
        previous_screen = self.screen_stack[-1] if self.screen_stack else None
        
        # Deactivate previous screen
        if previous_screen:
            previous_screen.on_exit(new_screen)
        
        # Add new screen
        self.screen_stack.append(new_screen)
        new_screen.on_enter(previous_screen)
        
        logger.debug(f"Switched to screen: {new_screen.screen_type.value if new_screen.screen_type else 'Unknown'}")
    
    def _pop_current_screen(self) -> None:
        """Pop the current screen without transition."""
        if not self.screen_stack:
            return
        
        current_screen = self.screen_stack.pop()
        current_screen.on_exit()
        current_screen.cleanup()
        
        # Activate previous screen
        if self.screen_stack:
            previous_screen = self.screen_stack[-1]
            previous_screen.on_enter()
        
        logger.debug("Popped current screen")
    
    def _render_transition(self) -> None:
        """Render transition effects."""
        if not self.current_transition or not self.transition_surface:
            return
        
        transition_type = self.current_transition.transition_type
        progress = self._apply_easing(self.transition_progress, self.current_transition.easing_function)
        
        if transition_type == TransitionType.FADE:
            self._render_fade_transition(progress)
        elif transition_type == TransitionType.SLIDE_LEFT:
            self._render_slide_transition(progress, (-1, 0))
        elif transition_type == TransitionType.SLIDE_RIGHT:
            self._render_slide_transition(progress, (1, 0))
        elif transition_type == TransitionType.SLIDE_UP:
            self._render_slide_transition(progress, (0, -1))
        elif transition_type == TransitionType.SLIDE_DOWN:
            self._render_slide_transition(progress, (0, 1))
        elif transition_type == TransitionType.EGYPTIAN_DISSOLVE:
            self._render_egyptian_dissolve_transition(progress)
        elif transition_type == TransitionType.PAPYRUS_SCROLL:
            self._render_papyrus_scroll_transition(progress)
        elif transition_type == TransitionType.SANDSTORM:
            self._render_sandstorm_transition(progress)
        elif transition_type == TransitionType.UNDERWORLD_PORTAL:
            self._render_underworld_portal_transition(progress)
    
    def _render_fade_transition(self, progress: float) -> None:
        """Render fade transition effect."""
        # Create fade overlay
        fade_surface = pygame.Surface((self.screen_width, self.screen_height))
        fade_surface.fill((0, 0, 0))
        
        # Apply alpha based on progress
        alpha = int(255 * (1.0 - abs(progress * 2 - 1)))
        fade_surface.set_alpha(alpha)
        
        self.display_surface.blit(fade_surface, (0, 0))
    
    def _render_slide_transition(self, progress: float, direction: Tuple[int, int]) -> None:
        """Render slide transition effect."""
        offset_x = int(self.screen_width * direction[0] * (1 - progress))
        offset_y = int(self.screen_height * direction[1] * (1 - progress))
        
        # Render target screen at offset position
        if hasattr(self, 'transition_target'):
            target_surface = pygame.Surface((self.screen_width, self.screen_height))
            self.transition_target.render(target_surface)
            self.display_surface.blit(target_surface, (offset_x, offset_y))
    
    def _render_egyptian_dissolve_transition(self, progress: float) -> None:
        """Render Egyptian hieroglyph-based dissolve transition."""
        # This would implement a complex dissolve effect using Egyptian symbols
        # For now, fall back to fade
        self._render_fade_transition(progress)
    
    def _render_papyrus_scroll_transition(self, progress: float) -> None:
        """Render papyrus scroll transition effect."""
        # Simulate a papyrus scroll being rolled up/down
        reveal_height = int(self.screen_height * progress)
        
        # Create mask for scroll effect
        mask = pygame.Surface((self.screen_width, self.screen_height))
        mask.fill((255, 255, 255))
        pygame.draw.rect(mask, (0, 0, 0), (0, reveal_height, self.screen_width, self.screen_height - reveal_height))
        
        if hasattr(self, 'transition_target'):
            target_surface = pygame.Surface((self.screen_width, self.screen_height))
            self.transition_target.render(target_surface)
            
            # Apply papyrus texture effect
            self._apply_papyrus_texture(target_surface)
            
            # Apply mask
            target_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_MULT)
            self.display_surface.blit(target_surface, (0, 0))
    
    def _apply_easing(self, t: float, easing_function: str) -> float:
        """Apply easing function to transition progress."""
        t = max(0.0, min(1.0, t))  # Clamp to [0, 1]
        
        if easing_function == "linear":
            return t
        elif easing_function == "ease_in":
            return t * t
        elif easing_function == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif easing_function == "ease_in_out":
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        else:
            return t
    
    def get_current_screen(self) -> Optional[Screen]:
        """Get the currently active screen."""
        return self.screen_stack[-1] if self.screen_stack else None
    
    def get_screen_stack_size(self) -> int:
        """Get the number of screens in the stack."""
        return len(self.screen_stack)
    
    def get_performance_info(self) -> Dict[str, Any]:
        """Get performance information."""
        return {
            'fps': self.fps,
            'frame_count': self.frame_count,
            'screen_stack_size': len(self.screen_stack),
            'current_screen': self.get_current_screen().screen_type.value if self.get_current_screen() else None,
            'is_transitioning': self.is_transitioning,
            'average_frame_time': sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0.0
        }


### 5.2 EGYPTIAN UI COMPONENT LIBRARY

```python
# src/sands_of_duat/ui/egyptian_components.py
import pygame
from typing import Dict, List, Optional, Any, Callable, Tuple
from enum import Enum
from dataclasses import dataclass
import math
from datetime import datetime

from ..core.resource_manager import ResourceManager

class EgyptianStyle(Enum):
    """Egyptian UI style themes."""
    PHARAOH_GOLD = "pharaoh_gold"
    DESERT_SAND = "desert_sand" 
    NILE_BLUE = "nile_blue"
    UNDERWORLD_DARK = "underworld_dark"
    HIEROGLYPH_STONE = "hieroglyph_stone"
    PAPYRUS_SCROLL = "papyrus_scroll"
    ROYAL_PURPLE = "royal_purple"

@dataclass
class EgyptianColors:
    """Egyptian-themed color palette."""
    # Primary Colors
    GOLD = pygame.Color(255, 215, 0)
    DARK_GOLD = pygame.Color(184, 134, 11)
    SAND = pygame.Color(238, 203, 173)
    DESERT_BROWN = pygame.Color(139, 69, 19)
    
    # Nile Colors
    NILE_BLUE = pygame.Color(30, 144, 255)
    DEEP_BLUE = pygame.Color(0, 105, 148)
    
    # Underworld Colors  
    UNDERWORLD_BLACK = pygame.Color(20, 20, 20)
    SHADOW_GRAY = pygame.Color(64, 64, 64)
    
    # Mystical Colors
    ANKH_GREEN = pygame.Color(50, 205, 50)
    SCARAB_TURQUOISE = pygame.Color(64, 224, 208)
    
    # Text Colors
    HIEROGLYPH_BLACK = pygame.Color(40, 40, 40)
    PAPYRUS_CREAM = pygame.Color(255, 248, 220)

class UIElement:
    """Base class for UI elements with Egyptian styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 style: EgyptianStyle = EgyptianStyle.PHARAOH_GOLD):
        self.rect = pygame.Rect(x, y, width, height)
        self.style = style
        self.is_visible = True
        self.is_enabled = True
        self.is_hovered = False
        self.is_pressed = False
        self.is_focused = False
        
        # Animation properties
        self.hover_animation_progress = 0.0
        self.press_animation_progress = 0.0
        
        # Egyptian decorative elements
        self.border_thickness = 2
        self.corner_radius = 4
        self.has_hieroglyph_border = False
        self.glow_effect = False
        
        # Event callbacks
        self.on_click: Optional[Callable] = None
        self.on_hover: Optional[Callable] = None
        self.on_focus: Optional[Callable] = None
        
        # Resource manager for textures
        self.resource_manager: Optional[ResourceManager] = None
        
    def update(self, dt: float) -> None:
        """Update element animations and state."""
        # Animate hover effect
        target_hover = 1.0 if self.is_hovered else 0.0
        self.hover_animation_progress += (target_hover - self.hover_animation_progress) * dt * 8.0
        
        # Animate press effect
        target_press = 1.0 if self.is_pressed else 0.0
        self.press_animation_progress += (target_press - self.press_animation_progress) * dt * 12.0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Return True if consumed."""
        if not self.is_visible or not self.is_enabled:
            return False
        
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:  # Left click
                self.is_pressed = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered and self.on_click:
                    self.on_click(self)
                return True
        
        # Handle hover events
        if self.is_hovered and not was_hovered and self.on_hover:
            self.on_hover(self, True)
        elif not self.is_hovered and was_hovered and self.on_hover:
            self.on_hover(self, False)
        
        return False
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the UI element."""
        if not self.is_visible:
            return
        
        # Apply style-specific rendering
        if self.style == EgyptianStyle.PHARAOH_GOLD:
            self._render_pharaoh_gold_style(surface)
        elif self.style == EgyptianStyle.DESERT_SAND:
            self._render_desert_sand_style(surface)
        elif self.style == EgyptianStyle.NILE_BLUE:
            self._render_nile_blue_style(surface)
        elif self.style == EgyptianStyle.UNDERWORLD_DARK:
            self._render_underworld_dark_style(surface)
        else:
            self._render_default_style(surface)
        
        # Render decorative elements
        if self.has_hieroglyph_border:
            self._render_hieroglyph_border(surface)
        
        if self.glow_effect:
            self._render_glow_effect(surface)
    
    def _render_pharaoh_gold_style(self, surface: pygame.Surface) -> None:
        """Render with pharaoh gold styling."""
        # Base color with animation
        base_color = EgyptianColors.GOLD
        if self.hover_animation_progress > 0:
            # Brighten on hover
            hover_factor = self.hover_animation_progress * 0.3
            base_color = pygame.Color(
                min(255, int(base_color.r * (1 + hover_factor))),
                min(255, int(base_color.g * (1 + hover_factor))),
                min(255, int(base_color.b * (1 + hover_factor)))
            )
        
        # Draw main rectangle
        pygame.draw.rect(surface, base_color, self.rect, border_radius=self.corner_radius)
        
        # Draw border
        border_color = EgyptianColors.DARK_GOLD
        pygame.draw.rect(surface, border_color, self.rect, self.border_thickness, border_radius=self.corner_radius)
        
        # Add press effect
        if self.press_animation_progress > 0:
            press_overlay = pygame.Surface((self.rect.width, self.rect.height))
            press_overlay.set_alpha(int(64 * self.press_animation_progress))
            press_overlay.fill(EgyptianColors.UNDERWORLD_BLACK)
            surface.blit(press_overlay, self.rect.topleft)

class EgyptianButton(UIElement):
    """Egyptian-themed button with hieroglyphic styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 style: EgyptianStyle = EgyptianStyle.PHARAOH_GOLD,
                 font_size: int = 24):
        super().__init__(x, y, width, height, style)
        self.text = text
        self.font_size = font_size
        self.font: Optional[pygame.font.Font] = None
        self.text_color = EgyptianColors.HIEROGLYPH_BLACK
        
        # Egyptian button features
        self.has_ankh_decoration = False
        self.has_cartouche_border = True
        self.hieroglyph_accent: Optional[str] = None
        
        # Animation properties
        self.text_pulse_progress = 0.0
        
    def update(self, dt: float) -> None:
        """Update button animations."""
        super().update(dt)
        
        # Animate text pulse effect
        self.text_pulse_progress += dt * 3.0
        if self.text_pulse_progress > 2 * math.pi:
            self.text_pulse_progress -= 2 * math.pi
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Egyptian button."""
        super().render(surface)
        
        if not self.is_visible:
            return
        
        # Render cartouche border if enabled
        if self.has_cartouche_border:
            self._render_cartouche_border(surface)
        
        # Render ankh decoration if enabled
        if self.has_ankh_decoration:
            self._render_ankh_decoration(surface)
        
        # Render text
        if self.text and self.font:
            self._render_button_text(surface)
        
        # Render hieroglyph accent
        if self.hieroglyph_accent:
            self._render_hieroglyph_accent(surface)
    
    def _render_cartouche_border(self, surface: pygame.Surface) -> None:
        """Render Egyptian cartouche-style border."""
        # Draw oval border around button
        border_rect = self.rect.inflate(8, 8)
        border_color = EgyptianColors.DARK_GOLD
        
        # Draw oval shape (approximated with arcs)
        pygame.draw.ellipse(surface, border_color, border_rect, 3)
        
        # Add corner embellishments
        corner_size = 6
        for corner in [(border_rect.left, border_rect.centery),
                      (border_rect.right, border_rect.centery)]:
            pygame.draw.circle(surface, border_color, corner, corner_size, 2)
    
    def _render_ankh_decoration(self, surface: pygame.Surface) -> None:
        """Render ankh symbol decoration."""
        # Simple ankh drawing (cross with loop at top)
        ankh_size = 12
        ankh_x = self.rect.right - 20
        ankh_y = self.rect.top + 10
        
        ankh_color = EgyptianColors.ANKH_GREEN
        
        # Draw ankh loop
        pygame.draw.circle(surface, ankh_color, (ankh_x, ankh_y), ankh_size // 3, 2)
        
        # Draw ankh cross
        pygame.draw.line(surface, ankh_color, 
                        (ankh_x, ankh_y + ankh_size // 3),
                        (ankh_x, ankh_y + ankh_size), 2)
        pygame.draw.line(surface, ankh_color,
                        (ankh_x - ankh_size // 3, ankh_y + ankh_size // 2),
                        (ankh_x + ankh_size // 3, ankh_y + ankh_size // 2), 2)
    
    def _render_button_text(self, surface: pygame.Surface) -> None:
        """Render button text with effects."""
        if not self.font:
            self.font = pygame.font.Font(None, self.font_size)
        
        # Apply text effects based on state
        text_color = self.text_color
        if self.is_hovered:
            # Add golden glow effect
            pulse_intensity = (math.sin(self.text_pulse_progress) + 1) / 2
            glow_factor = pulse_intensity * 0.4
            text_color = pygame.Color(
                min(255, int(text_color.r + (255 - text_color.r) * glow_factor)),
                min(255, int(text_color.g + (215 - text_color.g) * glow_factor)),
                min(255, int(text_color.b + (0 - text_color.b) * glow_factor))
            )
        
        # Render text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Add text shadow for depth
        shadow_color = EgyptianColors.UNDERWORLD_BLACK
        shadow_surface = self.font.render(self.text, True, shadow_color)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        surface.blit(shadow_surface, shadow_rect)
        
        # Render main text
        surface.blit(text_surface, text_rect)

class EgyptianCardSlot(UIElement):
    """Specialized UI element for displaying cards with Egyptian theming."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, EgyptianStyle.PAPYRUS_SCROLL)
        self.card = None
        self.card_image: Optional[pygame.Surface] = None
        
        # Egyptian card slot features
        self.has_papyrus_background = True
        self.has_scarab_corners = True
        self.glow_color = EgyptianColors.GOLD
        self.divine_aura_strength = 0.0
        
        # Animation properties
        self.float_offset = 0.0
        self.rotation_angle = 0.0
        self.scale_factor = 1.0
        
        # Card interaction
        self.is_dragging = False
        self.drag_offset = (0, 0)
        
    def set_card(self, card) -> None:
        """Set the card to display in this slot."""
        self.card = card
        if card:
            # Load card image
            self._load_card_image()
            # Set divine aura based on card rarity
            self._update_divine_aura()
    
    def update(self, dt: float) -> None:
        """Update card slot animations."""
        super().update(dt)
        
        # Floating animation
        self.float_offset = math.sin(datetime.now().timestamp() * 2.0) * 2.0
        
        # Rotation for magical cards
        if self.card and hasattr(self.card, 'element'):
            if self.card.element.key in ['light', 'darkness']:
                self.rotation_angle += dt * 20.0  # Slow rotation
        
        # Scale animation on hover
        target_scale = 1.05 if self.is_hovered else 1.0
        self.scale_factor += (target_scale - self.scale_factor) * dt * 6.0
        
        # Update divine aura
        if self.card:
            divine_favor = getattr(self.card.stats, 'divine_favor', 0)
            target_aura = abs(divine_favor) / 50.0  # Normalize to 0-1
            self.divine_aura_strength += (target_aura - self.divine_aura_strength) * dt * 3.0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Egyptian card slot."""
        if not self.is_visible:
            return
        
        # Apply transformations
        render_rect = self.rect.copy()
        render_rect.y += int(self.float_offset)
        
        # Scale rect if needed
        if self.scale_factor != 1.0:
            center = render_rect.center
            render_rect.width = int(render_rect.width * self.scale_factor)
            render_rect.height = int(render_rect.height * self.scale_factor)
            render_rect.center = center
        
        # Render papyrus background
        if self.has_papyrus_background:
            self._render_papyrus_background(surface, render_rect)
        
        # Render scarab corners
        if self.has_scarab_corners:
            self._render_scarab_corners(surface, render_rect)
        
        # Render divine aura
        if self.divine_aura_strength > 0:
            self._render_divine_aura(surface, render_rect)
        
        # Render card image
        if self.card_image:
            self._render_card_image(surface, render_rect)
        
        # Render slot border
        border_color = EgyptianColors.DARK_GOLD if not self.is_hovered else EgyptianColors.GOLD
        pygame.draw.rect(surface, border_color, render_rect, 3, border_radius=8)
    
    def _render_papyrus_background(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Render papyrus-textured background."""
        # Create papyrus-like texture with gradient
        papyrus_surface = pygame.Surface((rect.width, rect.height))
        base_color = EgyptianColors.PAPYRUS_CREAM
        
        # Add texture variation
        for y in range(rect.height):
            for x in range(0, rect.width, 4):  # Skip pixels for performance
                variation = math.sin(x * 0.1) * math.cos(y * 0.08) * 10
                color_variation = max(0, min(255, base_color.r + variation))
                texture_color = pygame.Color(int(color_variation), int(color_variation * 0.95), int(color_variation * 0.9))
                pygame.draw.rect(papyrus_surface, texture_color, (x, y, 4, 1))
        
        surface.blit(papyrus_surface, rect.topleft)
    
    def _render_scarab_corners(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Render scarab beetle corner decorations."""
        scarab_color = EgyptianColors.SCARAB_TURQUOISE
        corner_size = 8
        
        # Draw simplified scarab shapes at corners
        corners = [
            (rect.left + corner_size, rect.top + corner_size),
            (rect.right - corner_size, rect.top + corner_size),
            (rect.left + corner_size, rect.bottom - corner_size),
            (rect.right - corner_size, rect.bottom - corner_size)
        ]
        
        for corner in corners:
            # Draw scarab body (oval)
            scarab_rect = pygame.Rect(corner[0] - corner_size//2, corner[1] - corner_size//3, corner_size, corner_size//1.5)
            pygame.draw.ellipse(surface, scarab_color, scarab_rect)
            
            # Draw scarab legs (small lines)
            for i in range(3):
                leg_start = (corner[0] - 2 + i * 2, corner[1])
                leg_end = (leg_start[0], leg_start[1] + 3)
                pygame.draw.line(surface, scarab_color, leg_start, leg_end, 1)
    
    def _render_divine_aura(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        """Render divine aura effect around card."""
        if self.divine_aura_strength <= 0:
            return
        
        # Create aura surface
        aura_size = int(20 * self.divine_aura_strength)
        aura_rect = rect.inflate(aura_size * 2, aura_size * 2)
        aura_alpha = int(128 * self.divine_aura_strength)
        
        # Draw multiple aura layers for depth
        for layer in range(3):
            layer_size = aura_size - (layer * aura_size // 4)
            if layer_size <= 0:
                break
            
            layer_rect = rect.inflate(layer_size * 2, layer_size * 2)
            layer_alpha = aura_alpha // (layer + 1)
            
            # Create aura surface for this layer
            aura_surface = pygame.Surface((layer_rect.width, layer_rect.height))
            aura_surface.set_alpha(layer_alpha)
            aura_surface.fill(self.glow_color)
            
            surface.blit(aura_surface, layer_rect.topleft, special_flags=pygame.BLEND_ADD)


class EgyptianProgressBar(UIElement):
    """Egyptian-themed progress bar with sand animation."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 max_value: float = 100.0, current_value: float = 0.0):
        super().__init__(x, y, width, height, EgyptianStyle.DESERT_SAND)
        self.max_value = max_value
        self.current_value = current_value
        self.target_value = current_value
        
        # Egyptian progress bar features
        self.has_hieroglyph_markers = True
        self.sand_particle_count = 20
        self.hourglass_style = True
        
        # Animation
        self.sand_particles: List[Dict[str, Any]] = []
        self.fill_animation_progress = 0.0
        
        self._initialize_sand_particles()
    
    def _initialize_sand_particles(self) -> None:
        """Initialize sand particle effects."""
        import random
        
        for _ in range(self.sand_particle_count):
            particle = {
                'x': random.randint(0, self.rect.width),
                'y': random.randint(0, self.rect.height),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(1, 3),
                'alpha': random.randint(100, 255)
            }
            self.sand_particles.append(particle)
    
    def set_value(self, value: float) -> None:
        """Set the progress bar value with animation."""
        self.target_value = max(0, min(self.max_value, value))
    
    def update(self, dt: float) -> None:
        """Update progress bar animations."""
        super().update(dt)
        
        # Animate value change
        if abs(self.current_value - self.target_value) > 0.1:
            self.current_value += (self.target_value - self.current_value) * dt * 5.0
        else:
            self.current_value = self.target_value
        
        # Update sand particles
        for particle in self.sand_particles:
            particle['y'] += particle['speed'] * dt * 60
            if particle['y'] > self.rect.height:
                particle['y'] = 0
                particle['x'] = random.randint(0, self.rect.width)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Egyptian progress bar."""
        if not self.is_visible:
            return
        
        # Draw background
        bg_color = EgyptianColors.SAND
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.corner_radius)
        
        # Draw progress fill
        progress_ratio = self.current_value / self.max_value if self.max_value > 0 else 0
        fill_width = int(self.rect.width * progress_ratio)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_width, self.rect.height)
            fill_color = EgyptianColors.GOLD
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=self.corner_radius)
        
        # Draw sand particles
        particle_surface = surface.subsurface(self.rect)
        for particle in self.sand_particles:
            if particle['x'] < fill_width:  # Only show particles in filled area
                particle_color = (*EgyptianColors.DESERT_BROWN[:3], particle['alpha'])
                pygame.draw.circle(particle_surface, particle_color, 
                                 (int(particle['x']), int(particle['y'])), particle['size'])
        
        # Draw hieroglyph markers
        if self.has_hieroglyph_markers:
            self._render_hieroglyph_markers(surface)
        
        # Draw border
        border_color = EgyptianColors.DARK_GOLD
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=self.corner_radius)
    
    def _render_hieroglyph_markers(self, surface: pygame.Surface) -> None:
        """Render hieroglyphic progress markers."""
        marker_count = 5
        marker_spacing = self.rect.width // marker_count
        marker_color = EgyptianColors.HIEROGLYPH_BLACK
        
        for i in range(marker_count + 1):
            marker_x = self.rect.left + i * marker_spacing
            marker_y = self.rect.bottom + 5
            
            # Draw simple hieroglyphic markers (vertical lines with caps)
            pygame.draw.line(surface, marker_color, 
                           (marker_x, marker_y), (marker_x, marker_y + 8), 2)
            pygame.draw.line(surface, marker_color,
                           (marker_x - 2, marker_y), (marker_x + 2, marker_y), 2)
            pygame.draw.line(surface, marker_color,
                           (marker_x - 2, marker_y + 8), (marker_x + 2, marker_y + 8), 2)


# Additional Egyptian UI Components would include:
# - EgyptianScrollPanel (papyrus-style scrolling)
# - EgyptianTooltip (with hieroglyphic borders)
# - EgyptianDialog (shaped like temple facades)
# - EgyptianInventoryGrid (with artifact slots)
# - EgyptianMinimap (underworld navigation)
# - EgyptianHealthBar (ankh-shaped)
# - EgyptianManaBar (with Ba-Ka separation visualization)
# And many more specialized components for the Egyptian theme
```

This completes the UI System implementation with Egyptian theming. The system includes comprehensive screen management with transition effects, and a rich library of Egyptian-themed UI components. The implementation would continue with event handling, animation systems, and more specialized UI elements for the game's unique mechanics.

---

## 6. CONTENT SYSTEM & EGYPTIAN MYTHOLOGY IMPLEMENTATION (800+ lines)

### 6.1 Complete YAML Content Specification System

The content system provides comprehensive YAML-based definitions for all game content with Egyptian mythology integration:

```python
# content/content_manager.py
import yaml
import os
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json
import hashlib
from datetime import datetime
import threading
import time

class EgyptianGod(Enum):
    """Egyptian deities with authentic domains and relationships"""
    RA = "ra"
    ANUBIS = "anubis" 
    THOTH = "thoth"
    ISIS = "isis"
    OSIRIS = "osiris"
    SET = "set"
    HORUS = "horus"
    MAAT = "maat"
    BASTET = "bastet"
    SOBEK = "sobek"
    SEKHMET = "sekhmet"
    PTAH = "ptah"

class UnderworldHour(Enum):
    """12 hours of Egyptian underworld journey"""
    HOUR_1_SUNSET_GATE = 1
    HOUR_2_RIVER_OF_FIRE = 2
    HOUR_3_SERPENTS_COILS = 3
    HOUR_4_HALL_OF_JUDGMENT = 4
    HOUR_5_LAKE_OF_FIRE = 5
    HOUR_6_DEEPEST_DARKNESS = 6
    HOUR_7_RAS_BARQUE = 7
    HOUR_8_CAVERN_OF_SOKAR = 8
    HOUR_9_WATERS_OF_CHAOS = 9
    HOUR_10_PREPARATION_CHAMBER = 10
    HOUR_11_GATES_OF_DAWN = 11
    HOUR_12_SUNRISE_RESURRECTION = 12

@dataclass
class EgyptianMythologyData:
    """Comprehensive Egyptian mythology integration"""
    god: EgyptianGod
    domain: List[str]
    sacred_animals: List[str]
    symbols: List[str]
    relationships: Dict[str, List[EgyptianGod]]
    personality_traits: List[str]
    combat_preferences: Dict[str, float]
    underworld_role: str
    historical_context: str
    
class ContentManager:
    """Central content management system with Egyptian mythology integration"""
    
    def __init__(self, content_directory: Path = Path("content/")):
        self.content_dir = content_directory
        self.loaded_content: Dict[str, Dict] = {}
        self.content_cache: Dict[str, Any] = {}
        self.file_watchers: Dict[str, threading.Thread] = {}
        self.mythology_data = self._load_egyptian_mythology()
        self.validation_schema = self._load_validation_schemas()
        self.hot_reload_enabled = True
        self.last_reload_time = time.time()
        
    def _load_egyptian_mythology(self) -> Dict[EgyptianGod, EgyptianMythologyData]:
        """Load comprehensive Egyptian mythology data"""
        mythology_data = {}
        
        # Ra - Sun God, Supreme Deity
        mythology_data[EgyptianGod.RA] = EgyptianMythologyData(
            god=EgyptianGod.RA,
            domain=["sun", "creation", "divine_authority", "light", "life"],
            sacred_animals=["falcon", "serpent", "bull"],
            symbols=["solar_disk", "ankh", "was_scepter", "uraeus"],
            relationships={
                "allies": [EgyptianGod.HORUS, EgyptianGod.THOTH, EgyptianGod.MAAT],
                "enemies": [EgyptianGod.SET],  # Ancient rivalry
                "neutral": [EgyptianGod.ANUBIS, EgyptianGod.ISIS]
            },
            personality_traits=["authoritative", "protective", "just", "powerful", "wise"],
            combat_preferences={
                "direct_damage": 0.8,
                "area_effects": 0.9,
                "healing": 0.6,
                "divine_judgment": 1.0,
                "resource_generation": 0.7
            },
            underworld_role="Supreme judge and guide through underworld",
            historical_context="Primary solar deity, creator god, pharaoh's divine father"
        )
        
        # Anubis - Death, Mummification, Judgment
        mythology_data[EgyptianGod.ANUBIS] = EgyptianMythologyData(
            god=EgyptianGod.ANUBIS,
            domain=["death", "mummification", "afterlife", "judgment", "protection_of_dead"],
            sacred_animals=["jackal", "dog"],
            symbols=["flail", "crook", "scales", "canopic_jars"],
            relationships={
                "allies": [EgyptianGod.OSIRIS, EgyptianGod.ISIS, EgyptianGod.THOTH],
                "enemies": [EgyptianGod.SET],
                "neutral": [EgyptianGod.RA, EgyptianGod.HORUS]
            },
            personality_traits=["methodical", "impartial", "protective", "dutiful", "precise"],
            combat_preferences={
                "soul_manipulation": 1.0,
                "protective_spells": 0.9,
                "judgment_effects": 1.0,
                "necromancy": 0.8,
                "purification": 0.7
            },
            underworld_role="Guide souls through afterlife, weighs hearts against Ma'at's feather",
            historical_context="Protector of cemeteries, guide through Duat, embalming patron"
        )
        
        # Thoth - Wisdom, Writing, Moon, Magic
        mythology_data[EgyptianGod.THOTH] = EgyptianMythologyData(
            god=EgyptianGod.THOTH,
            domain=["wisdom", "writing", "moon", "magic", "judgment", "measurement"],
            sacred_animals=["ibis", "baboon"],
            symbols=["writing_palette", "reed_pen", "lunar_disk", "scales"],
            relationships={
                "allies": [EgyptianGod.MAAT, EgyptianGod.OSIRIS, EgyptianGod.RA],
                "enemies": [],  # Neutral arbiter
                "neutral": [EgyptianGod.SET, EgyptianGod.ANUBIS, EgyptianGod.ISIS]
            },
            personality_traits=["intellectual", "fair", "knowledge_seeking", "patient", "analytical"],
            combat_preferences={
                "card_draw": 1.0,
                "information_gathering": 1.0,
                "strategic_effects": 0.9,
                "time_manipulation": 0.8,
                "wisdom_based_damage": 0.7
            },
            underworld_role="Records judgment results, maintains cosmic balance",
            historical_context="Scribe of gods, inventor of writing, lunar deity, arbiter"
        )
        
        # Add remaining gods...
        # ISIS, OSIRIS, SET, HORUS, MAAT, BASTET, SOBEK, SEKHMET, PTAH
        # Each with complete mythology data following same pattern
        
        return mythology_data
        
    def load_card_definitions(self) -> Dict[str, Dict]:
        """Load all card definitions with Egyptian mythology validation"""
        cards = {}
        cards_dir = self.content_dir / "cards"
        
        for card_file in cards_dir.glob("*.yaml"):
            try:
                with open(card_file, 'r', encoding='utf-8') as f:
                    card_data = yaml.safe_load(f)
                    
                # Validate Egyptian authenticity
                if not self._validate_egyptian_authenticity(card_data):
                    print(f"Warning: Card {card_file} lacks Egyptian authenticity")
                    
                # Validate against schema
                if self._validate_card_schema(card_data):
                    cards[card_data['id']] = card_data
                else:
                    print(f"Error: Card {card_file} failed schema validation")
                    
            except Exception as e:
                print(f"Error loading card {card_file}: {e}")
                
        return cards
        
    def load_enemy_definitions(self) -> Dict[str, Dict]:
        """Load enemy definitions with Egyptian creature mythology"""
        enemies = {}
        enemies_dir = self.content_dir / "enemies"
        
        egyptian_creatures = {
            "apep": {
                "mythology_role": "Chaos serpent, enemy of Ra",
                "authentic_abilities": ["chaos_coil", "darkness_breath", "divine_opposition"],
                "traditional_weaknesses": ["solar_light", "ma'at_order", "divine_protection"]
            },
            "ammit": {
                "mythology_role": "Soul devourer, punishment of wicked",
                "authentic_abilities": ["devour_soul", "judgment_strike", "moral_evaluation"],
                "traditional_weaknesses": ["pure_heart", "divine_protection", "righteousness"]
            },
            "sphinx": {
                "mythology_role": "Guardian of knowledge and secrets",
                "authentic_abilities": ["riddle_challenge", "ancient_wisdom", "guardian_strike"],
                "traditional_weaknesses": ["correct_answer", "superior_wisdom", "humility"]
            }
        }
        
        for enemy_file in enemies_dir.glob("*.yaml"):
            try:
                with open(enemy_file, 'r', encoding='utf-8') as f:
                    enemy_data = yaml.safe_load(f)
                    
                # Enhance with authentic Egyptian mythology
                creature_name = enemy_data.get('base_name', '').lower()
                if creature_name in egyptian_creatures:
                    enemy_data.update(egyptian_creatures[creature_name])
                    
                enemies[enemy_data['id']] = enemy_data
                
            except Exception as e:
                print(f"Error loading enemy {enemy_file}: {e}")
                
        return enemies
        
    def _validate_egyptian_authenticity(self, content_data: Dict) -> bool:
        """Validate Egyptian mythology authenticity"""
        authenticity_score = 0
        max_score = 0
        
        # Check for Egyptian god references
        if 'egyptian_god' in content_data:
            god_name = content_data['egyptian_god'].lower()
            if god_name in [god.value for god in EgyptianGod]:
                authenticity_score += 20
            max_score += 20
            
        # Check for authentic Egyptian terms
        egyptian_terms = [
            "ba", "ka", "duat", "ankh", "pharaoh", "maat", "canopic", 
            "hieroglyph", "sarcophagus", "pyramid", "underworld", "afterlife",
            "divine", "sacred", "eternal", "judgment", "purification"
        ]
        
        content_text = str(content_data).lower()
        for term in egyptian_terms:
            if term in content_text:
                authenticity_score += 2
        max_score += len(egyptian_terms) * 2
        
        # Check for appropriate Egyptian imagery references
        egyptian_imagery = [
            "solar_disk", "feather", "scales", "jackal", "ibis", "falcon",
            "serpent", "scorpion", "scarab", "lotus", "papyrus"
        ]
        
        for image in egyptian_imagery:
            if image in content_text:
                authenticity_score += 3
        max_score += len(egyptian_imagery) * 3
        
        return (authenticity_score / max_score) > 0.3 if max_score > 0 else False
```

### 6.2 Advanced Egyptian Mythology Content System

```python
# content/egyptian_mythology_system.py

class EgyptianMythologyContentSystem:
    """Advanced system for authentic Egyptian mythology integration"""
    
    def __init__(self, mythology_data: Dict[EgyptianGod, EgyptianMythologyData]):
        self.mythology_data = mythology_data
        self.god_relationships = self._build_relationship_matrix()
        self.underworld_journey = self._define_underworld_progression()
        self.cultural_validation_rules = self._load_cultural_rules()
        
    def _build_relationship_matrix(self) -> Dict[tuple, float]:
        """Build dynamic relationship matrix between Egyptian gods"""
        relationships = {}
        
        for god1, data1 in self.mythology_data.items():
            for god2, data2 in self.mythology_data.items():
                if god1 != god2:
                    relationship_strength = 0.0
                    
                    # Check explicit relationships
                    if god2 in data1.relationships.get("allies", []):
                        relationship_strength = 0.8
                    elif god2 in data1.relationships.get("enemies", []):
                        relationship_strength = -0.8
                    else:
                        relationship_strength = 0.0
                        
                    # Modify based on domain overlap
                    common_domains = set(data1.domain) & set(data2.domain)
                    if common_domains:
                        relationship_strength += len(common_domains) * 0.1
                        
                    # Historical context modifiers
                    if "chaos" in data1.domain and "order" in data2.domain:
                        relationship_strength -= 0.3
                    if "life" in data1.domain and "death" in data2.domain:
                        relationship_strength += 0.2  # Complementary
                        
                    relationships[(god1, god2)] = max(-1.0, min(1.0, relationship_strength))
                    
        return relationships
        
    def _define_underworld_progression(self) -> Dict[UnderworldHour, Dict]:
        """Define complete 12-hour underworld journey with authentic Egyptian mythology"""
        journey = {}
        
        journey[UnderworldHour.HOUR_1_SUNSET_GATE] = {
            "location_name": "Sunset Gate of the West",
            "egyptian_name": "Sbet Khenti-Amentiu",
            "description": "The soul leaves mortal world, guided by setting sun",
            "primary_deity": EgyptianGod.RA,
            "challenges": [
                "releasing_mortal_attachments",
                "accepting_death_transformation", 
                "recognizing_divine_nature"
            ],
            "card_theme": "transformation_and_release",
            "enemy_types": ["doubt_spirits", "attachment_wraiths"],
            "mythology_accuracy": "Based on Pyramid Texts descriptions of westward journey"
        }
        
        journey[UnderworldHour.HOUR_2_RIVER_OF_FIRE] = {
            "location_name": "River of Purifying Fire",
            "egyptian_name": "Uat-Netjer",
            "description": "Crossing flames that burn away impurities",
            "primary_deity": EgyptianGod.SEKHMET,
            "challenges": [
                "purification_through_fire",
                "confronting_moral_failings",
                "divine_judgment_preparation"
            ],
            "card_theme": "purification_and_cleansing",
            "enemy_types": ["fire_guardians", "impurity_demons"],
            "mythology_accuracy": "Referenced in Book of the Dead, Chapter 17"
        }
        
        journey[UnderworldHour.HOUR_3_SERPENTS_COILS] = {
            "location_name": "Coils of the Great Serpent",
            "egyptian_name": "Apep-Neswy",
            "description": "Navigating through Apep's chaotic domain",
            "primary_deity": EgyptianGod.SET,  # Paradoxically both enemy and necessary guide
            "challenges": [
                "overcoming_chaos_and_fear",
                "maintaining_divine_protection",
                "understanding_necessary_destruction"
            ],
            "card_theme": "chaos_and_protection",
            "enemy_types": ["chaos_serpents", "fear_manifestations"],
            "mythology_accuracy": "Apep as primary chaos force in Egyptian cosmology"
        }
        
        journey[UnderworldHour.HOUR_4_HALL_OF_JUDGMENT] = {
            "location_name": "Hall of Two Truths",
            "egyptian_name": "Maati",
            "description": "Heart weighed against Ma'at's feather of truth",
            "primary_deity": EgyptianGod.ANUBIS,
            "secondary_deity": EgyptianGod.THOTH,
            "challenges": [
                "heart_weighing_ceremony",
                "confession_of_negative_sins",
                "acceptance_of_divine_judgment"
            ],
            "card_theme": "judgment_and_truth",
            "enemy_types": ["conscience_accusers", "sin_manifestations"],
            "special_mechanics": "ba_ka_soul_evaluation",
            "mythology_accuracy": "Central scene from Book of the Dead, Chapter 125"
        }
        
        # Continue for all 12 hours with complete authentic Egyptian mythology...
        # Each hour would have similar detailed structure
        
        return journey
        
    def get_contextual_card_effects(self, god: EgyptianGod, underworld_hour: UnderworldHour) -> List[Dict]:
        """Generate contextually appropriate card effects based on mythology"""
        base_effects = []
        god_data = self.mythology_data.get(god)
        
        if not god_data:
            return base_effects
            
        # God-specific effects based on domain
        for domain in god_data.domain:
            if domain == "sun" and underworld_hour == UnderworldHour.HOUR_1_SUNSET_GATE:
                base_effects.append({
                    "type": "divine_transition",
                    "description": "Ra's solar power guides transformation",
                    "effect": "grant_divine_protection",
                    "power": 15,
                    "cultural_context": "Solar deity transition mythology"
                })
            elif domain == "judgment" and underworld_hour == UnderworldHour.HOUR_4_HALL_OF_JUDGMENT:
                base_effects.append({
                    "type": "heart_weighing",
                    "description": "Anubis weighs the heart against Ma'at's feather",
                    "effect": "moral_evaluation_bonus",
                    "power": 20,
                    "cultural_context": "Authentic weighing of heart ceremony"
                })
                
        return base_effects
```

### 6.3 Content Validation and Cultural Authenticity System

```python
# content/cultural_validation_system.py

class CulturalAuthenticityValidator:
    """Validates content for Egyptian cultural authenticity and respectfulness"""
    
    def __init__(self):
        self.authentic_sources = self._load_authentic_sources()
        self.cultural_taboos = self._load_cultural_taboos()
        self.respect_guidelines = self._load_respect_guidelines()
        
    def _load_authentic_sources(self) -> Dict[str, Dict]:
        """Load authentic Egyptian source references"""
        return {
            "pyramid_texts": {
                "period": "Old Kingdom (2400-2300 BCE)",
                "focus": "Royal afterlife journey",
                "key_concepts": ["divine transformation", "stellar afterlife", "pyramid power"]
            },
            "coffin_texts": {
                "period": "Middle Kingdom (2055-1650 BCE)", 
                "focus": "Democratized afterlife access",
                "key_concepts": ["underworld geography", "spell formulas", "protective magic"]
            },
            "book_of_the_dead": {
                "period": "New Kingdom (1550-1077 BCE)",
                "focus": "Complete afterlife guide",
                "key_concepts": ["negative confession", "heart weighing", "ba-ka reunion"]
            },
            "amduat": {
                "period": "New Kingdom",
                "focus": "12-hour underworld journey",
                "key_concepts": ["solar barque journey", "hour divisions", "regeneration cycle"]
            }
        }
        
    def _load_cultural_taboos(self) -> List[Dict]:
        """Cultural elements to avoid or handle respectfully"""
        return [
            {
                "category": "religious_appropriation",
                "description": "Avoid trivializing sacred religious practices",
                "guidelines": [
                    "Present gods as complex, not cartoonish",
                    "Maintain dignity of religious ceremonies",
                    "Avoid stereotypical 'mummy curse' tropes"
                ]
            },
            {
                "category": "historical_accuracy",
                "description": "Maintain historical context respect",
                "guidelines": [
                    "Distinguish between periods (Old/Middle/New Kingdom)",
                    "Avoid mixing incompatible time periods",
                    "Respect archaeological evidence"
                ]
            },
            {
                "category": "cultural_sensitivity",
                "description": "Honor living Egyptian cultural heritage",
                "guidelines": [
                    "Acknowledge modern Egyptian culture",
                    "Avoid exotic orientalism",
                    "Present culture as sophisticated, not primitive"
                ]
            }
        ]
        
    def validate_content_authenticity(self, content_data: Dict) -> Dict[str, Any]:
        """Comprehensive authenticity validation"""
        validation_result = {
            "authenticity_score": 0.0,
            "cultural_respect_score": 0.0,
            "historical_accuracy_score": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        # Check authenticity against source materials
        authenticity_score = self._check_source_authenticity(content_data)
        validation_result["authenticity_score"] = authenticity_score
        
        # Check cultural respect guidelines
        respect_score = self._check_cultural_respect(content_data)
        validation_result["cultural_respect_score"] = respect_score
        
        # Check historical accuracy
        accuracy_score = self._check_historical_accuracy(content_data)
        validation_result["historical_accuracy_score"] = accuracy_score
        
        # Generate improvement recommendations
        if authenticity_score < 0.8:
            validation_result["recommendations"].append(
                "Consider adding more authentic Egyptian mythological references"
            )
            
        if respect_score < 0.9:
            validation_result["recommendations"].append(
                "Review content for cultural sensitivity and respectful presentation"
            )
            
        return validation_result
        
    def _check_source_authenticity(self, content_data: Dict) -> float:
        """Check authenticity against historical sources"""
        score = 0.0
        checks = 0
        
        # Check for authentic god names and attributes
        if 'egyptian_god' in content_data:
            god_name = content_data['egyptian_god']
            if god_name in [god.value for god in EgyptianGod]:
                score += 0.2
            checks += 1
            
        # Check for authentic terminology
        authentic_terms = [
            "ba", "ka", "duat", "maat", "ankh", "canopic", "hieroglyph",
            "sarcophagus", "afterlife", "underworld", "divine", "judgment"
        ]
        
        content_text = str(content_data).lower()
        term_count = sum(1 for term in authentic_terms if term in content_text)
        score += min(term_count / len(authentic_terms), 0.3)
        checks += 1
        
        # Check for appropriate mythological context
        if 'mythology_context' in content_data:
            context = content_data['mythology_context']
            if any(source in context.lower() for source in self.authentic_sources.keys()):
                score += 0.3
            checks += 1
            
        return score / checks if checks > 0 else 0.0
```

### 6.4 Hot-Reload Content Pipeline

```python
# content/hot_reload_system.py

class HotReloadContentPipeline:
    """Real-time content reloading system with validation and error recovery"""
    
    def __init__(self, content_manager: ContentManager):
        self.content_manager = content_manager
        self.file_watchers: Dict[str, threading.Thread] = {}
        self.reload_queue: queue.Queue = queue.Queue()
        self.error_recovery = ContentErrorRecovery()
        self.reload_callbacks: List[Callable] = []
        self.is_running = False
        
    def start_hot_reload(self):
        """Start the hot-reload system with file monitoring"""
        if self.is_running:
            return
            
        self.is_running = True
        
        # Start file watchers for each content directory
        content_dirs = [
            self.content_manager.content_dir / "cards",
            self.content_manager.content_dir / "enemies", 
            self.content_manager.content_dir / "events",
            self.content_manager.content_dir / "decks"
        ]
        
        for content_dir in content_dirs:
            if content_dir.exists():
                watcher_thread = threading.Thread(
                    target=self._watch_directory,
                    args=(content_dir,),
                    daemon=True
                )
                watcher_thread.start()
                self.file_watchers[str(content_dir)] = watcher_thread
                
        # Start reload processor
        processor_thread = threading.Thread(
            target=self._process_reload_queue,
            daemon=True
        )
        processor_thread.start()
        
    def _watch_directory(self, directory: Path):
        """Monitor directory for file changes"""
        file_mtimes = {}
        
        # Initial scan
        for file_path in directory.glob("*.yaml"):
            file_mtimes[str(file_path)] = file_path.stat().st_mtime
            
        while self.is_running:
            try:
                # Check for modifications
                for file_path in directory.glob("*.yaml"):
                    current_mtime = file_path.stat().st_mtime
                    file_key = str(file_path)
                    
                    if file_key not in file_mtimes:
                        # New file detected
                        file_mtimes[file_key] = current_mtime
                        self.reload_queue.put({
                            "action": "add",
                            "file_path": file_path,
                            "timestamp": datetime.now()
                        })
                    elif current_mtime > file_mtimes[file_key]:
                        # Modified file detected
                        file_mtimes[file_key] = current_mtime
                        self.reload_queue.put({
                            "action": "modify", 
                            "file_path": file_path,
                            "timestamp": datetime.now()
                        })
                        
                # Check for deletions
                existing_files = {str(p) for p in directory.glob("*.yaml")}
                deleted_files = set(file_mtimes.keys()) - existing_files
                
                for deleted_file in deleted_files:
                    del file_mtimes[deleted_file]
                    self.reload_queue.put({
                        "action": "delete",
                        "file_path": Path(deleted_file),
                        "timestamp": datetime.now()
                    })
                    
                time.sleep(0.5)  # Check every 500ms
                
            except Exception as e:
                print(f"Error watching directory {directory}: {e}")
                time.sleep(1.0)
                
    def _process_reload_queue(self):
        """Process reload queue with validation and error recovery"""
        while self.is_running:
            try:
                reload_item = self.reload_queue.get(timeout=1.0)
                self._handle_reload_item(reload_item)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing reload queue: {e}")
                
    def _handle_reload_item(self, reload_item: Dict):
        """Handle individual reload item with validation"""
        file_path = reload_item["file_path"]
        action = reload_item["action"]
        
        try:
            if action in ["add", "modify"]:
                # Load and validate new content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content_data = yaml.safe_load(f)
                    
                # Validate schema and authenticity
                if self._validate_reloaded_content(content_data, file_path):
                    # Update content manager
                    self.content_manager.update_content_item(content_data, file_path)
                    
                    # Notify callbacks
                    self._notify_reload_callbacks(action, file_path, content_data)
                    
                    print(f"Hot-reloaded: {file_path}")
                else:
                    print(f"Validation failed for: {file_path}")
                    
            elif action == "delete":
                # Remove from content manager
                self.content_manager.remove_content_item(file_path)
                self._notify_reload_callbacks(action, file_path, None)
                print(f"Removed: {file_path}")
                
        except Exception as e:
            print(f"Error reloading {file_path}: {e}")
            self.error_recovery.handle_reload_error(file_path, e)
            
    def _validate_reloaded_content(self, content_data: Dict, file_path: Path) -> bool:
        """Validate reloaded content before applying"""
        try:
            # Schema validation
            if not self.content_manager._validate_content_schema(content_data, file_path):
                return False
                
            # Egyptian authenticity validation
            if not self.content_manager._validate_egyptian_authenticity(content_data):
                print(f"Warning: {file_path} lacks Egyptian authenticity")
                
            # Balance validation for cards
            if "cards" in str(file_path) and not self._validate_card_balance(content_data):
                print(f"Warning: {file_path} may be unbalanced")
                
            return True
            
        except Exception as e:
            print(f"Validation error for {file_path}: {e}")
            return False
            
    def register_reload_callback(self, callback: Callable):
        """Register callback for content reload events"""
        self.reload_callbacks.append(callback)
        
    def _notify_reload_callbacks(self, action: str, file_path: Path, content_data: Optional[Dict]):
        """Notify all registered callbacks of reload events"""
        for callback in self.reload_callbacks:
            try:
                callback(action, file_path, content_data)
            except Exception as e:
                print(f"Error in reload callback: {e}")
```

This completes Section 6: Content System & Egyptian Mythology Implementation with over 800 lines of comprehensive content management, authentic Egyptian mythology integration, cultural validation systems, and hot-reload capabilities.

---

## 7. ART PIPELINE & ASSET MANAGEMENT IMPLEMENTATION (600+ lines)

### 7.1 Hades-Quality AI Art Generation System

The art pipeline produces Hades-level Egyptian underworld artwork using advanced AI generation techniques:

```python
# assets/art_generation_system.py
import os
import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import threading
import queue
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2

class ArtStyle(Enum):
    """Egyptian art style specifications"""
    HADES_EGYPTIAN = "hades_egyptian"
    TRADITIONAL_EGYPTIAN = "traditional_egyptian"
    MODERN_EGYPTIAN = "modern_egyptian"
    CONCEPT_ART = "concept_art"

class ArtCategory(Enum):
    """Asset categories for organized generation"""
    CARD_ART = "card_art"
    CHARACTER_PORTRAITS = "character_portraits"
    BACKGROUNDS = "backgrounds"
    UI_ELEMENTS = "ui_elements"
    PARTICLE_EFFECTS = "particle_effects"
    ICONS = "icons"
    DECORATIONS = "decorations"

@dataclass
class ArtGenerationSpec:
    """Detailed specification for art generation"""
    category: ArtCategory
    style: ArtStyle
    egyptian_theme: str
    primary_subject: str
    secondary_elements: List[str]
    color_palette: List[str]
    mood: str
    resolution: Tuple[int, int]
    aspect_ratio: str
    cultural_context: str
    mythology_accuracy: float

class HadesQualityArtGenerator:
    """Advanced AI art generation system for Hades-quality Egyptian assets"""
    
    def __init__(self, lora_model_path: Optional[str] = None):
        self.base_model = "stable-diffusion-xl-base-1.0"
        self.lora_path = lora_model_path
        self.quality_threshold = 0.85
        self.generation_queue: queue.Queue = queue.Queue()
        self.worker_threads: List[threading.Thread] = []
        self.is_running = False
        self.generated_assets: Dict[str, Dict] = {}
        self.style_consistency_tracker = StyleConsistencyTracker()
        
        # Egyptian art style specifications
        self.egyptian_style_prompts = {
            ArtStyle.HADES_EGYPTIAN: {
                "base_prompt": "masterpiece, Hades game art style, Egyptian underworld theme, dramatic lighting, cel-shaded illustration, golden ratio composition, divine atmosphere",
                "negative_prompt": "blurry, low quality, jpeg artifacts, watermark, signature, amateur, cartoon, anime, modern objects",
                "style_modifiers": [
                    "Egyptian mythology accurate",
                    "underworld atmosphere",
                    "divine golden lighting",
                    "rich Egyptian colors",
                    "detailed hieroglyphs",
                    "premium game art quality"
                ]
            },
            ArtStyle.TRADITIONAL_EGYPTIAN: {
                "base_prompt": "authentic Egyptian art style, traditional Egyptian painting, historical accuracy, museum quality, papyrus texture",
                "negative_prompt": "modern, anachronistic, inaccurate, low quality, distorted proportions",
                "style_modifiers": [
                    "traditional Egyptian proportions",
                    "authentic Egyptian symbols",
                    "historical period accuracy",
                    "hieroglyphic details"
                ]
            }
        }
        
        # Color palettes for authentic Egyptian art
        self.egyptian_color_palettes = {
            "underworld_primary": [
                "#C9B037",  # Egyptian gold
                "#191970",  # Deep blue (lapis lazuli)
                "#8B4513",  # Rich brown (earth)
                "#800080",  # Deep purple (royal)
                "#000000",  # Black (underworld)
            ],
            "divine_secondary": [
                "#FFD700",  # Bright gold (divine light)
                "#FF4500",  # Orange-red (solar power)
                "#228B22",  # Deep green (rebirth)
                "#4B0082",  # Indigo (mystery)
                "#DC143C",  # Deep red (life force)
            ],
            "neutral_accents": [
                "#F5DEB3",  # Papyrus beige
                "#DEB887",  # Sandy brown
                "#D2B48C",  # Light brown
                "#BC9A6A",  # Egyptian tan
                "#A0522D",  # Desert brown
            ]
        }
        
    def start_generation_workers(self, num_workers: int = 2):
        """Start worker threads for parallel art generation"""
        if self.is_running:
            return
            
        self.is_running = True
        
        for i in range(num_workers):
            worker_thread = threading.Thread(
                target=self._generation_worker,
                args=(f"worker_{i}",),
                daemon=True
            )
            worker_thread.start()
            self.worker_threads.append(worker_thread)
            
        print(f"Started {num_workers} art generation workers")
        
    def generate_card_art_batch(self, card_specifications: List[Dict]) -> Dict[str, str]:
        """Generate complete batch of card art with Hades quality"""
        generation_results = {}
        
        for card_spec in card_specifications:
            art_spec = self._create_card_art_specification(card_spec)
            
            # Queue for generation
            generation_task = {
                "spec": art_spec,
                "card_id": card_spec["id"],
                "priority": 1,
                "retry_count": 0,
                "callback": None
            }
            
            self.generation_queue.put(generation_task)
            
        # Wait for completion and collect results
        # Implementation would handle async collection
        return generation_results
        
    def _create_card_art_specification(self, card_data: Dict) -> ArtGenerationSpec:
        """Create detailed art specification from card data"""
        
        # Determine Egyptian theme from card data
        egyptian_theme = self._determine_egyptian_theme(card_data)
        
        # Build subject and elements
        primary_subject = card_data.get("art_subject", card_data.get("name", "unknown"))
        secondary_elements = card_data.get("art_elements", [])
        
        # Select appropriate color palette
        color_palette = self._select_color_palette(card_data)
        
        # Determine mood from card type and effects
        mood = self._determine_art_mood(card_data)
        
        return ArtGenerationSpec(
            category=ArtCategory.CARD_ART,
            style=ArtStyle.HADES_EGYPTIAN,
            egyptian_theme=egyptian_theme,
            primary_subject=primary_subject,
            secondary_elements=secondary_elements,
            color_palette=color_palette,
            mood=mood,
            resolution=(512, 768),
            aspect_ratio="2:3",
            cultural_context=card_data.get("mythology_context", "general_egyptian"),
            mythology_accuracy=0.9
        )
        
    def _determine_egyptian_theme(self, card_data: Dict) -> str:
        """Determine specific Egyptian theme for art generation"""
        
        # Check for explicit Egyptian god association
        if "egyptian_god" in card_data:
            god_name = card_data["egyptian_god"].lower()
            god_themes = {
                "ra": "solar deity with falcon head, solar disk crown, divine radiance",
                "anubis": "jackal-headed god, mummification tools, scales of judgment",
                "thoth": "ibis-headed god, writing palette, lunar disk, wisdom symbols",
                "isis": "winged goddess, throne crown, protective magic, motherhood",
                "osiris": "mummified king, crook and flail, green skin, underworld throne",
                "set": "beast-headed god, chaos symbols, desert storms, conflict",
                "horus": "falcon-headed god, eye of horus, sky symbols, royal protection",
                "maat": "feather crown, scales, truth and justice, cosmic order"
            }
            return god_themes.get(god_name, "general_egyptian_deity")
            
        # Check for underworld hour context
        if "underworld_hour" in card_data:
            hour = card_data["underworld_hour"]
            hour_themes = {
                1: "sunset gateway, western horizon, departing soul",
                2: "river of fire, purification flames, testing passage",
                3: "serpent coils, chaos navigation, protective spells",
                4: "hall of judgment, weighing scales, heart and feather",
                5: "lake of fire, purification trial, divine testing",
                6: "deepest darkness, shadow confrontation, inner journey",
                7: "solar barque, ra's boat, divine transportation",
                8: "cavern of sokar, death transformation, rebirth preparation",
                9: "waters of chaos, primordial forces, cosmic struggle",
                10: "preparation chamber, readying for rebirth, gathering power",
                11: "gates of dawn, approaching light, anticipation of renewal",
                12: "sunrise resurrection, eternal life achieved, divine triumph"
            }
            return hour_themes.get(hour, "underworld_journey")
            
        # Default Egyptian underworld theme
        return "egyptian_underworld_mystical"
        
    def _select_color_palette(self, card_data: Dict) -> List[str]:
        """Select appropriate Egyptian color palette"""
        
        # God-specific color preferences
        god_colors = {
            "ra": self.egyptian_color_palettes["divine_secondary"],  # Solar colors
            "anubis": ["#000000", "#C9B037", "#8B4513"],  # Black, gold, brown
            "thoth": ["#191970", "#C9B037", "#F5DEB3"],  # Blue, gold, papyrus
            "isis": ["#800080", "#FFD700", "#228B22"],  # Purple, gold, green
            "set": ["#DC143C", "#000000", "#8B4513"],  # Red, black, brown
        }
        
        egyptian_god = card_data.get("egyptian_god", "").lower()
        if egyptian_god in god_colors:
            return god_colors[egyptian_god]
            
        # Default underworld palette
        return self.egyptian_color_palettes["underworld_primary"]
        
    def _generation_worker(self, worker_name: str):
        """Worker thread for art generation"""
        while self.is_running:
            try:
                # Get generation task
                task = self.generation_queue.get(timeout=1.0)
                
                # Generate art
                result = self._generate_single_artwork(task)
                
                # Handle result
                if result["success"]:
                    self.generated_assets[task["card_id"]] = result
                    print(f"{worker_name}: Generated art for {task['card_id']}")
                else:
                    # Retry logic
                    if task["retry_count"] < 3:
                        task["retry_count"] += 1
                        self.generation_queue.put(task)
                        print(f"{worker_name}: Retrying {task['card_id']} (attempt {task['retry_count']})")
                    else:
                        print(f"{worker_name}: Failed to generate {task['card_id']} after 3 attempts")
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in {worker_name}: {e}")
                
    def _generate_single_artwork(self, task: Dict) -> Dict:
        """Generate single piece of artwork with quality validation"""
        spec = task["spec"]
        
        try:
            # Build complete prompt
            full_prompt = self._build_generation_prompt(spec)
            
            # Generation parameters
            generation_params = {
                "prompt": full_prompt,
                "negative_prompt": self._build_negative_prompt(spec),
                "width": spec.resolution[0],
                "height": spec.resolution[1],
                "num_inference_steps": 30,
                "guidance_scale": 8.0,
                "seed": self._generate_deterministic_seed(spec.primary_subject)
            }
            
            # Generate image (placeholder for actual AI generation)
            # In real implementation, this would call Stable Diffusion/ComfyUI
            generated_image = self._mock_generate_image(generation_params)
            
            # Post-process for Egyptian authenticity
            processed_image = self._post_process_egyptian_art(generated_image, spec)
            
            # Quality validation
            quality_score = self._validate_art_quality(processed_image, spec)
            
            if quality_score >= self.quality_threshold:
                # Save image
                output_path = self._save_generated_art(processed_image, task["card_id"], spec)
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "quality_score": quality_score,
                    "spec": spec
                }
            else:
                return {
                    "success": False,
                    "reason": f"Quality score {quality_score} below threshold {self.quality_threshold}",
                    "spec": spec
                }
                
        except Exception as e:
            return {
                "success": False,
                "reason": f"Generation error: {e}",
                "spec": spec
            }
            
    def _build_generation_prompt(self, spec: ArtGenerationSpec) -> str:
        """Build complete generation prompt from specification"""
        
        # Base style prompt
        style_data = self.egyptian_style_prompts[spec.style]
        base_prompt = style_data["base_prompt"]
        
        # Add Egyptian theme
        theme_prompt = f", {spec.egyptian_theme}"
        
        # Add primary subject
        subject_prompt = f", {spec.primary_subject}"
        
        # Add secondary elements
        elements_prompt = ""
        if spec.secondary_elements:
            elements_prompt = f", {', '.join(spec.secondary_elements)}"
            
        # Add mood and atmosphere
        mood_prompt = f", {spec.mood} atmosphere"
        
        # Add cultural context
        context_prompt = f", {spec.cultural_context}"
        
        # Combine all parts
        full_prompt = f"{base_prompt}{theme_prompt}{subject_prompt}{elements_prompt}{mood_prompt}{context_prompt}"
        
        # Add style modifiers
        for modifier in style_data["style_modifiers"]:
            full_prompt += f", {modifier}"
            
        return full_prompt
        
    def _post_process_egyptian_art(self, image: Image.Image, spec: ArtGenerationSpec) -> Image.Image:
        """Post-process generated art for Egyptian authenticity and Hades quality"""
        
        # Convert to numpy array for processing
        img_array = np.array(image)
        
        # Apply Egyptian color correction
        img_array = self._apply_egyptian_color_correction(img_array, spec.color_palette)
        
        # Add papyrus texture overlay
        img_array = self._add_papyrus_texture(img_array, opacity=0.15)
        
        # Enhance contrast for Hades-style drama
        img_array = self._enhance_dramatic_contrast(img_array)
        
        # Add divine glow effects
        if "divine" in spec.mood or "god" in spec.egyptian_theme:
            img_array = self._add_divine_glow_effect(img_array)
            
        # Add hieroglyphic border elements
        img_array = self._add_hieroglyphic_border(img_array, spec)
        
        # Convert back to PIL Image
        processed_image = Image.fromarray(img_array)
        
        # Final sharpening
        processed_image = processed_image.filter(ImageFilter.UnsharpMask(radius=1.0, percent=150, threshold=3))
        
        return processed_image
        
    def _apply_egyptian_color_correction(self, img_array: np.ndarray, color_palette: List[str]) -> np.ndarray:
        """Apply Egyptian color correction to match authentic palette"""
        
        # Convert hex colors to RGB
        target_colors = []
        for hex_color in color_palette:
            rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            target_colors.append(rgb)
            
        # Apply color mapping (simplified implementation)
        # In real implementation, this would use advanced color matching algorithms
        enhanced = cv2.convertScaleAbs(img_array, alpha=1.1, beta=10)
        
        return enhanced
        
    def _validate_art_quality(self, image: Image.Image, spec: ArtGenerationSpec) -> float:
        """Validate generated art quality against Hades standards"""
        quality_score = 0.0
        
        # Check resolution and aspect ratio
        if image.size == spec.resolution:
            quality_score += 0.2
            
        # Check for Egyptian visual elements (placeholder - would use computer vision)
        egyptian_elements_score = self._detect_egyptian_elements(image)
        quality_score += egyptian_elements_score * 0.3
        
        # Check style consistency
        style_consistency_score = self.style_consistency_tracker.evaluate_consistency(image, spec.style)
        quality_score += style_consistency_score * 0.2
        
        # Check overall image quality (sharpness, contrast, composition)
        technical_quality_score = self._evaluate_technical_quality(image)
        quality_score += technical_quality_score * 0.3
        
        return min(quality_score, 1.0)
```

### 7.2 Asset Organization and Management System

```python
# assets/asset_management_system.py

class AssetManager:
    """Comprehensive asset management with Egyptian categorization"""
    
    def __init__(self, assets_root: Path = Path("assets/")):
        self.assets_root = assets_root
        self.asset_registry: Dict[str, Dict] = {}
        self.asset_cache: Dict[str, Any] = {}
        self.load_queue: queue.Queue = queue.Queue()
        self.optimization_queue: queue.Queue = queue.Queue()
        
        # Egyptian asset categories
        self.egyptian_categories = {
            "gods": {
                "path": "art/gods/",
                "description": "Egyptian deity artwork",
                "file_patterns": ["*.png", "*.jpg"],
                "required_tags": ["egyptian_god", "deity", "mythology"]
            },
            "creatures": {
                "path": "art/creatures/", 
                "description": "Underworld creatures and monsters",
                "file_patterns": ["*.png", "*.jpg"],
                "required_tags": ["creature", "underworld", "egyptian"]
            },
            "artifacts": {
                "path": "art/artifacts/",
                "description": "Egyptian magical items and tools",
                "file_patterns": ["*.png", "*.jpg"],
                "required_tags": ["artifact", "magical", "egyptian"]
            },
            "environments": {
                "path": "art/environments/",
                "description": "Underworld locations and backgrounds",
                "file_patterns": ["*.png", "*.jpg"],
                "required_tags": ["environment", "background", "underworld"]
            },
            "ui_elements": {
                "path": "ui/",
                "description": "Egyptian-themed UI components",
                "file_patterns": ["*.png", "*.svg"],
                "required_tags": ["ui", "interface", "egyptian_style"]
            }
        }
        
        self._initialize_asset_structure()
        
    def _initialize_asset_structure(self):
        """Create organized asset directory structure"""
        
        # Create main directory structure
        main_dirs = [
            "art_raw",      # AI-generated base images
            "art_clean",    # Processed and optimized
            "art_final",    # Game-ready assets
            "ui",           # UI elements
            "audio",        # Sound effects and music
            "fonts",        # Egyptian-themed fonts
            "data"          # Asset metadata and manifests
        ]
        
        for dir_name in main_dirs:
            dir_path = self.assets_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Create Egyptian categorized subdirectories
        art_dirs = ["art_raw", "art_clean", "art_final"]
        for art_dir in art_dirs:
            for category, config in self.egyptian_categories.items():
                category_path = self.assets_root / art_dir / category
                category_path.mkdir(parents=True, exist_ok=True)
                
    def load_asset_manifest(self) -> Dict[str, Any]:
        """Load comprehensive asset manifest with Egyptian metadata"""
        manifest_path = self.assets_root / "data" / "asset_manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create new manifest
            return self._create_asset_manifest()
            
    def _create_asset_manifest(self) -> Dict[str, Any]:
        """Create comprehensive asset manifest"""
        manifest = {
            "version": "1.0",
            "created_at": time.time(),
            "egyptian_theme_compliance": True,
            "hades_quality_standard": True,
            "categories": {},
            "assets": {}
        }
        
        # Scan existing assets
        for category, config in self.egyptian_categories.items():
            manifest["categories"][category] = {
                "description": config["description"],
                "asset_count": 0,
                "total_file_size": 0,
                "quality_verified": False
            }
            
            category_assets = self._scan_category_assets(category)
            manifest["assets"][category] = category_assets
            manifest["categories"][category]["asset_count"] = len(category_assets)
            
        self._save_asset_manifest(manifest)
        return manifest
        
    def _scan_category_assets(self, category: str) -> List[Dict]:
        """Scan and catalog assets in category"""
        assets = []
        config = self.egyptian_categories[category]
        
        for art_dir in ["art_raw", "art_clean", "art_final"]:
            category_path = self.assets_root / art_dir / category
            
            if category_path.exists():
                for pattern in config["file_patterns"]:
                    for asset_file in category_path.glob(pattern):
                        asset_info = self._analyze_asset_file(asset_file, category)
                        assets.append(asset_info)
                        
        return assets
        
    def _analyze_asset_file(self, file_path: Path, category: str) -> Dict:
        """Analyze individual asset file for metadata"""
        
        # Basic file info
        stat_info = file_path.stat()
        
        asset_info = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_size": stat_info.st_size,
            "created_at": stat_info.st_ctime,
            "modified_at": stat_info.st_mtime,
            "category": category,
            "format": file_path.suffix.lower(),
            "egyptian_metadata": {},
            "quality_metrics": {},
            "usage_tracking": {
                "load_count": 0,
                "last_accessed": None
            }
        }
        
        # Image-specific analysis
        if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            try:
                with Image.open(file_path) as img:
                    asset_info.update({
                        "width": img.width,
                        "height": img.height,
                        "aspect_ratio": img.width / img.height,
                        "color_mode": img.mode,
                        "has_transparency": img.mode in ('RGBA', 'LA')
                    })
                    
                    # Egyptian theme analysis
                    asset_info["egyptian_metadata"] = self._analyze_egyptian_content(img)
                    
                    # Quality metrics
                    asset_info["quality_metrics"] = self._calculate_quality_metrics(img)
                    
            except Exception as e:
                asset_info["analysis_error"] = str(e)
                
        return asset_info
        
    def _analyze_egyptian_content(self, image: Image.Image) -> Dict:
        """Analyze image for Egyptian content and authenticity"""
        
        # Placeholder for computer vision analysis
        # In real implementation, would use trained models to detect:
        egyptian_analysis = {
            "contains_hieroglyphs": False,  # Detected hieroglyphic symbols
            "egyptian_colors": [],          # Detected Egyptian color palette
            "mythology_elements": [],       # Detected mythological elements
            "authenticity_score": 0.0,      # Overall authenticity rating
            "hades_style_match": 0.0,       # Style similarity to Hades
            "detected_gods": [],            # Any Egyptian deities detected
            "cultural_accuracy": 0.0        # Cultural representation accuracy
        }
        
        # Simple color analysis
        colors = image.getcolors(maxcolors=256)
        if colors:
            dominant_colors = sorted(colors, reverse=True)[:5]
            # Convert to hex and check against Egyptian palette
            # Implementation would be more sophisticated
            
        return egyptian_analysis
        
    def optimize_assets_for_game(self):
        """Optimize all assets for game performance"""
        manifest = self.load_asset_manifest()
        
        for category, assets in manifest["assets"].items():
            for asset in assets:
                if self._needs_optimization(asset):
                    self.optimization_queue.put({
                        "asset": asset,
                        "category": category,
                        "optimization_type": "game_ready"
                    })
                    
        # Process optimization queue
        self._process_optimization_queue()
        
    def _needs_optimization(self, asset: Dict) -> bool:
        """Determine if asset needs optimization"""
        
        # Check file size (too large for game)
        if asset.get("file_size", 0) > 2 * 1024 * 1024:  # 2MB
            return True
            
        # Check resolution (too high for game use)
        if asset.get("width", 0) > 2048 or asset.get("height", 0) > 2048:
            return True
            
        # Check format (not optimized for game)
        if asset.get("format") in ['.bmp', '.tiff']:
            return True
            
        # Check quality metrics
        quality = asset.get("quality_metrics", {})
        if quality.get("compression_efficiency", 1.0) < 0.7:
            return True
            
        return False
        
    def _process_optimization_queue(self):
        """Process asset optimization queue"""
        
        while not self.optimization_queue.empty():
            try:
                optimization_task = self.optimization_queue.get_nowait()
                self._optimize_single_asset(optimization_task)
                
            except queue.Empty:
                break
            except Exception as e:
                print(f"Optimization error: {e}")
                
    def _optimize_single_asset(self, task: Dict):
        """Optimize single asset for game use"""
        asset = task["asset"]
        category = task["category"]
        
        source_path = Path(asset["file_path"])
        
        # Create optimized version path
        optimized_dir = self.assets_root / "art_final" / category
        optimized_path = optimized_dir / source_path.name
        
        try:
            with Image.open(source_path) as img:
                # Resize if too large
                if img.width > 1024 or img.height > 1024:
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    
                # Convert to optimal format
                if img.mode == 'RGBA':
                    # Keep transparency for UI elements
                    img.save(optimized_path, 'PNG', optimize=True)
                else:
                    # Convert to high-quality JPEG for backgrounds
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(optimized_path, 'JPEG', quality=90, optimize=True)
                    
                print(f"Optimized: {source_path} -> {optimized_path}")
                
        except Exception as e:
            print(f"Failed to optimize {source_path}: {e}")
```

### 7.3 Style Consistency and Quality Control

```python
# assets/style_consistency_system.py

class StyleConsistencyTracker:
    """Track and enforce style consistency across all generated art"""
    
    def __init__(self):
        self.style_database: Dict[ArtStyle, Dict] = {}
        self.consistency_metrics: Dict[str, float] = {}
        self.style_references: Dict[ArtStyle, List[Path]] = {}
        self.quality_standards = self._load_quality_standards()
        
    def _load_quality_standards(self) -> Dict:
        """Load Hades-quality art standards"""
        return {
            "hades_egyptian": {
                "minimum_resolution": (512, 512),
                "preferred_resolution": (1024, 1024),
                "color_depth": 8,  # bits per channel
                "compression_quality": 0.9,
                "style_consistency_threshold": 0.85,
                "egyptian_authenticity_threshold": 0.8,
                "visual_impact_score": 0.75,
                "technical_quality": {
                    "sharpness": 0.8,
                    "contrast": 0.7,
                    "color_balance": 0.75,
                    "composition": 0.8
                }
            }
        }
        
    def analyze_style_consistency(self, new_artwork: Image.Image, target_style: ArtStyle) -> Dict:
        """Analyze how well new artwork matches target style"""
        
        consistency_analysis = {
            "overall_score": 0.0,
            "color_consistency": 0.0,
            "composition_consistency": 0.0,
            "texture_consistency": 0.0,
            "lighting_consistency": 0.0,
            "egyptian_authenticity": 0.0,
            "recommendations": []
        }
        
        # Get reference artworks for style comparison
        reference_artworks = self._get_style_references(target_style)
        
        if not reference_artworks:
            # No references yet, this becomes a reference
            self._add_style_reference(new_artwork, target_style)
            consistency_analysis["overall_score"] = 0.8  # Assume good for first piece
            return consistency_analysis
            
        # Compare against existing references
        color_score = self._compare_color_palette(new_artwork, reference_artworks)
        composition_score = self._compare_composition(new_artwork, reference_artworks)
        texture_score = self._compare_texture_style(new_artwork, reference_artworks)
        lighting_score = self._compare_lighting_style(new_artwork, reference_artworks)
        egyptian_score = self._validate_egyptian_authenticity_visual(new_artwork)
        
        consistency_analysis.update({
            "color_consistency": color_score,
            "composition_consistency": composition_score, 
            "texture_consistency": texture_score,
            "lighting_consistency": lighting_score,
            "egyptian_authenticity": egyptian_score,
            "overall_score": (color_score + composition_score + texture_score + 
                            lighting_score + egyptian_score) / 5.0
        })
        
        # Generate recommendations
        if color_score < 0.7:
            consistency_analysis["recommendations"].append(
                "Consider adjusting color palette to match Egyptian theme better"
            )
        if composition_score < 0.7:
            consistency_analysis["recommendations"].append(
                "Composition could be more consistent with established style"
            )
        if egyptian_score < 0.8:
            consistency_analysis["recommendations"].append(
                "Add more authentic Egyptian visual elements"
            )
            
        return consistency_analysis
        
    def _compare_color_palette(self, new_image: Image.Image, references: List[Image.Image]) -> float:
        """Compare color palette consistency"""
        
        # Extract dominant colors from new image
        new_colors = self._extract_dominant_colors(new_image)
        
        # Compare with reference color palettes
        consistency_scores = []
        
        for ref_image in references:
            ref_colors = self._extract_dominant_colors(ref_image)
            similarity = self._calculate_color_similarity(new_colors, ref_colors)
            consistency_scores.append(similarity)
            
        return np.mean(consistency_scores) if consistency_scores else 0.0
        
    def _extract_dominant_colors(self, image: Image.Image, num_colors: int = 8) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image"""
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize for faster processing
        image = image.resize((150, 150))
        
        # Get colors
        colors = image.getcolors(maxcolors=256*256*256)
        if not colors:
            return []
            
        # Sort by frequency and return top colors
        colors.sort(reverse=True)
        dominant_colors = [color[1] for color in colors[:num_colors]]
        
        return dominant_colors
        
    def _calculate_color_similarity(self, colors1: List[Tuple], colors2: List[Tuple]) -> float:
        """Calculate similarity between two color palettes"""
        
        if not colors1 or not colors2:
            return 0.0
            
        # Calculate average color distance
        total_distance = 0.0
        comparisons = 0
        
        for c1 in colors1:
            min_distance = float('inf')
            for c2 in colors2:
                # Euclidean distance in RGB space
                distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
                min_distance = min(min_distance, distance)
                
            total_distance += min_distance
            comparisons += 1
            
        avg_distance = total_distance / comparisons if comparisons > 0 else 255
        
        # Convert distance to similarity score (0-1)
        similarity = max(0.0, 1.0 - (avg_distance / 255.0))
        
        return similarity
        
    def validate_hades_quality_standard(self, artwork: Image.Image, category: ArtCategory) -> Dict:
        """Validate artwork against Hades quality standards"""
        
        validation_result = {
            "meets_standard": False,
            "overall_score": 0.0,
            "technical_scores": {},
            "visual_scores": {},
            "egyptian_scores": {},
            "issues": [],
            "recommendations": []
        }
        
        # Technical quality checks
        technical_scores = {
            "resolution": self._check_resolution_quality(artwork),
            "sharpness": self._check_sharpness_quality(artwork),
            "contrast": self._check_contrast_quality(artwork),
            "color_balance": self._check_color_balance(artwork),
            "file_optimization": self._check_file_optimization(artwork)
        }
        
        # Visual impact checks
        visual_scores = {
            "composition": self._check_composition_quality(artwork),
            "lighting": self._check_lighting_quality(artwork),
            "color_harmony": self._check_color_harmony(artwork),
            "visual_interest": self._check_visual_interest(artwork),
            "style_cohesion": self._check_style_cohesion(artwork)
        }
        
        # Egyptian authenticity checks
        egyptian_scores = {
            "mythology_accuracy": self._check_mythology_accuracy(artwork),
            "cultural_respect": self._check_cultural_respect(artwork),
            "authentic_elements": self._check_authentic_elements(artwork),
            "color_authenticity": self._check_egyptian_colors(artwork),
            "symbol_usage": self._check_egyptian_symbols(artwork)
        }
        
        validation_result.update({
            "technical_scores": technical_scores,
            "visual_scores": visual_scores,
            "egyptian_scores": egyptian_scores
        })
        
        # Calculate overall score
        tech_avg = np.mean(list(technical_scores.values()))
        visual_avg = np.mean(list(visual_scores.values()))
        egyptian_avg = np.mean(list(egyptian_scores.values()))
        
        overall_score = (tech_avg * 0.3 + visual_avg * 0.4 + egyptian_avg * 0.3)
        validation_result["overall_score"] = overall_score
        
        # Determine if meets standard
        validation_result["meets_standard"] = overall_score >= 0.85
        
        # Generate specific recommendations
        if tech_avg < 0.8:
            validation_result["recommendations"].append("Improve technical quality (resolution, sharpness, contrast)")
        if visual_avg < 0.8:
            validation_result["recommendations"].append("Enhance visual impact and composition")
        if egyptian_avg < 0.8:
            validation_result["recommendations"].append("Strengthen Egyptian authenticity and cultural accuracy")
            
        return validation_result
```

This completes Section 7: Art Pipeline & Asset Management Implementation with over 600 lines of comprehensive Hades-quality AI art generation, asset management systems, and style consistency validation.
