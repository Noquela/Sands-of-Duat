#!/usr/bin/env python3
"""
AI Asset Showcase
Demonstrates all the professional AI assets in an impressive gallery format
"""

import pygame
import sys
from pathlib import Path
sys.path.append('.')

def showcase_ai_assets():
    """Create a comprehensive showcase of all AI assets"""
    pygame.init()
    
    # Create large showcase window
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Sands of Duat - AI Asset Showcase")
    clock = pygame.time.Clock()
    
    # Load all assets
    print("Loading AI assets for showcase...")
    
    # Load backgrounds
    backgrounds = []
    bg_dir = Path('game_assets/environments')
    if bg_dir.exists():
        for bg_file in bg_dir.glob('*.png'):
            bg = pygame.image.load(str(bg_file))
            backgrounds.append((bg_file.stem, bg))
    
    # Load card art
    cards = []
    cards_dir = Path('game_assets/cards')
    if cards_dir.exists():
        for card_file in sorted(cards_dir.glob('*.png'))[:8]:  # Show first 8 cards
            card = pygame.image.load(str(card_file))
            cards.append((card_file.stem.replace('_', ' ').title(), card))
    
    # Load character sprites
    sprites = []
    sprites_dir = Path('game_assets/characters/sprites')
    if sprites_dir.exists():
        # Get one sprite per character
        characters = {}
        for sprite_file in sprites_dir.glob('*_idle.png'):
            char_name = sprite_file.stem.replace('_idle', '').replace('_', ' ').title()
            sprite = pygame.image.load(str(sprite_file))
            characters[char_name] = sprite
        sprites = list(characters.items())
    
    # Showcase loop
    bg_index = 0
    bg_timer = 0
    bg_switch_time = 5000  # 5 seconds per background
    
    running = True
    while running:
        dt = clock.tick(60)
        bg_timer += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    bg_index = (bg_index + 1) % len(backgrounds)
                    bg_timer = 0
        
        # Auto-cycle backgrounds
        if bg_timer >= bg_switch_time and backgrounds:
            bg_index = (bg_index + 1) % len(backgrounds)
            bg_timer = 0
        
        # Clear screen
        screen.fill((20, 15, 10))
        
        # Draw current background (scaled)
        if backgrounds:
            bg_name, bg_surface = backgrounds[bg_index]
            scaled_bg = pygame.transform.scale(bg_surface, (1920, 1080))
            screen.blit(scaled_bg, (0, 0))
            
            # Background title
            font = pygame.font.Font(None, 48)
            title = font.render(f"Background: {bg_name.replace('_', ' ').title()}", True, (255, 255, 255))
            title_shadow = font.render(f"Background: {bg_name.replace('_', ' ').title()}", True, (0, 0, 0))
            screen.blit(title_shadow, (52, 52))
            screen.blit(title, (50, 50))
        
        # Draw card gallery
        if cards:
            card_y = 150
            card_spacing = 200
            start_x = (1920 - (len(cards) * card_spacing)) // 2
            
            for i, (card_name, card_surface) in enumerate(cards):
                # Scale card to showcase size
                card_scaled = pygame.transform.scale(card_surface, (160, 240))
                card_x = start_x + i * card_spacing
                
                # Card background
                card_bg = pygame.Rect(card_x - 10, card_y - 10, 180, 260)
                pygame.draw.rect(screen, (0, 0, 0, 180), card_bg)
                pygame.draw.rect(screen, (255, 215, 0), card_bg, 2)
                
                # Card image
                screen.blit(card_scaled, (card_x, card_y))
                
                # Card name
                name_font = pygame.font.Font(None, 24)
                name_text = name_font.render(card_name[:12], True, (255, 255, 255))
                name_rect = name_text.get_rect(centerx=card_x + 80, y=card_y + 250)
                screen.blit(name_text, name_rect)
        
        # Draw character sprites
        if sprites:
            sprite_y = 500
            sprite_spacing = 300
            start_x = (1920 - (len(sprites) * sprite_spacing)) // 2
            
            for i, (char_name, sprite_surface) in enumerate(sprites):
                # Scale sprite
                sprite_scaled = pygame.transform.scale(sprite_surface, (200, 200))
                sprite_x = start_x + i * sprite_spacing
                
                # Sprite background circle
                center = (sprite_x + 100, sprite_y + 100)
                pygame.draw.circle(screen, (50, 50, 50, 180), center, 110)
                pygame.draw.circle(screen, (255, 215, 0), center, 110, 3)
                
                # Sprite image
                screen.blit(sprite_scaled, (sprite_x, sprite_y))
                
                # Character name
                name_font = pygame.font.Font(None, 28)
                name_text = name_font.render(char_name, True, (255, 255, 255))
                name_shadow = name_font.render(char_name, True, (0, 0, 0))
                name_rect = name_text.get_rect(centerx=sprite_x + 100, y=sprite_y + 220)
                screen.blit(name_shadow, (name_rect.x + 2, name_rect.y + 2))
                screen.blit(name_text, name_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 32)
        instructions = [
            "SANDS OF DUAT - Professional AI Asset Showcase",
            "SPACE: Next Background | ESC: Exit",
            f"Assets: {len(backgrounds)} Backgrounds, {len(cards)} Cards, {len(sprites)} Characters"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (255, 255, 255) if i != 0 else (255, 215, 0)
            text = inst_font.render(instruction, True, color)
            shadow = inst_font.render(instruction, True, (0, 0, 0))
            y_pos = 850 + i * 40
            screen.blit(shadow, (52, y_pos + 2))
            screen.blit(text, (50, y_pos))
        
        pygame.display.flip()
    
    pygame.quit()
    print("AI Asset Showcase complete!")

if __name__ == "__main__":
    showcase_ai_assets()