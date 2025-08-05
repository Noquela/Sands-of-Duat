#!/usr/bin/env python3
"""
Test if our changes are working by launching the game directly
"""

import pygame
import sys
from pathlib import Path

# Add the game directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_dynamic_combat_directly():
    """Test the dynamic combat screen directly"""
    print("Testing dynamic combat screen directly...")
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Direct Dynamic Combat Test")
    clock = pygame.time.Clock()
    
    # Import and create the dynamic combat screen
    try:
        from sands_duat.ui.dynamic_combat_screen import DynamicCombatScreen
        from sands_duat.core.dynamic_combat_manager import DynamicCombatManager
        
        # Create the screen
        combat_screen = DynamicCombatScreen()
        
        # Create combat manager
        combat_manager = DynamicCombatManager()
        combat_screen.combat_manager = combat_manager
        combat_screen.active = True
        
        print("Dynamic combat screen created successfully")
        
        # Test loop
        running = True
        while running:
            dt = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # Let the screen handle events
                combat_screen.handle_event(event)
            
            # Update
            combat_screen.update(dt)
            
            # Render
            screen.fill((0, 0, 0))
            combat_screen.render(screen)
            
            pygame.display.flip()
        
    except Exception as e:
        print(f"Error testing dynamic combat: {e}")
        import traceback
        traceback.print_exc()
    
    pygame.quit()

if __name__ == "__main__":
    test_dynamic_combat_directly()