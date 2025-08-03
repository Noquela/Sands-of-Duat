#!/usr/bin/env python3
"""
Debug deck size limits and initialization.
"""

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def debug_deck_limits():
    """Debug deck initialization and size limits."""
    print("Debugging deck limits...")
    
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.core.cards import Deck
        
        # Create setup
        screen = pygame.display.set_mode((100, 100), pygame.NOFRAME)
        theme = initialize_theme(1920, 1080)
        deck_builder = DeckBuilderScreen()
        deck_builder.activate()
        
        print("Step 1: Checking deck initialization")
        print(f"   Current deck: {deck_builder.current_deck}")
        if deck_builder.current_deck:
            print(f"   Deck name: {deck_builder.current_deck.name}")
            print(f"   Deck cards: {len(deck_builder.current_deck.cards)}")
            print(f"   Deck max_size: {deck_builder.current_deck.max_size}")
            print(f"   Deck min_size: {deck_builder.current_deck.min_size}")
        
        print("\nStep 2: Checking deck view")
        if deck_builder.deck_view:
            print(f"   Deck view deck: {deck_builder.deck_view.deck}")
            if deck_builder.deck_view.deck:
                dv_deck = deck_builder.deck_view.deck
                print(f"   DeckView deck name: {dv_deck.name}")
                print(f"   DeckView deck cards: {len(dv_deck.cards)}")
                print(f"   DeckView deck max_size: {dv_deck.max_size}")
                print(f"   DeckView deck min_size: {dv_deck.min_size}")
        
        print("\nStep 3: Testing manual deck creation")
        test_deck = Deck(name="Test Deck")
        print(f"   New deck max_size: {test_deck.max_size}")
        print(f"   New deck cards: {len(test_deck.cards)}")
        
        # Test adding to new deck
        if deck_builder.available_cards:
            test_card = deck_builder.available_cards[0]
            print(f"   Testing add of {test_card.name} to new deck")
            added = test_deck.add_card(test_card)
            print(f"   Add successful: {added}")
            print(f"   New deck size: {len(test_deck.cards)}")
        
        print("\nStep 4: Checking DeckView.add_card logic")
        if deck_builder.deck_view and deck_builder.available_cards:
            test_card = deck_builder.available_cards[0]
            print(f"   Testing DeckView.add_card with {test_card.name}")
            
            # Check the conditions manually
            has_deck = deck_builder.deck_view.deck is not None
            deck_size = len(deck_builder.deck_view.deck.cards) if has_deck else "N/A"
            size_under_30 = deck_size < 30 if has_deck else False
            
            print(f"   Has deck: {has_deck}")
            print(f"   Deck size: {deck_size}")
            print(f"   Size under 30: {size_under_30}")
            
            if has_deck:
                print(f"   Deck max_size: {deck_builder.deck_view.deck.max_size}")
                
                # Test the deck.add_card directly
                deck_add_result = deck_builder.deck_view.deck.add_card(test_card)
                print(f"   Direct deck.add_card result: {deck_add_result}")
                print(f"   Deck size after direct add: {len(deck_builder.deck_view.deck.cards)}")
                
                # Now test the DeckView.add_card
                dv_add_result = deck_builder.deck_view.add_card(test_card)
                print(f"   DeckView.add_card result: {dv_add_result}")
                print(f"   Deck size after DeckView add: {len(deck_builder.deck_view.deck.cards)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR in deck limits debug: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("DECK LIMITS DEBUG")
    print("=" * 40)
    
    success = debug_deck_limits()
    
    print("=" * 40)
    if success:
        print("Deck limits debug completed")
    else:
        print("Deck limits debug failed")