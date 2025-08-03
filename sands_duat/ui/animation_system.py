"""
Animation System for Sands of Duat UI

Provides smooth interpolation and transition effects for UI elements,
including fade in/out, slide transitions, scale animations, and easing functions.
"""

import pygame
import math
import time
from typing import Dict, List, Optional, Callable, Tuple, Any
from enum import Enum


class EasingType(Enum):
    """Different easing functions for animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"
    BACK = "back"


class AnimationType(Enum):
    """Types of animations supported."""
    FADE = "fade"
    SLIDE = "slide"
    SCALE = "scale"
    ROTATE = "rotate"
    COLOR = "color"
    POSITION = "position"


class Animation:
    """
    Represents a single animation with start/end values and timing.
    """
    
    def __init__(self, 
                 animation_type: AnimationType,
                 start_value: Any,
                 end_value: Any,
                 duration: float,
                 easing: EasingType = EasingType.EASE_OUT,
                 delay: float = 0.0,
                 callback: Optional[Callable] = None):
        self.type = animation_type
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing = easing
        self.delay = delay
        self.callback = callback
        
        self.start_time = time.time() + delay
        self.is_playing = False
        self.is_complete = False
        self.current_value = start_value
    
    def update(self, current_time: float) -> Any:
        """Update animation and return current interpolated value."""
        if not self.is_playing and current_time >= self.start_time:
            self.is_playing = True
        
        if not self.is_playing:
            return self.start_value
        
        if self.is_complete:
            return self.end_value
        
        # Calculate progress (0 to 1)
        elapsed = current_time - self.start_time
        progress = min(1.0, elapsed / self.duration)
        
        # Apply easing
        eased_progress = self._apply_easing(progress)
        
        # Interpolate value
        self.current_value = self._interpolate(self.start_value, self.end_value, eased_progress)
        
        # Check completion
        if progress >= 1.0:
            self.is_complete = True
            self.current_value = self.end_value
            if self.callback:
                self.callback()
        
        return self.current_value
    
    def _apply_easing(self, t: float) -> float:
        """Apply easing function to progress value."""
        if self.easing == EasingType.LINEAR:
            return t
        elif self.easing == EasingType.EASE_IN:
            return t * t
        elif self.easing == EasingType.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif self.easing == EasingType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - pow(-2 * t + 2, 2) / 2
        elif self.easing == EasingType.BOUNCE:
            return self._bounce_ease_out(t)
        elif self.easing == EasingType.ELASTIC:
            return self._elastic_ease_out(t)
        elif self.easing == EasingType.BACK:
            c1 = 1.70158
            c3 = c1 + 1
            return c3 * t * t * t - c1 * t * t
        else:
            return t
    
    def _bounce_ease_out(self, t: float) -> float:
        """Bounce easing function."""
        n1 = 7.5625
        d1 = 2.75
        
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t = t - 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t = t - 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t = t - 2.625 / d1
            return n1 * t * t + 0.984375
    
    def _elastic_ease_out(self, t: float) -> float:
        """Elastic easing function."""
        c4 = (2 * math.pi) / 3
        
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1
    
    def _interpolate(self, start: Any, end: Any, t: float) -> Any:
        """Interpolate between start and end values."""
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            return start + (end - start) * t
        elif isinstance(start, tuple) and isinstance(end, tuple):
            # For colors, positions, etc.
            return tuple(start[i] + (end[i] - start[i]) * t for i in range(len(start)))
        elif isinstance(start, pygame.Rect) and isinstance(end, pygame.Rect):
            return pygame.Rect(
                start.x + (end.x - start.x) * t,
                start.y + (end.y - start.y) * t,
                start.width + (end.width - start.width) * t,
                start.height + (end.height - start.height) * t
            )
        else:
            # For discrete values, snap at 50%
            return end if t >= 0.5 else start


class AnimationManager:
    """
    Manages multiple animations and provides convenient methods
    for creating common UI animation effects.
    """
    
    def __init__(self):
        self.animations: Dict[str, List[Animation]] = {}
        self.paused = False
        
    def add_animation(self, target_id: str, animation: Animation) -> None:
        """Add an animation to a target object."""
        if target_id not in self.animations:
            self.animations[target_id] = []
        self.animations[target_id].append(animation)
    
    def remove_animations(self, target_id: str) -> None:
        """Remove all animations for a target."""
        if target_id in self.animations:
            del self.animations[target_id]
    
    def update(self, delta_time: float) -> Dict[str, Dict[AnimationType, Any]]:
        """Update all animations and return current values."""
        if self.paused:
            return {}
        
        current_time = time.time()
        current_values = {}
        
        for target_id, target_animations in list(self.animations.items()):
            target_values = {}
            
            # Update animations and collect completed ones
            completed_animations = []
            for animation in target_animations:
                value = animation.update(current_time)
                target_values[animation.type] = value
                
                if animation.is_complete:
                    completed_animations.append(animation)
            
            # Remove completed animations
            for completed in completed_animations:
                target_animations.remove(completed)
            
            # Remove empty animation lists
            if not target_animations:
                del self.animations[target_id]
            else:
                current_values[target_id] = target_values
        
        return current_values
    
    def pause(self) -> None:
        """Pause all animations."""
        self.paused = True
    
    def resume(self) -> None:
        """Resume all animations."""
        self.paused = False
    
    def is_animating(self, target_id: str) -> bool:
        """Check if a target has active animations."""
        return target_id in self.animations and len(self.animations[target_id]) > 0
    
    # Convenience methods for common animations
    
    def fade_in(self, target_id: str, duration: float = 0.5, 
                easing: EasingType = EasingType.EASE_OUT, 
                delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a fade in animation."""
        animation = Animation(
            AnimationType.FADE, 0.0, 1.0, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def fade_out(self, target_id: str, duration: float = 0.5,
                 easing: EasingType = EasingType.EASE_IN,
                 delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a fade out animation."""
        animation = Animation(
            AnimationType.FADE, 1.0, 0.0, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def slide_in(self, target_id: str, start_pos: Tuple[int, int], 
                end_pos: Tuple[int, int], duration: float = 0.8,
                easing: EasingType = EasingType.EASE_OUT,
                delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a slide in animation."""
        animation = Animation(
            AnimationType.POSITION, start_pos, end_pos, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def slide_out(self, target_id: str, start_pos: Tuple[int, int],
                  end_pos: Tuple[int, int], duration: float = 0.5,
                  easing: EasingType = EasingType.EASE_IN,
                  delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a slide out animation."""
        animation = Animation(
            AnimationType.POSITION, start_pos, end_pos, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def scale_in(self, target_id: str, duration: float = 0.6,
                 easing: EasingType = EasingType.BACK,
                 delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a scale in animation."""
        animation = Animation(
            AnimationType.SCALE, 0.0, 1.0, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def scale_out(self, target_id: str, duration: float = 0.4,
                  easing: EasingType = EasingType.EASE_IN,
                  delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a scale out animation."""
        animation = Animation(
            AnimationType.SCALE, 1.0, 0.0, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def bounce_in(self, target_id: str, duration: float = 1.0,
                  delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a bouncy scale in animation."""
        animation = Animation(
            AnimationType.SCALE, 0.0, 1.0, duration, EasingType.BOUNCE, delay, callback
        )
        self.add_animation(target_id, animation)
    
    def color_transition(self, target_id: str, start_color: Tuple[int, int, int],
                        end_color: Tuple[int, int, int], duration: float = 0.5,
                        easing: EasingType = EasingType.EASE_IN_OUT,
                        delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a color transition animation."""
        animation = Animation(
            AnimationType.COLOR, start_color, end_color, duration, easing, delay, callback
        )
        self.add_animation(target_id, animation)


class UITransitionEffect:
    """
    Manages screen transition effects like crossfades, wipes, and slides.
    """
    
    def __init__(self, screen_size: Tuple[int, int]):
        self.screen_size = screen_size
        self.transition_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.is_transitioning = False
        self.transition_progress = 0.0
        self.transition_duration = 0.5
        self.transition_type = "fade"
        self.on_transition_complete: Optional[Callable] = None
    
    def start_transition(self, transition_type: str = "fade", 
                        duration: float = 0.5,
                        callback: Optional[Callable] = None) -> None:
        """Start a screen transition effect."""
        self.is_transitioning = True
        self.transition_progress = 0.0
        self.transition_duration = duration
        self.transition_type = transition_type
        self.on_transition_complete = callback
    
    def update(self, delta_time: float) -> None:
        """Update transition progress."""
        if not self.is_transitioning:
            return
        
        self.transition_progress += delta_time / self.transition_duration
        
        if self.transition_progress >= 1.0:
            self.transition_progress = 1.0
            self.is_transitioning = False
            if self.on_transition_complete:
                self.on_transition_complete()
    
    def render_transition_overlay(self, surface: pygame.Surface) -> None:
        """Render transition overlay effect."""
        if not self.is_transitioning:
            return
        
        self.transition_surface.fill((0, 0, 0, 0))  # Clear
        
        if self.transition_type == "fade":
            self._render_fade_transition()
        elif self.transition_type == "slide_left":
            self._render_slide_transition(-1, 0)
        elif self.transition_type == "slide_right":
            self._render_slide_transition(1, 0)
        elif self.transition_type == "slide_up":
            self._render_slide_transition(0, -1)
        elif self.transition_type == "slide_down":
            self._render_slide_transition(0, 1)
        elif self.transition_type == "circle_wipe":
            self._render_circle_wipe()
        
        surface.blit(self.transition_surface, (0, 0))
    
    def _render_fade_transition(self) -> None:
        """Render fade transition effect."""
        # Smooth fade using ease-out
        eased_progress = 1 - (1 - self.transition_progress) ** 2
        alpha = int(255 * eased_progress)
        self.transition_surface.fill((0, 0, 0, alpha))
    
    def _render_slide_transition(self, dir_x: int, dir_y: int) -> None:
        """Render slide transition effect."""
        # Slide overlay across screen
        width, height = self.screen_size
        progress = self.transition_progress
        
        # Use ease-out easing
        eased_progress = 1 - (1 - progress) ** 3
        
        x_offset = int(width * dir_x * (1 - eased_progress))
        y_offset = int(height * dir_y * (1 - eased_progress))
        
        # Draw sliding overlay
        overlay_rect = pygame.Rect(x_offset, y_offset, width, height)
        pygame.draw.rect(self.transition_surface, (0, 0, 0, 255), overlay_rect)
    
    def _render_circle_wipe(self) -> None:
        """Render circular wipe transition effect."""
        width, height = self.screen_size
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(center_x**2 + center_y**2)
        
        # Use ease-out easing
        eased_progress = 1 - (1 - self.transition_progress) ** 2
        current_radius = int(max_radius * eased_progress)
        
        # Fill entire surface, then cut out circle
        self.transition_surface.fill((0, 0, 0, 255))
        pygame.draw.circle(self.transition_surface, (0, 0, 0, 0), 
                          (center_x, center_y), current_radius)