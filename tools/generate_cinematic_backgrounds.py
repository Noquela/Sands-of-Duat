#!/usr/bin/env python3
"""
Generate cinematic Hades-quality backgrounds for Sands of Duat.
Focus on deck builder and progression screen backgrounds.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.hades_style_art_generator import HadesStyleArtGenerator

def main():
    print("SANDS OF DUAT - Cinematic Backgrounds Generator")
    print("=" * 50)
    
    # Define missing backgrounds with optimized prompts
    backgrounds = {
        "deck_builder_background": (
            "Hades game style, masterpiece illustration, "
            "ancient Egyptian temple library, scholarly chamber, "
            "papyrus scrolls everywhere, magical writing implements, "
            "Thoth's wisdom shrine, peaceful study atmosphere, "
            "warm candlelight, stone columns with hieroglyphs, "
            "ancient library aesthetic, dramatic lighting"
        ),
        "progression_background": (
            "Hades game style, masterpiece illustration, "
            "map of Egyptian underworld, Duat realm passages, "
            "glowing pathways through afterlife, divine judgment chambers, "
            "mystical journey map, celestial Egyptian art style, "
            "golden constellation patterns, ethereal lighting, "
            "ancient cartography aesthetic"
        )
    }
    
    # Initialize generator
    generator = HadesStyleArtGenerator(model="sdxl", high_quality=True)
    generator.load_pipeline()
    
    output_dir = project_root / "game_assets" / "environments" / "hades_quality"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    successful = 0
    total = len(backgrounds)
    
    for i, (bg_name, prompt) in enumerate(backgrounds.items()):
        print(f"\nGenerating {bg_name} ({i+1}/{total})...")
        
        output_path = str(output_dir / f"{bg_name}.png")
        
        # Generate with HD settings for backgrounds
        if generator.generate_professional_image(
            prompt, output_path,
            width=1920, height=1080,  # HD resolution
            steps=60,  # Higher quality for backgrounds
            cfg=7.0,  # Slightly lower CFG for backgrounds
            seed=100 + i
        ):
            successful += 1
            print(f"✓ Successfully generated: {bg_name}")
        else:
            print(f"✗ Failed to generate: {bg_name}")
    
    print(f"\n" + "=" * 50)
    print(f"Background Generation Complete: {successful}/{total}")
    print(f"Backgrounds saved to: {output_dir}")

if __name__ == "__main__":
    main()