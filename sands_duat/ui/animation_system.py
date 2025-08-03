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
    # Egyptian-themed animations
    ANKH_GLOW = "ankh_glow"
    SCARAB_SPIN = "scarab_spin"
    LOTUS_BLOOM = "lotus_bloom"
    SAND_PARTICLE = "sand_particle"
    EGYPTIAN_PULSE = "egyptian_pulse"


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
    
    # Egyptian-themed animation methods
    
    def ankh_selection(self, target_id: str, duration: float = 0.8,
                      delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create an Ankh-themed glow animation for card selection."""
        # Ankh glow effect with pulsing golden light
        glow_animation = Animation(
            AnimationType.ANKH_GLOW, 0.0, 1.0, duration, EasingType.EASE_IN_OUT, delay, callback
        )
        self.add_animation(target_id, glow_animation)
    
    def scarab_rare_rotation(self, target_id: str, duration: float = 2.0,
                           delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a rotating scarab animation for rare cards."""
        # Continuous rotation with elastic easing for mystical effect
        rotation_animation = Animation(
            AnimationType.SCARAB_SPIN, 0.0, 360.0, duration, EasingType.ELASTIC, delay, callback
        )
        self.add_animation(target_id, rotation_animation)
    
    def lotus_hover_bloom(self, target_id: str, duration: float = 0.6,
                         delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a lotus bloom animation for hover effects."""
        # Scaling bloom with back easing for natural flower opening
        bloom_animation = Animation(
            AnimationType.LOTUS_BLOOM, 0.8, 1.2, duration, EasingType.BACK, delay, callback
        )
        self.add_animation(target_id, bloom_animation)
    
    def egyptian_pulse(self, target_id: str, intensity: float = 0.3, duration: float = 1.5,
                      delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create a mystical Egyptian pulse animation."""
        # Gentle pulsing effect for special cards or UI elements
        pulse_animation = Animation(
            AnimationType.EGYPTIAN_PULSE, 1.0, 1.0 + intensity, duration, EasingType.EASE_IN_OUT, delay, callback
        )
        self.add_animation(target_id, pulse_animation)
    
    def sand_particle_drift(self, target_id: str, start_pos: Tuple[int, int],
                           end_pos: Tuple[int, int], duration: float = 3.0,
                           delay: float = 0.0, callback: Optional[Callable] = None) -> None:
        """Create drifting sand particle animation."""
        # Smooth particle movement with slight randomness
        drift_animation = Animation(
            AnimationType.SAND_PARTICLE, start_pos, end_pos, duration, EasingType.EASE_OUT, delay, callback
        )
        self.add_animation(target_id, drift_animation)
    
    def chain_egyptian_effects(self, target_id: str, effect_sequence: List[str]) -> None:
        """Chain multiple Egyptian effects together."""
        base_delay = 0.0
        for effect in effect_sequence:
            if effect == "ankh":
                self.ankh_selection(target_id, delay=base_delay)
                base_delay += 0.8
            elif effect == "scarab":
                self.scarab_rare_rotation(target_id, delay=base_delay)
                base_delay += 2.0
            elif effect == "lotus":
                self.lotus_hover_bloom(target_id, delay=base_delay)
                base_delay += 0.6
            elif effect == "pulse":
                self.egyptian_pulse(target_id, delay=base_delay)
                base_delay += 1.5
    
    def get_egyptian_renderer(self) -> 'EgyptianAnimationRenderer':
        """Get the Egyptian animation renderer for custom effects."""
        if not hasattr(self, '_egyptian_renderer'):
            self._egyptian_renderer = EgyptianAnimationRenderer()
        return self._egyptian_renderer


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


class EgyptianAnimationRenderer:
    """
    Specialized renderer for Egyptian-themed animations.
    Handles complex visual effects like Ankh glows, scarab rotations, and lotus blooms.
    """
    
    def __init__(self):
        self.egyptian_colors = {
            'gold': (255, 215, 0),
            'bronze': (139, 117, 93),
            'sandstone': (245, 222, 179),
            'deep_brown': (47, 27, 20)
        }
    
    def render_ankh_glow(self, surface: pygame.Surface, rect: pygame.Rect, 
                        glow_intensity: float, base_color: Tuple[int, int, int] = None) -> None:
        """Render an Ankh-shaped glow effect."""
        if base_color is None:
            base_color = self.egyptian_colors['gold']
        
        # Calculate glow parameters
        glow_radius = int(10 * glow_intensity)
        glow_alpha = int(100 * glow_intensity)
        
        # Create glow surface
        glow_surface = pygame.Surface((rect.width + glow_radius * 2, rect.height + glow_radius * 2), pygame.SRCALPHA)
        
        # Draw multiple circles for glow effect
        center_x = glow_surface.get_width() // 2
        center_y = glow_surface.get_height() // 2
        
        for i in range(glow_radius, 0, -2):
            alpha = int(glow_alpha * (glow_radius - i) / glow_radius)
            glow_color = (*base_color, alpha)
            pygame.draw.circle(glow_surface, glow_color, (center_x, center_y), i)
        
        # Simple Ankh symbol (cross with loop on top)
        ankh_color = (*base_color, min(255, int(200 * glow_intensity)))
        
        # Ankh loop (circle)
        loop_radius = min(8, rect.width // 6)
        loop_center = (center_x, center_y - rect.height // 4)
        pygame.draw.circle(glow_surface, ankh_color, loop_center, loop_radius, 2)
        
        # Ankh vertical line
        pygame.draw.line(glow_surface, ankh_color, 
                        (center_x, loop_center[1]), 
                        (center_x, center_y + rect.height // 3), 3)
        
        # Ankh horizontal line
        h_line_y = center_y - rect.height // 8
        pygame.draw.line(glow_surface, ankh_color,
                        (center_x - rect.width // 4, h_line_y),
                        (center_x + rect.width // 4, h_line_y), 3)
        
        # Blit to main surface
        surface.blit(glow_surface, (rect.x - glow_radius, rect.y - glow_radius))
    
    def render_scarab_rotation(self, surface: pygame.Surface, rect: pygame.Rect, 
                              rotation_angle: float, base_color: Tuple[int, int, int] = None) -> None:
        """Render a rotating scarab beetle effect."""
        if base_color is None:
            base_color = self.egyptian_colors['bronze']
        
        # Create scarab surface
        scarab_size = min(rect.width, rect.height) // 3
        scarab_surface = pygame.Surface((scarab_size * 2, scarab_size * 2), pygame.SRCALPHA)
        
        center = scarab_size
        
        # Simple scarab shape (oval body with small circles for details)
        body_rect = pygame.Rect(center - scarab_size//3, center - scarab_size//2, 
                               scarab_size//1.5, scarab_size)
        
        # Rotate the scarab
        import math
        cos_a = math.cos(math.radians(rotation_angle))
        sin_a = math.sin(math.radians(rotation_angle))
        
        # Draw scarab body
        pygame.draw.ellipse(scarab_surface, base_color, body_rect)
        
        # Add wing details
        wing_points = [
            (center - scarab_size//4, center - scarab_size//3),
            (center + scarab_size//4, center - scarab_size//3),
            (center + scarab_size//3, center),
            (center - scarab_size//3, center)
        ]
        
        # Rotate wing points
        rotated_points = []
        for x, y in wing_points:
            rx = center + (x - center) * cos_a - (y - center) * sin_a
            ry = center + (x - center) * sin_a + (y - center) * cos_a
            rotated_points.append((rx, ry))
        
        if len(rotated_points) >= 3:
            pygame.draw.polygon(scarab_surface, 
                              (base_color[0] + 20, base_color[1] + 20, base_color[2] + 20), 
                              rotated_points)
        
        # Blit to main surface
        blit_x = rect.centerx - scarab_size
        blit_y = rect.centery - scarab_size
        surface.blit(scarab_surface, (blit_x, blit_y))
    
    def render_lotus_bloom(self, surface: pygame.Surface, rect: pygame.Rect, 
                          bloom_scale: float, base_color: Tuple[int, int, int] = None) -> None:
        """Render a blooming lotus flower effect."""
        if base_color is None:
            base_color = (100, 180, 100)  # Green lotus
        
        # Calculate bloom parameters
        petal_count = 8
        center_x, center_y = rect.center
        base_radius = min(rect.width, rect.height) // 6
        bloom_radius = int(base_radius * bloom_scale)
        
        # Draw petals
        import math
        for i in range(petal_count):
            angle = (2 * math.pi * i) / petal_count
            
            # Petal positions
            petal_x = center_x + int(bloom_radius * math.cos(angle) * 0.7)
            petal_y = center_y + int(bloom_radius * math.sin(angle) * 0.7)
            
            # Petal size based on bloom scale
            petal_size = int(8 * bloom_scale)
            
            # Draw petal as small circle
            if petal_size > 0:
                pygame.draw.circle(surface, base_color, (petal_x, petal_y), petal_size)
        
        # Draw center
        center_size = int(4 * bloom_scale)
        if center_size > 0:
            pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), center_size)
    
    def render_egyptian_pulse(self, surface: pygame.Surface, rect: pygame.Rect, 
                             pulse_intensity: float, base_color: Tuple[int, int, int] = None) -> None:
        """Render a mystical Egyptian pulse effect."""
        if base_color is None:
            base_color = self.egyptian_colors['gold']
        
        # Create pulse overlay
        pulse_alpha = int(50 * pulse_intensity)
        if pulse_alpha > 0:
            pulse_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            pulse_color = (*base_color, pulse_alpha)
            pygame.draw.rect(pulse_surface, pulse_color, (0, 0, rect.width, rect.height))
            
            # Add border glow
            border_color = (*base_color, min(255, int(100 * pulse_intensity)))
            pygame.draw.rect(pulse_surface, border_color, (0, 0, rect.width, rect.height), 2)
            
            surface.blit(pulse_surface, rect.topleft)
    
    def render_sand_particles(self, surface: pygame.Surface, particles: List[Tuple[int, int, float]]) -> None:
        """Render drifting sand particles."""
        sand_color = self.egyptian_colors['sandstone']
        
        for x, y, alpha in particles:
            if 0 <= alpha <= 1:
                particle_color = (*sand_color, int(255 * alpha))
                particle_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle_color, (1, 1), 1)
                surface.blit(particle_surface, (int(x), int(y)))