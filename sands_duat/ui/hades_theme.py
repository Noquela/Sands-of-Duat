"""
Hades-Style UI Theme for Sands of Duat
Egyptian underworld aesthetic inspired by Hades game design.
"""

import pygame
import math
from typing import Tuple, Dict, Optional
from pathlib import Path

class HadesEgyptianTheme:
    """Professional Hades-style theme for Egyptian underworld."""
    
    def __init__(self, display_size: Tuple[int, int]):
        self.display_size = display_size
        self.scale_factor = min(display_size[0] / 1920, display_size[1] / 1080)
        
        # Egyptian Underworld Color Palette (Hades-inspired)
        self.colors = {
            # Primary Colors
            'duat_gold': (218, 165, 32),        # #DAA520 - Divine gold
            'pharaoh_bronze': (205, 127, 50),   # #CD7F32 - Royal bronze  
            'underworld_crimson': (139, 0, 0),  # #8B0000 - Blood red
            'night_blue': (25, 25, 112),        # #191970 - Deep night
            'obsidian_black': (12, 12, 12),     # #0C0C0C - Void black
            'papyrus_cream': (245, 230, 163),   # #F5E6A3 - Ancient paper
            
            # Secondary Colors
            'sacred_turquoise': (64, 224, 208), # #40E0D0 - Divine protection
            'desert_amber': (255, 191, 0),      # #FFBF00 - Solar energy
            'mummy_linen': (250, 240, 230),     # #FAF0E6 - Burial wraps
            'hieroglyph_green': (0, 100, 0),    # #006400 - Sacred writing
            'royal_purple': (102, 51, 153),     # #663399 - Divine royalty
            
            # UI States
            'hover_gold': (255, 215, 0),        # #FFD700 - Interactive highlight
            'active_bronze': (184, 134, 11),    # #B8860B - Active state
            'disabled_gray': (105, 105, 105),   # #696969 - Inactive
            'error_red': (220, 20, 60),         # #DC143C - Warning/Error
            'success_green': (34, 139, 34),     # #228B22 - Success state
            
            # Transparency variants
            'glass_gold': (218, 165, 32, 180),  # Semi-transparent gold
            'shadow_black': (0, 0, 0, 120),     # Soft shadow
            'glow_white': (255, 255, 255, 80),  # Soft glow
        }
        
        # Typography Settings
        self.fonts = {
            'title': {'size': int(48 * self.scale_factor), 'bold': True},
            'header': {'size': int(32 * self.scale_factor), 'bold': True}, 
            'body': {'size': int(18 * self.scale_factor), 'bold': False},
            'small': {'size': int(14 * self.scale_factor), 'bold': False},
            'card_title': {'size': int(16 * self.scale_factor), 'bold': True},
            'card_text': {'size': int(12 * self.scale_factor), 'bold': False},
        }
        
        # UI Element Dimensions
        self.dimensions = {
            'button_height': int(50 * self.scale_factor),
            'button_padding': int(20 * self.scale_factor),
            'card_width': int(120 * self.scale_factor),
            'card_height': int(180 * self.scale_factor),
            'border_width': max(2, int(3 * self.scale_factor)),
            'corner_radius': int(8 * self.scale_factor),
            'glow_radius': int(6 * self.scale_factor),
        }
        
        # Load or create UI textures
        self._load_textures()
    
    def _load_textures(self):
        """Load Egyptian decorative textures."""
        self.textures = {}
        
        # Try to load existing textures, create placeholders if not found
        texture_dir = Path("game_assets/ui_elements")
        texture_dir.mkdir(parents=True, exist_ok=True)
        
        # Create basic textures programmatically
        self._create_basic_textures()
    
    def _create_basic_textures(self):
        """Create basic Egyptian-style textures."""
        # Papyrus texture pattern
        papyrus_surface = pygame.Surface((64, 64))
        papyrus_surface.fill(self.colors['papyrus_cream'])
        
        # Add papyrus fiber pattern
        for i in range(0, 64, 8):
            for j in range(0, 64, 8):
                if (i + j) % 16 == 0:
                    pygame.draw.rect(papyrus_surface, self.colors['desert_amber'], 
                                   (i, j, 6, 2))
                    pygame.draw.rect(papyrus_surface, self.colors['desert_amber'], 
                                   (i, j, 2, 6))
        
        self.textures['papyrus'] = papyrus_surface
        
        # Gold metallic texture
        gold_surface = pygame.Surface((32, 32))
        gold_surface.fill(self.colors['duat_gold'])
        
        # Add metallic shine pattern
        for i in range(0, 32, 4):
            color = self.colors['hover_gold'] if i % 8 == 0 else self.colors['pharaoh_bronze']
            pygame.draw.line(gold_surface, color, (i, 0), (i, 32))
        
        self.textures['gold_metal'] = gold_surface
    
    def draw_ornate_button(self, surface: pygame.Surface, rect: pygame.Rect, 
                          text: str, state: str = 'normal') -> pygame.Rect:
        """Draw a Hades-style ornate Egyptian button."""
        
        # Determine colors based on state
        color_map = {
            'normal': {'bg': self.colors['pharaoh_bronze'], 'border': self.colors['duat_gold']},
            'hover': {'bg': self.colors['duat_gold'], 'border': self.colors['hover_gold']},
            'active': {'bg': self.colors['active_bronze'], 'border': self.colors['desert_amber']},
            'disabled': {'bg': self.colors['disabled_gray'], 'border': self.colors['disabled_gray']}
        }
        
        colors = color_map.get(state, color_map['normal'])
        
        # Draw shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(surface, self.colors['shadow_black'], shadow_rect, 
                        border_radius=self.dimensions['corner_radius'])
        
        # Draw main button background
        pygame.draw.rect(surface, colors['bg'], rect, 
                        border_radius=self.dimensions['corner_radius'])
        
        # Draw ornate border
        border_width = self.dimensions['border_width']
        pygame.draw.rect(surface, colors['border'], rect, 
                        width=border_width, border_radius=self.dimensions['corner_radius'])
        
        # Add inner decorative border
        inner_rect = rect.inflate(-border_width*2, -border_width*2)
        pygame.draw.rect(surface, colors['border'], inner_rect, 
                        width=1, border_radius=self.dimensions['corner_radius'])
        
        # Draw hieroglyphic decorations on corners
        self._draw_corner_decorations(surface, rect, colors['border'])
        
        # Draw text with shadow
        font_size = self.fonts['body']['size']
        font = pygame.font.Font(None, font_size)
        
        # Text shadow
        text_surface_shadow = font.render(text, True, self.colors['obsidian_black'])
        text_rect = text_surface_shadow.get_rect(center=(rect.centerx + 1, rect.centery + 1))
        surface.blit(text_surface_shadow, text_rect)
        
        # Main text
        text_color = self.colors['papyrus_cream'] if state != 'disabled' else self.colors['disabled_gray']
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
        return rect
    
    def _draw_corner_decorations(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int]):
        """Draw Egyptian corner decorations."""
        size = 8
        
        # Top-left corner
        points = [(rect.left + 5, rect.top + 5), 
                  (rect.left + 5 + size, rect.top + 5),
                  (rect.left + 5, rect.top + 5 + size)]
        pygame.draw.polygon(surface, color, points)
        
        # Top-right corner
        points = [(rect.right - 5, rect.top + 5),
                  (rect.right - 5 - size, rect.top + 5), 
                  (rect.right - 5, rect.top + 5 + size)]
        pygame.draw.polygon(surface, color, points)
        
        # Bottom-left corner
        points = [(rect.left + 5, rect.bottom - 5),
                  (rect.left + 5 + size, rect.bottom - 5),
                  (rect.left + 5, rect.bottom - 5 - size)]
        pygame.draw.polygon(surface, color, points)
        
        # Bottom-right corner
        points = [(rect.right - 5, rect.bottom - 5),
                  (rect.right - 5 - size, rect.bottom - 5),
                  (rect.right - 5, rect.bottom - 5 + size)]
        pygame.draw.polygon(surface, color, points)
    
    def draw_card_frame(self, surface: pygame.Surface, rect: pygame.Rect, 
                       card_type: str = 'normal', rarity: str = 'common') -> pygame.Rect:
        """Draw an ornate Hades-style card frame."""
        
        # Rarity-based colors
        rarity_colors = {
            'common': self.colors['pharaoh_bronze'],
            'uncommon': self.colors['sacred_turquoise'], 
            'rare': self.colors['duat_gold'],
            'epic': self.colors['royal_purple'],
            'legendary': self.colors['underworld_crimson']
        }
        
        frame_color = rarity_colors.get(rarity, self.colors['pharaoh_bronze'])
        
        # Draw card shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, self.colors['shadow_black'], shadow_rect,
                        border_radius=self.dimensions['corner_radius'])
        
        # Draw papyrus background
        surface.blit(self.textures['papyrus'], rect, 
                    special_flags=pygame.BLEND_MULTIPLY)
        
        # Draw ornate frame border
        border_width = self.dimensions['border_width'] + 1
        pygame.draw.rect(surface, frame_color, rect,
                        width=border_width, border_radius=self.dimensions['corner_radius'])
        
        # Inner decorative border
        inner_rect = rect.inflate(-border_width*2, -border_width*2)
        pygame.draw.rect(surface, self.colors['duat_gold'], inner_rect,
                        width=1, border_radius=self.dimensions['corner_radius'])
        
        # Draw Egyptian decorative elements
        self._draw_egyptian_card_decorations(surface, rect, frame_color)
        
        return inner_rect
    
    def _draw_egyptian_card_decorations(self, surface: pygame.Surface, rect: pygame.Rect, color: Tuple[int, int, int]):
        """Draw Egyptian hieroglyphic decorations on card."""
        # Top center ankh symbol
        ankh_size = 6
        center_x = rect.centerx
        top_y = rect.top + 8
        
        # Ankh loop
        pygame.draw.circle(surface, color, (center_x, top_y), ankh_size//2, 2)
        # Ankh cross
        pygame.draw.line(surface, color, (center_x, top_y + ankh_size//2), 
                        (center_x, top_y + ankh_size), 2)
        pygame.draw.line(surface, color, (center_x - ankh_size//2, top_y + ankh_size//3),
                        (center_x + ankh_size//2, top_y + ankh_size//3), 2)
        
        # Side decorations
        side_size = 4
        # Left side
        pygame.draw.rect(surface, color, (rect.left + 2, rect.centery - side_size//2, 
                                        2, side_size))
        # Right side  
        pygame.draw.rect(surface, color, (rect.right - 4, rect.centery - side_size//2,
                                        2, side_size))
    
    def draw_health_orb(self, surface: pygame.Surface, center: Tuple[int, int], 
                       current_health: int, max_health: int, radius: int = 30) -> pygame.Rect:
        """Draw Egyptian-style health orb with scarab design."""
        
        # Health ratio for color interpolation
        health_ratio = current_health / max_health if max_health > 0 else 0
        
        # Color interpolation from red to gold based on health
        if health_ratio > 0.5:
            # Gold to green
            ratio = (health_ratio - 0.5) * 2
            color = (
                int(self.colors['underworld_crimson'][0] * (1-ratio) + self.colors['success_green'][0] * ratio),
                int(self.colors['underworld_crimson'][1] * (1-ratio) + self.colors['success_green'][1] * ratio),
                int(self.colors['underworld_crimson'][2] * (1-ratio) + self.colors['success_green'][2] * ratio)
            )
        else:
            # Red to gold
            ratio = health_ratio * 2
            color = (
                int(self.colors['error_red'][0] * (1-ratio) + self.colors['duat_gold'][0] * ratio),
                int(self.colors['error_red'][1] * (1-ratio) + self.colors['duat_gold'][1] * ratio), 
                int(self.colors['error_red'][2] * (1-ratio) + self.colors['duat_gold'][2] * ratio)
            )
        
        # Draw glow effect
        for i in range(5):
            glow_radius = radius + i * 3
            glow_alpha = max(0, 50 - i * 10)
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*color, glow_alpha), (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (center[0] - glow_radius, center[1] - glow_radius))
        
        # Draw main orb
        pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(surface, self.colors['duat_gold'], center, radius, 3)
        
        # Draw scarab beetle silhouette
        self._draw_scarab_symbol(surface, center, radius - 5, self.colors['obsidian_black'])
        
        # Draw health text
        font = pygame.font.Font(None, int(radius * 0.8))
        health_text = f"{current_health}"
        text_surface = font.render(health_text, True, self.colors['papyrus_cream'])
        text_rect = text_surface.get_rect(center=(center[0], center[1] + radius//3))
        surface.blit(text_surface, text_rect)
        
        return pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
    
    def _draw_scarab_symbol(self, surface: pygame.Surface, center: Tuple[int, int], 
                           size: int, color: Tuple[int, int, int]):
        """Draw simplified scarab beetle symbol."""
        x, y = center
        
        # Scarab body (oval)
        body_rect = pygame.Rect(x - size//3, y - size//2, size//1.5, size)
        pygame.draw.ellipse(surface, color, body_rect)
        
        # Scarab wings (smaller ovals)
        wing_size = size // 3
        left_wing = pygame.Rect(x - size//2, y - wing_size//2, wing_size, wing_size)
        right_wing = pygame.Rect(x + size//6, y - wing_size//2, wing_size, wing_size)
        pygame.draw.ellipse(surface, color, left_wing)
        pygame.draw.ellipse(surface, color, right_wing)
    
    def draw_mana_crystal(self, surface: pygame.Surface, center: Tuple[int, int],
                         current_mana: int, max_mana: int, size: int = 25) -> pygame.Rect:
        """Draw Egyptian ankh-shaped mana crystal."""
        
        # Mana ratio for glow intensity
        mana_ratio = current_mana / max_mana if max_mana > 0 else 0
        
        # Blue crystal color with golden ankh
        crystal_color = self.colors['night_blue']
        ankh_color = self.colors['duat_gold']
        
        # Draw crystal glow
        if mana_ratio > 0:
            glow_intensity = int(mana_ratio * 100)
            glow_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*crystal_color, glow_intensity), 
                             (size * 1.5, size * 1.5), size * 1.5)
            surface.blit(glow_surface, (center[0] - size * 1.5, center[1] - size * 1.5))
        
        # Draw crystal base
        crystal_rect = pygame.Rect(center[0] - size, center[1] - size, size * 2, size * 2)
        pygame.draw.ellipse(surface, crystal_color, crystal_rect)
        pygame.draw.ellipse(surface, ankh_color, crystal_rect, 2)
        
        # Draw ankh symbol
        ankh_size = size // 2
        # Ankh loop
        pygame.draw.circle(surface, ankh_color, center, ankh_size//2, 2)
        # Ankh vertical line
        pygame.draw.line(surface, ankh_color, (center[0], center[1] + ankh_size//2),
                        (center[0], center[1] + ankh_size), 3)
        # Ankh horizontal line  
        pygame.draw.line(surface, ankh_color, (center[0] - ankh_size//2, center[1] + ankh_size//4),
                        (center[0] + ankh_size//2, center[1] + ankh_size//4), 3)
        
        # Draw mana text
        font = pygame.font.Font(None, int(size * 0.6))
        mana_text = f"{current_mana}"
        text_surface = font.render(mana_text, True, self.colors['papyrus_cream'])
        text_rect = text_surface.get_rect(center=(center[0], center[1] + size + 8))
        surface.blit(text_surface, text_rect)
        
        return crystal_rect
    
    def draw_title_text(self, surface: pygame.Surface, text: str, 
                       position: Tuple[int, int], style: str = 'title') -> pygame.Rect:
        """Draw ornate title text with Egyptian styling."""
        font_config = self.fonts.get(style, self.fonts['title'])
        font = pygame.font.Font(None, font_config['size'])
        if font_config['bold']:
            font.set_bold(True)
        
        # Draw text shadow
        shadow_surface = font.render(text, True, self.colors['obsidian_black'])
        shadow_rect = shadow_surface.get_rect(center=(position[0] + 2, position[1] + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Draw golden outline
        outline_surface = font.render(text, True, self.colors['duat_gold'])
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                outline_rect = outline_surface.get_rect(center=(position[0] + dx, position[1] + dy))
                surface.blit(outline_surface, outline_rect)
        
        # Draw main text
        main_surface = font.render(text, True, self.colors['papyrus_cream'])
        main_rect = main_surface.get_rect(center=position)
        surface.blit(main_surface, main_rect)
        
        return main_rect
    
    def draw_background_overlay(self, surface: pygame.Surface, alpha: int = 120):
        """Draw atmospheric Egyptian underworld overlay."""
        overlay = pygame.Surface(self.display_size, pygame.SRCALPHA)
        
        # Gradient from dark top to lighter bottom
        height = self.display_size[1]
        for y in range(height):
            ratio = y / height
            r = int(self.colors['obsidian_black'][0] + ratio * 20)
            g = int(self.colors['obsidian_black'][1] + ratio * 15)  
            b = int(self.colors['obsidian_black'][2] + ratio * 10)
            color = (r, g, b, alpha)
            
            line_surface = pygame.Surface((self.display_size[0], 1), pygame.SRCALPHA)
            line_surface.fill(color)
            overlay.blit(line_surface, (0, y))
        
        surface.blit(overlay, (0, 0))
    
    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Get color by name from the Egyptian palette."""
        return self.colors.get(color_name, self.colors['papyrus_cream'])
    
    def get_font_size(self, style: str) -> int:
        """Get font size for given style."""
        return self.fonts.get(style, self.fonts['body'])['size']
    
    def draw_screen_transition(self, surface: pygame.Surface, transition_type: str, 
                              progress: float, overlay_alpha: int = 200) -> None:
        """Draw Egyptian-themed screen transitions with sand and mystical effects."""
        width, height = surface.get_size()
        
        if transition_type == "sand_wipe":
            self._draw_sand_wipe_transition(surface, progress, width, height)
        elif transition_type == "hieroglyph_fade":
            self._draw_hieroglyph_fade_transition(surface, progress, width, height)
        elif transition_type == "ankh_spiral":
            self._draw_ankh_spiral_transition(surface, progress, width, height)
        elif transition_type == "duat_portal":
            self._draw_duat_portal_transition(surface, progress, width, height)
        else:
            # Default fade with Egyptian overlay
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            alpha = int(overlay_alpha * progress)
            overlay.fill((*self.colors['obsidian_black'], alpha))
            surface.blit(overlay, (0, 0))
    
    def _draw_sand_wipe_transition(self, surface: pygame.Surface, progress: float, 
                                  width: int, height: int) -> None:
        """Draw sand particles flowing across screen transition."""
        import random
        random.seed(42)  # Consistent pattern
        
        # Create sand particle overlay
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Sand flows from right to left
        sand_width = int(width * progress * 1.2)
        
        for _ in range(min(200, sand_width // 4)):
            x = random.randint(width - sand_width, width + 50)
            y = random.randint(0, height)
            size = random.randint(1, 4)
            alpha = random.randint(100, 255)
            
            # Vary sand colors for realism
            base_color = self.colors['desert_amber']
            variation = random.randint(-30, 30)
            sand_color = (
                max(0, min(255, base_color[0] + variation)),
                max(0, min(255, base_color[1] + variation)),
                max(0, min(255, base_color[2] + variation)),
                alpha
            )
            
            pygame.draw.circle(overlay, sand_color, (x, y), size)
        
        surface.blit(overlay, (0, 0))
    
    def _draw_hieroglyph_fade_transition(self, surface: pygame.Surface, progress: float,
                                        width: int, height: int) -> None:
        """Draw hieroglyphs appearing across screen during transition."""
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Background fade
        bg_alpha = int(180 * progress)
        overlay.fill((*self.colors['obsidian_black'], bg_alpha))
        
        # Draw hieroglyphs at various scales and positions
        glyph_alpha = int(255 * max(0, progress - 0.3))
        if glyph_alpha > 0:
            glyph_color = (*self.colors['duat_gold'], glyph_alpha)
            
            # Ankh symbols
            for i in range(5):
                x = (width // 6) * (i + 1)
                y = height // 3
                self._draw_transition_ankh(overlay, (x, y), 20, glyph_color)
            
            # Eye of Horus symbols  
            for i in range(4):
                x = (width // 5) * (i + 1)
                y = 2 * height // 3
                self._draw_transition_eye(overlay, (x, y), 15, glyph_color)
        
        surface.blit(overlay, (0, 0))
    
    def _draw_ankh_spiral_transition(self, surface: pygame.Surface, progress: float,
                                    width: int, height: int) -> None:
        """Draw spiral of ankh symbols expanding from center."""
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(width**2 + height**2) // 2
        
        # Number of ankhs increases with progress
        num_ankhs = int(20 * progress)
        spiral_radius = max_radius * progress
        
        for i in range(num_ankhs):
            angle = (i / num_ankhs) * 4 * math.pi  # 2 full rotations
            radius = spiral_radius * (i / num_ankhs)
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            # Fade ankhs based on distance from center
            fade_ratio = 1.0 - (radius / spiral_radius) if spiral_radius > 0 else 1.0
            alpha = int(255 * fade_ratio * progress)
            
            if 0 <= x < width and 0 <= y < height and alpha > 0:
                ankh_color = (*self.colors['sacred_turquoise'], alpha)
                self._draw_transition_ankh(overlay, (int(x), int(y)), 12, ankh_color)
        
        # Add central background fade
        bg_alpha = int(150 * progress)
        center_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        center_overlay.fill((*self.colors['night_blue'], bg_alpha))
        overlay.blit(center_overlay, (0, 0))
        
        surface.blit(overlay, (0, 0))
    
    def _draw_duat_portal_transition(self, surface: pygame.Surface, progress: float,
                                    width: int, height: int) -> None:
        """Draw portal to the Duat opening from center."""
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 3
        
        # Portal grows from center
        portal_radius = int(max_radius * progress)
        
        if portal_radius > 0:
            # Create swirling portal effect
            num_rings = 8
            for ring in range(num_rings):
                ring_radius = portal_radius * (ring + 1) / num_rings
                ring_alpha = int(200 * (1 - ring / num_rings) * progress)
                
                if ring_alpha > 0:
                    # Alternate colors for mystical effect
                    color = self.colors['royal_purple'] if ring % 2 == 0 else self.colors['underworld_crimson']
                    ring_color = (*color, ring_alpha)
                    
                    # Draw ring
                    ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(ring_surface, ring_color, (ring_radius, ring_radius), ring_radius, 3)
                    overlay.blit(ring_surface, (center_x - ring_radius, center_y - ring_radius))
        
        # Add background fade
        bg_alpha = int(180 * progress)
        bg_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_overlay.fill((*self.colors['obsidian_black'], bg_alpha))
        surface.blit(bg_overlay, (0, 0))
        surface.blit(overlay, (0, 0))
    
    def _draw_transition_ankh(self, surface: pygame.Surface, center: Tuple[int, int], 
                             size: int, color: Tuple[int, int, int, int]) -> None:
        """Draw ankh symbol for transitions."""
        x, y = center
        
        # Ankh loop
        pygame.draw.circle(surface, color, (x, y - size//3), size//3, 2)
        # Ankh vertical line
        pygame.draw.line(surface, color, (x, y - size//6), (x, y + size//2), 3)
        # Ankh horizontal line
        pygame.draw.line(surface, color, (x - size//3, y), (x + size//3, y), 3)
    
    def _draw_transition_eye(self, surface: pygame.Surface, center: Tuple[int, int],
                            size: int, color: Tuple[int, int, int, int]) -> None:
        """Draw Eye of Horus for transitions."""
        x, y = center
        
        # Eye outline
        eye_rect = pygame.Rect(x - size, y - size//2, size * 2, size)
        pygame.draw.arc(surface, color, eye_rect, 0, math.pi, 2)
        
        # Eye pupil
        pygame.draw.circle(surface, color, (x, y), size//3)
        
        # Eye decoration
        pygame.draw.line(surface, color, (x + size//2, y + size//4), 
                        (x + size, y + size//2), 2)
    
    def draw_loading_indicator(self, surface: pygame.Surface, center: Tuple[int, int],
                              progress: float, style: str = "ankh_rotation") -> None:
        """Draw Egyptian-themed loading indicators."""
        if style == "ankh_rotation":
            self._draw_ankh_loading(surface, center, progress)
        elif style == "sand_timer":
            self._draw_sand_timer_loading(surface, center, progress)
        elif style == "scarab_circle":
            self._draw_scarab_circle_loading(surface, center, progress)
    
    def _draw_ankh_loading(self, surface: pygame.Surface, center: Tuple[int, int], 
                          progress: float) -> None:
        """Draw rotating ankh loading indicator."""
        x, y = center
        size = 30
        rotation = progress * 360
        
        # Create rotated ankh surface
        ankh_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        # Draw ankh on temporary surface
        temp_center = (size, size)
        self._draw_transition_ankh(ankh_surface, temp_center, size, 
                                  (*self.colors['duat_gold'], 255))
        
        # Rotate surface
        rotated_surface = pygame.transform.rotate(ankh_surface, rotation)
        
        # Blit to main surface
        rotated_rect = rotated_surface.get_rect(center=center)
        surface.blit(rotated_surface, rotated_rect)
    
    def _draw_sand_timer_loading(self, surface: pygame.Surface, center: Tuple[int, int],
                                progress: float) -> None:
        """Draw hourglass with flowing sand loading indicator."""
        x, y = center
        size = 25
        
        # Draw hourglass outline
        hourglass_color = self.colors['pharaoh_bronze']
        
        # Top bulb
        top_rect = pygame.Rect(x - size//2, y - size, size, size//2)
        pygame.draw.ellipse(surface, hourglass_color, top_rect, 2)
        
        # Bottom bulb
        bottom_rect = pygame.Rect(x - size//2, y + size//2, size, size//2)
        pygame.draw.ellipse(surface, hourglass_color, bottom_rect, 2)
        
        # Neck
        pygame.draw.line(surface, hourglass_color, 
                        (x - size//4, y - size//2), (x + size//4, y + size//2), 2)
        pygame.draw.line(surface, hourglass_color,
                        (x + size//4, y - size//2), (x - size//4, y + size//2), 2)
        
        # Sand level (decreases in top, increases in bottom)
        sand_color = self.colors['desert_amber']
        
        # Top sand (empties as progress increases)
        top_sand_height = int((size//2) * (1 - progress))
        if top_sand_height > 0:
            top_sand_rect = pygame.Rect(x - size//3, y - size + (size//2 - top_sand_height),
                                       2 * size//3, top_sand_height)
            pygame.draw.ellipse(surface, sand_color, top_sand_rect)
        
        # Bottom sand (fills as progress increases)
        bottom_sand_height = int((size//2) * progress)
        if bottom_sand_height > 0:
            bottom_sand_rect = pygame.Rect(x - size//3, y + size - bottom_sand_height,
                                          2 * size//3, bottom_sand_height)
            pygame.draw.ellipse(surface, sand_color, bottom_sand_rect)
    
    def _draw_scarab_circle_loading(self, surface: pygame.Surface, center: Tuple[int, int],
                                   progress: float) -> None:
        """Draw scarabs moving in circle loading indicator."""
        x, y = center
        radius = 40
        num_scarabs = 6
        
        for i in range(num_scarabs):
            angle = (progress * 360 + i * (360 / num_scarabs)) * math.pi / 180
            scarab_x = x + radius * math.cos(angle)
            scarab_y = y + radius * math.sin(angle)
            
            # Draw simplified scarab
            scarab_color = self.colors['hieroglyph_green']
            scarab_size = 6
            
            # Scarab body
            pygame.draw.ellipse(surface, scarab_color, 
                               (scarab_x - scarab_size, scarab_y - scarab_size//2,
                                scarab_size * 2, scarab_size))
            
            # Scarab wings
            wing_size = 3
            pygame.draw.circle(surface, scarab_color, 
                              (int(scarab_x - scarab_size//2), int(scarab_y)), wing_size)
            pygame.draw.circle(surface, scarab_color,
                              (int(scarab_x + scarab_size//2), int(scarab_y)), wing_size)