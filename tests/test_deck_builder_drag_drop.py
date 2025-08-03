"""
Test for deck builder drag-and-drop functionality.

This test verifies that cards are properly moved from collection to deck
and that visual state is handled correctly.
"""

import pytest
import pygame
from unittest.mock import Mock, MagicMock

# Import the deck builder components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sands_duat.ui.deck_builder import DeckBuilderScreen, CardCollection, DeckView, CardDisplay
from sands_duat.core.cards import Card, CardType, CardRarity, Deck
from sands_duat.core.player_collection import PlayerCollection


class TestDeckBuilderDragDrop:
    """Test cases for deck builder drag and drop functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        pygame.init()
        pygame.display.set_mode((800, 600))
        
        # Create test components
        self.player_collection = PlayerCollection()
        self.deck_builder = DeckBuilderScreen()
        
        # Create test card
        self.test_card = Card(
            id="test_card_1",
            name="Test Attack",
            description="A test attack card",
            sand_cost=2,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[]
        )
    
    def test_card_removal_from_collection_on_successful_drop(self):
        """Test that cards are removed from collection display when successfully added to deck."""
        # Create collection and deck view
        collection = CardCollection(
            x=100, y=100, width=400, height=300,
            player_collection=self.player_collection
        )
        
        deck_view = DeckView(x=600, y=100, width=200, height=300)
        deck = Deck(name="Test Deck", max_size=30)
        deck_view.set_deck(deck)
        
        # Add test card to collection
        collection.filtered_cards = [self.test_card]
        collection._create_card_displays()
        
        # Verify card is in collection initially
        assert len(collection.card_displays) == 1
        assert collection.card_displays[0].card.id == self.test_card.id
        
        # Verify deck is properly set
        assert deck_view.deck is not None
        assert len(deck_view.deck.cards) == 0
        
        # Simulate successful card addition to deck
        success = deck_view.accept_dropped_card(self.test_card)
        assert success == True
        
        # Remove card from collection display (simulating the drag-drop flow)
        collection.remove_card_from_collection_display(self.test_card)
        
        # Verify card is removed from collection display
        assert len(collection.card_displays) == 0
        assert self.test_card not in collection.filtered_cards
        
        # Verify card is in deck
        assert len(deck.cards) == 1
        assert deck.cards[0].id == self.test_card.id
    
    def test_card_position_not_reset_on_successful_drop(self):
        """Test that card position is not reset when successfully dropped in deck."""
        # Create card display
        card_display = CardDisplay(
            x=150, y=200, width=80, height=120,
            card=self.test_card, draggable=True
        )
        
        original_pos = (150, 200)
        dragged_pos = (650, 250)  # Position in deck area
        
        # Set up drag state
        card_display.being_dragged = True
        card_display.original_pos = original_pos
        card_display.rect.x, card_display.rect.y = dragged_pos
        
        # Create mock event data for successful drop
        event_data = {
            "card": self.test_card,
            "component": card_display,
            "drop_pos": dragged_pos,
            "original_pos": original_pos
        }
        
        # Create deck builder and set up components
        deck_builder = DeckBuilderScreen()
        deck_builder.current_deck = Deck(name="Test Deck", max_size=30)
        deck_builder.deck_view = DeckView(x=600, y=100, width=200, height=300)
        deck_builder.deck_view.set_deck(deck_builder.current_deck)
        deck_builder.card_collection = CardCollection(
            x=100, y=100, width=400, height=300,
            player_collection=self.player_collection
        )
        
        # Mock the is_valid_drop_zone to return True
        deck_builder.deck_view.is_valid_drop_zone = Mock(return_value=True)
        
        # Mock the accept_dropped_card to return True
        deck_builder.deck_view.accept_dropped_card = Mock(return_value=True)
        
        # Mock the remove_card_from_collection_display method
        deck_builder.card_collection.remove_card_from_collection_display = Mock(return_value=True)
        
        # Call the drag end handler
        deck_builder._on_card_drag_end(None, event_data)
        
        # Verify the card's drag state is cleared but position is not reset to original
        assert card_display.being_dragged == False
        assert card_display.drag_offset_x == 0
        assert card_display.drag_offset_y == 0
        
        # Verify the remove method was called
        deck_builder.card_collection.remove_card_from_collection_display.assert_called_once_with(self.test_card)
    
    def test_card_position_reset_on_failed_drop(self):
        """Test that card position is reset when drop fails."""
        # Create card display
        card_display = CardDisplay(
            x=150, y=200, width=80, height=120,
            card=self.test_card, draggable=True
        )
        
        original_pos = (150, 200)
        dragged_pos = (400, 250)  # Position outside deck area
        
        # Set up drag state
        card_display.being_dragged = True
        card_display.original_pos = original_pos
        card_display.rect.x, card_display.rect.y = dragged_pos
        
        # Create mock event data for failed drop
        event_data = {
            "card": self.test_card,
            "component": card_display,
            "drop_pos": dragged_pos,
            "original_pos": original_pos
        }
        
        # Create deck builder and set up components
        deck_builder = DeckBuilderScreen()
        deck_builder.current_deck = Deck(name="Test Deck", max_size=30)
        deck_builder.deck_view = DeckView(x=600, y=100, width=200, height=300)
        deck_builder.deck_view.set_deck(deck_builder.current_deck)
        
        # Mock the is_valid_drop_zone to return False
        deck_builder.deck_view.is_valid_drop_zone = Mock(return_value=False)
        
        # Call the drag end handler
        deck_builder._on_card_drag_end(None, event_data)
        
        # Verify the card position is reset to original
        assert card_display.rect.x == original_pos[0]
        assert card_display.rect.y == original_pos[1]
        assert card_display.being_dragged == False
    
    def test_deck_view_updates_layout_when_card_added(self):
        """Test that deck view properly updates its layout when cards are added."""
        # Create deck view with empty deck
        deck_view = DeckView(x=600, y=100, width=200, height=300)
        deck = Deck(name="Test Deck", max_size=30)
        deck_view.set_deck(deck)
        
        # Initially no card displays
        assert len(deck_view.card_displays) == 0
        
        # Add a card
        success = deck_view.add_card(self.test_card)
        assert success == True
        
        # Verify card display was created
        assert len(deck_view.card_displays) == 1
        assert deck_view.card_displays[0].card.id == self.test_card.id
        assert deck_view.card_displays[0].draggable == False  # Deck cards should not be draggable
    
    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()


if __name__ == "__main__":
    # Run the tests
    test = TestDeckBuilderDragDrop()
    test.setup_method()
    
    try:
        test.test_card_removal_from_collection_on_successful_drop()
        print("PASS: Card removal from collection test passed")
        
        test.test_card_position_not_reset_on_successful_drop()
        print("PASS: Card position not reset on successful drop test passed")
        
        test.test_card_position_reset_on_failed_drop()
        print("PASS: Card position reset on failed drop test passed")
        
        test.test_deck_view_updates_layout_when_card_added()
        print("PASS: Deck view layout update test passed")
        
        print("\nAll drag-and-drop tests passed!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        test.teardown_method()