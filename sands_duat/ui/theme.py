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
from typing import Tuple, Dict, Any, NamedTuple, Optional
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
    """Enhanced Egyptian-themed color palette with improved sandstone hierarchy."""
    
    # Sandstone color hierarchy - F5DEB3 base with variations
    SANDSTONE_LIGHT = (250, 240, 195)   # F5DEB3 + 15 lightness - Lightest backgrounds
    SANDSTONE = (245, 222, 179)         # F5DEB3 Primary sandstone background
    SANDSTONE_MEDIUM = (235, 212, 169)  # F5DEB3 - 10 lightness - Secondary panels
    SANDSTONE_DARK = (225, 202, 159)    # F5DEB3 - 20 lightness - Pressed states
    SANDSTONE_DARKER = (215, 192, 149)  # F5DEB3 - 30 lightness - Deep backgrounds
    
    # Complementary warm colors
    PAPYRUS = (240, 230, 200)           # Light papyrus color
    GOLD = (255, 215, 0)                # Egyptian gold accents
    BRONZE = (139, 117, 93)             # Bronze borders and details
    COPPER = (184, 115, 51)             # Copper highlights
    DEEP_BROWN = (47, 27, 20)           # Dark text and elements
    VERY_DARK = (25, 15, 10)            # Minimal use backgrounds
    
    # Improved backgrounds with hierarchy
    PRIMARY_BG = SANDSTONE              # Main screen background
    SECONDARY_BG = SANDSTONE_MEDIUM     # Panel backgrounds
    TERTIARY_BG = SANDSTONE_LIGHT       # Card backgrounds
    
    # Deck builder specific colors
    COLLECTION_BG = SANDSTONE_MEDIUM    # Card collection background
    DECK_VIEW_BG = SANDSTONE_DARK       # Deck view background
    FILTER_PANEL_BG = SANDSTONE         # Filter panel background
    CARD_BG = SANDSTONE_LIGHT           # Individual card background
    CARD_SELECTED = GOLD                # Selected card highlight
    
    # Alias for UI compatibility
    background = PRIMARY_BG
    
    # Status colors with sandstone harmony
    HEALTH_RED = (200, 60, 60)          # Muted red for health
    MANA_BLUE = (90, 140, 190)          # Softer blue for mana
    SAND_GOLD = GOLD                    # Sand particles
    
    # UI interaction states
    HOVER = (220, 195, 155)             # Sandstone + warmth for hover
    PRESSED = SANDSTONE_DARK            # Darker sandstone for pressed
    DISABLED = (180, 160, 130)          # Muted sandstone for disabled
    SELECTED = (255, 235, 180)          # Golden sandstone for selection
    
    # Accessibility improvements
    HIGH_CONTRAST_TEXT = (25, 15, 10)   # Very dark for readability
    MEDIUM_CONTRAST_TEXT = (60, 40, 25) # Medium dark for secondary text
    LOW_CONTRAST_TEXT = (100, 80, 60)   # Lighter for hints/placeholders
    
    # Transparency levels
    GLASS = (245, 222, 179, 120)        # Sandstone with transparency
    SHADOW = (47, 27, 20, 80)           # Dark brown shadows
    OVERLAY = (245, 222, 179, 200)      # Semi-opaque sandstone overlay
    
    # Rarity colors that harmonize with sandstone
    RARITY_COMMON = BRONZE              # Bronze for common
    RARITY_UNCOMMON = (100, 150, 100)   # Muted green
    RARITY_RARE = (100, 100, 200)       # Muted blue
    RARITY_LEGENDARY = GOLD             # Golden for legendary
    
    # Card type colors
    TYPE_ATTACK = (180, 100, 90)        # Warm red
    TYPE_SKILL = (100, 150, 110)        # Earthy green
    TYPE_POWER = (110, 120, 180)        # Soft blue
    TYPE_CURSE = (140, 80, 140)         # Muted purple


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
            
            # Deck Builder zones - Redesigned with upper/lower layout
            'deck_filter_panel': LayoutZone(50, 80, 300, 600),         # Left side filters (upper half)
            'deck_collection': LayoutZone(380, 80, 2600, 600),         # Upper area for card collection
            'deck_view': LayoutZone(380, 720, 2600, 660),              # Lower area for current deck
            'deck_controls': LayoutZone(3020, 80, 370, 600),           # Right side deck management
            'deck_back_button': LayoutZone(50, 20, 200, 50),           # Top left back button
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
            
            # Deck Builder zones - Widescreen upper/lower layout
            'deck_filter_panel': LayoutZone(40, 70, 250, 500),
            'deck_collection': LayoutZone(310, 70, 1900, 500),
            'deck_view': LayoutZone(310, 590, 1900, 550),
            'deck_controls': LayoutZone(2230, 70, 280, 500),
            'deck_back_button': LayoutZone(40, 20, 180, 40),
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
            
            # Deck Builder zones - Standard upper/lower layout
            'deck_filter_panel': LayoutZone(20, 60, 200, 400),
            'deck_collection': LayoutZone(240, 60, 1440, 400),
            'deck_view': LayoutZone(240, 480, 1440, 400),
            'deck_controls': LayoutZone(1700, 60, 200, 400),
            'deck_back_button': LayoutZone(20, 20, 150, 30),
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
            
            # Deck Builder zones - Compact upper/lower layout
            'deck_filter_panel': LayoutZone(10, 40, 150, 250),
            'deck_collection': LayoutZone(170, 40, 680, 250),
            'deck_view': LayoutZone(170, 300, 680, 250),
            'deck_controls': LayoutZone(860, 40, 150, 250),
            'deck_back_button': LayoutZone(10, 10, 120, 25),
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
        # Ensure pygame font module is initialized
        if not pygame.font.get_init():
            pygame.font.init()
        
        try:
            # Always use default fonts for now since egyptian.ttf doesn't exist
            for name, base_size in self.base_sizes.items():
                size = self.display_manager.scale_font_size(base_size)
                try:
                    # Use pygame's default font which is guaranteed to work
                    self.fonts[name] = pygame.font.Font(None, size)
                except Exception as font_error:
                    logging.warning(f"Failed to create font {name} with size {size}: {font_error}")
                    # Last resort fallback - use minimum viable font
                    self.fonts[name] = pygame.font.Font(None, 16)
        except Exception as e:
            logging.error(f"Critical font loading error: {e}, using emergency fallback")
            self._load_emergency_fonts()
    
    def _load_default_fonts(self):
        """Load default pygame fonts as fallback."""
        for name, base_size in self.base_sizes.items():
            size = self.display_manager.scale_font_size(base_size)
            self.fonts[name] = pygame.font.Font(None, size)
    
    def _load_emergency_fonts(self):
        """Emergency font loading - absolute minimum viable fonts."""
        emergency_size = 16
        for name in self.base_sizes.keys():
            try:
                self.fonts[name] = pygame.font.Font(None, emergency_size)
            except Exception:
                # If even this fails, create a minimal font dict
                self.fonts[name] = None
        logging.error("Emergency font fallback activated - some text may not display")
    
    def get_font(self, size_name: str) -> pygame.font.Font:
        """Get a font by size name."""
        font = self.fonts.get(size_name, self.fonts.get('medium'))
        if font is None:
            # Ultimate fallback - create a font on demand
            try:
                font = pygame.font.Font(None, 16)
                self.fonts[size_name] = font
            except Exception:
                # If pygame font creation still fails, return the first available font
                for f in self.fonts.values():
                    if f is not None:
                        return f
                # If no fonts exist at all, create one last attempt
                return pygame.font.Font(None, 16)
        return font
    
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
        
        logging.info(f"Theme initialized for {self.display.display_mode.value} mode with sandstone color hierarchy")
        
        # Validate color accessibility
        self._validate_color_accessibility()
    
    def get_zone(self, zone_name: str) -> LayoutZone:
        """Get a layout zone by name."""
        return self.zones.get(zone_name, LayoutZone(0, 0, 100, 100))
    
    def _validate_color_accessibility(self) -> None:
        """Validate color contrast ratios for accessibility."""
        def calculate_luminance(color: Tuple[int, int, int]) -> float:
            """Calculate relative luminance of a color."""
            def component_luminance(c: int) -> float:
                c = c / 255.0
                if c <= 0.03928:
                    return c / 12.92
                else:
                    return pow((c + 0.055) / 1.055, 2.4)
            
            r, g, b = color
            return 0.2126 * component_luminance(r) + 0.7152 * component_luminance(g) + 0.0722 * component_luminance(b)
        
        def contrast_ratio(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
            """Calculate contrast ratio between two colors."""
            l1 = calculate_luminance(color1)
            l2 = calculate_luminance(color2)
            lighter = max(l1, l2)
            darker = min(l1, l2)
            return (lighter + 0.05) / (darker + 0.05)
        
        # Check critical text combinations
        bg_text_contrast = contrast_ratio(self.colors.PRIMARY_BG, self.colors.HIGH_CONTRAST_TEXT)
        button_text_contrast = contrast_ratio(self.colors.SECONDARY_BG, self.colors.HIGH_CONTRAST_TEXT)
        
        if bg_text_contrast < 4.5:  # WCAG AA standard
            logging.warning(f"Background-text contrast ratio {bg_text_contrast:.2f} may be too low for accessibility")
        else:
            logging.info(f"Background-text contrast ratio: {bg_text_contrast:.2f} (good)")
        
        if button_text_contrast < 4.5:
            logging.warning(f"Button-text contrast ratio {button_text_contrast:.2f} may be too low for accessibility")
        else:
            logging.info(f"Button-text contrast ratio: {button_text_contrast:.2f} (good)")
    
    def create_button_style(self, state: str = "normal") -> Dict[str, Any]:
        """Create a button style dictionary with improved sandstone hierarchy."""
        if state == "hover":
            bg_color = self.colors.HOVER
            border_color = self.colors.GOLD
            text_color = self.colors.HIGH_CONTRAST_TEXT
        elif state == "pressed":
            bg_color = self.colors.PRESSED
            border_color = self.colors.BRONZE
            text_color = self.colors.HIGH_CONTRAST_TEXT
        elif state == "disabled":
            bg_color = self.colors.DISABLED
            border_color = self.colors.DISABLED
            text_color = self.colors.LOW_CONTRAST_TEXT
        else:  # normal
            bg_color = self.colors.SECONDARY_BG
            border_color = self.colors.BRONZE
            text_color = self.colors.HIGH_CONTRAST_TEXT
        
        return {
            'background_color': bg_color,
            'border_color': border_color,
            'text_color': text_color,
            'border_width': 2,
            'font': self.fonts.get_font('medium')
        }
    
    def create_deck_builder_style(self) -> Dict[str, Any]:
        """Create specialized styling for deck builder components."""
        return {
            'collection_background': self.colors.COLLECTION_BG,
            'deck_view_background': self.colors.DECK_VIEW_BG,
            'filter_panel_background': self.colors.FILTER_PANEL_BG,
            'card_background': self.colors.CARD_BG,
            'card_selected': self.colors.CARD_SELECTED,
            'card_hover': self.colors.HOVER,
            'border_color': self.colors.BRONZE,
            'text_primary': self.colors.HIGH_CONTRAST_TEXT,
            'text_secondary': self.colors.MEDIUM_CONTRAST_TEXT,
            'text_hint': self.colors.LOW_CONTRAST_TEXT,
            'accent_color': self.colors.GOLD
        }
    
    def create_card_style(self, rarity: Optional[Any] = None, card_type: Optional[Any] = None) -> Dict[str, Any]:
        """Create card-specific styling based on rarity and type."""
        # Import here to avoid circular imports
        try:
            from ..core.cards import CardRarity, CardType
            
            # Rarity-based styling
            if rarity == CardRarity.LEGENDARY:
                border_color = self.colors.RARITY_LEGENDARY
                bg_modifier = (20, 15, 0)  # Golden tint
            elif rarity == CardRarity.RARE:
                border_color = self.colors.RARITY_RARE
                bg_modifier = (0, 5, 15)  # Blue tint
            elif rarity == CardRarity.UNCOMMON:
                border_color = self.colors.RARITY_UNCOMMON
                bg_modifier = (0, 10, 5)  # Green tint
            else:  # Common
                border_color = self.colors.RARITY_COMMON
                bg_modifier = (0, 0, 0)  # No tint
            
            # Type-based accent
            type_accent = self.colors.BRONZE
            if card_type == CardType.ATTACK:
                type_accent = self.colors.TYPE_ATTACK
            elif card_type == CardType.SKILL:
                type_accent = self.colors.TYPE_SKILL
            elif card_type == CardType.POWER:
                type_accent = self.colors.TYPE_POWER
            elif card_type == CardType.CURSE:
                type_accent = self.colors.TYPE_CURSE
                
        except ImportError:
            # Fallback if card types not available
            border_color = self.colors.BRONZE
            bg_modifier = (0, 0, 0)
            type_accent = self.colors.BRONZE
        
        # Apply background modifier
        base_bg = self.colors.CARD_BG
        modified_bg = tuple(min(255, max(0, base_bg[i] + bg_modifier[i])) for i in range(3))
        
        return {
            'background_color': modified_bg,
            'border_color': border_color,
            'type_accent': type_accent,
            'text_color': self.colors.HIGH_CONTRAST_TEXT,
            'cost_color': self.colors.GOLD,
            'hover_color': self.colors.HOVER,
            'selected_color': self.colors.SELECTED
        }
    
    def create_sand_gauge_style(self) -> Dict[str, Any]:
        """Create styling for sand gauge components with sandstone hierarchy."""
        return {
            'glass_color': self.colors.GLASS,
            'sand_color': self.colors.SAND_GOLD,
            'frame_color': self.colors.BRONZE,
            'background_color': self.colors.SECONDARY_BG,
            'text_color': self.colors.HIGH_CONTRAST_TEXT,
            'label_color': self.colors.MEDIUM_CONTRAST_TEXT,
            'countdown_font': self.fonts.get_font('sand_counter'),
            'label_font': self.fonts.get_font('small')
        }


# Global theme instance (initialized by main.py)
theme: ThemeManager = None


def initialize_theme(screen_width: int, screen_height: int) -> ThemeManager:
    """Initialize the global theme manager with sandstone color hierarchy."""
    global theme
    theme = ThemeManager(screen_width, screen_height)
    logging.info(f"Initialized sandstone theme for {screen_width}x{screen_height} display")
    return theme


def get_theme() -> ThemeManager:
    """Get the global theme manager instance."""
    if theme is None:
        raise RuntimeError("Theme not initialized. Call initialize_theme() first.")
    return theme


def get_sandstone_color(lightness_modifier: int = 0) -> Tuple[int, int, int]:
    """Get a sandstone color variant with specified lightness modifier."""
    base_sandstone = (245, 222, 179)  # F5DEB3
    return tuple(min(255, max(0, base_sandstone[i] + lightness_modifier)) for i in range(3))