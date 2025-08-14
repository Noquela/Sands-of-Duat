"""
Enhanced Card Rendering System
Professional card renderer using ultra-high resolution frames and artwork.
"""

import pygame
import math
from typing import Optional, Tuple, Dict
from enum import Enum

from ...core.constants import Colors, Layout, FontSizes
from ...core.asset_loader import get_asset_loader


class CardRarity(Enum):
    """Card rarity levels."""
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class EnhancedCardRenderer:
    """
    Professional card renderer with themed frames and ultra-high resolution artwork.
    """
    
    def __init__(self):
        self.asset_loader = get_asset_loader()
        
        # Rarity color schemes
        self.rarity_colors = {
            CardRarity.COMMON: {
                'border': Colors.DESERT_SAND,
                'glow': (245, 245, 220, 100),
                'text': Colors.BLACK
            },
            CardRarity.RARE: {
                'border': (65, 105, 225),
                'glow': (65, 105, 225, 120),
                'text': Colors.WHITE
            },
            CardRarity.EPIC: {
                'border': (138, 43, 226),
                'glow': (138, 43, 226, 140),
                'text': Colors.WHITE
            },
            CardRarity.LEGENDARY: {
                'border': Colors.GOLD,
                'glow': (*Colors.GOLD, 160),
                'text': Colors.BLACK
            }
        }
        
        print("[CARD_RENDERER] Enhanced card rendering system initialized")
    
    def render_card(self, surface: pygame.Surface, x: int, y: int, width: int, height: int,
                   card_name: str, card_data: Dict, hover_intensity: float = 0.0,
                   glow_intensity: float = 0.0) -> pygame.Rect:
        """
        Render a professional card with themed frame and ultra-HD artwork.
        
        Args:
            surface: Target surface to render on
            x, y: Card position
            width, height: Card dimensions
            card_name: Name of the card
            card_data: Card data dictionary (cost, attack, health, rarity, etc.)
            hover_intensity: Hover effect intensity (0.0 to 1.0)
            glow_intensity: Glow effect intensity (0.0 to 1.0)
        
        Returns:
            pygame.Rect: The card's bounding rectangle
        """
        card_rect = pygame.Rect(x, y, width, height)
        
        # Get rarity and color scheme
        rarity_str = card_data.get('rarity', 'common').lower()
        try:
            rarity = CardRarity(rarity_str)
        except ValueError:
            rarity = CardRarity.COMMON
        
        colors = self.rarity_colors[rarity]
        
        # Create card surface
        card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Render glow effect first (behind card)
        if glow_intensity > 0:
            self._render_card_glow(surface, card_rect, colors['glow'], glow_intensity)
        
        # Load and render themed frame
        frame_asset = self._load_card_frame(rarity)
        if frame_asset:
            # Scale frame to card size
            scaled_frame = pygame.transform.smoothscale(frame_asset, (width, height))
            card_surface.blit(scaled_frame, (0, 0))
        else:
            # Fallback: draw themed frame
            self._draw_fallback_frame(card_surface, width, height, colors)
        
        # Load and render card artwork
        artwork = self.asset_loader.load_card_art_by_name(card_name)
        if artwork:
            self._render_card_artwork(card_surface, artwork, width, height)
        else:
            # Fallback artwork
            self._draw_fallback_artwork(card_surface, width, height, rarity)
        
        # Render card text elements
        self._render_card_text(card_surface, card_data, width, height, colors)
        
        # Apply hover effect
        if hover_intensity > 0:
            self._apply_hover_effect(card_surface, hover_intensity, colors)
        
        # Blit final card to surface
        surface.blit(card_surface, (x, y))
        
        return card_rect
    
    def _load_card_frame(self, rarity: CardRarity) -> Optional[pygame.Surface]:
        """Load themed card frame based on rarity."""
        frame_mapping = {
            CardRarity.LEGENDARY: "ui_card_frame_legendary",
            CardRarity.EPIC: "ui_card_frame_epic", 
            CardRarity.RARE: "ui_card_frame_rare",
            CardRarity.COMMON: "ui_card_frame_common"
        }
        
        frame_name = frame_mapping.get(rarity)
        if frame_name:
            return self.asset_loader.load_ui_element(frame_name)
        return None
    
    def _draw_fallback_frame(self, surface: pygame.Surface, width: int, height: int, colors: Dict):
        """Draw fallback frame when themed frame is not available."""
        # Background
        bg_color = (240, 235, 220) if colors['text'] == Colors.BLACK else (30, 25, 40)
        surface.fill(bg_color)
        
        # Border
        pygame.draw.rect(surface, colors['border'], (0, 0, width, height), 3)
        
        # Inner decorative border
        inner_rect = pygame.Rect(5, 5, width - 10, height - 10)
        pygame.draw.rect(surface, colors['border'], inner_rect, 1)
        
        # Corner decorations
        corner_size = 12
        for corner_pos in [(0, 0), (width - corner_size, 0), 
                          (0, height - corner_size), (width - corner_size, height - corner_size)]:
            corner_rect = pygame.Rect(corner_pos[0], corner_pos[1], corner_size, corner_size)
            pygame.draw.rect(surface, colors['border'], corner_rect)
    
    def _render_card_artwork(self, surface: pygame.Surface, artwork: pygame.Surface, 
                           width: int, height: int):
        """Render ultra-high resolution card artwork."""
        # Define artwork area (top portion of card)
        art_margin = 8
        art_height = int(height * 0.55)  # 55% of card height for artwork
        art_rect = pygame.Rect(art_margin, art_margin + 25, 
                              width - art_margin * 2, art_height - 35)
        
        # Scale artwork with quality preservation
        scaled_artwork = pygame.transform.smoothscale(artwork, (art_rect.width, art_rect.height))
        surface.blit(scaled_artwork, art_rect.topleft)
        
        # Artwork border
        pygame.draw.rect(surface, Colors.GOLD, art_rect, 2)
    
    def _draw_fallback_artwork(self, surface: pygame.Surface, width: int, height: int, 
                             rarity: CardRarity):
        """Draw fallback artwork when card art is not available."""
        art_margin = 8
        art_height = int(height * 0.55)
        art_rect = pygame.Rect(art_margin, art_margin + 25, 
                              width - art_margin * 2, art_height - 35)
        
        # Rarity-based fallback colors
        fallback_colors = {
            CardRarity.COMMON: Colors.DESERT_SAND,
            CardRarity.RARE: Colors.LAPIS_LAZULI,
            CardRarity.EPIC: (138, 43, 226),
            CardRarity.LEGENDARY: Colors.GOLD
        }
        
        base_color = fallback_colors.get(rarity, Colors.DESERT_SAND)
        surface.fill(base_color, art_rect)
        
        # Add Egyptian-style pattern
        pattern_color = tuple(max(0, c - 40) for c in base_color[:3])
        
        # Hieroglyphic-style patterns
        center_x = art_rect.centerx
        center_y = art_rect.centery
        
        # Ankh symbol
        pygame.draw.circle(surface, pattern_color, (center_x, center_y - 15), 8, 2)
        pygame.draw.line(surface, pattern_color, (center_x, center_y - 5), (center_x, center_y + 20), 3)
        pygame.draw.line(surface, pattern_color, (center_x - 10, center_y), (center_x + 10, center_y), 3)
        
        pygame.draw.rect(surface, Colors.GOLD, art_rect, 2)
    
    def _render_card_text(self, surface: pygame.Surface, card_data: Dict, 
                         width: int, height: int, colors: Dict):
        """Render card text elements with proper positioning."""
        text_color = colors['text']
        
        # Card name
        name = card_data.get('name', 'Unknown Card')
        name_font = pygame.font.Font(None, FontSizes.CARD_NAME)
        name_surface = name_font.render(name, True, text_color)
        name_rect = name_surface.get_rect(center=(width // 2, height - 80))
        
        # Name background for readability
        name_bg = pygame.Surface((name_surface.get_width() + 10, name_surface.get_height() + 4), pygame.SRCALPHA)
        # Use RGB color and set alpha separately to avoid invalid color argument
        if text_color == Colors.WHITE:
            name_bg.fill((0, 0, 0))
            name_bg.set_alpha(150)
        else:
            name_bg.fill((255, 255, 255))
            name_bg.set_alpha(150)
        surface.blit(name_bg, (name_rect.x - 5, name_rect.y - 2))
        surface.blit(name_surface, name_rect)
        
        # Cost (top-left corner)
        cost = card_data.get('cost', 0)
        cost_font = pygame.font.Font(None, FontSizes.BUTTON)
        cost_surface = cost_font.render(str(cost), True, Colors.WHITE)
        
        # Cost gem
        cost_center = (20, 20)
        pygame.draw.circle(surface, Colors.LAPIS_LAZULI, cost_center, 15)
        pygame.draw.circle(surface, Colors.GOLD, cost_center, 15, 2)
        
        cost_rect = cost_surface.get_rect(center=cost_center)
        surface.blit(cost_surface, cost_rect)
        
        # Attack and Health (for creatures)
        card_type = card_data.get('card_type', 'creature')
        if card_type == 'creature':
            # Attack (bottom-left)
            attack = card_data.get('attack', 0)
            attack_center = (20, height - 20)
            pygame.draw.circle(surface, Colors.DESERT_SAND, attack_center, 12)
            pygame.draw.circle(surface, Colors.GOLD, attack_center, 12, 2)
            
            attack_surface = cost_font.render(str(attack), True, Colors.BLACK)
            attack_rect = attack_surface.get_rect(center=attack_center)
            surface.blit(attack_surface, attack_rect)
            
            # Health (bottom-right)
            health = card_data.get('health', 0)
            health_center = (width - 20, height - 20)
            pygame.draw.circle(surface, Colors.LAPIS_LAZULI, health_center, 12)
            pygame.draw.circle(surface, Colors.GOLD, health_center, 12, 2)
            
            health_surface = cost_font.render(str(health), True, Colors.WHITE)
            health_rect = health_surface.get_rect(center=health_center)
            surface.blit(health_surface, health_rect)
        
        # Description (bottom area)
        description = card_data.get('description', '')
        if description:
            desc_font = pygame.font.Font(None, FontSizes.CARD_TEXT)
            self._render_wrapped_text(surface, description, desc_font, text_color,
                                    pygame.Rect(8, height - 55, width - 16, 40))
    
    def _render_wrapped_text(self, surface: pygame.Surface, text: str, font: pygame.font.Font,
                           color: Tuple[int, int, int], rect: pygame.Rect):
        """Render text with word wrapping."""
        words = text.split()
        lines = []
        current_line = []
        
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
        for line in lines[:2]:  # Max 2 lines
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect(center=(rect.centerx, y_offset + 10))
            
            # Text background for readability
            if color == Colors.WHITE:
                bg_surface = pygame.Surface((line_surface.get_width() + 8, line_surface.get_height() + 2), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0))
                bg_surface.set_alpha(120)
                surface.blit(bg_surface, (line_rect.x - 4, line_rect.y - 1))
            
            surface.blit(line_surface, line_rect)
            y_offset += 18
    
    def _render_card_glow(self, surface: pygame.Surface, card_rect: pygame.Rect, 
                         glow_color: Tuple[int, int, int, int], intensity: float):
        """Render card glow effect."""
        glow_size = int(20 * intensity)
        glow_rect = card_rect.inflate(glow_size, glow_size)
        glow_alpha = int(glow_color[3] * intensity)
        
        # Create glow surface
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        
        # Multi-layer glow
        for i in range(8):
            alpha = max(0, glow_alpha - i * 20)
            if alpha <= 0:
                break
            
            layer_color = (*glow_color[:3], alpha)
            layer_rect = pygame.Rect(i, i, glow_rect.width - i * 2, glow_rect.height - i * 2)
            pygame.draw.rect(glow_surface, layer_color, layer_rect, max(1, 3 - i // 2))
        
        surface.blit(glow_surface, (glow_rect.x, glow_rect.y))
    
    def _apply_hover_effect(self, surface: pygame.Surface, intensity: float, colors: Dict):
        """Apply hover effect to card surface."""
        # Create hover overlay
        hover_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        hover_alpha = int(50 * intensity)
        hover_surface.fill((*colors['border'][:3], hover_alpha))
        
        # Subtle brightness increase
        surface.blit(hover_surface, (0, 0), special_flags=pygame.BLEND_ADD)


# Global instance for easy access
enhanced_card_renderer = EnhancedCardRenderer()