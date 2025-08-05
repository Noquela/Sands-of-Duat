#!/usr/bin/env python3
"""
Quick script to generate missing Hades-quality cards for Sands of Duat.
Optimized for efficiency and quality.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.hades_style_art_generator import HadesStyleArtGenerator

def main():
    print("SANDS OF DUAT - Missing Cards Generator")
    print("=" * 50)
    
    # Priority cards that need Hades-style upgrades
    missing_cards = [
        "tomb_strike",
        "scarab_swarm", 
        "ankh_blessing",
        "pyramid_power",
        "papyrus_scroll",
        "desert_whisper",
        "thoths_wisdom",
        "pharaohs_resurrection",
        "mummys_wrath",
        "sand_grain"
    ]
    
    # Initialize generator
    generator = HadesStyleArtGenerator(model="sdxl", high_quality=True)
    generator.load_pipeline()
    
    output_dir = project_root / "game_assets" / "cards" / "hades_quality"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    successful = 0
    total = len(missing_cards)
    
    for i, card_name in enumerate(missing_cards):
        print(f"\nGenerating {card_name} ({i+1}/{total})...")
        
        # Get the optimized prompt
        if card_name in generator.prompts["cards"]:
            prompt = generator.prompts["cards"][card_name]
        else:
            print(f"Warning: No prompt found for {card_name}, skipping")
            continue
        
        output_path = str(output_dir / f"{card_name}.png")
        
        # Generate with optimal settings
        if generator.generate_professional_image(
            prompt, output_path,
            width=512, height=768,  # Card aspect ratio
            steps=50,  # Balanced quality/speed
            cfg=7.5,
            seed=42 + i
        ):
            successful += 1
            print(f"✓ Successfully generated: {card_name}")
        else:
            print(f"✗ Failed to generate: {card_name}")
    
    print(f"\n" + "=" * 50)
    print(f"Generation Complete: {successful}/{total} cards")
    print(f"Cards saved to: {output_dir}")

if __name__ == "__main__":
    main()