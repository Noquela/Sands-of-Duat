"""
Dynamic Lighting System for Sands of Duat

Advanced lighting effects that enhance AI-generated backgrounds and sprites
with realistic lighting, shadows, and atmospheric effects.
"""

import pygame
import math
import random
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
from dataclasses import dataclass
import logging


class LightType(Enum):
    """Types of light sources"""
    POINT = "point"          # Point light source (torch, orb)
    DIRECTIONAL = "directional"  # Directional light (sunlight, moonlight)
    AMBIENT = "ambient"      # Ambient lighting
    SPOT = "spot"           # Spotlight with cone
    AREA = "area"           # Area light source


@dataclass
class Light:
    """Individual light source"""
    x: float
    y: float
    color: Tuple[int, int, int]
    intensity: float
    radius: float
    light_type: LightType
    angle: float = 0.0          # For directional/spot lights
    cone_angle: float = 45.0    # For spot lights
    flicker_intensity: float = 0.0  # 0-1 flicker amount
    flicker_speed: float = 1.0      # Flicker frequency
    enabled: bool = True
    
    # Animation properties
    pulse_speed: float = 0.0    # 0 = no pulse
    pulse_amplitude: float = 0.2  # How much intensity varies
    
    # Internal state
    _flicker_time: float = 0.0
    _pulse_time: float = 0.0


class ParticleSystem:
    """Enhanced particle system for atmospheric effects"""
    
    def __init__(self):
        self.particles: List[Dict[str, Any]] = []
        self.max_particles = 500
        
    def add_dust_motes(self, x: int, y: int, count: int = 20, area_radius: int = 100) -> None:
        """Add floating dust motes in a light beam"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, area_radius)
            
            particle = {
                'x': x + math.cos(angle) * distance,
                'y': y + math.sin(angle) * distance,
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(-5, 5),
                'size': random.uniform(1, 3),
                'life': random.uniform(5, 10),
                'max_life': random.uniform(5, 10),
                'color': (255, 248, 220),  # Warm dust color
                'type': 'dust_mote',
                'float_amplitude': random.uniform(5, 15),
                'float_speed': random.uniform(0.5, 2.0),
                'float_time': random.uniform(0, 2 * math.pi)
            }
            particle['max_life'] = particle['life']
            self.particles.append(particle)
    
    def add_magical_sparkles(self, x: int, y: int, count: int = 15, color: Tuple[int, int, int] = (255, 215, 0)) -> None:
        """Add magical sparkle particles"""
        for _ in range(count):
            particle = {
                'x': x + random.uniform(-20, 20),
                'y': y + random.uniform(-20, 20),
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-30, 30),
                'size': random.uniform(2, 4),
                'life': random.uniform(1, 3),
                'max_life': random.uniform(1, 3),
                'color': color,
                'type': 'sparkle',
                'twinkle_speed': random.uniform(2, 5),
                'twinkle_time': random.uniform(0, 2 * math.pi)
            }
            particle['max_life'] = particle['life']
            self.particles.append(particle)
    
    def update(self, delta_time: float) -> None:
        """Update all particles"""
        for particle in self.particles[:]:
            particle['life'] -= delta_time
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            
            # Update particle-specific behaviors
            if particle['type'] == 'dust_mote':
                # Floating motion
                particle['float_time'] += particle['float_speed'] * delta_time
                particle['y'] += math.sin(particle['float_time']) * particle['float_amplitude'] * delta_time
                
                # Gravity effect
                particle['vy'] += 5 * delta_time
                
            elif particle['type'] == 'sparkle':
                # Twinkling effect
                particle['twinkle_time'] += particle['twinkle_speed'] * delta_time
                
                # Fade out
                particle['vy'] -= 20 * delta_time  # Float upward
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Limit particle count
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
    
    def render(self, surface: pygame.Surface, lighting_surface: pygame.Surface = None) -> None:
        """Render particles with lighting effects"""
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = int(255 * (particle['life'] / particle['max_life']))
                
                if particle['type'] == 'sparkle':
                    # Twinkling sparkles
                    twinkle = (math.sin(particle['twinkle_time']) + 1) / 2
                    alpha = int(alpha * (0.3 + 0.7 * twinkle))
                
                if alpha > 0:
                    color = (*particle['color'], alpha)
                    size = int(particle['size'])
                    
                    if size > 0:
                        try:
                            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                            pygame.draw.circle(particle_surface, color, (size, size), size)
                            surface.blit(particle_surface, (int(particle['x'] - size), int(particle['y'] - size)))
                        except:
                            pass


class LightingSystem:
    """Main lighting system for dynamic effects"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lights: List[Light] = []
        self.particle_system = ParticleSystem()
        self.logger = logging.getLogger(__name__)
        
        # Lighting surfaces
        self.lighting_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.shadow_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        
        # Ambient lighting
        self.ambient_color = (40, 35, 50)  # Dark purple night
        self.ambient_intensity = 0.3
        
        # Performance settings
        self.light_quality = "medium"  # low, medium, high
        self.enable_shadows = True
        self.enable_particles = True
        
    def add_light(self, light: Light) -> None:
        """Add a light source"""
        self.lights.append(light)
        self.logger.debug(f"Added {light.light_type.value} light at ({light.x}, {light.y})")
    
    def remove_light(self, light: Light) -> None:
        """Remove a light source"""
        if light in self.lights:
            self.lights.remove(light)
    
    def clear_lights(self) -> None:
        """Remove all lights"""
        self.lights.clear()
    
    def create_torch_light(self, x: int, y: int, flicker: bool = True) -> Light:
        """Create a flickering torch light"""
        light = Light(
            x=x, y=y,
            color=(255, 147, 41),  # Warm orange
            intensity=0.8,
            radius=150,
            light_type=LightType.POINT,
            flicker_intensity=0.3 if flicker else 0.0,
            flicker_speed=3.0,
            pulse_speed=1.5,
            pulse_amplitude=0.2
        )
        self.add_light(light)
        return light
    
    def create_magical_orb(self, x: int, y: int, color: Tuple[int, int, int] = (100, 200, 255)) -> Light:
        """Create a magical orb light"""
        light = Light(
            x=x, y=y,
            color=color,
            intensity=0.6,
            radius=120,
            light_type=LightType.POINT,
            pulse_speed=2.0,
            pulse_amplitude=0.3
        )
        self.add_light(light)
        
        # Add magical sparkles
        if self.enable_particles:
            self.particle_system.add_magical_sparkles(x, y, 10, color)
        
        return light
    
    def create_moonlight(self, angle: float = -45.0) -> Light:
        """Create directional moonlight"""
        light = Light(
            x=self.screen_width // 2,
            y=0,
            color=(200, 200, 255),  # Cool blue-white
            intensity=0.4,
            radius=max(self.screen_width, self.screen_height),
            light_type=LightType.DIRECTIONAL,
            angle=math.radians(angle)
        )
        self.add_light(light)
        return light
    
    def create_combat_lighting(self, player_x: int, player_y: int, enemy_x: int, enemy_y: int) -> None:
        """Create dramatic combat lighting"""
        # Player area light (warm)
        self.create_torch_light(player_x - 100, player_y - 50, flicker=True)
        
        # Enemy area light (cool/menacing)
        enemy_light = Light(
            x=enemy_x + 100, y=enemy_y - 50,
            color=(150, 100, 200),  # Purple
            intensity=0.7,
            radius=140,
            light_type=LightType.POINT,
            flicker_intensity=0.4,
            flicker_speed=2.0
        )
        self.add_light(enemy_light)
        
        # Central dramatic lighting
        center_x = (player_x + enemy_x) // 2
        center_y = (player_y + enemy_y) // 2
        self.create_magical_orb(center_x, center_y - 150, (255, 215, 0))  # Golden light above
    
    def update(self, delta_time: float) -> None:
        """Update lighting system"""
        # Update light animations
        for light in self.lights:
            if light.enabled:
                # Update flicker
                if light.flicker_intensity > 0:
                    light._flicker_time += light.flicker_speed * delta_time
                
                # Update pulse
                if light.pulse_speed > 0:
                    light._pulse_time += light.pulse_speed * delta_time
        
        # Update particles
        if self.enable_particles:
            self.particle_system.update(delta_time)
    
    def render_lighting(self, target_surface: pygame.Surface) -> None:
        """Render lighting effects to target surface"""
        # Clear lighting surface
        self.lighting_surface.fill((0, 0, 0, 0))
        
        # Apply ambient lighting
        ambient_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        ambient_alpha = int(255 * self.ambient_intensity)
        ambient_surface.fill((*self.ambient_color, ambient_alpha))
        self.lighting_surface.blit(ambient_surface, (0, 0))
        
        # Render each light
        for light in self.lights:
            if light.enabled:
                self._render_light(light)
        
        # Apply lighting to target surface
        target_surface.blit(self.lighting_surface, (0, 0), special_flags=pygame.BLEND_MULTIPLY)
        
        # Render particles on top
        if self.enable_particles:
            self.particle_system.render(target_surface, self.lighting_surface)
    
    def _render_light(self, light: Light) -> None:
        """Render individual light source"""
        # Calculate current intensity with animations
        current_intensity = light.intensity
        
        # Apply pulse
        if light.pulse_speed > 0:
            pulse_factor = math.sin(light._pulse_time) * light.pulse_amplitude
            current_intensity *= (1.0 + pulse_factor)
        
        # Apply flicker
        if light.flicker_intensity > 0:
            flicker_factor = (math.sin(light._flicker_time * 3) + 
                            math.sin(light._flicker_time * 7) * 0.5) / 1.5
            flicker_amount = light.flicker_intensity * flicker_factor
            current_intensity *= (1.0 + flicker_amount)
        
        current_intensity = max(0.0, min(1.0, current_intensity))
        
        if current_intensity <= 0:
            return
        
        # Render based on light type
        if light.light_type == LightType.POINT:
            self._render_point_light(light, current_intensity)
        elif light.light_type == LightType.DIRECTIONAL:
            self._render_directional_light(light, current_intensity)
        elif light.light_type == LightType.SPOT:
            self._render_spot_light(light, current_intensity)
    
    def _render_point_light(self, light: Light, intensity: float) -> None:
        """Render point light source"""
        if light.radius <= 0:
            return
        
        # Create light gradient
        light_surface = pygame.Surface((int(light.radius * 2), int(light.radius * 2)), pygame.SRCALPHA)
        
        # Quality-based rendering
        if self.light_quality == "high":
            steps = 32
        elif self.light_quality == "medium":
            steps = 16
        else:
            steps = 8
        
        # Draw concentric circles for smooth gradient
        for i in range(steps):
            radius_factor = (steps - i) / steps
            current_radius = int(light.radius * radius_factor)
            alpha = int(255 * intensity * radius_factor * radius_factor)  # Quadratic falloff
            
            if alpha > 0 and current_radius > 0:
                color = (*light.color, alpha)
                pygame.draw.circle(light_surface, color, 
                                 (int(light.radius), int(light.radius)), current_radius)
        
        # Blit to lighting surface
        light_rect = light_surface.get_rect(center=(int(light.x), int(light.y)))
        self.lighting_surface.blit(light_surface, light_rect, special_flags=pygame.BLEND_ADD)
    
    def _render_directional_light(self, light: Light, intensity: float) -> None:
        """Render directional light (moonlight, sunlight)"""
        # Create directional light effect
        alpha = int(255 * intensity)
        color = (*light.color, alpha)
        
        # Simple directional light as overlay
        directional_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        directional_surface.fill(color)
        
        self.lighting_surface.blit(directional_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def _render_spot_light(self, light: Light, intensity: float) -> None:
        """Render spot light with cone"""
        # For now, render as point light
        # Full implementation would create cone-shaped light
        self._render_point_light(light, intensity)
    
    def set_ambient_lighting(self, color: Tuple[int, int, int], intensity: float) -> None:
        """Set ambient lighting color and intensity"""
        self.ambient_color = color
        self.ambient_intensity = max(0.0, min(1.0, intensity))
    
    def transition_ambient_lighting(self, target_color: Tuple[int, int, int], 
                                  target_intensity: float, duration: float) -> None:
        """Smoothly transition ambient lighting (simplified implementation)"""
        self.set_ambient_lighting(target_color, target_intensity)
    
    def create_hour_lighting(self, hour: int) -> None:
        """Create lighting appropriate for the hour of night"""
        self.clear_lights()
        
        if hour <= 3:
            # Early night
            self.set_ambient_lighting((30, 20, 60), 0.2)  # Deep purple
            self.create_moonlight(-30)
        elif hour <= 6:
            # Deep night
            self.set_ambient_lighting((15, 15, 40), 0.1)  # Very dark blue
            self.create_moonlight(-45)
        elif hour <= 9:
            # Late night
            self.set_ambient_lighting((20, 15, 30), 0.15)  # Dark purple-brown
            self.create_moonlight(-60)
        else:
            # Pre-dawn
            self.set_ambient_lighting((40, 30, 20), 0.25)  # Warm brown
            self.create_moonlight(-75)


# Global lighting system
_global_lighting_system = None

def get_lighting_system(screen_width: int = 3440, screen_height: int = 1440) -> LightingSystem:
    """Get global lighting system"""
    global _global_lighting_system
    if _global_lighting_system is None:
        _global_lighting_system = LightingSystem(screen_width, screen_height)
    return _global_lighting_system

def create_lighting_for_screen(screen_name: str, context: Dict[str, Any] = None) -> None:
    """Create appropriate lighting for a screen"""
    lighting = get_lighting_system()
    lighting.clear_lights()
    
    context = context or {}
    
    if screen_name == "combat":
        # Dramatic combat lighting
        if "player_pos" in context and "enemy_pos" in context:
            player_x, player_y = context["player_pos"]
            enemy_x, enemy_y = context["enemy_pos"]
            lighting.create_combat_lighting(player_x, player_y, enemy_x, enemy_y)
        else:
            # Default combat lighting
            lighting.create_combat_lighting(600, 400, 1200, 400)
    
    elif screen_name == "menu":
        # Atmospheric menu lighting
        lighting.set_ambient_lighting((50, 40, 30), 0.4)
        lighting.create_torch_light(200, 300, True)
        lighting.create_torch_light(1200, 300, True)
    
    elif screen_name == "map":
        # Map lighting based on hour
        hour = context.get("hour", 1)
        lighting.create_hour_lighting(hour)
    
    else:
        # Default atmospheric lighting
        lighting.set_ambient_lighting((40, 35, 30), 0.3)
        lighting.create_moonlight()