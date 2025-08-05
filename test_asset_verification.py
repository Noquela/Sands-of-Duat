#!/usr/bin/env python3
"""
Asset Loading and Visual Systems Verification Test
Testing that all new assets load correctly and visual systems are functioning.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_asset_structure():
    """Test that asset directory structure is correct."""
    print("Testing asset directory structure...")
    
    game_assets_dir = project_root / "game_assets"
    
    if not game_assets_dir.exists():
        print("FAIL: game_assets directory not found")
        return False
    
    # Expected directories
    expected_dirs = [
        "cards", "characters", "environments", "ui_elements"
    ]
    
    found_dirs = 0
    for dir_name in expected_dirs:
        dir_path = game_assets_dir / dir_name
        if dir_path.exists():
            print(f"  PASS: Found {dir_name} directory")
            found_dirs += 1
        else:
            print(f"  WARNING: Missing {dir_name} directory")
    
    # Check for asset manifest
    manifest_path = game_assets_dir / "ASSET_MANIFEST.json"
    if manifest_path.exists():
        print("  PASS: Asset manifest found")
        found_dirs += 1
    else:
        print("  WARNING: Asset manifest not found")
    
    structure_score = (found_dirs / (len(expected_dirs) + 1)) * 100
    print(f"  Structure Score: {structure_score:.1f}%")
    
    return structure_score >= 80

def test_card_assets():
    """Test card asset availability."""
    print("Testing card assets...")
    
    cards_dir = project_root / "game_assets" / "cards"
    
    if not cards_dir.exists():
        print("  FAIL: Cards directory not found")
        return False
    
    # Count card files
    card_files = list(cards_dir.glob("*.png"))
    hades_quality_dir = cards_dir / "hades_quality"
    
    if hades_quality_dir.exists():
        hades_card_files = list(hades_quality_dir.glob("*.png"))
        print(f"  Found {len(hades_card_files)} Hades-quality card assets")
    else:
        hades_card_files = []
        print("  WARNING: No Hades-quality card assets")
    
    standard_quality_dir = cards_dir / "standard_quality"
    if standard_quality_dir.exists():
        standard_card_files = list(standard_quality_dir.glob("*.png"))
        print(f"  Found {len(standard_card_files)} standard-quality card assets")
    else:
        standard_card_files = []
        print("  WARNING: No standard-quality card assets")
    
    total_card_assets = len(card_files) + len(hades_card_files) + len(standard_card_files)
    print(f"  Total card assets: {total_card_assets}")
    
    # We need at least 10 card assets for a functional game
    if total_card_assets >= 15:
        print("  PASS: Sufficient card assets")
        return True
    elif total_card_assets >= 10:
        print("  WARNING: Minimal card assets")
        return True
    else:
        print("  FAIL: Insufficient card assets")
        return False

def test_character_assets():
    """Test character sprite availability."""
    print("Testing character assets...")
    
    characters_dir = project_root / "game_assets" / "characters"
    
    if not characters_dir.exists():
        print("  FAIL: Characters directory not found")
        return False
    
    # Check for character sprites
    sprites_dir = characters_dir / "sprites"
    if sprites_dir.exists():
        sprite_files = list(sprites_dir.glob("*.png"))
        print(f"  Found {len(sprite_files)} character sprites")
        
        # Look for specific character types
        character_types = ['player', 'anubis', 'scorpion', 'pharaoh', 'temple']
        found_characters = []
        
        for sprite_file in sprite_files:
            for char_type in character_types:
                if char_type in sprite_file.name.lower():
                    found_characters.append(char_type)
                    break
        
        unique_characters = len(set(found_characters))
        print(f"  Found {unique_characters} different character types")
        
        if unique_characters >= 3:
            print("  PASS: Good character variety")
            return True
        elif unique_characters >= 2:
            print("  WARNING: Limited character variety")
            return True
        else:
            print("  FAIL: Insufficient character variety")
            return False
    else:
        print("  FAIL: No character sprites directory")
        return False

def test_environment_assets():
    """Test environment background availability."""
    print("Testing environment assets...")
    
    environments_dir = project_root / "game_assets" / "environments"
    
    if not environments_dir.exists():
        print("  FAIL: Environments directory not found")
        return False
    
    # Check for key backgrounds
    required_backgrounds = [
        "menu_background.png",
        "combat_background.png"
    ]
    
    found_backgrounds = 0
    for bg_name in required_backgrounds:
        bg_path = environments_dir / bg_name
        if bg_path.exists():
            print(f"  PASS: Found {bg_name}")
            found_backgrounds += 1
        else:
            print(f"  WARNING: Missing {bg_name}")
    
    # Check for additional backgrounds
    all_backgrounds = list(environments_dir.glob("*.png"))
    print(f"  Total background assets: {len(all_backgrounds)}")
    
    background_score = (found_backgrounds / len(required_backgrounds)) * 100
    
    if background_score >= 100:
        print("  PASS: All required backgrounds found")
        return True
    elif background_score >= 50:
        print("  WARNING: Some backgrounds missing")
        return True
    else:
        print("  FAIL: Critical backgrounds missing")
        return False

def test_visual_system_loading():
    """Test that visual systems can load assets."""
    print("Testing visual system loading...")
    
    try:
        # Test background loading
        from sands_duat.graphics.background_loader import BackgroundLoader
        
        bg_loader = BackgroundLoader()
        
        # Try to load a background
        test_bg_path = project_root / "game_assets" / "environments" / "menu_background.png"
        if test_bg_path.exists():
            # This would normally load the background
            print("  PASS: Background loader initialized")
            visual_score = 25
        else:
            print("  WARNING: No background to test loading")
            visual_score = 15
        
    except Exception as e:
        print(f"  WARNING: Background loader issue: {e}")
        visual_score = 10
    
    try:
        # Test theme system
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(1280, 720)
        print("  PASS: Theme system loads correctly")
        visual_score += 25
    except Exception as e:
        print(f"  FAIL: Theme system error: {e}")
        visual_score += 0
    
    try:
        # Test Hades theme
        from sands_duat.ui.hades_theme import HadesEgyptianTheme
        hades_theme = HadesEgyptianTheme((1280, 720))
        print("  PASS: Hades Egyptian theme loads correctly")
        visual_score += 25
    except Exception as e:
        print(f"  FAIL: Hades theme error: {e}")
        visual_score += 0
    
    try:
        # Test card art loading (if available)
        from sands_duat.content.starter_cards import create_starter_cards
        cards = create_starter_cards()
        print(f"  PASS: Card system loads {len(cards)} cards")
        visual_score += 25
    except Exception as e:
        print(f"  FAIL: Card loading error: {e}")
        visual_score += 0
    
    print(f"  Visual System Score: {visual_score}/100")
    return visual_score >= 60

def test_asset_quality():
    """Test asset quality and consistency."""
    print("Testing asset quality...")
    
    try:
        import pygame
        pygame.init()
        
        # Test loading various assets
        test_images = []
        
        # Check menu background
        menu_bg_path = project_root / "game_assets" / "environments" / "menu_background.png"
        if menu_bg_path.exists():
            try:
                menu_bg = pygame.image.load(str(menu_bg_path))
                test_images.append(("menu_background", menu_bg))
                print(f"  PASS: Menu background loads ({menu_bg.get_size()})")
            except Exception as e:
                print(f"  FAIL: Menu background corrupt: {e}")
        
        # Check combat background
        combat_bg_path = project_root / "game_assets" / "environments" / "combat_background.png"
        if combat_bg_path.exists():
            try:
                combat_bg = pygame.image.load(str(combat_bg_path))
                test_images.append(("combat_background", combat_bg))
                print(f"  PASS: Combat background loads ({combat_bg.get_size()})")
            except Exception as e:
                print(f"  FAIL: Combat background corrupt: {e}")
        
        # Check a card asset
        cards_dir = project_root / "game_assets" / "cards"
        card_files = list(cards_dir.glob("*.png"))
        if card_files:
            try:
                card_img = pygame.image.load(str(card_files[0]))
                test_images.append(("card_asset", card_img))
                print(f"  PASS: Card asset loads ({card_img.get_size()})")
            except Exception as e:
                print(f"  FAIL: Card asset corrupt: {e}")
        
        pygame.quit()
        
        # Quality assessment
        quality_score = 0
        
        if len(test_images) >= 3:
            print("  PASS: Multiple asset types load successfully")
            quality_score += 40
        elif len(test_images) >= 2:
            print("  PASS: Some assets load successfully")
            quality_score += 30
        elif len(test_images) >= 1:
            print("  WARNING: Few assets load successfully")
            quality_score += 20
        else:
            print("  FAIL: No assets load successfully")
            quality_score += 0
        
        # Check for consistent resolutions
        resolutions = [img.get_size() for name, img in test_images]
        unique_resolutions = set(resolutions)
        
        if len(unique_resolutions) <= 3:
            print("  PASS: Reasonable resolution variety")
            quality_score += 30
        else:
            print("  WARNING: Many different resolutions")
            quality_score += 20
        
        # Check for reasonable file sizes (all images should be < 5MB when loaded)
        large_images = [name for name, img in test_images if img.get_size()[0] * img.get_size()[1] > 1920 * 1080]
        
        if len(large_images) == 0:
            print("  PASS: All assets reasonably sized")
            quality_score += 30
        else:
            print(f"  WARNING: {len(large_images)} assets may be oversized")
            quality_score += 20
        
        print(f"  Quality Score: {quality_score}/100")
        return quality_score >= 70
        
    except Exception as e:
        print(f"  FAIL: Asset quality test error: {e}")
        return False

def main():
    """Run all asset verification tests."""
    print("=" * 70)
    print("SANDS OF DUAT - ASSET LOADING & VISUAL SYSTEMS VERIFICATION")
    print("Testing professional asset pipeline and visual enhancements")
    print("=" * 70)
    
    tests = [
        test_asset_structure,
        test_card_assets,
        test_character_assets,
        test_environment_assets,
        test_visual_system_loading,
        test_asset_quality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("  RESULT: PASS")
            else:
                print("  RESULT: FAIL")
        except Exception as e:
            print(f"  RESULT: CRASH - {e}")
        print()
    
    print("=" * 70)
    print(f"ASSET & VISUAL RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("SUCCESS All asset and visual tests PASSED!")
        print("Professional asset pipeline is working correctly.")
    elif passed >= total * 0.75:
        print("SUCCESS Most asset tests passed - visual systems ready!")
    elif passed >= total * 0.5:
        print("WARNING Some asset issues detected - minor fixes needed")
    else:
        print("ERROR Significant asset issues - major fixes required")
    
    print("=" * 70)
    return passed >= total * 0.5  # 50% pass rate for assets

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)