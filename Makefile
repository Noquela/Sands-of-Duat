.PHONY: assets cleanbg atlas ui pack run setup clean

# Main targets
assets: cleanbg atlas ui pack

setup:
	python -m venv .venv
	.venv/Scripts/pip install -r tools/requirements.txt
	@echo "Setup complete! Activate with: .venv\\Scripts\\activate"

cleanbg:
	@echo "Removing backgrounds from raw SDXL images..."
	.venv/Scripts/python tools/clean_bg.py art/sdxl/raw art/sdxl/clean
	.venv/Scripts/python tools/halo_fix.py art/sdxl/clean art/sdxl/clean

atlas:
	@echo "Creating sprite atlases..."
	@if exist art\\sdxl\\clean\\player_idle ( \
		.venv/Scripts/python tools/make_atlas.py art/sdxl/clean/player_idle assets/sprites/player_idle.png assets/sprites/player_idle.json \
	) else ( \
		echo "No player_idle folder found in art/sdxl/clean/" \
	)

ui:
	@echo "Processing UI icons..."
	@echo "UI vectorization requires ImageMagick and potrace - install manually if needed"

pack:
	@echo "Packing all assets..."
	.venv/Scripts/python tools/pack_assets.py

run:
	cargo run --release

clean:
	@echo "Cleaning generated assets..."
	rmdir /s /q art\\sdxl\\clean 2>nul || echo "Clean folder already empty"
	rmdir /s /q assets\\sprites 2>nul || echo "Sprites folder already empty"
	rmdir /s /q assets\\textures 2>nul || echo "Textures folder already empty"
	rmdir /s /q assets\\ui 2>nul || echo "UI folder already empty"

check:
	@echo "Checking transparency in processed assets..."
	@if exist art\\sdxl\\clean ( \
		.venv/Scripts/python tools/check_transparency.py art/sdxl/clean \
	) else ( \
		echo "No clean assets to check" \
	)

# Development workflow
dev: assets run