"""
Ultrawide Layout System - Responsive scaling for 3440x1440 and other resolutions.
Fixes UI elements getting lost in ultrawide displays with proper proportional scaling.
"""

import pygame
from typing import Tuple, Dict, Any
from ...core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER

class UltraWideLayout:
    """Manages responsive layout scaling for ultrawide displays."""
    
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
        
        # Detect display type
        self.is_ultrawide = self.aspect_ratio > 2.0  # 21:9 or wider
        self.is_standard = 1.5 <= self.aspect_ratio <= 1.8  # 16:9, 16:10
        self.is_4k = SCREEN_WIDTH >= 3840 or SCREEN_HEIGHT >= 2160
        
        # Calculate scaling factors
        self._calculate_scale_factors()
        
        # Layout zones for ultrawide
        self._setup_layout_zones()
    
    def _calculate_scale_factors(self):
        """Calculate scaling factors based on resolution and aspect ratio."""
        # Base scaling from 1920x1080
        base_width, base_height = 1920, 1080
        
        # Resolution-based scaling
        self.resolution_scale_x = self.screen_width / base_width
        self.resolution_scale_y = self.screen_height / base_height
        self.resolution_scale = min(self.resolution_scale_x, self.resolution_scale_y)
        
        # Ultrawide specific adjustments
        if self.is_ultrawide:
            # Scale UI elements larger to prevent them getting lost
            self.ui_scale_factor = 1.4  # 40% larger buttons/text
            self.content_margin_percent = 0.15  # 15% margins on sides
            self.card_spacing_factor = 1.5  # More space between elements
            self.font_scale_factor = 1.3  # Larger fonts
        else:
            self.ui_scale_factor = 1.0
            self.content_margin_percent = 0.05
            self.card_spacing_factor = 1.0
            self.font_scale_factor = 1.0
        
        # 4K additional scaling
        if self.is_4k:
            self.ui_scale_factor *= 1.2
            self.font_scale_factor *= 1.15
    
    def _setup_layout_zones(self):
        """Define layout zones for organized content placement."""
        margin_x = int(self.screen_width * self.content_margin_percent)
        margin_y = int(self.screen_height * 0.05)  # 5% top/bottom margin
        
        # Content area (safe zone)
        self.content_area = pygame.Rect(
            margin_x, margin_y,
            self.screen_width - (2 * margin_x),
            self.screen_height - (2 * margin_y)
        )
        
        # UI zones for different screen areas
        self.zones = {
            'left_panel': pygame.Rect(
                margin_x, margin_y,
                int(self.content_area.width * 0.2), self.content_area.height
            ),
            'center_content': pygame.Rect(
                margin_x + int(self.content_area.width * 0.2), margin_y,
                int(self.content_area.width * 0.6), self.content_area.height
            ),
            'right_panel': pygame.Rect(
                margin_x + int(self.content_area.width * 0.8), margin_y,
                int(self.content_area.width * 0.2), self.content_area.height
            ),
            'top_hud': pygame.Rect(
                margin_x, margin_y,
                self.content_area.width, int(self.content_area.height * 0.1)
            ),
            'bottom_hud': pygame.Rect(
                margin_x, margin_y + int(self.content_area.height * 0.9),
                self.content_area.width, int(self.content_area.height * 0.1)
            )
        }
    
    def scale_size(self, width: int, height: int) -> Tuple[int, int]:
        """Scale width and height based on layout factors."""
        scaled_width = int(width * self.ui_scale_factor * self.resolution_scale)
        scaled_height = int(height * self.ui_scale_factor * self.resolution_scale)
        return scaled_width, scaled_height
    
    def scale_font_size(self, base_size: int) -> int:
        """Scale font size for better readability."""
        return int(base_size * self.font_scale_factor * self.resolution_scale)
    
    def get_button_size(self, button_type: str = 'default') -> Tuple[int, int]:
        """Get properly scaled button sizes."""
        base_sizes = {
            'default': (200, 50),
            'wide': (300, 60),
            'large': (250, 70),
            'icon': (50, 50)
        }
        
        base_width, base_height = base_sizes.get(button_type, base_sizes['default'])
        return self.scale_size(base_width, base_height)
    
    def get_card_size(self) -> Tuple[int, int]:
        """Get properly scaled card dimensions."""
        # Base card size (poker card proportions)
        base_width, base_height = 120, 168
        return self.scale_size(base_width, base_height)
    
    def get_card_spacing(self) -> int:
        """Get spacing between cards to prevent overlap."""
        base_spacing = 20
        return int(base_spacing * self.card_spacing_factor * self.resolution_scale)
    
    def center_in_zone(self, zone_name: str, width: int, height: int) -> Tuple[int, int]:
        """Center an element within a specific zone."""
        if zone_name not in self.zones:
            # Fallback to screen center
            return (SCREEN_CENTER[0] - width // 2, SCREEN_CENTER[1] - height // 2)
        
        zone = self.zones[zone_name]
        x = zone.x + (zone.width - width) // 2
        y = zone.y + (zone.height - height) // 2
        return x, y
    
    def position_in_zone(self, zone_name: str, x_percent: float, y_percent: float) -> Tuple[int, int]:
        """Position element at percentage within zone."""
        if zone_name not in self.zones:
            return (0, 0)
        
        zone = self.zones[zone_name]
        x = zone.x + int(zone.width * x_percent)
        y = zone.y + int(zone.height * y_percent)
        return x, y
    
    def get_layout_info(self) -> Dict[str, Any]:
        """Get current layout information for debugging."""
        return {
            'resolution': f"{self.screen_width}x{self.screen_height}",
            'aspect_ratio': round(self.aspect_ratio, 2),
            'is_ultrawide': self.is_ultrawide,
            'is_4k': self.is_4k,
            'ui_scale': round(self.ui_scale_factor, 2),
            'font_scale': round(self.font_scale_factor, 2),
            'content_area': (self.content_area.x, self.content_area.y, 
                           self.content_area.width, self.content_area.height),
            'zones': {name: (zone.x, zone.y, zone.width, zone.height) 
                     for name, zone in self.zones.items()}
        }

# Global layout manager instance
ultrawide_layout = UltraWideLayout()