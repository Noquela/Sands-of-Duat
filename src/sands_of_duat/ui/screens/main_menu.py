#!/usr/bin/env python3
"""
SANDS OF DUAT - MAIN MENU SCREEN
===============================

Main menu with authentic Egyptian temple background and premium UI elements.
Uses high-quality assets from final_dataset for temple scenes.
"""

import pygame
import sys
from pathlib import Path
from typing import Optional, Tuple

# Asset paths
ASSETS_ROOT = Path(__file__).parent.parent.parent.parent.parent / "assets"
FINAL_DATASET_PATH = ASSETS_ROOT / "images" / "lora_training" / "final_dataset"

class MainMenuScreen:
    """Premium Egyptian-themed main menu with temple background."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Egyptian color palette
        self.colors = {
            'GOLD': (255, 215, 0),
            'GOLD_DARK': (184, 134, 11),
            'LAPIS_LAZULI': (26, 81, 171),
            'PAPYRUS': (245, 245, 220),
            'DESERT_SAND': (238, 203, 173),
            'DARK_BLUE': (25, 25, 112),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'HOVER_GLOW': (255, 255, 255, 100)
        }
        
        # Load high-quality temple background
        self.background = self._load_temple_background()
        
        # Initialize fonts
        self._init_fonts()
        
        # Menu buttons
        self.buttons = self._create_menu_buttons()
        self.selected_button = 0
        self.button_hover_alpha = 0
        
        # Title animation
        self.title_glow = 0
        self.title_glow_direction = 1
        
    def _load_temple_background(self) -> pygame.Surface:
        """Load the highest quality Egyptian temple background."""
        # Try to load the temple scene backgrounds in quality order
        temple_assets = [
            "egyptian_god_scene_06_q82.png",  # Specified high-quality temple
            "egyptian_myth_09_q84.png",       # Highest quality background
            "egyptian_god_scene_02_q78.png",
            "egyptian_god_scene_09_q76.png",
            "egyptian_god_scene_10_q73.png"
        ]
        
        for asset_name in temple_assets:
            asset_path = FINAL_DATASET_PATH / asset_name
            if asset_path.exists():
                try:
                    bg_image = pygame.image.load(str(asset_path))
                    # Scale to fit screen while maintaining aspect ratio
                    return self._scale_background(bg_image)
                except pygame.error as e:
                    print(f"Could not load {asset_name}: {e}")
                    continue
        
        # Fallback to solid Egyptian background
        print("Warning: Could not load temple background, using solid color")
        fallback = pygame.Surface((self.screen_width, self.screen_height))
        fallback.fill(self.colors['DARK_BLUE'])
        return fallback
    
    def _scale_background(self, image: pygame.Surface) -> pygame.Surface:
        """Scale background image to fit screen while maintaining aspect ratio."""
        img_width, img_height = image.get_size()
        scale_x = self.screen_width / img_width
        scale_y = self.screen_height / img_height
        scale = max(scale_x, scale_y)  # Scale to cover entire screen
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        scaled_image = pygame.transform.scale(image, (new_width, new_height))
        
        # Center the image
        final_surface = pygame.Surface((self.screen_width, self.screen_height))
        x_offset = (self.screen_width - new_width) // 2
        y_offset = (self.screen_height - new_height) // 2
        final_surface.blit(scaled_image, (x_offset, y_offset))
        
        return final_surface
    
    def _init_fonts(self):
        """Initialize Egyptian-themed fonts."""
        try:
            # Try to use a more Egyptian-style font if available
            self.title_font = pygame.font.Font(None, 72)
            self.subtitle_font = pygame.font.Font(None, 32)
            self.button_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 20)
        except:
            # Fallback to default fonts
            self.title_font = pygame.font.Font(None, 72)
            self.subtitle_font = pygame.font.Font(None, 32)
            self.button_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 20)
    
    def _create_menu_buttons(self) -> list:
        """Create main menu buttons with Egyptian styling."""
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = self.screen_height // 2
        
        buttons = [
            {
                'text': 'ENTER THE UNDERWORLD',
                'action': 'start_game',
                'rect': pygame.Rect(
                    self.screen_width // 2 - button_width // 2,
                    start_y,
                    button_width,
                    button_height
                )
            },
            {
                'text': 'BUILD YOUR DECK',
                'action': 'deck_builder',
                'rect': pygame.Rect(
                    self.screen_width // 2 - button_width // 2,
                    start_y + button_spacing,
                    button_width,
                    button_height
                )
            },
            {
                'text': 'HALL OF GODS',
                'action': 'collection',
                'rect': pygame.Rect(
                    self.screen_width // 2 - button_width // 2,
                    start_y + button_spacing * 2,
                    button_width,
                    button_height
                )
            },
            {
                'text': 'SETTINGS',
                'action': 'settings',
                'rect': pygame.Rect(
                    self.screen_width // 2 - button_width // 2,
                    start_y + button_spacing * 3,
                    button_width,
                    button_height
                )
            },
            {
                'text': 'EXIT TO MORTAL REALM',
                'action': 'quit',
                'rect': pygame.Rect(
                    self.screen_width // 2 - button_width // 2,
                    start_y + button_spacing * 4,
                    button_width,
                    button_height
                )
            }
        ]
        
        return buttons
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input events and return action if button clicked."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.buttons[self.selected_button]['action']
            elif event.key == pygame.K_ESCAPE:
                return 'quit'
                
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for i, button in enumerate(self.buttons):
                if button['rect'].collidepoint(mouse_pos):
                    self.selected_button = i
                    break
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        return button['action']
        
        return None
    
    def update(self, dt: float):
        """Update animations and effects."""
        # Title glow animation
        self.title_glow += self.title_glow_direction * dt * 100
        if self.title_glow >= 50:
            self.title_glow = 50
            self.title_glow_direction = -1
        elif self.title_glow <= 0:
            self.title_glow = 0
            self.title_glow_direction = 1
        
        # Button hover effect
        if self.button_hover_alpha < 255:
            self.button_hover_alpha = min(255, self.button_hover_alpha + dt * 500)
    
    def _draw_egyptian_border(self, surface: pygame.Surface, rect: pygame.Rect, 
                             color: Tuple[int, int, int], thickness: int = 3):
        """Draw Egyptian-style decorative border."""
        # Main border
        pygame.draw.rect(surface, color, rect, thickness)
        
        # Corner decorations
        corner_size = 10
        corners = [
            rect.topleft,
            (rect.topright[0] - corner_size, rect.topright[1]),
            (rect.bottomleft[0], rect.bottomleft[1] - corner_size),
            (rect.bottomright[0] - corner_size, rect.bottomright[1] - corner_size)
        ]
        
        for corner in corners:
            pygame.draw.lines(surface, color, False, [
                (corner[0], corner[1] + corner_size),
                corner,
                (corner[0] + corner_size, corner[1])
            ], thickness)
    
    def draw(self):
        """Draw the main menu screen with Egyptian theming."""
        # Draw temple background
        self.screen.blit(self.background, (0, 0))
        
        # Add dark overlay for better text readability
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(120)
        overlay.fill(self.colors['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with glow effect
        title_text = "SANDS OF DUAT"
        title_surface = self.title_font.render(title_text, True, self.colors['GOLD'])
        
        # Glow effect
        glow_color = (*self.colors['GOLD'], int(self.title_glow))
        glow_surface = self.title_font.render(title_text, True, self.colors['GOLD'])
        glow_surface.set_alpha(int(self.title_glow))
        
        title_x = self.screen_width // 2 - title_surface.get_width() // 2
        title_y = 80
        
        # Draw glow
        for offset in range(1, 4):
            for dx, dy in [(-offset, -offset), (offset, -offset), 
                          (-offset, offset), (offset, offset)]:
                self.screen.blit(glow_surface, (title_x + dx, title_y + dy))
        
        # Draw main title
        self.screen.blit(title_surface, (title_x, title_y))
        
        # Draw subtitle
        subtitle_text = "EGYPTIAN UNDERWORLD CARD GAME"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.colors['PAPYRUS'])
        subtitle_x = self.screen_width // 2 - subtitle_surface.get_width() // 2
        self.screen.blit(subtitle_surface, (subtitle_x, title_y + 80))
        
        # Draw menu buttons
        for i, button in enumerate(self.buttons):
            is_selected = i == self.selected_button
            
            # Button background
            if is_selected:
                # Glowing selected button
                glow_rect = button['rect'].inflate(10, 10)
                pygame.draw.rect(self.screen, self.colors['GOLD_DARK'], glow_rect)
                pygame.draw.rect(self.screen, self.colors['GOLD'], glow_rect, 3)
            
            # Draw Egyptian-style border
            self._draw_egyptian_border(self.screen, button['rect'], 
                                     self.colors['GOLD'] if is_selected else self.colors['DESERT_SAND'])
            
            # Button text
            text_color = self.colors['PAPYRUS'] if is_selected else self.colors['DESERT_SAND']
            text_surface = self.button_font.render(button['text'], True, text_color)
            text_x = button['rect'].centerx - text_surface.get_width() // 2
            text_y = button['rect'].centery - text_surface.get_height() // 2
            self.screen.blit(text_surface, (text_x, text_y))
        
        # Draw version info
        version_text = "Following Master Implementation Plan | Premium Egyptian Assets"
        version_surface = self.small_font.render(version_text, True, self.colors['DESERT_SAND'])
        version_x = self.screen_width // 2 - version_surface.get_width() // 2
        self.screen.blit(version_surface, (version_x, self.screen_height - 30))


def create_main_menu(screen: pygame.Surface) -> MainMenuScreen:
    """Factory function to create main menu screen."""
    return MainMenuScreen(screen)