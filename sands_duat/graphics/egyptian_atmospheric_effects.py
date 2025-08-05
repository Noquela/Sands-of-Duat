"""
Egyptian Atmospheric Effects System

Specialized atmospheric effects for creating an immersive Egyptian underworld experience.
Includes sand storms, mystical energies, floating hieroglyphs, and other thematic effects.
"""

import pygame
import math
import random
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np

from .advanced_particle_system import ParticleSystem, ParticleType, ParticleConfig, get_particle_system
from .performance_optimizer import get_performance_optimizer, optimize_for_performance


class AtmosphericType(Enum):
    """Types of atmospheric effects."""
    DESERT_SANDSTORM = "desert_sandstorm"
    MYSTICAL_ENERGY = "mystical_energy"
    FLOATING_HIEROGLYPHS = "floating_hieroglyphs"
    UNDERWORLD_MIST = "underworld_mist"
    DIVINE_LIGHT_RAYS = "divine_light_rays"
    SCARAB_SWARM = "scarab_swarm"
    ANCIENT_DUST = "ancient_dust"
    ENERGY_RIVERS = "energy_rivers"
    TOMB_FOG = "tomb_fog"
    PAPYRUS_FRAGMENTS = "papyrus_fragments"


@dataclass
class AtmosphericConfig:
    """Configuration for atmospheric effects."""
    effect_type: AtmosphericType
    intensity: float = 0.5  # 0.0 to 1.0
    particle_density: int = 50
    spawn_area: Tuple[int, int, int, int] = (0, 0, 1920, 1080)  # x, y, width, height
    wind_direction: float = 0.0  # radians
    wind_strength: float = 20.0
    color_palette: List[Tuple[int, int, int]] = None
    animation_speed: float = 1.0
    depth_layers: int = 3  # Number of depth layers for parallax


class EgyptianAtmosphericEffect:
    """Base class for Egyptian-themed atmospheric effects."""
    
    def __init__(self, config: AtmosphericConfig):
        self.config = config
        self.particles: List[Dict[str, Any]] = []
        self.time_offset = random.uniform(0, 2 * math.pi)
        self.update_time = 0.0
        self.last_spawn_time = 0.0
        
        # Performance optimization
        self.performance_optimizer = get_performance_optimizer()
        
        # Default color palettes for different effects
        self.color_palettes = {
            AtmosphericType.DESERT_SANDSTORM: [
                (255, 215, 0), (255, 165, 0), (218, 165, 32), (184, 134, 11)
            ],
            AtmosphericType.MYSTICAL_ENERGY: [
                (0, 255, 200), (100, 255, 255), (0, 200, 255), (50, 150, 255)
            ],
            AtmosphericType.FLOATING_HIEROGLYPHS: [
                (255, 215, 0), (255, 140, 0), (139, 117, 93), (101, 67, 33)
            ],
            AtmosphericType.UNDERWORLD_MIST: [
                (100, 100, 120), (80, 80, 100), (60, 60, 80), (40, 40, 60)
            ],
            AtmosphericType.DIVINE_LIGHT_RAYS: [
                (255, 255, 255), (255, 245, 200), (255, 235, 150), (255, 225, 100)
            ]
        }
        
        if not self.config.color_palette:
            self.config.color_palette = self.color_palettes.get(
                self.config.effect_type, 
                [(255, 215, 0), (255, 165, 0)]
            )
    
    def update(self, delta_time: float):
        """Update atmospheric effect."""
        self.update_time += delta_time
        current_time = time.time()
        
        # Update existing particles
        for particle in self.particles[:]:
            if not self._update_particle(particle, delta_time):
                self.particles.remove(particle)
        
        # Spawn new particles based on intensity, density, and performance
        quality_settings = self.performance_optimizer.get_current_settings()
        
        # Adjust spawn rate based on performance settings
        base_spawn_rate = self.config.particle_density * self.config.intensity
        adjusted_spawn_rate = base_spawn_rate * quality_settings.particle_density_scale
        
        if current_time - self.last_spawn_time > 1.0 / max(adjusted_spawn_rate, 1):
            # Limit particle count based on quality settings
            if len(self.particles) < quality_settings.max_particles:
                self._spawn_particles()
            self.last_spawn_time = current_time
    
    def _update_particle(self, particle: Dict[str, Any], delta_time: float) -> bool:
        """Update a single particle. Returns False if particle should be removed."""
        # Update lifetime
        particle['life'] -= delta_time
        if particle['life'] <= 0:
            return False
        
        # Update position with wind effect
        wind_x = math.cos(self.config.wind_direction) * self.config.wind_strength
        wind_y = math.sin(self.config.wind_direction) * self.config.wind_strength
        
        particle['x'] += (particle['vx'] + wind_x) * delta_time
        particle['y'] += (particle['vy'] + wind_y) * delta_time
        
        # Update alpha based on lifecycle
        life_ratio = particle['life'] / particle['max_life']
        if life_ratio > 0.8:
            # Fade in
            particle['alpha'] = int(255 * (1.0 - life_ratio) * 5)
        elif life_ratio < 0.2:
            # Fade out
            particle['alpha'] = int(255 * life_ratio * 5)
        else:
            particle['alpha'] = 255
        
        particle['alpha'] = min(255, max(0, particle['alpha']))
        
        # Update rotation if applicable
        if 'rotation' in particle:
            particle['rotation'] += particle.get('rotation_speed', 0) * delta_time
        
        # Check if particle is still in bounds (with margin for wind effects)
        spawn_area = self.config.spawn_area
        margin = 200
        if (particle['x'] < spawn_area[0] - margin or 
            particle['x'] > spawn_area[0] + spawn_area[2] + margin or
            particle['y'] < spawn_area[1] - margin or 
            particle['y'] > spawn_area[1] + spawn_area[3] + margin):
            return False
        
        return True
    
    def _spawn_particles(self):
        """Spawn new particles."""
        # Implemented by subclasses
        pass
    
    @optimize_for_performance
    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Render atmospheric effect with performance optimization."""
        camera_x, camera_y = camera_offset
        quality_settings = self.performance_optimizer.get_current_settings()
        
        # Skip rendering if atmospheric effects are disabled
        if not quality_settings.atmospheric_effects_enabled:
            return
        
        particles_rendered = 0
        max_particles_to_render = int(len(self.particles) * quality_settings.particle_density_scale)
        
        for particle in self.particles:
            if particles_rendered >= max_particles_to_render:
                break
                
            if particle['alpha'] > 5:
                # Calculate render position with camera offset
                render_x = particle['x'] - camera_x * particle.get('parallax_factor', 1.0)
                render_y = particle['y'] - camera_y * particle.get('parallax_factor', 1.0)
                
                # Skip if outside visible area
                if (render_x < -50 or render_x > surface.get_width() + 50 or
                    render_y < -50 or render_y > surface.get_height() + 50):
                    continue
                
                # Check if should render based on distance and performance
                distance = math.sqrt((render_x - surface.get_width()/2)**2 + (render_y - surface.get_height()/2)**2)
                if self.performance_optimizer.should_render_effect(distance, particle.get('priority', 0.5)):
                    self._render_particle(surface, particle, (int(render_x), int(render_y)))
                    particles_rendered += 1
    
    def _render_particle(self, surface: pygame.Surface, particle: Dict[str, Any], position: Tuple[int, int]):
        """Render a single particle."""
        # Implemented by subclasses
        pass


class DesertSandstormEffect(EgyptianAtmosphericEffect):
    """Desert sandstorm atmospheric effect."""
    
    def _spawn_particles(self):
        """Spawn sand particles."""
        spawn_area = self.config.spawn_area
        num_particles = max(1, int(self.config.intensity * 5))
        
        for _ in range(num_particles):
            # Spawn from upwind side
            if self.config.wind_direction > -math.pi/2 and self.config.wind_direction < math.pi/2:
                # Wind blowing right
                spawn_x = spawn_area[0] - 100
            else:
                # Wind blowing left
                spawn_x = spawn_area[0] + spawn_area[2] + 100
            
            spawn_y = random.uniform(spawn_area[1], spawn_area[1] + spawn_area[3])
            
            color = random.choice(self.config.color_palette)
            
            particle = {
                'x': spawn_x,
                'y': spawn_y,
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-5, 5),
                'size': random.uniform(1, 4),
                'life': random.uniform(8, 15),
                'max_life': 12,
                'alpha': 0,
                'color': color,
                'parallax_factor': random.uniform(0.8, 1.2),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-30, 30)
            }
            self.particles.append(particle)
    
    def _render_particle(self, surface: pygame.Surface, particle: Dict[str, Any], position: Tuple[int, int]):
        """Render sand particle."""
        x, y = position
        size = int(particle['size'])
        color = (*particle['color'], particle['alpha'])
        
        # Create particle surface with alpha
        particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (size, size), size)
        
        # Apply rotation if needed
        if 'rotation' in particle:
            particle_surface = pygame.transform.rotate(particle_surface, particle['rotation'])
        
        # Blit to main surface
        surface.blit(particle_surface, (x - size, y - size), special_flags=pygame.BLEND_ALPHA_SDL2)


class MysticalEnergyEffect(EgyptianAtmosphericEffect):
    """Mystical energy atmospheric effect."""
    
    def _spawn_particles(self):
        """Spawn mystical energy particles."""
        spawn_area = self.config.spawn_area
        num_particles = max(1, int(self.config.intensity * 3))
        
        for _ in range(num_particles):
            spawn_x = random.uniform(spawn_area[0], spawn_area[0] + spawn_area[2])
            spawn_y = random.uniform(spawn_area[1], spawn_area[1] + spawn_area[3])
            
            color = random.choice(self.config.color_palette)
            
            # Energy particles have more complex movement
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            
            particle = {
                'x': spawn_x,
                'y': spawn_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.uniform(3, 8),
                'life': random.uniform(5, 12),
                'max_life': 8,
                'alpha': 0,
                'color': color,
                'parallax_factor': random.uniform(0.6, 1.4),
                'energy_phase': random.uniform(0, 2 * math.pi),
                'pulse_rate': random.uniform(2, 6),
                'trail': []  # Energy trail
            }
            self.particles.append(particle)
    
    def _update_particle(self, particle: Dict[str, Any], delta_time: float) -> bool:
        """Update mystical energy particle with special effects."""
        # Call base update
        if not super()._update_particle(particle, delta_time):
            return False
        
        # Update energy-specific effects
        particle['energy_phase'] += particle['pulse_rate'] * delta_time
        
        # Add to trail
        particle['trail'].append((particle['x'], particle['y'], particle['alpha']))
        
        # Limit trail length
        if len(particle['trail']) > 10:
            particle['trail'].pop(0)
        
        # Add swirling motion
        swirl_strength = 20.0 * math.sin(particle['energy_phase'])
        particle['vx'] += swirl_strength * delta_time
        particle['vy'] += swirl_strength * math.cos(particle['energy_phase']) * delta_time
        
        return True
    
    def _render_particle(self, surface: pygame.Surface, particle: Dict[str, Any], position: Tuple[int, int]):
        """Render mystical energy particle with glow and trail."""
        x, y = position
        
        # Render energy trail
        trail = particle.get('trail', [])
        for i, (trail_x, trail_y, trail_alpha) in enumerate(trail):
            trail_size = int(particle['size'] * (i / len(trail)) * 0.5)
            trail_color = (*particle['color'], max(10, trail_alpha // 3))
            
            if trail_size > 0:
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, trail_color, (trail_size, trail_size), trail_size)
                surface.blit(trail_surface, (int(trail_x) - trail_size, int(trail_y) - trail_size), 
                           special_flags=pygame.BLEND_ADD)
        
        # Render main energy particle with glow
        size = int(particle['size'])
        color = particle['color']
        alpha = particle['alpha']
        
        # Pulsing effect
        pulse = 1.0 + 0.3 * math.sin(particle['energy_phase'])
        glow_size = int(size * pulse)
        
        # Outer glow
        glow_surface = pygame.Surface((glow_size * 3, glow_size * 3), pygame.SRCALPHA)
        glow_color = (*color, alpha // 4)
        pygame.draw.circle(glow_surface, glow_color, (glow_size * 3 // 2, glow_size * 3 // 2), glow_size)
        surface.blit(glow_surface, (x - glow_size * 3 // 2, y - glow_size * 3 // 2), 
                    special_flags=pygame.BLEND_ADD)
        
        # Core particle
        core_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        core_color = (*color, alpha)
        pygame.draw.circle(core_surface, core_color, (size, size), size)
        surface.blit(core_surface, (x - size, y - size), special_flags=pygame.BLEND_ADD)


class FloatingHieroglyphsEffect(EgyptianAtmosphericEffect):
    """Floating hieroglyphs atmospheric effect."""
    
    def __init__(self, config: AtmosphericConfig):
        super().__init__(config)
        # Predefined hieroglyph symbols (simplified)
        self.hieroglyph_symbols = ['𓂀', '𓁹', '𓆓', '𓇋', '𓈖', '𓊪', '𓋴', '𓎡']
    
    def _spawn_particles(self):
        """Spawn hieroglyph particles."""
        spawn_area = self.config.spawn_area
        num_particles = max(1, int(self.config.intensity * 2))
        
        for _ in range(num_particles):
            spawn_x = random.uniform(spawn_area[0], spawn_area[0] + spawn_area[2])
            spawn_y = spawn_area[1] + spawn_area[3] + 50  # Spawn below visible area
            
            color = random.choice(self.config.color_palette)
            symbol = random.choice(self.hieroglyph_symbols)
            
            particle = {
                'x': spawn_x,
                'y': spawn_y,
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(-30, -10),  # Float upward
                'size': random.uniform(20, 40),
                'life': random.uniform(15, 25),
                'max_life': 20,
                'alpha': 0,
                'color': color,
                'parallax_factor': random.uniform(0.3, 0.8),
                'symbol': symbol,
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-10, 10),
                'sway_phase': random.uniform(0, 2 * math.pi),
                'sway_amplitude': random.uniform(5, 15)
            }
            self.particles.append(particle)
    
    def _update_particle(self, particle: Dict[str, Any], delta_time: float) -> bool:
        """Update hieroglyph particle with floating motion."""
        if not super()._update_particle(particle, delta_time):
            return False
        
        # Add swaying motion
        particle['sway_phase'] += delta_time * 2
        sway_offset = math.sin(particle['sway_phase']) * particle['sway_amplitude']
        particle['x'] += sway_offset * delta_time * 0.5
        
        return True
    
    def _render_particle(self, surface: pygame.Surface, particle: Dict[str, Any], position: Tuple[int, int]):
        """Render hieroglyph particle."""
        x, y = position
        size = int(particle['size'])
        color = (*particle['color'], particle['alpha'])
        
        # Create font for hieroglyph (fallback to simple shapes if font not available)
        try:
            font = pygame.font.Font(None, size)
            text_surface = font.render(particle['symbol'], True, color[:3])
            text_surface.set_alpha(particle['alpha'])
            
            # Apply rotation
            if 'rotation' in particle:
                text_surface = pygame.transform.rotate(text_surface, particle['rotation'])
            
            # Center the text
            text_rect = text_surface.get_rect(center=(x, y))
            surface.blit(text_surface, text_rect, special_flags=pygame.BLEND_ALPHA_SDL2)
            
        except:
            # Fallback: draw simple shapes
            shape_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.rect(shape_surface, color, (0, 0, size, size), 2)
            pygame.draw.line(shape_surface, color, (size//4, size//4), (3*size//4, 3*size//4), 2)
            
            if 'rotation' in particle:
                shape_surface = pygame.transform.rotate(shape_surface, particle['rotation'])
            
            surface.blit(shape_surface, (x - size//2, y - size//2), special_flags=pygame.BLEND_ALPHA_SDL2)


class EgyptianAtmosphericManager:
    """Manager for Egyptian atmospheric effects."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.effects: Dict[str, EgyptianAtmosphericEffect] = {}
        self.active_effects: List[str] = []
        
        # Default spawn area (full screen)
        self.default_spawn_area = (0, 0, screen_width, screen_height)
    
    def add_effect(self, name: str, effect_type: AtmosphericType, 
                   intensity: float = 0.5, **kwargs):
        """Add an atmospheric effect."""
        config = AtmosphericConfig(
            effect_type=effect_type,
            intensity=intensity,
            spawn_area=kwargs.get('spawn_area', self.default_spawn_area),
            **{k: v for k, v in kwargs.items() if k != 'spawn_area'}
        )
        
        # Create appropriate effect class
        if effect_type == AtmosphericType.DESERT_SANDSTORM:
            effect = DesertSandstormEffect(config)
        elif effect_type == AtmosphericType.MYSTICAL_ENERGY:
            effect = MysticalEnergyEffect(config)
        elif effect_type == AtmosphericType.FLOATING_HIEROGLYPHS:
            effect = FloatingHieroglyphsEffect(config)
        else:
            # Default to base effect
            effect = EgyptianAtmosphericEffect(config)
        
        self.effects[name] = effect
        if name not in self.active_effects:
            self.active_effects.append(name)
    
    def remove_effect(self, name: str):
        """Remove an atmospheric effect."""
        if name in self.effects:
            del self.effects[name]
        if name in self.active_effects:
            self.active_effects.remove(name)
    
    def set_effect_intensity(self, name: str, intensity: float):
        """Set the intensity of an effect."""
        if name in self.effects:
            self.effects[name].config.intensity = max(0.0, min(1.0, intensity))
    
    def update(self, delta_time: float):
        """Update all active atmospheric effects."""
        for effect_name in self.active_effects:
            if effect_name in self.effects:
                self.effects[effect_name].update(delta_time)
    
    def render(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Render all active atmospheric effects."""
        for effect_name in self.active_effects:
            if effect_name in self.effects:
                self.effects[effect_name].render(surface, camera_offset)
    
    def setup_screen_atmosphere(self, screen_name: str):
        """Setup atmospheric effects for specific screens."""
        # Clear existing effects
        self.effects.clear()
        self.active_effects.clear()
        
        if screen_name == "menu":
            # Desert menu atmosphere
            self.add_effect("desert_wind", AtmosphericType.DESERT_SANDSTORM, 
                          intensity=0.4, wind_direction=0.3, wind_strength=25.0)
            self.add_effect("ancient_dust", AtmosphericType.ANCIENT_DUST, intensity=0.3)
        
        elif screen_name == "combat":
            # Combat atmosphere
            self.add_effect("mystical_energy", AtmosphericType.MYSTICAL_ENERGY, intensity=0.6)
            self.add_effect("tomb_fog", AtmosphericType.TOMB_FOG, intensity=0.4)
            self.add_effect("light_rays", AtmosphericType.DIVINE_LIGHT_RAYS, intensity=0.3)
        
        elif screen_name == "deck_builder":
            # Scholarly chamber atmosphere
            self.add_effect("floating_hieroglyphs", AtmosphericType.FLOATING_HIEROGLYPHS, intensity=0.5)
            self.add_effect("papyrus_fragments", AtmosphericType.PAPYRUS_FRAGMENTS, intensity=0.4)
            self.add_effect("mystical_ink", AtmosphericType.MYSTICAL_ENERGY, intensity=0.3)
        
        elif screen_name == "progression":
            # Underworld map atmosphere
            self.add_effect("energy_rivers", AtmosphericType.ENERGY_RIVERS, intensity=0.7)
            self.add_effect("underworld_mist", AtmosphericType.UNDERWORLD_MIST, intensity=0.5)
            self.add_effect("divine_light", AtmosphericType.DIVINE_LIGHT_RAYS, intensity=0.4)


# Global atmospheric manager
_global_atmospheric_manager = None

def get_atmospheric_manager(screen_width: int = 3440, screen_height: int = 1440) -> EgyptianAtmosphericManager:
    """Get global atmospheric effects manager."""
    global _global_atmospheric_manager
    if _global_atmospheric_manager is None:
        _global_atmospheric_manager = EgyptianAtmosphericManager(screen_width, screen_height)
    return _global_atmospheric_manager