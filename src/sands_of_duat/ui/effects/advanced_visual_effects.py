"""
Advanced Visual Effects System - Hades-Level Polish
Professional glow, particle, and lighting effects for UI elements.
"""

import pygame
import math
import random
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum, auto
from dataclasses import dataclass

from ...core.constants import Colors, SCREEN_WIDTH, SCREEN_HEIGHT

class EffectType(Enum):
    """Types of visual effects."""
    BUTTON_GLOW = auto()        # Glowing button effects
    PARTICLE_TRAIL = auto()     # Particle trails
    ENERGY_PULSE = auto()       # Energy pulsing effects
    LIGHTNING_ARC = auto()      # Lightning/energy arcs
    DIVINE_AURA = auto()        # Divine god-like aura
    SAND_SWIRL = auto()         # Egyptian sand effects
    ANKH_BLESSING = auto()      # Ankh symbol effects
    HIEROGLYPH_FLOAT = auto()   # Floating hieroglyphs
    CRYSTAL_SHINE = auto()      # Crystal/gem shine effects
    FIRE_EMBER = auto()         # Fire ember effects

@dataclass
class VisualEffect:
    """A single visual effect instance."""
    effect_type: EffectType
    x: float
    y: float
    width: float = 0
    height: float = 0
    duration: float = 1.0
    elapsed_time: float = 0.0
    active: bool = True
    color: Tuple[int, int, int] = Colors.GOLD
    intensity: float = 1.0
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}

class AdvancedVisualEffects:
    """
    Advanced visual effects system for professional UI polish.
    Provides various effects like glows, particles, and divine auras.
    """
    
    def __init__(self):
        """Initialize the visual effects system."""
        self.active_effects: List[VisualEffect] = []
        self.effect_surfaces: Dict[str, pygame.Surface] = {}
        
        # Create reusable surfaces for performance
        self._create_effect_templates()
        
        print("Advanced Visual Effects System initialized")
    
    def _create_effect_templates(self):
        """Create reusable effect templates for performance."""
        # Glow templates for different sizes
        for size in [32, 64, 128, 256]:
            glow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size // 2
            
            # Create radial glow gradient
            for radius in range(center):
                alpha = int(255 * (1 - radius / center) ** 2)
                if alpha > 0:
                    pygame.draw.circle(glow_surface, (*Colors.GOLD, alpha), 
                                     (center, center), radius)
            
            self.effect_surfaces[f'glow_{size}'] = glow_surface
        
        # Create particle templates
        for size in [2, 4, 6, 8]:
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, Colors.GOLD, (size, size), size)
            self.effect_surfaces[f'particle_{size}'] = particle_surface
    
    def add_button_glow(self, x: float, y: float, width: float, height: float, 
                       color: Tuple[int, int, int] = Colors.GOLD, 
                       intensity: float = 1.0, duration: float = 2.0):
        """Add a glowing effect to a button."""
        effect = VisualEffect(
            effect_type=EffectType.BUTTON_GLOW,
            x=x, y=y, width=width, height=height,
            color=color, intensity=intensity, duration=duration
        )
        self.active_effects.append(effect)
    
    def add_particle_trail(self, x: float, y: float, target_x: float, target_y: float,
                          color: Tuple[int, int, int] = Colors.GOLD, 
                          particle_count: int = 20):
        """Add a particle trail effect."""
        effect = VisualEffect(
            effect_type=EffectType.PARTICLE_TRAIL,
            x=x, y=y, color=color, duration=1.5,
            data={
                'target_x': target_x,
                'target_y': target_y,
                'particles': self._create_trail_particles(x, y, target_x, target_y, particle_count)
            }
        )
        self.active_effects.append(effect)
    
    def add_energy_pulse(self, x: float, y: float, max_radius: float = 100, 
                        color: Tuple[int, int, int] = Colors.LAPIS_LAZULI):
        """Add an energy pulse effect."""
        effect = VisualEffect(
            effect_type=EffectType.ENERGY_PULSE,
            x=x, y=y, color=color, duration=0.8,
            data={'max_radius': max_radius, 'current_radius': 0}
        )
        self.active_effects.append(effect)
    
    def add_lightning_arc(self, start_x: float, start_y: float, 
                         end_x: float, end_y: float,
                         color: Tuple[int, int, int] = Colors.GOLD):
        """Add a lightning arc effect."""
        effect = VisualEffect(
            effect_type=EffectType.LIGHTNING_ARC,
            x=start_x, y=start_y, color=color, duration=0.3,
            data={
                'end_x': end_x,
                'end_y': end_y,
                'segments': self._create_lightning_segments(start_x, start_y, end_x, end_y)
            }
        )
        self.active_effects.append(effect)
    
    def add_divine_aura(self, x: float, y: float, radius: float = 150,
                       color: Tuple[int, int, int] = Colors.GOLD):
        """Add a divine aura effect around gods or important elements."""
        effect = VisualEffect(
            effect_type=EffectType.DIVINE_AURA,
            x=x, y=y, color=color, duration=3.0,
            data={'radius': radius, 'phase': 0.0}
        )
        self.active_effects.append(effect)
    
    def add_sand_swirl(self, x: float, y: float, radius: float = 80):
        """Add Egyptian sand swirl effect."""
        effect = VisualEffect(
            effect_type=EffectType.SAND_SWIRL,
            x=x, y=y, color=Colors.DESERT_SAND, duration=2.0,
            data={
                'radius': radius,
                'particles': [self._create_sand_particle(x, y, radius) for _ in range(30)]
            }
        )
        self.active_effects.append(effect)
    
    def add_ankh_blessing(self, x: float, y: float):
        """Add an ankh symbol blessing effect."""
        effect = VisualEffect(
            effect_type=EffectType.ANKH_BLESSING,
            x=x, y=y, color=Colors.GOLD, duration=2.5,
            data={'scale': 0.0, 'rotation': 0.0}
        )
        self.active_effects.append(effect)
    
    def add_hieroglyph_float(self, x: float, y: float, count: int = 5):
        """Add floating hieroglyph effects."""
        effect = VisualEffect(
            effect_type=EffectType.HIEROGLYPH_FLOAT,
            x=x, y=y, color=Colors.GOLD, duration=4.0,
            data={
                'hieroglyphs': [self._create_hieroglyph_particle(x, y) for _ in range(count)]
            }
        )
        self.active_effects.append(effect)
    
    def add_crystal_shine(self, x: float, y: float, width: float, height: float):
        """Add crystal shine effect for UI elements."""
        effect = VisualEffect(
            effect_type=EffectType.CRYSTAL_SHINE,
            x=x, y=y, width=width, height=height,
            color=Colors.WHITE, duration=1.0,
            data={'shine_pos': -width}
        )
        self.active_effects.append(effect)
    
    def add_fire_ember(self, x: float, y: float, count: int = 15):
        """Add fire ember effects."""
        effect = VisualEffect(
            effect_type=EffectType.FIRE_EMBER,
            x=x, y=y, color=(255, 100, 0), duration=3.0,
            data={
                'embers': [self._create_fire_ember(x, y) for _ in range(count)]
            }
        )
        self.active_effects.append(effect)
    
    def _create_trail_particles(self, start_x: float, start_y: float, 
                               end_x: float, end_y: float, count: int) -> List[Dict]:
        """Create particles for trail effect."""
        particles = []
        for i in range(count):
            progress = i / count
            particles.append({
                'x': start_x + (end_x - start_x) * progress,
                'y': start_y + (end_y - start_y) * progress,
                'size': random.randint(2, 6),
                'alpha': 255,
                'delay': i * 0.05  # Stagger particles
            })
        return particles
    
    def _create_lightning_segments(self, start_x: float, start_y: float,
                                  end_x: float, end_y: float) -> List[Tuple[float, float]]:
        """Create zigzag segments for lightning effect."""
        segments = [(start_x, start_y)]
        
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Create 5-8 zigzag points
        segment_count = random.randint(5, 8)
        for i in range(1, segment_count):
            progress = i / segment_count
            
            # Base position
            x = start_x + dx * progress
            y = start_y + dy * progress
            
            # Add random perpendicular offset
            perpendicular_x = -dy / distance * random.randint(-20, 20)
            perpendicular_y = dx / distance * random.randint(-20, 20)
            
            segments.append((x + perpendicular_x, y + perpendicular_y))
        
        segments.append((end_x, end_y))
        return segments
    
    def _create_sand_particle(self, center_x: float, center_y: float, radius: float) -> Dict:
        """Create a sand particle for swirl effect."""
        angle = random.random() * 2 * math.pi
        distance = random.random() * radius
        
        return {
            'x': center_x + math.cos(angle) * distance,
            'y': center_y + math.sin(angle) * distance,
            'angle': angle,
            'distance': distance,
            'angular_speed': random.uniform(1.0, 3.0),
            'size': random.randint(1, 3),
            'alpha': random.randint(100, 255)
        }
    
    def _create_hieroglyph_particle(self, center_x: float, center_y: float) -> Dict:
        """Create a hieroglyph particle."""
        return {
            'x': center_x + random.randint(-50, 50),
            'y': center_y + random.randint(-50, 50),
            'vx': random.uniform(-20, 20),
            'vy': random.uniform(-30, -10),  # Generally float upward
            'rotation': random.random() * 360,
            'rotation_speed': random.uniform(-90, 90),
            'symbol': random.choice(['☥', '𓋹', '𓂀', '𓇯', '𓅃']),  # Ankh and other symbols
            'alpha': 255,
            'size': random.randint(16, 24)
        }
    
    def _create_fire_ember(self, center_x: float, center_y: float) -> Dict:
        """Create a fire ember particle."""
        return {
            'x': center_x + random.randint(-20, 20),
            'y': center_y + random.randint(-20, 20),
            'vx': random.uniform(-30, 30),
            'vy': random.uniform(-50, -20),
            'size': random.randint(2, 5),
            'alpha': random.randint(200, 255),
            'color': random.choice([(255, 100, 0), (255, 150, 0), (255, 200, 100)])
        }
    
    def update(self, dt: float):
        """Update all active effects."""
        for effect in self.active_effects[:]:  # Copy list to safely remove items
            if not effect.active:
                continue
            
            effect.elapsed_time += dt
            
            # Remove expired effects
            if effect.elapsed_time >= effect.duration:
                effect.active = False
                self.active_effects.remove(effect)
                continue
            
            # Update effect-specific data
            self._update_effect(effect, dt)
    
    def _update_effect(self, effect: VisualEffect, dt: float):
        """Update a specific effect."""
        progress = effect.elapsed_time / effect.duration
        
        if effect.effect_type == EffectType.PARTICLE_TRAIL:
            for particle in effect.data['particles']:
                particle['alpha'] = int(255 * (1 - progress))
        
        elif effect.effect_type == EffectType.ENERGY_PULSE:
            effect.data['current_radius'] = effect.data['max_radius'] * progress
        
        elif effect.effect_type == EffectType.DIVINE_AURA:
            effect.data['phase'] += dt * 2
        
        elif effect.effect_type == EffectType.SAND_SWIRL:
            for particle in effect.data['particles']:
                particle['angle'] += particle['angular_speed'] * dt
                particle['x'] = effect.x + math.cos(particle['angle']) * particle['distance']
                particle['y'] = effect.y + math.sin(particle['angle']) * particle['distance']
        
        elif effect.effect_type == EffectType.ANKH_BLESSING:
            effect.data['scale'] = min(1.0, progress * 2)
            effect.data['rotation'] += dt * 45  # Slow rotation
        
        elif effect.effect_type == EffectType.HIEROGLYPH_FLOAT:
            for hieroglyph in effect.data['hieroglyphs']:
                hieroglyph['x'] += hieroglyph['vx'] * dt
                hieroglyph['y'] += hieroglyph['vy'] * dt
                hieroglyph['rotation'] += hieroglyph['rotation_speed'] * dt
                hieroglyph['alpha'] = int(255 * (1 - progress))
        
        elif effect.effect_type == EffectType.CRYSTAL_SHINE:
            effect.data['shine_pos'] = -effect.width + (effect.width * 2) * progress
        
        elif effect.effect_type == EffectType.FIRE_EMBER:
            for ember in effect.data['embers']:
                ember['x'] += ember['vx'] * dt
                ember['y'] += ember['vy'] * dt
                ember['alpha'] = int(ember['alpha'] * (1 - progress))
    
    def render(self, surface: pygame.Surface):
        """Render all active effects."""
        for effect in self.active_effects:
            if not effect.active:
                continue
            
            self._render_effect(surface, effect)
    
    def _render_effect(self, surface: pygame.Surface, effect: VisualEffect):
        """Render a specific effect."""
        if effect.effect_type == EffectType.BUTTON_GLOW:
            self._render_button_glow(surface, effect)
        elif effect.effect_type == EffectType.PARTICLE_TRAIL:
            self._render_particle_trail(surface, effect)
        elif effect.effect_type == EffectType.ENERGY_PULSE:
            self._render_energy_pulse(surface, effect)
        elif effect.effect_type == EffectType.LIGHTNING_ARC:
            self._render_lightning_arc(surface, effect)
        elif effect.effect_type == EffectType.DIVINE_AURA:
            self._render_divine_aura(surface, effect)
        elif effect.effect_type == EffectType.SAND_SWIRL:
            self._render_sand_swirl(surface, effect)
        elif effect.effect_type == EffectType.ANKH_BLESSING:
            self._render_ankh_blessing(surface, effect)
        elif effect.effect_type == EffectType.HIEROGLYPH_FLOAT:
            self._render_hieroglyph_float(surface, effect)
        elif effect.effect_type == EffectType.CRYSTAL_SHINE:
            self._render_crystal_shine(surface, effect)
        elif effect.effect_type == EffectType.FIRE_EMBER:
            self._render_fire_ember(surface, effect)
    
    def _render_button_glow(self, surface: pygame.Surface, effect: VisualEffect):
        """Render button glow effect."""
        progress = effect.elapsed_time / effect.duration
        intensity = effect.intensity * (1 - progress)
        
        # Create glow surface
        glow_margin = 20
        glow_surface = pygame.Surface((int(effect.width + glow_margin * 2), 
                                      int(effect.height + glow_margin * 2)), pygame.SRCALPHA)
        
        # Draw expanding glow
        for i in range(glow_margin):
            alpha = int(intensity * 100 * (1 - i / glow_margin))
            if alpha > 0:
                color = (*effect.color, alpha)
                pygame.draw.rect(glow_surface, color,
                               (glow_margin - i, glow_margin - i,
                                int(effect.width + i * 2), int(effect.height + i * 2)))
        
        surface.blit(glow_surface, (int(effect.x - glow_margin), int(effect.y - glow_margin)))
    
    def _render_particle_trail(self, surface: pygame.Surface, effect: VisualEffect):
        """Render particle trail effect."""
        for particle in effect.data['particles']:
            if particle['alpha'] > 0:
                color = (*effect.color, particle['alpha'])
                pygame.draw.circle(surface, color,
                                 (int(particle['x']), int(particle['y'])),
                                 particle['size'])
    
    def _render_energy_pulse(self, surface: pygame.Surface, effect: VisualEffect):
        """Render energy pulse effect."""
        radius = int(effect.data['current_radius'])
        if radius > 0:
            progress = effect.elapsed_time / effect.duration
            alpha = int(255 * (1 - progress))
            color = (*effect.color, alpha)
            
            # Draw pulse rings
            for i in range(3):
                ring_radius = radius - i * 5
                if ring_radius > 0:
                    ring_alpha = alpha // (i + 1)
                    ring_color = (*effect.color, ring_alpha)
                    pygame.draw.circle(surface, ring_color,
                                     (int(effect.x), int(effect.y)), ring_radius, 2)
    
    def _render_lightning_arc(self, surface: pygame.Surface, effect: VisualEffect):
        """Render lightning arc effect."""
        segments = effect.data['segments']
        progress = effect.elapsed_time / effect.duration
        alpha = int(255 * (1 - progress))
        
        if alpha > 0:
            color = (*effect.color, alpha)
            
            # Draw lightning segments
            for i in range(len(segments) - 1):
                start_pos = (int(segments[i][0]), int(segments[i][1]))
                end_pos = (int(segments[i + 1][0]), int(segments[i + 1][1]))
                pygame.draw.line(surface, color, start_pos, end_pos, 3)
                
                # Add glow
                pygame.draw.line(surface, (*effect.color, alpha // 2), start_pos, end_pos, 1)
    
    def _render_divine_aura(self, surface: pygame.Surface, effect: VisualEffect):
        """Render divine aura effect."""
        progress = effect.elapsed_time / effect.duration
        phase = effect.data['phase']
        radius = effect.data['radius']
        
        # Pulsing aura
        pulse_intensity = 0.5 + 0.5 * math.sin(phase)
        alpha = int(100 * pulse_intensity * (1 - progress * 0.5))
        
        if alpha > 0:
            # Draw multiple aura rings
            for i in range(3):
                ring_radius = int(radius * (0.7 + i * 0.15))
                ring_alpha = alpha // (i + 1)
                color = (*effect.color, ring_alpha)
                pygame.draw.circle(surface, color,
                                 (int(effect.x), int(effect.y)), ring_radius, 2)
    
    def _render_sand_swirl(self, surface: pygame.Surface, effect: VisualEffect):
        """Render sand swirl effect."""
        for particle in effect.data['particles']:
            if particle['alpha'] > 0:
                color = (*Colors.DESERT_SAND, particle['alpha'])
                pygame.draw.circle(surface, color,
                                 (int(particle['x']), int(particle['y'])),
                                 particle['size'])
    
    def _render_ankh_blessing(self, surface: pygame.Surface, effect: VisualEffect):
        """Render ankh blessing effect."""
        scale = effect.data['scale']
        rotation = effect.data['rotation']
        
        if scale > 0:
            # Draw ankh symbol (simplified)
            font_size = int(48 * scale)
            if font_size > 0:
                font = pygame.font.Font(None, font_size)
                ankh_surface = font.render('☥', True, effect.color)
                
                # Apply rotation (simplified)
                rotated_surface = ankh_surface  # Could add rotation here
                
                rect = rotated_surface.get_rect(center=(int(effect.x), int(effect.y)))
                surface.blit(rotated_surface, rect)
    
    def _render_hieroglyph_float(self, surface: pygame.Surface, effect: VisualEffect):
        """Render floating hieroglyph effect."""
        for hieroglyph in effect.data['hieroglyphs']:
            if hieroglyph['alpha'] > 0:
                font = pygame.font.Font(None, hieroglyph['size'])
                color = (*effect.color, hieroglyph['alpha'])
                
                try:
                    text_surface = font.render(hieroglyph['symbol'], True, color)
                    rect = text_surface.get_rect(center=(int(hieroglyph['x']), int(hieroglyph['y'])))
                    surface.blit(text_surface, rect)
                except:
                    # Fallback if symbol can't be rendered
                    pygame.draw.circle(surface, color,
                                     (int(hieroglyph['x']), int(hieroglyph['y'])), 3)
    
    def _render_crystal_shine(self, surface: pygame.Surface, effect: VisualEffect):
        """Render crystal shine effect."""
        shine_pos = effect.data['shine_pos']
        
        if 0 <= shine_pos <= effect.width:
            # Draw shine line
            shine_x = int(effect.x + shine_pos)
            shine_alpha = int(150 * (1 - abs(shine_pos - effect.width/2) / (effect.width/2)))
            
            if shine_alpha > 0:
                color = (*Colors.WHITE, shine_alpha)
                pygame.draw.line(surface, color,
                               (shine_x, int(effect.y)),
                               (shine_x, int(effect.y + effect.height)), 2)
    
    def _render_fire_ember(self, surface: pygame.Surface, effect: VisualEffect):
        """Render fire ember effect."""
        for ember in effect.data['embers']:
            if ember['alpha'] > 0:
                color = (*ember['color'], ember['alpha'])
                pygame.draw.circle(surface, color,
                                 (int(ember['x']), int(ember['y'])),
                                 ember['size'])
    
    def clear_all_effects(self):
        """Clear all active effects."""
        self.active_effects.clear()
    
    def get_active_effect_count(self) -> int:
        """Get the number of active effects."""
        return len(self.active_effects)

# Global visual effects system instance
advanced_visual_effects = AdvancedVisualEffects()