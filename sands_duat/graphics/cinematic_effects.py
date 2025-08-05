"""
Cinematic Effects System

Provides screen shake, smooth camera movements, transitions, and other
cinematic polish effects that make the game feel like an interactive
Egyptian mythology art book.
"""

import pygame
import math
import random
import time
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class TransitionType(Enum):
    """Types of screen transitions."""
    FADE = "fade"
    SAND_STORM = "sand_storm"
    MYSTICAL_PORTAL = "mystical_portal"
    SLIDE = "slide"
    DISSOLVE = "dissolve"
    PAPYRUS_SCROLL = "papyrus_scroll"


class CameraMovementType(Enum):
    """Types of camera movements."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    ELASTIC = "elastic"
    BOUNCE = "bounce"


@dataclass
class ScreenShake:
    """Screen shake effect properties."""
    intensity: float
    duration: float
    frequency: float = 15.0
    decay: float = 1.0
    time_elapsed: float = 0.0
    active: bool = True


@dataclass
class CameraMovement:
    """Camera movement animation."""
    start_x: float
    start_y: float
    target_x: float
    target_y: float
    duration: float
    movement_type: CameraMovementType
    time_elapsed: float = 0.0
    active: bool = True
    ease_function: Optional[Callable] = None


@dataclass
class ScreenTransition:
    """Screen transition effect."""
    transition_type: TransitionType
    duration: float
    progress: float = 0.0
    active: bool = True
    direction: int = 1  # 1 for in, -1 for out
    color: Tuple[int, int, int, int] = (0, 0, 0, 255)
    custom_data: Dict[str, Any] = field(default_factory=dict)


class CinematicEffectsSystem:
    """Main system for cinematic effects and screen polish."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Camera properties
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_zoom = 1.0
        self.camera_rotation = 0.0
        
        # Effects
        self.screen_shakes: List[ScreenShake] = []
        self.camera_movements: List[CameraMovement] = []
        self.current_transition: Optional[ScreenTransition] = None
        
        # Visual effects
        self.chromatic_aberration = 0.0
        self.bloom_intensity = 0.0
        self.vignette_intensity = 0.0
        self.screen_distortion = 0.0
        
        # Timing and smoothing
        self.smooth_camera = True
        self.camera_smoothing_factor = 0.1
        self.target_camera_x = 0.0
        self.target_camera_y = 0.0
        
        # Performance settings
        self.high_quality_effects = True
        self.particle_density = 1.0
        
        # Surfaces for effects
        self.effect_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.transition_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    
    def trigger_screen_shake(self, intensity: float, duration: float, frequency: float = 15.0) -> None:
        """Trigger screen shake effect."""
        shake = ScreenShake(
            intensity=intensity,
            duration=duration,
            frequency=frequency,
            decay=1.0
        )
        self.screen_shakes.append(shake)
    
    def move_camera_to(self, target_x: float, target_y: float, duration: float, 
                      movement_type: CameraMovementType = CameraMovementType.EASE_IN_OUT) -> None:
        """Animate camera to target position."""
        movement = CameraMovement(
            start_x=self.camera_x,
            start_y=self.camera_y,
            target_x=target_x,
            target_y=target_y,
            duration=duration,
            movement_type=movement_type
        )
        
        # Set appropriate easing function
        if movement_type == CameraMovementType.EASE_IN:
            movement.ease_function = self._ease_in
        elif movement_type == CameraMovementType.EASE_OUT:
            movement.ease_function = self._ease_out
        elif movement_type == CameraMovementType.EASE_IN_OUT:
            movement.ease_function = self._ease_in_out
        elif movement_type == CameraMovementType.ELASTIC:
            movement.ease_function = self._ease_elastic
        elif movement_type == CameraMovementType.BOUNCE:
            movement.ease_function = self._ease_bounce
        else:  # LINEAR
            movement.ease_function = lambda t: t
        
        self.camera_movements.append(movement)
    
    def _ease_in(self, t: float) -> float:
        """Ease in (quadratic)."""
        return t * t
    
    def _ease_out(self, t: float) -> float:
        """Ease out (quadratic)."""
        return 1 - (1 - t) * (1 - t)
    
    def _ease_in_out(self, t: float) -> float:
        """Ease in-out (quadratic)."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)
    
    def _ease_elastic(self, t: float) -> float:
        """Elastic ease out."""
        if t == 0 or t == 1:
            return t
        
        p = 0.3
        s = p / 4
        return 1 + math.pow(2, -10 * t) * math.sin((t - s) * 2 * math.pi / p)
    
    def _ease_bounce(self, t: float) -> float:
        """Bounce ease out."""
        if t < 1/2.75:
            return 7.5625 * t * t
        elif t < 2/2.75:
            t -= 1.5/2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5/2.75:
            t -= 2.25/2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625/2.75
            return 7.5625 * t * t + 0.984375
    
    def start_transition(self, transition_type: TransitionType, duration: float, 
                        direction: int = 1, **kwargs) -> None:
        """Start a screen transition effect."""
        transition = ScreenTransition(
            transition_type=transition_type,
            duration=duration,
            direction=direction,
            custom_data=kwargs
        )
        
        # Set transition-specific properties
        if transition_type == TransitionType.FADE:
            transition.color = kwargs.get('color', (0, 0, 0, 255))
        elif transition_type == TransitionType.SAND_STORM:
            transition.color = (194, 154, 108, 255)  # Sand color
        elif transition_type == TransitionType.MYSTICAL_PORTAL:
            transition.color = (138, 43, 226, 255)  # Mystical purple
        
        self.current_transition = transition
    
    def set_visual_effect(self, effect_name: str, intensity: float) -> None:
        """Set visual effect intensity."""
        intensity = max(0.0, min(1.0, intensity))
        
        if effect_name == "chromatic_aberration":
            self.chromatic_aberration = intensity
        elif effect_name == "bloom":
            self.bloom_intensity = intensity
        elif effect_name == "vignette":
            self.vignette_intensity = intensity
        elif effect_name == "distortion":
            self.screen_distortion = intensity
    
    def update(self, delta_time: float) -> None:
        """Update all cinematic effects."""
        self._update_screen_shakes(delta_time)
        self._update_camera_movements(delta_time)
        self._update_transition(delta_time)
        self._update_smooth_camera(delta_time)
    
    def _update_screen_shakes(self, delta_time: float) -> None:
        """Update screen shake effects."""
        for shake in self.screen_shakes[:]:
            shake.time_elapsed += delta_time
            
            if shake.time_elapsed >= shake.duration:
                shake.active = False
                self.screen_shakes.remove(shake)
            else:
                # Apply decay
                progress = shake.time_elapsed / shake.duration
                shake.intensity *= (1.0 - progress * shake.decay)
    
    def _update_camera_movements(self, delta_time: float) -> None:
        """Update camera movement animations."""
        for movement in self.camera_movements[:]:
            movement.time_elapsed += delta_time
            progress = min(1.0, movement.time_elapsed / movement.duration)
            
            if progress >= 1.0:
                # Movement complete
                self.camera_x = movement.target_x
                self.camera_y = movement.target_y
                movement.active = False
                self.camera_movements.remove(movement)
            else:
                # Apply easing
                eased_progress = movement.ease_function(progress) if movement.ease_function else progress
                
                self.camera_x = movement.start_x + (movement.target_x - movement.start_x) * eased_progress
                self.camera_y = movement.start_y + (movement.target_y - movement.start_y) * eased_progress
    
    def _update_transition(self, delta_time: float) -> None:
        """Update screen transition."""
        if not self.current_transition:
            return
        
        self.current_transition.progress += delta_time / self.current_transition.duration
        
        if self.current_transition.progress >= 1.0:
            self.current_transition.progress = 1.0
            if self.current_transition.direction == 1:
                # Transition in complete, start transition out
                self.current_transition.direction = -1
                self.current_transition.progress = 0.0
            else:
                # Transition complete
                self.current_transition = None
    
    def _update_smooth_camera(self, delta_time: float) -> None:
        """Update smooth camera movement."""
        if not self.smooth_camera:
            return
        
        # Smooth movement toward target
        if abs(self.camera_x - self.target_camera_x) > 1.0:
            self.camera_x += (self.target_camera_x - self.camera_x) * self.camera_smoothing_factor
        else:
            self.camera_x = self.target_camera_x
        
        if abs(self.camera_y - self.target_camera_y) > 1.0:
            self.camera_y += (self.target_camera_y - self.camera_y) * self.camera_smoothing_factor
        else:
            self.camera_y = self.target_camera_y
    
    def get_camera_offset(self) -> Tuple[float, float]:
        """Get current camera offset including shake."""
        offset_x = -self.camera_x
        offset_y = -self.camera_y
        
        # Add screen shake
        for shake in self.screen_shakes:
            if shake.active:
                shake_magnitude = shake.intensity * math.sin(shake.time_elapsed * shake.frequency * 2 * math.pi)
                offset_x += random.uniform(-shake_magnitude, shake_magnitude)
                offset_y += random.uniform(-shake_magnitude, shake_magnitude)
        
        return offset_x, offset_y
    
    def apply_visual_effects(self, surface: pygame.Surface) -> None:
        """Apply visual effects to the surface."""
        if not self.high_quality_effects:
            return
        
        # Apply chromatic aberration
        if self.chromatic_aberration > 0:
            self._apply_chromatic_aberration(surface)
        
        # Apply bloom effect
        if self.bloom_intensity > 0:
            self._apply_bloom_effect(surface)
        
        # Apply vignette
        if self.vignette_intensity > 0:
            self._apply_vignette(surface)
        
        # Apply screen distortion
        if self.screen_distortion > 0:
            self._apply_screen_distortion(surface)
    
    def _apply_chromatic_aberration(self, surface: pygame.Surface) -> None:
        """Apply chromatic aberration effect."""
        try:
            # Simple chromatic aberration by shifting color channels
            offset = int(self.chromatic_aberration * 5)
            if offset <= 0:
                return
            
            # Create shifted surfaces for R, G, B channels
            red_surface = surface.copy()
            blue_surface = surface.copy()
            
            # Shift red channel
            shifted_red = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            shifted_red.blit(red_surface, (offset, 0))
            
            # Shift blue channel
            shifted_blue = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            shifted_blue.blit(blue_surface, (-offset, 0))
            
            # Combine channels
            surface.blit(shifted_red, (0, 0), special_flags=pygame.BLEND_ADD)
            surface.blit(shifted_blue, (0, 0), special_flags=pygame.BLEND_ADD)
            
        except Exception:
            # Fail silently for effect errors
            pass
    
    def _apply_bloom_effect(self, surface: pygame.Surface) -> None:
        """Apply bloom effect."""
        try:
            # Simple bloom by blurring and adding back
            bloom_surface = surface.copy()
            
            # Scale down for blur effect
            small_size = (surface.get_width() // 4, surface.get_height() // 4)
            bloom_surface = pygame.transform.smoothscale(bloom_surface, small_size)
            
            # Scale back up for blur
            bloom_surface = pygame.transform.smoothscale(bloom_surface, surface.get_size())
            
            # Set alpha based on bloom intensity
            bloom_surface.set_alpha(int(255 * self.bloom_intensity * 0.5))
            
            # Add bloom to original
            surface.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
        except Exception:
            pass
    
    def _apply_vignette(self, surface: pygame.Surface) -> None:
        """Apply vignette effect."""
        try:
            # Create vignette surface
            vignette_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            
            center_x = surface.get_width() // 2
            center_y = surface.get_height() // 2
            max_distance = math.sqrt(center_x * center_x + center_y * center_y)
            
            # Draw vignette gradient
            for radius in range(int(max_distance), 0, -10):
                alpha = int(255 * self.vignette_intensity * (1.0 - radius / max_distance))
                if alpha > 0:
                    pygame.draw.circle(vignette_surface, (0, 0, 0, alpha), 
                                     (center_x, center_y), radius, 5)
            
            surface.blit(vignette_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            
        except Exception:
            pass
    
    def _apply_screen_distortion(self, surface: pygame.Surface) -> None:
        """Apply screen distortion effect (simplified)."""
        # This would require more complex pixel manipulation
        # For now, apply a simple wave distortion by shifting sections
        if self.screen_distortion <= 0:
            return
        
        try:
            distortion_strength = int(self.screen_distortion * 10)
            current_time = time.time()
            
            # Create temporary surface
            temp_surface = surface.copy()
            surface.fill((0, 0, 0))
            
            # Apply wave distortion to horizontal strips
            strip_height = 20
            for y in range(0, surface.get_height(), strip_height):
                wave_offset = math.sin(current_time * 5 + y * 0.01) * distortion_strength
                strip_rect = pygame.Rect(0, y, surface.get_width(), min(strip_height, surface.get_height() - y))
                surface.blit(temp_surface, (int(wave_offset), y), strip_rect)
            
        except Exception:
            pass
    
    def render_transition(self, surface: pygame.Surface) -> None:
        """Render current screen transition."""
        if not self.current_transition:
            return
        
        # Calculate transition progress
        progress = self.current_transition.progress
        if self.current_transition.direction == -1:
            progress = 1.0 - progress
        
        # Clear transition surface
        self.transition_surface.fill((0, 0, 0, 0))
        
        if self.current_transition.transition_type == TransitionType.FADE:
            self._render_fade_transition(progress)
        
        elif self.current_transition.transition_type == TransitionType.SAND_STORM:
            self._render_sand_storm_transition(progress)
        
        elif self.current_transition.transition_type == TransitionType.MYSTICAL_PORTAL:
            self._render_mystical_portal_transition(progress)
        
        elif self.current_transition.transition_type == TransitionType.SLIDE:
            self._render_slide_transition(progress)
        
        elif self.current_transition.transition_type == TransitionType.PAPYRUS_SCROLL:
            self._render_papyrus_scroll_transition(progress)
        
        # Blit transition to main surface
        surface.blit(self.transition_surface, (0, 0))
    
    def _render_fade_transition(self, progress: float) -> None:
        """Render fade transition."""
        alpha = int(255 * progress)
        color = (*self.current_transition.color[:3], alpha)
        self.transition_surface.fill(color)
    
    def _render_sand_storm_transition(self, progress: float) -> None:
        """Render sand storm transition."""
        # Create sand particle effect across screen
        particle_count = int(200 * progress)
        
        for _ in range(particle_count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 4)
            alpha = random.randint(100, 255)
            
            color = (*self.current_transition.color[:3], alpha)
            pygame.draw.circle(self.transition_surface, color, (x, y), size)
    
    def _render_mystical_portal_transition(self, progress: float) -> None:
        """Render mystical portal transition."""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Portal expanding from center
        max_radius = math.sqrt(center_x * center_x + center_y * center_y)
        current_radius = int(max_radius * progress)
        
        if current_radius > 0:
            # Create spiral pattern
            for angle in range(0, 360, 5):
                spiral_radius = current_radius * (1.0 - (angle % 60) / 60.0)
                rad = math.radians(angle + progress * 360)
                
                x = center_x + math.cos(rad) * spiral_radius
                y = center_y + math.sin(rad) * spiral_radius
                
                if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                    alpha = int(255 * (1.0 - spiral_radius / max_radius))
                    color = (*self.current_transition.color[:3], alpha)
                    pygame.draw.circle(self.transition_surface, color, (int(x), int(y)), 3)
    
    def _render_slide_transition(self, progress: float) -> None:
        """Render slide transition."""
        slide_distance = int(self.screen_width * progress)
        slide_rect = pygame.Rect(0, 0, slide_distance, self.screen_height)
        pygame.draw.rect(self.transition_surface, self.current_transition.color, slide_rect)
    
    def _render_papyrus_scroll_transition(self, progress: float) -> None:
        """Render papyrus scroll transition."""
        # Scroll effect from top and bottom
        scroll_height = int(self.screen_height * progress * 0.5)
        
        # Top scroll
        top_rect = pygame.Rect(0, 0, self.screen_width, scroll_height)
        pygame.draw.rect(self.transition_surface, (240, 220, 180, 255), top_rect)
        
        # Bottom scroll
        bottom_rect = pygame.Rect(0, self.screen_height - scroll_height, 
                                 self.screen_width, scroll_height)
        pygame.draw.rect(self.transition_surface, (240, 220, 180, 255), bottom_rect)
        
        # Add papyrus texture lines
        for i in range(0, self.screen_width, 20):
            if scroll_height > 10:
                pygame.draw.line(self.transition_surface, (220, 200, 160, 180),
                               (i, 0), (i, scroll_height), 1)
                pygame.draw.line(self.transition_surface, (220, 200, 160, 180),
                               (i, self.screen_height - scroll_height), (i, self.screen_height), 1)
    
    def create_impact_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create impact effect with shake and visual effects."""
        # Screen shake
        self.trigger_screen_shake(intensity * 10, 0.3)
        
        # Visual effects
        self.set_visual_effect("chromatic_aberration", intensity * 0.1)
        self.set_visual_effect("distortion", intensity * 0.05)
        
        # Temporary bloom
        self.set_visual_effect("bloom", intensity * 0.3)
    
    def create_magical_effect(self, intensity: float = 1.0) -> None:
        """Create magical effect for spells and abilities."""
        # Gentle shake
        self.trigger_screen_shake(intensity * 5, 0.5, 8.0)
        
        # Mystical visual effects
        self.set_visual_effect("bloom", intensity * 0.4)
        self.set_visual_effect("vignette", intensity * 0.2)
    
    def focus_camera_on(self, target_x: float, target_y: float, smooth: bool = True) -> None:
        """Focus camera on target position."""
        if smooth and self.smooth_camera:
            self.target_camera_x = target_x - self.screen_width // 2
            self.target_camera_y = target_y - self.screen_height // 2
        else:
            self.camera_x = target_x - self.screen_width // 2
            self.camera_y = target_y - self.screen_height // 2
    
    def reset_camera(self) -> None:
        """Reset camera to default position."""
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.target_camera_x = 0.0
        self.target_camera_y = 0.0
        self.camera_zoom = 1.0
        self.camera_rotation = 0.0
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.screen_shakes.clear()
        self.camera_movements.clear()
        self.current_transition = None
        
        self.chromatic_aberration = 0.0
        self.bloom_intensity = 0.0
        self.vignette_intensity = 0.0
        self.screen_distortion = 0.0


# Global cinematic effects system
_global_cinematic_system = None

def get_cinematic_system(screen_width: int = 3440, screen_height: int = 1440) -> CinematicEffectsSystem:
    """Get global cinematic effects system."""
    global _global_cinematic_system
    if _global_cinematic_system is None:
        _global_cinematic_system = CinematicEffectsSystem(screen_width, screen_height)
    return _global_cinematic_system