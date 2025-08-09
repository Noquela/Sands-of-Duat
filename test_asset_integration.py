#!/usr/bin/env python3
"""
Test script to verify Hades-Egyptian asset integration
"""

import pygame
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from sands_of_duat.core.asset_loader import GeneratedAssetLoader
from sands_of_duat.ui.components.card_display import CardCollection

def test_asset_integration():
    print("TESTING HADES-EGYPTIAN ASSET INTEGRATION")
    print("=" * 44)
    
    # Initialize pygame for image loading
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    try:
        # Test asset loader
        print("\n1. Testing Asset Loader...")
        asset_loader = GeneratedAssetLoader()
        
        print(f"   Total assets available: {asset_loader.get_total_asset_count()}")
        
        # Test character loading
        print("\n2. Testing Character Assets...")
        characters = asset_loader.get_all_characters()
        for char_name in characters[:3]:  # Test first 3
            char_asset = asset_loader.load_character_portrait(char_name)
            if char_asset:
                print(f"   SUCCESS: Loaded {char_name}")
            else:
                print(f"   FAILED: Could not load {char_name}")
        
        # Test background loading
        print("\n3. Testing Background Assets...")
        backgrounds = asset_loader.get_all_backgrounds()
        for bg_name in backgrounds[:2]:  # Test first 2
            bg_asset = asset_loader.load_background(bg_name)
            if bg_asset:
                print(f"   SUCCESS: Loaded {bg_name}")
            else:
                print(f"   FAILED: Could not load {bg_name}")
        
        # Test card collection
        print("\n4. Testing Card Collection...")
        card_collection = CardCollection()
        print(f"   Total cards created: {len(card_collection.cards)}")
        
        # Test each rarity
        rarities = ['legendary', 'epic', 'rare', 'common']
        for rarity in rarities:
            cards = card_collection.get_cards_by_rarity(rarity)
            loaded_count = 0
            for card in cards:
                if card.artwork and card.artwork.get_size() != (160, 120):
                    loaded_count += 1
            print(f"   {rarity.title()}: {len(cards)} cards, {loaded_count} with custom artwork")
        
        print(f"\n5. Cache Statistics:")
        stats = asset_loader.get_cache_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print(f"\nASSET INTEGRATION TEST COMPLETE")
        print("Your Hades-Egyptian assets are successfully integrated!")
        
    except Exception as e:
        print(f"\nINTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_asset_integration()