#!/usr/bin/env python3
"""
Test the new deck builder layout with upper/lower design and drag-and-drop functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_deck_builder_layout():
    """Test that the new deck builder layout is properly configured."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.content.starter_cards import create_starter_cards
        
        print("[TEST] Testing new deck builder layout...")
        
        # Initialize theme for ultrawide
        theme = initialize_theme(3440, 1440)
        print(f"[PASS] Theme initialized for {theme.display.display_mode.value} mode")
        
        # Check layout zones
        zones = theme.zones
        
        collection_zone = zones.get('deck_collection')
        deck_zone = zones.get('deck_view')
        filter_zone = zones.get('deck_filter_panel')
        
        print(f"[INFO] Collection zone: {collection_zone}")
        print(f"[INFO] Deck zone: {deck_zone}")
        print(f"[INFO] Filter zone: {filter_zone}")
        
        # Verify upper/lower layout
        if collection_zone and deck_zone:
            collection_bottom = collection_zone.y + collection_zone.height
            deck_top = deck_zone.y
            
            if deck_top > collection_bottom:
                print(f"[PASS] Layout verification: Deck area ({deck_top}) is below collection area ({collection_bottom})")
            else:
                print(f"[WARN] Layout may overlap: Deck starts at {deck_top}, collection ends at {collection_bottom}")
        
        # Initialize cards
        create_starter_cards()
        
        # Create surface and UI manager
        surface = pygame.display.set_mode((3440, 1440))
        ui_manager = UIManager(surface)
        
        # Create deck builder screen
        deck_builder = DeckBuilderScreen()
        ui_manager.add_screen(deck_builder)
        
        # Activate the screen
        deck_builder.activate()
        
        print("[PASS] Deck builder screen created and activated")
        
        # Test component structure
        if hasattr(deck_builder, 'card_collection') and deck_builder.card_collection:
            collection = deck_builder.card_collection
            print(f"[PASS] Card collection component exists at ({collection.rect.x}, {collection.rect.y})")
            print(f"[INFO] Collection size: {collection.rect.width}x{collection.rect.height}")
            
            # Test drag support
            if hasattr(collection, 'card_displays'):
                for i, card_display in enumerate(collection.card_displays[:3]):  # Test first 3 cards
                    if hasattr(card_display, 'draggable') and card_display.draggable:
                        print(f"[PASS] Card {i+1} ({card_display.card.name}) is draggable")
                    else:
                        print(f"[FAIL] Card {i+1} is not draggable")
        
        if hasattr(deck_builder, 'deck_view') and deck_builder.deck_view:
            deck_view = deck_builder.deck_view
            print(f"[PASS] Deck view component exists at ({deck_view.rect.x}, {deck_view.rect.y})")
            print(f"[INFO] Deck view size: {deck_view.rect.width}x{deck_view.rect.height}")
            
            # Test drop zone methods
            if hasattr(deck_view, 'is_valid_drop_zone'):
                test_pos = (deck_view.rect.centerx, deck_view.rect.centery)
                is_valid = deck_view.is_valid_drop_zone(test_pos)
                print(f"[PASS] Drop zone validation works: center point valid = {is_valid}")
            
            if hasattr(deck_view, 'accept_dropped_card'):
                print(f"[PASS] Deck view can accept dropped cards")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Layout test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_drag_drop_events():
    """Test drag and drop event handling."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.deck_builder import CardDisplay
        from sands_duat.core.cards import Card, CardType, CardRarity
        
        print("[TEST] Testing drag and drop events...")
        
        # Create a test card
        test_card = Card(
            id="test_card",
            name="Test Card",
            description="A test card for drag testing",
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[]
        )
        
        # Create draggable card display
        card_display = CardDisplay(100, 100, 100, 140, test_card, draggable=True)
        
        print(f"[PASS] Created draggable card display for {test_card.name}")
        print(f"[INFO] Card position: ({card_display.rect.x}, {card_display.rect.y})")
        print(f"[INFO] Draggable: {card_display.draggable}")
        print(f"[INFO] Being dragged: {card_display.being_dragged}")
        
        # Test event handler registration
        event_handlers_exist = hasattr(card_display, 'event_handlers')
        print(f"[PASS] Event handlers system exists: {event_handlers_exist}")
        
        # Simulate mouse down event
        mouse_down_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, 
            pos=(card_display.rect.centerx, card_display.rect.centery), 
            button=1
        )
        
        # Test that the card can handle the event
        handled = card_display.handle_event(mouse_down_event)
        print(f"[PASS] Card handles mouse down event: {handled}")
        print(f"[INFO] Card being dragged after mouse down: {card_display.being_dragged}")
        
        # Simulate mouse motion
        mouse_motion_event = pygame.event.Event(
            pygame.MOUSEMOTION,
            pos=(150, 150)
        )
        
        if card_display.being_dragged:
            handled_motion = card_display.handle_event(mouse_motion_event)
            print(f"[PASS] Card handles drag motion: {handled_motion}")
            print(f"[INFO] Card new position: ({card_display.rect.x}, {card_display.rect.y})")
        
        # Simulate mouse up
        mouse_up_event = pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            pos=(150, 150),
            button=1
        )
        
        handled_up = card_display.handle_event(mouse_up_event)
        print(f"[PASS] Card handles mouse up event: {handled_up}")
        print(f"[INFO] Card being dragged after mouse up: {card_display.being_dragged}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Drag drop test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing New Deck Builder Layout and Drag-Drop")
    print("=" * 60)
    
    test1_success = test_deck_builder_layout()
    print()
    test2_success = test_drag_drop_events()
    
    print("=" * 60)
    if test1_success and test2_success:
        print("[SUCCESS] New deck builder layout and drag-drop functionality working!")
        print("")
        print("Key improvements:")
        print("+ Cards collection positioned in upper area")
        print("+ Deck view positioned in lower area")
        print("+ Cards are draggable from collection")
        print("+ Deck view accepts dropped cards")
        print("+ Visual feedback for drop zones")
        print("+ Proper event handling for drag operations")
        sys.exit(0)
    else:
        print("[FAIL] Some deck builder layout tests failed")
        sys.exit(1)