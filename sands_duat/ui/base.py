"""
Base UI Components

Foundation classes for the Sands of Duat UI system, providing
common functionality for screens, components, and event handling.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import logging


class UIEvent(Enum):
    """UI event types."""
    CLICK = "click"
    HOVER_START = "hover_start"
    HOVER_END = "hover_end"
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"
    FOCUS_GAINED = "focus_gained"
    FOCUS_LOST = "focus_lost"


class UIComponent(ABC):
    """
    Base class for all UI components.
    
    Provides common functionality for positioning, rendering,
    and event handling for UI elements.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        self.focused = False
        self.hovered = False
        
        # Event handlers
        self.event_handlers: Dict[UIEvent, List[Callable]] = {}
        
        # Style properties
        self.background_color = (40, 30, 20)  # Dark brown
        self.border_color = (139, 117, 93)    # Bronze
        self.text_color = (255, 248, 220)     # Cornsilk
        self.border_width = 2
        
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update component logic."""
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the component."""
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events.
        
        Returns True if the event was consumed.
        """
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self._trigger_event(UIEvent.CLICK, {"button": event.button, "pos": event.pos})
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            # Handle hover
            mouse_over = self.rect.collidepoint(event.pos)
            if mouse_over and not self.hovered:
                self.hovered = True
                self._trigger_event(UIEvent.HOVER_START, {"pos": event.pos})
            elif not mouse_over and self.hovered:
                self.hovered = False
                self._trigger_event(UIEvent.HOVER_END, {"pos": event.pos})
        
        elif event.type == pygame.KEYDOWN:
            if self.focused:
                self._trigger_event(UIEvent.KEY_DOWN, {"key": event.key, "unicode": event.unicode})
                return True
        
        elif event.type == pygame.KEYUP:
            if self.focused:
                self._trigger_event(UIEvent.KEY_UP, {"key": event.key})
                return True
        
        return False
    
    def add_event_handler(self, event_type: UIEvent, handler: Callable) -> None:
        """Add an event handler for a specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def remove_event_handler(self, event_type: UIEvent, handler: Callable) -> None:
        """Remove an event handler."""
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
    
    def _trigger_event(self, event_type: UIEvent, event_data: Dict[str, Any]) -> None:
        """Trigger all handlers for an event type."""
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(self, event_data)
            except Exception as e:
                self.logger.error(f"Error in event handler: {e}")
    
    def set_position(self, x: int, y: int) -> None:
        """Set the component position."""
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width: int, height: int) -> None:
        """Set the component size."""
        self.rect.width = width
        self.rect.height = height
    
    def show(self) -> None:
        """Show the component."""
        self.visible = True
    
    def hide(self) -> None:
        """Hide the component."""
        self.visible = False
    
    def enable(self) -> None:
        """Enable the component."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable the component."""
        self.enabled = False
    
    def focus(self) -> None:
        """Give focus to this component."""
        self.focused = True
        self._trigger_event(UIEvent.FOCUS_GAINED, {})
    
    def unfocus(self) -> None:
        """Remove focus from this component."""
        self.focused = False
        self._trigger_event(UIEvent.FOCUS_LOST, {})
    
    def contains_point(self, point: Tuple[int, int]) -> bool:
        """Check if a point is within this component."""
        return self.rect.collidepoint(point)


class UIScreen(ABC):
    """
    Base class for game screens.
    
    Manages collections of UI components and provides
    screen-level functionality like transitions and state management.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.components: List[UIComponent] = []
        self.active = False
        self.background_color = (15, 10, 5)  # Very dark brown
        self.logger = logging.getLogger(f"Screen.{name}")
    
    @abstractmethod
    def on_enter(self) -> None:
        """Called when the screen becomes active."""
        pass
    
    @abstractmethod
    def on_exit(self) -> None:
        """Called when the screen becomes inactive.""" 
        pass
    
    def update(self, delta_time: float) -> None:
        """Update all components on the screen."""
        if not self.active:
            return
        
        for component in self.components:
            if component.visible:
                component.update(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the screen and all its components."""
        if not self.active:
            return
        
        # Clear screen with background
        surface.fill(self.background_color)
        
        # Render all visible components
        for component in self.components:
            if component.visible:
                component.render(surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events for all components on the screen.
        
        Returns True if any component consumed the event.
        """
        if not self.active:
            return False
        
        # Handle events in reverse order (top-most components first)
        for component in reversed(self.components):
            if component.handle_event(event):
                return True
        
        return False
    
    def add_component(self, component: UIComponent) -> None:
        """Add a component to the screen."""
        self.components.append(component)
    
    def remove_component(self, component: UIComponent) -> None:
        """Remove a component from the screen."""
        if component in self.components:
            self.components.remove(component)
    
    def clear_components(self) -> None:
        """Remove all components from the screen."""
        self.components.clear()
    
    def get_component_at(self, point: Tuple[int, int]) -> Optional[UIComponent]:
        """Get the top-most component at a given point."""
        for component in reversed(self.components):
            if component.visible and component.contains_point(point):
                return component
        return None
    
    def activate(self) -> None:
        """Activate this screen."""
        self.active = True
        self.on_enter()
    
    def deactivate(self) -> None:
        """Deactivate this screen."""
        self.active = False
        self.on_exit()


class UIManager:
    """
    Manages multiple UI screens and handles screen transitions.
    
    Provides a centralized system for switching between different
    game screens and managing the overall UI state.
    """
    
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.screens: Dict[str, UIScreen] = {}
        self.current_screen: Optional[UIScreen] = None
        self.transition_in_progress = False
        self.logger = logging.getLogger(__name__)
    
    def add_screen(self, screen: UIScreen) -> None:
        """Add a screen to the manager."""
        self.screens[screen.name] = screen
        self.logger.info(f"Added screen: {screen.name}")
    
    def remove_screen(self, screen_name: str) -> None:
        """Remove a screen from the manager."""
        if screen_name in self.screens:
            if self.current_screen and self.current_screen.name == screen_name:
                self.current_screen.deactivate()
                self.current_screen = None
            del self.screens[screen_name]
            self.logger.info(f"Removed screen: {screen_name}")
    
    def switch_to_screen(self, screen_name: str) -> bool:
        """Switch to a different screen."""
        if screen_name not in self.screens:
            self.logger.error(f"Screen not found: {screen_name}")
            return False
        
        if self.transition_in_progress:
            self.logger.warning("Screen transition already in progress")
            return False
        
        self.transition_in_progress = True
        
        # Deactivate current screen
        if self.current_screen:
            self.current_screen.deactivate()
        
        # Activate new screen
        self.current_screen = self.screens[screen_name]
        self.current_screen.activate()
        
        self.transition_in_progress = False
        self.logger.info(f"Switched to screen: {screen_name}")
        return True
    
    def get_current_screen_name(self) -> Optional[str]:
        """Get the name of the current screen."""
        return self.current_screen.name if self.current_screen else None
    
    def update(self, delta_time: float) -> None:
        """Update the current screen."""
        if self.current_screen:
            self.current_screen.update(delta_time)
    
    def render(self) -> None:
        """Render the current screen."""
        if self.current_screen:
            self.current_screen.render(self.surface)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for the current screen."""
        if self.current_screen:
            return self.current_screen.handle_event(event)
        return False
    
    def shutdown(self) -> None:
        """Clean shutdown of the UI manager."""
        if self.current_screen:
            self.current_screen.deactivate()
        self.screens.clear()
        self.current_screen = None