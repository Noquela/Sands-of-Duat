#!/usr/bin/env python3
"""
Simple test to verify the core menu button fix.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_ui_manager_screen_access():
    """Test that UI manager screen access works correctly."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.ui.menu_screen import MenuScreen
        
        surface = pygame.display.set_mode((100, 100))
        ui_manager = UIManager(surface)
        
        # Verify ui_manager has screens dict
        assert hasattr(ui_manager, 'screens'), "UI manager should have screens attribute"
        assert isinstance(ui_manager.screens, dict), "screens should be a dictionary"
        
        # Create and add a menu screen
        menu_screen = MenuScreen()
        ui_manager.add_screen(menu_screen)
        
        # Test the specific access pattern that was failing
        screen_by_dict = ui_manager.screens.get("menu")
        
        assert screen_by_dict is not None, "Should be able to access screen via screens dict"
        assert screen_by_dict == menu_screen, "Should get the same screen object"
        
        print("[PASS] UI manager screen access working correctly")
        print(f"[PASS] Available screens: {list(ui_manager.screens.keys())}")
        
        # Test that the pattern used in the fix works
        test_screen = ui_manager.screens.get("tutorial")  # Should return None gracefully
        assert test_screen is None, "Non-existent screen should return None"
        print("[PASS] Non-existent screen access returns None correctly")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] UI manager test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing core menu fix...")
    print("=" * 50)
    
    success = test_ui_manager_screen_access()
    
    print("=" * 50)
    if success:
        print("[SUCCESS] Menu fix is working correctly!")
        print("The ui_manager.screens.get() pattern is now working.")
        print("Game should no longer crash on 'New Game' button click.")
        sys.exit(0)
    else:
        print("[FAIL] Menu fix test failed")
        sys.exit(1)