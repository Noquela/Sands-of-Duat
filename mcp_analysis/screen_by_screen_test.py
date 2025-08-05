"""
Screen-by-screen functionality test for Sands of Duat
Tests each individual screen and its functionality
"""

import subprocess
import time
import sys
import pygame
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

def test_individual_screen(screen_name, duration=3):
    """Test a specific screen for functionality"""
    print(f"\n=== TESTING {screen_name.upper()} SCREEN ===")
    
    try:
        # Set up pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))  # Smaller size for testing
        pygame.display.set_caption(f"Testing: {screen_name}")
        
        # Import and initialize theme
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(screen)
        
        # Import UI manager
        from sands_duat.ui.ui_manager import UIManager
        ui_manager = UIManager(screen)
        
        # Import specific screen
        screen_classes = {
            'menu': 'get_menu_screen',
            'combat': 'get_combat_screen',
            'map': 'get_map_screen',
            'deck_builder': 'get_deck_builder_screen',
            'tutorial': 'get_tutorial_screen',
            'progression': 'get_progression_screen',
            'victory': 'get_victory_screen',
            'defeat': 'get_defeat_screen',
            'dynamic_combat': 'get_dynamic_combat_screen'
        }
        
        if screen_name not in screen_classes:
            print(f"ERROR: Unknown screen name '{screen_name}'")
            return False
        
        # Import and create screen
        from sands_duat.ui.ui_manager import get_menu_screen, get_combat_screen, get_map_screen, get_deck_builder_screen, get_tutorial_screen, get_progression_screen, get_victory_screen, get_defeat_screen, get_dynamic_combat_screen
        
        screen_func = eval(screen_classes[screen_name])
        screen_instance = screen_func()()
        
        # Add screen to UI manager
        ui_manager.add_screen(screen_instance)
        ui_manager.switch_to_screen(screen_name)
        
        print(f"SUCCESS: {screen_name} screen created and initialized")
        
        # Test basic functionality for a few seconds
        clock = pygame.time.Clock()
        test_duration = duration
        start_time = time.time()
        
        events_handled = 0
        renders_completed = 0
        
        while time.time() - start_time < test_duration:
            delta_time = clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                ui_manager.handle_event(event)
                events_handled += 1
            
            # Update and render
            ui_manager.update(delta_time)
            screen.fill((0, 0, 0))
            ui_manager.render(screen)
            pygame.display.flip()
            renders_completed += 1
        
        print(f"SUCCESS: {screen_name} screen ran for {test_duration}s")
        print(f"  - Events handled: {events_handled}")
        print(f"  - Renders completed: {renders_completed}")
        print(f"  - Average FPS: {renders_completed/test_duration:.1f}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to test {screen_name} screen: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        return False

def analyze_screen_assets():
    """Analyze which assets are being used by each screen"""
    print("\n=== ANALYZING SCREEN ASSETS ===")
    
    # Check background assets
    bg_path = Path("game_assets/environments")
    backgrounds = list(bg_path.glob("*.png")) if bg_path.exists() else []
    
    print(f"Available backgrounds: {len(backgrounds)}")
    for bg in backgrounds:
        print(f"  - {bg.name}")
    
    # Check if logs show asset loading
    log_file = Path("sands_duat.log")
    if log_file.exists():
        with open(log_file, 'r') as f:
            content = f.read()
            
        asset_loads = content.count("Loaded AI background")
        print(f"\nRecent AI background loads: {asset_loads}")
        
        # Extract specific asset loads
        lines = content.split('\n')
        for line in lines[-50:]:  # Last 50 lines
            if "Loaded AI background" in line:
                print(f"  {line.split(' - ')[-1]}")

def main():
    print("SANDS OF DUAT - SCREEN-BY-SCREEN ANALYSIS")
    print("=" * 60)
    
    # Change to game directory
    os.chdir(Path(__file__).parent.parent)
    
    # Test each screen individually
    screens_to_test = [
        'menu',
        'combat', 
        'deck_builder',
        'map',
        'tutorial',
        'progression'
    ]
    
    successful_screens = 0
    total_screens = len(screens_to_test)
    
    for screen_name in screens_to_test:
        success = test_individual_screen(screen_name, duration=2)
        if success:
            successful_screens += 1
        time.sleep(1)  # Brief pause between tests
    
    # Analyze assets
    analyze_screen_assets()
    
    # Summary
    print(f"\n{'='*60}")
    print("SCREEN TESTING SUMMARY")
    print(f"{'='*60}")
    print(f"Successful screens: {successful_screens}/{total_screens}")
    print(f"Success rate: {(successful_screens/total_screens)*100:.1f}%")
    
    if successful_screens == total_screens:
        print("CONCLUSION: ALL SCREENS ARE FUNCTIONAL")
    elif successful_screens >= total_screens * 0.8:
        print("CONCLUSION: MOST SCREENS ARE FUNCTIONAL")
    else:
        print("CONCLUSION: SIGNIFICANT SCREEN ISSUES DETECTED")

if __name__ == "__main__":
    main()