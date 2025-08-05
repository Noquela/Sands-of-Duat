"""
Interactive Parallax System for Sands of Duat

Adds responsive visual effects and mouse-driven parallax interactions
to create a living, breathing Egyptian underworld experience.
"""

import pygame
import math
import time
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

from .parallax_background_system import get_parallax_renderer, ParallaxRenderer
from .advanced_particle_system import get_particle_system
from .performance_optimizer import get_performance_optimizer, optimize_for_performance


class InteractionType(Enum):
    """Types of interactive events that can trigger parallax responses."""
    MOUSE_MOVE = "mouse_move"
    BUTTON_HOVER = "button_hover"
    BUTTON_CLICK = "button_click"
    CARD_HOVER = "card_hover"
    CARD_PLAY = "card_play"
    SCREEN_TRANSITION = "screen_transition"
    COMBAT_ACTION = "combat_action"


@dataclass
class InteractionEffect:
    """Configuration for an interactive parallax effect."""
    effect_type: InteractionType
    parallax_influence: float = 0.1  # How much interaction affects parallax
    particle_burst: bool = False
    particle_count: int = 10
    camera_shake: float = 0.0
    ripple_effect: bool = False
    ripple_radius: float = 100.0
    duration: float = 0.5
    ease_out: bool = True


class InteractiveParallaxSystem:
    """Enhanced parallax system with interactive responsiveness."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Get core parallax renderer
        self.parallax_renderer = get_parallax_renderer(screen_width, screen_height)
        self.particle_system = get_particle_system()
        
        # Performance optimization
        self.performance_optimizer = get_performance_optimizer()
        
        # Mouse tracking
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_velocity_x = 0.0
        self.mouse_velocity_y = 0.0
        
        # Interactive effects
        self.active_effects: List[Dict[str, Any]] = []
        self.effect_configs: Dict[InteractionType, InteractionEffect] = {}
        
        # Camera system enhancements
        self.base_camera_x = 0.0
        self.base_camera_y = 0.0
        self.interactive_offset_x = 0.0
        self.interactive_offset_y = 0.0
        self.camera_smoothing = 0.15
        
        # Ripple effects
        self.ripples: List[Dict[str, Any]] = []
        
        # Screen-specific configurations
        self.current_screen = "menu"
        self.screen_configs = self._initialize_screen_configs()
        
        # Performance tracking
        self.update_time = 0.0
        
        self._setup_default_effects()
    
    def _initialize_screen_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize screen-specific parallax configurations."""
        return {
            "menu": {
                "mouse_sensitivity": 0.8,
                "particle_density": 1.0,
                "atmosphere": {"sandstorm": 0.2, "heat": 0.6, "wind_speed": 15.0},
                "camera_bounds": (-50, -30, 50, 30)
            },
            "combat": {
                "mouse_sensitivity": 0.4,
                "particle_density": 1.5,
                "atmosphere": {"sandstorm": 0.4, "heat": 0.8, "mystical_energy": 0.7},
                "camera_bounds": (-30, -20, 30, 20)
            },
            "deck_builder": {
                "mouse_sensitivity": 0.6,
                "particle_density": 0.8,
                "atmosphere": {"mystical_energy": 0.9, "floating_scrolls": 0.6},
                "camera_bounds": (-40, -25, 40, 25)
            },
            "progression": {
                "mouse_sensitivity": 0.5,
                "particle_density": 0.9,
                "atmosphere": {"energy_rivers": 0.8, "underworld_mist": 0.5},
                "camera_bounds": (-35, -20, 35, 20)
            }
        }
    
    def _setup_default_effects(self):
        """Setup default interactive effects for different interaction types."""
        self.effect_configs = {
            InteractionType.MOUSE_MOVE: InteractionEffect(
                effect_type=InteractionType.MOUSE_MOVE,
                parallax_influence=0.1,
                duration=0.0  # Continuous
            ),
            
            InteractionType.BUTTON_HOVER: InteractionEffect(
                effect_type=InteractionType.BUTTON_HOVER,
                parallax_influence=0.05,
                particle_burst=True,
                particle_count=5,
                ripple_effect=True,
                ripple_radius=50.0,
                duration=0.3
            ),
            
            InteractionType.BUTTON_CLICK: InteractionEffect(
                effect_type=InteractionType.BUTTON_CLICK,
                parallax_influence=0.15,
                particle_burst=True,
                particle_count=15,
                camera_shake=2.0,
                ripple_effect=True,
                ripple_radius=80.0,
                duration=0.6
            ),
            
            InteractionType.CARD_HOVER: InteractionEffect(
                effect_type=InteractionType.CARD_HOVER,
                parallax_influence=0.08,
                particle_burst=True,
                particle_count=8,
                ripple_effect=True,
                ripple_radius=60.0,
                duration=0.4
            ),
            
            InteractionType.CARD_PLAY: InteractionEffect(
                effect_type=InteractionType.CARD_PLAY,
                parallax_influence=0.2,
                particle_burst=True,
                particle_count=25,
                camera_shake=3.0,
                ripple_effect=True,
                ripple_radius=120.0,
                duration=1.0
            ),
            
            InteractionType.COMBAT_ACTION: InteractionEffect(
                effect_type=InteractionType.COMBAT_ACTION,
                parallax_influence=0.25,
                particle_burst=True,
                particle_count=30,
                camera_shake=4.0,
                ripple_effect=True,
                ripple_radius=150.0,
                duration=1.2
            )
        }
    
    def set_current_screen(self, screen_name: str):
        """Set the current screen for context-aware effects."""
        self.current_screen = screen_name
        
        # Load appropriate parallax environment
        if screen_name == "menu":
            self.parallax_renderer.load_background_for_environment("desert")
        elif screen_name == "combat":
            self.parallax_renderer.load_background_for_environment("temple")
        elif screen_name == "deck_builder":
            self.parallax_renderer.load_background_for_environment("pyramid")
        elif screen_name == "progression":
            self.parallax_renderer.load_background_for_environment("pyramid")
        
        # Update atmospheric conditions
        screen_config = self.screen_configs.get(screen_name, {})
        atmosphere = screen_config.get("atmosphere", {})
        self.parallax_renderer.set_weather_conditions(atmosphere)
    
    def handle_mouse_motion(self, mouse_x: int, mouse_y: int):
        """Handle mouse movement for responsive parallax."""
        self.last_mouse_x = self.mouse_x
        self.last_mouse_y = self.mouse_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
        # Calculate mouse velocity
        self.mouse_velocity_x = mouse_x - self.last_mouse_x
        self.mouse_velocity_y = mouse_y - self.last_mouse_y
        
        # Trigger mouse move effect
        self.trigger_interaction_effect(InteractionType.MOUSE_MOVE, mouse_x, mouse_y)
    
    def trigger_interaction_effect(self, effect_type: InteractionType, x: int, y: int, 
                                 custom_config: Optional[InteractionEffect] = None):
        """Trigger an interactive parallax effect."""
        config = custom_config or self.effect_configs.get(effect_type)
        if not config:
            return
        
        screen_config = self.screen_configs.get(self.current_screen, {})
        sensitivity = screen_config.get("mouse_sensitivity", 1.0)
        
        effect = {
            "type": effect_type,
            "config": config,
            "start_time": time.time(),
            "x": x,
            "y": y,
            "sensitivity": sensitivity,
            "active": True,
            "intensity": 1.0
        }
        
        # Add particle burst if configured
        if config.particle_burst and self.particle_system:
            self._create_interaction_particles(x, y, config.particle_count)
        
        # Add ripple effect if configured
        if config.ripple_effect:
            self._create_ripple_effect(x, y, config.ripple_radius)
        
        # Add camera shake if configured
        if config.camera_shake > 0:
            self._apply_camera_shake(config.camera_shake)
        
        self.active_effects.append(effect)
    
    def _create_interaction_particles(self, x: int, y: int, count: int):
        """Create particle effects for interactions."""
        if not self.particle_system:
            return
        
        # Create Egyptian-themed particles based on current screen
        if self.current_screen == "menu":
            # Desert sand particles
            for _ in range(count):
                self.particle_system.add_particle(
                    x=x + random.uniform(-20, 20),
                    y=y + random.uniform(-20, 20),
                    velocity_x=random.uniform(-30, 30),
                    velocity_y=random.uniform(-50, -10),
                    color=(255, 215, 0),  # Gold sand
                    size=random.uniform(2, 4),
                    lifetime=random.uniform(1.0, 2.0),
                    particle_type="sand"
                )
        
        elif self.current_screen == "combat":
            # Mystical energy particles
            for _ in range(count):
                self.particle_system.add_particle(
                    x=x + random.uniform(-30, 30),
                    y=y + random.uniform(-30, 30),
                    velocity_x=random.uniform(-40, 40),
                    velocity_y=random.uniform(-60, -20),
                    color=(0, 255, 200),  # Mystical teal
                    size=random.uniform(3, 6),
                    lifetime=random.uniform(1.5, 3.0),
                    particle_type="energy"
                )
        
        elif self.current_screen == "deck_builder":
            # Floating ink/scroll particles
            for _ in range(count):
                self.particle_system.add_particle(
                    x=x + random.uniform(-25, 25),
                    y=y + random.uniform(-25, 25),
                    velocity_x=random.uniform(-20, 20),
                    velocity_y=random.uniform(-30, 30),
                    color=(139, 117, 93),  # Ancient parchment
                    size=random.uniform(2, 5),
                    lifetime=random.uniform(2.0, 4.0),
                    particle_type="parchment"
                )
    
    def _create_ripple_effect(self, x: int, y: int, radius: float):
        """Create a ripple effect that influences parallax layers."""
        ripple = {
            "x": x,
            "y": y,
            "max_radius": radius,
            "current_radius": 0.0,
            "intensity": 1.0,
            "start_time": time.time(),
            "duration": 1.0
        }
        self.ripples.append(ripple)
    
    def _apply_camera_shake(self, intensity: float):
        """Apply camera shake effect."""
        import random
        shake_x = random.uniform(-intensity, intensity)
        shake_y = random.uniform(-intensity, intensity)
        
        # Add shake to interactive offset
        self.interactive_offset_x += shake_x
        self.interactive_offset_y += shake_y
    
    def update(self, delta_time: float):
        """Update interactive parallax system."""
        current_time = time.time()
        
        # Update active effects
        for effect in self.active_effects[:]:
            elapsed = current_time - effect["start_time"]
            
            if effect["config"].duration > 0 and elapsed > effect["config"].duration:
                # Effect expired
                self.active_effects.remove(effect)
                continue
            
            # Update effect intensity (ease out if configured)
            if effect["config"].ease_out and effect["config"].duration > 0:
                progress = elapsed / effect["config"].duration
                effect["intensity"] = 1.0 - progress
            
            # Apply effect to camera
            self._apply_effect_to_camera(effect)
        
        # Update ripple effects
        for ripple in self.ripples[:]:
            elapsed = current_time - ripple["start_time"]
            if elapsed > ripple["duration"]:
                self.ripples.remove(ripple)
                continue
            
            # Update ripple expansion
            progress = elapsed / ripple["duration"]
            ripple["current_radius"] = ripple["max_radius"] * progress
            ripple["intensity"] = 1.0 - progress
        
        # Update mouse-based parallax
        self._update_mouse_parallax()
        
        # Apply smoothed camera position
        target_x = self.base_camera_x + self.interactive_offset_x
        target_y = self.base_camera_y + self.interactive_offset_y
        
        # Apply camera bounds
        screen_config = self.screen_configs.get(self.current_screen, {})
        bounds = screen_config.get("camera_bounds", (-50, -30, 50, 30))
        min_x, min_y, max_x, max_y = bounds
        
        target_x = max(min_x, min(max_x, target_x))
        target_y = max(min_y, min(max_y, target_y))
        
        self.parallax_renderer.set_camera_position(target_x, target_y, smooth=True)
        
        # Update core parallax system
        screen_config = self.screen_configs.get(self.current_screen, {})
        atmosphere = screen_config.get("atmosphere", {})
        self.parallax_renderer.update(delta_time, atmosphere)
        
        # Decay interactive offset
        self.interactive_offset_x *= (1.0 - delta_time * 2.0)
        self.interactive_offset_y *= (1.0 - delta_time * 2.0)
    
    def _apply_effect_to_camera(self, effect: Dict[str, Any]):
        """Apply an interactive effect to the camera position."""
        if effect["type"] == InteractionType.MOUSE_MOVE:
            # Continuous mouse-based parallax
            return  # Handled in _update_mouse_parallax
        
        config = effect["config"]
        intensity = effect["intensity"] * effect["sensitivity"]
        
        # Calculate effect offset based on position and type
        if effect["type"] in [InteractionType.BUTTON_HOVER, InteractionType.BUTTON_CLICK]:
            # Center-based offset
            center_x = self.screen_width / 2
            center_y = self.screen_height / 2
            offset_x = (effect["x"] - center_x) / center_x * config.parallax_influence * intensity
            offset_y = (effect["y"] - center_y) / center_y * config.parallax_influence * intensity
            
            self.interactive_offset_x += offset_x * 0.1
            self.interactive_offset_y += offset_y * 0.1
    
    def _update_mouse_parallax(self):
        """Update mouse-driven parallax effects."""
        screen_config = self.screen_configs.get(self.current_screen, {})
        sensitivity = screen_config.get("mouse_sensitivity", 1.0)
        
        # Calculate normalized mouse position (-1 to 1)
        norm_x = (self.mouse_x / self.screen_width - 0.5) * 2.0
        norm_y = (self.mouse_y / self.screen_height - 0.5) * 2.0
        
        # Apply mouse-based camera offset
        mouse_offset_x = norm_x * 20.0 * sensitivity
        mouse_offset_y = norm_y * 15.0 * sensitivity
        
        # Smooth transition to mouse position
        self.interactive_offset_x += (mouse_offset_x - self.interactive_offset_x) * 0.05
        self.interactive_offset_y += (mouse_offset_y - self.interactive_offset_y) * 0.05
    
    @optimize_for_performance
    def render(self, surface: pygame.Surface, camera_rect: Optional[pygame.Rect] = None):
        """Render the interactive parallax background."""
        # Get quality settings
        quality_settings = self.performance_optimizer.get_current_settings()
        
        # Render core parallax background
        self.parallax_renderer.render(surface, camera_rect)
        
        # Render ripple effects only if interactive effects are enabled
        if quality_settings.interactive_effects_enabled:
            self._render_ripple_effects(surface)
    
    def _render_ripple_effects(self, surface: pygame.Surface):
        """Render ripple effects on the background."""
        for ripple in self.ripples:
            if ripple["intensity"] > 0.1:
                # Draw subtle ripple rings
                alpha = int(ripple["intensity"] * 50)
                ripple_color = (255, 255, 255, alpha)
                
                # Create ripple surface
                ripple_surface = pygame.Surface((int(ripple["current_radius"] * 2), 
                                               int(ripple["current_radius"] * 2)), pygame.SRCALPHA)
                
                center = (int(ripple["current_radius"]), int(ripple["current_radius"]))
                
                # Draw multiple rings for depth
                for i in range(3):
                    ring_radius = int(ripple["current_radius"] * (0.8 + i * 0.1))
                    if ring_radius > 2:
                        pygame.draw.circle(ripple_surface, (255, 255, 255), center, ring_radius, 2)
                
                # Apply alpha
                ripple_surface.set_alpha(alpha)
                
                # Blit to main surface
                ripple_pos = (ripple["x"] - ripple["current_radius"], 
                             ripple["y"] - ripple["current_radius"])
                surface.blit(ripple_surface, ripple_pos, special_flags=pygame.BLEND_ADD)
    
    def get_render_statistics(self) -> Dict[str, Any]:
        """Get rendering and performance statistics."""
        stats = self.parallax_renderer.get_render_statistics()
        stats.update({
            "active_effects": len(self.active_effects),
            "active_ripples": len(self.ripples),
            "current_screen": self.current_screen,
            "interactive_offset": (self.interactive_offset_x, self.interactive_offset_y)
        })
        return stats


# Global interactive parallax system
_global_interactive_parallax = None

def get_interactive_parallax_system(screen_width: int = 3440, screen_height: int = 1440) -> InteractiveParallaxSystem:
    """Get global interactive parallax system."""
    global _global_interactive_parallax
    if _global_interactive_parallax is None:
        _global_interactive_parallax = InteractiveParallaxSystem(screen_width, screen_height)
    return _global_interactive_parallax


def trigger_ui_interaction(interaction_type: InteractionType, x: int, y: int):
    """Convenient function to trigger UI interactions from any screen."""
    system = get_interactive_parallax_system()
    system.trigger_interaction_effect(interaction_type, x, y)


def handle_mouse_parallax(mouse_x: int, mouse_y: int):
    """Convenient function to handle mouse parallax from any screen."""
    system = get_interactive_parallax_system()
    system.handle_mouse_motion(mouse_x, mouse_y)