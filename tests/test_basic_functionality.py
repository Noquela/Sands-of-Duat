#!/usr/bin/env python3
"""
SANDS OF DUAT - BASIC FUNCTIONALITY TESTS
=========================================

Basic tests to verify the Egyptian card game integration works.
"""

import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from sands_of_duat.core.asset_loader import EgyptianAssetLoader, AssetCategory
        print("  - Asset loader: OK")
        
        from sands_of_duat.cards.egyptian_cards import EgyptianCard, CardType, EgyptianDeckBuilder
        print("  - Card system: OK")
        
        from sands_of_duat.ui.game_interface import SandsOfDuatGame, GameState
        print("  - Game interface: OK")
        
        return True
    except ImportError as e:
        print(f"  - Import failed: {e}")
        return False

def test_asset_categories():
    """Test that asset categories are properly defined."""
    print("Testing asset categories...")
    
    try:
        from sands_of_duat.core.asset_loader import AssetCategory
        
        categories = list(AssetCategory)
        print(f"  - Found {len(categories)} asset categories")
        
        expected_categories = ['GODS', 'ARTIFACTS', 'OBJECTS', 'MYTHS', 'STYLES']
        found_categories = [cat.name for cat in categories]
        
        for expected in expected_categories:
            if expected in found_categories:
                print(f"    * {expected}: OK")
            else:
                print(f"    * {expected}: MISSING")
                return False
        
        return True
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_card_types():
    """Test that card types are properly defined."""
    print("Testing card types...")
    
    try:
        from sands_of_duat.cards.egyptian_cards import CardType, CardRarity
        
        card_types = list(CardType)
        rarities = list(CardRarity)
        
        print(f"  - Found {len(card_types)} card types")
        print(f"  - Found {len(rarities)} rarity levels")
        
        expected_types = ['GOD', 'ARTIFACT', 'SPELL', 'LOCATION', 'CREATURE']
        found_types = [ct.name for ct in card_types]
        
        for expected in expected_types:
            if expected in found_types:
                print(f"    * {expected}: OK")
            else:
                print(f"    * {expected}: MISSING")
                return False
        
        return True
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_deck_builder_creation():
    """Test that deck builder can be created."""
    print("Testing deck builder...")
    
    try:
        # Mock the asset loader to avoid file dependencies
        import unittest.mock
        
        with unittest.mock.patch('sands_of_duat.core.asset_loader.get_asset_loader'):
            from sands_of_duat.cards.egyptian_cards import EgyptianDeckBuilder
            
            builder = EgyptianDeckBuilder()
            cards = builder.get_all_cards()
            
            print(f"  - Created deck builder: OK")
            print(f"  - Generated {len(cards)} cards")
            
            if len(cards) > 0:
                print(f"  - Sample card: {cards[0].name}")
                return True
            else:
                print("  - No cards generated")
                return False
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_asset_paths():
    """Test that asset paths are correctly configured."""
    print("Testing asset paths...")
    
    try:
        assets_path = PROJECT_ROOT / "assets" / "images" / "lora_training" / "final_dataset"
        
        print(f"  - Assets path: {assets_path}")
        
        if assets_path.exists():
            png_files = list(assets_path.glob("*.png"))
            print(f"  - Found {len(png_files)} PNG files")
            
            if len(png_files) > 0:
                print(f"  - Sample asset: {png_files[0].name}")
                return len(png_files) >= 70  # Should have around 71 assets
            else:
                print("  - No PNG assets found")
                return False
        else:
            print("  - Assets directory not found")
            return False
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def run_basic_tests():
    """Run all basic functionality tests."""
    print("SANDS OF DUAT - BASIC FUNCTIONALITY TESTS")
    print("=" * 45)
    
    tests = [
        ("Module Imports", test_imports),
        ("Asset Categories", test_asset_categories),
        ("Card Types", test_card_types),
        ("Deck Builder", test_deck_builder_creation),
        ("Asset Paths", test_asset_paths)
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
    
    print(f"\n" + "=" * 45)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All basic functionality tests passed!")
        print("The Sands of Duat system is ready for gameplay.")
    else:
        print("Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)