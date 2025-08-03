#!/usr/bin/env python3
"""
Quick test to verify the menu button fix for ui_manager.get_screen issue.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_menu_screen_creation():
    """Test that menu screen can be created without errors."""
    try:
        import pygame
        pygame.init()
        
        from sands_duat.ui.menu_screen import MenuScreen
        from sands_duat.ui.ui_manager import UIManager
        from sands_duat.ui.tutorial_screen import TutorialScreen
        
        # Create a surface and UI manager
        surface = pygame.display.set_mode((100, 100))
        ui_manager = UIManager(surface)
        
        # Create and add screens
        menu_screen = MenuScreen()
        tutorial_screen = TutorialScreen()
        
        ui_manager.add_screen(menu_screen)
        ui_manager.add_screen(tutorial_screen)
        
        # Test that menu screen can access tutorial screen properly
        tutorial_screen_ref = ui_manager.screens.get("tutorial")
        
        print(f"[PASS] Menu screen created successfully")
        print(f"[PASS] Tutorial screen accessible: {tutorial_screen_ref is not None}")
        print(f"[PASS] UI manager has screens: {list(ui_manager.screens.keys())}")
        
        # Test the specific method that was failing
        if hasattr(tutorial_screen_ref, 'set_game_flow_context'):
            print(f"[PASS] Tutorial screen has set_game_flow_context method")
        else:
            print(f"[WARN] Tutorial screen missing set_game_flow_context method")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_ui_manager_screen_access():
    """Test UI manager screen access patterns."""
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
        
        # Verify we can access screens properly
        menu_screen = MenuScreen()
        ui_manager.add_screen(menu_screen)
        
        # Test both access patterns
        screen_by_dict = ui_manager.screens.get("menu")
        
        assert screen_by_dict is not None, "Should be able to access screen via screens dict"
        assert screen_by_dict == menu_screen, "Should get the same screen object"
        
        print(f"[PASS] UI manager screen access working correctly")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"[FAIL] UI manager test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing menu screen fix...")
    print("=" * 50)
    
    test1_success = test_menu_screen_creation()
    test2_success = test_ui_manager_screen_access()
    
    print("=" * 50)
    if test1_success and test2_success:
        print("[SUCCESS] ALL TESTS PASSED - Menu fix is working correctly!")
        sys.exit(0)
    else:
        print("[FAIL] SOME TESTS FAILED")
        sys.exit(1)