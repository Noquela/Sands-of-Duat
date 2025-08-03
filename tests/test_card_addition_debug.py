#!/usr/bin/env python3
"""
Debug card addition to deck functionality.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_card_addition_chain():
    """Test the complete card addition chain from click to deck."""
    print("Testing card addition chain...")
    
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.theme import initialize_theme
        
        # Create setup
        screen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
        theme = initialize_theme(1920, 1080)
        deck_builder = DeckBuilderScreen()
        deck_builder.activate()
        
        print("Step 1: Initial state")
        print(f"   Deck has {len(deck_builder.current_deck.cards)} cards")
        print(f"   Card collection has {len(deck_builder.card_collection.card_displays)} card displays")
        
        # Get the first card display
        if deck_builder.card_collection.card_displays:
            first_card = deck_builder.card_collection.card_displays[0]
            print(f"   First card: {first_card.card.name}")
            
            # Monkey patch the _on_card_selected method to add logging
            original_method = deck_builder._on_card_selected
            def logged_on_card_selected(component, event_data):
                print(f"   _on_card_selected called with data: {event_data}")
                result = original_method(component, event_data)
                print(f"   After _on_card_selected, deck has {len(deck_builder.current_deck.cards)} cards")
                return result
            deck_builder._on_card_selected = logged_on_card_selected
            
            # Monkey patch the CardCollection._on_card_selected to add logging
            original_cc_method = deck_builder.card_collection._on_card_selected  
            def logged_cc_on_card_selected(component, event_data):
                print(f"   CardCollection._on_card_selected called with: {event_data}")
                result = original_cc_method(component, event_data)
                print(f"   CardCollection triggered parent event")
                return result
            deck_builder.card_collection._on_card_selected = logged_cc_on_card_selected
            
            # Monkey patch the CardDisplay._trigger_event to add logging
            original_trigger = first_card._trigger_event
            def logged_trigger_event(event_type, event_data):
                print(f"   CardDisplay triggering event '{event_type}' with data: {event_data}")
                return original_trigger(event_type, event_data)
            first_card._trigger_event = logged_trigger_event
            
            print("\nStep 2: Simulating card click")
            card_center = first_card.rect.center
            card_click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                'pos': card_center,
                'button': 1
            })
            
            print(f"   Clicking card at {card_center}")
            print(f"   Card selected before: {first_card.selected}")
            
            # Handle the event
            handled = deck_builder.handle_event(card_click_event)
            print(f"   Event handled: {handled}")
            print(f"   Card selected after: {first_card.selected}")
            
            print("\nStep 3: Checking event handler chain")
            
            # Check if CardCollection has handlers for the right event
            cc_handlers = deck_builder.card_collection.event_handlers
            print(f"   CardCollection handlers: {list(cc_handlers.keys())}")
            
            if "card_selection_changed" in cc_handlers:
                handlers = cc_handlers["card_selection_changed"]
                print(f"   Number of card_selection_changed handlers: {len(handlers)}")
                for i, handler in enumerate(handlers):
                    print(f"     Handler {i}: {handler}")
            
            # Manually test the event chain
            print("\nStep 4: Manual event chain test")
            print("   Manually calling CardDisplay._trigger_event...")
            first_card._trigger_event("card_selected", {
                "card": first_card.card, 
                "selected": True
            })
            
            # Check if deck view can add cards
            print("\nStep 5: Testing deck view directly")
            if deck_builder.deck_view and deck_builder.available_cards:
                test_card = deck_builder.available_cards[0]
                print(f"   Testing direct add of {test_card.name}")
                added = deck_builder.deck_view.add_card(test_card)
                print(f"   Direct add successful: {added}")
                print(f"   Deck size after direct add: {len(deck_builder.current_deck.cards)}")
                
        return True
        
    except Exception as e:
        print(f"ERROR in card addition test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("CARD ADDITION CHAIN DEBUG")
    print("=" * 50)
    
    success = test_card_addition_chain()
    
    print("=" * 50)
    if success:
        print("Card addition test completed")
    else:
        print("Card addition test failed")