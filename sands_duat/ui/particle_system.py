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
import colorsys
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class ParticleType(Enum):
    """Types of particles available."""
    SAND_GRAIN = "sand_grain"
    SAND_FLOW = "sand_flow"
    COMBAT_HIT = "combat_hit"
    HEAL_SPARKLE = "heal_sparkle"
    MAGIC_GLOW = "magic_glow"
    ATMOSPHERIC = "atmospheric"
    
    # Card-specific particle types
    FIRE_SPARK = "fire_spark"        # Attack cards - fire effects
    LIGHTNING_BOLT = "lightning_bolt" # Skill cards - blue lightning
    GOLDEN_AURA = "golden_aura"      # Power cards - golden energy
    MYSTICAL_RUNE = "mystical_rune"  # Status cards - purple magic
    
    # Enhanced effects
    EMBER_TRAIL = "ember_trail"      # Trailing fire particles
    ENERGY_ORB = "energy_orb"        # Floating energy spheres
    SAND_SPIRAL = "sand_spiral"      # Swirling sand patterns
    
    # Egyptian mystical effects
    ANKH_GLOW = "ankh_glow"          # Ankh symbol with divine energy
    HIEROGLYPH_MAGIC = "hieroglyph_magic"  # Glowing hieroglyphs
    MUMMY_BANDAGES = "mummy_bandages"      # Floating mummy wrappings
    SCARAB_SWARM = "scarab_swarm"          # Flying scarab beetles
    PYRAMID_ENERGY = "pyramid_energy"      # Triangular energy beams
    CANOPIC_MIST = "canopic_mist"          # Ethereal preservation mist
    DESERT_MIRAGE = "desert_mirage"        # Heat shimmer effects
    PAPYRUS_SCROLL = "papyrus_scroll"      # Floating papyrus fragments
    PHARAOH_CROWN = "pharaoh_crown"        # Golden pharaoh energy
    UNDERWORLD_FLAME = "underworld_flame"  # Blue-green underworld fire
    
    # Atmospheric cinematic effects
    DUST_MOTE = "dust_mote"               # Floating dust in light beams
    TORCH_FLICKER = "torch_flicker"       # Torch flame particles
    SPIRIT_WISP = "spirit_wisp"           # Ghostly spirit particles
    SHADOW_TENDRIL = "shadow_tendril"     # Dark shadow effects
    CRYSTAL_SPARKLE = "crystal_sparkle"   # Crystalline light effects


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
    
    # Enhanced properties for cinematic effects
    rotation: float = 0.0
    rotation_speed: float = 0.0
    scale: float = 1.0
    scale_speed: float = 0.0
    pulse_frequency: float = 0.0
    pulse_amplitude: float = 0.0
    trail_length: int = 0
    trail_positions: List[Tuple[float, float]] = field(default_factory=list)
    custom_data: Dict[str, Any] = field(default_factory=dict)
    update_function: Optional[Callable] = None
    
    def update(self, delta_time: float) -> bool:
        """Update particle physics. Returns True if particle is still alive."""
        # Store previous position for trails
        if self.trail_length > 0:
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > self.trail_length:
                self.trail_positions.pop(0)
        
        # Update position
        self.x += self.vel_x * delta_time
        self.y += self.vel_y * delta_time
        
        # Apply gravity
        self.vel_y += self.gravity * delta_time
        
        # Update rotation
        self.rotation += self.rotation_speed * delta_time
        
        # Update scale
        self.scale += self.scale_speed * delta_time
        
        # Update life and alpha
        self.life -= delta_time * self.fade_rate
        life_ratio = max(0, min(1, self.life / self.max_life))
        
        # Apply pulse effect to alpha
        if self.pulse_frequency > 0:
            pulse = math.sin(time.time() * self.pulse_frequency) * self.pulse_amplitude
            life_ratio = max(0, min(1, life_ratio + pulse))
        
        self.alpha = int(255 * life_ratio)
        
        # Custom update function
        if self.update_function:
            self.update_function(self, delta_time)
        
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
        
        elif self.particle_type == ParticleType.FIRE_SPARK:
            # Fire spark for attack cards
            spark_size = int(self.size * 1.8)
            # Draw flame-like shape with gradient effect
            center_color = self.color
            outer_color = tuple(max(0, c - 50) for c in self.color)
            
            pygame.draw.circle(surface, outer_color, (int(self.x), int(self.y)), spark_size)
            pygame.draw.circle(surface, center_color, (int(self.x), int(self.y)), max(1, spark_size // 2))
        
        elif self.particle_type == ParticleType.LIGHTNING_BOLT:
            # Lightning effect for skill cards
            bolt_length = int(self.size * 3)
            # Draw jagged lightning bolt
            points = [
                (int(self.x), int(self.y - bolt_length)),
                (int(self.x + bolt_length//3), int(self.y - bolt_length//2)),
                (int(self.x - bolt_length//3), int(self.y)),
                (int(self.x + bolt_length//2), int(self.y + bolt_length//2))
            ]
            if len(points) >= 2:
                pygame.draw.lines(surface, self.color, False, points, 2)
        
        elif self.particle_type == ParticleType.GOLDEN_AURA:
            # Golden aura for power cards
            aura_size = int(self.size * 2)
            # Draw layered golden circles for aura effect
            for i in range(3):
                size = aura_size - i * 2
                alpha_mod = self.alpha - i * 30
                if size > 0 and alpha_mod > 0:
                    aura_color = tuple(min(255, c + i * 20) for c in self.color)
                    pygame.draw.circle(surface, aura_color, (int(self.x), int(self.y)), size, 1)
        
        elif self.particle_type == ParticleType.MYSTICAL_RUNE:
            # Mystical rune for status cards
            rune_size = int(self.size * 2)
            # Draw rune-like symbol
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), rune_size, 2)
            # Add inner pattern
            inner_size = rune_size // 2
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), inner_size)
        
        elif self.particle_type == ParticleType.EMBER_TRAIL:
            # Trailing ember particles
            trail_length = int(self.size * 4)
            # Draw fading trail behind particle
            trail_color = tuple(c // 2 for c in self.color)
            pygame.draw.line(surface, trail_color, 
                           (int(self.x - self.vel_x * 0.1), int(self.y - self.vel_y * 0.1)),
                           (int(self.x), int(self.y)), max(1, int(self.size)))
        
        elif self.particle_type == ParticleType.ENERGY_ORB:
            # Floating energy orb
            orb_size = int(self.size * 1.5)
            # Draw pulsing orb with glow
            pulse = math.sin(time.time() * 5) * 0.3 + 0.7  # Pulsing effect
            current_size = int(orb_size * pulse)
            
            # Outer glow
            glow_color = tuple(min(255, c + 30) for c in self.color)
            pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), current_size + 2)
            # Inner orb
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), current_size)
        
        elif self.particle_type == ParticleType.SAND_SPIRAL:
            # Swirling sand pattern
            spiral_time = time.time() * 3 + self.x * 0.01  # Offset by position
            spiral_radius = self.size * 2
            
            # Draw spiral points
            for i in range(5):
                angle = spiral_time + i * math.pi / 2.5
                offset_x = math.cos(angle) * spiral_radius
                offset_y = math.sin(angle) * spiral_radius
                
                point_x = int(self.x + offset_x)
                point_y = int(self.y + offset_y)
                pygame.draw.circle(surface, self.color, (point_x, point_y), max(1, int(self.size // 2)))
        
        elif self.particle_type == ParticleType.ANKH_GLOW:
            # Ankh symbol with divine energy
            size = int(self.size * self.scale)
            # Draw ankh shape with glowing effect
            center_x, center_y = int(self.x), int(self.y)
            
            # Cross part
            pygame.draw.line(surface, self.color, 
                           (center_x, center_y - size), (center_x, center_y + size), 3)
            pygame.draw.line(surface, self.color, 
                           (center_x - size//2, center_y - size//3), 
                           (center_x + size//2, center_y - size//3), 3)
            
            # Loop part
            loop_radius = size // 3
            pygame.draw.circle(surface, self.color, (center_x, center_y - size//2), loop_radius, 2)
            
            # Glow effect
            glow_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(surface, glow_color, (center_x, center_y), size + 5, 1)
        
        elif self.particle_type == ParticleType.HIEROGLYPH_MAGIC:
            # Glowing hieroglyphs
            size = int(self.size * self.scale)
            center_x, center_y = int(self.x), int(self.y)
            
            # Draw simplified hieroglyph pattern
            points = [
                (center_x - size, center_y - size),
                (center_x, center_y - size//2),
                (center_x + size, center_y),
                (center_x, center_y + size),
                (center_x - size//2, center_y + size//2)
            ]
            
            if len(points) >= 2:
                pygame.draw.lines(surface, self.color, False, points, 2)
            
            # Add mystical glow
            pulse = math.sin(time.time() * 4 + self.x * 0.1) * 0.3 + 0.7
            glow_alpha = int(self.alpha * pulse * 0.5)
            if glow_alpha > 0:
                glow_color = (*self.color, glow_alpha)
                pygame.draw.circle(surface, self.color, (center_x, center_y), size + 3, 1)
        
        elif self.particle_type == ParticleType.SCARAB_SWARM:
            # Flying scarab beetles
            size = int(self.size * self.scale)
            center_x, center_y = int(self.x), int(self.y)
            
            # Wing animation based on velocity
            wing_angle = math.sin(time.time() * 10 + self.x * 0.1) * 0.3
            
            # Body
            pygame.draw.ellipse(surface, self.color, 
                              (center_x - size//2, center_y - size//3, size, size//2))
            
            # Wings
            wing_color = tuple(c // 2 for c in self.color)
            wing_points_left = [
                (center_x - size//4, center_y),
                (center_x - size + int(wing_angle * size), center_y - size//2),
                (center_x - size//2, center_y + size//4)
            ]
            wing_points_right = [
                (center_x + size//4, center_y),
                (center_x + size - int(wing_angle * size), center_y - size//2),
                (center_x + size//2, center_y + size//4)
            ]
            
            if len(wing_points_left) >= 3:
                pygame.draw.polygon(surface, wing_color, wing_points_left)
            if len(wing_points_right) >= 3:
                pygame.draw.polygon(surface, wing_color, wing_points_right)
        
        elif self.particle_type == ParticleType.PYRAMID_ENERGY:
            # Triangular energy beams
            size = int(self.size * self.scale)
            center_x, center_y = int(self.x), int(self.y)
            
            # Draw energy pyramid/triangle
            points = [
                (center_x, center_y - size),
                (center_x - size, center_y + size),
                (center_x + size, center_y + size)
            ]
            
            # Inner bright triangle
            pygame.draw.polygon(surface, self.color, points)
            
            # Outer glow
            glow_color = tuple(min(255, c + 30) for c in self.color)
            pygame.draw.polygon(surface, glow_color, points, 2)
        
        elif self.particle_type == ParticleType.UNDERWORLD_FLAME:
            # Blue-green underworld fire
            size = int(self.size * self.scale)
            center_x, center_y = int(self.x), int(self.y)
            
            # Flame flicker
            flicker = math.sin(time.time() * 8 + self.x * 0.1) * 0.2 + 0.8
            flame_height = int(size * flicker * 2)
            
            # Multiple flame layers for depth
            for i in range(3):
                layer_size = size - i
                layer_height = flame_height - i * 2
                if layer_size > 0 and layer_height > 0:
                    layer_alpha = self.alpha - i * 30
                    if layer_alpha > 0:
                        # Create flame shape
                        flame_points = [
                            (center_x, center_y - layer_height),
                            (center_x - layer_size//2, center_y - layer_height//2),
                            (center_x - layer_size, center_y),
                            (center_x + layer_size, center_y),
                            (center_x + layer_size//2, center_y - layer_height//2)
                        ]
                        
                        # Vary color for each layer
                        layer_color = (
                            max(0, self.color[0] - i * 20),
                            min(255, self.color[1] + i * 10),
                            min(255, self.color[2] + i * 30)
                        )
                        
                        if len(flame_points) >= 3:
                            pygame.draw.polygon(surface, layer_color, flame_points)
        
        elif self.particle_type == ParticleType.DUST_MOTE:
            # Floating dust in light beams
            size = max(1, int(self.size * self.scale))
            # Simple dust particle with subtle movement
            float_offset = math.sin(time.time() * 2 + self.x * 0.01) * 2
            pygame.draw.circle(surface, self.color, 
                             (int(self.x + float_offset), int(self.y)), size)
        
        elif self.particle_type == ParticleType.SPIRIT_WISP:
            # Ghostly spirit particles
            size = int(self.size * self.scale)
            center_x, center_y = int(self.x), int(self.y)
            
            # Wispy trail effect
            if self.trail_positions:
                for i, (trail_x, trail_y) in enumerate(self.trail_positions):
                    trail_alpha = int(self.alpha * (i + 1) / len(self.trail_positions) * 0.3)
                    if trail_alpha > 0:
                        trail_size = max(1, size - (len(self.trail_positions) - i))
                        pygame.draw.circle(surface, self.color, 
                                         (int(trail_x), int(trail_y)), trail_size)
            
            # Main wisp
            pygame.draw.circle(surface, self.color, (center_x, center_y), size)
            
            # Ethereal glow
            glow_size = size + 3
            glow_alpha = max(0, self.alpha // 3)
            if glow_alpha > 0:
                glow_color = tuple(min(255, c + 20) for c in self.color)
                pygame.draw.circle(surface, glow_color, (center_x, center_y), glow_size, 1)
        
        else:
            # Default circular particle with enhanced rendering
            size = max(1, int(self.size * self.scale))
            center_x, center_y = int(self.x), int(self.y)
            
            # Draw trail if enabled
            if self.trail_positions:
                for i, (trail_x, trail_y) in enumerate(self.trail_positions):
                    trail_alpha = int(self.alpha * (i + 1) / len(self.trail_positions) * 0.5)
                    if trail_alpha > 0:
                        trail_size = max(1, size - (len(self.trail_positions) - i))
                        trail_color = tuple(c // 2 for c in self.color)
                        pygame.draw.circle(surface, trail_color, 
                                         (int(trail_x), int(trail_y)), trail_size)
            
            # Main particle
            pygame.draw.circle(surface, self.color, (center_x, center_y), size)


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
    
    def create_attack_card_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create fire particle effects for attack cards."""
        particle_count = int(15 * intensity)
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 100) * intensity
            
            particle = Particle(
                x=x + random.uniform(-8, 8),
                y=y + random.uniform(-8, 8),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(2, 5),
                life=random.uniform(0.8, 1.5),
                max_life=1.2,
                color=(255, 100, 50),  # Orange-red fire
                alpha=255,
                gravity=20.0,
                particle_type=ParticleType.FIRE_SPARK
            )
            
            self.particles.append(particle)
    
    def create_skill_card_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create lightning particle effects for skill cards."""
        particle_count = int(12 * intensity)
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 120) * intensity
            
            particle = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(1, 3),
                life=random.uniform(0.5, 1.0),
                max_life=0.8,
                color=(100, 150, 255),  # Blue lightning
                alpha=255,
                gravity=0.0,  # Lightning floats
                particle_type=ParticleType.LIGHTNING_BOLT
            )
            
            self.particles.append(particle)
    
    def create_power_card_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create golden aura effects for power cards."""
        particle_count = int(18 * intensity)
        
        for _ in range(particle_count):
            # Create expanding aura pattern
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(10, 40) * intensity
            
            particle = Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(2, 4),
                life=random.uniform(1.5, 2.5),
                max_life=2.0,
                color=(255, 215, 0),  # Golden
                alpha=255,
                gravity=-5.0,  # Slight upward float
                particle_type=ParticleType.GOLDEN_AURA
            )
            
            self.particles.append(particle)
    
    def create_status_card_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create mystical rune effects for status cards."""
        particle_count = int(10 * intensity)
        
        for _ in range(particle_count):
            # Create mystical swirling pattern
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60) * intensity
            
            particle = Particle(
                x=x + random.uniform(-12, 12),
                y=y + random.uniform(-12, 12),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(3, 6),
                life=random.uniform(1.0, 2.0),
                max_life=1.5,
                color=(150, 50, 200),  # Purple mystical
                alpha=255,
                gravity=0.0,
                particle_type=ParticleType.MYSTICAL_RUNE
            )
            
            self.particles.append(particle)
    
    def create_card_type_effect(self, card_type: str, x: float, y: float, intensity: float = 1.0) -> None:
        """Create appropriate particle effect based on card type."""
        card_type_lower = card_type.lower()
        
        if card_type_lower == "attack":
            self.create_attack_card_effect(x, y, intensity)
        elif card_type_lower == "skill":
            self.create_skill_card_effect(x, y, intensity)
        elif card_type_lower == "power":
            self.create_power_card_effect(x, y, intensity)
        elif card_type_lower in ["status", "curse", "blessing"]:
            self.create_status_card_effect(x, y, intensity)
        else:
            # Default effect
            self.create_attack_card_effect(x, y, intensity)
    
    def create_enhanced_sand_effect(self, start_x: float, start_y: float, 
                                  end_x: float, end_y: float, intensity: float = 1.0) -> None:
        """Create enhanced sand effect with spiral patterns."""
        # Create basic sand flow
        self.create_sand_flow_effect(start_x, start_y, end_x, end_y, intensity)
        
        # Add spiral sand effects
        spiral_count = int(8 * intensity)
        
        for i in range(spiral_count):
            t = i / max(1, spiral_count - 1)
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
            
            particle = Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vel_x=random.uniform(-20, 20),
                vel_y=random.uniform(-20, 20),
                size=random.uniform(2, 4),
                life=random.uniform(1.0, 2.0),
                max_life=1.5,
                color=(255, 215, 0),  # Golden sand
                alpha=255,
                gravity=15.0,
                particle_type=ParticleType.SAND_SPIRAL
            )
            
            self.particles.append(particle)
    
    def create_egyptian_mystical_effect(self, x: float, y: float, effect_type: str, intensity: float = 1.0) -> None:
        """Create Egyptian mystical effects."""
        if effect_type == "ankh_blessing":
            self.create_ankh_blessing_effect(x, y, intensity)
        elif effect_type == "hieroglyph_magic":
            self.create_hieroglyph_magic_effect(x, y, intensity)
        elif effect_type == "scarab_swarm":
            self.create_scarab_swarm_effect(x, y, intensity)
        elif effect_type == "pyramid_energy":
            self.create_pyramid_energy_effect(x, y, intensity)
        elif effect_type == "underworld_flame":
            self.create_underworld_flame_effect(x, y, intensity)
        elif effect_type == "spirit_wisp":
            self.create_spirit_wisp_effect(x, y, intensity)
        else:
            # Default to golden aura
            self.create_power_card_effect(x, y, intensity)
    
    def create_ankh_blessing_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create ankh blessing with divine energy."""
        particle_count = int(8 * intensity)
        
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60) * intensity
            
            particle = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed - 20,  # Upward bias
                size=random.uniform(8, 15),
                life=random.uniform(2.0, 4.0),
                max_life=3.0,
                color=(255, 215, 0),  # Divine gold
                alpha=255,
                gravity=-10.0,  # Float upward
                particle_type=ParticleType.ANKH_GLOW,
                scale=random.uniform(0.8, 1.2),
                pulse_frequency=2.0,
                pulse_amplitude=0.3
            )
            
            self.particles.append(particle)
    
    def create_hieroglyph_magic_effect(self, x: float, y: float, intensity: float = 1.0) -> None:
        """Create glowing hieroglyph magic."""
        particle_count = int(12 * intensity)
        
        for _ in range(particle_count):
            # Create circular pattern
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(20, 80) * intensity
            
            particle_x = x + math.cos(angle) * radius
            particle_y = y + math.sin(angle) * radius
            
            particle = Particle(
                x=particle_x,
                y=particle_y,
                vel_x=random.uniform(-10, 10),
                vel_y=random.uniform(-30, -10),  # Float upward
                size=random.uniform(6, 12),
                life=random.uniform(2.5, 4.5),
                max_life=3.5,
                color=(138, 43, 226),  # Mystical purple
                alpha=255,
                gravity=0.0,
                particle_type=ParticleType.HIEROGLYPH_MAGIC,
                scale=random.uniform(0.6, 1.0),
                rotation_speed=random.uniform(-2, 2),
                pulse_frequency=3.0,
                pulse_amplitude=0.4
            )
            
            self.particles.append(particle)
    
    def create_atmospheric_dust_motes(self, x: float, y: float, width: float, height: float, intensity: float = 1.0) -> None:
        """Create floating dust motes in light beams."""
        particle_count = int(30 * intensity)
        
        for _ in range(particle_count):
            particle = Particle(
                x=x + random.uniform(-width/2, width/2),
                y=y + random.uniform(-height/2, height/2),
                vel_x=random.uniform(-5, 5),
                vel_y=random.uniform(-10, 5),
                size=random.uniform(1, 3),
                life=random.uniform(10.0, 20.0),  # Long-lived atmospheric effect
                max_life=15.0,
                color=(255, 248, 220),  # Warm dust color
                alpha=120,  # Subtle
                gravity=2.0,  # Very light gravity
                particle_type=ParticleType.DUST_MOTE,
                scale=random.uniform(0.8, 1.2)
            )
            
            self.particles.append(particle)
    
    def create_cinematic_card_effect(self, card_type: str, x: float, y: float, rarity: str = "common", intensity: float = 1.0) -> None:
        """Create cinematic card effects based on type and rarity."""
        # Base effect based on card type
        self.create_card_type_effect(card_type, x, y, intensity)
        
        # Additional effects based on rarity
        if rarity == "rare":
            # Add golden sparkles
            self.create_power_card_effect(x, y, intensity * 0.5)
        elif rarity == "epic":
            # Add purple mystical effects
            self.create_hieroglyph_magic_effect(x, y, intensity * 0.7)
        elif rarity == "legendary":
            # Add divine ankh blessing
            self.create_ankh_blessing_effect(x, y, intensity * 0.8)
    
    def clear_all(self) -> None:
        """Clear all particles and emitters."""
        self.particles.clear()
        self.emitters.clear()