#!/usr/bin/env python3
"""
Basic functionality test for Sands of Duat
Testing core systems to ensure they work properly after recent changes.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_card_system():
    """Test that card system works."""
    print("Testing card system...")
    try:
        from sands_duat.content.starter_cards import create_starter_cards
        cards = create_starter_cards()
        print(f"PASS Card system works: loaded {len(cards)} cards")
        return True
    except Exception as e:
        print(f"FAIL Card system error: {e}")
        return False

def test_hourglass_system():
    """Test HourGlass functionality."""
    print("Testing HourGlass system...")
    try:
        from sands_duat.core.hourglass import HourGlass
        hourglass = HourGlass()
        hourglass.set_sand(5)
        initial_sand = hourglass.current_sand
        spent = hourglass.spend_sand(2)
        final_sand = hourglass.current_sand
        
        if spent and initial_sand == 5 and final_sand == 3:
            print("PASS HourGlass system works correctly")
            return True
        else:
            print(f"FAIL HourGlass logic error: {initial_sand} -> {final_sand}, spent: {spent}")
            return False
    except Exception as e:
        print(f"FAIL HourGlass system error: {e}")
        return False

def test_theme_system():
    """Test theme initialization."""
    print("Testing theme system...")
    try:
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(1280, 720)
        print(f"PASS Theme system works: {theme.display.display_mode}")
        return True
    except Exception as e:
        print(f"FAIL Theme system error: {e}")
        return False

def test_save_system():
    """Test save system creation."""
    print("Testing save system...")
    try:
        from sands_duat.core.save_system import SaveSystem
        save_system = SaveSystem()
        print("PASS Save system initializes correctly")
        return True
    except Exception as e:
        print(f"FAIL Save system error: {e}")
        return False

def test_audio_system():
    """Test audio manager."""
    print("Testing audio system...")
    try:
        from sands_duat.audio.audio_manager import AudioManager
        audio_manager = AudioManager()
        print("PASS Audio system initializes correctly")
        return True
    except Exception as e:
        print(f"FAIL Audio system error: {e}")
        return False

def test_asset_loading():
    """Test that key assets exist."""
    print("Testing asset availability...")
    try:
        from sands_duat.content.egyptian_card_loader import EgyptianCardLoader
        loader = EgyptianCardLoader()
        cards = loader.load_cards()
        print(f"PASS Asset loading works: {len(cards)} Egyptian cards loaded")
        return True
    except Exception as e:
        print(f"FAIL Asset loading error: {e}")
        return False

def main():
    """Run all basic functionality tests."""
    print("=" * 60)
    print("SANDS OF DUAT - BASIC FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        test_card_system,
        test_hourglass_system,
        test_theme_system,
        test_save_system,
        test_audio_system,
        test_asset_loading
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"CRASH Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("SUCCESS All basic functionality tests PASSED!")
        print("The game core systems are working correctly.")
    elif passed >= total * 0.8:
        print("WARNING Most tests passed - minor issues detected")
    elif passed >= total * 0.5:
        print("WARNING Some tests failed - significant issues detected")
    else:
        print("ERROR Many tests failed - critical issues detected")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)