"""
Quick test of the new transition and loading systems.
"""

import pygame
import sys
import time
from src.sands_of_duat.core.game_engine import GameEngine
from src.sands_of_duat.core.constants import SCREEN_SIZE

def main():
    """Test the enhanced transition system."""
    pygame.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Sands of Duat - SPRINT 3: Game State Flow & Transitions")
    
    engine = GameEngine(screen)
    
    print("Testing SPRINT 3: Enhanced Game State Flow & Transitions")
    print("Features:")
    print("  - Professional loading screens with Egyptian theming")
    print("  - Smooth state transitions with context-aware messages")
    print("  - Enhanced menu navigation with proper back flow")
    print("  - Ultrawide display support for all screens")
    print()
    print("Controls:")
    print("  - Navigate menus and test transitions")
    print("  - ESC to go back to main menu from any screen") 
    print("  - F11 for fullscreen, F1 for debug info")
    print("  - Try all menu options to see the new transition system!")
    print()
    
    last_time = time.time()
    
    try:
        while engine.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Cap delta time to prevent large jumps
            dt = min(dt, 1.0 / 30.0)  # Minimum 30 FPS equivalent
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    engine.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not engine.handle_escape():
                            engine.running = False
                    else:
                        engine.handle_event(event)
                else:
                    engine.handle_event(event)
            
            # Update and render
            engine.update(dt)
            engine.render()
            
            # Maintain 60 FPS
            engine.clock.tick(60)
    
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.shutdown()
        pygame.quit()

if __name__ == "__main__":
    main()