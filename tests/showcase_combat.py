#!/usr/bin/env python3
"""
Showcase Combat Screen
A spectacular display of all our AI assets in combat format
"""

import pygame
import sys
import random
import math
import time
from pathlib import Path

# Add game path
sys.path.insert(0, str(Path(__file__).parent))

def create_showcase_combat():
    """Create a spectacular combat showcase"""
    pygame.init()
    
    # Full screen for maximum impact
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    pygame.display.set_caption("Sands of Duat - AI Combat Showcase")
    
    clock = pygame.time.Clock()
    
    # Load AI background
    try:
        from sands_duat.graphics.background_loader import load_background
        background = load_background('combat', (screen_width, screen_height))
        if not background:
            # Create Egyptian gradient
            background = pygame.Surface((screen_width, screen_height))
            for y in range(screen_height):
                blend = y / screen_height
                r = int(80 * (1 - blend) + 25 * blend)
                g = int(60 * (1 - blend) + 15 * blend)
                b = int(30 * (1 - blend) + 5 * blend)
                pygame.draw.line(background, (r, g, b), (0, y), (screen_width, y))
    except:
        background = pygame.Surface((screen_width, screen_height))
        background.fill((40, 25, 10))
    
    # Load AI character sprites
    player_sprite = None
    enemy_sprite = None
    
    try:
        player_path = Path('game_assets/characters/sprites/player_character_idle.png')
        enemy_path = Path('game_assets/characters/sprites/anubis_guardian_idle.png')
        
        if player_path.exists():
            player_sprite = pygame.image.load(str(player_path))
            # Scale to be impressive (40% of screen height)
            target_height = int(screen_height * 0.4)
            scale_factor = target_height / player_sprite.get_height()
            new_width = int(player_sprite.get_width() * scale_factor)
            player_sprite = pygame.transform.scale(player_sprite, (new_width, target_height))
        
        if enemy_path.exists():
            enemy_sprite = pygame.image.load(str(enemy_path))
            # Scale to be slightly larger (45% of screen height)
            target_height = int(screen_height * 0.45)
            scale_factor = target_height / enemy_sprite.get_height()
            new_width = int(enemy_sprite.get_width() * scale_factor)
            enemy_sprite = pygame.transform.scale(enemy_sprite, (new_width, target_height))
            # Flip to face player
            enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    except Exception as e:
        print(f"Error loading sprites: {e}")
    
    # Load AI card art
    cards = []
    try:
        from sands_duat.graphics.card_art_loader import load_card_art
        card_names = [
            "Mummy's Wrath", "Desert Whisper", "Anubis Judgment", 
            "Ra's Solar Flare", "Isis's Grace", "Pyramid Power"
        ]
        
        for card_name in card_names:
            card_art = load_card_art(card_name, (200, 280))
            if card_art:
                cards.append((card_name, card_art))
    except Exception as e:
        print(f"Error loading cards: {e}")
    
    # Animation variables
    glow_time = 0
    card_float_time = 0
    title_pulse = 0
    
    # Main showcase loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F11:
                    running = False
        
        # Update animations
        glow_time += dt
        card_float_time += dt * 2
        title_pulse += dt * 3
        
        # Draw background
        screen.blit(background, (0, 0))
        
        # Add atmospheric overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((20, 15, 5, 50))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        font_large = pygame.font.Font(None, int(screen_height * 0.08))
        title_alpha = int(200 + 55 * math.sin(title_pulse))
        title = font_large.render("SANDS OF DUAT", True, (255, 215, 0))
        title.set_alpha(title_alpha)
        title_rect = title.get_rect(centerx=screen_width//2, y=screen_height//12)
        screen.blit(title, title_rect)
        
        subtitle = font_large.render("AI COMBAT SHOWCASE", True, (200, 150, 50))
        subtitle_rect = subtitle.get_rect(centerx=screen_width//2, y=title_rect.bottom + 10)
        screen.blit(subtitle, subtitle_rect)
        
        # Draw character sprites with glow effects
        if player_sprite and enemy_sprite:
            # Player position (right side)
            player_x = screen_width * 3 // 4
            player_y = screen_height * 2 // 3
            
            # Enemy position (left side)
            enemy_x = screen_width // 4
            enemy_y = screen_height * 2 // 3
            
            # Glow effects
            glow_radius = int(30 + 15 * math.sin(glow_time * 2))
            
            # Player glow (blue)
            player_center = (player_x, player_y)
            for radius in range(glow_radius, 0, -5):
                alpha = int(30 * (radius / glow_radius))
                glow_surf = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (100, 150, 255, alpha), (radius*2, radius*2), radius)
                screen.blit(glow_surf, (player_x - radius*2, player_y - radius*2))
            
            # Enemy glow (red)
            enemy_center = (enemy_x, enemy_y)
            for radius in range(glow_radius, 0, -5):
                alpha = int(30 * (radius / glow_radius))
                glow_surf = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 100, 100, alpha), (radius*2, radius*2), radius)
                screen.blit(glow_surf, (enemy_x - radius*2, enemy_y - radius*2))
            
            # Character sprites
            player_rect = player_sprite.get_rect(center=(player_x, player_y))
            enemy_rect = enemy_sprite.get_rect(center=(enemy_x, enemy_y))
            
            screen.blit(enemy_sprite, enemy_rect)
            screen.blit(player_sprite, player_rect)
            
            # Character names
            font_med = pygame.font.Font(None, 48)
            
            player_name = font_med.render("Egyptian Warrior", True, (100, 200, 255))
            player_name_rect = player_name.get_rect(centerx=player_x, y=player_rect.bottom + 20)
            screen.blit(player_name, player_name_rect)
            
            enemy_name = font_med.render("Anubis Guardian", True, (255, 100, 100))
            enemy_name_rect = enemy_name.get_rect(centerx=enemy_x, y=enemy_rect.bottom + 20)
            screen.blit(enemy_name, enemy_name_rect)
        
        # Draw AI card showcase at bottom
        if cards:
            card_y = screen_height - 320
            card_spacing = min(220, (screen_width - 400) // len(cards))
            start_x = (screen_width - (len(cards) * card_spacing)) // 2
            
            for i, (card_name, card_art) in enumerate(cards):
                # Floating animation
                float_offset = int(10 * math.sin(card_float_time + i * 0.5))
                card_x = start_x + i * card_spacing
                card_y_offset = card_y + float_offset
                
                # Card glow
                glow_alpha = int(100 + 50 * math.sin(glow_time + i * 0.3))
                card_glow = pygame.Surface((240, 320), pygame.SRCALPHA)
                pygame.draw.rect(card_glow, (255, 215, 0, glow_alpha), card_glow.get_rect(), 3)
                screen.blit(card_glow, (card_x - 20, card_y_offset - 20))
                
                # Card art
                screen.blit(card_art, (card_x, card_y_offset))
                
                # Card name
                font_small = pygame.font.Font(None, 24)
                name_text = font_small.render(card_name, True, (255, 215, 0))
                name_rect = name_text.get_rect(centerx=card_x + 100, y=card_y_offset + 290)
                screen.blit(name_text, name_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 36)
        instructions = [
            "Professional AI-Generated Assets",
            "Egyptian Mythology Theme",
            "Press ESC to Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (200, 200, 200))
            text_rect = text.get_rect(centerx=screen_width//2, y=50 + i * 40)
            screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    create_showcase_combat()