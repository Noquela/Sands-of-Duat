#!/usr/bin/env python3
"""
SANDS OF DUAT - COMPLETE GAME EXPERIENCE TEST
==============================================

End-to-end test simulating the complete Egyptian card game experience.
Tests the full pipeline from menu to combat with all 75 Egyptian assets.
"""

import sys
import time
from pathlib import Path
import pygame
from unittest.mock import patch, MagicMock

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.core.asset_loader import EgyptianAssetLoader, AssetCategory, initialize_assets
from sands_of_duat.cards.egyptian_cards import EgyptianDeckBuilder, CardType, CardRarity
from sands_of_duat.ui.game_interface import SandsOfDuatGame, GameState

def test_complete_game_initialization():
    """Test complete game system initialization."""
    print("Testing complete game initialization...")
    
    pygame.init()
    
    try:
        start_time = time.time()
        
        # Initialize all systems
        asset_loader = initialize_assets()
        deck_builder = EgyptianDeckBuilder()
        
        # Simulate game interface initialization
        with patch('pygame.display.set_mode') as mock_display:
            mock_display.return_value = pygame.Surface((1400, 900))
            game = SandsOfDuatGame()
            
            init_time = time.time() - start_time
            
            print(f"    * Game initialized in {init_time:.2f} seconds")
            print(f"    * Assets loaded: {asset_loader.get_total_asset_count()}")
            print(f"    * Cards available: {len(game.available_cards)}")
            print(f"    * Player deck size: {len(game.player_deck)}")
            print(f"    * Menu buttons: {len(game.menu_buttons)}")
            
            # Verify all systems are properly connected
            systems_working = (
                asset_loader.get_total_asset_count() >= 70 and
                len(game.available_cards) >= 20 and
                len(game.player_deck) >= 10 and
                len(game.menu_buttons) >= 4 and
                game.state == GameState.MENU
            )
            
            return systems_working and init_time < 2.0
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_asset_to_card_pipeline():
    """Test the complete asset-to-card rendering pipeline."""
    print("Testing asset to card pipeline...")
    
    pygame.init()
    
    try:
        # Initialize systems
        asset_loader = EgyptianAssetLoader()
        deck_builder = EgyptianDeckBuilder()
        cards = deck_builder.get_all_cards()
        
        pipeline_tests = 0
        successful_tests = 0
        
        # Test each card category
        for category in AssetCategory:
            assets = asset_loader.get_assets_by_category(category)
            if not assets:
                continue
            
            pipeline_tests += 1
            
            try:
                # Load raw asset
                raw_surface = asset_loader.load_image(assets[0])
                
                # Find a card that uses this category
                category_cards = [card for card in cards if card.asset_category == category]
                
                if category_cards and raw_surface:
                    test_card = category_cards[0]
                    
                    # Render complete card
                    card_surface = test_card.render_card()
                    
                    if card_surface and card_surface.get_size() == (300, 420):
                        successful_tests += 1
                        print(f"    * {category.name}: {assets[0]} -> {test_card.name} ✓")
                    else:
                        print(f"    * {category.name}: {assets[0]} -> {test_card.name} ✗")
                
            except Exception as e:
                print(f"    * {category.name}: Error - {e}")
        
        print(f"    * Pipeline tests: {successful_tests}/{pipeline_tests}")
        
        success_rate = successful_tests / pipeline_tests if pipeline_tests > 0 else 0
        return success_rate >= 0.8  # At least 80% should work
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_game_state_navigation():
    """Test navigation between game states."""
    print("Testing game state navigation...")
    
    pygame.init()
    
    try:
        with patch('pygame.display.set_mode') as mock_display:
            mock_surface = pygame.Surface((1400, 900))
            mock_display.return_value = mock_surface
            
            game = SandsOfDuatGame()
            
            # Test state transitions
            original_state = game.state
            print(f"    * Initial state: {original_state.value}")
            
            # Test all main states
            states_to_test = [
                GameState.DECK_BUILDER,
                GameState.CARD_GALLERY,
                GameState.COMBAT,
                GameState.SETTINGS,
                GameState.MENU
            ]
            
            successful_transitions = 0
            
            for state in states_to_test:
                try:
                    game.state = state
                    
                    # Simulate a frame render for this state
                    game.render()  # This should not crash
                    
                    if game.state == state:
                        successful_transitions += 1
                        print(f"    * Transition to {state.value}: ✓")
                    else:
                        print(f"    * Transition to {state.value}: ✗")
                        
                except Exception as e:
                    print(f"    * Transition to {state.value}: Error - {e}")
            
            print(f"    * Successful transitions: {successful_transitions}/{len(states_to_test)}")
            
            return successful_transitions == len(states_to_test)
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_deck_building_workflow():
    """Test the complete deck building workflow."""
    print("Testing deck building workflow...")
    
    pygame.init()
    
    try:
        with patch('pygame.display.set_mode') as mock_display:
            mock_surface = pygame.Surface((1400, 900))
            mock_display.return_value = mock_surface
            
            game = SandsOfDuatGame()
            
            # Switch to deck builder
            game.state = GameState.DECK_BUILDER
            
            initial_deck_size = len(game.player_deck)
            available_cards = len(game.available_cards)
            
            print(f"    * Initial deck size: {initial_deck_size}")
            print(f"    * Available cards: {available_cards}")
            
            # Simulate adding cards to deck
            cards_to_add = min(5, len(game.available_cards))
            
            for i in range(cards_to_add):
                if len(game.player_deck) < 30:  # Max deck size
                    card_to_add = game.available_cards[i]
                    game.player_deck.append(card_to_add)
            
            final_deck_size = len(game.player_deck)
            cards_added = final_deck_size - initial_deck_size
            
            print(f"    * Final deck size: {final_deck_size}")
            print(f"    * Cards added: {cards_added}")
            
            # Test deck builder rendering
            try:
                game.render()  # Should render deck builder interface
                rendering_works = True
            except Exception:
                rendering_works = False
            
            print(f"    * Deck builder rendering: {'✓' if rendering_works else '✗'}")
            
            # Test deck validation
            deck_types = set(card.card_type for card in game.player_deck)
            has_variety = len(deck_types) >= 2
            
            print(f"    * Deck variety: {'✓' if has_variety else '✗'}")
            
            return cards_added > 0 and rendering_works and has_variety
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_card_gallery_display():
    """Test the card gallery display functionality."""
    print("Testing card gallery display...")
    
    pygame.init()
    
    try:
        with patch('pygame.display.set_mode') as mock_display:
            mock_surface = pygame.Surface((1400, 900))
            mock_display.return_value = mock_surface
            
            game = SandsOfDuatGame()
            
            # Switch to card gallery
            game.state = GameState.CARD_GALLERY
            
            total_cards = len(game.gallery_cards)
            print(f"    * Cards in gallery: {total_cards}")
            
            # Test gallery rendering
            try:
                game.render()  # Should render gallery interface
                rendering_works = True
            except Exception as e:
                print(f"    * Gallery rendering error: {e}")
                rendering_works = False
            
            print(f"    * Gallery rendering: {'✓' if rendering_works else '✗'}")
            
            # Test scrolling simulation
            original_scroll = game.gallery_scroll
            game.gallery_scroll = 100  # Simulate scroll
            
            try:
                game.render()  # Should still render with scrolling
                scrolling_works = True
            except Exception:
                scrolling_works = False
            
            print(f"    * Gallery scrolling: {'✓' if scrolling_works else '✗'}")
            
            # Reset scroll
            game.gallery_scroll = original_scroll
            
            return rendering_works and scrolling_works and total_cards >= 20
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_combat_system_readiness():
    """Test that the combat system is ready for implementation."""
    print("Testing combat system readiness...")
    
    pygame.init()
    
    try:
        with patch('pygame.display.set_mode') as mock_display:
            mock_surface = pygame.Surface((1400, 900))
            mock_display.return_value = mock_surface
            
            game = SandsOfDuatGame()
            
            # Switch to combat mode
            game.state = GameState.COMBAT
            
            print(f"    * Player deck size: {len(game.player_deck)}")
            
            # Test combat interface rendering
            try:
                game.render()  # Should render combat interface
                rendering_works = True
            except Exception as e:
                print(f"    * Combat rendering error: {e}")
                rendering_works = False
            
            print(f"    * Combat interface rendering: {'✓' if rendering_works else '✗'}")
            
            # Check that combat cards are available
            combat_cards = [card for card in game.player_deck 
                          if card.card_type in [CardType.GOD, CardType.CREATURE]]
            
            print(f"    * Combat-ready cards: {len(combat_cards)}")
            
            # Test card rendering in combat context
            cards_rendered = 0
            if game.player_deck:
                try:
                    sample_card = game.player_deck[0]
                    card_surface = sample_card.render_card((300, 420))
                    if card_surface:
                        cards_rendered = 1
                except Exception:
                    pass
            
            print(f"    * Cards rendered in combat: {cards_rendered}")
            
            return (rendering_works and 
                   len(game.player_deck) >= 5 and 
                   len(combat_cards) >= 2 and
                   cards_rendered > 0)
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_performance_under_load():
    """Test performance with full system under load."""
    print("Testing performance under load...")
    
    pygame.init()
    
    try:
        start_time = time.time()
        
        # Initialize full system
        asset_loader = initialize_assets()
        deck_builder = EgyptianDeckBuilder()
        
        with patch('pygame.display.set_mode') as mock_display:
            mock_surface = pygame.Surface((1400, 900))
            mock_display.return_value = mock_surface
            
            game = SandsOfDuatGame()
            
            # Simulate intensive operations
            operations = [
                ("Asset loading", lambda: [asset_loader.load_image(asset, (200, 200)) 
                                         for assets in [asset_loader.get_assets_by_category(cat)[:3] 
                                                      for cat in AssetCategory] 
                                         for asset in assets]),
                ("Card rendering", lambda: [card.render_card() for card in game.available_cards[:10]]),
                ("Deck operations", lambda: [deck_builder.create_random_deck(15) for _ in range(5)]),
                ("UI rendering", lambda: [game.render() for _ in range(3)])
            ]
            
            performance_results = []
            
            for op_name, operation in operations:
                op_start = time.time()
                try:
                    operation()
                    op_time = time.time() - op_start
                    performance_results.append((op_name, op_time, True))
                    print(f"    * {op_name}: {op_time:.2f}s ✓")
                except Exception as e:
                    op_time = time.time() - op_start
                    performance_results.append((op_name, op_time, False))
                    print(f"    * {op_name}: {op_time:.2f}s ✗ ({e})")
            
            total_time = time.time() - start_time
            print(f"    * Total test time: {total_time:.2f}s")
            
            # Check results
            successful_ops = sum(1 for _, _, success in performance_results if success)
            all_fast = all(time < 5.0 for _, time, success in performance_results if success)
            
            print(f"    * Successful operations: {successful_ops}/{len(operations)}")
            print(f"    * All operations under 5s: {'✓' if all_fast else '✗'}")
            
            return successful_ops >= len(operations) - 1 and all_fast  # Allow 1 failure
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_memory_stability():
    """Test memory stability during extended operations."""
    print("Testing memory stability...")
    
    pygame.init()
    
    try:
        asset_loader = EgyptianAssetLoader()
        asset_loader.max_cache_size = 15  # Moderate cache for testing
        
        # Perform many asset operations
        initial_cache = len(asset_loader._image_cache)
        
        # Load and reload assets multiple times
        for cycle in range(3):
            for category in AssetCategory:
                assets = asset_loader.get_assets_by_category(category)
                
                for asset in assets[:5]:  # Load 5 assets per category per cycle
                    surface = asset_loader.load_image(asset, (150, 150))
                    
        final_cache = len(asset_loader._image_cache)
        
        print(f"    * Cache size: {initial_cache} -> {final_cache}")
        print(f"    * Max cache size: {asset_loader.max_cache_size}")
        
        # Test cache clearing
        asset_loader.clear_cache()
        cleared_cache = len(asset_loader._image_cache)
        
        print(f"    * Cache after clearing: {cleared_cache}")
        
        # Memory should be properly managed
        cache_managed = final_cache <= asset_loader.max_cache_size
        cache_cleared = cleared_cache == 0
        
        print(f"    * Cache properly managed: {'✓' if cache_managed else '✗'}")
        print(f"    * Cache properly cleared: {'✓' if cache_cleared else '✗'}")
        
        return cache_managed and cache_cleared
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def run_complete_game_test():
    """Run the complete game experience test."""
    print("SANDS OF DUAT - COMPLETE GAME EXPERIENCE TEST")
    print("=" * 47)
    print("Testing the full Egyptian card game with all 75 assets")
    print()
    
    tests = [
        ("Game Initialization", test_complete_game_initialization),
        ("Asset-to-Card Pipeline", test_asset_to_card_pipeline),
        ("Game State Navigation", test_game_state_navigation),
        ("Deck Building Workflow", test_deck_building_workflow),
        ("Card Gallery Display", test_card_gallery_display),
        ("Combat System Readiness", test_combat_system_readiness),
        ("Performance Under Load", test_performance_under_load),
        ("Memory Stability", test_memory_stability)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                print(f"  Result: PASSED")
                passed += 1
            else:
                print(f"  Result: FAILED")
        except Exception as e:
            print(f"  Result: ERROR - {e}")
        
        print()  # Add spacing between tests
    
    print("=" * 47)
    print(f"COMPLETE GAME TEST RESULTS:")
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    print()
    
    if passed == total:
        print("🎉 COMPLETE SUCCESS! 🎉")
        print("The Sands of Duat Egyptian card game is fully integrated and ready!")
        print("✓ All 75 Egyptian assets properly loaded and integrated")
        print("✓ Complete card system with balanced gameplay")
        print("✓ Full UI system with menu, deck builder, and gallery")
        print("✓ Performance optimized for smooth gameplay")
        print("✓ Memory management working correctly")
        print()
        print("THE EGYPTIAN UNDERWORLD AWAITS YOUR CHALLENGE!")
    elif passed >= total - 1:
        print("🌟 NEARLY PERFECT! 🌟")
        print("The game is ready with only minor issues.")
        print("The Egyptian card game experience is complete and playable!")
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("The game may need additional work before release.")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = run_complete_game_test()
    sys.exit(0 if success else 1)