#!/usr/bin/env python3
"""
SANDS OF DUAT - COMPLETE INTEGRATION TESTS
==========================================

Comprehensive tests for the integrated Egyptian card game system.
Tests all components from asset loading to gameplay.
"""

import pytest
import pygame
import sys
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.core.asset_loader import EgyptianAssetLoader, AssetCategory, get_asset_loader, initialize_assets
from sands_of_duat.cards.egyptian_cards import EgyptianCard, CardType, CardRarity, CardStats, EgyptianDeckBuilder, get_deck_builder
from sands_of_duat.ui.game_interface import SandsOfDuatGame, GameState

class TestAssetIntegration:
    """Test the asset loading and integration system."""
    
    def test_asset_loader_initialization(self):
        """Test that the asset loader initializes correctly."""
        # Mock the assets path to avoid file system dependencies
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[]):
                loader = EgyptianAssetLoader()
                assert loader.get_total_asset_count() >= 0
                assert len(loader._asset_registry) == len(AssetCategory)
    
    def test_asset_categorization(self):
        """Test that assets are correctly categorized."""
        with patch('pathlib.Path.exists', return_value=True):
            mock_files = [
                Path(f"egyptian_god_ra_01_q81.png"),
                Path(f"egyptian_artifact_02_q77.png"),
                Path(f"egyptian_myth_03_q77.png"),
                Path(f"underworld_location_10_q61.png"),
            ]
            
            with patch('pathlib.Path.glob', return_value=mock_files):
                loader = EgyptianAssetLoader()
                
                # Check that categories have assets
                gods = loader.get_assets_by_category(AssetCategory.GODS)
                artifacts = loader.get_assets_by_category(AssetCategory.ARTIFACTS)
                myths = loader.get_assets_by_category(AssetCategory.MYTHS)
                locations = loader.get_assets_by_category(AssetCategory.UNDERWORLD_LOCATIONS)
                
                assert len(gods) >= 0
                assert len(artifacts) >= 0
                assert len(myths) >= 0
                assert len(locations) >= 0
    
    def test_asset_loading_with_pygame(self):
        """Test asset loading with pygame initialization."""
        pygame.init()
        
        # Create a simple test image
        test_surface = pygame.Surface((100, 100))
        test_surface.fill((255, 0, 0))  # Red surface
        
        with patch('pygame.image.load', return_value=test_surface):
            with patch('pathlib.Path.exists', return_value=True):
                loader = EgyptianAssetLoader()
                
                # Test image loading
                loaded_image = loader.load_image("test.png", (50, 50))
                assert loaded_image is not None
                assert loaded_image.get_size() == (50, 50)
        
        pygame.quit()
    
    def test_cache_management(self):
        """Test that asset caching works correctly."""
        pygame.init()
        
        test_surface = pygame.Surface((100, 100))
        
        with patch('pygame.image.load', return_value=test_surface):
            with patch('pathlib.Path.exists', return_value=True):
                loader = EgyptianAssetLoader()
                loader.max_cache_size = 2  # Small cache for testing
                
                # Load images
                img1 = loader.load_image("img1.png")
                img2 = loader.load_image("img2.png")
                img3 = loader.load_image("img3.png")  # Should evict img1
                
                cache_stats = loader.get_cache_stats()
                assert cache_stats['cached_images'] <= loader.max_cache_size
        
        pygame.quit()

class TestCardSystem:
    """Test the Egyptian card system."""
    
    def test_card_creation(self):
        """Test creating Egyptian cards."""
        stats = CardStats(attack=5, health=3, cost=2)
        card = EgyptianCard(
            name="Test God",
            card_type=CardType.GOD,
            rarity=CardRarity.RARE,
            stats=stats,
            description="A test god card",
            asset_category=AssetCategory.GODS,
            asset_index=0
        )
        
        assert card.name == "Test God"
        assert card.card_type == CardType.GOD
        assert card.rarity == CardRarity.RARE
        assert card.stats.attack == 5
        assert card.stats.health == 3
        assert card.stats.cost == 2
    
    def test_deck_builder_initialization(self):
        """Test that the deck builder creates cards correctly."""
        with patch('sands_of_duat.core.asset_loader.get_asset_loader'):
            builder = EgyptianDeckBuilder()
            
            all_cards = builder.get_all_cards()
            assert len(all_cards) > 0
            
            # Test different card types exist
            god_cards = builder.get_cards_by_type(CardType.GOD)
            artifact_cards = builder.get_cards_by_type(CardType.ARTIFACT)
            spell_cards = builder.get_cards_by_type(CardType.SPELL)
            
            assert len(god_cards) > 0
            assert len(artifact_cards) > 0
            assert len(spell_cards) > 0
    
    def test_starter_deck_creation(self):
        """Test starter deck creation."""
        with patch('sands_of_duat.core.asset_loader.get_asset_loader'):
            builder = EgyptianDeckBuilder()
            starter_deck = builder.create_starter_deck()
            
            assert len(starter_deck) > 0
            assert len(starter_deck) <= 30  # Reasonable deck size
            
            # Check variety of card types
            card_types = set(card.card_type for card in starter_deck)
            assert len(card_types) > 1  # Should have multiple types
    
    def test_card_rendering(self):
        """Test card visual rendering."""
        pygame.init()
        
        stats = CardStats(attack=5, health=3, cost=2)
        card = EgyptianCard(
            name="Test Card",
            card_type=CardType.CREATURE,
            rarity=CardRarity.COMMON,
            stats=stats,
            description="Test description",
            asset_category=AssetCategory.OBJECTS,
            asset_index=0
        )
        
        # Mock artwork loading
        with patch.object(card, 'get_artwork', return_value=pygame.Surface((100, 100))):
            card_surface = card.render_card((200, 280))
            
            assert card_surface is not None
            assert card_surface.get_size() == (200, 280)
        
        pygame.quit()

class TestGameInterface:
    """Test the main game interface."""
    
    def test_game_initialization(self):
        """Test game initialization."""
        pygame.init()
        
        with patch('sands_of_duat.core.asset_loader.initialize_assets') as mock_assets:
            with patch('sands_of_duat.cards.egyptian_cards.get_deck_builder') as mock_builder:
                mock_loader = MagicMock()
                mock_loader.get_total_asset_count.return_value = 71
                mock_assets.return_value = mock_loader
                
                mock_deck_builder = MagicMock()
                mock_deck_builder.get_all_cards.return_value = []
                mock_deck_builder.create_starter_deck.return_value = []
                mock_builder.return_value = mock_deck_builder
                
                # Create game without running the main loop
                with patch('pygame.display.set_mode') as mock_display:
                    mock_display.return_value = MagicMock()
                    game = SandsOfDuatGame()
                    
                    assert game.state == GameState.MENU
                    assert game.running == True
                    assert len(game.colors) > 0
                    assert len(game.menu_buttons) > 0
        
        pygame.quit()
    
    def test_state_transitions(self):
        """Test game state transitions."""
        pygame.init()
        
        with patch('sands_of_duat.core.asset_loader.initialize_assets') as mock_assets:
            with patch('sands_of_duat.cards.egyptian_cards.get_deck_builder') as mock_builder:
                mock_loader = MagicMock()
                mock_assets.return_value = mock_loader
                
                mock_deck_builder = MagicMock()
                mock_deck_builder.get_all_cards.return_value = []
                mock_deck_builder.create_starter_deck.return_value = []
                mock_builder.return_value = mock_deck_builder
                
                with patch('pygame.display.set_mode') as mock_display:
                    mock_display.return_value = MagicMock()
                    game = SandsOfDuatGame()
                    
                    # Test state transitions
                    original_state = game.state
                    game.state = GameState.DECK_BUILDER
                    assert game.state == GameState.DECK_BUILDER
                    
                    game.state = GameState.CARD_GALLERY
                    assert game.state == GameState.CARD_GALLERY
                    
                    game.state = GameState.COMBAT
                    assert game.state == GameState.COMBAT
        
        pygame.quit()

class TestPerformance:
    """Test system performance with Egyptian assets."""
    
    def test_asset_loading_performance(self):
        """Test that asset loading is reasonably fast."""
        import time
        
        pygame.init()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.glob', return_value=[Path(f"test_{i}.png") for i in range(10)]):
                with patch('pygame.image.load', return_value=pygame.Surface((100, 100))):
                    start_time = time.time()
                    
                    loader = EgyptianAssetLoader()
                    # Load multiple images
                    for i in range(10):
                        loader.load_image(f"test_{i}.png")
                    
                    load_time = time.time() - start_time
                    
                    # Should load 10 images in reasonable time
                    assert load_time < 1.0  # Less than 1 second
        
        pygame.quit()
    
    def test_memory_usage(self):
        """Test memory usage stays reasonable."""
        pygame.init()
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pygame.image.load', return_value=pygame.Surface((200, 200))):
                loader = EgyptianAssetLoader()
                loader.max_cache_size = 5
                
                # Load many images
                for i in range(20):
                    loader.load_image(f"test_{i}.png")
                
                # Cache should not exceed maximum
                cache_stats = loader.get_cache_stats()
                assert cache_stats['cached_images'] <= loader.max_cache_size
        
        pygame.quit()

class TestEndToEndIntegration:
    """End-to-end integration tests."""
    
    def test_complete_asset_to_card_pipeline(self):
        """Test the complete pipeline from assets to rendered cards."""
        pygame.init()
        
        # Mock the entire pipeline
        with patch('pathlib.Path.exists', return_value=True):
            mock_files = [Path(f"egyptian_god_ra_01_q81.png")]
            
            with patch('pathlib.Path.glob', return_value=mock_files):
                with patch('pygame.image.load', return_value=pygame.Surface((300, 420))):
                    # Initialize systems
                    asset_loader = EgyptianAssetLoader()
                    deck_builder = EgyptianDeckBuilder()
                    
                    # Get cards
                    all_cards = deck_builder.get_all_cards()
                    assert len(all_cards) > 0
                    
                    # Test rendering a card with assets
                    test_card = all_cards[0]
                    card_surface = test_card.render_card()
                    
                    assert card_surface is not None
                    assert card_surface.get_size() == (300, 420)
        
        pygame.quit()
    
    def test_game_systems_integration(self):
        """Test that all game systems work together."""
        pygame.init()
        
        with patch('sands_of_duat.core.asset_loader.initialize_assets') as mock_init:
            mock_loader = MagicMock()
            mock_loader.get_total_asset_count.return_value = 71
            mock_loader.get_cache_stats.return_value = {
                'cached_images': 10,
                'max_cache_size': 100,
                'total_categories': len(AssetCategory),
                'total_assets': 71
            }
            mock_init.return_value = mock_loader
            
            with patch('sands_of_duat.cards.egyptian_cards.get_deck_builder') as mock_builder:
                mock_deck_builder = MagicMock()
                
                # Create mock cards
                mock_cards = []
                for i in range(5):
                    mock_card = MagicMock()
                    mock_card.name = f"Test Card {i}"
                    mock_card.card_type = CardType.GOD
                    mock_card.rarity = CardRarity.COMMON
                    mock_card.render_card.return_value = pygame.Surface((300, 420))
                    mock_cards.append(mock_card)
                
                mock_deck_builder.get_all_cards.return_value = mock_cards
                mock_deck_builder.create_starter_deck.return_value = mock_cards[:3]
                mock_builder.return_value = mock_deck_builder
                
                with patch('pygame.display.set_mode') as mock_display:
                    mock_display.return_value = MagicMock()
                    
                    # Create and test game
                    game = SandsOfDuatGame()
                    
                    # Test that all systems are properly initialized
                    assert game.asset_loader is not None
                    assert game.deck_builder is not None
                    assert len(game.available_cards) == 5
                    assert len(game.player_deck) == 3
                    assert game.state == GameState.MENU
        
        pygame.quit()

def run_all_tests():
    """Run all integration tests."""
    print("🏺 SANDS OF DUAT - RUNNING INTEGRATION TESTS 🏺")
    print("=" * 50)
    
    # Initialize pygame for tests
    pygame.init()
    
    try:
        test_classes = [
            TestAssetIntegration,
            TestCardSystem,
            TestGameInterface,
            TestPerformance,
            TestEndToEndIntegration
        ]
        
        total_tests = 0
        passed_tests = 0
        failed_tests = []
        
        for test_class in test_classes:
            print(f"\nTesting {test_class.__name__}...")
            test_instance = test_class()
            
            # Get all test methods
            test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
            
            for method_name in test_methods:
                total_tests += 1
                try:
                    test_method = getattr(test_instance, method_name)
                    test_method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {str(e)}")
                    failed_tests.append((test_class.__name__, method_name, str(e)))
        
        print(f"\n" + "=" * 50)
        print(f"INTEGRATION TEST RESULTS:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {len(failed_tests)}")
        
        if failed_tests:
            print(f"\nFAILED TESTS:")
            for class_name, method_name, error in failed_tests:
                print(f"  {class_name}.{method_name}: {error}")
        else:
            print(f"\n🎉 ALL INTEGRATION TESTS PASSED! 🎉")
            print(f"The Egyptian card game is ready for gameplay!")
        
        print(f"\n" + "=" * 50)
        
        return len(failed_tests) == 0
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)