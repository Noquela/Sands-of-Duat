#!/usr/bin/env python
import shutil, pathlib

def cp(source, dest):
    pa, pb = pathlib.Path(source), pathlib.Path(dest)
    if not pa.exists():
        print(f"Warning: {pa} not found, skipping...")
        return
    pb.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pa, pb)
    print(f"Copied: {pa} -> {pb}")

# Texture mappings
texture_mapping = {
    "art/sdxl/tiles_out/sand_albedo.png": "assets/textures/sand_albedo.png",
    "art/sdxl/tiles_out/stone_albedo.png": "assets/textures/stone_albedo.png", 
    "art/sdxl/tiles_out/rune_emit.png": "assets/textures/rune_emit.png",
}

print("Packing textures...")
for source, dest in texture_mapping.items():
    cp(source, dest)

# Copy sprites from clean folder
print("Packing sprites...")
sprites_dir = pathlib.Path("assets/sprites")
sprites_dir.mkdir(parents=True, exist_ok=True)
art_clean = pathlib.Path("art/sdxl/clean")
if art_clean.exists():
    for png_file in art_clean.glob("**/*.png"):
        if "atlas" not in png_file.name and "sheet" not in png_file.name:
            dest = sprites_dir / png_file.name
            cp(png_file, dest)

# Copy UI SVGs
print("Packing UI assets...")
ui_dir = pathlib.Path("assets/ui")
ui_dir.mkdir(parents=True, exist_ok=True)
ui_svg = pathlib.Path("art/sdxl/ui_svg")
if ui_svg.exists():
    for svg_file in ui_svg.glob("*.svg"):
        dest = ui_dir / svg_file.name
        cp(svg_file, dest)

print("OK: pack_assets -> assets/ completed")