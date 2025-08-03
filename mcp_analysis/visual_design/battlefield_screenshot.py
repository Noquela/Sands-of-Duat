#!/usr/bin/env python3
"""
Battlefield Screenshot Capture Script
Captures the current combat screen to analyze atmospheric elements.
"""

import sys
import pygame
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

from core.engine import GameEngine
from ui.ui_manager import UIManager
from ui.theme import initialize_theme
from content.starter_cards import create_starter_cards
from audio.audio_manager import initialize_audio_manager

def capture_battlefield_screenshot():
    """Capture a screenshot of the current battlefield implementation."""
    try:
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Create display
        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Battlefield Screenshot Capture")
        
        # Initialize game systems
        engine = GameEngine()
        engine.initialize()
        
        theme = initialize_theme(1920, 1080)
        create_starter_cards()
        audio_manager = initialize_audio_manager()
        
        # Set up UI manager
        ui_manager = UIManager(screen)
        
        # Import and add screens
        from ui.ui_manager import get_combat_screen
        combat_screen = get_combat_screen()()
        ui_manager.add_screen(combat_screen)
        
        # Switch to combat screen
        ui_manager.switch_to_screen("combat")
        
        # Let the screen initialize
        for _ in range(30):  # 30 frames at 60fps = 0.5 seconds
            delta_time = 1/60
            
            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                ui_manager.handle_event(event)
            
            # Update and render
            engine.update(delta_time)
            ui_manager.update(delta_time)
            ui_manager.render()
            pygame.display.flip()
        
        # Capture screenshot
        timestamp = int(time.time())
        screenshot_path = Path(__file__).parent / f"battlefield_current_{timestamp}.png"
        pygame.image.save(screen, str(screenshot_path))
        
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Save a copy for analysis
        analysis_path = Path(__file__).parent / "battlefield_analysis_current.png"
        pygame.image.save(screen, str(analysis_path))
        
        print(f"Analysis copy saved to: {analysis_path}")
        
        return str(screenshot_path)
        
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None
        
    finally:
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    capture_battlefield_screenshot()