#!/usr/bin/env python3
"""
Test Script for Professional Sprite Animation System
Demonstrates the integration between asset pipeline and game
"""

import pygame
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sands_duat.graphics.sprite_animator import CharacterSprite, AnimationState, create_character_sprite


class SpriteAnimationDemo:
    """Demo application to test sprite animations"""
    
    def __init__(self):
        pygame.init()
        
        # Setup display
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sands of Duat - Professional Sprite Animation Demo")
        
        # Setup clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0.0
        
        # Colors
        self.bg_color = (44, 24, 16)  # Egyptian brown
        self.text_color = (218, 165, 32)  # Gold
        self.ui_color = (139, 69, 19)  # Darker brown
        
        # Font
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Create character sprite
        self.character = None
        self.load_character()
        
        # Animation control
        self.current_animation_index = 0
        self.available_animations = []
        if self.character:
            self.available_animations = self.character.get_available_animations()
        
        # UI state
        self.show_info = True
        self.animation_speed = 1.0
    
    def load_character(self):
        """Load the Anubis Guardian character"""
        try:
            self.character = create_character_sprite("anubis_guardian", "assets")
            self.character.set_position(self.screen_width // 2, self.screen_height // 2)
            self.character.set_scale(4.0)  # Large scale for demo
            print(f"[OK] Loaded character with animations: {self.character.get_available_animations()}")
        except Exception as e:
            print(f"[FAIL] Failed to load character: {e}")
            self.character = None
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    self.cycle_animation()
                
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                
                elif event.key == pygame.K_r:
                    self.restart_current_animation()
                
                elif event.key == pygame.K_f:
                    if self.character:
                        self.character.set_flip(not self.character.flip_horizontal)
                
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.animation_speed = min(3.0, self.animation_speed + 0.2)
                
                elif event.key == pygame.K_MINUS:
                    self.animation_speed = max(0.2, self.animation_speed - 0.2)
                
                elif event.key == pygame.K_1:
                    self.set_animation("idle")
                elif event.key == pygame.K_2:
                    self.set_animation("walk")
                elif event.key == pygame.K_3:
                    self.set_animation("attack")
    
    def cycle_animation(self):
        """Cycle to next available animation"""
        if not self.character or not self.available_animations:
            return
        
        self.current_animation_index = (self.current_animation_index + 1) % len(self.available_animations)
        animation_name = self.available_animations[self.current_animation_index]
        
        # Convert to AnimationState if possible
        try:
            state = AnimationState(animation_name)
            self.character.set_state(state, force_restart=True)
        except ValueError:
            print(f"Unknown animation state: {animation_name}")
    
    def set_animation(self, animation_name: str):
        """Set specific animation by name"""
        if not self.character:
            return
        
        try:
            state = AnimationState(animation_name)
            self.character.set_state(state, force_restart=True)
            
            # Update current index
            if animation_name in self.available_animations:
                self.current_animation_index = self.available_animations.index(animation_name)
        except ValueError:
            print(f"Animation '{animation_name}' not available")
    
    def restart_current_animation(self):
        """Restart the current animation"""
        if not self.character:
            return
        
        self.character.set_state(self.character.current_state, force_restart=True)
    
    def update(self):
        """Update game state"""
        if self.character:
            # Apply animation speed multiplier
            adjusted_delta = self.delta_time * self.animation_speed
            self.character.update(adjusted_delta)
    
    def render_ui(self):
        """Render UI elements"""
        if not self.show_info:
            return
        
        y_offset = 10
        
        # Title
        title_text = self.title_font.render("Professional Sprite Animation Demo", True, self.text_color)
        self.screen.blit(title_text, (10, y_offset))
        y_offset += 40
        
        # Character info
        if self.character:
            char_info = [
                f"Character: anubis_guardian",
                f"Current Animation: {self.character.current_state.value}",
                f"Animation Speed: {self.animation_speed:.1f}x",
                f"Available Animations: {len(self.available_animations)}",
                f"Scale: {self.character.scale:.1f}x",
                f"Flipped: {self.character.flip_horizontal}"
            ]
            
            for info in char_info:
                text = self.font.render(info, True, self.text_color)
                self.screen.blit(text, (10, y_offset))
                y_offset += 25
        
        y_offset += 10
        
        # Controls
        controls = [
            "Controls:",
            "SPACE - Cycle animations",
            "1/2/3 - Idle/Walk/Attack",
            "R - Restart current animation",
            "F - Flip character",
            "+/- - Animation speed",
            "I - Toggle info",
            "ESC - Exit"
        ]
        
        for control in controls:
            color = self.text_color if control != "Controls:" else (255, 255, 255)
            text = self.font.render(control, True, color)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # Animation progress bar
        if self.character and self.character.animator.current_animation:
            progress = self.character.animator.get_animation_progress()
            bar_width = 200
            bar_height = 10
            bar_x = self.screen_width - bar_width - 20
            bar_y = 20
            
            # Background
            pygame.draw.rect(self.screen, self.ui_color, 
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Progress
            progress_width = int(bar_width * progress)
            pygame.draw.rect(self.screen, self.text_color,
                           (bar_x, bar_y, progress_width, bar_height))
            
            # Label
            progress_text = self.font.render(f"Animation Progress: {progress:.1%}", True, self.text_color)
            self.screen.blit(progress_text, (bar_x, bar_y - 25))
    
    def render(self):
        """Render everything"""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Render character
        if self.character:
            self.character.render(self.screen)
        else:
            # Show error message
            error_text = self.title_font.render("Failed to load character assets", True, (255, 100, 100))
            text_rect = error_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(error_text, text_rect)
            
            info_text = self.font.render("Make sure to run the asset pipeline first:", True, (200, 200, 200))
            info_rect = info_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 40))
            self.screen.blit(info_text, info_rect)
            
            cmd_text = self.font.render("python tools/advanced_asset_pipeline.py anubis_guardian", True, (150, 150, 150))
            cmd_rect = cmd_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 65))
            self.screen.blit(cmd_text, cmd_rect)
        
        # Render UI
        self.render_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("=== Sands of Duat - Professional Sprite Animation Demo ===")
        print("Controls:")
        print("  SPACE - Cycle animations")
        print("  1/2/3 - Idle/Walk/Attack animations")
        print("  R - Restart current animation")
        print("  F - Flip character")
        print("  +/- - Adjust animation speed")
        print("  I - Toggle info display")
        print("  ESC - Exit")
        print()
        
        while self.running:
            # Calculate delta time
            self.delta_time = self.clock.tick(60) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update
            self.update()
            
            # Render
            self.render()
        
        pygame.quit()


def main():
    """Run sprite animation demo"""
    # Check if assets exist
    assets_dir = Path("assets")
    if not assets_dir.exists():
        print("Assets not found! Please run the asset pipeline first:")
        print("python tools/advanced_asset_pipeline.py all --output ./assets")
        return
    
    # Check for specific character assets
    anubis_sprites = assets_dir / "sprites"
    if not anubis_sprites.exists() or not list(anubis_sprites.glob("anubis_guardian_*.png")):
        print("Anubis Guardian sprites not found! Please generate them first:")
        print("python tools/advanced_asset_pipeline.py all --output ./assets")
        return
    
    # Run demo
    demo = SpriteAnimationDemo()
    demo.run()


if __name__ == "__main__":
    main()