#!/usr/bin/env python3
"""
Generate AI backgrounds with memory-efficient approach
Create at 1920x1080 then upscale to 3440x1440
"""

import torch
import gc
from ultra_ai_pipeline import UltraAIPipeline, AssetConfig
from PIL import Image
from pathlib import Path

def main():
    print("[BACKGROUNDS] Generating memory-efficient AI backgrounds...")
    
    # Initialize pipeline
    pipeline = UltraAIPipeline("game_assets")
    
    backgrounds = {
        # Core backgrounds needed for gameplay
        "menu_background": "Epic Egyptian desert sunset, pyramid silhouettes, golden dunes, cinematic landscape",
        "combat_background": "Egyptian tomb chamber, stone walls, torchlight, battle arena atmosphere",
        "map_background": "Ancient Egyptian temple courtyard, stone columns, desert vista, atmospheric"
    }
    
    generated = []
    total = len(backgrounds)
    current = 0
    
    for bg_name, prompt in backgrounds.items():
        current += 1
        print(f"[{current}/{total}] Generating: {bg_name}")
        
        # Generate at smaller size first (save memory)
        config = AssetConfig(
            name=f"{bg_name}_base",
            type="environment",
            prompt=f"{prompt}, professional game background art, high detail, wide aspect ratio",
            size=(1920, 1080),  # Standard HD resolution
            steps=40,  # Fewer steps to save time/memory
            guidance=7.5
        )
        
        result = pipeline.generate_ultra_image(config)
        if result:
            # Load and upscale to ultrawide
            try:
                base_path = Path(result)
                if base_path.exists():
                    # Load base image
                    img = Image.open(base_path)
                    
                    # Upscale to ultrawide (stretch horizontally)
                    ultrawide_img = img.resize((3440, 1440), Image.Resampling.LANCZOS)
                    
                    # Save ultrawide version
                    final_path = base_path.parent / f"{bg_name}.png"
                    ultrawide_img.save(final_path, "PNG", optimize=True)
                    
                    # Remove base version
                    base_path.unlink()
                    
                    generated.append(str(final_path))
                    print(f"   [OK] Generated and upscaled: {final_path}")
                    
                    # Clear memory
                    del img, ultrawide_img
                    gc.collect()
                    torch.cuda.empty_cache()
                    
                else:
                    print(f"   [ERROR] Base file not found: {result}")
                    
            except Exception as e:
                print(f"   [ERROR] Upscaling failed: {e}")
        else:
            print(f"   [ERROR] Failed to generate: {bg_name}")
    
    print(f"\n[COMPLETE] Generated {len(generated)}/{total} ultrawide backgrounds!")
    return generated

if __name__ == "__main__":
    main()