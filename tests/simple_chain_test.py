#!/usr/bin/env python3
"""
Simple test of the event chain without monkey patching.
"""

import sys
from pathlib import Path
import logging

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def simple_chain_test():
    """Simple test of event chain."""
    
    # Enable debug logging to see all events
    logging.basicConfig(level=logging.DEBUG)
    
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
        
        print(f"Initial deck size: {len(deck_builder.current_deck.cards)}")
        
        # Test manual card addition first
        if deck_builder.available_cards:
            test_card = deck_builder.available_cards[0]
            print(f"Testing manual add of {test_card.name}")
            
            # Test DeckView.add_card directly
            success = deck_builder.deck_view.add_card(test_card)
            print(f"Manual add result: {success}")
            print(f"Deck size after manual add: {len(deck_builder.current_deck.cards)}")
            
            # Reset deck
            deck_builder.current_deck.cards.clear()
            print("Reset deck to 0 cards")
            
            # Test via click simulation
            print("\nTesting via click simulation...")
            if deck_builder.card_collection.card_displays:
                first_card_display = deck_builder.card_collection.card_displays[0]
                card_center = first_card_display.rect.center
                
                print(f"Clicking on {first_card_display.card.name} at {card_center}")
                
                card_click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
                    'pos': card_center,
                    'button': 1
                })
                
                handled = deck_builder.handle_event(card_click_event)
                print(f"Event handled: {handled}")
                print(f"Card selected: {first_card_display.selected}")
                print(f"Final deck size: {len(deck_builder.current_deck.cards)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("SIMPLE CHAIN TEST")
    print("=" * 40)
    
    success = simple_chain_test()
    
    print("=" * 40)
    if success:
        print("Simple chain test completed")
    else:
        print("Simple chain test failed")