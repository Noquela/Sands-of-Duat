"""
Optimized Hades-Style UI Theme for Sands of Duat

Performance-optimized Egyptian underworld aesthetic with:
- Cached surface rendering for UI elements
- GPU-friendly texture operations
- Reduced draw calls through batching
- Memory-efficient glow effects
- Adaptive detail levels based on performance
"""

import pygame
import math
import time
from typing import Tuple, Dict, Optional, List
from pathlib import Path
from functools import lru_cache
import numpy as np

from ..core.performance_profiler import profile_operation
from ..assets.optimized_asset_manager import get_asset_manager, AssetType


class OptimizedHadesEgyptianTheme:
    """Performance-optimized Hades-style theme for Egyptian underworld."""
    
    def __init__(self, display_size: Tuple[int, int]):
        self.display_size = display_size
        self.scale_factor = min(display_size[0] / 1920, display_size[1] / 1080)
        
        # Performance settings
        self.enable_glow_effects = True
        self.enable_animations = True
        self.max_detail_level = 3  # 0=minimal, 3=ultra
        self.current_detail_level = 2
        
        # Egyptian Underworld Color Palette (optimized)
        self.colors = self._initialize_color_palette()
        
        # Typography Settings (cached)
        self.fonts = self._initialize_fonts()
        
        # UI Element Dimensions (pre-calculated)
        self.dimensions = self._initialize_dimensions()
        
        # Cached surfaces for common UI elements
        self.surface_cache: Dict[str, pygame.Surface] = {}
        self.cache_max_size = 50
        
        # Pre-computed glow surfaces
        self.glow_cache: Dict[Tuple[int, Tuple[int, int, int]], pygame.Surface] = {}
        
        # Texture patterns (optimized)
        self.textures = {}
        self._create_optimized_textures()
        
        # Animation timing
        self.animation_time = 0.0
        self.last_frame_time = time.time()
        
        # Performance metrics
        self.render_stats = {
            "buttons_rendered": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "glow_effects_rendered": 0
        }
        
        # Get asset manager
        self.asset_manager = get_asset_manager()
    
    def _initialize_color_palette(self) -> Dict[str, Tuple[int, int, int]]:
        """Initialize optimized color palette."""
        return {
            # Primary Colors
            'duat_gold': (218, 165, 32),
            'pharaoh_bronze': (205, 127, 50),
            'underworld_crimson': (139, 0, 0),
            'night_blue': (25, 25, 112),
            'obsidian_black': (12, 12, 12),
            'papyrus_cream': (245, 230, 163),
            
            # Secondary Colors
            'sacred_turquoise': (64, 224, 208),
            'desert_amber': (255, 191, 0),
            'mummy_linen': (250, 240, 230),
            'hieroglyph_green': (0, 100, 0),
            'royal_purple': (102, 51, 153),
            
            # UI States
            'hover_gold': (255, 215, 0),
            'active_bronze': (184, 134, 11),
            'disabled_gray': (105, 105, 105),
            'error_red': (220, 20, 60),
            'success_green': (34, 139, 34),
        }
    
    def _initialize_fonts(self) -> Dict[str, Dict]:
        """Initialize font configurations with caching."""
        return {
            'title': {'size': int(48 * self.scale_factor), 'bold': True},
            'header': {'size': int(32 * self.scale_factor), 'bold': True}, 
            'body': {'size': int(18 * self.scale_factor), 'bold': False},
            'small': {'size': int(14 * self.scale_factor), 'bold': False},
            'card_title': {'size': int(16 * self.scale_factor), 'bold': True},
            'card_text': {'size': int(12 * self.scale_factor), 'bold': False},
        }
    
    def _initialize_dimensions(self) -> Dict[str, int]:
        """Initialize UI dimensions with scaling."""
        return {
            'button_height': int(50 * self.scale_factor),
            'button_padding': int(20 * self.scale_factor),
            'card_width': int(120 * self.scale_factor),
            'card_height': int(180 * self.scale_factor),
            'border_width': max(2, int(3 * self.scale_factor)),
            'corner_radius': int(8 * self.scale_factor),
            'glow_radius': int(6 * self.scale_factor),
        }
    
    def _create_optimized_textures(self):
        """Create optimized texture patterns."""
        # Simplified papyrus texture
        papyrus_size = 32  # Reduced from 64 for performance
        papyrus_surface = pygame.Surface((papyrus_size, papyrus_size), pygame.SRCALPHA)
        papyrus_surface.fill(self.colors['papyrus_cream'])
        
        # Simplified fiber pattern
        for i in range(0, papyrus_size, 8):
            for j in range(0, papyrus_size, 8):
                if (i + j) % 16 == 0:
                    pygame.draw.rect(papyrus_surface, self.colors['desert_amber'], 
                                   (i, j, 4, 1))
                    pygame.draw.rect(papyrus_surface, self.colors['desert_amber'], 
                                   (i, j, 1, 4))
        
        self.textures['papyrus'] = papyrus_surface
        
        # Optimized gold metallic texture
        gold_size = 16  # Reduced from 32
        gold_surface = pygame.Surface((gold_size, gold_size))
        gold_surface.fill(self.colors['duat_gold'])
        
        # Simplified metallic pattern
        for i in range(0, gold_size, 2):
            color = self.colors['hover_gold'] if i % 4 == 0 else self.colors['pharaoh_bronze']
            pygame.draw.line(gold_surface, color, (i, 0), (i, gold_size), 1)
        
        self.textures['gold_metal'] = gold_surface
    
    @lru_cache(maxsize=32)
    def _get_cached_font(self, style: str) -> pygame.font.Font:
        """Get cached font object."""
        font_config = self.fonts.get(style, self.fonts['body'])
        font = pygame.font.Font(None, font_config['size'])
        if font_config['bold']:
            font.set_bold(True)
        return font
    
    def _get_glow_surface(self, radius: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Get cached glow surface."""
        cache_key = (radius, color)
        
        if cache_key not in self.glow_cache:
            # Create glow surface
            size = radius * 2
            glow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Create radial gradient
            center = radius
            for r in range(radius):
                alpha = int(128 * (1 - r / radius))
                if alpha > 0:
                    glow_color = (*color, alpha)
                    pygame.draw.circle(glow_surface, glow_color, (center, center), radius - r)
            
            self.glow_cache[cache_key] = glow_surface
            
            # Limit cache size
            if len(self.glow_cache) > 20:
                # Remove oldest entry
                oldest_key = next(iter(self.glow_cache))
                del self.glow_cache[oldest_key]
        
        return self.glow_cache[cache_key]
    
    def _get_button_cache_key(self, rect: pygame.Rect, text: str, state: str) -> str:
        """Generate cache key for button."""
        return f"btn_{rect.width}x{rect.height}_{text}_{state}_{self.current_detail_level}"
    
    def update_animation_time(self, delta_time: float):
        """Update animation timing."""
        if self.enable_animations:
            self.animation_time += delta_time
    
    def set_detail_level(self, level: int):
        """Set rendering detail level (0=minimal, 3=ultra)."""
        self.current_detail_level = max(0, min(3, level))
        
        # Clear cache when detail level changes
        self.surface_cache.clear()
        
        # Adjust performance settings
        if level <= 1:
            self.enable_glow_effects = False
            self.enable_animations = False
        elif level == 2:
            self.enable_glow_effects = True
            self.enable_animations = False
        else:
            self.enable_glow_effects = True
            self.enable_animations = True
    
    def draw_ornate_button(self, surface: pygame.Surface, rect: pygame.Rect, 
                          text: str, state: str = 'normal') -> pygame.Rect:
        """Draw optimized Hades-style ornate Egyptian button."""
        
        with profile_operation("hades_theme_button"):
            cache_key = self._get_button_cache_key(rect, text, state)
            
            # Check cache first
            if cache_key in self.surface_cache:
                surface.blit(self.surface_cache[cache_key], rect.topleft)
                self.render_stats["cache_hits"] += 1
                return rect
            
            self.render_stats["cache_misses"] += 1
            
            # Create button surface
            button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            
            # Determine colors based on state
            color_map = {
                'normal': {'bg': self.colors['pharaoh_bronze'], 'border': self.colors['duat_gold']},
                'hover': {'bg': self.colors['duat_gold'], 'border': self.colors['hover_gold']},
                'active': {'bg': self.colors['active_bronze'], 'border': self.colors['desert_amber']},
                'disabled': {'bg': self.colors['disabled_gray'], 'border': self.colors['disabled_gray']}
            }
            
            colors = color_map.get(state, color_map['normal'])
            
            # Simplified rendering for lower detail levels
            if self.current_detail_level <= 1:
                # Minimal detail - simple rectangles
                pygame.draw.rect(button_surface, colors['bg'], 
                               (0, 0, rect.width, rect.height))
                pygame.draw.rect(button_surface, colors['border'], 
                               (0, 0, rect.width, rect.height), 
                               self.dimensions['border_width'])
            else:
                # Full detail rendering
                self._draw_full_detail_button(button_surface, rect, colors, state)
            
            # Draw text
            self._draw_button_text(button_surface, rect, text, state)
            
            # Cache the button if we have space
            if len(self.surface_cache) < self.cache_max_size:
                self.surface_cache[cache_key] = button_surface.copy()
            
            # Blit to main surface
            surface.blit(button_surface, rect.topleft)
            self.render_stats["buttons_rendered"] += 1
            
            return rect
    
    def _draw_full_detail_button(self, button_surface: pygame.Surface, rect: pygame.Rect, 
                                colors: Dict, state: str):
        """Draw full detail button with all effects."""
        # Draw shadow (if detail level allows)
        if self.current_detail_level >= 2:
            shadow_rect = pygame.Rect(3, 3, rect.width, rect.height)
            pygame.draw.rect(button_surface, (0, 0, 0, 120), shadow_rect, 
                           border_radius=self.dimensions['corner_radius'])
        
        # Draw main button background
        main_rect = pygame.Rect(0, 0, rect.width, rect.height)
        pygame.draw.rect(button_surface, colors['bg'], main_rect, 
                        border_radius=self.dimensions['corner_radius'])
        
        # Draw border
        border_width = self.dimensions['border_width']
        pygame.draw.rect(button_surface, colors['border'], main_rect, 
                        width=border_width, border_radius=self.dimensions['corner_radius'])
        
        # Draw inner decorative border (high detail only)
        if self.current_detail_level >= 3:
            inner_rect = pygame.Rect(border_width, border_width, 
                                   rect.width - border_width*2, rect.height - border_width*2)
            pygame.draw.rect(button_surface, colors['border'], inner_rect, 
                           width=1, border_radius=self.dimensions['corner_radius'])
            
            # Draw corner decorations
            self._draw_corner_decorations(button_surface, main_rect, colors['border'])
        
        # Add glow effect for hover state
        if state == 'hover' and self.enable_glow_effects and self.current_detail_level >= 2:
            glow_surface = self._get_glow_surface(self.dimensions['glow_radius'], colors['border'])
            glow_rect = glow_surface.get_rect(center=main_rect.center)
            button_surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
            self.render_stats["glow_effects_rendered"] += 1
    
    def _draw_button_text(self, button_surface: pygame.Surface, rect: pygame.Rect, 
                         text: str, state: str):
        """Draw button text with optimized rendering."""
        font = self._get_cached_font('body')
        
        # Text color
        text_color = self.colors['papyrus_cream'] if state != 'disabled' else self.colors['disabled_gray']
        
        # Render text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(rect.width//2, rect.height//2))
        
        # Add text shadow for better detail levels
        if self.current_detail_level >= 2:
            shadow_surface = font.render(text, True, self.colors['obsidian_black'])
            shadow_rect = pygame.Rect(text_rect.x + 1, text_rect.y + 1, text_rect.width, text_rect.height)
            button_surface.blit(shadow_surface, shadow_rect)
        
        button_surface.blit(text_surface, text_rect)
    
    def _draw_corner_decorations(self, surface: pygame.Surface, rect: pygame.Rect, 
                                color: Tuple[int, int, int]):
        """Draw simplified corner decorations."""
        size = min(6, self.dimensions['corner_radius'])  # Smaller decorations
        
        # Only draw decorations if detail level is high enough
        if self.current_detail_level < 3:
            return
        
        positions = [
            (rect.left + 5, rect.top + 5),      # Top-left
            (rect.right - 5, rect.top + 5),     # Top-right
            (rect.left + 5, rect.bottom - 5),   # Bottom-left
            (rect.right - 5, rect.bottom - 5)   # Bottom-right
        ]
        
        for x, y in positions:
            pygame.draw.circle(surface, color, (x, y), 2)
    
    def draw_card_frame(self, surface: pygame.Surface, rect: pygame.Rect, 
                       card_type: str = 'normal', rarity: str = 'common') -> pygame.Rect:
        """Draw optimized Hades-style card frame."""
        
        with profile_operation("hades_theme_card_frame"):
            # Cache key for card frames
            cache_key = f"card_{rect.width}x{rect.height}_{card_type}_{rarity}_{self.current_detail_level}"
            
            if cache_key in self.surface_cache:
                surface.blit(self.surface_cache[cache_key], rect.topleft)
                return rect
            
            # Create card surface
            card_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            
            # Rarity-based colors
            rarity_colors = {
                'common': self.colors['pharaoh_bronze'],
                'uncommon': self.colors['sacred_turquoise'], 
                'rare': self.colors['duat_gold'],
                'epic': self.colors['royal_purple'],
                'legendary': self.colors['underworld_crimson']
            }
            
            frame_color = rarity_colors.get(rarity, self.colors['pharaoh_bronze'])
            
            # Simplified rendering based on detail level
            if self.current_detail_level <= 1:
                # Simple frame
                pygame.draw.rect(card_surface, self.colors['papyrus_cream'], 
                               (0, 0, rect.width, rect.height))
                pygame.draw.rect(card_surface, frame_color, 
                               (0, 0, rect.width, rect.height), 
                               self.dimensions['border_width'])
            else:
                self._draw_full_detail_card(card_surface, rect, frame_color)
            
            # Cache if we have space
            if len(self.surface_cache) < self.cache_max_size:
                self.surface_cache[cache_key] = card_surface.copy()
            
            surface.blit(card_surface, rect.topleft)
            
            return rect
    
    def _draw_full_detail_card(self, card_surface: pygame.Surface, rect: pygame.Rect, 
                              frame_color: Tuple[int, int, int]):
        """Draw full detail card with all effects."""
        # Draw shadow
        if self.current_detail_level >= 2:
            shadow_rect = pygame.Rect(2, 2, rect.width, rect.height)
            pygame.draw.rect(card_surface, (0, 0, 0, 100), shadow_rect,
                           border_radius=self.dimensions['corner_radius'])
        
        # Draw papyrus background
        main_rect = pygame.Rect(0, 0, rect.width, rect.height)
        pygame.draw.rect(card_surface, self.colors['papyrus_cream'], main_rect,
                        border_radius=self.dimensions['corner_radius'])
        
        # Apply papyrus texture if detail level allows
        if self.current_detail_level >= 3 and 'papyrus' in self.textures:
            texture = self.textures['papyrus']
            # Tile the texture
            for x in range(0, rect.width, texture.get_width()):
                for y in range(0, rect.height, texture.get_height()):
                    card_surface.blit(texture, (x, y), special_flags=pygame.BLEND_MULTIPLY)
        
        # Draw frame border
        border_width = self.dimensions['border_width'] + 1
        pygame.draw.rect(card_surface, frame_color, main_rect,
                        width=border_width, border_radius=self.dimensions['corner_radius'])
        
        # Inner decorative border
        if self.current_detail_level >= 3:
            inner_rect = pygame.Rect(border_width, border_width,
                                   rect.width - border_width*2, rect.height - border_width*2)
            pygame.draw.rect(card_surface, self.colors['duat_gold'], inner_rect,
                           width=1, border_radius=self.dimensions['corner_radius'])
            
            # Add Egyptian decorations
            self._draw_egyptian_card_decorations(card_surface, rect, frame_color)
    
    def _draw_egyptian_card_decorations(self, surface: pygame.Surface, rect: pygame.Rect, 
                                       color: Tuple[int, int, int]):
        """Draw simplified Egyptian decorations."""
        if self.current_detail_level < 3:
            return
        
        # Top center ankh symbol (simplified)
        center_x = rect.width // 2
        top_y = 8
        
        # Simple ankh representation
        pygame.draw.circle(surface, color, (center_x, top_y), 3, 1)
        pygame.draw.line(surface, color, (center_x, top_y + 2), (center_x, top_y + 6), 1)
        pygame.draw.line(surface, color, (center_x - 2, top_y + 4), (center_x + 2, top_y + 4), 1)
    
    def draw_health_orb(self, surface: pygame.Surface, center: Tuple[int, int], 
                       current_health: int, max_health: int, radius: int = 30) -> pygame.Rect:
        """Draw optimized Egyptian-style health orb."""
        
        with profile_operation("hades_theme_health_orb"):
            # Health ratio for color interpolation
            health_ratio = current_health / max_health if max_health > 0 else 0
            
            # Simplified color calculation
            if health_ratio > 0.5:
                color = self.colors['success_green']
            elif health_ratio > 0.25:
                color = self.colors['duat_gold']
            else:
                color = self.colors['error_red']
            
            # Draw simplified orb based on detail level
            if self.current_detail_level <= 1:
                # Simple circle
                pygame.draw.circle(surface, color, center, radius)
                pygame.draw.circle(surface, self.colors['duat_gold'], center, radius, 2)
            else:
                # Full detail orb
                self._draw_full_detail_orb(surface, center, radius, color, current_health)
            
            return pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    
    def _draw_full_detail_orb(self, surface: pygame.Surface, center: Tuple[int, int], 
                             radius: int, color: Tuple[int, int, int], health: int):
        """Draw full detail health orb."""
        # Glow effect
        if self.enable_glow_effects and self.current_detail_level >= 2:
            for i in range(3):
                glow_radius = radius + i * 2
                alpha = max(0, 40 - i * 10)
                glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*color, alpha), (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surface, (center[0] - glow_radius, center[1] - glow_radius))
            
            self.render_stats["glow_effects_rendered"] += 1
        
        # Main orb
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, self.colors['duat_gold'], center, radius, 3)
        
        # Scarab symbol (simplified)
        if self.current_detail_level >= 3:
            self._draw_simple_scarab(surface, center, radius - 5)
        
        # Health text
        font = self._get_cached_font('body')
        health_text = str(health)
        text_surface = font.render(health_text, True, self.colors['papyrus_cream'])
        text_rect = text_surface.get_rect(center=(center[0], center[1] + radius//3))
        surface.blit(text_surface, text_rect)
    
    def _draw_simple_scarab(self, surface: pygame.Surface, center: Tuple[int, int], size: int):
        """Draw simplified scarab symbol."""
        x, y = center
        
        # Simple scarab body
        body_rect = pygame.Rect(x - size//3, y - size//2, size//1.5, size)
        pygame.draw.ellipse(surface, self.colors['obsidian_black'], body_rect)
        
        # Simple wings
        wing_size = size // 4
        left_wing = pygame.Rect(x - size//2, y - wing_size//2, wing_size, wing_size)
        right_wing = pygame.Rect(x + size//6, y - wing_size//2, wing_size, wing_size)
        pygame.draw.ellipse(surface, self.colors['obsidian_black'], left_wing)
        pygame.draw.ellipse(surface, self.colors['obsidian_black'], right_wing)
    
    def draw_title_text(self, surface: pygame.Surface, text: str, 
                       position: Tuple[int, int], style: str = 'title') -> pygame.Rect:
        """Draw optimized title text with Egyptian styling."""
        
        with profile_operation("hades_theme_title_text"):
            font = self._get_cached_font(style)
            
            # Simplified text rendering based on detail level
            if self.current_detail_level <= 1:
                # Simple text
                text_surface = font.render(text, True, self.colors['papyrus_cream'])
                text_rect = text_surface.get_rect(center=position)
                surface.blit(text_surface, text_rect)
                return text_rect
            
            # Full detail text with effects
            return self._draw_full_detail_text(surface, text, position, font)
    
    def _draw_full_detail_text(self, surface: pygame.Surface, text: str, 
                              position: Tuple[int, int], font: pygame.font.Font) -> pygame.Rect:
        """Draw full detail text with shadow and outline."""
        # Text shadow
        if self.current_detail_level >= 2:
            shadow_surface = font.render(text, True, self.colors['obsidian_black'])
            shadow_rect = shadow_surface.get_rect(center=(position[0] + 2, position[1] + 2))
            surface.blit(shadow_surface, shadow_rect)
        
        # Golden outline (high detail only)
        if self.current_detail_level >= 3:
            outline_surface = font.render(text, True, self.colors['duat_gold'])
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    outline_rect = outline_surface.get_rect(center=(position[0] + dx, position[1] + dy))
                    surface.blit(outline_surface, outline_rect)
        
        # Main text
        main_surface = font.render(text, True, self.colors['papyrus_cream'])
        main_rect = main_surface.get_rect(center=position)
        surface.blit(main_surface, main_rect)
        
        return main_rect
    
    def draw_background_overlay(self, surface: pygame.Surface, alpha: int = 120):
        """Draw optimized atmospheric Egyptian underworld overlay."""
        
        with profile_operation("hades_theme_background_overlay"):
            if self.current_detail_level <= 1:
                # Simple overlay
                overlay = pygame.Surface(self.display_size, pygame.SRCALPHA)
                overlay.fill((*self.colors['obsidian_black'], alpha))
                surface.blit(overlay, (0, 0))
                return
            
            # Full detail gradient overlay
            self._draw_gradient_overlay(surface, alpha)
    
    def _draw_gradient_overlay(self, surface: pygame.Surface, alpha: int):
        """Draw gradient overlay with optimized rendering."""
        overlay = pygame.Surface(self.display_size, pygame.SRCALPHA)
        
        # Simplified gradient - fewer steps for performance
        height = self.display_size[1]
        steps = 20 if self.current_detail_level >= 3 else 10
        
        for i in range(steps):
            y_ratio = i / steps
            y_pos = int(height * y_ratio)
            step_height = height // steps
            
            # Color interpolation
            brightness = int(20 * y_ratio)
            color = (
                self.colors['obsidian_black'][0] + brightness,
                self.colors['obsidian_black'][1] + int(brightness * 0.75),
                self.colors['obsidian_black'][2] + int(brightness * 0.5),
                alpha
            )
            
            step_surface = pygame.Surface((self.display_size[0], step_height), pygame.SRCALPHA)
            step_surface.fill(color)
            overlay.blit(step_surface, (0, y_pos))
        
        surface.blit(overlay, (0, 0))
    
    def clear_cache(self):
        """Clear surface cache to free memory."""
        self.surface_cache.clear()
        self.glow_cache.clear()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get theme rendering performance statistics."""
        cache_efficiency = 0.0
        total_requests = self.render_stats["cache_hits"] + self.render_stats["cache_misses"]
        if total_requests > 0:
            cache_efficiency = self.render_stats["cache_hits"] / total_requests
        
        return {
            "detail_level": self.current_detail_level,
            "cache_size": len(self.surface_cache),
            "cache_efficiency": cache_efficiency,
            "glow_cache_size": len(self.glow_cache),
            "render_stats": self.render_stats.copy(),
            "performance_settings": {
                "glow_effects": self.enable_glow_effects,
                "animations": self.enable_animations
            }
        }
    
    def optimize_for_performance(self, target_fps: float, current_fps: float):
        """Automatically optimize theme settings based on performance."""
        if current_fps < target_fps * 0.8:  # 20% below target
            # Reduce detail level
            if self.current_detail_level > 0:
                self.set_detail_level(self.current_detail_level - 1)
        elif current_fps > target_fps * 1.1:  # 10% above target
            # Increase detail level
            if self.current_detail_level < self.max_detail_level:
                self.set_detail_level(self.current_detail_level + 1)
    
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get color by name from the Egyptian palette."""
        return self.colors.get(color_name, self.colors['papyrus_cream'])
    
    def get_font_size(self, style: str) -> int:
        """Get font size for given style."""
        return self.fonts.get(style, self.fonts['body'])['size']