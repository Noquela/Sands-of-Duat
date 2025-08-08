"""
Transition Screen - Handles smooth transitions between major game states.
Provides context-aware loading with Egyptian theming.
"""

import pygame
import math
import time
from typing import Dict, Any, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes, Timing
)
from ...core.state_manager import GameState
from .loading_screen import LoadingScreen, LoadingType

class TransitionType(Enum):
    """Types of transition screens."""
    ENTERING_COMBAT = auto()
    LEAVING_COMBAT = auto()
    DECK_BUILDING = auto()
    COLLECTING_CARDS = auto()
    SETTINGS_MENU = auto()
    RETURNING_HOME = auto()

class TransitionScreen:
    """
    Context-aware transition screen that provides smooth flow between game states.
    Features Egyptian theming, atmospheric effects, and meaningful loading messages.
    """
    
    def __init__(self, transition_type: TransitionType,
                 from_state: GameState, to_state: GameState,
                 completion_callback: Optional[Callable] = None,
                 context_data: Dict[str, Any] = None):
        """
        Initialize transition screen.
        
        Args:
            transition_type: Type of transition
            from_state: State transitioning from
            to_state: State transitioning to
            completion_callback: Called when transition completes
            context_data: Additional context for the transition
        """
        self.transition_type = transition_type
        self.from_state = from_state
        self.to_state = to_state
        self.completion_callback = completion_callback
        self.context_data = context_data or {}
        
        # Transition timing
        self.start_time = time.time()
        self.min_duration = 1.5  # Minimum time to show transition
        self.current_phase = 0  # 0=fade_out, 1=loading, 2=fade_in
        self.phase_progress = 0.0
        
        # Animation state
        self.animation_time = 0.0
        self.fade_alpha = 0
        
        # Loading system
        loading_type = self._get_loading_type()
        self.loading_screen = LoadingScreen(loading_type, self._on_loading_complete)
        
        # Visual elements
        self.egyptian_symbols = self._create_symbols()
        self.is_complete = False
        
        # Context-specific content
        self.transition_title = self._get_transition_title()
        self.transition_subtitle = self._get_transition_subtitle()
        
    def _get_loading_type(self) -> LoadingType:
        """Map transition type to loading type."""
        mapping = {
            TransitionType.ENTERING_COMBAT: LoadingType.ENTERING_COMBAT,
            TransitionType.LEAVING_COMBAT: LoadingType.GENERAL,
            TransitionType.DECK_BUILDING: LoadingType.BUILDING_DECK,
            TransitionType.COLLECTING_CARDS: LoadingType.GENERAL,
            TransitionType.SETTINGS_MENU: LoadingType.GENERAL,
            TransitionType.RETURNING_HOME: LoadingType.GENERAL
        }
        return mapping.get(self.transition_type, LoadingType.GENERAL)
    
    def _get_transition_title(self) -> str:
        """Get contextual title for the transition."""
        titles = {
            TransitionType.ENTERING_COMBAT: "ENTERING THE BATTLEFIELD",
            TransitionType.LEAVING_COMBAT: "RETURNING TO TEMPLE",
            TransitionType.DECK_BUILDING: "OPENING THE SACRED LIBRARY", 
            TransitionType.COLLECTING_CARDS: "HALL OF DIVINE ARTIFACTS",
            TransitionType.SETTINGS_MENU: "TEMPLE SANCTUM",
            TransitionType.RETURNING_HOME: "RETURNING TO THE MAIN HALL"
        }
        return titles.get(self.transition_type, "TRANSITIONING")
    
    def _get_transition_subtitle(self) -> str:
        """Get contextual subtitle for the transition."""
        subtitles = {
            TransitionType.ENTERING_COMBAT: "Where legends are forged",
            TransitionType.LEAVING_COMBAT: "Your deeds echo in eternity",
            TransitionType.DECK_BUILDING: "Craft your divine arsenal",
            TransitionType.COLLECTING_CARDS: "Behold your growing power",
            TransitionType.SETTINGS_MENU: "Commune with the gods",
            TransitionType.RETURNING_HOME: "The pharaoh's throne awaits"
        }
        return subtitles.get(self.transition_type, "The journey continues")
    
    def _create_symbols(self) -> list:
        """Create floating Egyptian symbols for atmosphere."""
        symbols = []
        symbol_chars = ["☥", "𓂀", "𓁹", "𓅃", "𓊽"]  # Ankh, Scarab, Eye, Bird, Djed
        
        for i in range(6):
            symbols.append({
                'char': symbol_chars[i % len(symbol_chars)],
                'x': Layout.UI_SAFE_LEFT + (i * Layout.UI_SAFE_WIDTH / 6),
                'y': SCREEN_HEIGHT * (0.2 + 0.6 * (i % 2)),
                'rotation': 0,
                'rotation_speed': 15 + (i * 5),
                'float_phase': i * 0.8,
                'size': FontSizes.TITLE_MEDIUM + (i % 3) * 10
            })
        
        return symbols
    
    def _on_loading_complete(self):
        """Called when loading screen completes."""
        elapsed = time.time() - self.start_time
        if elapsed >= self.min_duration:
            self.current_phase = 2  # Move to fade-in
        # Otherwise, wait for minimum duration
    
    def update(self, dt: float):
        """
        Update transition animations and progress.
        
        Args:
            dt: Delta time in seconds
        """
        self.animation_time += dt
        elapsed = time.time() - self.start_time
        
        # Update Egyptian symbols
        for symbol in self.egyptian_symbols:
            symbol['rotation'] += symbol['rotation_speed'] * dt
            symbol['y'] += math.sin(self.animation_time * 0.5 + symbol['float_phase']) * 10 * dt
        
        # Handle transition phases
        if self.current_phase == 0:  # Fade out from old state
            self.phase_progress = min(1.0, elapsed / 0.5)
            self.fade_alpha = int(255 * self.phase_progress)
            
            if self.phase_progress >= 1.0:
                self.current_phase = 1  # Move to loading phase
                self.phase_progress = 0.0
        
        elif self.current_phase == 1:  # Loading phase
            self.loading_screen.update(dt)
            
            # Simulate loading progress (in real game, this would be driven by actual loading)
            progress = min(1.0, (elapsed - 0.5) / 2.0)  # 2 second loading simulation
            self.loading_screen.set_progress(progress)
            
            # Check if we can move to fade-in
            if elapsed >= self.min_duration and self.loading_screen.is_complete:
                self.current_phase = 2
                self.phase_progress = 0.0
        
        elif self.current_phase == 2:  # Fade in to new state
            self.phase_progress = min(1.0, (elapsed - self.min_duration - 0.5) / 0.5)
            self.fade_alpha = int(255 * (1.0 - self.phase_progress))
            
            if self.phase_progress >= 1.0 and not self.is_complete:
                self.is_complete = True
                if self.completion_callback:
                    self.completion_callback()
    
    def render(self, surface: pygame.Surface):
        """
        Render the transition screen.
        
        Args:
            surface: Surface to render to
        """
        if self.current_phase == 0:
            # Fade out phase - render black overlay
            surface.fill(Colors.BLACK)
            
            # Draw transition title
            self._render_transition_title(surface)
            
            # Apply fade effect
            if self.fade_alpha < 255:
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.set_alpha(255 - self.fade_alpha)
                fade_surface.fill(Colors.BLACK)
                surface.blit(fade_surface, (0, 0))
        
        elif self.current_phase == 1:
            # Loading phase - show loading screen
            self.loading_screen.render(surface)
            
            # Overlay context-specific elements
            self._render_context_overlay(surface)
        
        elif self.current_phase == 2:
            # Fade in phase - render new state background with fade
            surface.fill(Colors.DARK_BLUE)
            
            # Apply fade effect
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.set_alpha(self.fade_alpha)
            fade_surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
    
    def _render_transition_title(self, surface: pygame.Surface):
        """Render the main transition title with effects."""
        # Main title
        title_font = pygame.font.Font(None, FontSizes.TITLE_LARGE)
        title_surface = title_font.render(self.transition_title, True, Colors.GOLD)
        title_rect = title_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_CENTER[1] - 30))
        
        # Glow effect
        glow_surface = title_font.render(self.transition_title, True, Colors.PAPYRUS)
        glow_rect = glow_surface.get_rect(center=(SCREEN_CENTER[0] + 2, SCREEN_CENTER[1] - 28))
        glow_surface.set_alpha(120)
        
        surface.blit(glow_surface, glow_rect)
        surface.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, FontSizes.BODY)
        subtitle_surface = subtitle_font.render(self.transition_subtitle, True, Colors.DESERT_SAND)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_CENTER[1] + 10))
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _render_context_overlay(self, surface: pygame.Surface):
        """Render context-specific overlay elements."""
        # Draw floating Egyptian symbols
        for symbol in self.egyptian_symbols:
            try:
                # Create symbol surface
                font = pygame.font.Font(None, symbol['size'])
                symbol_surface = font.render(symbol['char'], True, Colors.GOLD)
                
                # Apply rotation (simplified - just alpha pulsing for now)
                alpha = int(100 + 80 * abs(math.sin(self.animation_time + symbol['float_phase'])))
                symbol_surface.set_alpha(alpha)
                
                # Position and render
                symbol_rect = symbol_surface.get_rect(center=(symbol['x'], symbol['y']))
                surface.blit(symbol_surface, symbol_rect)
                
            except (UnicodeError, pygame.error):
                # Fallback for unsupported unicode characters
                fallback_surface = font.render("☥", True, Colors.GOLD)
                fallback_surface.set_alpha(alpha)
                symbol_rect = fallback_surface.get_rect(center=(symbol['x'], symbol['y']))
                surface.blit(fallback_surface, symbol_rect)
        
        # Draw ultrawide bars if needed
        if Layout.IS_ULTRAWIDE:
            left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
            
            pattern_color = (5, 5, 30)
            pygame.draw.rect(surface, pattern_color, left_bar)
            pygame.draw.rect(surface, pattern_color, right_bar)
    
    def is_transition_complete(self) -> bool:
        """Check if transition is complete."""
        return self.is_complete
    
    def get_current_phase(self) -> int:
        """Get current transition phase (0=fade_out, 1=loading, 2=fade_in)."""
        return self.current_phase
    
    def get_phase_progress(self) -> float:
        """Get progress of current phase (0.0 to 1.0)."""
        return self.phase_progress