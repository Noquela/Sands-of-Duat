"""
Enhanced Ultrawide Layout System - Sprint 1 UI Improvements
Advanced responsive layout that maximizes ultrawide screen real estate
while maintaining clean, professional presentation.
"""

import pygame
import math
from typing import Tuple, Dict, Any, List
from ...core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER, Colors
from enum import Enum

class LayoutZone(Enum):
    """Defined zones for ultrawide layout."""
    LEFT_PANEL = "left_panel"       # Left 25% - Secondary info, navigation
    CENTER_MAIN = "center_main"     # Center 50% - Primary content  
    RIGHT_PANEL = "right_panel"     # Right 25% - Tools, stats, inventory
    TOP_BAR = "top_bar"            # Top 10% - Title, notifications
    BOTTOM_BAR = "bottom_bar"      # Bottom 15% - Actions, status

class ElementType(Enum):
    """Types of UI elements for different scaling."""
    TITLE = "title"                 # Large, prominent text
    BUTTON = "button"               # Interactive elements
    CARD = "card"                   # Game cards
    TEXT_BODY = "text_body"         # Regular text content
    ICON = "icon"                   # Small icons and symbols
    BACKGROUND = "background"       # Background elements

class EnhancedUltrawideLayout:
    """Advanced layout system for professional ultrawide UI."""
    
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
        
        # Display classification
        self.is_ultrawide = self.aspect_ratio >= 2.0    # 21:9 or wider
        self.is_super_ultrawide = self.aspect_ratio >= 2.5  # 32:9
        self.is_4k = SCREEN_WIDTH >= 3200 or SCREEN_HEIGHT >= 1800
        
        # Calculate enhanced scaling factors
        self._calculate_enhanced_scaling()
        
        # Create layout zones
        self._create_layout_zones()
        
        # Setup typography scaling
        self._setup_typography()
        
        # Create element positioning system
        self._setup_element_positioning()
    
    def _calculate_enhanced_scaling(self):
        """Calculate advanced scaling factors for different screen types."""
        # Base reference: 1920x1080
        base_width, base_height = 1920, 1080
        
        # Resolution scaling
        self.res_scale_x = self.screen_width / base_width
        self.res_scale_y = self.screen_height / base_height
        self.base_scale = min(self.res_scale_x, self.res_scale_y)
        
        if self.is_super_ultrawide:  # 32:9 displays
            self.ui_scale = 1.6          # Even larger UI elements
            self.content_width_percent = 0.6  # Use 60% of center for content
            self.margin_percent = 0.2    # 20% margins on each side
            self.font_scale = 1.5        # Much larger fonts
            self.spacing_multiplier = 1.8
            
        elif self.is_ultrawide:  # 21:9 displays  
            self.ui_scale = 1.4          # 40% larger UI elements
            self.content_width_percent = 0.7  # Use 70% of center for content
            self.margin_percent = 0.15   # 15% margins on each side
            self.font_scale = 1.3        # 30% larger fonts
            self.spacing_multiplier = 1.5
            
        else:  # Standard displays (16:9, 16:10)
            self.ui_scale = 1.0
            self.content_width_percent = 0.9
            self.margin_percent = 0.05
            self.font_scale = 1.0
            self.spacing_multiplier = 1.0
            
        # 4K adjustments
        if self.is_4k:
            self.ui_scale *= 1.2
            self.font_scale *= 1.2
    
    def _create_layout_zones(self):
        """Create defined zones for content placement."""
        self.zones = {}
        
        # Calculate zone boundaries
        left_margin = int(self.screen_width * self.margin_percent)
        right_margin = self.screen_width - left_margin
        content_width = right_margin - left_margin
        
        # Horizontal zones
        panel_width = content_width * 0.25
        center_width = content_width * 0.5
        
        self.zones[LayoutZone.LEFT_PANEL] = pygame.Rect(
            left_margin, 0, panel_width, self.screen_height
        )
        
        self.zones[LayoutZone.CENTER_MAIN] = pygame.Rect(
            left_margin + panel_width, int(self.screen_height * 0.1),
            center_width, int(self.screen_height * 0.75)
        )
        
        self.zones[LayoutZone.RIGHT_PANEL] = pygame.Rect(
            left_margin + panel_width + center_width, 0,
            panel_width, self.screen_height
        )
        
        # Vertical zones
        self.zones[LayoutZone.TOP_BAR] = pygame.Rect(
            left_margin, 0, content_width, int(self.screen_height * 0.1)
        )
        
        self.zones[LayoutZone.BOTTOM_BAR] = pygame.Rect(
            left_margin, int(self.screen_height * 0.85),
            content_width, int(self.screen_height * 0.15)
        )
    
    def _setup_typography(self):
        """Setup responsive typography scaling."""
        base_sizes = {
            'debug': 12,
            'small': 14,
            'body': 18,
            'button': 20,
            'subtitle': 24,
            'title': 32,
            'large_title': 48,
            'huge_title': 64
        }
        
        self.font_sizes = {}
        for size_name, base_size in base_sizes.items():
            scaled_size = int(base_size * self.font_scale)
            self.font_sizes[size_name] = scaled_size
    
    def _setup_element_positioning(self):
        """Setup element positioning helpers."""
        # Standard element sizes (scaled)
        self.element_sizes = {
            ElementType.BUTTON: (
                int(200 * self.ui_scale),
                int(50 * self.ui_scale)
            ),
            ElementType.CARD: (
                int(160 * self.ui_scale),
                int(240 * self.ui_scale)
            ),
            ElementType.ICON: (
                int(32 * self.ui_scale),
                int(32 * self.ui_scale)
            )
        }
        
        # Spacing values
        self.spacing = {
            'tiny': int(4 * self.spacing_multiplier),
            'small': int(8 * self.spacing_multiplier),
            'medium': int(16 * self.spacing_multiplier),
            'large': int(32 * self.spacing_multiplier),
            'huge': int(64 * self.spacing_multiplier)
        }
    
    def get_zone_rect(self, zone: LayoutZone) -> pygame.Rect:
        """Get the rectangle for a layout zone."""
        return self.zones.get(zone, pygame.Rect(0, 0, 100, 100))
    
    def get_font_size(self, size_name: str) -> int:
        """Get scaled font size."""
        return self.font_sizes.get(size_name, 18)
    
    def get_element_size(self, element_type: ElementType) -> Tuple[int, int]:
        """Get scaled element size."""
        return self.element_sizes.get(element_type, (100, 30))
    
    def get_spacing(self, spacing_name: str) -> int:
        """Get scaled spacing value."""
        return self.spacing.get(spacing_name, 16)
    
    def position_in_zone(self, zone: LayoutZone, x_percent: float, y_percent: float) -> Tuple[int, int]:
        """Position element within a zone using percentages."""
        zone_rect = self.get_zone_rect(zone)
        x = zone_rect.x + int(zone_rect.width * x_percent)
        y = zone_rect.y + int(zone_rect.height * y_percent)
        return (x, y)
    
    def center_in_zone(self, zone: LayoutZone, element_width: int, element_height: int) -> Tuple[int, int]:
        """Center element within a zone."""
        zone_rect = self.get_zone_rect(zone)
        x = zone_rect.x + (zone_rect.width - element_width) // 2
        y = zone_rect.y + (zone_rect.height - element_height) // 2
        return (x, y)
    
    def create_card_grid(self, zone: LayoutZone, cards_count: int, max_per_row: int = None) -> List[Tuple[int, int]]:
        """Create a responsive grid of card positions within a zone."""
        zone_rect = self.get_zone_rect(zone)
        card_width, card_height = self.get_element_size(ElementType.CARD)
        spacing = self.get_spacing('medium')
        
        # Calculate optimal layout
        if max_per_row is None:
            # Auto-calculate based on zone width
            max_per_row = max(1, (zone_rect.width + spacing) // (card_width + spacing))
        
        rows = math.ceil(cards_count / max_per_row)
        cols = min(cards_count, max_per_row)
        
        # Calculate grid dimensions
        total_width = cols * card_width + (cols - 1) * spacing
        total_height = rows * card_height + (rows - 1) * spacing
        
        # Center the grid in the zone
        start_x = zone_rect.x + (zone_rect.width - total_width) // 2
        start_y = zone_rect.y + (zone_rect.height - total_height) // 2
        
        # Generate positions
        positions = []
        for i in range(cards_count):
            row = i // max_per_row
            col = i % max_per_row
            
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            positions.append((x, y))
        
        return positions
    
    def create_button_layout(self, zone: LayoutZone, button_count: int, 
                           orientation: str = 'horizontal') -> List[Tuple[int, int]]:
        """Create responsive button layout."""
        zone_rect = self.get_zone_rect(zone)
        button_width, button_height = self.get_element_size(ElementType.BUTTON)
        spacing = self.get_spacing('medium')
        
        positions = []
        
        if orientation == 'horizontal':
            total_width = button_count * button_width + (button_count - 1) * spacing
            start_x = zone_rect.x + (zone_rect.width - total_width) // 2
            y = zone_rect.y + (zone_rect.height - button_height) // 2
            
            for i in range(button_count):
                x = start_x + i * (button_width + spacing)
                positions.append((x, y))
        
        else:  # vertical
            total_height = button_count * button_height + (button_count - 1) * spacing
            x = zone_rect.x + (zone_rect.width - button_width) // 2
            start_y = zone_rect.y + (zone_rect.height - total_height) // 2
            
            for i in range(button_count):
                y = start_y + i * (button_height + spacing)
                positions.append((x, y))
        
        return positions
    
    def get_layout_info(self) -> Dict[str, Any]:
        """Get comprehensive layout information for debugging."""
        return {
            'display_type': {
                'ultrawide': self.is_ultrawide,
                'super_ultrawide': self.is_super_ultrawide,
                'is_4k': self.is_4k,
                'aspect_ratio': round(self.aspect_ratio, 2)
            },
            'scaling': {
                'ui_scale': self.ui_scale,
                'font_scale': self.font_scale,
                'base_scale': self.base_scale,
                'spacing_multiplier': self.spacing_multiplier
            },
            'zones': {zone.name: rect for zone, rect in self.zones.items()},
            'font_sizes': self.font_sizes,
            'spacing': self.spacing
        }

# Global instance
enhanced_ultrawide_layout = EnhancedUltrawideLayout()