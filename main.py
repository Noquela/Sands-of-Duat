#!/usr/bin/env python3
"""
Sands of Duat - Main Entry Point

Entry point for the Sands of Duat roguelike deck-builder game.
Initializes the game engine and starts the main game loop.
"""

import sys
import logging
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent / "sands_duat"
sys.path.insert(0, str(project_root))

from core.engine import GameEngine
from ui.ui_manager import UIManager
from ui.theme import initialize_theme
from content.starter_cards import create_starter_cards
import pygame


def setup_logging(debug: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('sands_duat.log')
        ]
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Sands of Duat - Roguelike Deck-Builder Game"
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--windowed',
        action='store_true',
        help='Run in windowed mode (default is fullscreen)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=3440,
        help='Window width (default: 3440 for ultrawide)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=1440,
        help='Window height (default: 1440 for ultrawide)'
    )
    
    parser.add_argument(
        '--skip-intro',
        action='store_true',
        help='Skip intro sequence and go straight to main menu'
    )
    
    parser.add_argument(
        '--dev-mode',
        action='store_true',
        help='Enable development mode with extra debug features'
    )
    
    return parser.parse_args()


def initialize_pygame(args: argparse.Namespace) -> pygame.Surface:
    """Initialize pygame and create the main display surface with ultrawide support."""
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    # Set up display with ultrawide optimizations
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    
    if not args.windowed:
        flags |= pygame.FULLSCREEN
    elif args.width >= 3000:  # Ultrawide display
        # Use borderless for better ultrawide experience
        flags |= pygame.NOFRAME
        # Center window on ultrawide monitors
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
    
    screen = pygame.display.set_mode((args.width, args.height), flags)
    pygame.display.set_caption("Sands of Duat")
    
    # Set window icon (if available)
    icon_path = Path("sands_duat/assets/icon.png")
    if icon_path.exists():
        icon = pygame.image.load(str(icon_path))
        pygame.display.set_icon(icon)
    
    return screen


def main() -> int:
    """Main game function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Sands of Duat")
    logger.info(f"Debug mode: {args.debug}")
    logger.info(f"Development mode: {args.dev_mode}")
    
    try:
        # Initialize pygame
        screen = initialize_pygame(args)
        logger.info(f"Initialized display: {screen.get_size()}")
        
        # Create and initialize game engine
        engine = GameEngine()
        engine.initialize()
        
        # Initialize theme system for ultrawide support
        theme = initialize_theme(screen.get_width(), screen.get_height())
        logger.info(f"Theme initialized for {theme.display.display_mode.value} mode")
        
        # Initialize card system
        create_starter_cards()
        logger.info("Card system initialized")
        
        # Set up UI manager
        ui_manager = UIManager(screen)
        
        # Import and add screens using delayed imports
        from ui.ui_manager import get_menu_screen, get_combat_screen, get_map_screen, get_deck_builder_screen
        
        ui_manager.add_screen(get_menu_screen()())
        ui_manager.add_screen(get_combat_screen()())
        ui_manager.add_screen(get_map_screen()())
        ui_manager.add_screen(get_deck_builder_screen()())
        
        # Start with menu screen (or skip to combat if in dev mode)
        if args.dev_mode:
            ui_manager.switch_to_screen("combat")
        else:
            ui_manager.switch_to_screen("menu")
        
        # Main game loop
        clock = pygame.time.Clock()
        running = True
        
        logger.info("Entering main game loop")
        
        while running:
            delta_time = clock.tick(60) / 1000.0  # 60 FPS, convert to seconds
            
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Global hotkeys
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and (pygame.key.get_pressed()[pygame.K_LALT] or 
                                                    pygame.key.get_pressed()[pygame.K_RALT]):
                        running = False
                    elif event.key == pygame.K_F11:
                        # Toggle fullscreen
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE and args.dev_mode:
                        # ESC to exit in dev mode
                        running = False
                
                # Pass event to UI manager
                ui_manager.handle_event(event)
            
            # Update game systems
            engine.update(delta_time)
            ui_manager.update(delta_time)
            
            # Render
            ui_manager.render()
            pygame.display.flip()
        
        logger.info("Exiting main game loop")
        
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1
        
    finally:
        # Clean shutdown
        try:
            if 'engine' in locals():
                engine.shutdown()
            if 'ui_manager' in locals():
                ui_manager.shutdown()
            pygame.quit()
            logger.info("Clean shutdown completed")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())