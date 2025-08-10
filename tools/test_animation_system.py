#!/usr/bin/env python3
"""
Test Script - Animation System without GPU Requirements
Tests the animation integration without requiring ComfyUI or actual art generation
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root / "src"))

def create_test_animations():
    """Create test animation assets for testing."""
    
    # Create directory structure
    test_dirs = [
        "assets/approved_hades_quality/animated_cards",
        "assets/compressed_sprites/cards",
        "assets/generated_animations/cards"
    ]
    
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create dummy spritesheet metadata for testing
    test_cards = [
        'anubis_-_judgment_anim.png',
        'egyptian_warrior_anim.png', 
        'mummy_guardian_anim.png',
        'sphinx_guardian_anim.png'
    ]
    
    for card_filename in test_cards:
        # Create dummy metadata
        metadata = {
            "frame_count": 8,
            "frame_size": [300, 420],
            "sheet_size": [1200, 840],
            "cols": 4,
            "rows": 2,
            "fps": 12,
            "loop": True,
            "compressed": False
        }
        
        # Save metadata file
        metadata_path = Path("assets/approved_hades_quality/animated_cards") / card_filename.replace('.png', '.json')
        with open(metadata_path, 'w') as f:
            import json
            json.dump(metadata, f, indent=2)
        
        print(f"Created test metadata for {card_filename}")

def test_asset_loader():
    """Test the enhanced asset loader."""
    
    try:
        from sands_of_duat.core.asset_loader import get_asset_loader
        
        print("\nTesting Enhanced Asset Loader...")
        
        asset_loader = get_asset_loader()
        
        # Test animated card mappings
        animated_cards = asset_loader.get_all_animated_cards()
        print(f"Found {len(animated_cards)} animated card mappings")
        
        for card_name in animated_cards[:3]:  # Test first 3
            animation_info = asset_loader.get_animation_info(card_name)
            if animation_info:
                print(f"  - {card_name}: {animation_info.get('frame_count', 0)} frames")
            else:
                print(f"  - {card_name}: Animation info not found (expected for test)")
        
        # Test cache stats
        cache_stats = asset_loader.get_cache_stats()
        print(f"Cache Stats: {cache_stats}")
        
        # Test animation update (should not crash)
        asset_loader.update_animations(16.67)  # 60 FPS delta time
        print("Animation update successful")
        
        return True
        
    except Exception as e:
        print(f"Asset Loader Test Failed: {e}")
        return False

def test_combat_integration():
    """Test that combat system can handle animations."""
    
    try:
        # Import required modules
        import pygame
        pygame.init()
        
        # Set up minimal display for testing
        test_surface = pygame.Surface((800, 600))
        
        from sands_of_duat.ui.screens.professional_combat import ProfessionalCombat
        
        print("\nTesting Combat Animation Integration...")
        
        # Create combat instance
        combat = ProfessionalCombat()
        
        # Test that asset_loader was initialized
        if hasattr(combat, 'asset_loader'):
            print("Combat system has asset loader")
            
            # Test update with animation
            combat.update(0.016, [], (400, 300), False)  # 60 FPS
            print("Combat update with animations successful")
            
        else:
            print("Combat system missing asset loader")
            return False
        
        return True
        
    except Exception as e:
        print(f"Combat Integration Test Failed: {e}")
        return False

def test_quality_validator():
    """Test quality validation system."""
    
    try:
        sys.path.append(str(project_root / "tools"))
        from quality_validator import RTX5070QualityValidator, QualityMetrics
        
        print("\nTesting Quality Validation System...")
        
        validator = RTX5070QualityValidator()
        
        # Test metrics creation
        test_metrics = QualityMetrics(
            color_vibrancy=0.8,
            contrast_ratio=0.75,
            detail_complexity=0.9,
            egyptian_authenticity=0.85,
            animation_smoothness=0.7,
            overall_score=0.8
        )
        
        metrics_dict = test_metrics.to_dict()
        print(f"Quality metrics structure: {len(metrics_dict)} metrics")
        
        # Test cache stats don't crash
        cache_stats = validator.get_cache_stats()
        print(f"Validator initialized: {cache_stats}")
        
        return True
        
    except Exception as e:
        print(f"Quality Validator Test Failed: {e}")
        return False

def main():
    """Run animation system tests."""
    
    print("=" * 50)
    print("   ANIMATION SYSTEM TESTING")
    print("   (No GPU Required)")
    print("=" * 50)
    
    # Create test environment
    print("Setting up test environment...")
    create_test_animations()
    
    # Run tests
    tests = [
        ("Asset Loader", test_asset_loader),
        ("Combat Integration", test_combat_integration), 
        ("Quality Validator", test_quality_validator)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test...")
        print(f"{'='*50}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"[PASSED] {test_name} test")
            else:
                print(f"[FAILED] {test_name} test")
                
        except Exception as e:
            print(f"[CRASHED] {test_name} test: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "[PASSED]" if success else "[FAILED]"
        print(f"{test_name:.<30} {status}")
    
    success_rate = (passed / total) * 100
    print(f"\nOverall Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    if success_rate == 100:
        print("\nALL TESTS PASSED!")
        print("Animation system is ready for integration!")
        print("\nNext Steps:")
        print("- Run actual art generation with: python run_animation_pipeline.py")
        print("- Test in-game: python main.py (combat mode)")
    elif success_rate >= 75:
        print("\nMOSTLY SUCCESSFUL!")
        print("Core systems are working. Some features may need attention.")
    else:
        print("\nMULTIPLE FAILURES")
        print("Review error messages above and fix issues before proceeding.")
    
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)