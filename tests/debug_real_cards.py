#!/usr/bin/env python3
"""
Debug the real cards being used in deck builder.
"""

import os
import sys
import pygame
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_real_cards():
    """Debug the actual cards in the deck builder."""
    try:
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))
        
        # Initialize theme system
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(1920, 1080)
        
        # Create deck builder screen
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        deck_builder = DeckBuilderScreen()
        deck_builder.on_enter()
        
        # Find card collection component
        card_collection = None
        deck_view = None
        
        for component in deck_builder.components:
            if hasattr(component, 'card_displays') and hasattr(component, 'filtered_cards'):
                card_collection = component
            elif hasattr(component, 'deck') and hasattr(component, 'accept_dropped_card'):
                deck_view = component
        
        if not card_collection:
            print("Could not find CardCollection")
            return False
        
        if not deck_view:
            print("Could not find DeckView")
            return False
        
        print(f"Found {len(card_collection.filtered_cards)} cards in collection")
        
        if card_collection.filtered_cards:
            test_card = card_collection.filtered_cards[0]
            print(f"First card: {test_card.name}")
            print(f"Card type: {type(test_card)}")
            print(f"Card has id: {hasattr(test_card, 'id')}")
            print(f"Card has copy: {hasattr(test_card, 'copy')}")
            print(f"Card attributes: {list(test_card.__dict__.keys()) if hasattr(test_card, '__dict__') else 'No dict'}")
            
            # Try to copy the card
            try:
                if hasattr(test_card, 'copy'):
                    copied_card = test_card.copy(deep=True)
                    print(f"Successfully copied card: {copied_card.name}")
                else:
                    copied_card = test_card
                    print("No copy method, using original card")
                
                # Test deck addition
                print(f"\nTesting deck addition...")
                print(f"Deck before: {len(deck_view.deck.cards)} cards")
                print(f"Deck max_size: {deck_view.deck.max_size}")
                
                success = deck_view.deck.add_card(copied_card)
                print(f"Direct deck.add_card result: {success}")
                print(f"Deck after direct add: {len(deck_view.deck.cards)} cards")
                
                # Test DeckView.add_card
                if len(card_collection.filtered_cards) > 1:
                    test_card2 = card_collection.filtered_cards[1]
                    print(f"\nTesting DeckView.add_card with: {test_card2.name}")
                    success2 = deck_view.add_card(test_card2)
                    print(f"DeckView.add_card result: {success2}")
                    print(f"Deck after DeckView add: {len(deck_view.deck.cards)} cards")
                
            except Exception as e:
                print(f"Error during card operations: {e}")
                import traceback
                traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("REAL CARDS DEBUG TEST")
    print("=" * 60)
    
    success = debug_real_cards()
    
    print("=" * 60)
    if success:
        print("DEBUG COMPLETED")
    else:
        print("DEBUG FAILED")
    print("=" * 60)