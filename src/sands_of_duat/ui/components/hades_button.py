"""
Hades-Level Button Component
Professional 3-state button system inspired by AAA games.
"""

import pygame
import math
from typing import Optional, Callable, Tuple
from enum import Enum, auto

from ...core.constants import Colors, Layout, FontSizes

class ButtonState(Enum):
    """Button interaction states."""
    NORMAL = auto()
    HOVER = auto()
    PRESSED = auto()
    DISABLED = auto()

class HadesButton:
    """
    Professional button with Hades-level polish and Egyptian theming.
    Features smooth 3-state animations, glow effects, and hierarchical styling.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 theme_color: Tuple[int, int, int] = None, hieroglyph: str = "", 
                 on_click: Optional[Callable] = None):
        """
        Initialize Hades-style button.
        
        Args:
            x, y: Position
            width, height: Dimensions  
            text: Button text
            theme_color: Primary theme color (defaults to GOLD)
            hieroglyph: Egyptian symbol for decoration
            on_click: Callback function
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hieroglyph = hieroglyph
        self.on_click = on_click
        
        # Convenience properties for compatibility
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Theme colors
        self.theme_color = theme_color or Colors.GOLD
        self._setup_color_scheme()
        
        # Animation state
        self.state = ButtonState.NORMAL
        self.hover_progress = 0.0      # 0.0 to 1.0
        self.press_progress = 0.0      # 0.0 to 1.0
        self.glow_intensity = 0.0      # 0.0 to 1.0
        self.scale_factor = 1.0        # Scale multiplier
        
        # Timing constants
        self.hover_speed = 8.0         # Animation speed
        self.press_speed = 12.0
        self.glow_speed = 6.0
        
        # Visual effects
        self.has_glow = True
        self.has_scale = True
        self.has_sound = True
        
    def _setup_color_scheme(self):
        """Setup color scheme based on theme color."""
        # Background colors - Egyptian themed
        if self.theme_color == Colors.GOLD:
            self.bg_normal = (45, 35, 15)      # Rich golden brown
            self.bg_hover = (65, 50, 25)       # Brighter golden
            self.bg_pressed = (35, 25, 10)     # Darker pressed
        elif self.theme_color == Colors.LAPIS_LAZULI:
            self.bg_normal = (15, 25, 45)      # Rich lapis
            self.bg_hover = (25, 40, 65)       # Brighter lapis
            self.bg_pressed = (10, 20, 35)     # Darker pressed
        elif self.theme_color == Colors.PURPLE:
            self.bg_normal = (35, 15, 45)      # Rich purple
            self.bg_hover = (50, 25, 65)       # Brighter purple
            self.bg_pressed = (25, 10, 35)     # Darker pressed
        elif self.theme_color == Colors.RED:
            self.bg_normal = (45, 15, 15)      # Rich red
            self.bg_hover = (65, 25, 25)       # Brighter red
            self.bg_pressed = (35, 10, 10)     # Darker pressed
        else:
            # Fallback scheme
            self.bg_normal = (35, 35, 45)
            self.bg_hover = (50, 50, 65)
            self.bg_pressed = (25, 25, 35)
            
        # Border and accent colors
        self.border_color = self._darken_color(self.theme_color, 0.4)
        self.text_color = Colors.PAPYRUS
        self.glow_color = (*self.theme_color, 80)  # With alpha
        
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> bool:
        """
        Update button state and animations.
        
        Returns:
            bool: True if button was clicked this frame
        """
        # Check hover state
        was_hovered = self.state == ButtonState.HOVER
        is_hovered = self.rect.collidepoint(mouse_pos)
        is_pressed = is_hovered and mouse_pressed
        
        # Update state
        old_state = self.state
        if is_pressed:
            self.state = ButtonState.PRESSED
        elif is_hovered:
            self.state = ButtonState.HOVER
        else:
            self.state = ButtonState.NORMAL
            
        # Smooth animations with easing
        target_hover = 1.0 if is_hovered else 0.0
        target_press = 1.0 if is_pressed else 0.0
        target_glow = 1.0 if (is_hovered or is_pressed) else 0.0
        
        # Ease-out animation for smoothness
        self.hover_progress += (target_hover - self.hover_progress) * dt * self.hover_speed
        self.press_progress += (target_press - self.press_progress) * dt * self.press_speed
        self.glow_intensity += (target_glow - self.glow_intensity) * dt * self.glow_speed
        
        # Scale animation (subtle)
        if self.has_scale:
            if is_pressed:
                self.scale_factor = 0.98  # Slight shrink when pressed
            elif is_hovered:
                self.scale_factor = 1.02  # Slight grow on hover
            else:
                self.scale_factor = 1.0
                
        # Handle button click detection
        clicked = False
        
        # Detect click: mouse was pressed and is now released while over button
        if old_state == ButtonState.PRESSED and self.state == ButtonState.HOVER:
            # Button was clicked!
            if self.on_click:
                self.on_click()
            clicked = True
            
        # Sound effects (placeholder for audio system)
        if self.has_sound:
            if old_state != ButtonState.HOVER and self.state == ButtonState.HOVER:
                # Play hover sound
                pass  # TODO: self.audio_manager.play_sfx("button_hover")
            elif clicked:
                # Play click sound
                pass  # TODO: self.audio_manager.play_sfx("button_click")
                
        return clicked
        
    def render(self, surface: pygame.Surface, font: pygame.font.Font):
        """Render button with Hades-level visual effects."""
        # Calculate current rect with scaling
        scaled_width = int(self.rect.width * self.scale_factor)
        scaled_height = int(self.rect.height * self.scale_factor)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Background color interpolation
        bg_color = self._interpolate_colors(
            self.bg_normal, 
            self.bg_hover, 
            self.hover_progress
        )
        
        # Press effect
        if self.press_progress > 0.1:
            bg_color = self._interpolate_colors(
                bg_color,
                self.bg_pressed,
                self.press_progress * 0.6
            )
            
        # Glow effect (rendered first, behind button)
        if self.has_glow and self.glow_intensity > 0.1:
            self._render_glow(surface, scaled_rect)
            
        # Main button background
        pygame.draw.rect(surface, bg_color, scaled_rect, border_radius=8)
        
        # Gradient overlay for depth
        gradient_rect = pygame.Rect(scaled_rect.x, scaled_rect.y, 
                                  scaled_rect.width, scaled_rect.height // 3)
        gradient_color = self._brighten_color(bg_color, 0.2)
        pygame.draw.rect(surface, gradient_color, gradient_rect, border_radius=8)
        
        # Border with theme color intensity
        border_intensity = 0.5 + 0.5 * self.hover_progress
        border_color = self._interpolate_colors(
            self.border_color, 
            self.theme_color, 
            border_intensity
        )
        pygame.draw.rect(surface, border_color, scaled_rect, width=2, border_radius=8)
        
        # Accent line animation (Egyptian style)
        if self.hover_progress > 0.1:
            accent_width = int(scaled_rect.width * self.hover_progress * 0.8)
            accent_x = scaled_rect.centerx - accent_width // 2
            accent_rect = pygame.Rect(accent_x, scaled_rect.bottom - 4, accent_width, 2)
            pygame.draw.rect(surface, self.theme_color, accent_rect, border_radius=1)
            
        # Hieroglyph decoration
        if self.hieroglyph:
            self._render_hieroglyph(surface, scaled_rect, font)
            
        # Text rendering with shadow
        self._render_text(surface, scaled_rect, font)
        
    def _render_glow(self, surface: pygame.Surface, rect: pygame.Rect):
        """Render subtle glow effect around button."""
        glow_size = int(8 * self.glow_intensity)
        glow_rect = pygame.Rect(
            rect.x - glow_size, rect.y - glow_size,
            rect.width + glow_size * 2, rect.height + glow_size * 2
        )
        
        # Create glow surface
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        glow_alpha = int(50 * self.glow_intensity)
        
        # Multiple glow layers for smooth effect
        for i in range(3):
            layer_alpha = glow_alpha // (i + 1)
            layer_color = (*self.theme_color, layer_alpha)
            layer_rect = pygame.Rect(
                i * 2, i * 2, 
                glow_rect.width - i * 4, glow_rect.height - i * 4
            )
            glow_layer = pygame.Surface((layer_rect.width, layer_rect.height), pygame.SRCALPHA)
            glow_layer.fill(self.theme_color)
            glow_layer.set_alpha(layer_alpha)
            glow_surface.blit(glow_layer, (layer_rect.x, layer_rect.y))
            
        surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
    def _render_hieroglyph(self, surface: pygame.Surface, rect: pygame.Rect, font: pygame.font.Font):
        """Render hieroglyph decoration."""
        try:
            # Hieroglyph in theme color
            hieroglyph_size = int(font.get_height() * 1.1)
            hieroglyph_font = pygame.font.Font(None, hieroglyph_size)
            hieroglyph_surface = hieroglyph_font.render(self.hieroglyph, True, self.theme_color)
            
            # Position on left side
            hieroglyph_rect = hieroglyph_surface.get_rect()
            hieroglyph_rect.centery = rect.centery
            hieroglyph_rect.x = rect.x + 12
            
            # Shadow for hieroglyph
            shadow_surface = hieroglyph_font.render(self.hieroglyph, True, (0, 0, 0))
            shadow_surface.set_alpha(100)
            surface.blit(shadow_surface, (hieroglyph_rect.x + 1, hieroglyph_rect.y + 1))
            
            # Main hieroglyph
            surface.blit(hieroglyph_surface, hieroglyph_rect)
        except:
            pass  # Fail silently if hieroglyph can't render
            
    def _render_text(self, surface: pygame.Surface, rect: pygame.Rect, font: pygame.font.Font):
        """Render button text with shadow and press effect."""
        # Text positioning (offset for hieroglyph if present)
        text_offset_x = 35 if self.hieroglyph else 15
        
        # Press animation - slight text movement
        press_offset_y = int(self.press_progress * 1.5)
        
        # Render text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.centery = rect.centery + press_offset_y
        text_rect.x = rect.x + text_offset_x
        
        # Text shadow for better readability
        shadow_surface = font.render(self.text, True, (0, 0, 0))
        shadow_surface.set_alpha(120)
        surface.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        
        # Main text
        surface.blit(text_surface, text_rect)
        
    def _interpolate_colors(self, color1: Tuple[int, int, int], 
                           color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Linear interpolation between two colors."""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
        
    def _darken_color(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Darken a color by a factor (0.0 = black, 1.0 = original)."""
        return tuple(int(c * factor) for c in color)
        
    def _brighten_color(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Brighten a color by a factor."""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color)