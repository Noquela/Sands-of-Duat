"""
Master Visual Effects Manager

Coordinates all visual effects systems to create a cohesive cinematic
experience across all UI screens. Integrates particle systems, lighting,
parallax backgrounds, card effects, and cinematic polish.
"""

import pygame
import time
from typing import Dict, List, Tuple, Optional, Any

# Import all our visual effects systems
from .particle_system import ParticleSystem, ParticleType
from .lighting_system import LightingSystem, get_lighting_system, create_lighting_for_screen
from .parallax_system import ParallaxSystem, get_parallax_system, create_scene_for_screen
from .card_effects_system import CardEffectsSystem, get_card_effects_system, CardType, CardRarity
from .cinematic_effects import CinematicEffectsSystem, get_cinematic_system, TransitionType


class VisualEffectsManager:
    """Master manager that coordinates all visual effects systems."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize all systems
        self.particle_system = ParticleSystem(max_particles=2000)
        self.lighting_system = get_lighting_system(screen_width, screen_height)
        self.parallax_system = get_parallax_system(screen_width, screen_height)
        self.card_effects_system = get_card_effects_system()
        self.cinematic_system = get_cinematic_system(screen_width, screen_height)
        
        # Connect systems
        self.card_effects_system.set_particle_system(self.particle_system)
        
        # Current screen state
        self.current_screen = ""
        self.screen_context = {}
        
        # Master effects settings
        self.effects_enabled = True
        self.performance_mode = "high"  # low, medium, high
        self.atmospheric_intensity = 1.0
        
        # Screen-specific settings
        self.screen_effects_config = {
            "menu": {
                "particles": True,
                "lighting": True,
                "parallax": True,
                "atmospheric_dust": True,
                "camera_movement": False
            },
            "combat": {
                "particles": True,
                "lighting": True,
                "parallax": True,
                "atmospheric_dust": False,
                "camera_movement": True,
                "impact_effects": True
            },
            "deck_builder": {
                "particles": True,
                "lighting": False,
                "parallax": False,
                "card_effects": True,
                "focus_effects": True
            },
            "map": {
                "particles": True,
                "lighting": True,
                "parallax": True,
                "atmospheric_dust": True,
                "time_effects": True
            }
        }
        
        # Performance tracking
        self.last_performance_check = time.time()
        self.frame_times = []
        self.auto_adjust_quality = True
    
    def initialize_screen_effects(self, screen_name: str, context: Dict[str, Any] = None) -> None:
        """Initialize visual effects for a specific screen."""
        self.current_screen = screen_name
        self.screen_context = context or {}
        
        config = self.screen_effects_config.get(screen_name, {})
        
        # Set up parallax background
        if config.get("parallax", False):
            create_scene_for_screen(screen_name, context)
        else:
            self.parallax_system.clear_layers()
        
        # Set up lighting
        if config.get("lighting", False):
            create_lighting_for_screen(screen_name, context)
        else:
            self.lighting_system.clear_lights()
        
        # Set up atmospheric effects
        if config.get("atmospheric_dust", False):
            self._create_atmospheric_effects(screen_name)
        
        # Configure camera
        if not config.get("camera_movement", False):
            self.cinematic_system.reset_camera()
        
        # Screen-specific initialization
        if screen_name == "combat":
            self._initialize_combat_effects(context)
        elif screen_name == "menu":
            self._initialize_menu_effects(context)
        elif screen_name == "deck_builder":
            self._initialize_deck_builder_effects(context)
        elif screen_name == "map":
            self._initialize_map_effects(context)
    
    def _create_atmospheric_effects(self, screen_name: str) -> None:
        """Create atmospheric particle effects for the screen."""
        if screen_name in ["menu", "map"]:
            # Floating dust motes
            self.particle_system.create_atmospheric_dust_motes(
                self.screen_width // 2, self.screen_height // 2,
                self.screen_width, self.screen_height, 
                self.atmospheric_intensity * 0.5
            )
        
        elif screen_name == "combat":
            # Combat atmosphere - more intense
            self.particle_system.create_spirit_wisp_effect(
                self.screen_width // 4, self.screen_height // 3,
                self.atmospheric_intensity * 0.8
            )
            self.particle_system.create_spirit_wisp_effect(
                3 * self.screen_width // 4, self.screen_height // 3,
                self.atmospheric_intensity * 0.8
            )
    
    def _initialize_combat_effects(self, context: Dict[str, Any]) -> None:
        """Initialize combat-specific effects."""
        # Set dramatic lighting mode
        self.lighting_system.set_ambient_lighting((20, 15, 25), 0.15)
        
        # Add combat particles
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Background mystical effects
        self.particle_system.create_egyptian_mystical_effect(
            center_x, center_y - 100, "underworld_flame", 0.8
        )
        
        # Set cinematic mode
        self.cinematic_system.set_visual_effect("vignette", 0.2)
    
    def _initialize_menu_effects(self, context: Dict[str, Any]) -> None:
        """Initialize menu-specific effects."""
        # Gentle atmospheric effects
        self.lighting_system.set_ambient_lighting((50, 45, 40), 0.5)
        
        # Menu torches
        self.lighting_system.create_torch_light(200, 300, True)
        self.lighting_system.create_torch_light(self.screen_width - 200, 300, True)
        
        # Floating mystical orbs
        self.particle_system.create_egyptian_mystical_effect(
            300, 200, "spirit_wisp", 0.6
        )
        self.particle_system.create_egyptian_mystical_effect(
            self.screen_width - 300, 200, "spirit_wisp", 0.6
        )
    
    def _initialize_deck_builder_effects(self, context: Dict[str, Any]) -> None:
        """Initialize deck builder-specific effects."""
        # Clean, focused environment
        self.lighting_system.set_ambient_lighting((60, 55, 50), 0.6)
        
        # Subtle central lighting
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.lighting_system.create_magical_orb(center_x, center_y - 100, (200, 220, 255))
    
    def _initialize_map_effects(self, context: Dict[str, Any]) -> None:
        """Initialize map-specific effects."""
        hour = context.get("hour", 1)
        
        # Time-based effects
        if hour <= 3:
            # Early night - mystical
            self.particle_system.create_egyptian_mystical_effect(
                self.screen_width // 2, self.screen_height // 4, "hieroglyph_magic", 0.7
            )
        elif hour <= 6:
            # Deep night - ominous
            self.particle_system.create_egyptian_mystical_effect(
                self.screen_width // 3, self.screen_height // 3, "underworld_flame", 0.9
            )
        else:
            # Late night - ethereal
            self.particle_system.create_egyptian_mystical_effect(
                2 * self.screen_width // 3, self.screen_height // 4, "spirit_wisp", 0.8
            )
    
    def update(self, delta_time: float) -> None:
        """Update all visual effects systems."""
        if not self.effects_enabled:
            return
        
        # Update all systems
        self.particle_system.update(delta_time)
        self.lighting_system.update(delta_time)
        self.parallax_system.update(delta_time)
        self.card_effects_system.update(delta_time)
        self.cinematic_system.update(delta_time)
        
        # Performance monitoring
        self._check_performance(delta_time)
        
        # Screen-specific updates
        if self.current_screen == "combat":
            self._update_combat_effects(delta_time)
        elif self.current_screen == "menu":
            self._update_menu_effects(delta_time)
    
    def _update_combat_effects(self, delta_time: float) -> None:
        """Update combat-specific effects."""
        # Continuous atmospheric effects
        if self.particle_system.get_particle_count() < 100:
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            
            self.particle_system.create_atmospheric_dust_motes(
                center_x, center_y, 200, 150, 0.3
            )
    
    def _update_menu_effects(self, delta_time: float) -> None:
        """Update menu-specific effects."""
        # Periodic mystical effects
        current_time = time.time()
        if int(current_time) % 10 == 0 and (current_time % 1) < delta_time:
            self.particle_system.create_egyptian_mystical_effect(
                self.screen_width // 2, self.screen_height // 3, "ankh_blessing", 0.5
            )
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all visual effects to the surface."""
        if not self.effects_enabled:
            return
        
        # Get camera offset
        camera_offset = self.cinematic_system.get_camera_offset()
        
        # Render parallax background
        self.parallax_system.render(surface)
        
        # Render lighting
        self.lighting_system.render_lighting(surface)
        
        # Render particles
        self.particle_system.render(surface)
        
        # Apply cinematic effects
        self.cinematic_system.apply_visual_effects(surface)
        
        # Render transitions
        self.cinematic_system.render_transition(surface)
    
    def render_card_effects(self, surface: pygame.Surface, card_rect: pygame.Rect, card_id: str) -> None:
        """Render effects for a specific card."""
        if self.effects_enabled and self.screen_effects_config.get(self.current_screen, {}).get("card_effects", True):
            self.card_effects_system.render_card_effects(surface, card_rect, card_id)
    
    def register_card(self, card_id: str, card_type: str, rarity: str) -> None:
        """Register a card with the effects system."""
        try:
            card_type_enum = CardType(card_type.lower())
        except ValueError:
            card_type_enum = CardType.ATTACK
        
        try:
            rarity_enum = CardRarity(rarity.lower())
        except ValueError:
            rarity_enum = CardRarity.COMMON
        
        self.card_effects_system.register_card(card_id, card_type_enum, rarity_enum)
    
    def set_card_hover(self, card_id: str, hovering: bool) -> None:
        """Set card hover state."""
        if hovering:
            from .card_effects_system import EffectState
            self.card_effects_system.set_card_state(card_id, EffectState.HOVER)
        else:
            from .card_effects_system import EffectState
            self.card_effects_system.set_card_state(card_id, EffectState.IDLE)
    
    def play_card_effect(self, card_id: str, card_rect: pygame.Rect, target_pos: Tuple[int, int], card_type: str = "attack") -> None:
        """Play dramatic effect when a card is used."""
        # Card-specific effects
        self.card_effects_system.create_play_effect(card_id, card_rect, target_pos)
        
        # Screen effects
        config = self.screen_effects_config.get(self.current_screen, {})
        if config.get("impact_effects", False):
            # Screen shake based on card type
            if card_type == "attack":
                self.cinematic_system.create_impact_effect(target_pos[0], target_pos[1], 1.0)
            elif card_type == "power":
                self.cinematic_system.create_magical_effect(1.2)
            else:
                self.cinematic_system.create_magical_effect(0.8)
        
        # Lighting effects
        if config.get("lighting", False):
            self.lighting_system.create_card_play_lighting(target_pos[0], target_pos[1], card_type)
        
        # Particle trail
        start_x, start_y = card_rect.center
        self.particle_system.create_enhanced_sand_effect(
            start_x, start_y, target_pos[0], target_pos[1], 1.5
        )
    
    def trigger_screen_transition(self, transition_type: str, duration: float = 1.0) -> None:
        """Trigger a screen transition effect."""
        try:
            transition_enum = TransitionType(transition_type)
        except ValueError:
            transition_enum = TransitionType.FADE
        
        self.cinematic_system.start_transition(transition_enum, duration)
    
    def create_victory_effects(self) -> None:
        """Create victory celebration effects."""
        # Lighting
        self.lighting_system.create_victory_lighting()
        
        # Particles
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.particle_system.create_egyptian_mystical_effect(
            center_x, center_y, "ankh_blessing", 2.0
        )
        self.particle_system.create_egyptian_mystical_effect(
            center_x, center_y, "pyramid_energy", 1.5
        )
        
        # Screen effects
        self.cinematic_system.create_magical_effect(1.5)
        self.cinematic_system.set_visual_effect("bloom", 0.4)
    
    def create_defeat_effects(self) -> None:
        """Create defeat effects."""
        # Lighting
        self.lighting_system.create_defeat_lighting()
        
        # Screen effects
        self.cinematic_system.set_visual_effect("vignette", 0.6)
        self.cinematic_system.set_visual_effect("chromatic_aberration", 0.1)
    
    def _check_performance(self, delta_time: float) -> None:
        """Monitor performance and adjust quality if needed."""
        if not self.auto_adjust_quality:
            return
        
        current_time = time.time()
        self.frame_times.append(delta_time)
        
        # Check performance every 2 seconds
        if current_time - self.last_performance_check > 2.0:
            self.last_performance_check = current_time
            
            if len(self.frame_times) > 0:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 60
                
                # Adjust quality based on FPS
                if fps < 30 and self.performance_mode == "high":
                    self.set_performance_mode("medium")
                elif fps < 20 and self.performance_mode == "medium":
                    self.set_performance_mode("low")
                elif fps > 50 and self.performance_mode == "medium":
                    self.set_performance_mode("high")
                elif fps > 40 and self.performance_mode == "low":
                    self.set_performance_mode("medium")
            
            # Clear frame times
            self.frame_times = self.frame_times[-60:]  # Keep last 60 frames
    
    def set_performance_mode(self, mode: str) -> None:
        """Set performance mode for all effects systems."""
        self.performance_mode = mode
        
        if mode == "low":
            self.particle_system.max_particles = 500
            self.lighting_system.light_quality = "low"
            self.lighting_system.enable_particles = False
            self.parallax_system.enable_advanced_effects = False
            self.cinematic_system.high_quality_effects = False
            self.atmospheric_intensity = 0.5
        
        elif mode == "medium":
            self.particle_system.max_particles = 1000
            self.lighting_system.light_quality = "medium"
            self.lighting_system.enable_particles = True
            self.parallax_system.enable_advanced_effects = True
            self.cinematic_system.high_quality_effects = True
            self.atmospheric_intensity = 0.75
        
        else:  # high
            self.particle_system.max_particles = 2000
            self.lighting_system.light_quality = "high"
            self.lighting_system.enable_particles = True
            self.parallax_system.enable_advanced_effects = True
            self.cinematic_system.high_quality_effects = True
            self.atmospheric_intensity = 1.0
    
    def set_effects_enabled(self, enabled: bool) -> None:
        """Enable or disable all visual effects."""
        self.effects_enabled = enabled
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.particle_system.clear_all()
        self.lighting_system.clear_lights()
        self.parallax_system.clear_layers()
        self.card_effects_system.clear_all_effects()
        self.cinematic_system.clear_all_effects()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            "particle_count": self.particle_system.get_particle_count(),
            "light_count": self.lighting_system.get_light_count() if hasattr(self.lighting_system, 'get_light_count') else len(self.lighting_system.lights),
            "parallax_layers": self.parallax_system.get_layer_count(),
            "performance_mode": self.performance_mode,
            "effects_enabled": self.effects_enabled,
            "atmospheric_intensity": self.atmospheric_intensity
        }


# Global visual effects manager
_global_visual_effects_manager = None

def get_visual_effects_manager(screen_width: int = 3440, screen_height: int = 1440) -> VisualEffectsManager:
    """Get global visual effects manager."""
    global _global_visual_effects_manager
    if _global_visual_effects_manager is None:
        _global_visual_effects_manager = VisualEffectsManager(screen_width, screen_height)
    return _global_visual_effects_manager