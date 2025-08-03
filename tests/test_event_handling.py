#!/usr/bin/env python3
"""
Test event handling in deck builder to identify interaction issues.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_event_handling():
    """Test the event handling chain in deck builder."""
    print("Testing event handling chain...")
    
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.theme import initialize_theme
        
        # Create minimal setup
        screen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
        theme = initialize_theme(1920, 1080)
        deck_builder = DeckBuilderScreen()
        deck_builder.on_enter()
        
        print(f"Created deck builder with {len(deck_builder.components)} components")
        
        # Test 1: Check if components have proper event handling methods
        print("\n1. Checking component event handling capabilities...")
        for i, comp in enumerate(deck_builder.components):
            comp_type = type(comp).__name__
            has_handle_event = hasattr(comp, 'handle_event')
            has_event_handlers = hasattr(comp, 'event_handlers')
            
            print(f"   Component {i} ({comp_type}):")
            print(f"     - has handle_event: {has_handle_event}")
            print(f"     - has event_handlers: {has_event_handlers}")
            
            if has_event_handlers and hasattr(comp, 'event_handlers'):
                if comp.event_handlers:
                    print(f"     - registered handlers: {list(comp.event_handlers.keys())}")
                else:
                    print(f"     - no handlers registered")
        
        # Test 2: Check card collection event setup specifically
        print("\n2. Checking card collection event setup...")
        if deck_builder.card_collection:
            cc = deck_builder.card_collection
            print(f"   Card collection has {len(cc.card_displays)} card displays")
            
            # Check if card displays have proper event setup
            for i, card_display in enumerate(cc.card_displays[:3]):  # Check first 3
                print(f"   Card {i} ({card_display.card.name}):")
                print(f"     - rect: {card_display.rect}")
                print(f"     - visible: {card_display.visible}")
                print(f"     - enabled: {card_display.enabled}")
                print(f"     - has _trigger_event: {hasattr(card_display, '_trigger_event')}")
                
                # Check if card has event handlers
                if hasattr(card_display, 'event_handlers'):
                    if card_display.event_handlers:
                        print(f"     - handlers: {list(card_display.event_handlers.keys())}")
                    else:
                        print(f"     - no handlers registered")
        
        # Test 3: Simulate mouse events
        print("\n3. Testing simulated mouse events...")
        
        # Create test events
        test_positions = [
            (100, 100),  # Likely to hit back button
            (500, 300),  # Likely to hit card collection
            (800, 300),  # Likely to hit deck view
        ]
        
        for test_pos in test_positions:
            print(f"\n   Testing click at {test_pos}:")
            
            # Check which components this position would hit
            hit_components = []
            for i, comp in enumerate(deck_builder.components):
                if comp.rect.collidepoint(test_pos):
                    hit_components.append((i, comp))
            
            if hit_components:
                print(f"     Would hit {len(hit_components)} component(s):")
                for i, comp in hit_components:
                    print(f"       - Component {i}: {type(comp).__name__} at {comp.rect}")
            else:
                print(f"     Would not hit any components")
            
            # Test the event handling chain
            test_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': test_pos, 'button': 1})
            
            try:
                handled = deck_builder.handle_event(test_event)
                print(f"     Screen handled event: {handled}")
            except Exception as e:
                print(f"     ERROR handling event: {e}")
        
        # Test 4: Check card collection scrolling and interaction
        print("\n4. Testing card collection specific interactions...")
        if deck_builder.card_collection:
            cc = deck_builder.card_collection
            
            # Check scroll bounds
            print(f"   Scroll offset: {cc.scroll_offset}")
            print(f"   Max scroll: {cc.max_scroll}")
            print(f"   Collection rect: {cc.rect}")
            
            # Test if cards are positioned correctly
            if cc.card_displays:
                first_card = cc.card_displays[0]
                last_card = cc.card_displays[-1]
                print(f"   First card rect: {first_card.rect}")
                print(f"   Last card rect: {last_card.rect}")
                
                # Check if any cards are within the collection view
                visible_cards = []
                for i, card_display in enumerate(cc.card_displays):
                    if cc._is_card_visible(card_display):
                        visible_cards.append(i)
                
                print(f"   Visible cards: {len(visible_cards)} out of {len(cc.card_displays)}")
                if len(visible_cards) == 0:
                    print("   WARNING: No cards are visible! This could be the issue.")
        
        # Test 5: Check if base UIComponent event handling works
        print("\n5. Testing base component event handling...")
        if deck_builder.components:
            test_comp = deck_builder.components[0]  # Test first component
            test_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (test_comp.rect.centerx, test_comp.rect.centery), 'button': 1})
            
            print(f"   Testing {type(test_comp).__name__} at center {test_comp.rect.center}")
            try:
                # Call the base handle_event method directly
                from sands_duat.ui.base import UIComponent
                base_handled = UIComponent.handle_event(test_comp, test_event)
                print(f"   Base UIComponent.handle_event returned: {base_handled}")
                
                # Call the component's own handle_event
                comp_handled = test_comp.handle_event(test_event)
                print(f"   Component handle_event returned: {comp_handled}")
                
            except Exception as e:
                print(f"   ERROR in component event handling: {e}")
                import traceback
                traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"ERROR in event handling test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("EVENT HANDLING TEST")
    print("=" * 50)
    
    success = test_event_handling()
    
    print("=" * 50)
    if success:
        print("Event handling test completed - check results above")
    else:
        print("Event handling test failed - see errors above")