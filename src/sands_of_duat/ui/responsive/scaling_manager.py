"""
Scaling Manager - Handles all UI scaling operations for responsive design.
Provides unified scaling interface for fonts, components, and layouts.
"""

import pygame
from typing import Tuple, Dict, Optional
from .ultrawide_layout import ultrawide_layout

class ScalingManager:
    """Manages all UI scaling operations for consistent responsive design."""
    
    def __init__(self):
        self.layout = ultrawide_layout
        
        # Font scaling cache
        self._font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        
        # Standard font sizes (will be scaled automatically)
        self.font_sizes = {
            'debug': 12,
            'small': 14,
            'body': 16,
            'button': 18,
            'subtitle': 24,
            'title_medium': 32,
            'title_large': 48,
            'title_huge': 72
        }
        
        # Component base sizes
        self.component_sizes = {
            'button_default': (200, 50),
            'button_wide': (300, 60),
            'button_large': (250, 70),
            'card_small': (80, 112),
            'card_medium': (120, 168),
            'card_large': (160, 224),
            'health_bar': (200, 20),
            'mana_bar': (150, 16)
        }
    
    def get_font(self, font_type: str = 'body', custom_size: Optional[int] = None) -> pygame.font.Font:
        """Get a properly scaled font."""
        # Use custom size or predefined size
        base_size = custom_size if custom_size else self.font_sizes.get(font_type, 16)
        scaled_size = self.layout.scale_font_size(base_size)
        
        # Check cache first
        cache_key = (font_type, scaled_size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Create new font and cache it
        font = pygame.font.Font(None, scaled_size)  # Using default font for now
        self._font_cache[cache_key] = font
        
        return font
    
    def get_component_size(self, component_type: str) -> Tuple[int, int]:
        """Get properly scaled component size."""
        if component_type not in self.component_sizes:
            return self.layout.scale_size(100, 30)  # Default fallback
        
        base_width, base_height = self.component_sizes[component_type]
        return self.layout.scale_size(base_width, base_height)
    
    def scale_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Scale a rect proportionally."""
        width, height = self.layout.scale_size(rect.width, rect.height)
        return pygame.Rect(rect.x, rect.y, width, height)
    
    def scale_value(self, value: int, scale_type: str = 'ui') -> int:
        """Scale a single value."""
        if scale_type == 'ui':
            return int(value * self.layout.ui_scale_factor * self.layout.resolution_scale)
        elif scale_type == 'font':
            return self.layout.scale_font_size(value)
        elif scale_type == 'spacing':
            return int(value * self.layout.card_spacing_factor * self.layout.resolution_scale)
        else:
            return int(value * self.layout.resolution_scale)
    
    def get_button_layout(self, button_count: int, button_type: str = 'default', 
                         zone: str = 'center_content') -> list[Tuple[int, int]]:
        """Get positions for a set of buttons with proper spacing."""
        button_width, button_height = self.get_component_size(f'button_{button_type}')
        spacing = self.scale_value(20, 'spacing')
        
        # Calculate total height needed
        total_height = (button_count * button_height) + ((button_count - 1) * spacing)
        
        # Get zone info
        zone_rect = self.layout.zones.get(zone, self.layout.content_area)
        start_y = zone_rect.y + (zone_rect.height - total_height) // 2
        center_x = zone_rect.x + zone_rect.width // 2
        
        # Calculate positions
        positions = []
        for i in range(button_count):
            x = center_x - button_width // 2
            y = start_y + i * (button_height + spacing)
            positions.append((x, y))
        
        return positions
    
    def get_card_grid_layout(self, card_count: int, cards_per_row: int = 5, 
                           zone: str = 'center_content') -> list[Tuple[int, int]]:
        """Get positions for cards in a grid layout."""
        card_width, card_height = self.get_component_size('card_medium')
        spacing = self.layout.get_card_spacing()
        
        # Calculate grid dimensions
        rows = (card_count + cards_per_row - 1) // cards_per_row
        
        # Total dimensions
        total_width = (cards_per_row * card_width) + ((cards_per_row - 1) * spacing)
        total_height = (rows * card_height) + ((rows - 1) * spacing)
        
        # Starting position (centered in zone)
        zone_rect = self.layout.zones.get(zone, self.layout.content_area)
        start_x = zone_rect.x + (zone_rect.width - total_width) // 2
        start_y = zone_rect.y + (zone_rect.height - total_height) // 2
        
        # Generate positions
        positions = []
        for i in range(card_count):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            positions.append((x, y))
        
        return positions
    
    def create_responsive_surface(self, base_width: int, base_height: int) -> pygame.Surface:
        """Create a surface with responsive dimensions."""
        width, height = self.layout.scale_size(base_width, base_height)
        return pygame.Surface((width, height), pygame.SRCALPHA)
    
    def draw_scaled_text(self, surface: pygame.Surface, text: str, position: Tuple[int, int],
                        font_type: str = 'body', color: Tuple[int, int, int] = (255, 255, 255),
                        center: bool = False) -> pygame.Rect:
        """Draw text with proper scaling and positioning."""
        font = self.get_font(font_type)
        text_surface = font.render(text, True, color)
        
        if center:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)
        
        surface.blit(text_surface, text_rect)
        return text_rect
    
    def get_hud_layout(self) -> Dict[str, pygame.Rect]:
        """Get HUD element positions for combat screen."""
        # Top HUD: Health, mana, turn indicator
        top_zone = self.layout.zones['top_hud']
        
        # Bottom HUD: Action buttons
        bottom_zone = self.layout.zones['bottom_hud']
        
        # Health bar (top left)
        health_width, health_height = self.get_component_size('health_bar')
        health_rect = pygame.Rect(
            top_zone.x + self.scale_value(20),
            top_zone.y + (top_zone.height - health_height) // 2,
            health_width, health_height
        )
        
        # Mana bar (top right) 
        mana_width, mana_height = self.get_component_size('mana_bar')
        mana_rect = pygame.Rect(
            top_zone.right - mana_width - self.scale_value(20),
            top_zone.y + (top_zone.height - mana_height) // 2,
            mana_width, mana_height
        )
        
        # Turn indicator (top center)
        turn_rect = pygame.Rect(
            top_zone.x + top_zone.width // 2 - self.scale_value(100),
            top_zone.y + self.scale_value(10),
            self.scale_value(200), self.scale_value(30)
        )
        
        # Action buttons (bottom right)
        button_width, button_height = self.get_component_size('button_default')
        action_button_rect = pygame.Rect(
            bottom_zone.right - button_width - self.scale_value(20),
            bottom_zone.y + (bottom_zone.height - button_height) // 2,
            button_width, button_height
        )
        
        return {
            'health_bar': health_rect,
            'mana_bar': mana_rect, 
            'turn_indicator': turn_rect,
            'action_button': action_button_rect,
            'top_hud': top_zone,
            'bottom_hud': bottom_zone
        }
    
    def clear_font_cache(self):
        """Clear font cache to free memory."""
        self._font_cache.clear()

# Global scaling manager instance
scaling_manager = ScalingManager()