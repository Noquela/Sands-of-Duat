#!/usr/bin/env python3
"""
Advanced Particle Effects System for Sands of Duat
Creates Hades-quality visual effects for cards, combat, and atmospheric elements.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
import numpy as np

class ParticleType(Enum):
    """Types of particle effects available."""
    SAND_PARTICLES = "sand_particles"
    MAGIC_SPARKLES = "magic_sparkles" 
    DIVINE_LIGHT = "divine_light"
    FLOATING_HIEROGLYPHS = "floating_hieroglyphs"
    ENERGY_WISPS = "energy_wisps"
    SCARAB_SWARM = "scarab_swarm"
    GOLDEN_DUST = "golden_dust"
    MYSTICAL_FOG = "mystical_fog"
    SOLAR_FLARE = "solar_flare"
    ETHEREAL_SMOKE = "ethereal_smoke"

@dataclass
class ParticleConfig:
    """Configuration for particle system behavior."""
    max_particles: int = 100
    spawn_rate: float = 10.0  # particles per second
    lifetime: float = 3.0     # seconds
    speed: Tuple[float, float] = (50.0, 100.0)  # min, max pixels per second
    size: Tuple[float, float] = (2.0, 6.0)      # min, max size
    color_start: Tuple[int, int, int, int] = (255, 215, 0, 255)  # Gold
    color_end: Tuple[int, int, int, int] = (255, 215, 0, 0)      # Transparent gold
    gravity: float = 0.0
    fade_in_time: float = 0.2
    fade_out_time: float = 0.5
    wind_effect: float = 0.0
    rotation_speed: float = 0.0
    texture_path: Optional[str] = None
    blend_mode: int = pygame.BLEND_ALPHA_SDL2

class Particle:
    """Individual particle with position, velocity, and visual properties."""
    
    def __init__(self, x: float, y: float, config: ParticleConfig):
        self.x = x
        self.y = y
        self.config = config
        
        # Velocity with random variation
        speed = random.uniform(config.speed[0], config.speed[1])
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Visual properties
        self.size = random.uniform(config.size[0], config.size[1])
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = config.rotation_speed
        
        # Lifecycle
        self.age = 0.0
        self.lifetime = config.lifetime + random.uniform(-0.5, 0.5)  # Slight variation
        self.alpha = 0
        
        # Color interpolation
        self.start_color = config.color_start
        self.end_color = config.color_end
        
        # Load texture if specified
        self.texture = None
        if config.texture_path:
            try:
                self.texture = pygame.image.load(config.texture_path).convert_alpha()
                # Scale texture to particle size
                size_int = int(self.size)
                self.texture = pygame.transform.scale(self.texture, (size_int, size_int))
            except:
                self.texture = None
    
    def update(self, dt: float) -> bool:
        """Update particle. Returns False if particle should be removed."""
        self.age += dt
        
        if self.age >= self.lifetime:
            return False
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += self.config.gravity * dt
        
        # Apply wind effect
        self.vx += self.config.wind_effect * dt
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update alpha based on lifecycle
        life_ratio = self.age / self.lifetime
        
        if self.age < self.config.fade_in_time:
            # Fade in
            fade_ratio = self.age / self.config.fade_in_time
            self.alpha = int(self.start_color[3] * fade_ratio)
        elif self.age > (self.lifetime - self.config.fade_out_time):
            # Fade out
            fade_start = self.lifetime - self.config.fade_out_time
            fade_ratio = (self.age - fade_start) / self.config.fade_out_time
            self.alpha = int(self.start_color[3] * (1.0 - fade_ratio))
        else:
            # Full alpha
            self.alpha = self.start_color[3]
        
        return True
    
    def get_current_color(self) -> Tuple[int, int, int, int]:
        """Get current color based on particle age."""
        life_ratio = self.age / self.lifetime
        
        r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * life_ratio)
        g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * life_ratio)
        b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * life_ratio)
        
        return (r, g, b, self.alpha)
    
    def render(self, surface: pygame.Surface):
        """Render the particle."""
        if self.alpha <= 0:
            return
        
        if self.texture:
            # Render textured particle
            if self.rotation != 0:
                rotated = pygame.transform.rotate(self.texture, self.rotation)
                rect = rotated.get_rect(center=(int(self.x), int(self.y)))
                # Apply alpha
                rotated.set_alpha(self.alpha)
                surface.blit(rotated, rect, special_flags=self.config.blend_mode)
            else:
                rect = self.texture.get_rect(center=(int(self.x), int(self.y)))
                self.texture.set_alpha(self.alpha)
                surface.blit(self.texture, rect, special_flags=self.config.blend_mode)
        else:
            # Render colored circle particle
            color = self.get_current_color()
            if color[3] > 0:
                # Create temporary surface for alpha blending
                temp_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, color, (int(self.size), int(self.size)), int(self.size))
                
                surface.blit(temp_surf, 
                           (int(self.x - self.size), int(self.y - self.size)),
                           special_flags=self.config.blend_mode)

class ParticleSystem:
    """Complete particle system managing multiple particle types and effects."""
    
    def __init__(self):
        self.particle_groups: Dict[str, List[Particle]] = {}
        self.configs: Dict[ParticleType, ParticleConfig] = {}
        self.spawn_timers: Dict[str, float] = {}
        self.active_effects: Dict[str, bool] = {}
        
        # Initialize predefined particle configs
        self._setup_egyptian_particle_configs()
    
    def _setup_egyptian_particle_configs(self):
        """Setup predefined particle configurations for Egyptian theme."""
        
        # Sand particles for desert effects
        self.configs[ParticleType.SAND_PARTICLES] = ParticleConfig(
            max_particles=150,
            spawn_rate=30.0,
            lifetime=4.0,
            speed=(20.0, 60.0),
            size=(1.0, 4.0),
            color_start=(218, 165, 32, 200),  # Sandy brown
            color_end=(139, 69, 19, 0),       # Darker brown, transparent
            gravity=50.0,
            wind_effect=10.0,
            blend_mode=pygame.BLEND_ALPHA_SDL2
        )
        
        # Magic sparkles for divine effects
        self.configs[ParticleType.MAGIC_SPARKLES] = ParticleConfig(
            max_particles=100,
            spawn_rate=25.0,
            lifetime=2.5,
            speed=(30.0, 80.0),
            size=(2.0, 5.0),
            color_start=(255, 215, 0, 255),   # Gold
            color_end=(255, 255, 255, 0),     # White, transparent
            gravity=-20.0,  # Float upward
            rotation_speed=180.0,
            blend_mode=pygame.BLEND_ADD
        )
        
        # Divine light for god powers
        self.configs[ParticleType.DIVINE_LIGHT] = ParticleConfig(
            max_particles=80,
            spawn_rate=15.0,
            lifetime=3.0,
            speed=(10.0, 40.0),
            size=(3.0, 8.0),
            color_start=(255, 255, 220, 200), # Warm white
            color_end=(255, 215, 0, 0),       # Gold, transparent
            gravity=-10.0,
            fade_in_time=0.5,
            fade_out_time=1.0,
            blend_mode=pygame.BLEND_ADD
        )
        
        # Golden dust for treasure/reward effects
        self.configs[ParticleType.GOLDEN_DUST] = ParticleConfig(
            max_particles=200,
            spawn_rate=50.0,
            lifetime=3.5,
            speed=(15.0, 45.0),
            size=(1.0, 3.0),
            color_start=(255, 215, 0, 180),   # Gold
            color_end=(184, 134, 11, 0),      # Dark gold, transparent
            gravity=30.0,
            wind_effect=5.0,
            blend_mode=pygame.BLEND_ADD
        )
        
        # Energy wisps for magical effects
        self.configs[ParticleType.ENERGY_WISPS] = ParticleConfig(
            max_particles=60,
            spawn_rate=12.0,
            lifetime=4.0,
            speed=(25.0, 70.0),
            size=(4.0, 10.0),
            color_start=(65, 105, 225, 150),  # Royal blue
            color_end=(0, 191, 255, 0),       # Deep sky blue, transparent
            gravity=-5.0,
            rotation_speed=90.0,
            blend_mode=pygame.BLEND_ADD
        )
        
        # Mystical fog for atmospheric effects
        self.configs[ParticleType.MYSTICAL_FOG] = ParticleConfig(
            max_particles=40,
            spawn_rate=8.0,
            lifetime=6.0,
            speed=(5.0, 20.0),
            size=(15.0, 40.0),
            color_start=(139, 69, 19, 80),    # Sandy brown, low alpha
            color_end=(160, 82, 45, 0),       # Saddle brown, transparent
            gravity=-2.0,
            wind_effect=8.0,
            fade_in_time=1.0,
            fade_out_time=2.0,
            blend_mode=pygame.BLEND_ALPHA_SDL2
        )
        
        # Solar flare for Ra's power
        self.configs[ParticleType.SOLAR_FLARE] = ParticleConfig(
            max_particles=120,
            spawn_rate=40.0,
            lifetime=2.0,
            speed=(50.0, 150.0),
            size=(2.0, 6.0),
            color_start=(255, 69, 0, 255),    # Orange red
            color_end=(255, 215, 0, 0),       # Gold, transparent
            gravity=0.0,
            rotation_speed=360.0,
            blend_mode=pygame.BLEND_ADD
        )
    
    def start_effect(self, effect_type: ParticleType, effect_id: str, 
                    spawn_x: float, spawn_y: float):
        """Start a new particle effect."""
        if effect_id not in self.particle_groups:
            self.particle_groups[effect_id] = []
        
        self.spawn_timers[effect_id] = 0.0
        self.active_effects[effect_id] = True
        
        # Store spawn position for this effect
        setattr(self, f"{effect_id}_spawn_x", spawn_x)
        setattr(self, f"{effect_id}_spawn_y", spawn_y)
        setattr(self, f"{effect_id}_type", effect_type)
    
    def stop_effect(self, effect_id: str):
        """Stop spawning new particles for an effect."""
        if effect_id in self.active_effects:
            self.active_effects[effect_id] = False
    
    def clear_effect(self, effect_id: str):
        """Immediately clear all particles for an effect."""
        if effect_id in self.particle_groups:
            self.particle_groups[effect_id].clear()
        if effect_id in self.active_effects:
            del self.active_effects[effect_id]
        if effect_id in self.spawn_timers:
            del self.spawn_timers[effect_id]
    
    def update(self, dt: float):
        """Update all particle systems."""
        for effect_id, particles in list(self.particle_groups.items()):
            # Update existing particles
            self.particle_groups[effect_id] = [
                particle for particle in particles 
                if particle.update(dt)
            ]
            
            # Spawn new particles if effect is active
            if effect_id in self.active_effects and self.active_effects[effect_id]:
                self._spawn_particles(effect_id, dt)
    
    def _spawn_particles(self, effect_id: str, dt: float):
        """Spawn new particles for an active effect."""
        if not hasattr(self, f"{effect_id}_type"):
            return
        
        effect_type = getattr(self, f"{effect_id}_type")
        config = self.configs.get(effect_type)
        if not config:
            return
        
        # Update spawn timer
        self.spawn_timers[effect_id] += dt
        spawn_interval = 1.0 / config.spawn_rate
        
        # Check if we need to spawn particles
        particles_to_spawn = int(self.spawn_timers[effect_id] / spawn_interval)
        if particles_to_spawn > 0:
            self.spawn_timers[effect_id] -= particles_to_spawn * spawn_interval
            
            # Don't exceed max particles
            current_count = len(self.particle_groups[effect_id])
            particles_to_spawn = min(particles_to_spawn, 
                                   config.max_particles - current_count)
            
            # Spawn particles
            spawn_x = getattr(self, f"{effect_id}_spawn_x", 0)
            spawn_y = getattr(self, f"{effect_id}_spawn_y", 0)
            
            for _ in range(particles_to_spawn):
                # Add slight random offset to spawn position
                x = spawn_x + random.uniform(-10, 10)
                y = spawn_y + random.uniform(-10, 10)
                particle = Particle(x, y, config)
                self.particle_groups[effect_id].append(particle)
    
    def render(self, surface: pygame.Surface):
        """Render all particle effects."""
        for effect_id, particles in self.particle_groups.items():
            for particle in particles:
                particle.render(surface)
    
    def create_card_effect(self, card_name: str, x: float, y: float):
        """Create appropriate particle effect for a specific card."""
        effect_map = {
            "sand_strike": ParticleType.SAND_PARTICLES,
            "ra_solar_flare": ParticleType.SOLAR_FLARE,
            "ankh_blessing": ParticleType.DIVINE_LIGHT,
            "isis_grace": ParticleType.MAGIC_SPARKLES,
            "pharaohs_resurrection": ParticleType.GOLDEN_DUST,
            "thoths_wisdom": ParticleType.ENERGY_WISPS,
            "desert_whisper": ParticleType.MYSTICAL_FOG,
            "scarab_swarm": ParticleType.GOLDEN_DUST,
        }
        
        effect_type = effect_map.get(card_name, ParticleType.MAGIC_SPARKLES)
        effect_id = f"card_{card_name}_{id(self)}"
        
        self.start_effect(effect_type, effect_id, x, y)
        
        # Auto-stop effect after a duration
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)  # 3 seconds
        
        return effect_id
    
    def create_ambient_effect(self, scene_name: str, screen_width: int, screen_height: int):
        """Create ambient particle effects for different game scenes."""
        if scene_name == "combat":
            # Floating sand particles
            self.start_effect(ParticleType.SAND_PARTICLES, "ambient_sand",
                            screen_width / 2, screen_height)
            
            # Mystical fog
            self.start_effect(ParticleType.MYSTICAL_FOG, "ambient_fog",
                            0, screen_height / 2)
        
        elif scene_name == "deck_builder":
            # Floating magical wisps
            self.start_effect(ParticleType.ENERGY_WISPS, "library_wisps",
                            screen_width / 4, screen_height / 3)
            
            # Divine light
            self.start_effect(ParticleType.DIVINE_LIGHT, "divine_light",
                            3 * screen_width / 4, screen_height / 4)
        
        elif scene_name == "menu":
            # Golden dust falling
            self.start_effect(ParticleType.GOLDEN_DUST, "menu_gold",
                            screen_width / 2, 0)
    
    def get_particle_count(self) -> int:
        """Get total number of active particles."""
        return sum(len(particles) for particles in self.particle_groups.values())


# Integration with existing UI systems
class ParticleEffectManager:
    """High-level manager for integrating particle effects into game screens."""
    
    def __init__(self):
        self.particle_system = ParticleSystem()
        self.screen_effects: Dict[str, List[str]] = {}
    
    def setup_screen_effects(self, screen_name: str, screen_width: int, screen_height: int):
        """Setup ambient particle effects for a game screen."""
        # Clear existing effects for this screen
        if screen_name in self.screen_effects:
            for effect_id in self.screen_effects[screen_name]:
                self.particle_system.clear_effect(effect_id)
        
        self.screen_effects[screen_name] = []
        
        # Create ambient effects based on screen type
        self.particle_system.create_ambient_effect(screen_name, screen_width, screen_height)
        
        # Track effects for this screen
        for effect_id in self.particle_system.active_effects:
            if effect_id.startswith("ambient_") or effect_id.startswith(screen_name):
                self.screen_effects[screen_name].append(effect_id)
    
    def trigger_card_effect(self, card_name: str, x: float, y: float) -> str:
        """Trigger particle effect for card play."""
        return self.particle_system.create_card_effect(card_name, x, y)
    
    def update(self, dt: float):
        """Update all particle effects."""
        self.particle_system.update(dt)
    
    def render(self, surface: pygame.Surface):
        """Render all particle effects."""
        self.particle_system.render(surface)
    
    def clear_all_effects(self):
        """Clear all particle effects."""
        for effect_id in list(self.particle_system.particle_groups.keys()):
            self.particle_system.clear_effect(effect_id)
        self.screen_effects.clear()


# Example usage for testing
def test_particle_system():
    """Test the particle system with a simple demonstration."""
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    
    # Initialize particle manager
    particle_manager = ParticleEffectManager()
    particle_manager.setup_screen_effects("combat", 1920, 1080)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create particle effect at mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                particle_manager.trigger_card_effect("ra_solar_flare", mouse_x, mouse_y)
        
        # Update and render
        particle_manager.update(dt)
        
        screen.fill((20, 15, 10))  # Dark background
        particle_manager.render(screen)
        
        # Show particle count
        font = pygame.font.Font(None, 36)
        count_text = font.render(f"Particles: {particle_manager.particle_system.get_particle_count()}", 
                               True, (255, 255, 255))
        screen.blit(count_text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    test_particle_system()