#!/usr/bin/env python3
"""
Debug card dragging functionality in the actual game environment.
"""

import sys
from pathlib import Path
import pygame

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_card_dragging_in_game():
    """Test card dragging in actual game context."""
    try:
        pygame.init()
        
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.ui.deck_builder import DeckBuilderScreen, CardDisplay
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.content.starter_cards import create_starter_cards
        from sands_duat.core.cards import Card, CardType, CardRarity
        
        print("[DEBUG] Testing card dragging in game environment...")
        
        # Initialize theme and cards
        theme = initialize_theme(3440, 1440)
        create_starter_cards()
        
        # Create surface and UI manager
        surface = pygame.display.set_mode((3440, 1440))
        ui_manager = UIManager(surface)
        
        # Create deck builder screen
        deck_builder = DeckBuilderScreen()
        ui_manager.add_screen(deck_builder)
        deck_builder.activate()
        
        print(f"[INFO] Deck builder activated")
        
        # Check card collection exists and has cards
        if hasattr(deck_builder, 'card_collection') and deck_builder.card_collection:
            collection = deck_builder.card_collection
            print(f"[INFO] Card collection exists with {len(collection.card_displays)} cards")
            
            # Test first card if available
            if collection.card_displays:
                first_card = collection.card_displays[0]
                print(f"[INFO] First card: {first_card.card.name}")
                print(f"[INFO] Position: ({first_card.rect.x}, {first_card.rect.y})")
                print(f"[INFO] Draggable: {first_card.draggable}")
                print(f"[INFO] Being dragged: {first_card.being_dragged}")
                
                # Test event handling capability
                has_handle_event = hasattr(first_card, 'handle_event')
                print(f"[INFO] Has handle_event: {has_handle_event}")
                
                # Test event handlers
                has_event_handlers = hasattr(first_card, 'event_handlers')
                print(f"[INFO] Has event_handlers: {has_event_handlers}")
                
                if has_event_handlers:
                    print(f"[INFO] Event handlers: {list(first_card.event_handlers.keys())}")
                
                # Simulate a mouse click on the card
                click_pos = (first_card.rect.centerx, first_card.rect.centery)
                mouse_down_event = pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, 
                    pos=click_pos, 
                    button=1
                )
                
                print(f"[DEBUG] Simulating mouse down at {click_pos}")
                handled = first_card.handle_event(mouse_down_event)
                print(f"[INFO] Mouse down handled: {handled}")
                print(f"[INFO] Card being dragged after click: {first_card.being_dragged}")
                
                # Check if card collection is handling events
                collection_handled = collection.handle_event(mouse_down_event)
                print(f"[INFO] Collection handled event: {collection_handled}")
                
                # Check if deck builder is handling events
                deck_builder_handled = deck_builder.handle_event(mouse_down_event)
                print(f"[INFO] Deck builder handled event: {deck_builder_handled}")
                
        # Check deck view
        if hasattr(deck_builder, 'deck_view') and deck_builder.deck_view:
            deck_view = deck_builder.deck_view
            print(f"[INFO] Deck view exists at ({deck_view.rect.x}, {deck_view.rect.y})")
            
            # Test drop zone
            center_pos = (deck_view.rect.centerx, deck_view.rect.centery)
            is_valid_drop = deck_view.is_valid_drop_zone(center_pos)
            print(f"[INFO] Deck center is valid drop zone: {is_valid_drop}")
        
        # Test a simple card creation and drag
        print("\n[DEBUG] Testing standalone card drag...")
        test_card = Card(
            id="test_drag",
            name="Test Drag Card",
            description="Testing dragging",
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[]
        )
        
        standalone_card = CardDisplay(500, 300, 100, 140, test_card, draggable=True)
        print(f"[INFO] Standalone card draggable: {standalone_card.draggable}")
        
        # Test click on standalone card
        standalone_click = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            pos=(standalone_card.rect.centerx, standalone_card.rect.centery),
            button=1
        )
        
        standalone_handled = standalone_card.handle_event(standalone_click)
        print(f"[INFO] Standalone card handled click: {standalone_handled}")
        print(f"[INFO] Standalone card being dragged: {standalone_card.being_dragged}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Drag debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_event_propagation():
    """Test how events flow through the UI hierarchy."""
    try:
        print("\n[DEBUG] Testing event propagation...")
        
        import pygame
        pygame.init()
        
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.content.starter_cards import create_starter_cards
        
        # Initialize
        theme = initialize_theme(3440, 1440)
        create_starter_cards()
        surface = pygame.display.set_mode((800, 600))  # Smaller window for testing
        ui_manager = UIManager(surface)
        
        deck_builder = DeckBuilderScreen()
        ui_manager.add_screen(deck_builder)
        deck_builder.activate()
        
        # Create a test event
        test_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            pos=(400, 300),  # Center of screen
            button=1
        )
        
        print(f"[INFO] Test event: {test_event}")
        
        # Test event handling at different levels
        print("\n[DEBUG] Testing UI Manager event handling...")
        ui_handled = ui_manager.handle_event(test_event)
        print(f"[INFO] UI Manager handled event: {ui_handled}")
        
        print("\n[DEBUG] Testing Deck Builder event handling...")
        deck_handled = deck_builder.handle_event(test_event)
        print(f"[INFO] Deck Builder handled event: {deck_handled}")
        
        # Check if card collection gets the event
        if hasattr(deck_builder, 'card_collection') and deck_builder.card_collection:
            print("\n[DEBUG] Testing Card Collection event handling...")
            collection_handled = deck_builder.card_collection.handle_event(test_event)
            print(f"[INFO] Card Collection handled event: {collection_handled}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Event propagation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Debugging Card Dragging Functionality")
    print("=" * 50)
    
    test1_success = test_card_dragging_in_game()
    test2_success = test_event_propagation()
    
    print("=" * 50)
    if test1_success and test2_success:
        print("[SUCCESS] Debug tests completed")
    else:
        print("[FAIL] Some debug tests failed")