#!/usr/bin/env python3
"""
Simple Game Test - Direct rendering test to see SDXL assets
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    pygame.init()
    
    # Create screen
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("SDXL Assets Test - Sands of Duat")
    clock = pygame.time.Clock()
    
    # Load assets
    print("Loading SDXL assets...")
    from assets import load_assets, get_sprite
    load_assets()
    
    # Get sprites
    player_sprite = get_sprite("player_anubis")
    altar_ra = get_sprite("altar_ra")
    portal_arena = get_sprite("portal_arena")
    
    print(f"Player sprite: {player_sprite.get_size() if player_sprite else 'None'}")
    print(f"Altar Ra: {altar_ra.get_size() if altar_ra else 'None'}")
    print(f"Portal: {portal_arena.get_size() if portal_arena else 'None'}")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen with dark background
        screen.fill((20, 15, 10))
        
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Sands of Duat - SDXL Assets Test", True, (255, 215, 0))
        screen.blit(title, (50, 30))
        
        # Draw assets if they exist
        y_pos = 150
        
        if player_sprite:
            screen.blit(player_sprite, (100, y_pos))
            label = pygame.font.Font(None, 32).render("Player (Anubis Warrior)", True, (255, 255, 255))
            screen.blit(label, (300, y_pos + 50))
        
        if altar_ra:
            screen.blit(altar_ra, (100, y_pos + 200))
            label = pygame.font.Font(None, 32).render("Altar of Ra", True, (255, 255, 255))
            screen.blit(label, (300, y_pos + 250))
        
        if portal_arena:
            screen.blit(portal_arena, (100, y_pos + 400))
            label = pygame.font.Font(None, 32).render("Arena Portal", True, (255, 255, 255))
            screen.blit(label, (300, y_pos + 450))
        
        # Instructions
        instructions = [
            "High-Quality SDXL Generated Assets:",
            "- 768x768 resolution scaled for gameplay",
            "- 100 steps generation with RTX 5070",
            "- Professional Egyptian mythology artwork",
            "",
            "Press ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            text = pygame.font.Font(None, 24).render(instruction, True, color)
            screen.blit(text, (600, 200 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()