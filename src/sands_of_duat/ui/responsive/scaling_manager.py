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
        
        # Enhanced font sizes for SPRINT 1 - Strong Visual Hierarchy
        self.font_sizes = {
            'debug': 14,
            'small': 16,
            'card_text': 18,
            'tooltip': 20,
            'body': 24,
            'card_name': 26,
            'button': 28,       # Larger buttons for ultrawide
            'subtitle': 36,
            'title_medium': 48,
            'title_large': 64,  # Increased for better hierarchy
            'title_huge': 88    # Much larger main titles for impact
        }
        
        # Enhanced component sizes for SPRINT 1 - Better Visibility
        self.component_sizes = {
            'button_default': (280, 70),    # 40% larger for ultrawide
            'button_wide': (420, 84),       # 40% larger for ultrawide
            'button_large': (350, 98),      # 40% larger for ultrawide
            'button_icon': (70, 70),        # Square icon buttons
            'card_small': (112, 156),       # 40% larger cards
            'card_medium': (168, 235),      # 40% larger cards
            'card_large': (224, 313),       # 40% larger cards
            'health_bar': (280, 32),        # Thicker, more visible bars
            'mana_bar': (210, 28),          # Thicker, more visible bars
            'turn_indicator': (300, 50),    # Clear turn indicator
            'tooltip_box': (400, 120)       # Larger tooltips for readability
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
        """Get SPRINT 1 enhanced HUD layout - Horizontal bars, clear hierarchy."""
        # Enhanced zones for better visibility
        top_zone = self.layout.zones['top_hud']
        bottom_zone = self.layout.zones['bottom_hud']
        
        # SPRINT 1: Horizontal health bar spans top width with gradient
        health_width, health_height = self.get_component_size('health_bar')
        health_rect = pygame.Rect(
            top_zone.x + self.scale_value(40),
            top_zone.y + self.scale_value(15),
            health_width, health_height
        )
        
        # SPRINT 1: Horizontal mana bar below health with spacing
        mana_width, mana_height = self.get_component_size('mana_bar')
        mana_rect = pygame.Rect(
            top_zone.x + self.scale_value(40),
            health_rect.bottom + self.scale_value(10),
            mana_width, mana_height
        )
        
        # SPRINT 1: Large, prominent turn indicator (top center)
        turn_width, turn_height = self.get_component_size('turn_indicator')
        turn_rect = pygame.Rect(
            top_zone.centerx - turn_width // 2,
            top_zone.y + self.scale_value(20),
            turn_width, turn_height
        )
        
        # SPRINT 1: Action buttons grouped in bottom right corner
        button_width, button_height = self.get_component_size('button_default')
        button_spacing = self.scale_value(15)
        
        # End Turn button (primary action)
        end_turn_rect = pygame.Rect(
            bottom_zone.right - button_width - self.scale_value(30),
            bottom_zone.y + (bottom_zone.height - button_height) // 2,
            button_width, button_height
        )
        
        # Secondary action button (left of End Turn)
        action_rect = pygame.Rect(
            end_turn_rect.x - button_width - button_spacing,
            end_turn_rect.y,
            button_width, button_height
        )
        
        # SPRINT 1: Card counter (bottom left) 
        card_counter_rect = pygame.Rect(
            bottom_zone.x + self.scale_value(30),
            bottom_zone.y + self.scale_value(15),
            self.scale_value(200), self.scale_value(40)
        )
        
        return {
            'health_bar': health_rect,
            'mana_bar': mana_rect, 
            'turn_indicator': turn_rect,
            'end_turn_button': end_turn_rect,
            'action_button': action_rect,
            'card_counter': card_counter_rect,
            'top_hud': top_zone,
            'bottom_hud': bottom_zone
        }
    
    def clear_font_cache(self):
        """Clear font cache to free memory."""
        self._font_cache.clear()

# Global scaling manager instance
scaling_manager = ScalingManager()