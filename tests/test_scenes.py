#!/usr/bin/env python3
"""
Scene system test for Sands of Duat
Tests Hub and Arena scene functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def test_scene_imports():
    """Test that scene modules can be imported."""
    try:
        from scenes import SceneManager, HubScene, ArenaScene
        print("Scene modules imported successfully")
        return True
    except ImportError as e:
        print(f"Failed to import scene modules: {e}")
        return False

def test_scene_creation():
    """Test scene creation and initialization."""
    try:
        import pygame
        pygame.init()
        
        from scenes import SceneManager, HubScene, ArenaScene
        
        # Mock game object
        class MockGame:
            def __init__(self):
                self.screen = pygame.Surface((1920, 1080))
        
        game = MockGame()
        scene_manager = SceneManager(game)
        
        # Create scenes
        hub_scene = HubScene(game)
        arena_scene = ArenaScene(game)
        
        # Register scenes
        scene_manager.register_scene("hub", hub_scene)
        scene_manager.register_scene("arena", arena_scene)
        
        # Test transition
        success = scene_manager.transition_to("hub")
        assert success, "Failed to transition to hub scene"
        
        current_scene = scene_manager.get_current_scene_name()
        assert current_scene == "hub", f"Expected 'hub', got '{current_scene}'"
        
        print("Scene creation and transition working")
        return True
        
    except Exception as e:
        print(f"Scene creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_artifact_components():
    """Test artifact system components."""
    try:
        from ecs.components import Artifact, ArtifactInventory, Stats
        
        # Test artifact creation
        artifact = Artifact(
            name="Blessing of Ra",
            description="Increases damage by 25%",
            rarity="rare",
            effects={"damage_multiplier": 1.25},
            god_source="Ra"
        )
        
        assert artifact.name == "Blessing of Ra"
        assert artifact.effects["damage_multiplier"] == 1.25
        
        # Test inventory
        inventory = ArtifactInventory()
        success = inventory.add_artifact("Blessing of Ra")
        assert success, "Failed to add artifact to inventory"
        assert "Blessing of Ra" in inventory.equipped_artifacts
        
        # Test stats
        stats = Stats()
        assert stats.get_total_damage() == 25.0  # base_damage * damage_multiplier
        
        print("Artifact components working")
        return True
        
    except Exception as e:
        print(f"Artifact components test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run scene tests."""
    print("Testing Sands of Duat scene system...")
    print()
    
    tests = [
        test_scene_imports,
        test_scene_creation,
        test_artifact_components
    ]
    
    passed = 0
    for test in tests:
        print(f"Running {test.__name__}...")
        if test():
            passed += 1
            print("PASSED")
        else:
            print("FAILED")
        print()
    
    print(f"Scene tests: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("All scene tests passed! Hub/Arena system is working.")
        return 0
    else:
        print("Some scene tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())