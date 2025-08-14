"""
Enhanced Card Hover System - Hades-Level Interactive Cards
Smooth hover effects with scaling, glow, and detailed information display.
"""

import pygame
import math
from typing import Optional, Tuple, Dict, Any
from enum import Enum, auto

from ...core.constants import Colors, Layout, FontSizes, SCREEN_WIDTH, SCREEN_HEIGHT

class HoverState(Enum):
    """Card hover interaction states."""
    NORMAL = auto()
    HOVERING = auto()
    SELECTED = auto()
    PLAYING = auto()

class EnhancedCardHover:
    """
    Professional card hover system with Hades-level visual effects.
    Features smooth scaling, glow effects, and tooltip information.
    """
    
    def __init__(self, card_rect: pygame.Rect, card_data: Dict[str, Any]):
        """
        Initialize enhanced card hover.
        
        Args:
            card_rect: Base card rectangle
            card_data: Card information (name, cost, attack, health, description)
        """
        self.base_rect = card_rect.copy()
        self.current_rect = card_rect.copy()
        self.card_data = card_data
        
        # Hover state
        self.state = HoverState.NORMAL
        self.hover_progress = 0.0      # 0.0 to 1.0
        self.selection_progress = 0.0   # 0.0 to 1.0
        self.glow_intensity = 0.0       # 0.0 to 1.0
        
        # Animation settings
        self.hover_speed = 10.0         # Fast, responsive animations
        self.scale_factor = 1.15        # How much to scale on hover
        self.hover_offset_y = -15       # Lift card up slightly
        
        # Visual effects
        self.glow_color = self._get_rarity_glow_color()
        self.glow_radius = 12
        self.has_tooltip = True
        
        # Tooltip data
        self.tooltip_surface = None
        self.tooltip_rect = None
        self._create_tooltip()
        
    def _get_rarity_glow_color(self) -> Tuple[int, int, int]:
        """Get glow color based on card rarity."""
        rarity = self.card_data.get('rarity', 'common').lower()
        
        if rarity == 'legendary':
            return Colors.GOLD
        elif rarity == 'epic':
            return Colors.PURPLE
        elif rarity == 'rare':
            return Colors.LAPIS_LAZULI
        else:
            return Colors.DESERT_SAND
            
    def _create_tooltip(self):
        """Create tooltip with card information."""
        if not self.has_tooltip:
            return
            
        # Tooltip dimensions
        tooltip_width = 300
        tooltip_padding = 15
        line_spacing = 5
        
        # Create tooltip surface
        font_title = pygame.font.Font(None, FontSizes.CARD_NAME)
        font_body = pygame.font.Font(None, FontSizes.CARD_TEXT)
        font_stats = pygame.font.Font(None, FontSizes.BODY)
        
        # Calculate required height
        lines = []
        
        # Title
        title_text = self.card_data.get('name', 'Unknown Card')
        lines.append(('title', title_text, font_title, Colors.GOLD))
        
        # Cost/Stats line
        cost = self.card_data.get('cost', 0)
        attack = self.card_data.get('attack', 0)
        health = self.card_data.get('health', 0)
        stats_text = f"Cost: {cost} | Attack: {attack} | Health: {health}"
        lines.append(('stats', stats_text, font_stats, Colors.LAPIS_LAZULI))
        
        # Empty line
        lines.append(('spacer', '', font_body, Colors.WHITE))
        
        # Description (word wrap)
        description = self.card_data.get('description', 'No description available.')
        wrapped_lines = self._wrap_text(description, font_body, tooltip_width - tooltip_padding * 2)
        for line in wrapped_lines:
            lines.append(('description', line, font_body, Colors.PAPYRUS))
            
        # Calculate total height
        total_height = tooltip_padding * 2
        for line_type, text, font, color in lines:
            if line_type == 'spacer':
                total_height += line_spacing * 2
            else:
                total_height += font.get_height() + line_spacing
                
        # Create tooltip surface
        self.tooltip_surface = pygame.Surface((tooltip_width, total_height), pygame.SRCALPHA)
        
        # Dark background with border
        bg_color = (*Colors.BACKGROUND_SECONDARY, 240)
        pygame.draw.rect(self.tooltip_surface, Colors.BACKGROUND_SECONDARY, 
                        (0, 0, tooltip_width, total_height), border_radius=8)
        pygame.draw.rect(self.tooltip_surface, self.glow_color, 
                        (0, 0, tooltip_width, total_height), width=2, border_radius=8)
        
        # Render text lines
        y_offset = tooltip_padding
        for line_type, text, font, color in lines:
            if line_type == 'spacer':
                y_offset += line_spacing * 2
            elif text:  # Skip empty lines
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect()
                
                if line_type == 'title':
                    text_rect.centerx = tooltip_width // 2
                else:
                    text_rect.x = tooltip_padding
                    
                text_rect.y = y_offset
                self.tooltip_surface.blit(text_surface, text_rect)
                y_offset += font.get_height() + line_spacing
                
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        """Wrap text to fit within specified width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            
            if font.size(line_text)[0] > max_width:
                if len(current_line) > 1:
                    # Remove last word and complete line
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word too long, force break
                    lines.append(word)
                    current_line = []
                    
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
        
    def update(self, dt: float, mouse_pos: Tuple[int, int], is_selected: bool = False) -> bool:
        """
        Update hover state and animations.
        
        Returns:
            bool: True if card is being hovered
        """
        # Check hover state
        is_hovering = self.current_rect.collidepoint(mouse_pos)
        
        # Update state
        if is_selected:
            self.state = HoverState.SELECTED
        elif is_hovering:
            self.state = HoverState.HOVERING
        else:
            self.state = HoverState.NORMAL
            
        # Update animation values
        target_hover = 1.0 if is_hovering else 0.0
        target_selection = 1.0 if is_selected else 0.0
        target_glow = 1.0 if (is_hovering or is_selected) else 0.0
        
        # Smooth animations with easing
        self.hover_progress += (target_hover - self.hover_progress) * dt * self.hover_speed
        self.selection_progress += (target_selection - self.selection_progress) * dt * self.hover_speed
        self.glow_intensity += (target_glow - self.glow_intensity) * dt * self.hover_speed
        
        # Update card rectangle with scaling and offset
        scale = 1.0 + (self.scale_factor - 1.0) * max(self.hover_progress, self.selection_progress * 0.7)
        
        scaled_width = int(self.base_rect.width * scale)
        scaled_height = int(self.base_rect.height * scale)
        
        # Hover lift effect
        offset_y = int(self.hover_offset_y * self.hover_progress)
        
        self.current_rect = pygame.Rect(
            self.base_rect.centerx - scaled_width // 2,
            self.base_rect.centery - scaled_height // 2 + offset_y,
            scaled_width,
            scaled_height
        )
        
        # Update tooltip position
        if self.tooltip_surface and is_hovering:
            self._update_tooltip_position(mouse_pos)
            
        return is_hovering
        
    def _update_tooltip_position(self, mouse_pos: Tuple[int, int]):
        """Update tooltip position based on mouse position."""
        if not self.tooltip_surface:
            return
            
        tooltip_width = self.tooltip_surface.get_width()
        tooltip_height = self.tooltip_surface.get_height()
        
        # Default position: right of mouse
        x = mouse_pos[0] + 20
        y = mouse_pos[1] - tooltip_height // 2
        
        # Keep tooltip on screen
        if x + tooltip_width > SCREEN_WIDTH - 20:
            x = mouse_pos[0] - tooltip_width - 20  # Left of mouse
            
        if y < 20:
            y = 20
        elif y + tooltip_height > SCREEN_HEIGHT - 20:
            y = SCREEN_HEIGHT - tooltip_height - 20
            
        self.tooltip_rect = pygame.Rect(x, y, tooltip_width, tooltip_height)
        
    def render_glow(self, surface: pygame.Surface):
        """Render glow effect behind the card."""
        if self.glow_intensity < 0.1:
            return
            
        # Multiple glow layers for smooth effect
        glow_alpha = int(80 * self.glow_intensity)
        glow_size = int(self.glow_radius * self.glow_intensity)
        
        glow_rect = pygame.Rect(
            self.current_rect.x - glow_size,
            self.current_rect.y - glow_size,
            self.current_rect.width + glow_size * 2,
            self.current_rect.height + glow_size * 2
        )
        
        # Create glow surface
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        
        # Render multiple glow layers
        for i in range(4):
            layer_alpha = glow_alpha // (i + 1)
            layer_offset = i * 2
            layer_rect = pygame.Rect(
                layer_offset, layer_offset,
                glow_rect.width - layer_offset * 2,
                glow_rect.height - layer_offset * 2
            )
            
            layer_surface = pygame.Surface((layer_rect.width, layer_rect.height), pygame.SRCALPHA)
            layer_surface.fill(self.glow_color)
            layer_surface.set_alpha(layer_alpha)
            glow_surface.blit(layer_surface, (layer_rect.x, layer_rect.y))
            
        surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
        
    def render_tooltip(self, surface: pygame.Surface):
        """Render tooltip if hovering."""
        if (self.state == HoverState.HOVERING and self.tooltip_surface and 
            self.tooltip_rect and self.hover_progress > 0.7):
            
            # Fade in tooltip
            tooltip_alpha = int(255 * min(1.0, (self.hover_progress - 0.7) / 0.3))
            tooltip_surface = self.tooltip_surface.copy()
            tooltip_surface.set_alpha(tooltip_alpha)
            
            surface.blit(tooltip_surface, self.tooltip_rect)
            
    def get_render_rect(self) -> pygame.Rect:
        """Get current render rectangle for the card."""
        return self.current_rect