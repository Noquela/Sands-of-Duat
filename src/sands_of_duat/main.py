#!/usr/bin/env python3
"""
SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME
==============================================

Main entry point with complete Egyptian combat system implementation.
Features authentic Egyptian mythology integrated into strategic card gameplay.
"""

import pygame
import sys
import logging
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.combat.integrated_combat_system import IntegratedCombatSystem, GameState

def setup_logging():
    """Setup logging for the game."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

def main():
    """Main game entry point with complete Egyptian combat system."""
    setup_logging()
    logger = logging.getLogger("sands_of_duat")
    
    logger.info("🏺 SANDS OF DUAT - EGYPTIAN UNDERWORLD CARD GAME 🏺")
    logger.info("Complete Egyptian Combat System Implementation")
    
    # Initialize Pygame
    pygame.init()
    
    # Create display
    screen = pygame.display.set_mode((1400, 900))
    pygame.display.set_caption("Sands of Duat - Egyptian Underworld Card Battle")
    clock = pygame.time.Clock()
    
    # Initialize the integrated combat system
    combat_system = IntegratedCombatSystem(1400, 900)
    
    # Egyptian color scheme
    COLORS = {
        'GOLD': (255, 215, 0),
        'LAPIS_LAZULI': (26, 81, 171),
        'PAPYRUS': (245, 245, 220),
        'DESERT_SAND': (238, 203, 173),
        'DARK_BLUE': (25, 25, 112)
    }
    
    # Game state
    game_started = False
    show_instructions = True
    
    # Main game loop
    running = True
    logger.info("Starting Egyptian combat system...")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and not game_started:
                    # Start combat
                    combat_system.start_combat()
                    game_started = True
                    show_instructions = False
                    logger.info("Combat initiated - entering the underworld!")
                elif game_started:
                    # Pass keypress to combat system
                    combat_system.handle_keypress(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if show_instructions:
                        show_instructions = False
                    elif game_started:
                        # Pass click to combat system
                        combat_system.handle_click(event.pos)
        
        # Update game systems
        if game_started:
            # Update combat system
            combat_continues = combat_system.update()
            if not combat_continues:
                # Combat ended, could restart or show results
                game_state = combat_system.get_game_state_for_ui()
                if game_state['game_state'] in ['victory', 'defeat']:
                    logger.info(f"Combat ended: {game_state['game_state']}")
        
        # Render
        if show_instructions:
            _render_instructions(screen, COLORS)
        elif game_started:
            # Render combat system
            combat_system.render(screen)
        else:
            _render_menu(screen, COLORS)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    logger.info("May the gods remember your journey through the underworld...")

def _render_instructions(screen, colors):
    """Render game instructions."""
    screen.fill(colors['DARK_BLUE'])
    
    # Title
    font_title = pygame.font.Font(None, 48)
    title = font_title.render("SANDS OF DUAT", True, colors['GOLD'])
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))
    
    # Subtitle
    font_subtitle = pygame.font.Font(None, 28)
    subtitle = font_subtitle.render("Egyptian Underworld Card Battle System", True, colors['PAPYRUS'])
    screen.blit(subtitle, (screen.get_width()//2 - subtitle.get_width()//2, 100))
    
    # Instructions
    font_body = pygame.font.Font(None, 24)
    instructions = [
        "",
        "AUTHENTIC EGYPTIAN COMBAT SYSTEM",
        "",
        "• Hour-Glass Initiative: Actions flow like sand through time",
        "• 13-Phase Combat: Journey through the Egyptian underworld",
        "• Ba-Ka Soul Mechanics: Separate soul from body for power",
        "• Divine Judgment: Ma'at weighs your moral actions",
        "• Underworld Passage: Navigate the 12 hours of night",
        "• Resurrection System: Return from death through Egyptian rites",
        "",
        "CONTROLS:",
        "• Click cards in your hand to select them",
        "• Click action buttons to use abilities",
        "• Use Space to end your turn",
        "• Press 1 to separate Ba, 2 to manifest Ka",
        "",
        "Press ENTER to begin your journey into the underworld...",
        "",
        "Click anywhere to dismiss these instructions"
    ]
    
    y_offset = 150
    for instruction in instructions:
        if instruction.startswith("AUTHENTIC") or instruction.startswith("CONTROLS"):
            color = colors['GOLD']
            font = pygame.font.Font(None, 26)
        elif instruction == "":
            y_offset += 10
            continue
        else:
            color = colors['PAPYRUS']
            font = font_body
            
        text = font.render(instruction, True, color)
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, y_offset))
        y_offset += 30

def _render_menu(screen, colors):
    """Render main menu."""
    screen.fill(colors['DARK_BLUE'])
    
    # Title
    font = pygame.font.Font(None, 64)
    title = font.render("SANDS OF DUAT", True, colors['GOLD'])
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 200))
    
    # Ready message
    font_ready = pygame.font.Font(None, 32)
    ready = font_ready.render("Combat System Ready", True, colors['PAPYRUS'])
    screen.blit(ready, (screen.get_width()//2 - ready.get_width()//2, 300))
    
    # Start prompt
    font_start = pygame.font.Font(None, 24)
    start = font_start.render("Press ENTER to begin combat", True, colors['DESERT_SAND'])
    screen.blit(start, (screen.get_width()//2 - start.get_width()//2, 400))
    
    # Features
    features = [
        "✦ Authentic Egyptian mythology",
        "✦ Strategic card-based combat", 
        "✦ Soul manipulation mechanics",
        "✦ Divine judgment system",
        "✦ Underworld exploration"
    ]
    
    y_offset = 500
    for feature in features:
        feature_text = font_start.render(feature, True, colors['PAPYRUS'])
        screen.blit(feature_text, (screen.get_width()//2 - feature_text.get_width()//2, y_offset))
        y_offset += 30

if __name__ == "__main__":
    main()