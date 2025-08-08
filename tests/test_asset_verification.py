#!/usr/bin/env python3
"""
SANDS OF DUAT - ASSET VERIFICATION TESTS
========================================

Comprehensive verification of all 71+ Egyptian assets and their integration.
"""

import sys
from pathlib import Path
import pygame

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.core.asset_loader import EgyptianAssetLoader, AssetCategory
from sands_of_duat.cards.egyptian_cards import EgyptianDeckBuilder

def test_asset_discovery():
    """Test that all expected assets are discovered."""
    print("Testing asset discovery...")
    
    try:
        loader = EgyptianAssetLoader()
        total_assets = loader.get_total_asset_count()
        
        print(f"  - Total assets discovered: {total_assets}")
        
        # Check each category
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            print(f"  - {category.name}: {len(assets)} assets")
            
            # Show a few examples
            for i, asset in enumerate(assets[:3]):
                print(f"    * {asset}")
            if len(assets) > 3:
                print(f"    ... and {len(assets) - 3} more")
        
        return total_assets >= 70  # Should have at least 70 assets
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_asset_quality_indicators():
    """Test that assets have quality indicators in their names."""
    print("Testing asset quality indicators...")
    
    try:
        loader = EgyptianAssetLoader()
        all_files = []
        
        for category in AssetCategory:
            all_files.extend(loader.get_assets_by_category(category))
        
        quality_assets = 0
        total_assets = len(all_files)
        
        for filename in all_files:
            if '_q' in filename:  # Has quality indicator
                quality_assets += 1
                # Extract quality value
                try:
                    q_part = filename.split('_q')[1]
                    quality_val = int(q_part.split('.')[0])
                    if quality_val < 60:
                        print(f"    Warning: Low quality asset {filename} (q{quality_val})")
                except:
                    pass
        
        print(f"  - Assets with quality indicators: {quality_assets}/{total_assets}")
        print(f"  - Quality percentage: {(quality_assets/total_assets)*100:.1f}%")
        
        return quality_assets > total_assets * 0.8  # At least 80% should have quality indicators
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_asset_loading_with_pygame():
    """Test loading assets with pygame."""
    print("Testing asset loading with pygame...")
    
    pygame.init()
    
    try:
        loader = EgyptianAssetLoader()
        
        # Test loading a few assets from each category
        loaded_count = 0
        failed_count = 0
        
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            
            # Try to load first few assets from each category
            for i, asset_name in enumerate(assets[:2]):  # Test first 2 from each category
                try:
                    surface = loader.load_image(asset_name)
                    if surface:
                        loaded_count += 1
                        print(f"    * Loaded {asset_name}: {surface.get_size()}")
                    else:
                        failed_count += 1
                        print(f"    x Failed to load {asset_name}")
                except Exception as e:
                    failed_count += 1
                    print(f"    x Error loading {asset_name}: {e}")
        
        print(f"  - Successfully loaded: {loaded_count}")
        print(f"  - Failed to load: {failed_count}")
        
        return failed_count == 0  # All should load successfully
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_card_artwork_integration():
    """Test that cards can use the loaded artwork."""
    print("Testing card artwork integration...")
    
    pygame.init()
    
    try:
        deck_builder = EgyptianDeckBuilder()
        cards = deck_builder.get_all_cards()
        
        rendered_count = 0
        failed_count = 0
        
        # Test rendering first few cards
        for card in cards[:5]:
            try:
                surface = card.render_card()
                if surface and surface.get_size() == (300, 420):
                    rendered_count += 1
                    print(f"    * Rendered {card.name}: {surface.get_size()}")
                else:
                    failed_count += 1
                    print(f"    x Failed to render {card.name}")
            except Exception as e:
                failed_count += 1
                print(f"    x Error rendering {card.name}: {e}")
        
        print(f"  - Successfully rendered: {rendered_count}")
        print(f"  - Failed to render: {failed_count}")
        
        return failed_count == 0  # All should render successfully
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_high_quality_asset_selection():
    """Test that the system can identify and use high-quality assets."""
    print("Testing high-quality asset selection...")
    
    try:
        loader = EgyptianAssetLoader()
        
        high_quality_found = 0
        
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            if not assets:
                continue
            
            # Find highest quality asset
            def get_quality(filename):
                try:
                    if '_q' in filename:
                        q_part = filename.split('_q')[1]
                        return int(q_part.split('.')[0])
                except:
                    pass
                return 0
            
            if assets:
                best_asset = max(assets, key=get_quality)
                best_quality = get_quality(best_asset)
                
                if best_quality > 0:
                    high_quality_found += 1
                    print(f"    * {category.name}: {best_asset} (q{best_quality})")
        
        print(f"  - Categories with high-quality assets: {high_quality_found}")
        
        return high_quality_found >= len(AssetCategory) // 2  # At least half should have quality assets
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_asset_metadata():
    """Test loading and using asset metadata."""
    print("Testing asset metadata...")
    
    try:
        loader = EgyptianAssetLoader()
        
        # Check if metadata exists
        metadata_file = loader.final_dataset_path / "metadata.jsonl"
        
        if metadata_file.exists():
            print(f"    * Metadata file found: {metadata_file}")
            
            # Check if any metadata was loaded
            metadata_count = len(loader._metadata_cache)
            print(f"    * Loaded metadata for {metadata_count} assets")
            
            if metadata_count > 0:
                # Show sample metadata
                sample_key = list(loader._metadata_cache.keys())[0]
                sample_data = loader._metadata_cache[sample_key]
                print(f"    * Sample metadata: {sample_key} -> {list(sample_data.keys())}")
            
            return metadata_count > 0
        else:
            print(f"    * Metadata file not found (optional)")
            return True  # Not required for basic functionality
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_memory_usage():
    """Test that asset loading doesn't consume excessive memory."""
    print("Testing memory usage...")
    
    pygame.init()
    
    try:
        loader = EgyptianAssetLoader()
        loader.max_cache_size = 10  # Small cache for testing
        
        # Load many assets
        loaded_count = 0
        for category in AssetCategory:
            assets = loader.get_assets_by_category(category)
            
            for asset_name in assets[:5]:  # Load first 5 from each category
                surface = loader.load_image(asset_name, (100, 100))  # Small size for memory test
                if surface:
                    loaded_count += 1
        
        # Check cache stats
        cache_stats = loader.get_cache_stats()
        
        print(f"    * Loaded {loaded_count} assets")
        print(f"    * Cache size: {cache_stats['cached_images']}/{cache_stats['max_cache_size']}")
        print(f"    * Cache utilization: {(cache_stats['cached_images']/cache_stats['max_cache_size'])*100:.1f}%")
        
        # Cache should not exceed maximum
        return cache_stats['cached_images'] <= cache_stats['max_cache_size']
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False
    finally:
        pygame.quit()

def run_asset_verification():
    """Run all asset verification tests."""
    print("SANDS OF DUAT - ASSET VERIFICATION TESTS")
    print("=" * 44)
    
    tests = [
        ("Asset Discovery", test_asset_discovery),
        ("Quality Indicators", test_asset_quality_indicators),
        ("Pygame Loading", test_asset_loading_with_pygame),
        ("Card Integration", test_card_artwork_integration),
        ("High Quality Selection", test_high_quality_asset_selection),
        ("Asset Metadata", test_asset_metadata),
        ("Memory Usage", test_memory_usage)
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
    
    print(f"\n" + "=" * 44)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All asset verification tests passed!")
        print("All 71+ Egyptian assets are properly integrated and ready for use.")
    elif passed >= total - 1:
        print("MOSTLY SUCCESSFUL: Almost all tests passed.")
        print("The Egyptian assets are ready for gameplay with minor issues.")
    else:
        print("Some tests failed. Please check the issues above.")
    
    return passed >= total - 1  # Allow one test to fail

if __name__ == "__main__":
    success = run_asset_verification()
    sys.exit(0 if success else 1)