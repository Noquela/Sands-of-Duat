#!/usr/bin/env python3
"""
Generate AI backgrounds for all game screens
Optimized for 3440x1440 ultrawide resolution
"""

import torch
from ultra_ai_pipeline import UltraAIPipeline, AssetConfig

def main():
    print("[BACKGROUNDS] Generating AI backgrounds for 3440x1440...")
    
    # Initialize pipeline
    pipeline = UltraAIPipeline("game_assets")
    
    backgrounds = {
        # Menu/Main screens
        "menu_background": "Epic Egyptian desert landscape at sunset, pyramid silhouettes, golden sand dunes, ancient temple ruins in distance, cinematic ultrawide composition",
        "map_background": "Ancient Egyptian temple courtyard, stone columns with hieroglyphs, desert vista beyond walls, atmospheric lighting, ultrawide panoramic view",
        "combat_background": "Egyptian tomb interior, massive stone chambers, flickering torchlight, mysterious shadows, epic battle arena atmosphere, ultrawide cinematic",
        
        # Specific environments  
        "desert_battlefield": "Vast Egyptian desert battlefield, ancient warrior camp, banners in wind, pyramid backdrop, dramatic sky, ultrawide epic landscape",
        "temple_interior": "Grand Egyptian temple hall, towering columns, golden hieroglyphs, ray of sunlight through ceiling, majestic ultrawide architecture",
        "tomb_chamber": "Ancient pharaoh burial chamber, golden sarcophagi, treasure chests, mystical blue lighting, atmospheric ultrawide composition",
        
        # Additional environments
        "oasis_sanctuary": "Peaceful desert oasis, palm trees, crystal clear water, Egyptian temple by the shore, serene ultrawide paradise",
        "pyramid_chamber": "Inside great pyramid, massive stone blocks, mysterious hieroglyphic walls, golden light shafts, ultrawide architectural marvel"
    }
    
    generated = []
    total = len(backgrounds)
    current = 0
    
    for bg_name, prompt in backgrounds.items():
        current += 1
        print(f"[{current}/{total}] Generating: {bg_name}")
        
        config = AssetConfig(
            name=bg_name,
            type="environment",
            prompt=f"{prompt}, 3440x1440 ultrawide resolution, professional game art, high detail",
            size=(3440, 1440),  # Ultrawide resolution
            steps=50,  # Good quality but faster than 60 steps
            guidance=8.0
        )
        
        result = pipeline.generate_ultra_image(config)
        if result:
            generated.append(result)
            print(f"   [OK] {result}")
        else:
            print(f"   [ERROR] Failed: {bg_name}")
    
    print(f"\n[COMPLETE] Generated {len(generated)}/{total} ultrawide backgrounds!")
    return generated

if __name__ == "__main__":
    main()