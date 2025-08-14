"""
Combat Visual Effects - Hades-level battlefield effects system.
Creates immersive visual feedback for combat actions with particles, screen shake, and damage numbers.
"""

import pygame
import math
import random
from typing import Tuple, Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass
from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT

class EffectType(Enum):
    """Types of combat visual effects."""
    DAMAGE_NUMBER = "damage_number"
    HEALING_NUMBER = "healing_number"
    SCREEN_SHAKE = "screen_shake"
    PARTICLE_BURST = "particle_burst"
    LIGHTNING_STRIKE = "lightning_strike"
    ENERGY_WAVE = "energy_wave"
    BLOOD_SPLATTER = "blood_splatter"
    DIVINE_LIGHT = "divine_light"
    DUST_CLOUD = "dust_cloud"
    FIRE_EXPLOSION = "fire_explosion"
    ICE_SHARDS = "ice_shards"
    POISON_CLOUD = "poison_cloud"

class ParticleType(Enum):
    """Particle system types."""
    SPARK = "spark"
    DUST = "dust"
    BLOOD = "blood"
    ENERGY = "energy"
    FIRE = "fire"
    ICE = "ice"
    POISON = "poison"
    DIVINE = "divine"

@dataclass
class Particle:
    """Individual particle in a particle system."""
    x: float
    y: float
    vel_x: float
    vel_y: float
    life: float
    max_life: float
    size: float
    color: Tuple[int, int, int]
    gravity: float = 0.5
    fade: bool = True

@dataclass
class DamageNumber:
    """Floating damage/healing number."""
    x: float
    y: float
    value: int
    color: Tuple[int, int, int]
    life: float
    max_life: float = 2.0
    vel_y: float = -50.0
    scale: float = 1.0
    is_critical: bool = False

class CombatEffects:
    """Professional combat visual effects system with Hades-level polish."""
    
    def __init__(self):
        # Active effects tracking
        self.particles: List[Particle] = []
        self.damage_numbers: List[DamageNumber] = []
        self.screen_shake: Dict[str, float] = {'x': 0, 'y': 0, 'intensity': 0, 'duration': 0}
        
        # Effect pools for performance
        self.max_particles = 500
        self.max_damage_numbers = 20
        
        # Lightning system
        self.lightning_segments: List[Dict[str, Any]] = []
        
        # Screen flash system
        self.screen_flash = {'active': False, 'color': Colors.WHITE, 'alpha': 0, 'duration': 0}
        
        # Fonts for damage numbers
        self.damage_font = pygame.font.Font(None, 48)
        self.critical_font = pygame.font.Font(None, 64)
    
    def add_damage_number(self, x: float, y: float, damage: int, is_critical: bool = False, 
                         is_healing: bool = False):
        """Add floating damage/healing number."""
        if len(self.damage_numbers) >= self.max_damage_numbers:
            return
        
        # Determine color based on type
        if is_healing:
            color = Colors.GREEN
        elif is_critical:
            color = Colors.GOLD
        else:
            color = Colors.RED
        
        # Add slight random offset for multiple numbers
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-10, 10)
        
        number = DamageNumber(
            x=x + offset_x,
            y=y + offset_y,
            value=damage,
            color=color,
            life=2.5 if is_critical else 2.0,
            is_critical=is_critical,
            vel_y=-60.0 if is_critical else -45.0
        )
        
        self.damage_numbers.append(number)
    
    def add_screen_shake(self, intensity: float, duration: float):
        """Add screen shake effect."""
        self.screen_shake['intensity'] = max(self.screen_shake['intensity'], intensity)
        self.screen_shake['duration'] = max(self.screen_shake['duration'], duration)
    
    def add_particle_burst(self, x: float, y: float, particle_type: ParticleType, count: int = 15):
        """Create a burst of particles."""
        if len(self.particles) + count > self.max_particles:
            count = max(0, self.max_particles - len(self.particles))
        
        # Particle properties based on type
        type_configs = {
            ParticleType.SPARK: {
                'colors': [(255, 255, 100), (255, 200, 0), (255, 100, 0)],
                'size_range': (2, 6),
                'speed_range': (50, 150),
                'life_range': (0.5, 1.5),
                'gravity': 20
            },
            ParticleType.BLOOD: {
                'colors': [(200, 0, 0), (150, 0, 0), (100, 0, 0)],
                'size_range': (3, 8),
                'speed_range': (30, 100),
                'life_range': (1.0, 2.0),
                'gravity': 80
            },
            ParticleType.ENERGY: {
                'colors': [(100, 150, 255), (150, 100, 255), (200, 150, 255)],
                'size_range': (2, 5),
                'speed_range': (40, 120),
                'life_range': (0.8, 1.8),
                'gravity': -10
            },
            ParticleType.FIRE: {
                'colors': [(255, 100, 0), (255, 150, 0), (255, 200, 100)],
                'size_range': (4, 10),
                'speed_range': (20, 80),
                'life_range': (1.2, 2.2),
                'gravity': -30
            },
            ParticleType.DIVINE: {
                'colors': [(255, 215, 0), (255, 255, 200), (255, 255, 255)],
                'size_range': (3, 7),
                'speed_range': (20, 60),
                'life_range': (2.0, 3.0),
                'gravity': -15
            }
        }
        
        config = type_configs.get(particle_type, type_configs[ParticleType.SPARK])
        
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*config['speed_range'])
            
            particle = Particle(
                x=x,
                y=y,
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                life=random.uniform(*config['life_range']),
                max_life=random.uniform(*config['life_range']),
                size=random.uniform(*config['size_range']),
                color=random.choice(config['colors']),
                gravity=config['gravity']
            )
            
            self.particles.append(particle)
    
    def add_lightning_strike(self, start_x: float, start_y: float, end_x: float, end_y: float):
        """Create lightning effect between two points."""
        # Clear existing lightning
        self.lightning_segments.clear()
        
        # Generate lightning path with random segments
        num_segments = int(math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2) / 20)
        num_segments = max(3, min(num_segments, 15))
        
        points = [(start_x, start_y)]
        
        for i in range(1, num_segments):
            progress = i / num_segments
            base_x = start_x + (end_x - start_x) * progress
            base_y = start_y + (end_y - start_y) * progress
            
            # Add random displacement
            displacement = 30 * (1 - abs(progress - 0.5) * 2)  # Max displacement in middle
            offset_x = random.uniform(-displacement, displacement)
            offset_y = random.uniform(-displacement, displacement)
            
            points.append((base_x + offset_x, base_y + offset_y))
        
        points.append((end_x, end_y))
        
        # Create lightning segments
        for i in range(len(points) - 1):
            segment = {
                'start': points[i],
                'end': points[i + 1],
                'thickness': random.uniform(2, 6),
                'alpha': 255,
                'life': 0.3,
                'max_life': 0.3
            }
            self.lightning_segments.append(segment)
        
        # Add screen flash
        self.screen_flash = {
            'active': True,
            'color': (200, 200, 255),
            'alpha': 100,
            'duration': 0.1
        }
    
    def add_energy_wave(self, center_x: float, center_y: float, max_radius: float = 200):
        """Create expanding energy wave effect."""
        # Create ring of energy particles
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            start_x = center_x + math.cos(rad) * 20
            start_y = center_y + math.sin(rad) * 20
            
            particle = Particle(
                x=start_x,
                y=start_y,
                vel_x=math.cos(rad) * 150,
                vel_y=math.sin(rad) * 150,
                life=1.5,
                max_life=1.5,
                size=4,
                color=(100, 150, 255),
                gravity=0,
                fade=True
            )
            
            if len(self.particles) < self.max_particles:
                self.particles.append(particle)
    
    def add_divine_light(self, x: float, y: float):
        """Create divine light beam effect."""
        # Vertical light beam
        for i in range(20):
            offset_x = random.uniform(-15, 15)
            particle_y = y - i * 30 - random.uniform(0, 100)
            
            particle = Particle(
                x=x + offset_x,
                y=particle_y,
                vel_x=0,
                vel_y=20,
                life=2.0,
                max_life=2.0,
                size=random.uniform(6, 12),
                color=(255, 255, 200),
                gravity=0,
                fade=True
            )
            
            if len(self.particles) < self.max_particles:
                self.particles.append(particle)
    
    def trigger_effect(self, effect_type: EffectType, x: float, y: float, 
                      value: Optional[int] = None, **kwargs):
        """Trigger a specific combat effect."""
        if effect_type == EffectType.DAMAGE_NUMBER:
            is_critical = kwargs.get('is_critical', False)
            self.add_damage_number(x, y, value or 0, is_critical)
            self.add_particle_burst(x, y, ParticleType.BLOOD, 8)
            self.add_screen_shake(5.0 if is_critical else 2.0, 0.2)
        
        elif effect_type == EffectType.HEALING_NUMBER:
            self.add_damage_number(x, y, value or 0, is_healing=True)
            self.add_particle_burst(x, y, ParticleType.DIVINE, 12)
        
        elif effect_type == EffectType.LIGHTNING_STRIKE:
            end_x = kwargs.get('end_x', x + 200)
            end_y = kwargs.get('end_y', y)
            self.add_lightning_strike(x, y, end_x, end_y)
            self.add_screen_shake(8.0, 0.3)
        
        elif effect_type == EffectType.ENERGY_WAVE:
            self.add_energy_wave(x, y)
            self.add_screen_shake(4.0, 0.4)
        
        elif effect_type == EffectType.DIVINE_LIGHT:
            self.add_divine_light(x, y)
        
        elif effect_type == EffectType.FIRE_EXPLOSION:
            self.add_particle_burst(x, y, ParticleType.FIRE, 25)
            self.add_screen_shake(6.0, 0.3)
        
        elif effect_type == EffectType.PARTICLE_BURST:
            particle_type = kwargs.get('particle_type', ParticleType.SPARK)
            count = kwargs.get('count', 15)
            self.add_particle_burst(x, y, particle_type, count)
    
    def update(self, dt: float):
        """Update all combat effects."""
        # Update particles
        particles_to_remove = []
        for particle in self.particles:
            # Update position
            particle.x += particle.vel_x * dt
            particle.y += particle.vel_y * dt
            
            # Apply gravity
            particle.vel_y += particle.gravity * dt
            
            # Update life
            particle.life -= dt
            
            if particle.life <= 0:
                particles_to_remove.append(particle)
        
        # Remove dead particles
        for particle in particles_to_remove:
            self.particles.remove(particle)
        
        # Update damage numbers
        numbers_to_remove = []
        for number in self.damage_numbers:
            number.y += number.vel_y * dt
            number.life -= dt
            
            # Slow down over time
            number.vel_y *= 0.98
            
            if number.life <= 0:
                numbers_to_remove.append(number)
        
        # Remove expired numbers
        for number in numbers_to_remove:
            self.damage_numbers.remove(number)
        
        # Update screen shake
        if self.screen_shake['duration'] > 0:
            self.screen_shake['duration'] -= dt
            intensity = self.screen_shake['intensity'] * (self.screen_shake['duration'] / 1.0)
            
            self.screen_shake['x'] = math.sin(pygame.time.get_ticks() * 0.02) * intensity
            self.screen_shake['y'] = math.cos(pygame.time.get_ticks() * 0.03) * intensity
            
            if self.screen_shake['duration'] <= 0:
                self.screen_shake['x'] = 0
                self.screen_shake['y'] = 0
                self.screen_shake['intensity'] = 0
        
        # Update lightning
        segments_to_remove = []
        for segment in self.lightning_segments:
            segment['life'] -= dt
            segment['alpha'] = int(255 * (segment['life'] / segment['max_life']))
            
            if segment['life'] <= 0:
                segments_to_remove.append(segment)
        
        for segment in segments_to_remove:
            self.lightning_segments.remove(segment)
        
        # Update screen flash
        if self.screen_flash['active']:
            self.screen_flash['duration'] -= dt
            if self.screen_flash['duration'] <= 0:
                self.screen_flash['active'] = False
    
    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0):
        """Render all combat effects."""
        # Apply screen shake offset
        shake_x = int(self.screen_shake['x'])
        shake_y = int(self.screen_shake['y'])
        
        # Render particles
        for particle in self.particles:
            if particle.life > 0:
                # Calculate alpha based on remaining life
                alpha = 255
                if particle.fade:
                    alpha = int(255 * (particle.life / particle.max_life))
                
                # Create particle surface
                size = int(particle.size)
                if size <= 0:
                    continue
                
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color_with_alpha = (*particle.color, alpha)
                pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
                
                # Render with screen shake
                x = int(particle.x + offset_x + shake_x - size)
                y = int(particle.y + offset_y + shake_y - size)
                surface.blit(particle_surface, (x, y), special_flags=pygame.BLEND_ADD)
        
        # Render lightning
        for segment in self.lightning_segments:
            if segment['alpha'] > 0:
                start_x = int(segment['start'][0] + offset_x + shake_x)
                start_y = int(segment['start'][1] + offset_y + shake_y)
                end_x = int(segment['end'][0] + offset_x + shake_x)
                end_y = int(segment['end'][1] + offset_y + shake_y)
                
                # Draw main lightning bolt
                pygame.draw.line(surface, (255, 255, 255, segment['alpha']), 
                               (start_x, start_y), (end_x, end_y), int(segment['thickness']))
                
                # Draw inner core
                if segment['thickness'] > 2:
                    pygame.draw.line(surface, (200, 200, 255, segment['alpha']), 
                                   (start_x, start_y), (end_x, end_y), 
                                   max(1, int(segment['thickness'] / 2)))
        
        # Render damage numbers
        for number in self.damage_numbers:
            alpha = int(255 * (number.life / number.max_life))
            font = self.critical_font if number.is_critical else self.damage_font
            
            # Render text with alpha
            text_surface = font.render(str(number.value), True, number.color)
            text_surface.set_alpha(alpha)
            
            # Scale for critical hits
            if number.is_critical:
                scale = 1.0 + (1.0 - number.life / number.max_life) * 0.3
                scaled_surface = pygame.transform.scale(
                    text_surface, 
                    (int(text_surface.get_width() * scale), 
                     int(text_surface.get_height() * scale))
                )
                text_surface = scaled_surface
            
            # Render with screen shake
            x = int(number.x + offset_x + shake_x - text_surface.get_width() / 2)
            y = int(number.y + offset_y + shake_y - text_surface.get_height() / 2)
            surface.blit(text_surface, (x, y))
        
        # Render screen flash
        if self.screen_flash['active']:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # Use RGB color and set alpha separately to avoid invalid color argument
            flash_surface.fill(self.screen_flash['color'])
            flash_surface.set_alpha(self.screen_flash['alpha'])
            surface.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def get_screen_shake_offset(self) -> Tuple[int, int]:
        """Get current screen shake offset for camera system."""
        return int(self.screen_shake['x']), int(self.screen_shake['y'])
    
    def clear_all_effects(self):
        """Clear all active effects."""
        self.particles.clear()
        self.damage_numbers.clear()
        self.lightning_segments.clear()
        self.screen_shake = {'x': 0, 'y': 0, 'intensity': 0, 'duration': 0}
        self.screen_flash['active'] = False
    
    def get_effects_count(self) -> Dict[str, int]:
        """Get count of active effects for performance monitoring."""
        return {
            'particles': len(self.particles),
            'damage_numbers': len(self.damage_numbers),
            'lightning_segments': len(self.lightning_segments),
            'screen_shake_active': self.screen_shake['duration'] > 0,
            'screen_flash_active': self.screen_flash['active']
        }

# Global combat effects instance
combat_effects = CombatEffects()