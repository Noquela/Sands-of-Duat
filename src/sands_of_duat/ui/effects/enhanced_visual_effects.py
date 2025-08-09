"""
Enhanced Visual Effects - SPRINT 8: Final Polish
Professional Egyptian-themed visual effects for ultimate game polish.
"""

import pygame
import math
import random
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER

class EffectType(Enum):
    """Types of visual effects."""
    CARD_GLOW = auto()
    DAMAGE_NUMBERS = auto()
    HEALING_SPARKLES = auto()
    VICTORY_BURST = auto()
    DEFEAT_FADE = auto()
    TRANSITION_WIPE = auto()
    SAND_STORM = auto()
    DIVINE_LIGHT = auto()
    ENERGY_PULSE = auto()
    SCREEN_SHAKE = auto()

@dataclass
class Particle:
    """Individual particle for effects."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: Tuple[int, int, int, int]
    lifetime: float
    max_lifetime: float
    effect_data: Dict[str, Any]

class VisualEffect:
    """Base class for visual effects."""
    
    def __init__(self, effect_type: EffectType, x: float, y: float, duration: float = 1.0):
        self.effect_type = effect_type
        self.x = x
        self.y = y
        self.duration = duration
        self.time = 0.0
        self.active = True
        self.particles: List[Particle] = []
    
    def update(self, dt: float):
        """Update the effect."""
        self.time += dt
        
        if self.time >= self.duration:
            self.active = False
        
        # Update particles
        for particle in self.particles[:]:
            particle.lifetime -= dt
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                continue
            
            # Update position
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt
            
            # Update color alpha based on lifetime
            progress = 1.0 - (particle.lifetime / particle.max_lifetime)
            alpha = int(255 * (1.0 - progress))
            particle.color = (*particle.color[:3], max(0, min(255, alpha)))
    
    def render(self, surface: pygame.Surface):
        """Render the effect."""
        if not self.active:
            return
        
        for particle in self.particles:
            self._render_particle(surface, particle)
    
    def _render_particle(self, surface: pygame.Surface, particle: Particle):
        """Render a single particle."""
        if particle.size <= 0 or particle.color[3] <= 0:
            return
        
        # Create particle surface
        size = max(1, int(particle.size))
        particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, particle.color, (size, size), size)
        
        # Blend particle to screen
        pos = (int(particle.x - size), int(particle.y - size))
        surface.blit(particle_surface, pos, special_flags=pygame.BLEND_ADD)

class CardGlowEffect(VisualEffect):
    """Glowing effect around cards."""
    
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int] = Colors.GOLD):
        super().__init__(EffectType.CARD_GLOW, x, y, 0.5)
        self.width = width
        self.height = height
        self.base_color = color
        self.intensity = 1.0
    
    def render(self, surface: pygame.Surface):
        """Render card glow effect."""
        if not self.active:
            return
        
        # Pulsing glow intensity
        pulse = 0.7 + 0.3 * math.sin(self.time * 8.0)
        alpha = int(80 * pulse * self.intensity)
        
        # Create glow surface
        glow_size = 10
        glow_rect = pygame.Rect(
            self.x - glow_size, self.y - glow_size,
            self.width + glow_size * 2, self.height + glow_size * 2
        )
        
        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        glow_color = (*self.base_color, alpha)
        
        # Multiple glow layers for smooth effect
        for i in range(3):
            layer_alpha = alpha // (i + 1)
            layer_color = (*self.base_color, layer_alpha)
            layer_size = glow_size - i * 2
            
            if layer_size > 0:
                layer_rect = pygame.Rect(
                    layer_size, layer_size,
                    self.width + (glow_size - layer_size) * 2,
                    self.height + (glow_size - layer_size) * 2
                )
                pygame.draw.rect(glow_surface, layer_color, layer_rect, border_radius=5)
        
        surface.blit(glow_surface, glow_rect.topleft, special_flags=pygame.BLEND_ADD)

class DamageNumberEffect(VisualEffect):
    """Floating damage numbers."""
    
    def __init__(self, x: float, y: float, damage: int, is_healing: bool = False):
        super().__init__(EffectType.DAMAGE_NUMBERS, x, y, 1.5)
        self.damage = damage
        self.is_healing = is_healing
        self.font = pygame.font.Font(None, 36)
        self.start_y = y
        
    def render(self, surface: pygame.Surface):
        """Render damage numbers."""
        if not self.active:
            return
        
        # Movement and fade
        progress = self.time / self.duration
        current_y = self.start_y - progress * 60  # Float upward
        alpha = int(255 * (1.0 - progress))
        
        # Color based on type
        color = Colors.GREEN if self.is_healing else Colors.RED
        text_color = (*color, alpha)
        
        # Create text surface
        damage_text = f"+{self.damage}" if self.is_healing else f"-{self.damage}"
        text_surface = self.font.render(damage_text, True, color)
        
        # Add transparency
        text_surface.set_alpha(alpha)
        
        # Scale effect
        scale = 1.0 + progress * 0.5
        if scale != 1.0:
            size = text_surface.get_size()
            new_size = (int(size[0] * scale), int(size[1] * scale))
            text_surface = pygame.transform.scale(text_surface, new_size)
        
        # Render with outline for visibility
        text_rect = text_surface.get_rect(center=(self.x, current_y))
        surface.blit(text_surface, text_rect)

class VictoryBurstEffect(VisualEffect):
    """Burst of particles for victory."""
    
    def __init__(self, x: float, y: float):
        super().__init__(EffectType.VICTORY_BURST, x, y, 3.0)
        self._create_burst_particles()
    
    def _create_burst_particles(self):
        """Create victory burst particles."""
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            
            particle = Particle(
                x=self.x,
                y=self.y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                size=random.uniform(3, 8),
                color=random.choice([Colors.GOLD, Colors.LAPIS_LAZULI, (255, 215, 0, 255)]),
                lifetime=random.uniform(1.5, 3.0),
                max_lifetime=3.0,
                effect_data={}
            )
            
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Update victory burst."""
        super().update(dt)
        
        # Add gravity to particles
        for particle in self.particles:
            particle.vy += 200 * dt  # Gravity
            particle.vx *= 0.98  # Air resistance

class SandStormEffect(VisualEffect):
    """Egyptian sand storm effect."""
    
    def __init__(self):
        super().__init__(EffectType.SAND_STORM, 0, 0, 2.0)
        self._create_sand_particles()
    
    def _create_sand_particles(self):
        """Create sand storm particles."""
        for _ in range(80):
            particle = Particle(
                x=random.uniform(-50, SCREEN_WIDTH + 50),
                y=random.uniform(0, SCREEN_HEIGHT),
                vx=random.uniform(50, 150),
                vy=random.uniform(-20, 20),
                size=random.uniform(1, 3),
                color=(*Colors.DESERT_SAND, random.randint(50, 120)),
                lifetime=random.uniform(1.5, 2.5),
                max_lifetime=2.5,
                effect_data={"wind_speed": random.uniform(0.5, 1.5)}
            )
            
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Update sand storm."""
        super().update(dt)
        
        # Add wind effect
        for particle in self.particles:
            wind_speed = particle.effect_data.get("wind_speed", 1.0)
            particle.vx += math.sin(self.time * 2 + particle.y * 0.01) * 30 * wind_speed * dt
        
        # Wrap particles around screen
        for particle in self.particles:
            if particle.x > SCREEN_WIDTH + 50:
                particle.x = -50
            if particle.x < -50:
                particle.x = SCREEN_WIDTH + 50

class DivineLightEffect(VisualEffect):
    """Divine light rays effect."""
    
    def __init__(self, x: float, y: float):
        super().__init__(EffectType.DIVINE_LIGHT, x, y, 2.0)
        self.rays = []
        
        # Create light rays
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            self.rays.append({
                "angle": angle,
                "length": random.uniform(100, 200),
                "width": random.uniform(2, 6),
                "alpha": random.randint(80, 150)
            })
    
    def render(self, surface: pygame.Surface):
        """Render divine light rays."""
        if not self.active:
            return
        
        # Rotation and pulsing
        rotation = self.time * 30  # Slow rotation
        pulse = 0.7 + 0.3 * math.sin(self.time * 4)
        
        for ray in self.rays:
            angle = ray["angle"] + math.radians(rotation)
            length = ray["length"] * pulse
            
            # Calculate ray end point
            end_x = self.x + math.cos(angle) * length
            end_y = self.y + math.sin(angle) * length
            
            # Draw ray with fading alpha
            progress = self.time / self.duration
            alpha = int(ray["alpha"] * (1.0 - progress * 0.5))
            
            # Create ray surface
            ray_surface = pygame.Surface((length * 2, ray["width"]), pygame.SRCALPHA)
            ray_color = (*Colors.GOLD, alpha)
            ray_rect = pygame.Rect(0, ray["width"] // 2 - 1, length * 2, 2)
            pygame.draw.rect(ray_surface, ray_color, ray_rect)
            
            # Rotate and position ray
            rotated_surface = pygame.transform.rotate(ray_surface, math.degrees(angle))
            ray_rect = rotated_surface.get_rect(center=(self.x, self.y))
            surface.blit(rotated_surface, ray_rect, special_flags=pygame.BLEND_ADD)

class ScreenShakeEffect(VisualEffect):
    """Screen shake effect for impact."""
    
    def __init__(self, intensity: float = 10.0, duration: float = 0.3):
        super().__init__(EffectType.SCREEN_SHAKE, 0, 0, duration)
        self.intensity = intensity
        self.shake_x = 0
        self.shake_y = 0
    
    def update(self, dt: float):
        """Update screen shake."""
        super().update(dt)
        
        if self.active:
            # Decreasing intensity over time
            current_intensity = self.intensity * (1.0 - self.time / self.duration)
            
            self.shake_x = random.uniform(-current_intensity, current_intensity)
            self.shake_y = random.uniform(-current_intensity, current_intensity)
        else:
            self.shake_x = 0
            self.shake_y = 0
    
    def get_shake_offset(self) -> Tuple[float, float]:
        """Get current shake offset."""
        return (self.shake_x, self.shake_y)

class VisualEffectsManager:
    """Manages all visual effects in the game."""
    
    def __init__(self):
        """Initialize the visual effects manager."""
        self.effects: List[VisualEffect] = []
        self.screen_shake: Optional[ScreenShakeEffect] = None
        
        print("Visual Effects Manager initialized - Chamber of Mystical Arts ready")
    
    def add_effect(self, effect: VisualEffect):
        """Add a new visual effect."""
        if effect.effect_type == EffectType.SCREEN_SHAKE:
            self.screen_shake = effect
        else:
            self.effects.append(effect)
    
    def create_card_glow(self, x: float, y: float, width: float, height: float, 
                        color: Tuple[int, int, int] = Colors.GOLD):
        """Create card glow effect."""
        effect = CardGlowEffect(x, y, width, height, color)
        self.add_effect(effect)
        return effect
    
    def create_damage_numbers(self, x: float, y: float, damage: int, is_healing: bool = False):
        """Create floating damage numbers."""
        effect = DamageNumberEffect(x, y, damage, is_healing)
        self.add_effect(effect)
        return effect
    
    def create_victory_burst(self, x: float = None, y: float = None):
        """Create victory celebration effect."""
        if x is None:
            x = SCREEN_CENTER[0]
        if y is None:
            y = SCREEN_CENTER[1]
        
        effect = VictoryBurstEffect(x, y)
        self.add_effect(effect)
        return effect
    
    def create_sand_storm(self):
        """Create sand storm transition effect."""
        effect = SandStormEffect()
        self.add_effect(effect)
        return effect
    
    def create_divine_light(self, x: float, y: float):
        """Create divine light effect."""
        effect = DivineLightEffect(x, y)
        self.add_effect(effect)
        return effect
    
    def create_screen_shake(self, intensity: float = 10.0, duration: float = 0.3):
        """Create screen shake effect."""
        effect = ScreenShakeEffect(intensity, duration)
        self.add_effect(effect)
        return effect
    
    def update(self, dt: float):
        """Update all visual effects."""
        # Update regular effects
        for effect in self.effects[:]:
            effect.update(dt)
            if not effect.active:
                self.effects.remove(effect)
        
        # Update screen shake
        if self.screen_shake:
            self.screen_shake.update(dt)
            if not self.screen_shake.active:
                self.screen_shake = None
    
    def render(self, surface: pygame.Surface):
        """Render all visual effects."""
        # Apply screen shake offset if active
        shake_offset = (0, 0)
        if self.screen_shake:
            shake_offset = self.screen_shake.get_shake_offset()
        
        # Create temporary surface if shaking
        render_surface = surface
        if shake_offset != (0, 0):
            render_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        # Render all effects
        for effect in self.effects:
            effect.render(render_surface)
        
        # Apply shake offset
        if shake_offset != (0, 0):
            surface.blit(render_surface, shake_offset)
    
    def clear_effects(self):
        """Clear all active effects."""
        self.effects.clear()
        self.screen_shake = None
    
    def get_active_effect_count(self) -> int:
        """Get number of active effects."""
        count = len(self.effects)
        if self.screen_shake:
            count += 1
        return count

# Global visual effects manager
visual_effects = VisualEffectsManager()