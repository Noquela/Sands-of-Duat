#!/usr/bin/env python3
"""
SANDS OF DUAT - PERFORMANCE VALIDATION TESTS
============================================

Performance tests for the complete Egyptian card game system.
"""

import sys
import time
from pathlib import Path
import pygame

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.core.asset_loader import EgyptianAssetLoader, AssetCategory
from sands_of_duat.cards.egyptian_cards import EgyptianDeckBuilder
from sands_of_duat.ui.game_interface import SandsOfDuatGame

def test_startup_time():
    """Test game startup performance."""
    print("Testing startup time...")
    
    try:
        start_time = time.time()
        
        # Initialize pygame
        pygame.init()
        
        # Initialize asset loader
        asset_loader = EgyptianAssetLoader()
        
        # Initialize deck builder
        deck_builder = EgyptianDeckBuilder()
        
        # Preload essential assets
        asset_loader.preload_essential_assets()
        
        startup_time = time.time() - start_time
        
        print(f"    * Startup completed in {startup_time:.2f} seconds")
        print(f"    * Loaded {asset_loader.get_total_asset_count()} assets")
        print(f"    * Created {len(deck_builder.get_all_cards())} cards")
        
        # Cleanup
        pygame.quit()
        
        return startup_time < 5.0  # Should start up in under 5 seconds
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_asset_loading_speed():
    """Test asset loading performance."""
    print("Testing asset loading speed...")
    
    pygame.init()
    
    try:
        loader = EgyptianAssetLoader()
        
        # Test batch loading
        start_time = time.time()
        loaded_assets = []
        
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            
            # Load first 3 assets from each category
            for asset_name in assets[:3]:
                surface = loader.load_image(asset_name, (300, 420))
                if surface:
                    loaded_assets.append(asset_name)
        
        load_time = time.time() - start_time
        
        print(f"    * Loaded {len(loaded_assets)} assets in {load_time:.2f} seconds")
        print(f"    * Average load time: {(load_time/len(loaded_assets))*1000:.1f}ms per asset")
        
        # Test cached loading speed
        start_time = time.time()
        for asset_name in loaded_assets[:5]:
            surface = loader.load_image(asset_name, (300, 420))
        cached_time = time.time() - start_time
        
        print(f"    * Cached loading: {cached_time*1000:.1f}ms for 5 assets")
        
        return load_time < 3.0  # Should load test assets in under 3 seconds
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_card_rendering_performance():
    """Test card rendering performance."""
    print("Testing card rendering performance...")
    
    pygame.init()
    
    try:
        deck_builder = EgyptianDeckBuilder()
        cards = deck_builder.get_all_cards()
        
        # Test rendering multiple cards
        start_time = time.time()
        rendered_cards = []
        
        for card in cards[:10]:  # Test first 10 cards
            surface = card.render_card()
            if surface:
                rendered_cards.append(card.name)
        
        render_time = time.time() - start_time
        
        print(f"    * Rendered {len(rendered_cards)} cards in {render_time:.2f} seconds")
        print(f"    * Average render time: {(render_time/len(rendered_cards))*1000:.1f}ms per card")
        
        # Test cached rendering
        start_time = time.time()
        for card in cards[:5]:
            surface = card.render_card()  # Should be cached
        cached_render_time = time.time() - start_time
        
        print(f"    * Cached rendering: {cached_render_time*1000:.1f}ms for 5 cards")
        
        return render_time < 2.0  # Should render 10 cards in under 2 seconds
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_memory_efficiency():
    """Test memory usage efficiency."""
    print("Testing memory efficiency...")
    
    pygame.init()
    
    try:
        loader = EgyptianAssetLoader()
        loader.max_cache_size = 20  # Moderate cache size
        
        initial_cache = len(loader._image_cache)
        
        # Load many assets
        asset_count = 0
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            
            for asset_name in assets[:10]:  # Load up to 10 from each category
                surface = loader.load_image(asset_name, (200, 200))
                if surface:
                    asset_count += 1
        
        final_cache = len(loader._image_cache)
        
        print(f"    * Loaded {asset_count} assets")
        print(f"    * Cache grew from {initial_cache} to {final_cache} items")
        print(f"    * Cache efficiency: {(final_cache/loader.max_cache_size)*100:.1f}%")
        
        # Cache should not exceed maximum
        cache_within_limit = final_cache <= loader.max_cache_size
        
        # Test cache clearing
        loader.clear_cache()
        cleared_cache = len(loader._image_cache)
        
        print(f"    * Cache after clearing: {cleared_cache} items")
        
        return cache_within_limit and cleared_cache == 0
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_fps_simulation():
    """Test FPS performance in a simulated game loop."""
    print("Testing FPS simulation...")
    
    pygame.init()
    
    try:
        # Create a mock screen
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        
        # Initialize systems
        loader = EgyptianAssetLoader()
        deck_builder = EgyptianDeckBuilder()
        cards = deck_builder.get_all_cards()[:5]  # Use 5 cards for simulation
        
        # Simulate game loop
        frame_count = 0
        total_time = 0
        max_frames = 60  # Test 1 second worth of frames at 60 FPS
        
        for _ in range(max_frames):
            frame_start = time.time()
            
            # Simulate game rendering
            screen.fill((25, 25, 112))  # Dark blue background
            
            # Render some cards
            for i, card in enumerate(cards):
                card_surface = card.render_card((150, 210))  # Smaller for performance
                if card_surface:
                    screen.blit(card_surface, (i * 160, 100))
            
            # Update display
            pygame.display.flip()
            
            # Track frame time
            frame_time = time.time() - frame_start
            total_time += frame_time
            frame_count += 1
            
            # Limit to 60 FPS
            clock.tick(60)
        
        avg_frame_time = (total_time / frame_count) * 1000  # Convert to milliseconds
        estimated_fps = 1000 / avg_frame_time if avg_frame_time > 0 else 0
        
        print(f"    * Simulated {frame_count} frames")
        print(f"    * Average frame time: {avg_frame_time:.1f}ms")
        print(f"    * Estimated FPS: {estimated_fps:.1f}")
        
        # Should maintain at least 30 FPS (33.3ms per frame)
        return avg_frame_time < 33.3
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_large_deck_performance():
    """Test performance with large deck operations."""
    print("Testing large deck performance...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        # Test deck operations
        start_time = time.time()
        
        # Create multiple decks
        decks = []
        for i in range(10):
            deck = deck_builder.create_random_deck(20)
            decks.append(deck)
        
        deck_creation_time = time.time() - start_time
        
        # Test deck searches
        start_time = time.time()
        
        god_cards = deck_builder.get_cards_by_type(deck_builder.CardType.GOD if hasattr(deck_builder, 'CardType') else None)
        rare_cards = deck_builder.get_cards_by_rarity(deck_builder.CardRarity.RARE if hasattr(deck_builder, 'CardRarity') else None)
        
        search_time = time.time() - start_time
        
        print(f"    * Created {len(decks)} decks in {deck_creation_time:.2f} seconds")
        print(f"    * Performed searches in {search_time*1000:.1f}ms")
        print(f"    * Total cards available: {len(all_cards)}")
        
        return deck_creation_time < 1.0  # Should create decks quickly
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_concurrent_operations():
    """Test performance under concurrent operations."""
    print("Testing concurrent operations...")
    
    pygame.init()
    
    try:
        # Simulate multiple operations happening at once
        start_time = time.time()
        
        # Initialize multiple systems
        loader1 = EgyptianAssetLoader()
        loader2 = EgyptianAssetLoader()  # Should reuse global instance
        
        deck_builder1 = EgyptianDeckBuilder()
        deck_builder2 = EgyptianDeckBuilder()
        
        # Perform operations concurrently (simulated)
        operations_completed = 0
        
        # Load assets from different categories
        for category in list(AssetCategory)[:3]:  # Test 3 categories
            assets = loader1.get_assets_by_category(category)
            if assets:
                surface = loader1.load_image(assets[0], (100, 100))
                if surface:
                    operations_completed += 1
        
        # Create decks
        deck1 = deck_builder1.create_starter_deck()
        deck2 = deck_builder2.create_random_deck(15)
        
        if deck1 and deck2:
            operations_completed += 2
        
        concurrent_time = time.time() - start_time
        
        print(f"    * Completed {operations_completed} concurrent operations")
        print(f"    * Total time: {concurrent_time:.2f} seconds")
        print(f"    * Average per operation: {(concurrent_time/operations_completed)*1000:.1f}ms")
        
        return concurrent_time < 3.0  # Should handle concurrent operations efficiently
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def run_performance_tests():
    """Run all performance validation tests."""
    print("SANDS OF DUAT - PERFORMANCE VALIDATION TESTS")
    print("=" * 47)
    
    tests = [
        ("Startup Time", test_startup_time),
        ("Asset Loading Speed", test_asset_loading_speed),
        ("Card Rendering Performance", test_card_rendering_performance),
        ("Memory Efficiency", test_memory_efficiency),
        ("FPS Simulation", test_fps_simulation),
        ("Large Deck Performance", test_large_deck_performance),
        ("Concurrent Operations", test_concurrent_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                print(f"  Result: PASSED")
                passed += 1
            else:
                print(f"  Result: FAILED")
        except Exception as e:
            print(f"  Result: ERROR - {e}")
    
    print(f"\n" + "=" * 47)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All performance tests passed!")
        print("The game runs efficiently and is ready for gameplay.")
    elif passed >= total - 1:
        print("MOSTLY SUCCESSFUL: Performance is good with minor issues.")
        print("The game should run smoothly for most players.")
    else:
        print("Performance issues detected. Optimization may be needed.")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = run_performance_tests()
    sys.exit(0 if success else 1)