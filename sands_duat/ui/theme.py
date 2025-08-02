"""
UI Theme System

Centralized styling and layout management for Sands of Duat,
with special support for ultrawide displays (3440x1440).

Features:
- Responsive layout calculations
- Egyptian-themed color palette
- Font management with size scaling
- Ultrawide-optimized component positioning
"""

import pygame
from typing import Tuple, Dict, Any, NamedTuple
from enum import Enum
import logging


class DisplayMode(Enum):
    """Supported display modes."""
    ULTRAWIDE = "ultrawide"      # 3440x1440 (21:9)
    WIDESCREEN = "widescreen"    # 2560x1440 (16:9)
    STANDARD = "standard"        # 1920x1080 (16:9)
    COMPACT = "compact"          # 1024x768 (4:3)


class LayoutZone(NamedTuple):
    """Defines a UI layout zone."""
    x: int
    y: int
    width: int
    height: int


class EgyptianColors:
    """Egyptian-themed color palette."""
    
    # Main colors
    PAPYRUS = (255, 248, 220)           # Background/text
    GOLD = (255, 215, 0)                # Accents/sand
    BRONZE = (139, 117, 93)             # Borders/frames
    DEEP_BROWN = (40, 30, 20)           # Dark backgrounds
    VERY_DARK = (15, 10, 5)             # Screen backgrounds
    
    # Alias for UI compatibility
    background = VERY_DARK
    
    # Status colors
    HEALTH_RED = (220, 20, 60)          # Health bars
    MANA_BLUE = (70, 130, 180)          # Mana/energy
    SAND_GOLD = (255, 215, 0)           # Sand particles
    
    # UI states
    HOVER = (180, 150, 120)             # Hover state
    PRESSED = (100, 80, 60)             # Pressed state
    DISABLED = (60, 50, 40)             # Disabled state
    
    # Transparency levels
    GLASS = (200, 200, 255, 100)        # Semi-transparent overlays
    SHADOW = (0, 0, 0, 80)              # Drop shadows


class DisplayManager:
    """
    Manages display scaling and layout for different screen sizes.
    
    Optimized for 3440x1440 ultrawide displays with graceful fallbacks.
    """
    
    def __init__(self, target_width: int = 3440, target_height: int = 1440):
        self.base_width = target_width
        self.base_height = target_height
        self.base_aspect = target_width / target_height
        
        self.current_width = target_width
        self.current_height = target_height
        self.scale_factor = 1.0
        self.x_offset = 0
        self.y_offset = 0
        
        self.display_mode = self._detect_display_mode(target_width, target_height)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Display mode: {self.display_mode.value} ({target_width}x{target_height})")
    
    def _detect_display_mode(self, width: int, height: int) -> DisplayMode:
        """Detect the appropriate display mode based on resolution."""
        aspect_ratio = width / height
        
        if width >= 3200 and 2.3 <= aspect_ratio <= 2.5:  # ~21:9 ultrawide
            return DisplayMode.ULTRAWIDE
        elif width >= 2400 and 1.7 <= aspect_ratio <= 1.8:  # ~16:9 widescreen
            return DisplayMode.WIDESCREEN
        elif width >= 1800 and 1.7 <= aspect_ratio <= 1.8:  # ~16:9 standard
            return DisplayMode.STANDARD
        else:
            return DisplayMode.COMPACT
    
    def get_layout_zones(self) -> Dict[str, LayoutZone]:
        """Get UI layout zones optimized for current display mode."""
        if self.display_mode == DisplayMode.ULTRAWIDE:
            return self._get_ultrawide_layout()
        elif self.display_mode == DisplayMode.WIDESCREEN:
            return self._get_widescreen_layout()
        elif self.display_mode == DisplayMode.STANDARD:
            return self._get_standard_layout()
        else:
            return self._get_compact_layout()
    
    def _get_ultrawide_layout(self) -> Dict[str, LayoutZone]:
        """Optimized layout for 3440x1440 ultrawide displays."""
        return {
            'menu_bar': LayoutZone(0, 0, 3440, 60),
            'player_sand': LayoutZone(0, 60, 400, 1000),
            'combat_arena': LayoutZone(400, 60, 2640, 1000),
            'enemy_sand': LayoutZone(3040, 60, 400, 1000),
            'hand_display': LayoutZone(0, 1060, 3440, 380),
            
            # Combat sub-zones
            'player_area': LayoutZone(500, 800, 600, 260),
            'enemy_area': LayoutZone(2340, 200, 600, 260),
            'battlefield': LayoutZone(1100, 300, 1240, 500),
        }
    
    def _get_widescreen_layout(self) -> Dict[str, LayoutZone]:
        """Layout for 2560x1440 displays."""
        return {
            'menu_bar': LayoutZone(0, 0, 2560, 50),
            'player_sand': LayoutZone(0, 50, 320, 800),
            'combat_arena': LayoutZone(320, 50, 1920, 800),
            'enemy_sand': LayoutZone(2240, 50, 320, 800),
            'hand_display': LayoutZone(0, 850, 2560, 290),
            
            # Combat sub-zones
            'player_area': LayoutZone(400, 650, 480, 200),
            'enemy_area': LayoutZone(1680, 150, 480, 200),
            'battlefield': LayoutZone(880, 250, 800, 400),
        }
    
    def _get_standard_layout(self) -> Dict[str, LayoutZone]:
        """Layout for 1920x1080 displays."""
        return {
            'menu_bar': LayoutZone(0, 0, 1920, 40),
            'player_sand': LayoutZone(0, 40, 240, 600),
            'combat_arena': LayoutZone(240, 40, 1440, 600),
            'enemy_sand': LayoutZone(1680, 40, 240, 600),
            'hand_display': LayoutZone(0, 640, 1920, 240),
            
            # Combat sub-zones
            'player_area': LayoutZone(300, 490, 360, 150),
            'enemy_area': LayoutZone(1260, 120, 360, 150),
            'battlefield': LayoutZone(660, 200, 600, 300),
        }
    
    def _get_compact_layout(self) -> Dict[str, LayoutZone]:
        """Compact layout for smaller displays."""
        return {
            'menu_bar': LayoutZone(0, 0, 1024, 30),
            'player_sand': LayoutZone(0, 30, 160, 400),
            'combat_arena': LayoutZone(160, 30, 704, 400),
            'enemy_sand': LayoutZone(864, 30, 160, 400),
            'hand_display': LayoutZone(0, 430, 1024, 180),
            
            # Combat sub-zones
            'player_area': LayoutZone(200, 330, 240, 100),
            'enemy_area': LayoutZone(584, 80, 240, 100),
            'battlefield': LayoutZone(340, 130, 344, 200),
        }
    
    def scale_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """Scale a rectangle for the current display."""
        return pygame.Rect(
            int(rect.x * self.scale_factor) + self.x_offset,
            int(rect.y * self.scale_factor) + self.y_offset,
            int(rect.width * self.scale_factor),
            int(rect.height * self.scale_factor)
        )
    
    def scale_font_size(self, base_size: int) -> int:
        """Scale font size for current display."""
        return max(8, int(base_size * self.scale_factor))


class FontManager:
    """
    Manages fonts with automatic size scaling for different displays.
    """
    
    def __init__(self, display_manager: DisplayManager):
        self.display_manager = display_manager
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.base_sizes = {
            'title': 48,
            'large': 32,
            'medium': 24,
            'small': 18,
            'tiny': 12,
            'sand_counter': 72,  # Large countdown display
        }
        
        self._load_fonts()
    
    def _load_fonts(self):
        """Load and scale fonts for current display."""
        try:
            # Try to load Egyptian-themed fonts if available
            egyptian_font_path = "sands_duat/assets/fonts/egyptian.ttf"
            for name, base_size in self.base_sizes.items():
                size = self.display_manager.scale_font_size(base_size)
                try:
                    self.fonts[name] = pygame.font.Font(egyptian_font_path, size)
                except FileNotFoundError:
                    # Fallback to default font
                    self.fonts[name] = pygame.font.Font(None, size)
        except Exception as e:
            logging.warning(f"Font loading error: {e}, using default fonts")
            self._load_default_fonts()
    
    def _load_default_fonts(self):
        """Load default pygame fonts as fallback."""
        for name, base_size in self.base_sizes.items():
            size = self.display_manager.scale_font_size(base_size)
            self.fonts[name] = pygame.font.Font(None, size)
    
    def get_font(self, size_name: str) -> pygame.font.Font:
        """Get a font by size name."""
        return self.fonts.get(size_name, self.fonts['medium'])
    
    def render_text(self, text: str, size_name: str, 
                   color: Tuple[int, int, int] = EgyptianColors.PAPYRUS,
                   antialias: bool = True) -> pygame.Surface:
        """Render text with the specified font."""
        font = self.get_font(size_name)
        return font.render(text, antialias, color)


class ThemeManager:
    """
    Central theme management system combining display, colors, and fonts.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.display = DisplayManager(screen_width, screen_height)
        self.fonts = FontManager(self.display)
        self.colors = EgyptianColors()
        
        # Get layout zones for current display
        self.zones = self.display.get_layout_zones()
        
        logging.info(f"Theme initialized for {self.display.display_mode.value} mode")
    
    def get_zone(self, zone_name: str) -> LayoutZone:
        """Get a layout zone by name."""
        return self.zones.get(zone_name, LayoutZone(0, 0, 100, 100))
    
    def create_button_style(self, state: str = "normal") -> Dict[str, Any]:
        """Create a button style dictionary."""
        if state == "hover":
            bg_color = self.colors.HOVER
            border_color = self.colors.GOLD
        elif state == "pressed":
            bg_color = self.colors.PRESSED
            border_color = self.colors.BRONZE
        elif state == "disabled":
            bg_color = self.colors.DISABLED
            border_color = self.colors.DISABLED
        else:  # normal
            bg_color = self.colors.DEEP_BROWN
            border_color = self.colors.BRONZE
        
        return {
            'background_color': bg_color,
            'border_color': border_color,
            'text_color': self.colors.PAPYRUS,
            'border_width': 2,
            'font': self.fonts.get_font('medium')
        }
    
    def create_sand_gauge_style(self) -> Dict[str, Any]:
        """Create styling for sand gauge components."""
        return {
            'glass_color': self.colors.GLASS,
            'sand_color': self.colors.SAND_GOLD,
            'frame_color': self.colors.BRONZE,
            'text_color': self.colors.PAPYRUS,
            'countdown_font': self.fonts.get_font('sand_counter'),
            'label_font': self.fonts.get_font('small')
        }


# Global theme instance (initialized by main.py)
theme: ThemeManager = None


def initialize_theme(screen_width: int, screen_height: int) -> ThemeManager:
    """Initialize the global theme manager."""
    global theme
    theme = ThemeManager(screen_width, screen_height)
    return theme


def get_theme() -> ThemeManager:
    """Get the global theme manager instance."""
    if theme is None:
        raise RuntimeError("Theme not initialized. Call initialize_theme() first.")
    return theme