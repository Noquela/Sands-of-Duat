"""
Particle System for Visual Effects

Enhanced particle system for sand effects, combat animations,
and atmospheric elements in the Sands of Duat game.

Features:
- Sand particle effects for Hour-Glass system
- Combat impact particles
- Atmospheric sand dunes and flowing effects
- Performance-optimized particle pools
"""

import pygame
import random
import math
import time
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ParticleType(Enum):
    """Types of particles available."""
    SAND_GRAIN = "sand_grain"
    SAND_FLOW = "sand_flow"
    COMBAT_HIT = "combat_hit"
    HEAL_SPARKLE = "heal_sparkle"
    MAGIC_GLOW = "magic_glow"
    ATMOSPHERIC = "atmospheric"


@dataclass
class Particle:
    """Individual particle with physics and rendering properties."""
    x: float
    y: float
    vel_x: float
    vel_y: float
    size: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    alpha: int
    gravity: float = 0.0
    fade_rate: float = 1.0
    particle_type: ParticleType = ParticleType.SAND_GRAIN
    
    def update(self, delta_time: float) -> bool:
        """Update particle physics. Returns True if particle is still alive."""
        # Update position
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time
        
        # Apply gravity
        self.vel_y += self.gravity * delta_time
        
        # Update life and alpha
        self.life -= delta_time * self.fade_rate
        self.alpha = int(255 * max(0, min(1, self.life / self.max_life)))
        
        return self.life > 0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the particle to the surface."""
        if self.alpha <= 0:
            return
            
        color_with_alpha = (*self.color, self.alpha)
        
        if self.particle_type == ParticleType.SAND_GRAIN:
            # Small sand grain
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))
        
        elif self.particle_type == ParticleType.SAND_FLOW:
            # Flowing sand stream
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size * 1.5)))
        
        elif self.particle_type == ParticleType.COMBAT_HIT:
            # Combat impact spark
            spark_size = int(self.size * 2)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), spark_size)
        
        elif self.particle_type == ParticleType.HEAL_SPARKLE:
            # Healing sparkle effect
            sparkle_size = int(self.size * 1.5)
            # Draw a cross shape for sparkles
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), sparkle_size)
            pygame.draw.line(surface, self.color, 
                           (int(self.x - sparkle_size), int(self.y)), 
                           (int(self.x + sparkle_size), int(self.y)), 2)
            pygame.draw.line(surface, self.color, 
                           (int(self.x), int(self.y - sparkle_size)), 
                           (int(self.x), int(self.y + sparkle_size)), 2)
        
        else:
            # Default circular particle
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, int(self.size)))


class ParticleEmitter:
    """Manages emission of particles with various patterns."""
    
    def __init__(self, x: float, y: float, particle_type: ParticleType = ParticleType.SAND_GRAIN):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.emission_rate = 10.0  # particles per second
        self.emission_timer = 0.0
        self.active = True
        
        # Emission properties
        self.velocity_range = (-50, 50)  # pixels per second
        self.size_range = (1, 3)
        self.life_range = (1.0, 3.0)
        self.color = (255, 215, 0)  # Gold sand color
        self.spread_angle = math.pi / 4  # 45 degrees
        self.direction = math.pi / 2  # Downward
    
    def update(self, delta_time: float) -> List[Particle]:
        """Update emitter and return new particles to spawn."""
        if not self.active:
            return []
        
        new_particles = []
        self.emission_timer += delta_time
        
        # Check if it's time to emit particles
        time_per_particle = 1.0 / self.emission_rate if self.emission_rate > 0 else float('inf')
        
        while self.emission_timer >= time_per_particle:
            self.emission_timer -= time_per_particle
            new_particles.append(self._create_particle())
        
        return new_particles
    
    def _create_particle(self) -> Particle:
        """Create a new particle with randomized properties."""
        # Randomize direction within spread angle
        angle = self.direction + random.uniform(-self.spread_angle/2, self.spread_angle/2)
        speed = random.uniform(*self.velocity_range)
        
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        
        # Random size and life
        size = random.uniform(*self.size_range)
        life = random.uniform(*self.life_range)
        
        # Color variation for sand
        if self.particle_type == ParticleType.SAND_GRAIN:
            # Variations of gold/sand colors
            base_color = self.color
            variation = random.randint(-30, 30)
            color = (
                max(0, min(255, base_color[0] + variation)),
                max(0, min(255, base_color[1] + variation)),
                max(0, min(255, base_color[2] + variation//2))
            )
        else:
            color = self.color
        
        return Particle(
            x=self.x + random.uniform(-5, 5),
            y=self.y + random.uniform(-5, 5),
            vel_x=vel_x,
            vel_y=vel_y,
            size=size,
            life=life,
            max_life=life,
            color=color,
            alpha=255,
            gravity=30.0 if self.particle_type == ParticleType.SAND_GRAIN else 0.0,
            particle_type=self.particle_type
        )
    
    def set_position(self, x: float, y: float) -> None:
        """Update emitter position."""
        self.x = x
        self.y = y
    
    def burst(self, count: int) -> List[Particle]:
        """Create a burst of particles immediately."""
        return [self._create_particle() for _ in range(count)]


class ParticleSystem:
    """
    Main particle system managing all particles and emitters.
    
    Handles updating, rendering, and performance optimization
    of all particle effects in the game.
    """
    
    def __init__(self, max_particles: int = 1000):
        self.particles: List[Particle] = []
        self.emitters: Dict[str, ParticleEmitter] = {}
        self.max_particles = max_particles
        
        # Performance tracking
        self.last_cleanup = time.time()
        self.cleanup_interval = 1.0  # seconds
    
    def add_emitter(self, name: str, emitter: ParticleEmitter) -> None:
        """Add a named emitter to the system."""
        self.emitters[name] = emitter
    
    def remove_emitter(self, name: str) -> None:
        """Remove an emitter by name."""
        if name in self.emitters:
            del self.emitters[name]
    
    def get_emitter(self, name: str) -> Optional[ParticleEmitter]:
        """Get an emitter by name."""
        return self.emitters.get(name)
    
    def create_sand_flow_effect(self, start_x: float, start_y: float, 
                               end_x: float, end_y: float, intensity: float = 1.0) -> None:
        """Create a flowing sand effect between two points."""
        # Calculate flow direction
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return
        
        # Create multiple particles along the flow path
        particle_count = int(distance / 10 * intensity)
        
        for i in range(particle_count):
            t = i / max(1, particle_count - 1)
            x = start_x + dx * t
            y = start_y + dy * t
            
            # Add some randomization
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            
            # Velocity in flow direction
            vel_x = (dx / distance) * random.uniform(20, 60)
            vel_y = (dy / distance) * random.uniform(20, 60)
            
            particle = Particle(
                x=x, y=y,
                vel_x=vel_x, vel_y=vel_y,
                size=random.uniform(1, 2),
                life=random.uniform(0.5, 1.5),
                max_life=1.0,
                color=(255, 215, 0),
                alpha=255,
                gravity=20.0,
                particle_type=ParticleType.SAND_FLOW
            )
            
            self.particles.append(particle)
    
    def create_combat_hit_effect(self, x: float, y: float, damage: int) -> None:
        """Create combat hit particles."""
        particle_count = min(20, max(5, damage // 2))
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            
            particle = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(2, 4),
                life=random.uniform(0.3, 0.8),
                max_life=0.8,
                color=(255, 100, 100),  # Red for damage
                alpha=255,
                gravity=100.0,
                particle_type=ParticleType.COMBAT_HIT
            )
            
            self.particles.append(particle)
    
    def create_heal_effect(self, x: float, y: float, healing: int) -> None:
        """Create healing sparkle particles."""
        particle_count = min(15, max(3, healing // 3))
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 80)
            
            particle = Particle(
                x=x + random.uniform(-15, 15),
                y=y + random.uniform(-15, 15),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed - 30,  # Upward bias
                size=random.uniform(1, 3),
                life=random.uniform(1.0, 2.0),
                max_life=2.0,
                color=(100, 255, 100),  # Green for healing
                alpha=255,
                gravity=-20.0,  # Float upward
                particle_type=ParticleType.HEAL_SPARKLE
            )
            
            self.particles.append(particle)
    
    def update(self, delta_time: float) -> None:
        """Update all particles and emitters."""
        # Update emitters and collect new particles
        new_particles = []
        for emitter in self.emitters.values():
            new_particles.extend(emitter.update(delta_time))
        
        # Add new particles, respecting max limit
        for particle in new_particles:
            if len(self.particles) < self.max_particles:
                self.particles.append(particle)
        
        # Update existing particles
        self.particles = [p for p in self.particles if p.update(delta_time)]
        
        # Periodic cleanup for performance
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_particles()
            self.last_cleanup = current_time
    
    def _cleanup_particles(self) -> None:
        """Remove dead particles and optimize memory."""
        # Remove particles that are off-screen or dead
        screen_margin = 100
        self.particles = [
            p for p in self.particles 
            if (p.life > 0 and 
                -screen_margin < p.x < 4000 and  # Rough screen bounds with margin
                -screen_margin < p.y < 2000)
        ]
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all particles to the surface."""
        for particle in self.particles:
            particle.render(surface)
    
    def get_particle_count(self) -> int:
        """Get current number of active particles."""
        return len(self.particles)
    
    def clear_all(self) -> None:
        """Clear all particles and emitters."""
        self.particles.clear()
        self.emitters.clear()