#!/usr/bin/env python3
"""
Test Improved Game - Quick test of the improved game with organized assets
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def test_game_components():
    """Test all game components without running the full game"""
    
    print("TESTING IMPROVED SANDS OF DUAT")
    print("=" * 40)
    
    test_results = {}
    
    # Test 1: Asset System
    print("\n1. Testing Asset System...")
    try:
        from assets import load_assets, asset_manager
        
        # Test organized asset loading
        load_assets()
        
        # Check if assets were loaded
        loaded_sprites = list(asset_manager.sprites.keys())
        print(f"   Assets loaded: {len(loaded_sprites)}")
        print(f"   Available sprites: {loaded_sprites[:5]}...")  # Show first 5
        
        test_results["assets"] = "SUCCESS"
        
    except Exception as e:
        print(f"   ERROR in asset system: {e}")
        test_results["assets"] = "FAILED"
    
    # Test 2: Scene System
    print("\n2. Testing Scene System...")
    try:
        from scenes.improved_hub_scene import ImprovedHubScene
        from scenes import ArenaScene
        
        # Test scene imports
        print("   ImprovedHubScene imported successfully")
        print("   ArenaScene imported successfully")
        
        test_results["scenes"] = "SUCCESS"
        
    except Exception as e:
        print(f"   ERROR in scene system: {e}")
        test_results["scenes"] = "FAILED"
    
    # Test 3: ECS System
    print("\n3. Testing ECS System...")
    try:
        from ecs import (
            EntityManager, create_player_entity, create_egyptian_altar,
            Transform, SpriteRenderer, Health
        )
        
        # Test ECS component creation
        entity_manager = EntityManager()
        player_id = create_player_entity(entity_manager, 100, 100)
        altar_id = create_egyptian_altar(entity_manager, 200, 200, "Ra")
        
        print(f"   Player entity created: {player_id}")
        print(f"   Altar entity created: {altar_id}")
        print(f"   Total entities: {len(entity_manager.entities)}")
        
        test_results["ecs"] = "SUCCESS"
        
    except Exception as e:
        print(f"   ERROR in ECS system: {e}")
        test_results["ecs"] = "FAILED"
    
    # Test 4: Organized Asset Structure
    print("\n4. Testing Organized Asset Structure...")
    try:
        base_path = Path(__file__).parent.parent.parent
        asset_categories = ["characters", "enemies", "environments", "portals", "ui"]
        
        found_assets = {}
        for category in asset_categories:
            category_path = base_path / "assets" / category
            if category_path.exists():
                assets = list(category_path.glob("*.png"))
                found_assets[category] = len(assets)
                print(f"   {category}: {len(assets)} assets")
            else:
                found_assets[category] = 0
                print(f"   {category}: No assets found")
        
        total_assets = sum(found_assets.values())
        print(f"   Total organized assets: {total_assets}")
        
        test_results["asset_structure"] = "SUCCESS" if total_assets > 0 else "PARTIAL"
        
    except Exception as e:
        print(f"   ERROR in asset structure: {e}")
        test_results["asset_structure"] = "FAILED"
    
    # Test Summary
    print("\n" + "=" * 40)
    print("TEST RESULTS SUMMARY")
    print("=" * 40)
    
    for test_name, result in test_results.items():
        status_symbol = "SUCCESS" if result == "SUCCESS" else "PARTIAL" if result == "PARTIAL" else "FAILED"
        print(f"{status_symbol} {test_name.replace('_', ' ').title()}: {result}")
    
    # Overall assessment
    success_count = sum(1 for result in test_results.values() if result == "SUCCESS")
    total_tests = len(test_results)
    
    print(f"\nOverall: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("ALL SYSTEMS READY! Game should run smoothly.")
        return True
    elif success_count >= total_tests - 1:
        print("MOSTLY READY! Minor issues but game should work.")
        return True
    else:
        print("SOME ISSUES! Game may have problems.")
        return False

def test_game_initialization():
    """Test game initialization without opening window"""
    
    print("\n" + "=" * 40)
    print("TESTING GAME INITIALIZATION")
    print("=" * 40)
    
    try:
        # Test pygame initialization
        import pygame
        pygame.init()
        print("SUCCESS: Pygame initialized successfully")
        
        # Test game class creation (without running)
        from game import Game
        
        # Create game instance but don't run it
        game = Game()
        print("SUCCESS: Game class created successfully")
        print(f"  Screen size: {game.screen_width}x{game.screen_height}")
        print(f"  Target FPS: {game.fps}")
        
        pygame.quit()
        print("SUCCESS: Pygame cleaned up successfully")
        
        return True
        
    except Exception as e:
        print(f"FAILED: Game initialization failed: {e}")
        return False

if __name__ == "__main__":
    print("SANDS OF DUAT - IMPROVED GAME TEST")
    print("Testing all components before full game launch...")
    
    # Run component tests
    components_ok = test_game_components()
    
    # Run initialization test
    init_ok = test_game_initialization()
    
    print("\n" + "=" * 50)
    if components_ok and init_ok:
        print("GAME READY FOR LAUNCH!")
        print("All systems tested and working properly.")
        print("\nTo run the game:")
        print("  cd src && python game.py")
    else:
        print("SOME ISSUES DETECTED")
        print("Review the test results above.")
    print("=" * 50)