"""
Responsive Components - UI elements that automatically adapt to screen size.
Built on top of the ultrawide layout system for consistent scaling.
"""

import pygame
from typing import Tuple, Optional, Callable
from ...core.constants import Colors
from .scaling_manager import scaling_manager

class ResponsiveButton:
    """Button that automatically scales for ultrawide and 4K displays."""
    
    def __init__(self, text: str, button_type: str = 'default', 
                 action: Optional[Callable] = None, zone: str = 'center_content'):
        self.text = text
        self.button_type = button_type
        self.action = action
        self.zone = zone
        
        # Get scaled dimensions
        self.width, self.height = scaling_manager.get_component_size(f'button_{button_type}')
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.hover_scale = 1.0
        self.hover_target_scale = 1.0
        
        # Position (will be set externally)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Colors
        self.colors = {
            'normal': Colors.LAPIS_LAZULI,
            'hover': Colors.GOLD,
            'pressed': Colors.DESERT_SAND,
            'text': Colors.PAPYRUS,
            'text_hover': Colors.DARK_BLUE
        }
    
    def set_position(self, x: int, y: int):
        """Set button position."""
        self.rect.x = x
        self.rect.y = y
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_pressed: bool, events):
        """Update button state and animations."""
        # Check if mouse is over button
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Update hover animation
        if self.is_hovered:
            self.hover_target_scale = 1.05
        else:
            self.hover_target_scale = 1.0
        
        # Smooth scale animation
        scale_speed = 8.0
        scale_diff = self.hover_target_scale - self.hover_scale
        self.hover_scale += scale_diff * scale_speed * dt
        
        # Handle clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.is_hovered:  # Left click
                    self.is_pressed = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    if self.is_pressed and self.is_hovered and self.action:
                        self.action()
                    self.is_pressed = False
    
    def render(self, surface: pygame.Surface):
        """Render the button with scaling and hover effects."""
        # Calculate scaled dimensions for hover effect
        scaled_width = int(self.width * self.hover_scale)
        scaled_height = int(self.height * self.hover_scale)
        
        # Center the scaled button
        scaled_x = self.rect.x + (self.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.height - scaled_height) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Choose color based on state
        if self.is_pressed:
            bg_color = self.colors['pressed']
            text_color = self.colors['text']
        elif self.is_hovered:
            bg_color = self.colors['hover']
            text_color = self.colors['text_hover']
        else:
            bg_color = self.colors['normal']
            text_color = self.colors['text']
        
        # Draw button background with subtle gradient effect
        pygame.draw.rect(surface, bg_color, scaled_rect, border_radius=8)
        
        # Add border
        border_color = Colors.GOLD if self.is_hovered else Colors.PAPYRUS
        pygame.draw.rect(surface, border_color, scaled_rect, width=2, border_radius=8)
        
        # Draw text centered
        font = scaling_manager.get_font('button')
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)

class ResponsiveCard:
    """Card component that scales properly for ultrawide displays."""
    
    def __init__(self, card_data: dict, card_size: str = 'medium'):
        self.card_data = card_data
        self.card_size = card_size
        
        # Get scaled dimensions
        self.width, self.height = scaling_manager.get_component_size(f'card_{card_size}')
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Animation state
        self.hover_scale = 1.0
        self.hover_target_scale = 1.0
        self.is_hovered = False
        
        # Colors based on rarity
        rarity_colors = {
            'common': Colors.PAPYRUS,
            'rare': Colors.LAPIS_LAZULI,
            'epic': Colors.AMETHYST,  
            'legendary': Colors.GOLD
        }
        self.border_color = rarity_colors.get(card_data.get('rarity', 'common'), Colors.PAPYRUS)
    
    def set_position(self, x: int, y: int):
        """Set card position."""
        self.rect.x = x
        self.rect.y = y
    
    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        """Update card hover animations."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Update hover scale
        if self.is_hovered:
            self.hover_target_scale = 1.1
        else:
            self.hover_target_scale = 1.0
        
        # Smooth animation
        scale_speed = 6.0
        scale_diff = self.hover_target_scale - self.hover_scale
        self.hover_scale += scale_diff * scale_speed * dt
    
    def render(self, surface: pygame.Surface):
        """Render the card with proper scaling."""
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.hover_scale)
        scaled_height = int(self.height * self.hover_scale)
        
        scaled_x = self.rect.x + (self.width - scaled_width) // 2
        scaled_y = self.rect.y + (self.height - scaled_height) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Card background
        card_bg = Colors.DARK_BLUE if self.is_hovered else (20, 20, 40)
        pygame.draw.rect(surface, card_bg, scaled_rect, border_radius=8)
        
        # Card border (animated for rarity)
        border_width = 3 if self.is_hovered else 2
        pygame.draw.rect(surface, self.border_color, scaled_rect, 
                        width=border_width, border_radius=8)
        
        # Card content
        self._render_card_content(surface, scaled_rect)
    
    def _render_card_content(self, surface: pygame.Surface, card_rect: pygame.Rect):
        """Render card name, cost, and other details."""
        margin = scaling_manager.scale_value(8)
        
        # Card name
        name = self.card_data.get('name', 'Unknown Card')
        name_font = scaling_manager.get_font('small')
        name_surface = name_font.render(name, True, Colors.PAPYRUS)
        name_rect = pygame.Rect(
            card_rect.x + margin, card_rect.y + margin,
            card_rect.width - 2 * margin, scaling_manager.scale_value(20)
        )
        # Clip text if too long
        surface.blit(name_surface, name_rect, area=pygame.Rect(0, 0, name_rect.width, name_rect.height))
        
        # Cost (top right corner)
        cost = str(self.card_data.get('cost', 0))
        cost_font = scaling_manager.get_font('button')
        cost_surface = cost_font.render(cost, True, Colors.GOLD)
        cost_rect = cost_surface.get_rect()
        cost_rect.topright = (card_rect.right - margin, card_rect.top + margin)
        surface.blit(cost_surface, cost_rect)

class ResponsiveHealthBar:
    """Health/Mana bar that scales properly for different resolutions."""
    
    def __init__(self, max_value: int, bar_type: str = 'health'):
        self.max_value = max_value
        self.current_value = max_value
        self.bar_type = bar_type
        
        # Get scaled dimensions
        component_name = f'{bar_type}_bar'
        self.width, self.height = scaling_manager.get_component_size(component_name)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Animation
        self.display_value = float(max_value)
        self.target_value = float(max_value)
        
        # Colors
        if bar_type == 'health':
            self.colors = {
                'bg': (60, 20, 20),
                'fill': Colors.RED,
                'border': Colors.PAPYRUS
            }
        else:  # mana
            self.colors = {
                'bg': (20, 20, 60),
                'fill': Colors.LAPIS_LAZULI,
                'border': Colors.PAPYRUS
            }
    
    def set_position(self, x: int, y: int):
        """Set bar position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_value(self, value: int):
        """Set current value (will animate to this value)."""
        self.current_value = max(0, min(value, self.max_value))
        self.target_value = float(self.current_value)
    
    def update(self, dt: float):
        """Update bar animation."""
        # Smooth value animation
        value_speed = 100.0  # units per second
        value_diff = self.target_value - self.display_value
        
        if abs(value_diff) > 0.1:
            move_amount = value_speed * dt
            if value_diff > 0:
                self.display_value = min(self.display_value + move_amount, self.target_value)
            else:
                self.display_value = max(self.display_value - move_amount, self.target_value)
    
    def render(self, surface: pygame.Surface):
        """Render the health/mana bar."""
        # Background
        pygame.draw.rect(surface, self.colors['bg'], self.rect, border_radius=4)
        
        # Fill (current value)
        if self.max_value > 0:
            fill_ratio = self.display_value / self.max_value
            fill_width = int(self.rect.width * fill_ratio)
            
            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
                pygame.draw.rect(surface, self.colors['fill'], fill_rect, border_radius=4)
        
        # Border
        pygame.draw.rect(surface, self.colors['border'], self.rect, width=2, border_radius=4)
        
        # Text (value/max_value)
        text = f"{int(self.display_value)}/{self.max_value}"
        font = scaling_manager.get_font('small')
        text_surface = font.render(text, True, Colors.PAPYRUS)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class ResponsiveTurnIndicator:
    """Turn indicator that's clearly visible on any screen size."""
    
    def __init__(self):
        self.width, self.height = scaling_manager.scale_value(200), scaling_manager.scale_value(40)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        self.is_player_turn = True
        self.flash_timer = 0.0
        self.flash_intensity = 0.0
    
    def set_position(self, x: int, y: int):
        """Set indicator position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_turn(self, is_player_turn: bool):
        """Set whose turn it is."""
        if self.is_player_turn != is_player_turn:
            self.is_player_turn = is_player_turn
            self.flash_timer = 1.0  # Flash for 1 second when turn changes
    
    def update(self, dt: float):
        """Update turn indicator animations."""
        # Update flash animation
        if self.flash_timer > 0:
            self.flash_timer -= dt
            self.flash_intensity = max(0, self.flash_timer)
        else:
            self.flash_intensity = 0
    
    def render(self, surface: pygame.Surface):
        """Render the turn indicator."""
        # Background with flash effect
        base_color = Colors.GOLD if self.is_player_turn else Colors.RED
        
        if self.flash_intensity > 0:
            # Add white flash when turn changes
            flash_amount = int(100 * self.flash_intensity)
            bg_color = (
                min(255, base_color[0] + flash_amount),
                min(255, base_color[1] + flash_amount), 
                min(255, base_color[2] + flash_amount)
            )
        else:
            bg_color = base_color
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, Colors.PAPYRUS, self.rect, width=2, border_radius=8)
        
        # Text
        text = "YOUR TURN" if self.is_player_turn else "ENEMY TURN"
        font = scaling_manager.get_font('button')
        text_surface = font.render(text, True, Colors.DARK_BLUE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)