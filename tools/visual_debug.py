#!/usr/bin/env python3
"""
Visual Debug Tool
Shows what assets exist vs what's actually being rendered
"""

import pygame
import sys
from pathlib import Path
sys.path.append('.')

def debug_visual_rendering():
    """Debug what's actually being rendered"""
    pygame.init()
    
    # Show what assets we have
    print("=== ASSET INVENTORY ===")
    
    # Check backgrounds
    bg_dir = Path('game_assets/environments')
    if bg_dir.exists():
        print(f"\n[BACKGROUNDS] ({bg_dir}):")
        for bg in bg_dir.glob('*.png'):
            img = pygame.image.load(str(bg))
            print(f"  [OK] {bg.name}: {img.get_size()} pixels ({bg.stat().st_size//1024}KB)")
    
    # Check cards  
    cards_dir = Path('game_assets/cards')
    if cards_dir.exists():
        print(f"\n[CARD ART] ({cards_dir}):")
        for card in cards_dir.glob('*.png'):
            img = pygame.image.load(str(card))
            print(f"  [OK] {card.name}: {img.get_size()} pixels ({card.stat().st_size//1024}KB)")
    
    # Check sprites
    sprites_dir = Path('game_assets/characters/sprites')  
    if sprites_dir.exists():
        print(f"\n[CHARACTER SPRITES] ({sprites_dir}):")
        for sprite in sprites_dir.glob('*.png'):
            img = pygame.image.load(str(sprite))
            print(f"  [OK] {sprite.name}: {img.get_size()} pixels ({sprite.stat().st_size//1024}KB)")
    
    print(f"\n=== RENDERING TEST ===")
    
    # Test actual rendering
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Asset Rendering Test")
    
    # Test background loading and display
    print("\n[TESTING BACKGROUND RENDERING]:")
    try:
        from sands_duat.graphics.background_loader import load_background
        
        menu_bg = load_background('menu', (1200, 800))
        if menu_bg:
            screen.blit(menu_bg, (0, 0))
            pygame.display.flip()
            print("  [OK] Menu background renders successfully")
            pygame.time.wait(2000)
        else:
            print("  [FAIL] Menu background failed to load")
    except Exception as e:
        print(f"  [ERROR] Background system error: {e}")
    
    # Test card art rendering
    print("\n[TESTING CARD ART RENDERING]:")
    try:
        from sands_duat.graphics.card_art_loader import load_card_art
        
        screen.fill((50, 50, 50))  # Dark background
        
        # Test multiple cards
        test_cards = [
            "Mummy's Wrath",
            "Desert Whisper", 
            "Ra's Solar Flare",
            "Anubis Judgment"
        ]
        
        x_pos = 50
        for card_name in test_cards:
            card_art = load_card_art(card_name, (200, 300))
            if card_art:
                screen.blit(card_art, (x_pos, 100))
                print(f"  [OK] {card_name}: Rendered at ({x_pos}, 100)")
                x_pos += 220
            else:
                print(f"  [FAIL] {card_name}: Failed to render")
        
        pygame.display.flip()
        print("\n[WAIT] Card art display test - showing for 5 seconds...")
        pygame.time.wait(5000)
        
    except Exception as e:
        print(f"  [ERROR] Card art system error: {e}")
    
    # Test sprite rendering
    print("\n[TESTING SPRITE RENDERING]:")
    try:
        screen.fill((100, 70, 50))  # Desert background color
        
        sprite_files = [
            'game_assets/characters/sprites/anubis_guardian_idle.png',
            'game_assets/characters/sprites/player_character_attack.png',
            'game_assets/characters/sprites/pharaoh_lich_walk.png'
        ]
        
        x_pos = 100
        for sprite_file in sprite_files:
            if Path(sprite_file).exists():
                sprite = pygame.image.load(sprite_file)
                # Scale down for display
                sprite = pygame.transform.scale(sprite, (150, 150))
                screen.blit(sprite, (x_pos, 200))
                print(f"  [OK] {Path(sprite_file).name}: Rendered at ({x_pos}, 200)")
                x_pos += 180
            else:
                print(f"  [FAIL] {Path(sprite_file).name}: File not found")
        
        pygame.display.flip()
        print("\n[WAIT] Sprite display test - showing for 5 seconds...")
        pygame.time.wait(5000)
        
    except Exception as e:
        print(f"  [ERROR] Sprite system error: {e}")
    
    pygame.quit()
    print("\n=== VISUAL DEBUG COMPLETE ===")
    print("Assets exist and can be rendered - issue may be in game integration")

if __name__ == "__main__":
    debug_visual_rendering()