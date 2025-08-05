#!/usr/bin/env python3
"""
Completar geração dos assets restantes - Sprites + Ambientes
"""

import torch
from ultra_ai_pipeline import UltraAIPipeline, AssetConfig

def main():
    print("[COMPLETE] Gerando assets restantes...")
    
    # Inicializar pipeline
    pipeline = UltraAIPipeline("game_assets")
    
    generated = []
    total_needed = 20
    current = 0
    
    # SPRITES (15 assets)
    print("\n[SPRITES] Gerando sprites de personagens...")
    characters = {
        "anubis_guardian": "Anubis guardian warrior sprite, game character, clean background",
        "desert_scorpion": "Desert scorpion sprite, game enemy, clean background", 
        "pharaoh_lich": "Pharaoh lich sprite, undead king, game character, clean background",
        "temple_guardian": "Temple guardian statue sprite, game character, clean background",
        "player_character": "Egyptian warrior sprite, player character, clean background"
    }
    
    for char_name in characters.keys():
        for action in ["idle", "walk", "attack"]:
            current += 1
            sprite_name = f"{char_name}_{action}"
            print(f"[{current}/{total_needed}] Gerando sprite: {sprite_name}")
            
            config = AssetConfig(
                name=sprite_name,
                type="character_sprite",
                prompt=f"{characters[char_name]}, {action} pose, pixel art style, 512x512",
                size=(512, 512),
                steps=60,
                guidance=7.5
            )
            
            result = pipeline.generate_ultra_image(config)
            if result:
                generated.append(result)
                print(f"   [OK] {result}")
            else:
                print(f"   [ERRO] Falhou: {sprite_name}")
    
    # AMBIENTES (5 assets)  
    print("\n[AMBIENTES] Gerando backgrounds 4K...")
    environments = {
        "desert_battlefield": "Epic Egyptian desert battlefield, sand dunes, ancient ruins, dramatic sunset",
        "temple_interior": "Grand Egyptian temple interior, massive columns, hieroglyphic walls, torch lighting",
        "tomb_chamber": "Ancient pharaoh tomb chamber, golden sarcophagi, treasure, mysterious atmosphere", 
        "oasis": "Peaceful desert oasis, palm trees, crystal water, Egyptian setting, serene",
        "pyramid_chamber": "Inside great pyramid chamber, massive stone blocks, mystical lighting, architecture"
    }
    
    for env_name, prompt in environments.items():
        current += 1
        print(f"[{current}/{total_needed}] Gerando ambiente: {env_name}")
        
        config = AssetConfig(
            name=env_name,
            type="environment", 
            prompt=f"{prompt}, 4K quality, cinematic landscape, ultra wide",
            size=(2560, 1440),
            steps=60,
            guidance=9.0
        )
        
        result = pipeline.generate_ultra_image(config)
        if result:
            generated.append(result)
            print(f"   [OK] {result}")
        else:
            print(f"   [ERRO] Falhou: {env_name}")
    
    print(f"\n[FINAL] Gerados {len(generated)}/{total_needed} assets restantes!")
    return generated

if __name__ == "__main__":
    main()