#!/usr/bin/env python3
"""
Simple deck builder test without unicode characters.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_deck_builder():
    """Simple test of deck builder functionality."""
    print("1. Testing imports...")
    
    try:
        import pygame
        pygame.init()
        print("   OK: pygame import successful")
    except Exception as e:
        print(f"   ERROR: pygame import failed: {e}")
        return False
    
    try:
        from sands_duat.ui.deck_builder import DeckBuilderScreen, CardDisplay, CardCollection
        print("   OK: deck builder imports successful")
    except Exception as e:
        print(f"   ERROR: deck builder import failed: {e}")
        return False
    
    try:
        from sands_duat.ui.theme import initialize_theme
        print("   OK: theme system imports successful")
    except Exception as e:
        print(f"   ERROR: theme system import failed: {e}")
        return False
    
    print("\n2. Testing deck builder creation...")
    try:
        screen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
        theme = initialize_theme(1920, 1080)
        deck_builder = DeckBuilderScreen()
        print(f"   OK: deck builder created, theme mode: {theme.display.display_mode.value}")
        
        deck_builder.on_enter()
        print(f"   OK: deck builder entered, {len(deck_builder.components)} components created")
        
        # Check component details
        component_types = {}
        for comp in deck_builder.components:
            comp_type = type(comp).__name__
            component_types[comp_type] = component_types.get(comp_type, 0) + 1
            
            # Check for issues
            if not comp.visible:
                print(f"   WARNING: {comp_type} is not visible")
            if not comp.enabled:
                print(f"   WARNING: {comp_type} is not enabled")
            if comp.rect.width <= 0 or comp.rect.height <= 0:
                print(f"   ERROR: {comp_type} has invalid size: {comp.rect}")
        
        print(f"   Component breakdown: {component_types}")
        
        # Check card collection specifically
        if deck_builder.card_collection:
            cc = deck_builder.card_collection
            print(f"   Card collection: {len(cc.filtered_cards)} cards, {len(cc.card_displays)} displays")
            
            if len(cc.card_displays) == 0:
                print("   ERROR: No card displays created!")
                print(f"     Player collection has {len(cc.player_collection.owned_cards)} owned cards")
                print(f"     Filtered cards: {len(cc.filtered_cards)}")
                
                # Check why filtering might be failing
                if hasattr(cc, 'owned_only') and cc.owned_only:
                    print("     owned_only filter is active")
                if hasattr(cc, 'rarity_filter') and cc.rarity_filter:
                    print(f"     rarity_filter is set to: {cc.rarity_filter}")
            else:
                print("   OK: Card displays created successfully")
        else:
            print("   ERROR: No card collection component found!")
        
        return True
        
    except Exception as e:
        print(f"   ERROR: deck builder test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("DECK BUILDER SIMPLE TEST")
    print("=" * 40)
    
    success = test_deck_builder()
    
    print("=" * 40)
    if success:
        print("Test completed - check results above")
    else:
        print("Test failed - see errors above")