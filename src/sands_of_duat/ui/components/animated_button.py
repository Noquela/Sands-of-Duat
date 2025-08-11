"""
Animated Egyptian Button - Hades-level button animations.
Professional button component with smooth hover effects and Egyptian theming.
"""

import pygame
import math
from typing import Tuple, Optional, Callable
from enum import Enum, auto

from ...core.constants import Colors, Timing, FontSizes, Layout
from ..effects.advanced_visual_effects import advanced_visual_effects

class ButtonState(Enum):
    """Button interaction states."""
    NORMAL = auto()
    HOVERED = auto()
    PRESSED = auto()
    DISABLED = auto()

class AnimatedButton:
    """
    Professional animated button with Egyptian theming and Hades-level polish.
    Features smooth hover animations, glow effects, and satisfying feedback.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, font_size: int = FontSizes.BUTTON,
                 action: Optional[Callable] = None):
        """
        Initialize animated button.
        
        Args:
            x, y: Position coordinates
            width, height: Button dimensions
            text: Button text
            font_size: Text font size
            action: Callback function when clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        
        # Visual state
        self.state = ButtonState.NORMAL
        self.hover_progress = 0.0
        self.press_progress = 0.0
        self.glow_intensity = 0.0
        self.is_hovered = False
        
        # Animation timings
        self.hover_animation_time = 0.0
        self.press_animation_time = 0.0
        self.glow_animation_time = 0.0
        
        # Font rendering
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, Colors.PAPYRUS)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
        # Sound effects (will be implemented in audio sprint)
        self.hover_sound = None
        self.click_sound = None
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool):
        """
        Update button animations and state.
        
        Args:
            dt: Delta time in seconds
            mouse_pos: Current mouse position
            mouse_pressed: Whether mouse button is pressed
        """
        # Check if mouse is over button
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Update state
        if mouse_pressed and self.is_hovered:
            self.state = ButtonState.PRESSED
        elif self.is_hovered:
            self.state = ButtonState.HOVERED
        else:
            self.state = ButtonState.NORMAL
        
        # Play hover sound effect and trigger visual effects
        if self.is_hovered and not was_hovered:
            # Add button glow effect
            advanced_visual_effects.add_button_glow(
                self.rect.x, self.rect.y, self.rect.width, self.rect.height,
                Colors.GOLD, intensity=0.8, duration=1.5
            )
            
            if self.hover_sound:
                # self.hover_sound.play()
                pass
        
        # Update animations
        self._update_hover_animation(dt, self.is_hovered)
        self._update_press_animation(dt, mouse_pressed and self.is_hovered)
        self._update_glow_animation(dt)
    
    def _update_hover_animation(self, dt: float, is_hovered: bool):
        """Update hover animation progress."""
        target_progress = 1.0 if is_hovered else 0.0
        speed = 1.0 / Timing.BUTTON_HOVER_DURATION
        
        if self.hover_progress < target_progress:
            self.hover_progress = min(target_progress, self.hover_progress + speed * dt)
        elif self.hover_progress > target_progress:
            self.hover_progress = max(target_progress, self.hover_progress - speed * dt)
    
    def _update_press_animation(self, dt: float, is_pressed: bool):
        """Update press animation progress."""
        target_progress = 1.0 if is_pressed else 0.0
        speed = 8.0  # Fast press animation
        
        if self.press_progress < target_progress:
            self.press_progress = min(target_progress, self.press_progress + speed * dt)
        elif self.press_progress > target_progress:
            self.press_progress = max(target_progress, self.press_progress - speed * dt)
    
    def _update_glow_animation(self, dt: float):
        """Update glow pulsing animation."""
        self.glow_animation_time += dt
        # Gentle pulsing glow
        self.glow_intensity = 0.3 + 0.2 * math.sin(self.glow_animation_time * 2.0)
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Handle mouse click event.
        
        Args:
            mouse_pos: Mouse click position
            
        Returns:
            True if button was clicked
        """
        if self.rect.collidepoint(mouse_pos) and self.state != ButtonState.DISABLED:
            # Add click visual effects
            advanced_visual_effects.add_energy_pulse(
                self.rect.centerx, self.rect.centery, 
                max_radius=60, color=Colors.LAPIS_LAZULI
            )
            
            # Add crystal shine effect
            advanced_visual_effects.add_crystal_shine(
                self.rect.x, self.rect.y, self.rect.width, self.rect.height
            )
            
            if self.click_sound:
                # self.click_sound.play()
                pass
            
            if self.action:
                self.action()
            
            return True
        return False
    
    def render(self, surface: pygame.Surface):
        """
        Render the animated button with all effects.
        
        Args:
            surface: Surface to render to
        """
        # Calculate animated properties
        scale_factor = 1.0 + (self.hover_progress * 0.05) - (self.press_progress * 0.02)
        glow_alpha = int(self.glow_intensity * 255 * self.hover_progress)
        
        # Calculate scaled rect
        scaled_width = int(self.rect.width * scale_factor)
        scaled_height = int(self.rect.height * scale_factor)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Render glow effect
        if self.hover_progress > 0:
            self._render_glow(surface, scaled_rect, glow_alpha)
        
        # Render button background
        self._render_background(surface, scaled_rect)
        
        # Render border
        self._render_border(surface, scaled_rect)
        
        # Render text
        self._render_text(surface, scaled_rect)
    
    def _render_glow(self, surface: pygame.Surface, rect: pygame.Rect, alpha: int):
        """Render button glow effect."""
        if alpha <= 0:
            return
        
        glow_size = 8
        glow_rect = rect.inflate(glow_size * 2, glow_size * 2)
        
        # Create glow surface
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
        glow_surface.set_alpha(alpha)
        
        # Draw glow gradient (simplified version)
        for i in range(glow_size):
            alpha_step = alpha * (1.0 - i / glow_size)
            color = (*Colors.GOLD, int(alpha_step))
            
            glow_inner_rect = pygame.Rect(
                i, i,
                glow_rect.width - i * 2,
                glow_rect.height - i * 2
            )
            pygame.draw.rect(glow_surface, Colors.GOLD, glow_inner_rect, 1)
        
        surface.blit(glow_surface, glow_rect.topleft)
    
    def _render_background(self, surface: pygame.Surface, rect: pygame.Rect):
        """Render button background."""
        # Button colors based on state
        if self.state == ButtonState.PRESSED:
            bg_color = Colors.GOLD_DARK
        elif self.state == ButtonState.HOVERED:
            bg_color = Colors.LAPIS_LAZULI
        elif self.state == ButtonState.DISABLED:
            bg_color = Colors.BUTTON_DISABLED
        else:
            bg_color = Colors.DARK_BLUE
        
        # Add transparency based on hover
        alpha = int(200 + (self.hover_progress * 55))
        
        # Create background surface with alpha
        bg_surface = pygame.Surface((rect.width, rect.height))
        bg_surface.set_alpha(alpha)
        bg_surface.fill(bg_color)
        
        surface.blit(bg_surface, rect.topleft)
    
    def _render_border(self, surface: pygame.Surface, rect: pygame.Rect):
        """Render button border with Egyptian styling."""
        # Border color based on state
        if self.state == ButtonState.PRESSED:
            border_color = Colors.PAPYRUS
        elif self.state == ButtonState.HOVERED:
            border_color = Colors.GOLD
        else:
            border_color = Colors.DESERT_SAND
        
        # Main border
        border_width = 2 + int(self.hover_progress * 2)
        pygame.draw.rect(surface, border_color, rect, border_width)
        
        # Corner decorations (Egyptian style)
        corner_size = 8 + int(self.hover_progress * 4)
        self._draw_egyptian_corners(surface, rect, border_color, corner_size)
    
    def _draw_egyptian_corners(self, surface: pygame.Surface, rect: pygame.Rect, 
                              color: Tuple[int, int, int], size: int):
        """Draw Egyptian-style corner decorations."""
        corners = [
            (rect.left, rect.top),
            (rect.right - size, rect.top),
            (rect.left, rect.bottom - size),
            (rect.right - size, rect.bottom - size)
        ]
        
        for corner in corners:
            # Draw small L-shaped corner decoration
            lines = [
                [(corner[0], corner[1] + size), corner, (corner[0] + size, corner[1])]
            ]
            for line in lines:
                pygame.draw.lines(surface, color, False, line, 2)
    
    def _render_text(self, surface: pygame.Surface, rect: pygame.Rect):
        """Render button text."""
        # Text color based on state
        if self.state == ButtonState.PRESSED:
            text_color = Colors.DARK_BLUE
        elif self.state == ButtonState.HOVERED:
            text_color = Colors.PAPYRUS
        elif self.state == ButtonState.DISABLED:
            text_color = Colors.DESERT_SAND
        else:
            text_color = Colors.PAPYRUS
        
        # Re-render text if color changed
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        
        # Add subtle text shadow for depth
        if self.state != ButtonState.DISABLED:
            shadow_surface = self.font.render(self.text, True, Colors.BLACK)
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            surface.blit(shadow_surface, shadow_rect)
        
        surface.blit(text_surface, text_rect)
    
    def set_position(self, x: int, y: int):
        """Update button position."""
        self.rect.x = x
        self.rect.y = y
        self.text_rect.center = self.rect.center
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the button."""
        if enabled:
            self.state = ButtonState.NORMAL
        else:
            self.state = ButtonState.DISABLED