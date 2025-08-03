"""
UI Manager

Manages UI screens, transitions, and rendering coordination
for the Sands of Duat game interface.

Features:
- Screen management and transitions
- Event routing to active screens
- Render coordination
- Memory management for UI resources
"""

import pygame
import logging
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod

from .base import UIScreen, UIManager as BaseUIManager
from .theme import get_theme


class UIManager(BaseUIManager):
    """
    Enhanced UI manager with animation support.
    
    Extends the base UI manager with smooth transitions and enhanced effects.
    """
    
    def __init__(self, display_surface: pygame.Surface):
        super().__init__(display_surface)
        self.previous_screen: Optional[UIScreen] = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Enhanced UI Manager initialized for {display_surface.get_size()}")
    
    def add_screen(self, screen: UIScreen) -> None:
        """Add a screen to the manager and set UI manager reference."""
        super().add_screen(screen)
        # Always set self-reference for navigation and transitions
        screen.ui_manager = self
    
    def switch_to_screen_with_transition(self, screen_name: str, 
                                       transition_type: str = "slide_left") -> bool:
        """
        Switch to a different screen with enhanced animated transition.
        
        Args:
            screen_name: Name of the screen to switch to
            transition_type: Type of transition effect
            
        Returns:
            True if switch was successful
        """
        if screen_name not in self.screens:
            self.logger.error(f"Screen '{screen_name}' not found")
            return False
        
        # Store previous screen for context-aware animations
        self.previous_screen = self.current_screen
        
        # Use enhanced transition from base class
        return super().switch_to_screen(screen_name, transition_type, 0.6)
    
    def get_context_appropriate_transition(self, from_screen: str, to_screen: str) -> str:
        """Get appropriate transition based on screen context."""
        transitions = {
            ("menu", "combat"): "slide_left",
            ("combat", "menu"): "slide_right", 
            ("menu", "map"): "slide_up",
            ("map", "menu"): "slide_down",
            ("menu", "deck_builder"): "fade",
            ("deck_builder", "menu"): "fade"
        }
        
        return transitions.get((from_screen, to_screen), "fade")


# Screen factory functions for delayed imports
def get_menu_screen():
    """Get menu screen class (delayed import)."""
    from .menu_screen import MenuScreen
    return MenuScreen


def get_combat_screen():
    """Get combat screen class (delayed import)."""
    from .combat_screen import CombatScreen
    return CombatScreen


def get_map_screen():
    """Get map screen class (delayed import)."""
    # Placeholder - create a simple map screen
    class MapScreen(UIScreen):
        def __init__(self):
            super().__init__("map")
        
        def on_enter(self):
            self.logger.info("Entering map screen (placeholder)")
        
        def on_exit(self):
            self.logger.info("Exiting map screen (placeholder)")
        
        def render(self, surface: pygame.Surface):
            theme = get_theme()
            surface.fill(theme.colors.background)
            
            font = pygame.font.Font(None, 48)
            text = font.render("MAP SCREEN - COMING SOON", True, (255, 255, 255))
            text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
            surface.blit(text, text_rect)
    
    return MapScreen


def get_deck_builder_screen():
    """Get deck builder screen class (delayed import)."""
    from .deck_builder import DeckBuilderScreen
    return DeckBuilderScreen


def get_tutorial_screen():
    """Get tutorial screen class (delayed import)."""
    from .tutorial_screen import TutorialScreen
    return TutorialScreen


def get_progression_screen():
    """Get progression screen class (delayed import)."""
    from .progression_screen import ProgressionScreen
    return ProgressionScreen