"""
Enhanced Main Menu Screen - Sprint 1 UI Improvements
Uses the new enhanced ultrawide layout system for better space utilization
and cleaner visual hierarchy.
"""

import pygame
import math
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER
from ..responsive.enhanced_ultrawide_layout import enhanced_ultrawide_layout, LayoutZone, ElementType
from ...core.state_manager import GameState
from ...assets.smart_asset_loader import smart_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton
from ..effects.professional_transitions import professional_transitions, TransitionType

class MenuAction(Enum):
    """Main menu actions."""
    START_GAME = auto()
    DECK_BUILDER = auto()
    COLLECTION = auto()
    SETTINGS = auto()
    ANIMATION_FORGE = auto()
    QUIT = auto()

class EnhancedMainMenu:
    """
    Enhanced main menu using new ultrawide layout system.
    Maximizes screen real estate while maintaining clean presentation.
    """
    
    def __init__(self, on_menu_action: Optional[Callable[[MenuAction], None]] = None):
        self.on_menu_action = on_menu_action
        self.layout = enhanced_ultrawide_layout
        
        # Load background
        self._load_background()
        
        # Create UI elements using enhanced layout
        self._create_title()
        self._create_buttons()
        self._create_side_panels()
        
        # Animation state
        self.animation_time = 0.0
        self.hover_button = None
        
    def _load_background(self):
        """Load and prepare background with proper scaling."""
        # Try to load 4K background
        bg_surface = smart_asset_loader.load_asset('menu_background')
        if bg_surface:
            # Scale to screen size while maintaining aspect ratio
            self.background = pygame.transform.smoothscale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            # Fallback: create gradient background
            self.background = self._create_gradient_background()
    
    def _create_gradient_background(self):
        """Create Egyptian-themed gradient background."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Egyptian sunset gradient: deep blue to gold
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            
            # Interpolate between dark blue and gold
            r = int(Colors.DARK_BLUE[0] + (Colors.GOLD_DARK[0] - Colors.DARK_BLUE[0]) * progress)
            g = int(Colors.DARK_BLUE[1] + (Colors.GOLD_DARK[1] - Colors.DARK_BLUE[1]) * progress)
            b = int(Colors.DARK_BLUE[2] + (Colors.GOLD_DARK[2] - Colors.DARK_BLUE[2]) * progress)
            
            color = (r, g, b)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
        
        return surface
    
    def _create_title(self):
        """Create title using enhanced typography."""
        title_font_size = self.layout.get_font_size('huge_title')
        subtitle_font_size = self.layout.get_font_size('title')
        
        self.title_font = pygame.font.Font(None, title_font_size)
        self.subtitle_font = pygame.font.Font(None, subtitle_font_size)
        
        # Position title in top zone
        top_zone = self.layout.get_zone_rect(LayoutZone.TOP_BAR)
        
        self.title_text = self.title_font.render("SANDS OF DUAT", True, Colors.GOLD)
        self.subtitle_text = self.subtitle_font.render("Egyptian Underworld Card Game", True, Colors.PAPYRUS)
        
        # Center titles in top zone
        self.title_pos = self.layout.center_in_zone(
            LayoutZone.TOP_BAR, 
            self.title_text.get_width(), 
            self.title_text.get_height()
        )
        
        # Position subtitle below title
        subtitle_y = self.title_pos[1] + self.title_text.get_height() + self.layout.get_spacing('small')
        self.subtitle_pos = (
            top_zone.centerx - self.subtitle_text.get_width() // 2,
            subtitle_y
        )
    
    def _create_buttons(self):
        """Create menu buttons using enhanced layout."""
        # Button definitions
        button_configs = [
            ("Start Journey", MenuAction.START_GAME, Colors.GOLD),
            ("Deck Builder", MenuAction.DECK_BUILDER, Colors.LAPIS_LAZULI),
            ("Hall of Gods", MenuAction.COLLECTION, Colors.PURPLE),
            ("Animation Forge", MenuAction.ANIMATION_FORGE, Colors.GREEN),
            ("Settings", MenuAction.SETTINGS, Colors.GRAY),
            ("Exit to Afterlife", MenuAction.QUIT, Colors.RED)
        ]
        
        # Get button positions using layout system
        button_positions = self.layout.create_button_layout(
            LayoutZone.CENTER_MAIN, 
            len(button_configs), 
            'vertical'
        )
        
        button_width, button_height = self.layout.get_element_size(ElementType.BUTTON)
        button_font_size = self.layout.get_font_size('button')
        
        self.buttons = []
        for i, (text, action, color) in enumerate(button_configs):
            if i < len(button_positions):
                pos = button_positions[i]
                button = AnimatedButton(
                    x=pos[0],
                    y=pos[1], 
                    width=button_width,
                    height=button_height,
                    text=text,
                    font_size=button_font_size,
                    action=lambda a=action: self.on_menu_action(a) if self.on_menu_action else None
                )
                button.action = action  # Store action for reference
                self.buttons.append(button)
    
    def _create_side_panels(self):
        """Create side panels with game information."""
        panel_font_size = self.layout.get_font_size('body')
        self.panel_font = pygame.font.Font(None, panel_font_size)
        
        # Left panel: Game lore
        left_zone = self.layout.get_zone_rect(LayoutZone.LEFT_PANEL)
        lore_texts = [
            "Navigate the Egyptian",
            "underworld as a soul",
            "seeking eternal rest.",
            "",
            "Build powerful decks",
            "with cards blessed",
            "by ancient gods."
        ]
        
        self.left_panel_texts = []
        y_offset = left_zone.y + self.layout.get_spacing('large')
        
        for text in lore_texts:
            if text:  # Skip empty lines for spacing
                surface = self.panel_font.render(text, True, Colors.PAPYRUS)
                pos = (left_zone.x + self.layout.get_spacing('medium'), y_offset)
                self.left_panel_texts.append((surface, pos))
            y_offset += self.layout.get_spacing('medium')
        
        # Right panel: Game stats/features
        right_zone = self.layout.get_zone_rect(LayoutZone.RIGHT_PANEL)
        features = [
            "Features:",
            "",
            "• Hades-level polish", 
            "• Egyptian mythology",
            "• Strategic combat",
            "• Beautiful 4K art",
            "• Ultrawide support",
            "",
            "Version 1.0"
        ]
        
        self.right_panel_texts = []
        y_offset = right_zone.y + self.layout.get_spacing('large')
        
        for text in features:
            if text:
                color = Colors.GOLD if text.startswith("•") else Colors.PAPYRUS
                surface = self.panel_font.render(text, True, color)
                pos = (right_zone.x + self.layout.get_spacing('medium'), y_offset)
                self.right_panel_texts.append((surface, pos))
            y_offset += self.layout.get_spacing('medium')
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: tuple):
        """Update menu logic."""
        self.animation_time += dt
        
        # Handle events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                for button in self.buttons:
                    if button.handle_click(mouse_pos):
                        if self.on_menu_action and hasattr(button, 'action'):
                            self.on_menu_action(button.action)
        
        # Update buttons
        self.hover_button = None
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed[0] if mouse_pressed else False)
            if button.is_hovered:
                self.hover_button = button
    
    def render(self, surface: pygame.Surface):
        """Render enhanced menu."""
        # Background
        surface.blit(self.background, (0, 0))
        
        # Add subtle overlay for better text contrast
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(30)  # Light overlay
        surface.blit(overlay, (0, 0))
        
        # Render zone debug borders (if in debug mode)
        self._render_debug_zones(surface)
        
        # Title
        surface.blit(self.title_text, self.title_pos)
        surface.blit(self.subtitle_text, self.subtitle_pos)
        
        # Side panels
        for text_surface, pos in self.left_panel_texts:
            surface.blit(text_surface, pos)
        
        for text_surface, pos in self.right_panel_texts:
            surface.blit(text_surface, pos)
        
        # Buttons
        for button in self.buttons:
            button.render(surface)
        
        # Hover effect
        if self.hover_button:
            self._render_hover_effect(surface, self.hover_button)
    
    def _render_debug_zones(self, surface: pygame.Surface):
        """Render layout zones for debugging (optional)."""
        # Only show in debug mode
        debug_mode = False  # Set to True for layout debugging
        
        if debug_mode:
            for zone in LayoutZone:
                rect = self.layout.get_zone_rect(zone)
                pygame.draw.rect(surface, Colors.RED, rect, 2)
    
    def _render_hover_effect(self, surface: pygame.Surface, button):
        """Render subtle hover effect."""
        # Golden glow effect
        glow_size = 20
        glow_color = (*Colors.GOLD, 50)  # Semi-transparent gold
        
        # Create glow surface
        glow_surface = pygame.Surface(
            (button.width + glow_size * 2, button.height + glow_size * 2), 
            pygame.SRCALPHA
        )
        
        # Draw glow
        glow_rect = pygame.Rect(glow_size, glow_size, button.width, button.height)
        pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=10)
        
        # Blur effect (simple approximation)
        for i in range(3):
            glow_surface.set_alpha(glow_surface.get_alpha() // 2)
            surface.blit(glow_surface, (button.x - glow_size, button.y - glow_size))
    
    def reset_animations(self):
        """Reset all animations."""
        self.animation_time = 0.0
        for button in self.buttons:
            if hasattr(button, 'reset_animation'):
                button.reset_animation()