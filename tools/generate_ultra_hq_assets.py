#!/usr/bin/env python3
"""
ULTRA HIGH QUALITY ASSET GENERATION - RTX 5070 HADES STANDARD
Generate all assets in maximum resolution for professional Hades-quality game
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

def main():
    """Generate all ultra high quality assets for Sands of Duat"""
    
    print("=" * 80)
    print("[PYRAMID] SANDS OF DUAT - ULTRA HIGH QUALITY ASSET GENERATION [PYRAMID]")
    print("=" * 80)
    print("RTX 5070 CUDA 12.8 + SDXL + LoRA Pipeline")
    print("Hades-Quality Egyptian Art Generation")
    print("=" * 80)
    print()
    
    # Import generation functions
    from sands_of_duat.ai_art.ai_generation_pipeline import (
        generate_all_egyptian_cards,
        generate_all_backgrounds, 
        generate_all_characters
    )
    
    total_start_time = time.time()
    all_results = {}
    
    print("[CARDS] PHASE 1: ULTRA HIGH RESOLUTION CARDS (1024x1536)")
    print("-" * 60)
    card_results = generate_all_egyptian_cards()
    all_results["cards"] = card_results
    card_success = sum(1 for success in card_results.values() if success)
    print(f"[SUCCESS] Cards: {card_success}/{len(card_results)} generated successfully")
    print()
    
    print("[BACKGROUNDS] PHASE 2: PANORAMIC BACKGROUNDS (4096x2048)")
    print("-" * 60)
    bg_results = generate_all_backgrounds()
    all_results["backgrounds"] = bg_results
    bg_success = sum(1 for success in bg_results.values() if success)
    print(f"[SUCCESS] Backgrounds: {bg_success}/{len(bg_results)} generated successfully")
    print()
    
    print("[CHARACTERS] PHASE 3: CHARACTER PORTRAITS (2048x2048)")  
    print("-" * 60)
    char_results = generate_all_characters()
    all_results["characters"] = char_results
    char_success = sum(1 for success in char_results.values() if success)
    print(f"[SUCCESS] Characters: {char_success}/{len(char_results)} generated successfully")
    print()
    
    # Generate UI elements
    print("[UI] PHASE 4: UI ELEMENTS AND ICONS")
    print("-" * 60)
    ui_results = generate_ui_elements()
    all_results["ui"] = ui_results
    ui_success = sum(1 for success in ui_results.values() if success)
    print(f"[SUCCESS] UI Elements: {ui_success}/{len(ui_results)} generated successfully")
    print()
    
    total_time = time.time() - total_start_time
    total_assets = card_success + bg_success + char_success + ui_success
    total_possible = len(card_results) + len(bg_results) + len(char_results) + len(ui_results)
    
    print("=" * 80)
    print("[VICTORY] ULTRA HIGH QUALITY ASSET GENERATION COMPLETE")
    print("=" * 80)
    print(f"[TIME] Total Generation Time: {total_time/60:.1f} minutes")
    print(f"[STATS] Success Rate: {total_assets}/{total_possible} assets ({total_assets/total_possible*100:.1f}%)")
    print(f"[CARDS] Cards Generated: {card_success}/{len(card_results)} (1024x1536)")
    print(f"[BACKGROUNDS] Backgrounds Generated: {bg_success}/{len(bg_results)} (4096x2048)")
    print(f"[CHARACTERS] Characters Generated: {char_success}/{len(char_results)} (2048x2048)")
    print(f"[UI] UI Elements Generated: {ui_success}/{len(ui_results)} (various)")
    print()
    
    if total_assets == total_possible:
        print("[PERFECT] PERFECT SUCCESS! All assets generated with Hades quality!")
        print("[READY] Ready for ultra-high resolution gameplay!")
    elif total_assets > total_possible * 0.8:
        print("[EXCELLENT] Excellent results! Most assets generated successfully.")
        print("[CHECK] Check failed assets and retry if needed.")
    else:
        print("[WARNING] Some assets failed to generate. Check ComfyUI setup and retry.")
    
    print("=" * 80)
    return total_assets == total_possible

def generate_ui_elements():
    """Generate UI elements and icons"""
    
    # Import after adding path
    from sands_of_duat.ai_art.ai_generation_pipeline import get_pipeline
    
    pipeline = get_pipeline()
    results = {}
    
    ui_prompts = {
        "ankh_health_icon": f"{pipeline.prompts.BASE_STYLE}, golden egyptian ankh symbol, "
                           f"health icon, glowing divine energy, intricate details, "
                           f"512x512 icon resolution, game UI element",
        
        "scarab_energy_icon": f"{pipeline.prompts.BASE_STYLE}, mystical scarab beetle, "
                             f"energy icon, blue magical glow, egyptian ornaments, "
                             f"512x512 icon resolution, game UI element",
        
        "card_frame_legendary": f"{pipeline.prompts.BASE_STYLE}, ornate golden egyptian frame, "
                               f"legendary card border, hieroglyphic decorations, "
                               f"divine golden aura, intricate patterns, card frame template",
        
        "card_frame_epic": f"{pipeline.prompts.BASE_STYLE}, silver egyptian frame, "
                          f"epic card border, hieroglyphic engravings, "
                          f"mystical blue aura, detailed patterns, card frame template"
    }
    
    for ui_name, prompt in ui_prompts.items():
        print(f"    [GENERATING] {ui_name}...")
        
        # Determine resolution based on element type
        if "icon" in ui_name:
            width, height = 512, 512
        else:  # frames
            width, height = 1024, 1536  # Match card resolution
            
        image = pipeline.generator.generate_image(
            prompt=prompt,
            negative_prompt=pipeline.prompts.NEGATIVE_PROMPT,
            width=width,
            height=height,
            steps=50,
            cfg_scale=9.0
        )
        
        if image:
            filename = f"ui_{ui_name}.png"
            output_path = pipeline.approved_dir / "ui_elements" / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, 'PNG', quality=100)
            print(f"        [SUCCESS] {filename}")
            results[ui_name] = True
        else:
            print(f"        [FAILED] {ui_name}")
            results[ui_name] = False
    
    return results

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)