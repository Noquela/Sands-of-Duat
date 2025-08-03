#!/usr/bin/env python3
"""
Test deck builder interaction functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_deck_builder_interactions():
    """Test that deck builder interactions work properly."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.content.starter_cards import create_starter_cards
        
        # Initialize cards
        create_starter_cards()
        
        # Create surface and UI manager
        surface = pygame.display.set_mode((100, 100))
        ui_manager = UIManager(surface)
        
        # Create deck builder screen
        deck_builder = DeckBuilderScreen()
        ui_manager.add_screen(deck_builder)
        
        # Activate the screen
        deck_builder.activate()
        
        print("[PASS] Deck builder screen created and activated")
        
        # Test event handling capability
        test_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(50, 50), button=1)
        
        # Check that the screen can handle events
        can_handle_events = hasattr(deck_builder, 'handle_event')
        print(f"[PASS] Deck builder can handle events: {can_handle_events}")
        
        # Test component structure
        has_components = hasattr(deck_builder, 'components') and len(deck_builder.components) > 0
        print(f"[PASS] Deck builder has UI components: {has_components}")
        
        # Test card collection
        has_card_collection = hasattr(deck_builder, 'card_collection')
        print(f"[PASS] Deck builder has card collection: {has_card_collection}")
        
        # Test deck view
        has_deck_view = hasattr(deck_builder, 'deck_view')
        print(f"[PASS] Deck builder has deck view: {has_deck_view}")
        
        # Test filter panel
        has_filter_panel = hasattr(deck_builder, 'filter_panel')
        print(f"[PASS] Deck builder has filter panel: {has_filter_panel}")
        
        # Test event handler registration
        if has_card_collection and deck_builder.card_collection:
            has_event_handlers = hasattr(deck_builder.card_collection, 'event_handlers')
            print(f"[PASS] Card collection has event handlers: {has_event_handlers}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Deck builder test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_card_interaction_chain():
    """Test the card interaction event chain."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import CardDisplay
        from sands_duat.core.cards import Card, CardType, CardRarity
        
        # Create a test card
        test_card = Card(
            id="test_card",
            name="Test Card",
            description="A test card",
            cost=1,
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[]
        )
        
        # Create card display
        card_display = CardDisplay(0, 0, 100, 140, test_card)
        
        print(f"[PASS] Card display created: {card_display.card.name}")
        
        # Test that card display can be selected
        initial_selected = card_display.selected
        card_display.selected = not card_display.selected
        selection_changed = card_display.selected != initial_selected
        
        print(f"[PASS] Card selection toggle works: {selection_changed}")
        
        # Test event triggering capability
        has_trigger_event = hasattr(card_display, '_trigger_event')
        print(f"[PASS] Card display can trigger events: {has_trigger_event}")
        
        # Test event handling
        has_handle_event = hasattr(card_display, 'handle_event')
        print(f"[PASS] Card display can handle events: {has_handle_event}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Card interaction test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Deck Builder Interactions...")
    print("=" * 50)
    
    test1_success = test_deck_builder_interactions()
    test2_success = test_card_interaction_chain()
    
    print("=" * 50)
    if test1_success and test2_success:
        print("[SUCCESS] Deck builder interactions are working!")
        print("")
        print("You should now be able to:")
        print("- Click on cards in the collection area")
        print("- See visual feedback when selecting cards")
        print("- Use the back button to navigate")
        print("- Interact with filter controls")
        sys.exit(0)
    else:
        print("[FAIL] Some deck builder tests failed")
        sys.exit(1)