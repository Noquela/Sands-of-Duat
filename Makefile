# 🏺 HADES-QUALITY 3D GAME MAKEFILE
# Complete pipeline automation for Sands of Duat

# Configuration
PYTHON = python
BLENDER = "C:/Program Files/Blender Foundation/Blender 4.5/blender.exe"
CARGO = "C:/Users/Bruno/.cargo/bin/cargo.exe"

# Directories
TOOLS_3D = tools/3d_pipeline
ASSETS_3D = assets/3d
CONCEPTS = $(ASSETS_3D)/concepts  
RAW_MESHES = $(ASSETS_3D)/raw_meshes
CHARACTERS = $(ASSETS_3D)/characters

# Default characters to create
CHARACTERS_LIST = pharaoh_hero anubis_boss mummy_enemy isis_npc

.PHONY: all setup clean characters character concept mesh process run help

# Default target
all: setup characters run

# Help
help:
	@echo "🏺 Hades-Quality 3D Pipeline Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install all dependencies and setup pipeline"
	@echo ""
	@echo "Asset Creation:"
	@echo "  make characters     - Create all default characters"
	@echo "  make character NAME=pharaoh_hero PROMPT='Egyptian pharaoh warrior'"
	@echo "  make concept NAME=pharaoh_hero PROMPT='Egyptian pharaoh warrior'"
	@echo "  make mesh NAME=pharaoh_hero"  
	@echo "  make process NAME=pharaoh_hero"
	@echo ""
	@echo "Game:"
	@echo "  make run           - Build and run the game"
	@echo "  make build         - Build the game in release mode"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         - Clean generated assets"
	@echo "  make help          - Show this help"

# Setup pipeline
setup:
	@echo "🏺 Setting up Hades-Quality 3D Pipeline..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r $(TOOLS_3D)/requirements_3d.txt
	@mkdir -p $(CONCEPTS) $(RAW_MESHES) $(CHARACTERS)
	@$(PYTHON) $(TOOLS_3D)/hades_3d_pipeline.py --setup
	@echo "✅ Pipeline setup complete!"

# Create all default characters
characters: $(addprefix character-, $(CHARACTERS_LIST))

# Create individual character (usage: make character NAME=pharaoh_hero PROMPT="Egyptian pharaoh warrior")
character:
ifndef NAME
	@echo "❌ Please specify NAME: make character NAME=pharaoh_hero PROMPT='description'"
	@exit 1
endif
ifndef PROMPT
	@echo "❌ Please specify PROMPT: make character NAME=pharaoh_hero PROMPT='description'"  
	@exit 1
endif
	@echo "🏺 Creating character: $(NAME)"
	@$(PYTHON) $(TOOLS_3D)/hades_3d_pipeline.py --character $(NAME) --prompt "$(PROMPT)"

# Individual character targets
character-pharaoh_hero:
	@$(MAKE) character NAME=pharaoh_hero PROMPT="Egyptian pharaoh warrior, golden ceremonial armor with hieroglyphs, royal headdress, confident heroic pose, muscular build, holding khopesh sword, blue and gold color scheme"

character-anubis_boss:
	@$(MAKE) character NAME=anubis_boss PROMPT="Anubis god of death, jackal head, ancient Egyptian deity, ornate golden armor, staff of judgment, tall imposing figure, dark blue and gold colors, mystical aura, boss character"

character-mummy_enemy:
	@$(MAKE) character NAME=mummy_enemy PROMPT="Ancient Egyptian mummy warrior, wrapped in bandages, glowing eyes, shambling pose, weathered and ancient, carrying curved blade, sandy brown and bone colors"

character-isis_npc:
	@$(MAKE) character NAME=isis_npc PROMPT="Isis goddess, elegant Egyptian deity, flowing robes, feathered headdress, graceful pose, healing magic, white and gold colors, serene expression"

# Individual pipeline steps
concept:
ifndef NAME
	@echo "❌ Please specify NAME: make concept NAME=pharaoh_hero PROMPT='description'"
	@exit 1
endif
ifndef PROMPT
	@echo "❌ Please specify PROMPT: make concept NAME=pharaoh_hero PROMPT='description'"
	@exit 1
endif
	@echo "🎨 Generating concept for: $(NAME)"
	@mkdir -p $(CONCEPTS)
	@$(PYTHON) $(TOOLS_3D)/concept_generator.py --character $(NAME) --prompt "$(PROMPT)" --output $(CONCEPTS)

mesh:
ifndef NAME
	@echo "❌ Please specify NAME: make mesh NAME=pharaoh_hero"
	@exit 1
endif
	@echo "🔺 Creating mesh for: $(NAME)"
	@mkdir -p $(RAW_MESHES)
	@$(PYTHON) $(TOOLS_3D)/triposr_generator.py --input $(CONCEPTS)/$(NAME)_concept.png --output $(RAW_MESHES)/$(NAME).obj

process:
ifndef NAME
	@echo "❌ Please specify NAME: make process NAME=pharaoh_hero"
	@exit 1
endif
	@echo "🔧 Processing in Blender: $(NAME)"
	@mkdir -p $(CHARACTERS)
	@$(BLENDER) --background --python $(TOOLS_3D)/blender_hades_processor.py -- $(RAW_MESHES)/$(NAME).obj $(CHARACTERS)/$(NAME).glb $(NAME)

# Game targets
build:
	@echo "🏗️ Building Sands of Duat..."
	@$(CARGO) build --release

run: build
	@echo "🎮 Running Sands of Duat..."
	@$(CARGO) run --release

# Quick development run
dev:
	@echo "🚀 Running in development mode..."
	@$(CARGO) run

# Clean generated assets
clean:
	@echo "🧹 Cleaning generated assets..."
	@rm -rf $(CONCEPTS)/* $(RAW_MESHES)/* $(CHARACTERS)/*
	@echo "✅ Assets cleaned"