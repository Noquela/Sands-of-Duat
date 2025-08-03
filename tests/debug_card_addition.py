#!/usr/bin/env python3
"""
Debug script to test card addition directly.
"""

import os
import sys
import pygame
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_card_addition():
    """Debug card addition issues."""
    try:
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))
        
        # Initialize theme system
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(1920, 1080)
        
        # Import required classes
        from sands_duat.core.cards import Deck, Card, CardType, CardRarity, CardEffect, EffectType, TargetType
        from sands_duat.ui.deck_builder import DeckView
        
        # Create a simple test card
        test_card = Card(
            name="Test Card",
            description="A test card for debugging",
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[CardEffect(
                effect_type=EffectType.DAMAGE,
                value=5,
                target=TargetType.ENEMY
            )]
        )
        
        print(f"Created test card: {test_card.name}")
        print(f"Card has copy method: {hasattr(test_card, 'copy')}")
        
        # Test direct deck operations
        test_deck = Deck(name="Test Deck", max_size=30)
        print(f"Created deck with max_size: {test_deck.max_size}")
        print(f"Initial deck size: {len(test_deck.cards)}")
        
        # Try direct deck addition
        direct_success = test_deck.add_card(test_card)
        print(f"Direct deck add_card result: {direct_success}")
        print(f"Deck size after direct add: {len(test_deck.cards)}")
        
        if direct_success:
            print(f"Card in deck: {test_deck.cards[0].name}")
        else:
            print("Direct deck addition failed!")
            return False
        
        # Test DeckView
        deck_view = DeckView(10, 10, 400, 300)
        deck_view.set_deck(test_deck)
        
        print(f"DeckView deck set, current size: {len(deck_view.deck.cards)}")
        
        # Test DeckView card addition
        test_card2 = Card(
            name="Test Card 2",
            description="Second test card",
            sand_cost=2,
            card_type=CardType.SKILL,
            rarity=CardRarity.COMMON,
            effects=[CardEffect(
                effect_type=EffectType.BLOCK,
                value=5,
                target=TargetType.SELF
            )]
        )
        
        print(f"\nTesting DeckView.add_card with: {test_card2.name}")
        deck_view_success = deck_view.add_card(test_card2)
        print(f"DeckView add_card result: {deck_view_success}")
        print(f"Deck size after DeckView add: {len(deck_view.deck.cards)}")
        
        if deck_view_success:
            print(f"Cards in deck: {[card.name for card in deck_view.deck.cards]}")
        
        # Test accept_dropped_card
        test_card3 = Card(
            name="Test Card 3",
            description="Third test card",
            sand_cost=3,
            card_type=CardType.POWER,
            rarity=CardRarity.UNCOMMON,
            effects=[CardEffect(
                effect_type=EffectType.DAMAGE,
                value=8,
                target=TargetType.ENEMY
            )]
        )
        
        print(f"\nTesting DeckView.accept_dropped_card with: {test_card3.name}")
        accept_success = deck_view.accept_dropped_card(test_card3)
        print(f"DeckView accept_dropped_card result: {accept_success}")
        print(f"Final deck size: {len(deck_view.deck.cards)}")
        
        if accept_success:
            print(f"Final cards in deck: {[card.name for card in deck_view.deck.cards]}")
        
        return True
        
    except Exception as e:
        print(f"Debug failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("CARD ADDITION DEBUG TEST")
    print("=" * 60)
    
    success = debug_card_addition()
    
    print("=" * 60)
    if success:
        print("DEBUG COMPLETED")
    else:
        print("DEBUG FAILED")
    print("=" * 60)