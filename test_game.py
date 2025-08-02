#!/usr/bin/env python3
"""
Quick test script for Sands of Duat
Tests basic functionality without opening a window
"""

import sys
import os

# Add src to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ecs_imports():
    """Test that ECS modules can be imported."""
    try:
        from ecs import EntityManager, create_player_entity
        from ecs.components import Transform, SpriteRenderer, InputController
        from ecs.systems import InputSystem, MovementSystem
        print("ECS modules imported successfully")
        return True
    except ImportError as e:
        print(f"Failed to import ECS modules: {e}")
        return False

def test_entity_creation():
    """Test entity creation and component assignment."""
    try:
        from ecs import EntityManager, create_player_entity
        from ecs.components import Transform, SpriteRenderer
        
        entity_manager = EntityManager()
        player_id = create_player_entity(entity_manager, 100, 200)
        
        # Check if components were added
        transform = entity_manager.get_component(player_id, Transform)
        sprite = entity_manager.get_component(player_id, SpriteRenderer)
        
        assert transform is not None, "Transform component missing"
        assert sprite is not None, "SpriteRenderer component missing"
        assert transform.x == 100, f"Expected x=100, got {transform.x}"
        assert transform.y == 200, f"Expected y=200, got {transform.y}"
        
        print("Entity creation and components working")
        return True
    except Exception as e:
        print(f"Entity creation failed: {e}")
        return False

def test_asset_manager():
    """Test asset manager functionality."""
    try:
        import pygame
        pygame.init()
        
        from assets import AssetManager
        
        asset_manager = AssetManager()
        placeholder = asset_manager.create_placeholder_sprite(64, 64, "test")
        
        assert placeholder.get_width() == 64, "Wrong sprite width"
        assert placeholder.get_height() == 64, "Wrong sprite height"
        
        print("Asset manager working")
        return True
    except Exception as e:
        print(f"Asset manager failed: {e}")
        return False

def test_systems():
    """Test ECS systems initialization."""
    try:
        import pygame
        pygame.init()
        
        from ecs import EntityManager
        from ecs.systems import InputSystem, MovementSystem, AnimationSystem
        
        entity_manager = EntityManager()
        screen = pygame.Surface((800, 600))
        
        systems = [
            InputSystem(entity_manager),
            MovementSystem(entity_manager),
            AnimationSystem(entity_manager)
        ]
        
        # Test system updates (should not crash)
        for system in systems:
            system.update(0.016)  # 60 FPS delta
        
        print("ECS systems working")
        return True
    except Exception as e:
        print(f"ECS systems failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Sands of Duat components...")
    print()
    
    tests = [
        test_ecs_imports,
        test_entity_creation,
        test_asset_manager,
        test_systems
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("All tests passed! The game should run correctly.")
        return 0
    else:
        print("Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())