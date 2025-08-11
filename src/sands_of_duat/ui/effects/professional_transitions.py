"""
Professional Transitions System - Hades-Level Polish
Smooth screen transitions with multiple effect types and easing functions.
"""

import pygame
import math
from typing import Optional, Callable, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import Colors, Timing, SCREEN_WIDTH, SCREEN_HEIGHT

class TransitionType(Enum):
    """Types of screen transitions."""
    FADE = auto()           # Classic fade in/out
    SLIDE_LEFT = auto()     # Slide from right to left
    SLIDE_RIGHT = auto()    # Slide from left to right
    SLIDE_UP = auto()       # Slide from bottom to top
    SLIDE_DOWN = auto()     # Slide from top to bottom
    ZOOM_IN = auto()        # Zoom into center
    ZOOM_OUT = auto()       # Zoom out from center
    DISSOLVE = auto()       # Particle-based dissolve
    EGYPTIAN_SANDS = auto() # Custom sand-based transition

class EasingType(Enum):
    """Easing functions for smooth animations."""
    LINEAR = auto()
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_IN_OUT = auto()
    EASE_IN_CUBIC = auto()
    EASE_OUT_CUBIC = auto()
    EASE_IN_OUT_CUBIC = auto()
    BOUNCE = auto()
    ELASTIC = auto()

@dataclass
class TransitionState:
    """Current state of a transition."""
    active: bool = False
    progress: float = 0.0
    duration: float = 1.0
    transition_type: TransitionType = TransitionType.FADE
    easing_type: EasingType = EasingType.EASE_IN_OUT
    from_surface: Optional[pygame.Surface] = None
    to_surface: Optional[pygame.Surface] = None
    callback: Optional[Callable] = None
    custom_data: Dict[str, Any] = None

class ProfessionalTransitions:
    """
    Professional screen transition system with Hades-level polish.
    Supports multiple transition types with smooth easing functions.
    """
    
    def __init__(self):
        """Initialize the transitions system."""
        self.current_transition = TransitionState()
        self.particle_effects = []
        
        # Screen capture surfaces
        self.screen_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        print("Professional Transitions System initialized")
    
    def start_transition(self, 
                        transition_type: TransitionType,
                        duration: float = None,
                        easing: EasingType = EasingType.EASE_IN_OUT,
                        callback: Callable = None,
                        from_surface: pygame.Surface = None) -> bool:
        """
        Start a screen transition.
        
        Args:
            transition_type: Type of transition to perform
            duration: Duration in seconds (uses default if None)
            easing: Easing function to use
            callback: Function to call when transition completes
            from_surface: Source surface (current screen)
            
        Returns:
            True if transition started successfully
        """
        if self.current_transition.active:
            return False
        
        # Set default duration based on transition type
        if duration is None:
            duration_map = {
                TransitionType.FADE: 0.5,
                TransitionType.SLIDE_LEFT: 0.6,
                TransitionType.SLIDE_RIGHT: 0.6,
                TransitionType.SLIDE_UP: 0.6,
                TransitionType.SLIDE_DOWN: 0.6,
                TransitionType.ZOOM_IN: 0.8,
                TransitionType.ZOOM_OUT: 0.8,
                TransitionType.DISSOLVE: 1.0,
                TransitionType.EGYPTIAN_SANDS: 1.2
            }
            duration = duration_map.get(transition_type, 0.6)
        
        # Initialize transition state
        self.current_transition = TransitionState(
            active=True,
            progress=0.0,
            duration=duration,
            transition_type=transition_type,
            easing_type=easing,
            from_surface=from_surface.copy() if from_surface else None,
            callback=callback,
            custom_data={}
        )
        
        # Initialize effect-specific data
        if transition_type == TransitionType.DISSOLVE:
            self._init_dissolve_particles()
        elif transition_type == TransitionType.EGYPTIAN_SANDS:
            self._init_sand_particles()
        
        return True
    
    def update(self, dt: float):
        """Update active transitions."""
        if not self.current_transition.active:
            return
        
        # Update progress
        self.current_transition.progress += dt / self.current_transition.duration
        
        if self.current_transition.progress >= 1.0:
            # Transition complete
            self.current_transition.progress = 1.0
            self.current_transition.active = False
            
            # Call completion callback
            if self.current_transition.callback:
                self.current_transition.callback()
        
        # Update effect-specific elements
        if self.current_transition.transition_type == TransitionType.DISSOLVE:
            self._update_dissolve_particles(dt)
        elif self.current_transition.transition_type == TransitionType.EGYPTIAN_SANDS:
            self._update_sand_particles(dt)
    
    def render_transition(self, surface: pygame.Surface, to_surface: pygame.Surface = None):
        """
        Render the active transition effect.
        
        Args:
            surface: Target surface to render to
            to_surface: Destination surface (new screen)
        """
        if not self.current_transition.active:
            return
        
        # Apply easing to progress
        eased_progress = self._apply_easing(
            self.current_transition.progress, 
            self.current_transition.easing_type
        )
        
        # Clear transition surface
        self.transition_surface.fill((0, 0, 0, 0))
        
        # Render based on transition type
        if self.current_transition.transition_type == TransitionType.FADE:
            self._render_fade(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.SLIDE_LEFT:
            self._render_slide_left(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.SLIDE_RIGHT:
            self._render_slide_right(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.SLIDE_UP:
            self._render_slide_up(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.SLIDE_DOWN:
            self._render_slide_down(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.ZOOM_IN:
            self._render_zoom_in(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.ZOOM_OUT:
            self._render_zoom_out(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.DISSOLVE:
            self._render_dissolve(surface, to_surface, eased_progress)
        elif self.current_transition.transition_type == TransitionType.EGYPTIAN_SANDS:
            self._render_egyptian_sands(surface, to_surface, eased_progress)
    
    def _apply_easing(self, t: float, easing: EasingType) -> float:
        """Apply easing function to progress value."""
        if easing == EasingType.LINEAR:
            return t
        elif easing == EasingType.EASE_IN:
            return t * t
        elif easing == EasingType.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif easing == EasingType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        elif easing == EasingType.EASE_IN_CUBIC:
            return t * t * t
        elif easing == EasingType.EASE_OUT_CUBIC:
            return 1 - (1 - t) ** 3
        elif easing == EasingType.EASE_IN_OUT_CUBIC:
            if t < 0.5:
                return 4 * t * t * t
            else:
                return 1 - 4 * (1 - t) ** 3
        elif easing == EasingType.BOUNCE:
            if t < 0.5:
                return 2 * t * t
            else:
                return 2 * t * (2 - t)
        elif easing == EasingType.ELASTIC:
            if t == 0 or t == 1:
                return t
            return -(2 ** (10 * (t - 1))) * math.sin((t - 1.1) * 5 * math.pi)
        
        return t  # Fallback to linear
    
    def _render_fade(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render fade transition."""
        if self.current_transition.from_surface:
            # Fade out from surface
            from_alpha = int(255 * (1 - progress))
            fade_surface = self.current_transition.from_surface.copy()
            fade_surface.set_alpha(from_alpha)
            surface.blit(fade_surface, (0, 0))
        
        if to_surface:
            # Fade in to surface
            to_alpha = int(255 * progress)
            fade_to = to_surface.copy()
            fade_to.set_alpha(to_alpha)
            surface.blit(fade_to, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _render_slide_left(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render slide left transition."""
        offset_x = int(SCREEN_WIDTH * progress)
        
        if self.current_transition.from_surface:
            surface.blit(self.current_transition.from_surface, (-offset_x, 0))
        
        if to_surface:
            surface.blit(to_surface, (SCREEN_WIDTH - offset_x, 0))
    
    def _render_slide_right(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render slide right transition."""
        offset_x = int(SCREEN_WIDTH * progress)
        
        if self.current_transition.from_surface:
            surface.blit(self.current_transition.from_surface, (offset_x, 0))
        
        if to_surface:
            surface.blit(to_surface, (-SCREEN_WIDTH + offset_x, 0))
    
    def _render_slide_up(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render slide up transition."""
        offset_y = int(SCREEN_HEIGHT * progress)
        
        if self.current_transition.from_surface:
            surface.blit(self.current_transition.from_surface, (0, -offset_y))
        
        if to_surface:
            surface.blit(to_surface, (0, SCREEN_HEIGHT - offset_y))
    
    def _render_slide_down(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render slide down transition."""
        offset_y = int(SCREEN_HEIGHT * progress)
        
        if self.current_transition.from_surface:
            surface.blit(self.current_transition.from_surface, (0, offset_y))
        
        if to_surface:
            surface.blit(to_surface, (0, -SCREEN_HEIGHT + offset_y))
    
    def _render_zoom_in(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render zoom in transition."""
        if self.current_transition.from_surface:
            # Zoom out from surface
            scale = 1.0 + progress * 0.5
            scaled_size = (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))
            scaled_surface = pygame.transform.smoothscale(self.current_transition.from_surface, scaled_size)
            
            # Center the scaled surface
            x = (SCREEN_WIDTH - scaled_size[0]) // 2
            y = (SCREEN_HEIGHT - scaled_size[1]) // 2
            
            # Fade out while zooming
            alpha = int(255 * (1 - progress))
            scaled_surface.set_alpha(alpha)
            surface.blit(scaled_surface, (x, y))
        
        if to_surface:
            # Zoom in to surface
            scale = 0.5 + progress * 0.5
            scaled_size = (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))
            scaled_surface = pygame.transform.smoothscale(to_surface, scaled_size)
            
            # Center the scaled surface
            x = (SCREEN_WIDTH - scaled_size[0]) // 2
            y = (SCREEN_HEIGHT - scaled_size[1]) // 2
            
            # Fade in while zooming
            alpha = int(255 * progress)
            scaled_surface.set_alpha(alpha)
            surface.blit(scaled_surface, (x, y))
    
    def _render_zoom_out(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render zoom out transition."""
        if self.current_transition.from_surface:
            # Zoom in from surface
            scale = 1.0 - progress * 0.5
            scaled_size = (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))
            scaled_surface = pygame.transform.smoothscale(self.current_transition.from_surface, scaled_size)
            
            # Center the scaled surface
            x = (SCREEN_WIDTH - scaled_size[0]) // 2
            y = (SCREEN_HEIGHT - scaled_size[1]) // 2
            
            # Fade out while zooming
            alpha = int(255 * (1 - progress))
            scaled_surface.set_alpha(alpha)
            surface.blit(scaled_surface, (x, y))
        
        if to_surface:
            # Zoom out from surface
            scale = 1.5 - progress * 0.5
            scaled_size = (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale))
            scaled_surface = pygame.transform.smoothscale(to_surface, scaled_size)
            
            # Center the scaled surface
            x = (SCREEN_WIDTH - scaled_size[0]) // 2
            y = (SCREEN_HEIGHT - scaled_size[1]) // 2
            
            # Fade in while zooming
            alpha = int(255 * progress)
            scaled_surface.set_alpha(alpha)
            surface.blit(scaled_surface, (x, y))
    
    def _init_dissolve_particles(self):
        """Initialize particles for dissolve effect."""
        import random
        self.particle_effects.clear()
        
        # Create grid of particles
        particle_size = 8
        for y in range(0, SCREEN_HEIGHT, particle_size):
            for x in range(0, SCREEN_WIDTH, particle_size):
                self.particle_effects.append({
                    'x': x,
                    'y': y,
                    'size': particle_size,
                    'delay': random.random() * 0.8,  # Stagger the dissolve
                    'alpha': 255,
                    'active': False
                })
    
    def _update_dissolve_particles(self, dt: float):
        """Update dissolve particles."""
        progress = self.current_transition.progress
        
        for particle in self.particle_effects:
            if progress >= particle['delay'] and not particle['active']:
                particle['active'] = True
            
            if particle['active']:
                # Fade out particle
                fade_progress = (progress - particle['delay']) / (1.0 - particle['delay'])
                fade_progress = max(0, min(1, fade_progress))
                particle['alpha'] = int(255 * (1 - fade_progress))
    
    def _render_dissolve(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render dissolve transition."""
        # Draw base surface
        if to_surface:
            surface.blit(to_surface, (0, 0))
        
        # Draw dissolving from surface
        if self.current_transition.from_surface:
            for particle in self.particle_effects:
                if particle['alpha'] > 0:
                    # Extract particle area from source
                    particle_rect = pygame.Rect(particle['x'], particle['y'], 
                                               particle['size'], particle['size'])
                    try:
                        particle_surface = self.current_transition.from_surface.subsurface(particle_rect)
                        particle_copy = particle_surface.copy()
                        particle_copy.set_alpha(particle['alpha'])
                        surface.blit(particle_copy, (particle['x'], particle['y']))
                    except ValueError:
                        # Handle edge cases where particle goes off screen
                        pass
    
    def _init_sand_particles(self):
        """Initialize sand particles for Egyptian transition."""
        import random
        self.particle_effects.clear()
        
        for _ in range(200):
            self.particle_effects.append({
                'x': random.randint(-50, SCREEN_WIDTH + 50),
                'y': random.randint(-50, SCREEN_HEIGHT + 50),
                'vx': random.randint(-100, 100),
                'vy': random.randint(50, 200),
                'size': random.randint(2, 6),
                'alpha': random.randint(100, 255),
                'color': random.choice([Colors.GOLD, Colors.DESERT_SAND, Colors.PAPYRUS])
            })
    
    def _update_sand_particles(self, dt: float):
        """Update sand particles."""
        for particle in self.particle_effects:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            
            # Wrap around screen
            if particle['x'] < -50:
                particle['x'] = SCREEN_WIDTH + 50
            elif particle['x'] > SCREEN_WIDTH + 50:
                particle['x'] = -50
            
            if particle['y'] > SCREEN_HEIGHT + 50:
                particle['y'] = -50
    
    def _render_egyptian_sands(self, surface: pygame.Surface, to_surface: pygame.Surface, progress: float):
        """Render Egyptian sand transition."""
        # Base surfaces with alpha blending
        if self.current_transition.from_surface and progress < 0.8:
            from_alpha = int(255 * (1 - progress / 0.8))
            from_copy = self.current_transition.from_surface.copy()
            from_copy.set_alpha(from_alpha)
            surface.blit(from_copy, (0, 0))
        
        if to_surface and progress > 0.2:
            to_alpha = int(255 * ((progress - 0.2) / 0.8))
            to_copy = to_surface.copy()
            to_copy.set_alpha(to_alpha)
            surface.blit(to_copy, (0, 0))
        
        # Render sand particles
        sand_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for particle in self.particle_effects:
            # Vary alpha based on progress
            alpha = int(particle['alpha'] * (1 - abs(progress - 0.5) * 2))
            if alpha > 0:
                particle_color = (*particle['color'], alpha)
                pygame.draw.circle(sand_surface, particle_color,
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
        
        surface.blit(sand_surface, (0, 0))
    
    def is_active(self) -> bool:
        """Check if a transition is currently active."""
        return self.current_transition.active
    
    def get_progress(self) -> float:
        """Get current transition progress (0.0 to 1.0)."""
        return self.current_transition.progress if self.current_transition.active else 0.0

# Global transitions system instance
professional_transitions = ProfessionalTransitions()