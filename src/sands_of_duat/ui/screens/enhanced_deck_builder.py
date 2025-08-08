"""
Enhanced Deck Builder Screen - SPRINT 4: Deck Builder Excellence
Features Hades-level polish with smooth animations and professional UX.
"""

import pygame
import math
import time
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.state_manager import GameState
from .deck_builder import create_deck_builder, DeckBuilderScreen
from .transition_screen import TransitionType
from ..components.animated_button import AnimatedButton

class DeckBuilderAction(Enum):
    """Deck builder actions."""
    BACK_TO_MENU = auto()
    SAVE_DECK = auto()
    CLEAR_DECK = auto()
    EXPORT_DECK = auto()

class EnhancedDeckBuilder:
    """
    Professional deck builder with Hades-level polish and Egyptian theming.
    Features smooth animations, particle effects, and intuitive UX.
    """
    
    def __init__(self, on_action: Optional[Callable[[DeckBuilderAction], None]] = None):
        """
        Initialize enhanced deck builder.
        
        Args:
            on_action: Callback for deck builder actions
        """
        self.on_action = on_action
        
        # Legacy deck builder (for card logic) - initialize properly
        try:
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.legacy_builder = create_deck_builder(temp_surface)
        except Exception as e:
            print(f"Error initializing legacy deck builder: {e}")
            # Create a minimal fallback
            self.legacy_builder = type('DeckBuilder', (), {
                'filter_rarity': 'all',
                'current_deck': [],
                'scroll_offset': 0,
                'update': lambda self, dt: None,
                'handle_event': lambda self, event: None,
                '_update_card_positions': lambda self: None
            })()
        
        # Enhanced UI state
        self.animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Create enhanced UI elements
        self.buttons = self._create_buttons()
        self.filter_buttons = self._create_filter_buttons()
        
        # Enhanced visual effects
        self.sand_particles = []
        self.card_hover_effects = {}
        self.selection_glow = 0.0
        
        # Background with Egyptian theming
        self.background_surface = self._create_enhanced_background()
        
        # Initialize sand particles
        self._spawn_initial_particles()
        
        # Card grid layout (enhanced)
        self.cards_per_row = 6 if Layout.IS_ULTRAWIDE else 4
        self.card_scale = 0.8 if Layout.IS_ULTRAWIDE else 1.0
        
        # Search and filter state
        self.search_text = ""
        self.selected_filter = "all"
        
        print("🏗️ Enhanced Deck Builder initialized with Hades-level polish")
    
    def _create_enhanced_background(self) -> pygame.Surface:
        """Create enhanced background with Egyptian atmosphere."""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create gradient similar to other screens but more papyrus-like
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            
            # Egyptian papyrus gradient
            r = int(Colors.PAPYRUS[0] * (0.3 + ratio * 0.4))
            g = int(Colors.PAPYRUS[1] * (0.3 + ratio * 0.4))
            b = int(Colors.PAPYRUS[2] * (0.3 + ratio * 0.3))
            
            color = (max(20, min(255, r)), max(20, min(255, g)), max(20, min(255, b)))
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        return background
    
    def _spawn_initial_particles(self):
        """Spawn initial sand particles for atmosphere."""
        for _ in range(12):
            x = Layout.UI_SAFE_LEFT + (Layout.UI_SAFE_WIDTH * (0.1 + 0.8 * (len(self.sand_particles) / 12)))
            y = SCREEN_HEIGHT * (0.2 + 0.6 * (len(self.sand_particles) / 12))
            
            self.sand_particles.append({
                'x': x,
                'y': y,
                'size': 1 + (len(self.sand_particles) % 3),
                'speed': 15 + (len(self.sand_particles) % 15),
                'phase': len(self.sand_particles) * 0.7
            })
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create enhanced control buttons."""
        buttons = []
        
        button_configs = [
            ("BACK TO MENU", DeckBuilderAction.BACK_TO_MENU),
            ("SAVE DECK", DeckBuilderAction.SAVE_DECK),
            ("CLEAR ALL", DeckBuilderAction.CLEAR_DECK),
            ("EXPORT", DeckBuilderAction.EXPORT_DECK)
        ]
        
        button_width = 140
        button_height = 45
        button_spacing = 15
        
        # Position buttons in top-right corner
        start_x = SCREEN_WIDTH - (len(button_configs) * (button_width + button_spacing))
        y = 20
        
        for i, (text, action) in enumerate(button_configs):
            x = start_x + i * (button_width + button_spacing)
            
            button = AnimatedButton(
                x, y, button_width, button_height,
                text, FontSizes.BUTTON,
                action=lambda a=action: self._handle_button_action(a)
            )
            buttons.append(button)
        
        return buttons
    
    def _create_filter_buttons(self) -> List[AnimatedButton]:
        """Create enhanced filter buttons."""
        buttons = []
        
        filter_configs = [
            ("ALL CARDS", "all"),
            ("COMMON", "common"),
            ("RARE", "rare"),
            ("LEGENDARY", "legendary")
        ]
        
        button_width = 120
        button_height = 35
        button_spacing = 10
        
        # Position below title
        start_x = Layout.UI_SAFE_LEFT + 50
        y = 120
        
        for i, (text, filter_type) in enumerate(filter_configs):
            x = start_x + i * (button_width + button_spacing)
            
            button = AnimatedButton(
                x, y, button_width, button_height,
                text, FontSizes.CARD_TEXT,
                action=lambda f=filter_type: self._handle_filter_change(f)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_button_action(self, action: DeckBuilderAction):
        """Handle button actions."""
        if action == DeckBuilderAction.CLEAR_DECK:
            self.legacy_builder.current_deck.clear()
        
        if self.on_action:
            self.on_action(action)
    
    def _handle_filter_change(self, filter_type: str):
        """Handle filter changes."""
        self.selected_filter = filter_type
        self.legacy_builder.filter_rarity = filter_type
        self.legacy_builder.scroll_offset = 0
        self.legacy_builder._update_card_positions()
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """
        Update deck builder animations and handle input.
        
        Args:
            dt: Delta time in seconds
            events: Pygame events this frame
            mouse_pos: Current mouse position
            mouse_pressed: Whether mouse is pressed
        """
        self.animation_time += dt
        
        # Handle fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update sand particles
        for particle in self.sand_particles:
            particle['x'] += math.sin(self.animation_time * 0.4 + particle['phase']) * particle['speed'] * dt
            particle['y'] += math.cos(self.animation_time * 0.2 + particle['phase']) * particle['speed'] * dt * 0.3
            
            # Keep particles in safe area
            if particle['x'] < Layout.UI_SAFE_LEFT:
                particle['x'] = Layout.UI_SAFE_RIGHT
            elif particle['x'] > Layout.UI_SAFE_RIGHT:
                particle['x'] = Layout.UI_SAFE_LEFT
                
            if particle['y'] < SCREEN_HEIGHT * 0.1:
                particle['y'] = SCREEN_HEIGHT * 0.9
            elif particle['y'] > SCREEN_HEIGHT * 0.9:
                particle['y'] = SCREEN_HEIGHT * 0.1
        
        # Update selection glow
        self.selection_glow = (math.sin(self.animation_time * 3) + 1) * 0.5
        
        # Update enhanced buttons
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_pressed)
        
        for button in self.filter_buttons:
            button.update(dt, mouse_pos, mouse_pressed)
            # Highlight active filter
            if button.action and hasattr(button.action, '__call__'):
                # This is a bit hacky but works for our filter buttons
                button.is_active = (self.selected_filter in button.text.lower())
        
        # Update legacy deck builder
        self.legacy_builder.update(dt)
        
        # Handle events
        for event in events:
            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons + self.filter_buttons:
                    if button.handle_click(mouse_pos):
                        break
                else:
                    # Pass to legacy builder if no button was clicked
                    result = self.legacy_builder.handle_event(event)
                    if result and self.on_action:
                        if result == 'back':
                            self.on_action(DeckBuilderAction.BACK_TO_MENU)
            else:
                # Pass other events to legacy builder
                result = self.legacy_builder.handle_event(event)
                if result and self.on_action:
                    if result == 'back':
                        self.on_action(DeckBuilderAction.BACK_TO_MENU)
    
    def render(self, surface: pygame.Surface):
        """
        Render the enhanced deck builder with all effects.
        
        Args:
            surface: Surface to render to
        """
        # Clear surface with enhanced background
        surface.blit(self.background_surface, (0, 0))
        
        # Draw ultrawide side bars with Egyptian patterns
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Render sand particles
        self._render_sand_particles(surface)
        
        # Render main title with enhanced styling
        self._render_enhanced_title(surface)
        
        # Render deck statistics
        self._render_deck_stats(surface)
        
        # Use legacy deck builder for card rendering (for now)
        self.legacy_builder.draw()
        
        # Copy the legacy render but with enhancements
        self._render_enhanced_cards(surface)
        
        # Render enhanced UI elements
        for button in self.filter_buttons:
            # Highlight active filter
            if self.selected_filter in button.text.lower():
                glow_rect = button.rect.inflate(8, 8)
                glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                alpha = int(100 + 50 * self.selection_glow)
                glow_surface.fill((*Colors.GOLD, alpha))
                surface.blit(glow_surface, glow_rect.topleft)
            
            button.render(surface)
        
        for button in self.buttons:
            button.render(surface)
        
        # Render helpful hints
        self._render_enhanced_hints(surface)
        
        # Apply fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render Egyptian-themed side bars for ultrawide displays."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # Fill with papyrus-like pattern
        pattern_color = (35, 30, 25)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Add animated hieroglyphic border
        border_alpha = int(120 + 60 * abs(math.sin(self.animation_time * 1.5)))
        pattern_surface = pygame.Surface((8, SCREEN_HEIGHT))
        pattern_surface.set_alpha(border_alpha)
        pattern_surface.fill(Colors.GOLD)
        
        surface.blit(pattern_surface, (Layout.CONTENT_X_OFFSET - 8, 0))
        surface.blit(pattern_surface, (Layout.UI_SAFE_RIGHT, 0))
    
    def _render_sand_particles(self, surface: pygame.Surface):
        """Render floating sand particles for atmosphere."""
        for particle in self.sand_particles:
            alpha = int(120 + 80 * abs(math.sin(self.animation_time * 1.2 + particle['phase'])))
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.fill((*Colors.DESERT_SAND, alpha))
            
            pygame.draw.circle(particle_surface, Colors.DESERT_SAND, 
                             (particle['size'], particle['size']), particle['size'])
            particle_surface.set_alpha(alpha)
            
            surface.blit(particle_surface, 
                        (int(particle['x'] - particle['size']), 
                         int(particle['y'] - particle['size'])))
    
    def _render_enhanced_title(self, surface: pygame.Surface):
        """Render enhanced title with glow effects."""
        font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        
        title_text = "SACRED DECK BUILDER"
        
        # Glow effect
        glow_surface = font.render(title_text, True, Colors.DESERT_SAND)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0], 60))
        glow_surface.set_alpha(150)
        surface.blit(glow_surface, glow_rect)
        
        # Main title
        title_surface = font.render(title_text, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], 58))
        surface.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, FontSizes.BODY)
        subtitle_text = "Forge your divine arsenal"
        subtitle_surface = subtitle_font.render(subtitle_text, True, Colors.PAPYRUS)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_CENTER[0], 90))
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _render_deck_stats(self, surface: pygame.Surface):
        """Render deck statistics with Egyptian styling."""
        deck_count = len(self.legacy_builder.current_deck)
        max_count = self.legacy_builder.max_deck_size
        
        # Deck count with progress bar
        font = pygame.font.Font(None, FontSizes.BUTTON)
        stats_text = f"DECK: {deck_count}/{max_count} CARDS"
        
        # Position in bottom right
        stats_surface = font.render(stats_text, True, Colors.GOLD)
        stats_rect = stats_surface.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))
        surface.blit(stats_surface, stats_rect)
        
        # Progress bar
        bar_width = 200
        bar_height = 8
        bar_x = SCREEN_WIDTH - 300
        bar_y = SCREEN_HEIGHT - 30
        
        # Background
        bar_bg = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, Colors.DARK_BLUE, bar_bg)
        pygame.draw.rect(surface, Colors.GOLD, bar_bg, 2)
        
        # Progress fill
        if deck_count > 0:
            progress = deck_count / max_count
            fill_width = int(bar_width * progress)
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            
            # Color based on deck completion
            if progress < 0.5:
                fill_color = Colors.DESERT_SAND
            elif progress < 0.8:
                fill_color = Colors.GOLD
            else:
                fill_color = Colors.LAPIS_LAZULI
                
            pygame.draw.rect(surface, fill_color, fill_rect)
    
    def _render_enhanced_cards(self, surface: pygame.Surface):
        """Render cards with enhanced effects (placeholder for now)."""
        # For now, we'll use the legacy builder's rendering
        # This is where we'd add enhanced card hover effects, better animations, etc.
        pass
    
    def _render_enhanced_hints(self, surface: pygame.Surface):
        """Render helpful hints with better styling."""
        hints = [
            "Click cards to add them to your deck",
            "Mouse wheel to scroll • ESC to return to menu",
            "Build a balanced deck with 30 cards total"
        ]
        
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        hint_y = SCREEN_HEIGHT - 120
        
        for hint in hints:
            hint_surface = font.render(hint, True, Colors.DESERT_SAND)
            hint_rect = hint_surface.get_rect(center=(SCREEN_CENTER[0], hint_y))
            
            # Subtle background
            bg_rect = hint_rect.inflate(20, 8)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 100))
            surface.blit(bg_surface, bg_rect.topleft)
            
            surface.blit(hint_surface, hint_rect)
            hint_y += 25
    
    def reset_animations(self):
        """Reset all animations for clean entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.animation_time = 0.0
        
        # Reset button states
        for button in self.buttons + self.filter_buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0