#!/usr/bin/env python3
"""
Debug the complete event chain from card click to deck addition.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_complete_chain():
    """Debug the complete chain with detailed logging."""
    print("Debugging complete event chain...")
    
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
        
        print("Initial state:")
        print(f"   Deck size: {len(deck_builder.current_deck.cards)}")
        
        # Monkey patch all the methods to add detailed logging
        
        # 1. Patch CardCollection._on_card_selected
        original_cc_method = deck_builder.card_collection._on_card_selected
        def logged_cc_method(component, event_data):
            print(f"   [CardCollection._on_card_selected] Called with: {event_data}")
            result = original_cc_method(component, event_data)
            print(f"   [CardCollection._on_card_selected] Completed")
            return result
        deck_builder.card_collection._on_card_selected = logged_cc_method
        
        # 2. Patch DeckBuilderScreen._on_card_selected  
        original_screen_method = deck_builder._on_card_selected
        def logged_screen_method(component, event_data):
            print(f"   [DeckBuilderScreen._on_card_selected] Called with: {event_data}")
            print(f"   [DeckBuilderScreen._on_card_selected] Current deck size: {len(deck_builder.current_deck.cards)}")
            result = original_screen_method(component, event_data)
            print(f"   [DeckBuilderScreen._on_card_selected] Deck size after: {len(deck_builder.current_deck.cards)}")
            return result
        deck_builder._on_card_selected = logged_screen_method
        
        # 3. Patch DeckView.add_card
        original_add_card = deck_builder.deck_view.add_card
        def logged_add_card(card):
            print(f"   [DeckView.add_card] Called with: {card.name}")
            print(f"   [DeckView.add_card] Deck before: {len(deck_builder.deck_view.deck.cards)} cards")
            result = original_add_card(card)
            print(f"   [DeckView.add_card] Result: {result}")
            print(f"   [DeckView.add_card] Deck after: {len(deck_builder.deck_view.deck.cards)} cards")
            return result
        deck_builder.deck_view.add_card = logged_add_card
        
        # 4. Patch Deck.add_card
        original_deck_add = deck_builder.current_deck.add_card
        def logged_deck_add(card):
            print(f"   [Deck.add_card] Called with: {card.name}")
            print(f"   [Deck.add_card] Current size: {len(deck_builder.current_deck.cards)}")
            print(f"   [Deck.add_card] Max size: {deck_builder.current_deck.max_size}")
            result = original_deck_add(card)
            print(f"   [Deck.add_card] Result: {result}")
            return result
        deck_builder.current_deck.add_card = logged_deck_add
        
        print("\nTesting card click...")
        
        # Get first card and simulate click
        if deck_builder.card_collection.card_displays:
            first_card = deck_builder.card_collection.card_displays[0]
            card_center = first_card.rect.center
            
            print(f"Clicking on {first_card.card.name} at {card_center}")
            
            card_click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                'pos': card_center,
                'button': 1
            })
            
            handled = deck_builder.handle_event(card_click_event)
            print(f"Event handled: {handled}")
            
            print(f"\nFinal deck size: {len(deck_builder.current_deck.cards)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR in complete chain debug: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("COMPLETE CHAIN DEBUG")
    print("=" * 50)
    
    success = debug_complete_chain()
    
    print("=" * 50)
    if success:
        print("Complete chain debug finished")
    else:
        print("Complete chain debug failed")