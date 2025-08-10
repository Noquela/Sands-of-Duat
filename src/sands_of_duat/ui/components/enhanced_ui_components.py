"""
Enhanced UI Components System
Professional Egyptian-themed UI components using ultra-high resolution assets.
"""

import pygame
import math
from typing import Tuple, Optional, Callable
from enum import Enum

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT,
    FontSizes
)
from ...core.asset_loader import get_asset_loader


class IconType(Enum):
    """Types of UI icons available."""
    HEALTH = "ui_ankh_health_icon"
    MANA = "ui_scarab_energy_icon" 
    ATTACK = "ui_khopesh_attack_icon"
    DEFENSE = "ui_shield_defense_icon"


class EgyptianPanel:
    """
    Professional Egyptian-themed panel with ornate decorations.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 title: str = "", translucent: bool = True):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.translucent = translucent
        self.asset_loader = get_asset_loader()
        
        # Create ornate panel surface
        self.panel_surface = self._create_panel_surface()
    
    def _create_panel_surface(self) -> pygame.Surface:
        """Create the ornate panel background."""
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Base panel color
        if self.translucent:
            base_color = (*Colors.BLACK, 180)
        else:
            base_color = (30, 25, 40, 255)
        
        surface.fill(base_color)
        
        # Golden ornate border
        border_color = Colors.GOLD
        pygame.draw.rect(surface, border_color, (0, 0, self.rect.width, self.rect.height), 3)
        
        # Corner decorations
        corner_size = min(20, self.rect.width // 10, self.rect.height // 10)
        self._draw_corner_ornaments(surface, corner_size, border_color)
        
        # Inner decorative lines
        inner_margin = 8
        inner_rect = pygame.Rect(inner_margin, inner_margin, 
                               self.rect.width - inner_margin*2, 
                               self.rect.height - inner_margin*2)
        pygame.draw.rect(surface, (*border_color, 100), inner_rect, 1)
        
        return surface
    
    def _draw_corner_ornaments(self, surface: pygame.Surface, size: int, color: Tuple[int, int, int]):
        """Draw Egyptian-style corner ornaments."""
        # Top-left
        pygame.draw.polygon(surface, color, [
            (0, size), (0, 0), (size, 0)
        ])
        pygame.draw.line(surface, color, (size//2, 0), (size//2, size//2), 2)
        pygame.draw.line(surface, color, (0, size//2), (size//2, size//2), 2)
        
        # Top-right
        pygame.draw.polygon(surface, color, [
            (self.rect.width - size, 0), (self.rect.width, 0), (self.rect.width, size)
        ])
        pygame.draw.line(surface, color, (self.rect.width - size//2, 0), (self.rect.width - size//2, size//2), 2)
        pygame.draw.line(surface, color, (self.rect.width, size//2), (self.rect.width - size//2, size//2), 2)
        
        # Bottom corners
        pygame.draw.polygon(surface, color, [
            (0, self.rect.height - size), (0, self.rect.height), (size, self.rect.height)
        ])
        pygame.draw.polygon(surface, color, [
            (self.rect.width - size, self.rect.height), (self.rect.width, self.rect.height), 
            (self.rect.width, self.rect.height - size)
        ])
    
    def render(self, surface: pygame.Surface):
        """Render the panel."""
        surface.blit(self.panel_surface, self.rect.topleft)
        
        # Render title if provided
        if self.title:
            font = pygame.font.Font(None, FontSizes.SUBTITLE)
            title_surface = font.render(self.title, True, Colors.GOLD)
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 15)
            
            # Title background
            title_bg = pygame.Surface((title_surface.get_width() + 20, title_surface.get_height() + 8), pygame.SRCALPHA)
            title_bg.fill((*Colors.BLACK, 150))
            pygame.draw.rect(title_bg, Colors.GOLD, (0, 0, title_bg.get_width(), title_bg.get_height()), 1)
            
            surface.blit(title_bg, (title_rect.x - 10, title_rect.y - 4))
            surface.blit(title_surface, title_rect)


class EnhancedStatusBar:
    """
    Professional status bar with Egyptian icons and smooth animations.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 icon_type: IconType, max_value: int = 100):
        self.rect = pygame.Rect(x, y, width, height)
        self.icon_type = icon_type
        self.max_value = max_value
        self.current_value = max_value
        self.target_value = max_value
        self.asset_loader = get_asset_loader()
        
        # Animation state
        self.animation_speed = 5.0
        self.glow_phase = 0.0
        
        # Load icon
        self.icon = self._load_icon()
    
    def _load_icon(self) -> Optional[pygame.Surface]:
        """Load the appropriate icon from assets."""
        try:
            icon_surface = self.asset_loader.load_ui_icon(self.icon_type.value)
            if icon_surface:
                # Scale icon to appropriate size
                icon_size = min(self.rect.height - 4, 32)
                return pygame.transform.smoothscale(icon_surface, (icon_size, icon_size))
        except Exception as e:
            print(f"[STATUS_BAR] Could not load icon {self.icon_type.value}: {e}")
        return None
    
    def set_value(self, value: int):
        """Set target value for smooth animation."""
        self.target_value = max(0, min(self.max_value, value))
    
    def update(self, dt: float):
        """Update animations."""
        self.glow_phase += dt * 2
        
        # Smooth value animation
        if abs(self.current_value - self.target_value) > 0.1:
            diff = self.target_value - self.current_value
            self.current_value += diff * self.animation_speed * dt
        else:
            self.current_value = self.target_value
    
    def render(self, surface: pygame.Surface):
        """Render the status bar."""
        # Background
        bg_color = (20, 15, 30)
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, Colors.GOLD, self.rect, 2)
        
        # Fill based on current value
        if self.current_value > 0:
            fill_ratio = self.current_value / self.max_value
            fill_width = int((self.rect.width - 4) * fill_ratio)
            fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, fill_width, self.rect.height - 4)
            
            # Color based on icon type
            if self.icon_type == IconType.HEALTH:
                fill_color = Colors.GREEN if fill_ratio > 0.3 else Colors.RED
            elif self.icon_type == IconType.MANA:
                fill_color = Colors.LAPIS_LAZULI
            else:
                fill_color = Colors.GOLD
            
            pygame.draw.rect(surface, fill_color, fill_rect)
            
            # Glow effect when low
            if fill_ratio < 0.3:
                glow_alpha = int(100 * abs(math.sin(self.glow_phase)))
                glow_surface = pygame.Surface(fill_rect.size, pygame.SRCALPHA)
                glow_surface.fill((*fill_color, glow_alpha))
                surface.blit(glow_surface, fill_rect.topleft, special_flags=pygame.BLEND_ADD)
        
        # Icon
        if self.icon:
            icon_x = self.rect.right + 8
            icon_y = self.rect.centery - self.icon.get_height() // 2
            surface.blit(self.icon, (icon_x, icon_y))
        
        # Value text
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        value_text = f"{int(self.current_value)}/{self.max_value}"
        text_surface = font.render(value_text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text shadow
        shadow_surface = font.render(value_text, True, Colors.BLACK)
        surface.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)


class CardPreviewPanel:
    """
    Professional card preview panel showing full art and details.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.asset_loader = get_asset_loader()
        self.current_card = None
        self.fade_alpha = 0
        self.target_alpha = 0
        
        # Create panel background
        self.panel = EgyptianPanel(x, y, width, height, "Divine Inspection")
    
    def show_card(self, card_name: str, card_data: dict = None):
        """Show a card in the preview panel."""
        self.current_card = {
            'name': card_name,
            'data': card_data or {},
            'artwork': self.asset_loader.load_card_art_by_name(card_name)
        }
        self.target_alpha = 255
    
    def hide(self):
        """Hide the preview panel."""
        self.target_alpha = 0
    
    def update(self, dt: float):
        """Update fade animations."""
        if abs(self.fade_alpha - self.target_alpha) > 1:
            diff = self.target_alpha - self.fade_alpha
            self.fade_alpha += diff * 8 * dt  # Fast fade
        else:
            self.fade_alpha = self.target_alpha
            
        if self.fade_alpha <= 0:
            self.current_card = None
    
    def render(self, surface: pygame.Surface):
        """Render the card preview."""
        if not self.current_card or self.fade_alpha <= 0:
            return
        
        # Create surface with alpha
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Render panel background
        temp_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.panel.render(temp_surface)
        panel_surface.blit(temp_surface, (0, 0))
        
        # Render card artwork if available
        if self.current_card['artwork']:
            art_size = min(self.rect.width - 40, 300)
            art_rect = pygame.Rect(20, 60, art_size, int(art_size * 1.5))  # Card aspect ratio
            
            scaled_artwork = pygame.transform.smoothscale(
                self.current_card['artwork'], 
                (art_rect.width, art_rect.height)
            )
            panel_surface.blit(scaled_artwork, art_rect.topleft)
            
            # Artwork border
            pygame.draw.rect(panel_surface, Colors.GOLD, art_rect, 3)
        
        # Card name
        font_name = pygame.font.Font(None, FontSizes.SUBTITLE)
        name_surface = font_name.render(self.current_card['name'], True, Colors.GOLD)
        name_rect = name_surface.get_rect(centerx=self.rect.width//2, y=self.rect.height - 80)
        panel_surface.blit(name_surface, name_rect)
        
        # Card details
        if self.current_card['data']:
            details_y = name_rect.bottom + 10
            font_details = pygame.font.Font(None, FontSizes.CARD_TEXT)
            
            details = [
                f"Cost: {self.current_card['data'].get('cost', 'N/A')}",
                f"Attack: {self.current_card['data'].get('attack', 'N/A')}",
                f"Health: {self.current_card['data'].get('health', 'N/A')}",
                f"Rarity: {self.current_card['data'].get('rarity', 'Common').title()}"
            ]
            
            for detail in details:
                detail_surface = font_details.render(detail, True, Colors.PAPYRUS)
                detail_rect = detail_surface.get_rect(centerx=self.rect.width//2, y=details_y)
                panel_surface.blit(detail_surface, detail_rect)
                details_y += 20
        
        # Apply fade alpha
        panel_surface.set_alpha(int(self.fade_alpha))
        surface.blit(panel_surface, self.rect.topleft)


class ResponsiveButton:
    """
    Professional Egyptian-themed button with responsive sizing.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 on_click: Optional[Callable] = None, style: str = "default"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.style = style
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.hover_progress = 0.0
        self.press_progress = 0.0
        
        # Colors based on style
        if style == "primary":
            self.base_color = Colors.LAPIS_LAZULI
            self.hover_color = Colors.GOLD
        elif style == "danger":
            self.base_color = Colors.RED
            self.hover_color = (255, 100, 100)
        else:  # default
            self.base_color = (40, 35, 60)
            self.hover_color = Colors.GOLD
    
    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int]) -> bool:
        """Handle mouse events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.is_pressed = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(mouse_pos):
                if self.on_click:
                    self.on_click()
                self.is_pressed = False
                return True
            self.is_pressed = False
            
        return False
    
    def update(self, dt: float, mouse_pos: Tuple[int, int]):
        """Update button animations."""
        # Hover detection
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Hover animation
        if self.is_hovered:
            self.hover_progress = min(1.0, self.hover_progress + dt * 6)
        else:
            self.hover_progress = max(0.0, self.hover_progress - dt * 8)
        
        # Press animation
        if self.is_pressed:
            self.press_progress = min(1.0, self.press_progress + dt * 12)
        else:
            self.press_progress = max(0.0, self.press_progress - dt * 10)
    
    def render(self, surface: pygame.Surface):
        """Render the button."""
        # Calculate current color
        t = self.hover_progress
        current_color = tuple(
            int(self.base_color[i] + (self.hover_color[i] - self.base_color[i]) * t)
            for i in range(3)
        )
        
        # Button rect with press effect
        render_rect = self.rect.copy()
        if self.press_progress > 0:
            offset = int(3 * self.press_progress)
            render_rect.x += offset
            render_rect.y += offset
        
        # Background
        pygame.draw.rect(surface, current_color, render_rect)
        
        # Border with glow effect
        border_color = Colors.GOLD
        if self.hover_progress > 0:
            # Glow effect
            glow_alpha = int(100 * self.hover_progress)
            glow_surface = pygame.Surface((render_rect.width + 6, render_rect.height + 6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*border_color, glow_alpha), 
                           (0, 0, render_rect.width + 6, render_rect.height + 6), 3)
            surface.blit(glow_surface, (render_rect.x - 3, render_rect.y - 3))
        
        pygame.draw.rect(surface, border_color, render_rect, 2)
        
        # Text
        font = pygame.font.Font(None, FontSizes.BUTTON)
        text_surface = font.render(self.text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=render_rect.center)
        
        # Text shadow
        shadow_surface = font.render(self.text, True, Colors.BLACK)
        surface.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)