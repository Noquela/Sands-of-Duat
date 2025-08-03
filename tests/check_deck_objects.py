#!/usr/bin/env python3
"""
Check if deck objects are the same.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_deck_objects():
    """Check if deck objects are properly linked."""
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
        
        print("Checking deck object references...")
        
        current_deck = deck_builder.current_deck
        deck_view_deck = deck_builder.deck_view.deck
        
        print(f"DeckBuilderScreen.current_deck: {id(current_deck)}")
        print(f"DeckView.deck: {id(deck_view_deck)}")
        print(f"Are they the same object: {current_deck is deck_view_deck}")
        
        print(f"\nCurrent deck details:")
        print(f"  Name: {current_deck.name}")
        print(f"  Cards: {len(current_deck.cards)}")
        print(f"  Max size: {current_deck.max_size}")
        
        print(f"\nDeck view deck details:")
        print(f"  Name: {deck_view_deck.name}")
        print(f"  Cards: {len(deck_view_deck.cards)}")
        print(f"  Max size: {deck_view_deck.max_size}")
        
        # Test adding to each one separately
        if deck_builder.available_cards:
            test_card = deck_builder.available_cards[0]
            
            print(f"\nTesting direct add to current_deck:")
            result1 = current_deck.add_card(test_card)
            print(f"  Result: {result1}")
            print(f"  Current deck size: {len(current_deck.cards)}")
            print(f"  DeckView deck size: {len(deck_view_deck.cards)}")
            
            print(f"\nTesting add via DeckView:")
            result2 = deck_builder.deck_view.add_card(test_card)
            print(f"  Result: {result2}")
            print(f"  Current deck size: {len(current_deck.cards)}")
            print(f"  DeckView deck size: {len(deck_view_deck.cards)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("DECK OBJECT CHECK")
    print("=" * 40)
    
    success = check_deck_objects()
    
    print("=" * 40)
    if success:
        print("Deck object check completed")
    else:
        print("Deck object check failed")