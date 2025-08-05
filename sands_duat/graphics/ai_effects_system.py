"""
AI Effects System for Sands of Duat

Advanced magical effects system that complements AI-generated assets
with procedural effects, particles, and visual enhancements.
"""

import pygame
import math
import random
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum
from dataclasses import dataclass
import logging


class EffectType(Enum):
    """Types of magical effects"""
    CARD_CAST = "card_cast"
    DAMAGE_IMPACT = "damage_impact"
    HEALING_GLOW = "healing_glow"
    SAND_FLOW = "sand_flow"
    ANKH_BLESSING = "ankh_blessing"
    SCARAB_SWARM = "scarab_swarm"
    PYRAMID_POWER = "pyramid_power"
    DIVINE_LIGHT = "divine_light"
    SHADOW_CURSE = "shadow_curse"
    EGYPTIAN_RUNES = "egyptian_runes"


@dataclass
class EffectParticle:
    """Individual particle in an effect"""
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    size: float
    color: Tuple[int, int, int]
    alpha: int
    rotation: float = 0.0
    rotation_speed: float = 0.0
    scale: float = 1.0
    effect_data: Dict[str, Any] = None


class MagicalEffect:
    """Base class for magical effects"""
    
    def __init__(self, x: int, y: int, effect_type: EffectType):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.particles: List[EffectParticle] = []
        self.life_time = 0.0
        self.max_life_time = 2.0
        self.active = True
        self.intensity = 1.0
        
    def update(self, delta_time: float) -> None:
        """Update effect and particles"""
        self.life_time += delta_time
        
        # Update particles
        for particle in self.particles[:]:
            particle.life -= delta_time
            particle.x += particle.vx * delta_time
            particle.y += particle.vy * delta_time
            particle.rotation += particle.rotation_speed * delta_time
            
            # Update alpha based on life
            if particle.max_life > 0:
                particle.alpha = int(255 * (particle.life / particle.max_life))
            
            # Remove dead particles
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Check if effect is finished
        if self.life_time >= self.max_life_time and len(self.particles) == 0:
            self.active = False
    
    def render(self, surface: pygame.Surface) -> None:
        """Render effect particles"""
        for particle in self.particles:
            if particle.alpha > 0:
                self._render_particle(surface, particle)
    
    def _render_particle(self, surface: pygame.Surface, particle: EffectParticle) -> None:
        """Render individual particle - override in subclasses"""
        # Basic circle particle
        if particle.alpha > 0:
            color = (*particle.color, particle.alpha)
            try:
                particle_surface = pygame.Surface((int(particle.size * 2), int(particle.size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, 
                                 (int(particle.size), int(particle.size)), int(particle.size))
                surface.blit(particle_surface, (int(particle.x - particle.size), int(particle.y - particle.size)))
            except:
                pass  # Fail silently for invalid particles
    
    def is_active(self) -> bool:
        """Check if effect is still active"""
        return self.active


class SandFlowEffect(MagicalEffect):
    """Sand flowing and swirling effect"""
    
    def __init__(self, x: int, y: int, direction: Tuple[float, float] = (0, -1)):
        super().__init__(x, y, EffectType.SAND_FLOW)
        self.direction = direction
        self.max_life_time = 1.5
        self.spawn_timer = 0.0
        self.spawn_rate = 0.05  # Every 50ms
        
    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        
        # Spawn new sand particles
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_rate and self.life_time < self.max_life_time * 0.8:
            self._spawn_sand_particle()
            self.spawn_timer = 0.0
    
    def _spawn_sand_particle(self) -> None:
        """Spawn a sand particle"""
        # Random position around origin
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        
        # Velocity in general direction with some randomness
        base_speed = random.uniform(50, 100)
        vx = self.direction[0] * base_speed + random.uniform(-30, 30)
        vy = self.direction[1] * base_speed + random.uniform(-30, 30)
        
        particle = EffectParticle(
            x=self.x + offset_x,
            y=self.y + offset_y,
            vx=vx,
            vy=vy,
            life=random.uniform(0.8, 1.5),
            max_life=random.uniform(0.8, 1.5),
            size=random.uniform(2, 5),
            color=(194, 178, 128),  # Sand color
            alpha=255,
            rotation_speed=random.uniform(-2, 2)
        )
        particle.max_life = particle.life
        self.particles.append(particle)


class AnkhBlessingEffect(MagicalEffect):
    """Divine ankh symbol with radiating light"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y, EffectType.ANKH_BLESSING)
        self.max_life_time = 2.5
        self.glow_intensity = 0.0
        self.ankh_scale = 0.0
        self.blessing_particles_spawned = False
        
    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        
        # Animate ankh appearance
        progress = min(1.0, self.life_time / (self.max_life_time * 0.4))
        self.ankh_scale = progress
        self.glow_intensity = math.sin(progress * math.pi) * 255
        
        # Spawn blessing particles at peak
        if not self.blessing_particles_spawned and progress > 0.7:
            self._spawn_blessing_particles()
            self.blessing_particles_spawned = True
    
    def _spawn_blessing_particles(self) -> None:
        """Spawn divine blessing particles"""
        for i in range(12):
            angle = (i / 12) * 2 * math.pi
            distance = random.uniform(30, 60)
            
            particle = EffectParticle(
                x=self.x + math.cos(angle) * distance,
                y=self.y + math.sin(angle) * distance,
                vx=math.cos(angle) * random.uniform(20, 40),
                vy=math.sin(angle) * random.uniform(20, 40),
                life=random.uniform(1.0, 1.8),
                max_life=random.uniform(1.0, 1.8),
                size=random.uniform(3, 7),
                color=(255, 215, 0),  # Gold
                alpha=255
            )
            particle.max_life = particle.life
            self.particles.append(particle)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render ankh symbol and particles"""
        # Draw glow background
        if self.glow_intensity > 0:
            glow_size = int(50 * self.ankh_scale)
            if glow_size > 0:
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                glow_color = (255, 215, 0, int(self.glow_intensity * 0.3))
                pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
                surface.blit(glow_surface, (self.x - glow_size, self.y - glow_size))
        
        # Draw simplified ankh symbol
        if self.ankh_scale > 0.1:
            self._draw_ankh_symbol(surface, self.x, self.y, self.ankh_scale)
        
        # Draw particles
        super().render(surface)
    
    def _draw_ankh_symbol(self, surface: pygame.Surface, x: int, y: int, scale: float) -> None:
        """Draw simplified ankh symbol"""
        try:
            color = (255, 215, 0)  # Gold
            line_width = max(2, int(3 * scale))
            
            # Ankh dimensions scaled
            size = int(20 * scale)
            
            # Cross (vertical line)
            pygame.draw.line(surface, color, 
                           (x, y - size), (x, y + size), line_width)
            
            # Cross (horizontal line) 
            pygame.draw.line(surface, color,
                           (x - size//2, y), (x + size//2, y), line_width)
            
            # Loop (circle at top)
            pygame.draw.circle(surface, color, (x, y - size//2), size//3, line_width)
            
        except:
            pass  # Fail silently if drawing fails


class ScarabSwarmEffect(MagicalEffect):
    """Swarm of magical scarab beetles"""
    
    def __init__(self, x: int, y: int, target_x: int, target_y: int):
        super().__init__(x, y, EffectType.SCARAB_SWARM)
        self.target_x = target_x
        self.target_y = target_y
        self.max_life_time = 2.0
        self.scarabs_spawned = False
        
    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        
        # Spawn scarabs at start
        if not self.scarabs_spawned and self.life_time > 0.1:
            self._spawn_scarabs()
            self.scarabs_spawned = True
        
        # Update scarab movement toward target
        for particle in self.particles:
            if particle.effect_data and "is_scarab" in particle.effect_data:
                # Move toward target with some wandering
                dx = self.target_x - particle.x
                dy = self.target_y - particle.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 5:
                    # Add some wandering behavior
                    wander_x = math.sin(self.life_time * 3 + particle.rotation) * 20
                    wander_y = math.cos(self.life_time * 2 + particle.rotation) * 20
                    
                    particle.vx = (dx/distance) * 80 + wander_x
                    particle.vy = (dy/distance) * 80 + wander_y
                else:
                    # Arrived at target - explode into sparkles
                    if not particle.effect_data.get("exploded", False):
                        self._create_sparkle_explosion(particle.x, particle.y)
                        particle.effect_data["exploded"] = True
                        particle.life = 0  # Remove scarab
    
    def _spawn_scarabs(self) -> None:
        """Spawn magical scarab beetles"""
        for i in range(6):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 30)
            
            particle = EffectParticle(
                x=self.x + math.cos(angle) * distance,
                y=self.y + math.sin(angle) * distance,
                vx=0, vy=0,  # Will be set in update
                life=1.8,
                max_life=1.8,
                size=4,
                color=(139, 69, 19),  # Brown
                alpha=255,
                rotation=angle,
                rotation_speed=random.uniform(2, 4),
                effect_data={"is_scarab": True, "exploded": False}
            )
            self.particles.append(particle)
    
    def _create_sparkle_explosion(self, x: float, y: float) -> None:
        """Create sparkle explosion when scarab reaches target"""
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            speed = random.uniform(30, 60)
            
            sparkle = EffectParticle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=0.6,
                max_life=0.6,
                size=2,
                color=(255, 215, 0),  # Gold sparkles
                alpha=255
            )
            self.particles.append(sparkle)
            
    def _render_particle(self, surface: pygame.Surface, particle: EffectParticle) -> None:
        """Render scarab or sparkle particle"""
        if particle.effect_data and particle.effect_data.get("is_scarab", False):
            # Draw scarab as small oval
            try:
                scarab_size = int(particle.size)
                scarab_surface = pygame.Surface((scarab_size * 2, scarab_size), pygame.SRCALPHA)
                pygame.draw.ellipse(scarab_surface, (*particle.color, particle.alpha),
                                  scarab_surface.get_rect())
                
                # Rotate the scarab
                if particle.rotation != 0:
                    scarab_surface = pygame.transform.rotate(scarab_surface, 
                                                           math.degrees(particle.rotation))
                
                rect = scarab_surface.get_rect(center=(int(particle.x), int(particle.y)))
                surface.blit(scarab_surface, rect)
            except:
                pass
        else:
            # Draw sparkle as star-like shape
            super()._render_particle(surface, particle)


class AIEffectsSystem:
    """Main effects system manager"""
    
    def __init__(self):
        self.effects: List[MagicalEffect] = []
        self.logger = logging.getLogger(__name__)
        
    def add_effect(self, effect: MagicalEffect) -> None:
        """Add a new effect to the system"""
        self.effects.append(effect)
        self.logger.debug(f"Added {effect.effect_type.value} effect at ({effect.x}, {effect.y})")
    
    def create_sand_flow(self, x: int, y: int, direction: Tuple[float, float] = (0, -1)) -> None:
        """Create sand flow effect"""
        self.add_effect(SandFlowEffect(x, y, direction))
    
    def create_ankh_blessing(self, x: int, y: int) -> None:
        """Create ankh blessing effect"""
        self.add_effect(AnkhBlessingEffect(x, y))
    
    def create_card_cast_effect(self, x: int, y: int, card_name: str) -> None:
        """Create enhanced effect based on card name with Egyptian theming"""
        card_lower = card_name.lower()
        
        if "sand" in card_lower or "desert" in card_lower:
            self.create_sand_flow(x, y)
        elif "ankh" in card_lower or "blessing" in card_lower:
            self.create_ankh_blessing(x, y)
        elif "scarab" in card_lower:
            # Create scarab swarm effect
            target_x = x + random.randint(-100, 100)
            target_y = y + random.randint(-50, 50)
            self.create_scarab_swarm(x, y, target_x, target_y)
        elif "pyramid" in card_lower or "pharaoh" in card_lower:
            # Golden divine light effect
            self.create_divine_light(x, y)
        elif "mummy" in card_lower or "tomb" in card_lower:
            # Dark curse effect
            self.create_shadow_curse(x, y)
        elif "ra" in card_lower or "solar" in card_lower:
            # Bright solar effect
            self.create_solar_flare(x, y)
        elif "isis" in card_lower or "grace" in card_lower:
            # Healing glow effect
            self.create_healing_glow(x, y)
        elif "anubis" in card_lower or "judgment" in card_lower:
            # Dark judgment effect
            self.create_judgment_effect(x, y)
        elif "thoth" in card_lower or "wisdom" in card_lower:
            # Ancient runes effect
            self.create_runes_effect(x, y)
        else:
            # Default magical sparkle effect with Egyptian flair
            self.create_sand_flow(x, y, (random.uniform(-1, 1), random.uniform(-1, 1)))
    
    def create_scarab_swarm(self, start_x: int, start_y: int, target_x: int, target_y: int) -> None:
        """Create scarab swarm effect"""
        self.add_effect(ScarabSwarmEffect(start_x, start_y, target_x, target_y))
    
    def create_divine_light(self, x: int, y: int) -> None:
        """Create divine golden light effect"""
        # Enhanced ankh blessing with golden particles
        self.create_ankh_blessing(x, y)
        
        # Add fewer golden sparkles for performance
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(20, 80)
            spark_x = x + math.cos(angle) * distance
            spark_y = y + math.sin(angle) * distance
            
            effect = SandFlowEffect(int(spark_x), int(spark_y), (0, -1))
            # Override color to golden
            for particle in effect.particles:
                particle.color = (255, 215, 0)  # Gold
            self.add_effect(effect)
    
    def create_shadow_curse(self, x: int, y: int) -> None:
        """Create dark shadow curse effect"""
        effect = SandFlowEffect(x, y, (0, 1))  # Downward flow
        effect.max_life_time = 2.0
        
        # Override particles to be dark purple/black
        def spawn_shadow_particle():
            offset_x = random.uniform(-30, 30)
            offset_y = random.uniform(-30, 30)
            
            particle = EffectParticle(
                x=x + offset_x,
                y=y + offset_y,
                vx=random.uniform(-20, 20),
                vy=random.uniform(30, 60),  # Downward
                life=random.uniform(1.5, 2.5),
                max_life=random.uniform(1.5, 2.5),
                size=random.uniform(3, 8),
                color=(60, 20, 80),  # Dark purple
                alpha=255,
                rotation_speed=random.uniform(-3, 3)
            )
            particle.max_life = particle.life
            effect.particles.append(particle)
        
        # Add fewer shadow particles for performance
        for _ in range(6):
            spawn_shadow_particle()
            
        self.add_effect(effect)
    
    def create_solar_flare(self, x: int, y: int) -> None:
        """Create bright solar flare effect"""
        # Bright radiating effect
        self.create_ankh_blessing(x, y)
        
        # Add fewer particles for performance
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 120)
            
            particle = EffectParticle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.8, 1.5),
                max_life=random.uniform(0.8, 1.5),
                size=random.uniform(4, 8),
                color=(255, 200, 50),  # Bright yellow-orange
                alpha=255
            )
            particle.max_life = particle.life
            
            # Create temporary effect for this particle
            temp_effect = MagicalEffect(x, y, EffectType.DIVINE_LIGHT)
            temp_effect.particles.append(particle)
            self.add_effect(temp_effect)
    
    def create_healing_glow(self, x: int, y: int) -> None:
        """Create gentle healing glow effect"""
        # Soft green healing particles
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 40)
            
            particle = EffectParticle(
                x=x + math.cos(angle) * distance,
                y=y + math.sin(angle) * distance,
                vx=math.cos(angle) * random.uniform(10, 30),
                vy=random.uniform(-20, -10),  # Float upward
                life=random.uniform(2.0, 3.0),
                max_life=random.uniform(2.0, 3.0),
                size=random.uniform(3, 6),
                color=(100, 255, 150),  # Soft green
                alpha=255
            )
            particle.max_life = particle.life
            
            # Create temporary effect
            temp_effect = MagicalEffect(x, y, EffectType.HEALING_GLOW)
            temp_effect.particles.append(particle)
            self.add_effect(temp_effect)
    
    def create_judgment_effect(self, x: int, y: int) -> None:
        """Create dark judgment effect"""
        self.create_shadow_curse(x, y)
        
        # Add red judgment particles
        for _ in range(10):
            particle = EffectParticle(
                x=x + random.uniform(-20, 20),
                y=y + random.uniform(-20, 20),
                vx=random.uniform(-40, 40),
                vy=random.uniform(-40, 40),
                life=random.uniform(1.0, 2.0),
                max_life=random.uniform(1.0, 2.0),
                size=random.uniform(3, 7),
                color=(200, 50, 50),  # Dark red
                alpha=255
            )
            particle.max_life = particle.life
            
            temp_effect = MagicalEffect(x, y, EffectType.SHADOW_CURSE)
            temp_effect.particles.append(particle)
            self.add_effect(temp_effect)
    
    def create_runes_effect(self, x: int, y: int) -> None:
        """Create ancient Egyptian runes effect"""
        # Blue mystical particles
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(20, 60)
            
            particle = EffectParticle(
                x=x + math.cos(angle) * radius,
                y=y + math.sin(angle) * radius,
                vx=math.cos(angle + math.pi/2) * 30,  # Circular motion
                vy=math.sin(angle + math.pi/2) * 30,
                life=random.uniform(2.0, 3.5),
                max_life=random.uniform(2.0, 3.5),
                size=random.uniform(2, 5),
                color=(100, 150, 255),  # Mystical blue
                alpha=255,
                rotation_speed=random.uniform(1, 3)
            )
            particle.max_life = particle.life
            
            temp_effect = MagicalEffect(x, y, EffectType.EGYPTIAN_RUNES)
            temp_effect.particles.append(particle)
            self.add_effect(temp_effect)
    
    def update(self, delta_time: float) -> None:
        """Update all effects"""
        # Update effects and remove inactive ones
        for effect in self.effects[:]:
            effect.update(delta_time)
            if not effect.is_active():
                self.effects.remove(effect)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all effects"""
        for effect in self.effects:
            effect.render(surface)
    
    def clear_all_effects(self) -> None:
        """Clear all active effects"""
        self.effects.clear()
    
    def get_active_effect_count(self) -> int:
        """Get number of active effects"""
        return len(self.effects)


# Global effects system
_global_effects_system = None

def get_ai_effects() -> AIEffectsSystem:
    """Get global AI effects system"""
    global _global_effects_system
    if _global_effects_system is None:
        _global_effects_system = AIEffectsSystem()
    return _global_effects_system