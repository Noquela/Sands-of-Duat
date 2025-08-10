"""
Enhanced Responsive Typography System
Professional text rendering with outlines, shadows and responsive scaling.
"""

import pygame
from typing import Tuple, Optional, Dict, Any
from enum import Enum

from ...core.constants import Colors, FontSizes, Layout


class TextStyle(Enum):
    """Text style presets for different UI elements."""
    TITLE_HUGE = "title_huge"
    TITLE_LARGE = "title_large" 
    TITLE_MEDIUM = "title_medium"
    SUBTITLE = "subtitle"
    BUTTON = "button"
    BODY = "body"
    CARD_NAME = "card_name"
    CARD_TEXT = "card_text"
    TOOLTIP = "tooltip"
    DEBUG = "debug"


class TextEffect(Enum):
    """Text effect types."""
    NONE = "none"
    OUTLINE = "outline"
    SHADOW = "shadow"
    GLOW = "glow"
    EMBOSSED = "embossed"


class ResponsiveTypography:
    """
    Professional text rendering system with responsive scaling and effects.
    Optimized for 4K backgrounds and ultrawide displays.
    """
    
    def __init__(self):
        # Font cache for performance
        self.font_cache: Dict[Tuple[int, bool], pygame.font.Font] = {}
        
        # Style configurations
        self.text_styles = {
            TextStyle.TITLE_HUGE: {
                'size': FontSizes.TITLE_HUGE,
                'color': Colors.GOLD,
                'effect': TextEffect.OUTLINE,
                'effect_color': Colors.BLACK,
                'effect_size': 3
            },
            TextStyle.TITLE_LARGE: {
                'size': FontSizes.TITLE_LARGE,
                'color': Colors.GOLD,
                'effect': TextEffect.OUTLINE,
                'effect_color': Colors.BLACK,
                'effect_size': 2
            },
            TextStyle.TITLE_MEDIUM: {
                'size': FontSizes.TITLE_MEDIUM,
                'color': Colors.DESERT_SAND,
                'effect': TextEffect.SHADOW,
                'effect_color': Colors.BLACK,
                'effect_size': 2
            },
            TextStyle.SUBTITLE: {
                'size': FontSizes.SUBTITLE,
                'color': Colors.LAPIS_LAZULI,
                'effect': TextEffect.SHADOW,
                'effect_color': Colors.BLACK,
                'effect_size': 1
            },
            TextStyle.BUTTON: {
                'size': FontSizes.BUTTON,
                'color': Colors.WHITE,
                'effect': TextEffect.OUTLINE,
                'effect_color': Colors.BLACK,
                'effect_size': 1
            },
            TextStyle.BODY: {
                'size': FontSizes.BODY,
                'color': Colors.WHITE,
                'effect': TextEffect.SHADOW,
                'effect_color': Colors.BLACK,
                'effect_size': 1
            },
            TextStyle.CARD_NAME: {
                'size': FontSizes.CARD_NAME,
                'color': Colors.BLACK,
                'effect': TextEffect.NONE,
                'effect_color': Colors.WHITE,
                'effect_size': 0
            },
            TextStyle.CARD_TEXT: {
                'size': FontSizes.CARD_TEXT,
                'color': Colors.BLACK,
                'effect': TextEffect.NONE,
                'effect_color': Colors.WHITE,
                'effect_size': 0
            },
            TextStyle.TOOLTIP: {
                'size': FontSizes.TOOLTIP,
                'color': Colors.WHITE,
                'effect': TextEffect.OUTLINE,
                'effect_color': Colors.BLACK,
                'effect_size': 1
            },
            TextStyle.DEBUG: {
                'size': FontSizes.DEBUG,
                'color': Colors.WHITE,
                'effect': TextEffect.SHADOW,
                'effect_color': Colors.BLACK,
                'effect_size': 1
            }
        }
        
        print(f"[TYPOGRAPHY] Responsive typography system initialized with {len(self.text_styles)} styles")
    
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """Get cached font or create new one."""
        cache_key = (size, bold)
        if cache_key not in self.font_cache:
            self.font_cache[cache_key] = pygame.font.Font(None, size)
            if bold:
                self.font_cache[cache_key].set_bold(True)
        return self.font_cache[cache_key]
    
    def render_text(self, text: str, style: TextStyle, surface: pygame.Surface, 
                   position: Tuple[int, int], center: bool = False,
                   custom_color: Optional[Tuple[int, int, int]] = None,
                   custom_effect: Optional[TextEffect] = None) -> pygame.Rect:
        """
        Render text with specified style and effects.
        
        Args:
            text: Text to render
            style: Text style preset
            surface: Target surface
            position: Text position (x, y)
            center: Center text at position
            custom_color: Override style color
            custom_effect: Override style effect
            
        Returns:
            pygame.Rect: Text bounding rectangle
        """
        if not text:
            return pygame.Rect(position[0], position[1], 0, 0)
        
        style_config = self.text_styles[style]
        font = self.get_font(style_config['size'])
        
        # Determine colors
        text_color = custom_color or style_config['color']
        effect_color = style_config['effect_color']
        effect = custom_effect or style_config['effect']
        effect_size = style_config['effect_size']
        
        # Render text with effects
        if effect == TextEffect.OUTLINE:
            text_surface = self._render_outlined_text(text, font, text_color, effect_color, effect_size)
        elif effect == TextEffect.SHADOW:
            text_surface = self._render_shadow_text(text, font, text_color, effect_color, effect_size)
        elif effect == TextEffect.GLOW:
            text_surface = self._render_glow_text(text, font, text_color, effect_color, effect_size)
        elif effect == TextEffect.EMBOSSED:
            text_surface = self._render_embossed_text(text, font, text_color, effect_color)
        else:
            text_surface = font.render(text, True, text_color)
        
        # Position text
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        
        # Blit to surface
        surface.blit(text_surface, text_rect)
        
        return text_rect
    
    def _render_outlined_text(self, text: str, font: pygame.font.Font, 
                            text_color: Tuple[int, int, int], 
                            outline_color: Tuple[int, int, int], 
                            outline_size: int) -> pygame.Surface:
        """Render text with outline effect."""
        # Render outline
        outline_surfaces = []
        for dx in range(-outline_size, outline_size + 1):
            for dy in range(-outline_size, outline_size + 1):
                if dx != 0 or dy != 0:
                    outline_surface = font.render(text, True, outline_color)
                    outline_surfaces.append((outline_surface, (dx, dy)))
        
        # Calculate surface size
        text_surface = font.render(text, True, text_color)
        width = text_surface.get_width() + outline_size * 2
        height = text_surface.get_height() + outline_size * 2
        
        # Create final surface
        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Blit outline
        for outline_surface, (dx, dy) in outline_surfaces:
            final_surface.blit(outline_surface, (outline_size + dx, outline_size + dy))
        
        # Blit main text
        final_surface.blit(text_surface, (outline_size, outline_size))
        
        return final_surface
    
    def _render_shadow_text(self, text: str, font: pygame.font.Font,
                          text_color: Tuple[int, int, int],
                          shadow_color: Tuple[int, int, int],
                          shadow_offset: int) -> pygame.Surface:
        """Render text with drop shadow effect."""
        # Render shadow and main text
        shadow_surface = font.render(text, True, shadow_color)
        text_surface = font.render(text, True, text_color)
        
        # Create final surface
        width = max(text_surface.get_width(), shadow_surface.get_width()) + shadow_offset
        height = max(text_surface.get_height(), shadow_surface.get_height()) + shadow_offset
        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Blit shadow first, then text
        final_surface.blit(shadow_surface, (shadow_offset, shadow_offset))
        final_surface.blit(text_surface, (0, 0))
        
        return final_surface
    
    def _render_glow_text(self, text: str, font: pygame.font.Font,
                         text_color: Tuple[int, int, int],
                         glow_color: Tuple[int, int, int],
                         glow_size: int) -> pygame.Surface:
        """Render text with glow effect."""
        # Create glow layers
        glow_surfaces = []
        for i in range(glow_size):
            alpha = 255 - (i * 50)  # Fade out glow
            if alpha <= 0:
                break
            glow_layer = font.render(text, True, (*glow_color, min(255, alpha)))
            glow_surfaces.append((glow_layer, i))
        
        # Calculate surface size
        text_surface = font.render(text, True, text_color)
        width = text_surface.get_width() + glow_size * 2
        height = text_surface.get_height() + glow_size * 2
        
        # Create final surface
        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Blit glow layers
        for glow_layer, offset in reversed(glow_surfaces):
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    final_surface.blit(glow_layer, (glow_size + dx, glow_size + dy))
        
        # Blit main text
        final_surface.blit(text_surface, (glow_size, glow_size))
        
        return final_surface
    
    def _render_embossed_text(self, text: str, font: pygame.font.Font,
                            text_color: Tuple[int, int, int],
                            highlight_color: Tuple[int, int, int]) -> pygame.Surface:
        """Render text with embossed effect."""
        # Create highlight and shadow
        highlight = font.render(text, True, highlight_color)
        shadow = font.render(text, True, (0, 0, 0))
        text_surface = font.render(text, True, text_color)
        
        # Create final surface
        width = text_surface.get_width() + 2
        height = text_surface.get_height() + 2
        final_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Blit in order: shadow, highlight, main text
        final_surface.blit(shadow, (2, 2))
        final_surface.blit(highlight, (0, 0))
        final_surface.blit(text_surface, (1, 1))
        
        return final_surface
    
    def render_wrapped_text(self, text: str, style: TextStyle, surface: pygame.Surface,
                          rect: pygame.Rect, line_spacing: int = 5) -> int:
        """
        Render wrapped text within a rectangle.
        
        Args:
            text: Text to render
            style: Text style preset
            surface: Target surface
            rect: Bounding rectangle
            line_spacing: Spacing between lines
            
        Returns:
            int: Number of lines rendered
        """
        if not text:
            return 0
        
        style_config = self.text_styles[style]
        font = self.get_font(style_config['size'])
        
        words = text.split(' ')
        lines = []
        current_line = []
        
        # Build lines
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= rect.width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Render lines
        y_offset = rect.y
        lines_rendered = 0
        
        for line in lines:
            if y_offset + font.get_height() > rect.bottom:
                break
            
            self.render_text(line, style, surface, (rect.x, y_offset))
            y_offset += font.get_height() + line_spacing
            lines_rendered += 1
        
        return lines_rendered
    
    def measure_text(self, text: str, style: TextStyle) -> Tuple[int, int]:
        """Measure text dimensions for layout calculations."""
        if not text:
            return (0, 0)
        
        style_config = self.text_styles[style]
        font = self.get_font(style_config['size'])
        return font.size(text)
    
    def get_line_height(self, style: TextStyle) -> int:
        """Get line height for a text style."""
        style_config = self.text_styles[style]
        font = self.get_font(style_config['size'])
        return font.get_height()


# Global instance for easy access
responsive_typography = ResponsiveTypography()