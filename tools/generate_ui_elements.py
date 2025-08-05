#!/usr/bin/env python3
"""
Generate ornate Egyptian UI elements for Sands of Duat.
Professional quality elements with Hades-style craftsmanship.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.hades_style_art_generator import HadesStyleArtGenerator

def main():
    print("SANDS OF DUAT - UI Elements Generator")
    print("=" * 50)
    
    # Define UI elements with optimized prompts
    ui_elements = {
        "ornate_button": (
            "Hades game style, ornate Egyptian button design, "
            "golden hieroglyphic border, carved stone texture, "
            "ancient Egyptian decorative elements, clickable UI element, "
            "professional game UI, bronze and gold accents"
        ),
        "card_frame": (
            "Hades game style, elegant Egyptian card frame border, "
            "intricate golden decorations, hieroglyphic patterns, "
            "papyrus texture background, professional card game design, "
            "ornate frame artwork"
        ),
        "health_orb": (
            "Hades game style, Egyptian scarab health orb, "
            "golden beetle with gem center, life force energy, "
            "glowing magical essence, UI health indicator design, "
            "intricate metalwork details"
        ),
        "mana_crystal": (
            "Hades game style, Egyptian ankh mana crystal, "
            "mystical blue energy core, golden ankh structure, "
            "magical power reservoir, UI mana indicator design, "
            "ethereal energy glow"
        )
    }
    
    # Initialize generator
    generator = HadesStyleArtGenerator(model="sdxl", high_quality=True)
    generator.load_pipeline()
    
    output_dir = project_root / "game_assets" / "ui_elements" / "hades_quality"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    successful = 0
    total = len(ui_elements)
    
    for i, (element_name, prompt) in enumerate(ui_elements.items()):
        print(f"\nGenerating {element_name} ({i+1}/{total})...")
        
        output_path = str(output_dir / f"{element_name}.png")
        
        # Generate with UI-appropriate settings
        if generator.generate_professional_image(
            prompt, output_path,
            width=256, height=256,  # UI element size
            steps=50,
            cfg=7.5,
            seed=200 + i
        ):
            successful += 1
            print(f"✓ Successfully generated: {element_name}")
        else:
            print(f"✗ Failed to generate: {element_name}")
    
    print(f"\n" + "=" * 50)
    print(f"UI Elements Generation Complete: {successful}/{total}")
    print(f"Elements saved to: {output_dir}")

if __name__ == "__main__":
    main()