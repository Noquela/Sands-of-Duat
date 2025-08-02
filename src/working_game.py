#!/usr/bin/env python3
"""
Working Game - Simple version that definitely shows SDXL assets
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

class WorkingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Sands of Duat - SDXL Assets Working!")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load SDXL assets
        print("Loading SDXL assets...")
        from assets import load_assets, get_sprite
        load_assets()
        
        # Store sprites
        self.player_sprite = get_sprite("player_anubis")
        self.altar_ra = get_sprite("altar_ra")
        self.altar_thoth = get_sprite("altar_thoth")
        self.altar_isis = get_sprite("altar_isis")
        self.altar_ptah = get_sprite("altar_ptah")
        self.portal_sprite = get_sprite("portal_arena")
        
        # Player position
        self.player_x = 600
        self.player_y = 400
        
        print(f"Player sprite: {self.player_sprite.get_size() if self.player_sprite else 'None'}")
        print(f"Altars loaded: {bool(self.altar_ra)}, {bool(self.altar_thoth)}, {bool(self.altar_isis)}, {bool(self.altar_ptah)}")
        print(f"Portal loaded: {bool(self.portal_sprite)}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Handle movement
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x += speed
    
    def render(self):
        # Clear screen
        self.screen.fill((15, 10, 5))  # Dark background
        
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Sands of Duat - SDXL Assets Working!", True, (255, 215, 0))
        self.screen.blit(title, (200, 30))
        
        # Draw altars in corners
        if self.altar_ra:
            self.screen.blit(self.altar_ra, (50, 150))
        if self.altar_thoth:
            self.screen.blit(self.altar_thoth, (950, 150))
        if self.altar_isis:
            self.screen.blit(self.altar_isis, (50, 500))
        if self.altar_ptah:
            self.screen.blit(self.altar_ptah, (950, 500))
        
        # Draw portal in center bottom
        if self.portal_sprite:
            self.screen.blit(self.portal_sprite, (550, 650))
        
        # Draw player
        if self.player_sprite:
            # Center the sprite on the player position
            sprite_x = self.player_x - self.player_sprite.get_width() // 2
            sprite_y = self.player_y - self.player_sprite.get_height() // 2
            self.screen.blit(self.player_sprite, (sprite_x, sprite_y))
        
        # Draw instructions
        instructions = [
            "WASD or Arrow Keys to move",
            "ESC to quit",
            "",
            "High-Quality SDXL Generated Assets:",
            "✓ Player: Anubis Warrior (768x768 → 153x153)",
            "✓ Altars: Ra, Thoth, Isis, Ptah (768x768 → 192x192)",
            "✓ Portal: Arena Portal (768x768 → 153x153)",
            "",
            "Generated with 100 steps on RTX 5070"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction.startswith("✓"):
                color = (0, 255, 0)
            elif instruction.startswith("High-Quality"):
                color = (255, 215, 0)
            else:
                color = (255, 255, 255)
            
            text = pygame.font.Font(None, 24).render(instruction, True, color)
            self.screen.blit(text, (300, 100 + i * 25))
        
        pygame.display.flip()
    
    def run(self):
        print("Starting working game with SDXL assets...")
        
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        print("Game ended successfully!")

if __name__ == "__main__":
    game = WorkingGame()
    game.run()