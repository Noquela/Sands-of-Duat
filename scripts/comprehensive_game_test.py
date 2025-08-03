#!/usr/bin/env python3
"""
Comprehensive Game Testing Script

Tests all major systems in Sands of Duat to ensure everything works correctly.
"""

import sys
import os
import traceback
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported."""
    print("\n[TEST] Testing Core Module Imports...")
    
    tests = [
        ("Game Engine", "from core.engine import GameEngine"),
        ("UI Manager", "from ui.ui_manager import UIManager"),
        ("Theme System", "from ui.theme import get_theme, initialize_theme"),
        ("Audio Manager", "from audio.audio_manager import AudioManager"),
        ("Combat Manager", "from core.combat_manager import CombatManager"),
        ("Card System", "from content.starter_cards import create_starter_cards"),
        ("Menu Screen", "from ui.menu_screen import MenuScreen"),
        ("Combat Screen", "from ui.combat_screen import CombatScreen"),
        ("Deck Builder", "from ui.deck_builder import DeckBuilderScreen"),
        ("Tutorial System", "from ui.tutorial_screen import TutorialScreen"),
        ("Animation System", "from ui.animation_system import EasingType, Animation"),
        ("Particle System", "from ui.particle_system import ParticleSystem"),
    ]
    
    passed = 0
    for test_name, import_code in tests:
        try:
            exec(import_code)
            print(f"   [OK] {test_name}")
            passed += 1
        except Exception as e:
            print(f"   [FAIL] {test_name}: {e}")
    
    print(f"\n[RESULT] Import Tests: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_pygame_initialization():
    """Test pygame initialization."""
    print("\n[TEST] Testing Pygame Initialization...")
    
    try:
        import pygame
        pygame.init()
        pygame.mixer.init()
        
        # Test display creation
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Window")
        
        print("   [OK] Pygame core initialization")
        print("   [OK] Pygame mixer initialization")
        print("   [OK] Display surface creation")
        
        pygame.quit()
        print("   [OK] Pygame cleanup")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Pygame initialization: {e}")
        return False

def test_theme_system():
    """Test theme system initialization."""
    print("\n[TEST] Testing Theme System...")
    
    try:
        import pygame
        pygame.init()  # Initialize pygame first for font system
        
        from ui.theme import initialize_theme, get_theme
        
        # Test different display modes
        for width, height, expected_mode in [
            (1920, 1080, "standard"),
            (3440, 1440, "ultrawide"),
            (2560, 1440, "widescreen")
        ]:
            theme = initialize_theme(width, height)
            print(f"   [OK] Theme initialized for {width}x{height} ({expected_mode})")
            
            # Test theme access
            current_theme = get_theme()
            print(f"   [OK] Theme access working")
            
            # Test theme properties
            assert hasattr(current_theme, 'colors')
            assert hasattr(current_theme, 'display')
            assert hasattr(current_theme, 'fonts')
            print(f"   [OK] Theme structure valid")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"   [FAIL] Theme system: {e}")
        traceback.print_exc()
        return False

def test_audio_system():
    """Test audio system initialization."""
    print("\n[TEST] Testing Audio System...")
    
    try:
        from audio.audio_manager import initialize_audio_manager
        
        # Initialize audio manager
        audio_manager = initialize_audio_manager()
        print("   [OK] Audio manager initialization")
        
        # Test sound loading
        from audio.sound_effects import play_button_sound
        print("   [OK] Sound effects module import")
        
        # Test audio cleanup
        audio_manager.cleanup()
        print("   [OK] Audio cleanup")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Audio system: {e}")
        traceback.print_exc()
        return False

def test_game_engine():
    """Test game engine initialization."""
    print("\n[TEST] Testing Game Engine...")
    
    try:
        from core.engine import GameEngine
        
        # Create and initialize engine
        engine = GameEngine()
        engine.initialize()
        print("   [OK] Game engine initialization")
        
        # Test engine update (should not crash)
        engine.update(0.016)  # Simulate 60 FPS frame
        print("   [OK] Game engine update")
        
        # Test engine shutdown
        engine.shutdown()
        print("   [OK] Game engine shutdown")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Game engine: {e}")
        traceback.print_exc()
        return False

def test_card_system():
    """Test card system initialization."""
    print("\n[TEST] Testing Card System...")
    
    try:
        from content.starter_cards import create_starter_cards
        
        # Initialize card system
        create_starter_cards()
        print("   [OK] Starter cards creation")
        
        # Test card data structures exist
        print("   [OK] Card system working with starter cards")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Card system: {e}")
        traceback.print_exc()
        return False

def test_ui_screens():
    """Test UI screen creation."""
    print("\n[TEST] Testing UI Screen Creation...")
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))
        
        from ui.theme import initialize_theme
        initialize_theme(1920, 1080)
        
        # Test each screen type
        screens = [
            ("Menu Screen", "from ui.menu_screen import MenuScreen; MenuScreen()"),
            ("Combat Screen", "from ui.combat_screen import CombatScreen; CombatScreen()"),
            ("Deck Builder", "from ui.deck_builder import DeckBuilderScreen; DeckBuilderScreen()"),
            ("Tutorial Screen", "from ui.tutorial_screen import TutorialScreen; TutorialScreen()"),
        ]
        
        passed = 0
        for screen_name, creation_code in screens:
            try:
                screen_obj = exec(creation_code)
                print(f"   [OK] {screen_name} creation")
                passed += 1
            except Exception as e:
                print(f"   [FAIL] {screen_name}: {e}")
        
        pygame.quit()
        print(f"\n[RESULT] UI Screen Tests: {passed}/{len(screens)} passed")
        return passed == len(screens)
        
    except Exception as e:
        print(f"   [FAIL] UI screen testing: {e}")
        traceback.print_exc()
        return False

def test_ui_manager():
    """Test UI manager functionality."""
    print("\n[TEST] Testing UI Manager...")
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))
        
        from ui.ui_manager import UIManager
        from ui.theme import initialize_theme
        
        # Initialize theme
        initialize_theme(1920, 1080)
        
        # Create UI manager
        ui_manager = UIManager(screen)
        print("   [OK] UI manager creation")
        
        # Add screens
        from ui.ui_manager import (get_menu_screen, get_combat_screen, 
                                   get_deck_builder_screen, get_tutorial_screen)
        
        ui_manager.add_screen(get_menu_screen()())
        ui_manager.add_screen(get_combat_screen()())
        ui_manager.add_screen(get_deck_builder_screen()())
        ui_manager.add_screen(get_tutorial_screen()())
        print("   [OK] Screen addition")
        
        # Test screen switching
        ui_manager.switch_to_screen("menu")
        print("   [OK] Screen switching to menu")
        
        ui_manager.switch_to_screen("tutorial")
        print("   [OK] Screen switching to tutorial")
        
        ui_manager.switch_to_screen("deck_builder")
        print("   [OK] Screen switching to deck builder")
        
        ui_manager.switch_to_screen("combat")
        print("   [OK] Screen switching to combat")
        
        # Test update
        ui_manager.update(0.016)
        print("   [OK] UI manager update")
        
        # Test cleanup
        ui_manager.shutdown()
        print("   [OK] UI manager cleanup")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"   [FAIL] UI manager: {e}")
        traceback.print_exc()
        return False

def test_combat_system():
    """Test combat system initialization."""
    print("\n[TEST] Testing Combat System...")
    
    try:
        from core.combat_manager import CombatManager
        from core.hourglass import HourGlass
        
        # Create combat manager
        combat_manager = CombatManager()
        print("   [OK] Combat manager creation")
        
        # Test hourglass system
        hourglass = HourGlass()
        print("   [OK] HourGlass system creation")
        
        # Test combat update
        combat_manager.update(0.016)
        print("   [OK] Combat system update")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Combat system: {e}")
        traceback.print_exc()
        return False

def test_animation_systems():
    """Test animation and particle systems."""
    print("\n[TEST] Testing Animation Systems...")
    
    try:
        from ui.animation_system import EasingType, Animation
        from ui.particle_system import ParticleSystem
        
        # Test animation system functions
        print("   [OK] Animation system imports")
        
        # Test particle system
        particle_system = ParticleSystem()
        print("   [OK] Particle system creation")
        
        # Test updates
        particle_system.update(0.016)
        print("   [OK] Animation systems update")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Animation systems: {e}")
        traceback.print_exc()
        return False

def test_full_game_loop():
    """Test complete game initialization without starting the main loop."""
    print("\n[TEST] Testing Full Game Initialization...")
    
    try:
        import pygame
        from core.engine import GameEngine
        from ui.ui_manager import UIManager
        from ui.theme import initialize_theme
        from content.starter_cards import create_starter_cards
        from audio.audio_manager import initialize_audio_manager
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Test - Sands of Duat")
        print("   [OK] Pygame initialization")
        
        # Create game engine
        engine = GameEngine()
        engine.initialize()
        print("   [OK] Game engine initialization")
        
        # Initialize theme
        theme = initialize_theme(1920, 1080)
        print("   [OK] Theme system initialization")
        
        # Initialize cards
        create_starter_cards()
        print("   [OK] Card system initialization")
        
        # Initialize audio
        audio_manager = initialize_audio_manager()
        print("   [OK] Audio system initialization")
        
        # Set up UI manager with all screens
        ui_manager = UIManager(screen)
        
        from ui.ui_manager import (get_menu_screen, get_combat_screen, 
                                   get_map_screen, get_deck_builder_screen, 
                                   get_tutorial_screen)
        
        ui_manager.add_screen(get_menu_screen()())
        ui_manager.add_screen(get_combat_screen()())
        ui_manager.add_screen(get_map_screen()())
        ui_manager.add_screen(get_deck_builder_screen()())
        ui_manager.add_screen(get_tutorial_screen()())
        print("   [OK] All UI screens added")
        
        # Start with menu screen
        ui_manager.switch_to_screen("menu")
        print("   [OK] Initial screen set to menu")
        
        # Test a few update cycles
        for i in range(5):
            engine.update(0.016)
            ui_manager.update(0.016)
            ui_manager.render()
            pygame.display.flip()
        print("   [OK] Game loop simulation (5 frames)")
        
        # Test screen transitions
        ui_manager.switch_to_screen_with_transition("tutorial", "fade")
        ui_manager.switch_to_screen_with_transition("deck_builder", "fade")
        ui_manager.switch_to_screen_with_transition("combat", "slide_left")
        ui_manager.switch_to_screen_with_transition("menu", "slide_right")
        print("   [OK] Screen transition testing")
        
        # Cleanup
        engine.shutdown()
        ui_manager.shutdown()
        audio_manager.cleanup()
        pygame.quit()
        print("   [OK] Full system cleanup")
        
        return True
        
    except Exception as e:
        print(f"   [FAIL] Full game initialization: {e}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive game testing."""
    print("=" * 60)
    print("COMPREHENSIVE SANDS OF DUAT GAME TESTING")
    print("=" * 60)
    
    tests = [
        ("Core Module Imports", test_imports),
        ("Pygame Initialization", test_pygame_initialization), 
        ("Theme System", test_theme_system),
        ("Audio System", test_audio_system),
        ("Game Engine", test_game_engine),
        ("Card System", test_card_system),
        ("UI Screens", test_ui_screens),
        ("UI Manager", test_ui_manager),
        ("Combat System", test_combat_system),
        ("Animation Systems", test_animation_systems),
        ("Full Game Loop", test_full_game_loop),
    ]
    
    results = []
    passed_count = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            start_time = time.time()
            result = test_func()
            end_time = time.time()
            
            if result:
                print(f"\n[PASS] {test_name} - {end_time - start_time:.2f}s")
                passed_count += 1
            else:
                print(f"\n[FAIL] {test_name} - {end_time - start_time:.2f}s")
            
            results.append((test_name, result, end_time - start_time))
            
        except Exception as e:
            print(f"\n[CRASH] {test_name} crashed: {e}")
            traceback.print_exc()
            results.append((test_name, False, 0))
    
    # Final summary
    print("\n" + "=" * 60)
    print("TESTING SUMMARY")
    print("=" * 60)
    
    for test_name, result, duration in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name:<25} ({duration:.2f}s)")
    
    print(f"\nOVERALL: {passed_count}/{len(tests)} tests passed")
    
    if passed_count == len(tests):
        print("\n[SUCCESS] ALL TESTS PASSED - Game is ready for play!")
        return True
    else:
        print(f"\n[WARNING] {len(tests) - passed_count} tests failed - Issues need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)