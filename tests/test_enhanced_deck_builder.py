"""
Test for Enhanced Deck Builder with CrewAI Improvements

Tests the new features:
1. Collapsible filter panel with Egyptian styling
2. Egyptian-themed animations (Ankh, Scarab, Lotus)
3. Sandstone color hierarchy
4. Lazy loading performance optimizations
5. Accessibility features
"""

import pygame
import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sands_duat.ui.deck_builder import DeckBuilderScreen, FilterPanel, CardDisplay
from sands_duat.ui.theme import initialize_theme, get_sandstone_color
from sands_duat.ui.animation_system import AnimationManager, EgyptianAnimationRenderer
from sands_duat.core.cards import Card, CardRarity, CardType, CardEffect, EffectType, TargetType
from sands_duat.core.player_collection import PlayerCollection


class TestEnhancedDeckBuilder:
    """Test the enhanced deck builder functionality."""
    
    @classmethod
    def setup_class(cls):
        """Set up pygame and theme for testing."""
        pygame.init()
        cls.screen = pygame.display.set_mode((3440, 1440))  # Ultrawide test
        cls.theme = initialize_theme(3440, 1440)
    
    @classmethod
    def teardown_class(cls):
        """Clean up pygame."""
        pygame.quit()
    
    def test_sandstone_color_hierarchy(self):
        """Test that sandstone colors are properly implemented."""
        # Test sandstone color function
        base_sandstone = get_sandstone_color()
        lighter_sandstone = get_sandstone_color(15)
        darker_sandstone = get_sandstone_color(-15)
        
        assert base_sandstone == (245, 222, 179)  # F5DEB3
        assert lighter_sandstone == (255, 237, 194)  # Lighter
        assert darker_sandstone == (230, 207, 164)  # Darker
        
        # Test theme color hierarchy
        colors = self.theme.colors
        assert hasattr(colors, 'SANDSTONE_LIGHT')
        assert hasattr(colors, 'SANDSTONE')
        assert hasattr(colors, 'SANDSTONE_MEDIUM')
        assert hasattr(colors, 'SANDSTONE_DARK')
        
        print("✓ Sandstone color hierarchy implemented correctly")
    
    def test_filter_panel_collapsible(self):
        """Test the collapsible filter panel functionality."""
        filter_panel = FilterPanel(50, 50, 300, 600)
        
        # Test initial state
        assert not filter_panel.is_collapsed
        assert filter_panel.collapse_animation_progress == 1.0
        
        # Test collapse state
        filter_panel.is_collapsed = True
        filter_panel.update(0.1)  # Simulate animation update
        
        # Animation should be progressing toward collapsed state
        assert filter_panel.collapse_animation_progress < 1.0
        assert filter_panel.rect.height < filter_panel.expanded_height
        
        print("✓ Collapsible filter panel working correctly")
    
    def test_egyptian_animations(self):
        """Test Egyptian-themed animation system."""
        animation_manager = AnimationManager()
        renderer = EgyptianAnimationRenderer()
        
        # Test animation manager has Egyptian methods
        assert hasattr(animation_manager, 'ankh_selection')
        assert hasattr(animation_manager, 'scarab_rare_rotation')
        assert hasattr(animation_manager, 'lotus_hover_bloom')
        assert hasattr(animation_manager, 'egyptian_pulse')
        
        # Test renderer has Egyptian render methods
        assert hasattr(renderer, 'render_ankh_glow')
        assert hasattr(renderer, 'render_scarab_rotation')
        assert hasattr(renderer, 'render_lotus_bloom')
        assert hasattr(renderer, 'render_egyptian_pulse')
        
        # Test animation creation
        animation_manager.ankh_selection("test_card", duration=0.5)
        assert animation_manager.is_animating("test_card")
        
        print("✓ Egyptian animations implemented correctly")
    
    def test_card_display_accessibility(self):
        """Test accessibility features in card display."""
        # Create a test card
        test_card = Card(
            name="Test Card",
            description="A test card for accessibility",
            sand_cost=3,
            card_type=CardType.ATTACK,
            rarity=CardRarity.RARE,
            effects=[CardEffect(
                effect_type=EffectType.DAMAGE,
                value=5,
                target=TargetType.ENEMY
            )]
        )
        
        card_display = CardDisplay(100, 100, 120, 160, test_card, owned_count=2, is_favorite=True)
        
        # Test accessibility attributes
        assert hasattr(card_display, 'accessibility')
        assert card_display.accessibility['role'] == 'button'
        assert card_display.accessibility['keyboard_accessible'] == True
        assert 'Test Card' in card_display.accessibility['label']
        assert 'rare' in card_display.accessibility['label'].lower()
        assert 'attack' in card_display.accessibility['label'].lower()
        
        print("✓ Card accessibility features implemented correctly")
    
    def test_filter_panel_accessibility(self):
        """Test accessibility features in filter panel."""
        filter_panel = FilterPanel(50, 50, 300, 600)
        
        # Test accessibility methods
        assert hasattr(filter_panel, 'toggle_high_contrast')
        assert hasattr(filter_panel, 'get_accessibility_info')
        
        # Test accessibility info with no filters
        info = filter_panel.get_accessibility_info()
        assert "No active filters" in info
        
        # Test accessibility info with filters
        filter_panel.selected_rarity = CardRarity.RARE
        filter_panel.search_text = "fire"
        info = filter_panel.get_accessibility_info()
        assert "Rarity: rare" in info
        assert "Search: fire" in info
        
        # Test high contrast toggle
        initial_mode = filter_panel.high_contrast_mode
        filter_panel.toggle_high_contrast()
        assert filter_panel.high_contrast_mode != initial_mode
        
        print("✓ Filter panel accessibility features implemented correctly")
    
    def test_lazy_loading_optimization(self):
        """Test lazy loading performance optimization."""
        player_collection = PlayerCollection()
        
        # Create a large collection to test lazy loading
        test_cards = []
        for i in range(100):  # Large number of cards
            card = Card(
                name=f"Test Card {i}",
                description=f"Test card number {i}",
                sand_cost=i % 7,
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                effects=[]
            )
            test_cards.append(card)
            player_collection.add_card(card.id, 1)
        
        # Test collection with lazy loading enabled
        from sands_duat.ui.deck_builder import CardCollection
        collection = CardCollection(100, 100, 800, 600, player_collection)
        collection.lazy_loading_enabled = True
        collection.filtered_cards = test_cards
        
        # Test that visible range is calculated
        collection._create_card_displays()
        visible_range = collection.last_visible_range
        
        # Should not create displays for all 100 cards
        assert len(collection.card_displays) < len(test_cards)
        assert visible_range[0] >= 0
        assert visible_range[1] <= len(test_cards)
        
        print("✓ Lazy loading optimization working correctly")
    
    def test_deck_builder_theme_integration(self):
        """Test that deck builder properly uses the enhanced theme."""
        deck_builder = DeckBuilderScreen()
        deck_builder.on_enter()
        
        # Test that theme styling methods are available
        deck_style = self.theme.create_deck_builder_style()
        assert 'collection_background' in deck_style
        assert 'deck_view_background' in deck_style
        assert 'filter_panel_background' in deck_style
        assert 'card_background' in deck_style
        
        # Test card styling with rarity
        card_style = self.theme.create_card_style(CardRarity.LEGENDARY, CardType.ATTACK)
        assert 'background_color' in card_style
        assert 'border_color' in card_style
        assert 'type_accent' in card_style
        
        deck_builder.on_exit()
        
        print("✓ Deck builder theme integration working correctly")
    
    def test_keyboard_shortcuts(self):
        """Test keyboard accessibility shortcuts."""
        filter_panel = FilterPanel(50, 50, 300, 600)
        
        # Create mock events for testing
        class MockEvent:
            def __init__(self, event_type, key=None, mod=0, unicode=''):
                self.type = event_type
                self.key = key
                self.mod = mod
                self.unicode = unicode
        
        # Test F1 for high contrast
        f1_event = MockEvent(pygame.KEYDOWN, pygame.K_F1)
        initial_mode = filter_panel.high_contrast_mode
        handled = filter_panel.handle_event(f1_event)
        assert handled
        assert filter_panel.high_contrast_mode != initial_mode
        
        # Test Ctrl+C for clear filters
        filter_panel.selected_rarity = CardRarity.RARE
        ctrl_c_event = MockEvent(pygame.KEYDOWN, pygame.K_c, pygame.KMOD_CTRL)
        handled = filter_panel.handle_event(ctrl_c_event)
        assert handled
        assert filter_panel.selected_rarity is None
        
        # Test slash for search focus
        slash_event = MockEvent(pygame.KEYDOWN, pygame.K_SLASH)
        handled = filter_panel.handle_event(slash_event)
        assert handled
        assert filter_panel.search_input_active
        
        print("✓ Keyboard accessibility shortcuts working correctly")


def run_enhanced_deck_builder_test():
    """Run all enhanced deck builder tests."""
    print("Testing Enhanced Deck Builder with CrewAI Improvements...")
    print("=" * 60)
    
    test_instance = TestEnhancedDeckBuilder()
    test_instance.setup_class()
    
    try:
        test_instance.test_sandstone_color_hierarchy()
        test_instance.test_filter_panel_collapsible()
        test_instance.test_egyptian_animations()
        test_instance.test_card_display_accessibility()
        test_instance.test_filter_panel_accessibility()
        test_instance.test_lazy_loading_optimization()
        test_instance.test_deck_builder_theme_integration()
        test_instance.test_keyboard_shortcuts()
        
        print("=" * 60)
        print("🎉 All enhanced deck builder tests passed!")
        print()
        print("CrewAI Improvements Successfully Implemented:")
        print("✓ Collapsible filter panel with Egyptian styling")
        print("✓ Egyptian-themed animations (Ankh, Scarab, Lotus)")
        print("✓ Sandstone color hierarchy (F5DEB3 base)")
        print("✓ Lazy loading performance optimizations")
        print("✓ Comprehensive accessibility features")
        print("✓ Keyboard shortcuts and high contrast mode")
        print("✓ Ultrawide display compatibility (3440x1440)")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        test_instance.teardown_class()


if __name__ == "__main__":
    success = run_enhanced_deck_builder_test()
    sys.exit(0 if success else 1)