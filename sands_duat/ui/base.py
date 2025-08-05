"""
Base UI Components

Foundation classes for the Sands of Duat UI system, providing
common functionality for screens, components, and event handling.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from enum import Enum
import logging
from .animation_system import AnimationManager, UITransitionEffect


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
        
        # Animation properties
        self.animation_id = f"{self.__class__.__name__}_{id(self)}"
        self.alpha = 255
        self.scale = 1.0
        self.rotation = 0.0
        
        # Event handlers - support both UIEvent enums and custom string events
        self.event_handlers: Dict[Union[UIEvent, str], List[Callable]] = {}
        
        # Style properties
        self.background_color = (40, 30, 20)  # Dark brown
        self.border_color = (139, 117, 93)    # Bronze
        self.text_color = (255, 248, 220)     # Cornsilk
        self.border_width = 2
        
        # Egyptian interactive feedback properties
        self.egyptian_feedback = {
            'hover_glow': False,
            'glow_intensity': 0.0,
            'glow_color': (255, 215, 0),  # Egyptian gold
            'mystical_particles': False,
            'papyrus_highlight': False,
            'hieroglyph_animation': False,
            'bronze_shimmer': False,
            'feedback_enabled': True
        }
        
        # Feedback animation timers
        self._hover_animation_time = 0.0
        self._click_animation_time = 0.0
        self._focus_animation_time = 0.0
        
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
                # Trigger click feedback animation
                self.trigger_click_feedback()
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
    
    def add_event_handler(self, event_type: Union[UIEvent, str], handler: Callable) -> None:
        """Add an event handler for a specific event type (UIEvent enum or custom string)."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def remove_event_handler(self, event_type: Union[UIEvent, str], handler: Callable) -> None:
        """Remove an event handler."""
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
    
    def _trigger_event(self, event_type: Union[UIEvent, str], event_data: Dict[str, Any]) -> None:
        """Trigger all handlers for an event type (UIEvent enum or custom string)."""
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
    
    def update_egyptian_feedback(self, delta_time: float) -> None:
        """Update Egyptian interactive feedback animations."""
        if not self.egyptian_feedback['feedback_enabled']:
            return
        
        # Update hover glow animation
        if self.hovered and self.egyptian_feedback['hover_glow']:
            self._hover_animation_time += delta_time
            # Pulsing glow effect using sine wave
            import math
            pulse = 0.6 + 0.4 * math.sin(self._hover_animation_time * 4)
            self.egyptian_feedback['glow_intensity'] = min(1.0, pulse)
        else:
            # Fade out glow when not hovered
            self.egyptian_feedback['glow_intensity'] = max(0.0, 
                self.egyptian_feedback['glow_intensity'] - delta_time * 3)
            if self.egyptian_feedback['glow_intensity'] <= 0:
                self._hover_animation_time = 0.0
        
        # Update click animation
        if self._click_animation_time > 0:
            self._click_animation_time -= delta_time
            if self._click_animation_time <= 0:
                self.egyptian_feedback['bronze_shimmer'] = False
        
        # Update focus animation
        if self.focused:
            self._focus_animation_time += delta_time
        else:
            self._focus_animation_time = max(0.0, self._focus_animation_time - delta_time * 2)
    
    def render_egyptian_feedback(self, surface: pygame.Surface) -> None:
        """Render Egyptian-themed interactive feedback effects."""
        if not self.egyptian_feedback['feedback_enabled'] or not self.visible:
            return
        
        # Golden hover glow effect
        if self.egyptian_feedback['glow_intensity'] > 0:
            self._render_mystical_glow(surface)
        
        # Papyrus highlight for focused state
        if self.focused and self.egyptian_feedback['papyrus_highlight']:
            self._render_papyrus_highlight(surface)
        
        # Bronze shimmer for click feedback
        if self.egyptian_feedback['bronze_shimmer']:
            self._render_bronze_shimmer(surface)
        
        # Mystical particles for special interactions
        if self.egyptian_feedback['mystical_particles']:
            self._render_mystical_particles(surface)
    
    def _render_mystical_glow(self, surface: pygame.Surface) -> None:
        """Render golden mystical glow around component."""
        if self.egyptian_feedback['glow_intensity'] <= 0:
            return
        
        # Create glow surface with alpha
        glow_color = self.egyptian_feedback['glow_color']
        alpha = int(80 * self.egyptian_feedback['glow_intensity'])
        
        # Create layered glow effect
        for layer in range(3):
            layer_alpha = max(0, alpha - layer * 20)
            if layer_alpha <= 0:
                continue
            
            glow_size = (self.rect.width + (layer + 1) * 8, 
                        self.rect.height + (layer + 1) * 8)
            glow_surface = pygame.Surface(glow_size, pygame.SRCALPHA)
            glow_surface.fill((*glow_color, layer_alpha))
            
            glow_x = self.rect.x - (layer + 1) * 4
            glow_y = self.rect.y - (layer + 1) * 4
            surface.blit(glow_surface, (glow_x, glow_y))
    
    def _render_papyrus_highlight(self, surface: pygame.Surface) -> None:
        """Render papyrus-style highlight for focused elements."""
        import math
        
        # Animated papyrus border effect
        pulse = 0.8 + 0.2 * math.sin(self._focus_animation_time * 3)
        border_color = (255, 248, 220, int(150 * pulse))  # Papyrus color with alpha
        
        # Create border surface
        border_surface = pygame.Surface((self.rect.width + 6, self.rect.height + 6), pygame.SRCALPHA)
        border_rect = pygame.Rect(3, 3, self.rect.width, self.rect.height)
        pygame.draw.rect(border_surface, border_color, border_rect, 3)
        
        surface.blit(border_surface, (self.rect.x - 3, self.rect.y - 3))
    
    def _render_bronze_shimmer(self, surface: pygame.Surface) -> None:
        """Render bronze shimmer effect for click feedback."""
        # Animated bronze shimmer across the component
        shimmer_progress = 1.0 - (self._click_animation_time / 0.3)  # 0.3s animation
        
        if shimmer_progress >= 1.0:
            return
        
        # Create diagonal shimmer effect
        shimmer_width = self.rect.width // 3
        shimmer_x = int((self.rect.width + shimmer_width) * shimmer_progress - shimmer_width)
        
        if 0 <= shimmer_x <= self.rect.width:
            shimmer_surface = pygame.Surface((shimmer_width, self.rect.height), pygame.SRCALPHA)
            shimmer_surface.fill((139, 117, 93, 100))  # Bronze with alpha
            surface.blit(shimmer_surface, (self.rect.x + shimmer_x, self.rect.y))
    
    def _render_mystical_particles(self, surface: pygame.Surface) -> None:
        """Render mystical particle effects for special interactions."""
        import math
        import random
        
        # Simple particle system for mystical effects
        particle_count = 5
        for i in range(particle_count):
            # Calculate particle position based on time and index
            angle = (self._hover_animation_time * 2 + i * (math.pi * 2 / particle_count)) % (math.pi * 2)
            radius = 20 + 10 * math.sin(self._hover_animation_time * 3 + i)
            
            particle_x = self.rect.centerx + int(radius * math.cos(angle))
            particle_y = self.rect.centery + int(radius * math.sin(angle))
            
            # Particle alpha based on position in orbit
            alpha = int(100 * (0.5 + 0.5 * math.sin(angle)))
            if alpha > 0:
                pygame.draw.circle(surface, (255, 215, 0, alpha), (particle_x, particle_y), 2)
    
    def enable_egyptian_feedback(self, effect_type: str = 'all') -> None:
        """Enable specific Egyptian feedback effects."""
        if effect_type == 'all':
            self.egyptian_feedback.update({
                'hover_glow': True,
                'papyrus_highlight': True,
                'bronze_shimmer': True,
                'feedback_enabled': True
            })
        elif effect_type in self.egyptian_feedback:
            self.egyptian_feedback[effect_type] = True
    
    def disable_egyptian_feedback(self, effect_type: str = 'all') -> None:
        """Disable specific Egyptian feedback effects."""
        if effect_type == 'all':
            self.egyptian_feedback.update({
                'hover_glow': False,
                'papyrus_highlight': False,
                'bronze_shimmer': False,
                'mystical_particles': False,
                'feedback_enabled': False
            })
        elif effect_type in self.egyptian_feedback:
            self.egyptian_feedback[effect_type] = False
    
    def trigger_click_feedback(self) -> None:
        """Trigger click feedback animation."""
        if self.egyptian_feedback['feedback_enabled']:
            self.egyptian_feedback['bronze_shimmer'] = True
            self._click_animation_time = 0.3  # 300ms shimmer animation


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
        
        # Animation system
        self.animation_manager = AnimationManager()
        self.screen_alpha = 255
        self.transition_offset_x = 0
        self.transition_offset_y = 0
        
        # Background system
        self.background_surface = None
        self.use_ai_background = True
    
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
        
        # Update animations
        animation_values = self.animation_manager.update(delta_time)
        self._apply_animation_values(animation_values)
        
        for component in self.components:
            if component.visible:
                component.update(delta_time)
                # Update Egyptian feedback animations
                component.update_egyptian_feedback(delta_time)
    
    def load_background(self, screen_size: Tuple[int, int] = None) -> None:
        """Load AI background for this screen"""
        if not self.use_ai_background:
            return
            
        try:
            from ..graphics.background_loader import load_background
            self.background_surface = load_background(self.name, screen_size)
            if self.background_surface:
                self.logger.info(f"Loaded AI background for {self.name}")
            else:
                self.logger.warning(f"No AI background available for {self.name}")
        except Exception as e:
            self.logger.error(f"Failed to load background for {self.name}: {e}")
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the screen and all its components with animation support."""
        if not self.active:
            return
        
        # Draw AI background if available
        if self.background_surface:
            # Scale background to fit screen if needed
            if self.background_surface.get_size() != surface.get_size():
                scaled_bg = pygame.transform.smoothscale(
                    self.background_surface, 
                    surface.get_size()
                )
                surface.blit(scaled_bg, (0, 0))
            else:
                surface.blit(self.background_surface, (0, 0))
        else:
            # Fallback to solid color background
            surface.fill(self.background_color)
        
        # Create render surface for alpha blending
        if self.screen_alpha < 255 or self.transition_offset_x != 0 or self.transition_offset_y != 0:
            screen_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            
            # Draw AI background on render surface too if available
            if self.background_surface:
                if self.background_surface.get_size() != screen_surface.get_size():
                    scaled_bg = pygame.transform.smoothscale(
                        self.background_surface, 
                        screen_surface.get_size()
                    )
                    screen_surface.blit(scaled_bg, (0, 0))
                else:
                    screen_surface.blit(self.background_surface, (0, 0))
            else:
                screen_surface.fill(self.background_color)
            
            # Render components to screen surface
            for component in self.components:
                if component.visible:
                    # Render Egyptian feedback effects first (background layer)
                    component.render_egyptian_feedback(screen_surface)
                    # Then render the component itself
                    component.render(screen_surface)
            
            # Apply alpha and position offset
            if self.screen_alpha < 255:
                screen_surface.set_alpha(self.screen_alpha)
            
            # Blit with offset
            surface.blit(screen_surface, (self.transition_offset_x, self.transition_offset_y))
        else:
            # Normal rendering
            surface.fill(self.background_color)
            
            for component in self.components:
                if component.visible:
                    # Render Egyptian feedback effects first (background layer)
                    component.render_egyptian_feedback(surface)
                    # Then render the component itself
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
    
    def _apply_animation_values(self, animation_values: Dict[str, Dict]) -> None:
        """Apply animation values to screen and components."""
        from .animation_system import AnimationType
        
        # Apply screen-level animations
        screen_id = f"screen_{self.name}"
        if screen_id in animation_values:
            values = animation_values[screen_id]
            if AnimationType.FADE in values:
                self.screen_alpha = int(values[AnimationType.FADE] * 255)
            if AnimationType.POSITION in values:
                pos = values[AnimationType.POSITION]
                self.transition_offset_x = int(pos[0])
                self.transition_offset_y = int(pos[1])
        
        # Apply component animations
        for component in self.components:
            if component.animation_id in animation_values:
                values = animation_values[component.animation_id]
                if AnimationType.FADE in values:
                    component.alpha = int(values[AnimationType.FADE] * 255)
                if AnimationType.SCALE in values:
                    component.scale = values[AnimationType.SCALE]
                if AnimationType.POSITION in values:
                    pos = values[AnimationType.POSITION]
                    component.rect.x = int(pos[0])
                    component.rect.y = int(pos[1])
    
    def fade_in(self, duration: float = 0.5) -> None:
        """Fade in the entire screen."""
        screen_id = f"screen_{self.name}"
        self.animation_manager.fade_in(screen_id, duration)
    
    def fade_out(self, duration: float = 0.5) -> None:
        """Fade out the entire screen."""
        screen_id = f"screen_{self.name}"
        self.animation_manager.fade_out(screen_id, duration)
    
    def slide_in_from_right(self, duration: float = 0.8) -> None:
        """Slide screen in from the right."""
        screen_id = f"screen_{self.name}"
        screen_width = 3440  # Default ultrawide width
        self.animation_manager.slide_in(screen_id, (screen_width, 0), (0, 0), duration)
    
    def slide_out_to_left(self, duration: float = 0.5) -> None:
        """Slide screen out to the left."""
        screen_id = f"screen_{self.name}"
        screen_width = 3440  # Default ultrawide width
        self.animation_manager.slide_out(screen_id, (0, 0), (-screen_width, 0), duration)


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
        self.transition_effect = UITransitionEffect(surface.get_size())
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
    
    def switch_to_screen(self, screen_name: str, transition_type: str = "fade", 
                        transition_duration: float = 0.5) -> bool:
        """Switch to a different screen with animated transition."""
        if screen_name not in self.screens:
            self.logger.error(f"Screen not found: {screen_name}")
            return False
        
        if self.transition_in_progress:
            self.logger.warning("Screen transition already in progress")
            return False
        
        new_screen = self.screens[screen_name]
        
        # Start transition effect
        self.transition_in_progress = True
        self.transition_effect.start_transition(
            transition_type, 
            transition_duration,
            lambda: self._complete_screen_transition(new_screen)
        )
        
        self.logger.info(f"Starting transition to screen: {screen_name}")
        return True
    
    def _complete_screen_transition(self, new_screen: UIScreen) -> None:
        """Complete the screen transition."""
        # Deactivate current screen
        if self.current_screen:
            self.current_screen.deactivate()
        
        # Activate new screen with entrance animation
        self.current_screen = new_screen
        self.current_screen.activate()
        self.current_screen.fade_in(0.3)  # Quick fade in after transition
        
        self.transition_in_progress = False
        self.logger.info(f"Completed transition to screen: {new_screen.name}")
    
    def get_current_screen_name(self) -> Optional[str]:
        """Get the name of the current screen."""
        return self.current_screen.name if self.current_screen else None
    
    def update(self, delta_time: float) -> None:
        """Update the current screen and transition effects."""
        if self.current_screen:
            self.current_screen.update(delta_time)
        
        # Update transition effects
        self.transition_effect.update(delta_time)
    
    def render(self) -> None:
        """Render the current screen with transition effects."""
        if self.current_screen:
            self.current_screen.render(self.surface)
        
        # Render transition overlay
        self.transition_effect.render_transition_overlay(self.surface)
    
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