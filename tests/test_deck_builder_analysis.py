#!/usr/bin/env python3
"""
Analyze deck builder without GUI to identify specific issues.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def analyze_deck_builder_code():
    """Analyze deck builder code structure for potential issues."""
    print("1. Testing imports...")
    
    try:
        import pygame
        pygame.init()
        print("   ✓ pygame import successful")
    except Exception as e:
        print(f"   ✗ pygame import failed: {e}")
        return False
    
    try:
        from sands_duat.ui.deck_builder import DeckBuilderScreen, CardDisplay, CardCollection, DeckView
        print("   ✓ deck builder imports successful")
    except Exception as e:
        print(f"   ✗ deck builder import failed: {e}")
        return False
    
    try:
        from sands_duat.ui.theme import initialize_theme, get_theme
        print("   ✓ theme system imports successful")
    except Exception as e:
        print(f"   ✗ theme system import failed: {e}")
        return False
    
    try:
        from sands_duat.core.player_collection import PlayerCollection
        print("   ✓ player collection import successful")
    except Exception as e:
        print(f"   ✗ player collection import failed: {e}")
        return False
    
    print("\n2. Testing theme initialization...")
    try:
        theme = initialize_theme(1920, 1080)
        print(f"   ✓ theme initialized: {theme.display.display_mode.value}")
        
        # Check if required zones exist
        required_zones = ['deck_back_button', 'deck_filter_panel', 'deck_collection', 'deck_view']
        for zone_name in required_zones:
            try:
                zone = theme.get_zone(zone_name)
                print(f"   ✓ zone '{zone_name}': {zone.x}, {zone.y}, {zone.width}x{zone.height}")
            except Exception as e:
                print(f"   ✗ zone '{zone_name}' missing or invalid: {e}")
                
    except Exception as e:
        print(f"   ✗ theme initialization failed: {e}")
        return False
    
    print("\n3. Testing deck builder instantiation...")
    try:
        screen = pygame.display.set_mode((100, 100))  # Minimal surface
        deck_builder = DeckBuilderScreen()
        print("   ✓ deck builder created successfully")
        
        print("\n4. Testing component setup...")
        deck_builder.on_enter()
        print(f"   ✓ deck builder entered, components: {len(deck_builder.components)}")
        
        # Analyze components
        for i, comp in enumerate(deck_builder.components):
            comp_type = type(comp).__name__
            visible = comp.visible
            enabled = comp.enabled
            rect = comp.rect
            print(f"     Component {i}: {comp_type} - visible:{visible}, enabled:{enabled}, rect:{rect}")
            
            # Check for specific issues
            if hasattr(comp, 'callback') and comp.callback is None:
                print(f"       ⚠ Component {i} has no callback set")
            
            if rect.width <= 0 or rect.height <= 0:
                print(f"       ✗ Component {i} has invalid size: {rect.width}x{rect.height}")
            
            if not visible:
                print(f"       ⚠ Component {i} is not visible")
            
            if not enabled:
                print(f"       ⚠ Component {i} is not enabled")
        
        print("\n5. Testing event handling setup...")
        # Create a test click event
        test_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (100, 100), 'button': 1})
        
        for i, comp in enumerate(deck_builder.components):
            if comp.rect.collidepoint((100, 100)):
                print(f"   Component {i} ({type(comp).__name__}) would receive click at (100, 100)")
                
                # Test if component has proper event handling
                if hasattr(comp, 'handle_event'):
                    print(f"     ✓ has handle_event method")
                else:
                    print(f"     ✗ missing handle_event method")
                
                # Check if component has event handlers registered
                if hasattr(comp, 'event_handlers'):
                    if comp.event_handlers:
                        print(f"     ✓ has event handlers: {list(comp.event_handlers.keys())}")
                    else:
                        print(f"     ⚠ no event handlers registered")
                else:
                    print(f"     ✗ no event_handlers attribute")
        
        print("\n6. Testing card collection specifics...")
        if deck_builder.card_collection:
            card_collection = deck_builder.card_collection
            print(f"   Card collection: {len(card_collection.filtered_cards)} filtered cards")
            print(f"   Card displays: {len(card_collection.card_displays)} display components")
            
            if len(card_collection.card_displays) == 0:
                print("   ✗ No card displays created - this is likely the main issue!")
                
                # Check why no card displays
                print(f"   Player collection cards: {len(card_collection.filtered_cards)}")
                if len(card_collection.filtered_cards) == 0:
                    print("   ✗ No filtered cards available")
                    print(f"   All cards in player collection: {len(card_collection.player_collection.owned_cards)}")
                    
            else:
                print("   ✓ Card displays created successfully")
                
                # Test first card display
                first_card = card_collection.card_displays[0]
                print(f"   First card: {first_card.card.name} at {first_card.rect}")
                
                # Check if card display has event handling
                if hasattr(first_card, '_trigger_event'):
                    print("   ✓ Card displays have event triggering capability")
                else:
                    print("   ✗ Card displays missing event triggering")
        
        return True
        
    except Exception as e:
        print(f"   ✗ deck builder setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("=" * 70)
    print("DECK BUILDER CODE ANALYSIS")
    print("=" * 70)
    
    success = analyze_deck_builder_code()
    
    print("=" * 70)
    if success:
        print("✓ Analysis completed - check specific issues above")
    else:
        print("✗ Analysis failed - see errors above")