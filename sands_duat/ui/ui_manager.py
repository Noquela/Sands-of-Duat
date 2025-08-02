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

from .base import UIScreen
from .theme import get_theme


class UIManager:
    """
    Central manager for all UI screens and interactions.
    
    Handles screen transitions, event routing, and rendering
    coordination for the entire UI system.
    """
    
    def __init__(self, display_surface: pygame.Surface):
        self.display_surface = display_surface
        self.screens: Dict[str, UIScreen] = {}
        self.current_screen: Optional[UIScreen] = None
        self.previous_screen: Optional[UIScreen] = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"UI Manager initialized for {display_surface.get_size()}")
    
    def add_screen(self, screen: UIScreen) -> None:
        """Add a screen to the manager."""
        if screen.name in self.screens:
            self.logger.warning(f"Screen '{screen.name}' already exists, replacing")
        
        self.screens[screen.name] = screen
        self.logger.debug(f"Added screen: {screen.name}")
    
    def remove_screen(self, screen_name: str) -> None:
        """Remove a screen from the manager."""
        if screen_name in self.screens:
            screen = self.screens[screen_name]
            if self.current_screen == screen:
                self.current_screen = None
            del self.screens[screen_name]
            self.logger.debug(f"Removed screen: {screen_name}")
    
    def switch_to_screen(self, screen_name: str) -> bool:
        """
        Switch to a different screen.
        
        Args:
            screen_name: Name of the screen to switch to
            
        Returns:
            True if switch was successful
        """
        if screen_name not in self.screens:
            self.logger.error(f"Screen '{screen_name}' not found")
            return False
        
        new_screen = self.screens[screen_name]
        
        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()
            self.previous_screen = self.current_screen
        
        # Enter new screen
        self.current_screen = new_screen
        self.current_screen.on_enter()
        
        self.logger.info(f"Switched to screen: {screen_name}")
        return True
    
    def get_current_screen(self) -> Optional[UIScreen]:
        """Get the currently active screen."""
        return self.current_screen
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Route events to the current screen.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            True if event was handled
        """
        if self.current_screen:
            return self.current_screen.handle_event(event)
        return False
    
    def update(self, delta_time: float) -> None:
        """Update the current screen."""
        if self.current_screen:
            self.current_screen.update(delta_time)
    
    def render(self) -> None:
        """Render the current screen."""
        # Clear the display
        theme = get_theme()
        self.display_surface.fill(theme.colors.background)
        
        # Render current screen
        if self.current_screen:
            self.current_screen.render(self.display_surface)
    
    def shutdown(self) -> None:
        """Shutdown the UI manager and cleanup resources."""
        self.logger.info("Shutting down UI Manager")
        
        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()
        
        # Clear all screens
        for screen in self.screens.values():
            screen.clear_components()
        
        self.screens.clear()
        self.current_screen = None
        self.previous_screen = None


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
    # Placeholder - create a simple deck builder screen
    class DeckBuilderScreen(UIScreen):
        def __init__(self):
            super().__init__("deck_builder")
        
        def on_enter(self):
            self.logger.info("Entering deck builder screen (placeholder)")
        
        def on_exit(self):
            self.logger.info("Exiting deck builder screen (placeholder)")
        
        def render(self, surface: pygame.Surface):
            theme = get_theme()
            surface.fill(theme.colors.background)
            
            font = pygame.font.Font(None, 48)
            text = font.render("DECK BUILDER - COMING SOON", True, (255, 255, 255))
            text_rect = text.get_rect(center=(surface.get_width()//2, surface.get_height()//2))
            surface.blit(text, text_rect)
    
    return DeckBuilderScreen