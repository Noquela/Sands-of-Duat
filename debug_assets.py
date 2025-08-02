#!/usr/bin/env python3
"""
Debug Assets - Quick test to see if assets are loading properly
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_asset_loading():
    """Test if our SDXL assets are loading properly"""
    
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    print("Testing asset loading...")
    
    from assets import load_assets, get_sprite
    
    # Load assets
    load_assets()
    
    # Check what assets are available
    from assets import asset_manager
    print(f"\nLoaded sprites: {list(asset_manager.sprites.keys())}")
    
    # Test specific sprites
    player_sprite = get_sprite("player_anubis")
    if player_sprite:
        print(f"Player sprite loaded: {player_sprite.get_size()}")
    else:
        print("Player sprite NOT loaded!")
    
    altar_ra = get_sprite("altar_ra")
    if altar_ra:
        print(f"Altar Ra loaded: {altar_ra.get_size()}")
    else:
        print("Altar Ra NOT loaded!")
    
    portal_arena = get_sprite("portal_arena")
    if portal_arena:
        print(f"Portal arena loaded: {portal_arena.get_size()}")
    else:
        print("Portal arena NOT loaded!")

if __name__ == "__main__":
    test_asset_loading()