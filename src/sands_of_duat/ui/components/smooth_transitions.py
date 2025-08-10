"""
Smooth Transition System
Professional animation system for seamless transitions between game states and UI elements.
"""

import pygame
import math
from typing import Dict, List, Callable, Optional, Tuple, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import Colors, Timing


class EasingType(Enum):
    """Easing function types for smooth animations."""
    LINEAR = "linear"
    EASE_IN_QUAD = "ease_in_quad"
    EASE_OUT_QUAD = "ease_out_quad"
    EASE_IN_OUT_QUAD = "ease_in_out_quad"
    EASE_IN_CUBIC = "ease_in_cubic"
    EASE_OUT_CUBIC = "ease_out_cubic"
    EASE_IN_OUT_CUBIC = "ease_in_out_cubic"
    EASE_OUT_BOUNCE = "ease_out_bounce"
    EASE_OUT_ELASTIC = "ease_out_elastic"


class TransitionType(Enum):
    """Types of transitions available."""
    FADE = auto()
    SLIDE_LEFT = auto()
    SLIDE_RIGHT = auto()
    SLIDE_UP = auto()
    SLIDE_DOWN = auto()
    SCALE = auto()
    ROTATE = auto()
    DISSOLVE = auto()
    SWIPE = auto()


@dataclass
class Transition:
    """Represents an active transition."""
    transition_type: TransitionType
    start_time: float
    duration: float
    easing: EasingType
    from_value: Any
    to_value: Any
    current_value: Any = None
    on_complete: Optional[Callable] = None
    is_complete: bool = False


class SmoothTransitions:
    """
    Professional transition system for smooth animations and state changes.
    """
    
    def __init__(self):
        self.active_transitions: Dict[str, Transition] = {}
        self.screen_transition: Optional[Transition] = None
        self.fade_overlay_alpha = 0
        
        # Easing functions
        self.easing_functions = {
            EasingType.LINEAR: self._linear,
            EasingType.EASE_IN_QUAD: self._ease_in_quad,
            EasingType.EASE_OUT_QUAD: self._ease_out_quad,
            EasingType.EASE_IN_OUT_QUAD: self._ease_in_out_quad,
            EasingType.EASE_IN_CUBIC: self._ease_in_cubic,
            EasingType.EASE_OUT_CUBIC: self._ease_out_cubic,
            EasingType.EASE_IN_OUT_CUBIC: self._ease_in_out_cubic,
            EasingType.EASE_OUT_BOUNCE: self._ease_out_bounce,
            EasingType.EASE_OUT_ELASTIC: self._ease_out_elastic
        }
        
        print("[TRANSITIONS] Smooth transition system initialized")
    
    def start_transition(self, name: str, transition_type: TransitionType,
                        from_value: Any, to_value: Any, duration: float,
                        easing: EasingType = EasingType.EASE_OUT_QUAD,
                        on_complete: Optional[Callable] = None) -> None:
        """
        Start a new transition.
        
        Args:
            name: Unique name for this transition
            transition_type: Type of transition
            from_value: Starting value
            to_value: Target value
            duration: Transition duration in seconds
            easing: Easing function to use
            on_complete: Callback when transition completes
        """
        current_time = pygame.time.get_ticks() / 1000.0
        
        self.active_transitions[name] = Transition(
            transition_type=transition_type,
            start_time=current_time,
            duration=duration,
            easing=easing,
            from_value=from_value,
            to_value=to_value,
            current_value=from_value,
            on_complete=on_complete
        )
        
        print(f"[TRANSITIONS] Started transition '{name}': {transition_type.name} ({duration}s)")
    
    def update_transitions(self, dt: float) -> None:
        """Update all active transitions."""
        current_time = pygame.time.get_ticks() / 1000.0
        completed_transitions = []
        
        for name, transition in self.active_transitions.items():
            if transition.is_complete:
                completed_transitions.append(name)
                continue
            
            # Calculate progress (0.0 to 1.0)
            elapsed = current_time - transition.start_time
            progress = min(1.0, elapsed / transition.duration)
            
            # Apply easing function
            eased_progress = self.easing_functions[transition.easing](progress)
            
            # Calculate current value based on transition type
            if isinstance(transition.from_value, (int, float)):
                # Numeric interpolation
                transition.current_value = self._lerp(
                    transition.from_value, transition.to_value, eased_progress
                )
            elif isinstance(transition.from_value, tuple) and len(transition.from_value) >= 2:
                # Vector/position interpolation
                transition.current_value = tuple(
                    self._lerp(a, b, eased_progress) 
                    for a, b in zip(transition.from_value, transition.to_value)
                )
            else:
                # Default to target value
                transition.current_value = transition.to_value
            
            # Check if transition is complete
            if progress >= 1.0:
                transition.is_complete = True
                transition.current_value = transition.to_value
                
                if transition.on_complete:
                    transition.on_complete()
        
        # Remove completed transitions
        for name in completed_transitions:
            del self.active_transitions[name]
    
    def get_transition_value(self, name: str) -> Any:
        """Get current value of a transition."""
        if name in self.active_transitions:
            return self.active_transitions[name].current_value
        return None
    
    def is_transition_active(self, name: str) -> bool:
        """Check if a transition is currently active."""
        return name in self.active_transitions and not self.active_transitions[name].is_complete
    
    def stop_transition(self, name: str) -> None:
        """Stop a transition immediately."""
        if name in self.active_transitions:
            del self.active_transitions[name]
    
    def start_screen_transition(self, transition_type: TransitionType = TransitionType.FADE,
                              duration: float = Timing.MENU_TRANSITION_TIME,
                              on_complete: Optional[Callable] = None) -> None:
        """Start a full-screen transition effect."""
        self.start_transition(
            "screen_transition", transition_type, 0.0, 1.0, duration,
            EasingType.EASE_IN_OUT_QUAD, on_complete
        )
    
    def render_screen_transition(self, surface: pygame.Surface) -> None:
        """Render screen transition overlay."""
        if not self.is_transition_active("screen_transition"):
            return
        
        transition_value = self.get_transition_value("screen_transition")
        if transition_value is None:
            return
        
        # Create fade overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        alpha = int(255 * transition_value)
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))
    
    def fade_in_element(self, name: str, duration: float = Timing.FADE_DURATION,
                       on_complete: Optional[Callable] = None) -> None:
        """Fade in an element from transparent to opaque."""
        self.start_transition(
            f"{name}_fade", TransitionType.FADE, 0.0, 1.0, duration,
            EasingType.EASE_OUT_QUAD, on_complete
        )
    
    def fade_out_element(self, name: str, duration: float = Timing.FADE_DURATION,
                        on_complete: Optional[Callable] = None) -> None:
        """Fade out an element from opaque to transparent."""
        self.start_transition(
            f"{name}_fade", TransitionType.FADE, 1.0, 0.0, duration,
            EasingType.EASE_IN_QUAD, on_complete
        )
    
    def slide_in_element(self, name: str, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                        duration: float = Timing.SLIDE_DURATION,
                        easing: EasingType = EasingType.EASE_OUT_CUBIC,
                        on_complete: Optional[Callable] = None) -> None:
        """Slide an element from one position to another."""
        self.start_transition(
            f"{name}_slide", TransitionType.SLIDE_LEFT, from_pos, to_pos,
            duration, easing, on_complete
        )
    
    def scale_element(self, name: str, from_scale: float, to_scale: float,
                     duration: float = Timing.BUTTON_HOVER_DURATION,
                     easing: EasingType = EasingType.EASE_OUT_ELASTIC,
                     on_complete: Optional[Callable] = None) -> None:
        """Scale an element with elastic easing."""
        self.start_transition(
            f"{name}_scale", TransitionType.SCALE, from_scale, to_scale,
            duration, easing, on_complete
        )
    
    def create_card_play_transition(self, card_name: str, from_pos: Tuple[int, int], 
                                  to_pos: Tuple[int, int]) -> None:
        """Create smooth transition for playing a card."""
        # Slide to position
        self.slide_in_element(
            f"{card_name}_play", from_pos, to_pos, 
            Timing.CARD_FLIP_DURATION, EasingType.EASE_OUT_CUBIC
        )
        
        # Scale effect during play
        self.scale_element(
            f"{card_name}_play_scale", 1.0, 1.2, 
            Timing.CARD_FLIP_DURATION / 2, EasingType.EASE_OUT_QUAD
        )
        
        # Scale back
        def scale_back():
            self.scale_element(
                f"{card_name}_play_scale", 1.2, 1.0,
                Timing.CARD_FLIP_DURATION / 2, EasingType.EASE_IN_QUAD
            )
        
        # Delay the scale back
        pygame.time.set_timer(pygame.USEREVENT + 1, int(Timing.CARD_FLIP_DURATION * 500))
    
    def create_damage_number_transition(self, damage: int, position: Tuple[int, int]) -> None:
        """Create floating damage number animation."""
        damage_name = f"damage_{pygame.time.get_ticks()}"
        
        # Float upward
        end_pos = (position[0], position[1] - 50)
        self.slide_in_element(
            damage_name, position, end_pos,
            Timing.DAMAGE_NUMBER_DURATION, EasingType.EASE_OUT_QUAD
        )
        
        # Fade out
        self.fade_out_element(
            damage_name, Timing.DAMAGE_NUMBER_DURATION
        )
    
    def render_element_with_transitions(self, surface: pygame.Surface, element_surface: pygame.Surface,
                                      base_pos: Tuple[int, int], element_name: str) -> pygame.Rect:
        """Render an element with all active transitions applied."""
        # Start with base values
        current_pos = base_pos
        current_alpha = 255
        current_scale = 1.0
        
        # Apply slide transitions
        slide_name = f"{element_name}_slide"
        if self.is_transition_active(slide_name):
            slide_pos = self.get_transition_value(slide_name)
            if slide_pos:
                current_pos = slide_pos
        
        # Apply fade transitions
        fade_name = f"{element_name}_fade"
        if self.is_transition_active(fade_name):
            fade_value = self.get_transition_value(fade_name)
            if fade_value is not None:
                current_alpha = int(255 * fade_value)
        
        # Apply scale transitions
        scale_name = f"{element_name}_scale"
        if self.is_transition_active(scale_name):
            scale_value = self.get_transition_value(scale_name)
            if scale_value is not None:
                current_scale = scale_value
        
        # Apply transformations
        final_surface = element_surface.copy()
        
        # Apply alpha
        if current_alpha < 255:
            final_surface.set_alpha(current_alpha)
        
        # Apply scaling
        if current_scale != 1.0:
            new_size = (
                int(element_surface.get_width() * current_scale),
                int(element_surface.get_height() * current_scale)
            )
            if new_size[0] > 0 and new_size[1] > 0:
                final_surface = pygame.transform.smoothscale(element_surface, new_size)
                # Adjust position for centered scaling
                scale_offset_x = (final_surface.get_width() - element_surface.get_width()) // 2
                scale_offset_y = (final_surface.get_height() - element_surface.get_height()) // 2
                current_pos = (current_pos[0] - scale_offset_x, current_pos[1] - scale_offset_y)
        
        # Blit final surface
        surface.blit(final_surface, current_pos)
        
        return pygame.Rect(current_pos[0], current_pos[1], 
                          final_surface.get_width(), final_surface.get_height())
    
    # Easing functions
    def _linear(self, t: float) -> float:
        return t
    
    def _ease_in_quad(self, t: float) -> float:
        return t * t
    
    def _ease_out_quad(self, t: float) -> float:
        return 1 - (1 - t) * (1 - t)
    
    def _ease_in_out_quad(self, t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        return 1 - 2 * (1 - t) * (1 - t)
    
    def _ease_in_cubic(self, t: float) -> float:
        return t * t * t
    
    def _ease_out_cubic(self, t: float) -> float:
        return 1 - (1 - t) ** 3
    
    def _ease_in_out_cubic(self, t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - 4 * (1 - t) ** 3
    
    def _ease_out_bounce(self, t: float) -> float:
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    def _ease_out_elastic(self, t: float) -> float:
        if t == 0 or t == 1:
            return t
        return (2 ** (-10 * t)) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """Linear interpolation between two values."""
        return a + (b - a) * t


# Global instance for easy access
smooth_transitions = SmoothTransitions()