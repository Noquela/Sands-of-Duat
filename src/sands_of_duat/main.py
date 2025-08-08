#!/usr/bin/env python3
"""
SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME
==============================================

Main entry point with Hades-level polish and Egyptian theming.
Clean architecture focused on smooth UX and beautiful transitions.
"""

import pygame
import sys
import logging
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.core.game_engine import GameEngine
from sands_of_duat.core.constants import SCREEN_SIZE, Timing

def setup_logging():
    """Setup logging with Egyptian theming."""
    logging.basicConfig(
        level=logging.INFO,
        format='🏺 %(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
        datefmt='%H:%M:%S'
    )

def main():
    """Main game entry point with premium Egyptian experience."""
    setup_logging()
    logger = logging.getLogger("sands_of_duat")
    
    logger.info("🏺 SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME 🏺")
    logger.info("✨ Initializing Hades-level Egyptian experience...")
    
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    # Create display with Egyptian golden ratio dimensions
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Sands of Duat - Egyptian Underworld Card Game")
    
    # TODO: Set custom Egyptian icon when we generate assets
    # pygame.display.set_icon(icon_surface)
    
    clock = pygame.time.Clock()
    
    try:
        # Initialize game engine
        game_engine = GameEngine(screen)
        
        logger.info("✦ All systems initialized - entering the underworld...")
        
        # Main game loop with Egyptian precision
        while game_engine.running:
            # Calculate delta time
            dt = clock.tick(Timing.TARGET_FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_engine.running = False
                else:
                    game_engine.handle_event(event)
            
            # Update game systems
            game_engine.update(dt)
            
            # Render with Egyptian excellence
            game_engine.render()
        
    except Exception as e:
        logger.error(f"💀 Fatal error in main game loop: {e}")
        raise
    finally:
        # Cleanup with Egyptian grace
        logger.info("🏺 May the gods remember your journey through the underworld...")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()