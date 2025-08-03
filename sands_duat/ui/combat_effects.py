"""
Combat Visual Effects System

Advanced visual effects for combat actions in Sands of Duat.
Provides Egyptian-themed animations for cards, abilities, and combat feedback.

Features:
- Card play animations with sand explosions and Egyptian effects
- Particle systems for different card types
- Damage/healing visual feedback
- Turn transitions and combat state changes
- Hieroglyphic and sand-themed visual elements
"""

import pygame
import math
import random
import time
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

from .particle_system import ParticleSystem, ParticleEmitter, ParticleType, Particle
from ..audio.audio_manager import get_audio_manager, SoundType


class EffectType(Enum):
    """Types of visual effects."""
    CARD_PLAY = "card_play"
    CARD_HOVER = "card_hover"
    DAMAGE_DEALT = "damage_dealt"
    DAMAGE_RECEIVED = "damage_received"
    HEALING = "healing"
    BUFF_APPLIED = "buff_applied"
    DEBUFF_APPLIED = "debuff_applied"
    SAND_GAINED = "sand_gained"
    SAND_SPENT = "sand_spent"
    TURN_START = "turn_start"
    TURN_END = "turn_end"
    VICTORY = "victory"
    DEFEAT = "defeat"


class CardType(Enum):
    """Card types for visual differentiation."""
    ATTACK = "attack"      # Fire effects
    SKILL = "skill"        # Blue light effects  
    POWER = "power"        # Golden aura effects
    STATUS = "status"      # Purple mystical effects


@dataclass
class VisualEffect:
    """Individual visual effect with timing and rendering data."""
    effect_type: EffectType
    position: Tuple[float, float]
    start_time: float
    duration: float
    intensity: float = 1.0
    color: Tuple[int, int, int] = (255, 255, 255)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def progress(self) -> float:
        """Get effect progress (0.0 to 1.0)."""
        elapsed = time.time() - self.start_time
        return min(1.0, elapsed / self.duration)
    
    @property
    def is_finished(self) -> bool:
        """Check if effect has finished."""
        return self.progress >= 1.0
    
    def get_alpha(self) -> int:
        """Get current alpha value based on progress."""
        # Fade in quickly, fade out slowly
        if self.progress < 0.3:
            return int(255 * (self.progress / 0.3))
        else:
            return int(255 * (1.0 - (self.progress - 0.3) / 0.7))


class CombatEffectsSystem:
    """
    Main visual effects system for combat.
    
    Coordinates particle effects, animations, and visual feedback
    for all combat actions and state changes.
    """
    
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Core systems
        self.particle_system = ParticleSystem(max_particles=2000)
        self.audio_manager = get_audio_manager()
        
        # Active effects
        self.active_effects: List[VisualEffect] = []
        
        # Effect definitions
        self.effect_configs = self._initialize_effect_configs()
        
        # Animation timing
        self.last_update = time.time()
        
        # Screen shake system
        self.screen_shake_intensity = 0.0
        self.screen_shake_duration = 0.0
        self.screen_shake_start = 0.0
        
        logging.info("Combat Effects System initialized")
    
    def _initialize_effect_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize configuration for different effect types."""
        return {
            # Card play effects
            'attack_card': {
                'particle_type': ParticleType.COMBAT_HIT,
                'particle_count': 15,
                'color': (255, 100, 50),  # Orange-red fire
                'sound': SoundType.CARD_PLAY,
                'screen_shake': 0.3
            },
            'skill_card': {
                'particle_type': ParticleType.MAGIC_GLOW,
                'particle_count': 12,
                'color': (100, 150, 255),  # Blue magical light
                'sound': SoundType.CARD_PLAY,
                'screen_shake': 0.1
            },
            'power_card': {
                'particle_type': ParticleType.HEAL_SPARKLE,
                'particle_count': 20,
                'color': (255, 215, 0),   # Golden aura
                'sound': SoundType.CARD_PLAY,
                'screen_shake': 0.0
            },
            
            # Combat feedback effects
            'damage': {
                'particle_type': ParticleType.COMBAT_HIT,
                'particle_count': 8,
                'color': (255, 50, 50),   # Red damage
                'sound': SoundType.COMBAT_DAMAGE,
                'screen_shake': 0.4
            },
            'healing': {
                'particle_type': ParticleType.HEAL_SPARKLE,
                'particle_count': 10,
                'color': (100, 255, 100), # Green healing
                'sound': SoundType.COMBAT_HEAL,
                'screen_shake': 0.0
            },
            
            # Sand effects
            'sand_flow': {
                'particle_type': ParticleType.SAND_FLOW,
                'particle_count': 25,
                'color': (255, 215, 0),   # Golden sand
                'sound': SoundType.SAND_FLOW,
                'screen_shake': 0.0
            }
        }
    
    def trigger_card_play_effect(self, card_type: CardType, position: Tuple[float, float], 
                                intensity: float = 1.0) -> None:
        """Trigger visual effect for card being played."""
        
        # Get effect configuration
        config_key = f"{card_type.value}_card"
        config = self.effect_configs.get(config_key, self.effect_configs['attack_card'])
        
        # Create particle effect
        self._create_particle_burst(
            position, 
            config['particle_type'],
            int(config['particle_count'] * intensity),
            config['color']
        )
        
        # Add sand explosion for Egyptian theme
        self._create_sand_explosion(position, intensity)
        
        # Create visual effect object
        effect = VisualEffect(
            effect_type=EffectType.CARD_PLAY,
            position=position,
            start_time=time.time(),
            duration=1.0,
            intensity=intensity,
            color=config['color'],
            metadata={'card_type': card_type.value}
        )
        self.active_effects.append(effect)
        
        # Play sound
        self.audio_manager.play_sound(config['sound'], intensity * 0.8)
        
        # Screen shake for impact
        if config['screen_shake'] > 0:
            self.add_screen_shake(config['screen_shake'] * intensity, 0.3)
        
        logging.debug(f"Card play effect triggered: {card_type.value} at {position}")
    
    def trigger_damage_effect(self, position: Tuple[float, float], damage: int, 
                            is_critical: bool = False) -> None:
        """Trigger visual effect for damage dealt or received."""
        
        intensity = min(2.0, damage / 10.0)  # Scale with damage amount
        config = self.effect_configs['damage']
        
        # Create damage particles
        particle_count = int(config['particle_count'] * intensity)
        if is_critical:
            particle_count = int(particle_count * 1.5)
        
        self._create_particle_burst(
            position,
            config['particle_type'], 
            particle_count,
            config['color']
        )
        
        # Critical hit effects
        if is_critical:
            self._create_critical_hit_effect(position)
        
        # Create visual effect
        effect = VisualEffect(
            effect_type=EffectType.DAMAGE_DEALT,
            position=position,
            start_time=time.time(),
            duration=0.8,
            intensity=intensity,
            color=config['color'],
            metadata={'damage': damage, 'critical': is_critical}
        )
        self.active_effects.append(effect)
        
        # Audio and screen shake
        self.audio_manager.play_sound(config['sound'], min(1.0, intensity * 0.6))
        shake_intensity = config['screen_shake'] * intensity
        if is_critical:
            shake_intensity *= 1.5
        self.add_screen_shake(shake_intensity, 0.4)
    
    def trigger_healing_effect(self, position: Tuple[float, float], healing: int) -> None:
        """Trigger visual effect for healing."""
        
        intensity = min(1.5, healing / 15.0)
        config = self.effect_configs['healing']
        
        # Create healing sparkles
        self._create_particle_burst(
            position,
            config['particle_type'],
            int(config['particle_count'] * intensity),
            config['color']
        )
        
        # Add upward floating particles for healing theme
        self._create_floating_particles(position, intensity)
        
        # Create visual effect
        effect = VisualEffect(
            effect_type=EffectType.HEALING,
            position=position,
            start_time=time.time(),
            duration=1.2,
            intensity=intensity,
            color=config['color'],
            metadata={'healing': healing}
        )
        self.active_effects.append(effect)
        
        # Audio
        self.audio_manager.play_sound(config['sound'], min(1.0, intensity * 0.7))
    
    def trigger_sand_effect(self, start_pos: Tuple[float, float], 
                          end_pos: Tuple[float, float], sand_amount: int) -> None:
        """Trigger sand flow effect between two points."""
        
        intensity = min(1.0, sand_amount / 5.0)
        config = self.effect_configs['sand_flow']
        
        # Create sand flow particles
        self.particle_system.create_sand_flow_effect(
            start_pos[0], start_pos[1],
            end_pos[0], end_pos[1],
            intensity
        )
        
        # Create visual effect
        effect = VisualEffect(
            effect_type=EffectType.SAND_GAINED,
            position=end_pos,
            start_time=time.time(),
            duration=0.8,
            intensity=intensity,
            color=config['color'],
            metadata={'sand_amount': sand_amount}
        )
        self.active_effects.append(effect)
        
        # Audio
        self.audio_manager.play_sound(config['sound'], intensity * 0.5)
    
    def trigger_turn_transition(self, is_player_turn: bool) -> None:
        """Trigger visual effect for turn transitions."""
        
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Create sweeping sand effect across screen
        if is_player_turn:
            # Sand flows from left to right for player turn
            self._create_turn_sand_sweep(True)
            turn_color = (255, 215, 0)  # Golden for player
        else:
            # Sand flows from right to left for enemy turn  
            self._create_turn_sand_sweep(False)
            turn_color = (200, 100, 50)  # Darker sand for enemy
        
        # Create hourglass flip effect in center
        self._create_hourglass_flip_effect(center_x, center_y, is_player_turn)
        
        # Create turn effect
        effect = VisualEffect(
            effect_type=EffectType.TURN_START,
            position=(center_x, center_y),
            start_time=time.time(),
            duration=2.0,
            intensity=1.0,
            color=turn_color,
            metadata={'player_turn': is_player_turn}
        )
        self.active_effects.append(effect)
        
        # Audio
        self.audio_manager.play_sound(SoundType.UI_SCREEN_TRANSITION, 0.6)
    
    def trigger_damage_feedback(self, position: Tuple[float, float], damage: int,
                              damage_type: str = "physical", is_player_damage: bool = False) -> None:
        """Trigger enhanced damage feedback with type-specific effects."""
        
        intensity = min(2.5, damage / 8.0)
        
        # Color based on damage type
        damage_colors = {
            'physical': (255, 80, 80),     # Red
            'fire': (255, 150, 50),        # Orange
            'poison': (150, 255, 50),      # Green
            'divine': (255, 255, 150),     # Golden
            'shadow': (150, 50, 255),      # Purple
            'ice': (100, 200, 255)         # Blue
        }
        
        color = damage_colors.get(damage_type, damage_colors['physical'])
        
        # Enhanced particle effects for different damage types
        if damage_type == 'fire':
            self._create_fire_damage_effect(position, intensity)
        elif damage_type == 'poison':
            self._create_poison_damage_effect(position, intensity)
        elif damage_type == 'divine':
            self._create_divine_damage_effect(position, intensity)
        else:
            self._create_physical_damage_effect(position, intensity)
        
        # Damage number display effect
        self._create_damage_number_effect(position, damage, color, is_player_damage)
        
        # Screen shake based on damage
        shake_intensity = min(0.8, intensity * 0.3)
        if is_player_damage:
            shake_intensity *= 1.5  # Player damage is more impactful
        
        self.add_screen_shake(shake_intensity, 0.4)
    
    def trigger_healing_feedback(self, position: Tuple[float, float], healing: int,
                               healing_type: str = "divine") -> None:
        """Trigger enhanced healing feedback."""
        
        intensity = min(2.0, healing / 12.0)
        
        # Healing colors
        healing_colors = {
            'divine': (255, 255, 150),     # Golden divine
            'natural': (100, 255, 150),    # Green natural
            'magical': (150, 200, 255),    # Blue magical
            'regeneration': (200, 255, 100) # Light green regen
        }
        
        color = healing_colors.get(healing_type, healing_colors['divine'])
        
        # Enhanced healing effects
        self._create_enhanced_healing_effect(position, intensity, healing_type)
        
        # Healing number display
        self._create_healing_number_effect(position, healing, color)
    
    def trigger_status_effect_feedback(self, position: Tuple[float, float], 
                                     status_type: str, is_applied: bool = True) -> None:
        """Trigger feedback for status effects (buffs/debuffs)."""
        
        status_configs = {
            'strength': {'color': (255, 100, 100), 'particle_type': ParticleType.FIRE_SPARK},
            'dexterity': {'color': (100, 255, 100), 'particle_type': ParticleType.LIGHTNING_BOLT},
            'defense': {'color': (100, 100, 255), 'particle_type': ParticleType.GOLDEN_AURA},
            'poison': {'color': (150, 255, 50), 'particle_type': ParticleType.SAND_FLOW},
            'weak': {'color': (200, 200, 50), 'particle_type': ParticleType.MYSTICAL_RUNE},
            'vulnerable': {'color': (255, 150, 150), 'particle_type': ParticleType.COMBAT_HIT}
        }
        
        config = status_configs.get(status_type, status_configs['strength'])
        
        if is_applied:
            # Status applied - upward flowing effect
            self._create_status_application_effect(position, config, True)
        else:
            # Status removed - downward dispersing effect
            self._create_status_application_effect(position, config, False)
    
    def _create_particle_burst(self, position: Tuple[float, float], 
                             particle_type: ParticleType, count: int,
                             color: Tuple[int, int, int]) -> None:
        """Create a burst of particles at the specified position."""
        
        emitter = ParticleEmitter(position[0], position[1], particle_type)
        emitter.color = color
        emitter.emission_rate = 0  # Burst mode
        
        # Create particles in burst
        particles = emitter.burst(count)
        self.particle_system.particles.extend(particles)
    
    def _create_sand_explosion(self, position: Tuple[float, float], intensity: float) -> None:
        """Create Egyptian sand explosion effect."""
        
        # Create radiating sand particles
        particle_count = int(15 * intensity)
        
        for i in range(particle_count):
            angle = (i / particle_count) * 2 * math.pi
            speed = random.uniform(50, 150) * intensity
            
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x=position[0] + random.uniform(-10, 10),
                y=position[1] + random.uniform(-10, 10),
                vel_x=vel_x,
                vel_y=vel_y,
                size=random.uniform(1, 3),
                life=random.uniform(0.5, 1.2),
                max_life=1.0,
                color=(255, 215, 0),  # Golden sand
                alpha=255,
                gravity=30.0,
                particle_type=ParticleType.SAND_GRAIN
            )
            
            self.particle_system.particles.append(particle)
    
    def _create_critical_hit_effect(self, position: Tuple[float, float]) -> None:
        """Create special effect for critical hits."""
        
        # Create bright flash effect
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            distance = 30
            
            x = position[0] + math.cos(angle) * distance
            y = position[1] + math.sin(angle) * distance
            
            particle = Particle(
                x=x, y=y,
                vel_x=math.cos(angle) * 100,
                vel_y=math.sin(angle) * 100,
                size=4,
                life=0.3,
                max_life=0.3,
                color=(255, 255, 100),  # Bright yellow
                alpha=255,
                gravity=0,
                particle_type=ParticleType.COMBAT_HIT
            )
            
            self.particle_system.particles.append(particle)
    
    def _create_floating_particles(self, position: Tuple[float, float], intensity: float) -> None:
        """Create upward floating particles for healing effects."""
        
        particle_count = int(8 * intensity)
        
        for i in range(particle_count):
            particle = Particle(
                x=position[0] + random.uniform(-20, 20),
                y=position[1] + random.uniform(-10, 10),
                vel_x=random.uniform(-20, 20),
                vel_y=-random.uniform(30, 80),  # Upward movement
                size=random.uniform(2, 4),
                life=random.uniform(1.5, 2.5),
                max_life=2.0,
                color=(100, 255, 150),  # Light green
                alpha=255,
                gravity=-10.0,  # Float upward
                particle_type=ParticleType.HEAL_SPARKLE
            )
            
            self.particle_system.particles.append(particle)
    
    def _create_turn_sand_sweep(self, is_player_turn: bool) -> None:
        """Create sweeping sand effect for turn transitions."""
        center_y = self.screen_height // 2
        
        if is_player_turn:
            # Left to right sweep for player
            for i in range(25):
                x = i * (self.screen_width / 25)
                y = center_y + random.randint(-150, 150)
                
                self._create_particle_burst((x, y), ParticleType.SAND_FLOW, 8, (255, 215, 0))
                
                # Add delayed particles for wave effect
                delay_x = x + random.randint(10, 30)
                self._create_particle_burst((delay_x, y), ParticleType.SAND_GRAIN, 5, (255, 200, 50))
        else:
            # Right to left sweep for enemy
            for i in range(25):
                x = self.screen_width - (i * (self.screen_width / 25))
                y = center_y + random.randint(-150, 150)
                
                self._create_particle_burst((x, y), ParticleType.SAND_FLOW, 8, (200, 100, 50))
                
                # Add delayed particles
                delay_x = x - random.randint(10, 30)
                self._create_particle_burst((delay_x, y), ParticleType.SAND_GRAIN, 5, (180, 80, 30))
    
    def _create_hourglass_flip_effect(self, x: float, y: float, is_player_turn: bool) -> None:
        """Create hourglass flip effect in center of screen."""
        
        # Create sand falling effect
        sand_color = (255, 215, 0) if is_player_turn else (200, 100, 50)
        
        # Top sand falling down
        for i in range(15):
            fall_x = x + random.uniform(-20, 20)
            fall_y = y - 40 + random.uniform(-10, 10)
            
            particle = Particle(
                x=fall_x, y=fall_y,
                vel_x=random.uniform(-10, 10),
                vel_y=random.uniform(30, 80),  # Falling down
                size=random.uniform(1, 3),
                life=random.uniform(1.0, 2.0),
                max_life=1.5,
                color=sand_color,
                alpha=255,
                gravity=50.0,
                particle_type=ParticleType.SAND_GRAIN
            )
            self.particle_system.particles.append(particle)
        
        # Bottom sand accumulating
        for i in range(10):
            acc_x = x + random.uniform(-15, 15)
            acc_y = y + 40 + random.uniform(-5, 5)
            
            particle = Particle(
                x=acc_x, y=acc_y,
                vel_x=random.uniform(-5, 5),
                vel_y=random.uniform(-10, 10),
                size=random.uniform(1, 2),
                life=random.uniform(0.8, 1.5),
                max_life=1.0,
                color=sand_color,
                alpha=255,
                gravity=20.0,
                particle_type=ParticleType.SAND_GRAIN
            )
            self.particle_system.particles.append(particle)
    
    def _create_fire_damage_effect(self, position: Tuple[float, float], intensity: float) -> None:
        """Create fire damage effect."""
        x, y = position
        
        # Fire burst
        for i in range(int(10 * intensity)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(40, 120) * intensity
            
            particle = Particle(
                x=x + random.uniform(-8, 8),
                y=y + random.uniform(-8, 8),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(2, 5),
                life=random.uniform(0.6, 1.2),
                max_life=1.0,
                color=(255, random.randint(50, 150), 30),  # Fire colors
                alpha=255,
                gravity=30.0,
                particle_type=ParticleType.FIRE_SPARK
            )
            self.particle_system.particles.append(particle)
    
    def _create_poison_damage_effect(self, position: Tuple[float, float], intensity: float) -> None:
        """Create poison damage effect."""
        x, y = position
        
        # Bubbling poison effect
        for i in range(int(8 * intensity)):
            bubble_x = x + random.uniform(-12, 12)
            bubble_y = y + random.uniform(-12, 12)
            
            particle = Particle(
                x=bubble_x, y=bubble_y,
                vel_x=random.uniform(-20, 20),
                vel_y=-random.uniform(20, 60),  # Float upward
                size=random.uniform(2, 4),
                life=random.uniform(1.0, 2.0),
                max_life=1.5,
                color=(150, 255, 50),  # Poison green
                alpha=255,
                gravity=-10.0,  # Poison bubbles float
                particle_type=ParticleType.SAND_FLOW
            )
            self.particle_system.particles.append(particle)
    
    def _create_divine_damage_effect(self, position: Tuple[float, float], intensity: float) -> None:
        """Create divine damage effect."""
        x, y = position
        
        # Divine light rays
        for i in range(int(12 * intensity)):
            angle = (i / (12 * intensity)) * 2 * math.pi
            speed = random.uniform(60, 100) * intensity
            
            particle = Particle(
                x=x, y=y,
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(1, 3),
                life=random.uniform(0.8, 1.5),
                max_life=1.2,
                color=(255, 255, 150),  # Golden divine
                alpha=255,
                gravity=0.0,  # Divine light floats
                particle_type=ParticleType.GOLDEN_AURA
            )
            self.particle_system.particles.append(particle)
    
    def _create_physical_damage_effect(self, position: Tuple[float, float], intensity: float) -> None:
        """Create physical damage effect."""
        x, y = position
        
        # Impact sparks
        for i in range(int(8 * intensity)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 90) * intensity
            
            particle = Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vel_x=math.cos(angle) * speed,
                vel_y=math.sin(angle) * speed,
                size=random.uniform(1, 3),
                life=random.uniform(0.4, 0.8),
                max_life=0.6,
                color=(255, 80, 80),  # Red impact
                alpha=255,
                gravity=40.0,
                particle_type=ParticleType.COMBAT_HIT
            )
            self.particle_system.particles.append(particle)
    
    def _create_damage_number_effect(self, position: Tuple[float, float], damage: int,
                                   color: Tuple[int, int, int], is_player_damage: bool) -> None:
        """Create floating damage number effect."""
        x, y = position
        
        # Create visual effect for damage number (would need font rendering in full implementation)
        effect = VisualEffect(
            effect_type=EffectType.DAMAGE_DEALT if not is_player_damage else EffectType.DAMAGE_RECEIVED,
            position=(x, y - 20),  # Float upward
            start_time=time.time(),
            duration=1.2,
            intensity=min(2.0, damage / 10.0),
            color=color,
            metadata={'damage_value': damage, 'is_player': is_player_damage}
        )
        self.active_effects.append(effect)
    
    def _create_enhanced_healing_effect(self, position: Tuple[float, float], intensity: float,
                                      healing_type: str) -> None:
        """Create enhanced healing effect based on type."""
        x, y = position
        
        if healing_type == 'divine':
            # Golden divine healing
            for i in range(int(15 * intensity)):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(20, 60) * intensity
                
                particle = Particle(
                    x=x + random.uniform(-10, 10),
                    y=y + random.uniform(-10, 10),
                    vel_x=math.cos(angle) * speed,
                    vel_y=-random.uniform(30, 70),  # Float upward
                    size=random.uniform(2, 4),
                    life=random.uniform(1.5, 2.5),
                    max_life=2.0,
                    color=(255, 255, 150),  # Golden
                    alpha=255,
                    gravity=-15.0,
                    particle_type=ParticleType.HEAL_SPARKLE
                )
                self.particle_system.particles.append(particle)
        
        elif healing_type == 'natural':
            # Green natural healing
            for i in range(int(12 * intensity)):
                particle = Particle(
                    x=x + random.uniform(-15, 15),
                    y=y + random.uniform(-10, 10),
                    vel_x=random.uniform(-30, 30),
                    vel_y=-random.uniform(20, 50),
                    size=random.uniform(1, 3),
                    life=random.uniform(1.0, 2.0),
                    max_life=1.5,
                    color=(100, 255, 150),  # Green
                    alpha=255,
                    gravity=-20.0,
                    particle_type=ParticleType.HEAL_SPARKLE
                )
                self.particle_system.particles.append(particle)
    
    def _create_healing_number_effect(self, position: Tuple[float, float], healing: int,
                                    color: Tuple[int, int, int]) -> None:
        """Create floating healing number effect."""
        x, y = position
        
        effect = VisualEffect(
            effect_type=EffectType.HEALING,
            position=(x, y - 25),  # Float upward more than damage
            start_time=time.time(),
            duration=1.5,
            intensity=min(1.5, healing / 15.0),
            color=color,
            metadata={'healing_value': healing}
        )
        self.active_effects.append(effect)
    
    def _create_status_application_effect(self, position: Tuple[float, float], 
                                        config: Dict[str, Any], is_applied: bool) -> None:
        """Create status effect application/removal visual."""
        x, y = position
        
        if is_applied:
            # Status applied - upward swirl
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                radius = 20
                
                particle = Particle(
                    x=x + math.cos(angle) * radius,
                    y=y + math.sin(angle) * radius,
                    vel_x=-math.cos(angle) * 30,
                    vel_y=-math.sin(angle) * 30 - 20,  # Upward
                    size=random.uniform(2, 4),
                    life=random.uniform(1.0, 1.8),
                    max_life=1.4,
                    color=config['color'],
                    alpha=255,
                    gravity=-10.0,
                    particle_type=config['particle_type']
                )
                self.particle_system.particles.append(particle)
        else:
            # Status removed - dispersing effect
            for i in range(6):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(40, 80)
                
                particle = Particle(
                    x=x + random.uniform(-8, 8),
                    y=y + random.uniform(-8, 8),
                    vel_x=math.cos(angle) * speed,
                    vel_y=math.sin(angle) * speed,
                    size=random.uniform(1, 3),
                    life=random.uniform(0.5, 1.0),
                    max_life=0.8,
                    color=config['color'],
                    alpha=255,
                    gravity=20.0,
                    particle_type=config['particle_type']
                )
                self.particle_system.particles.append(particle)
    
    def add_screen_shake(self, intensity: float, duration: float) -> None:
        """Add screen shake effect."""
        self.screen_shake_intensity = max(self.screen_shake_intensity, intensity)
        self.screen_shake_duration = max(self.screen_shake_duration, duration)
        self.screen_shake_start = time.time()
    
    def get_screen_offset(self) -> Tuple[int, int]:
        """Get current screen offset for shake effect."""
        if self.screen_shake_duration <= 0:
            return (0, 0)
        
        elapsed = time.time() - self.screen_shake_start
        if elapsed >= self.screen_shake_duration:
            self.screen_shake_intensity = 0
            self.screen_shake_duration = 0
            return (0, 0)
        
        # Calculate shake intensity with decay
        progress = elapsed / self.screen_shake_duration
        current_intensity = self.screen_shake_intensity * (1.0 - progress)
        
        # Random shake offset
        max_offset = int(current_intensity * 10)
        offset_x = random.randint(-max_offset, max_offset)
        offset_y = random.randint(-max_offset, max_offset)
        
        return (offset_x, offset_y)
    
    def update(self, delta_time: float) -> None:
        """Update all visual effects."""
        current_time = time.time()
        
        # Update particle system
        self.particle_system.update(delta_time)
        
        # Remove finished effects
        self.active_effects = [effect for effect in self.active_effects if not effect.is_finished]
        
        self.last_update = current_time
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all visual effects."""
        
        # Apply screen shake offset
        shake_offset = self.get_screen_offset()
        if shake_offset != (0, 0):
            # Create temporary surface with shake offset
            temp_surface = surface.copy()
            surface.fill((0, 0, 0))  # Clear screen
            surface.blit(temp_surface, shake_offset)
        
        # Render particle system
        self.particle_system.render(surface)
        
        # Render special effects
        for effect in self.active_effects:
            self._render_effect(surface, effect)
    
    def _render_effect(self, surface: pygame.Surface, effect: VisualEffect) -> None:
        """Render an individual visual effect."""
        
        alpha = effect.get_alpha()
        if alpha <= 0:
            return
        
        x, y = effect.position
        
        # Create effect-specific visuals
        if effect.effect_type == EffectType.CARD_PLAY:
            self._render_card_play_effect(surface, effect, alpha)
        
        elif effect.effect_type in [EffectType.DAMAGE_DEALT, EffectType.DAMAGE_RECEIVED]:
            self._render_damage_effect(surface, effect, alpha)
        
        elif effect.effect_type == EffectType.HEALING:
            self._render_healing_effect(surface, effect, alpha)
        
        elif effect.effect_type == EffectType.TURN_START:
            self._render_turn_transition_effect(surface, effect, alpha)
    
    def _render_card_play_effect(self, surface: pygame.Surface, effect: VisualEffect, alpha: int) -> None:
        """Render card play effect."""
        x, y = effect.position
        progress = effect.progress
        
        # Expanding circle effect
        radius = int(30 * progress * effect.intensity)
        if radius > 0:
            color_with_alpha = (*effect.color, alpha)
            
            # Draw expanding ring
            if radius > 5:
                pygame.draw.circle(surface, effect.color, (int(x), int(y)), radius, 3)
            
            # Draw inner glow
            inner_radius = max(1, radius // 2)
            glow_color = tuple(min(255, c + 50) for c in effect.color)
            pygame.draw.circle(surface, glow_color, (int(x), int(y)), inner_radius)
    
    def _render_damage_effect(self, surface: pygame.Surface, effect: VisualEffect, alpha: int) -> None:
        """Render damage effect with impact visual."""
        x, y = effect.position
        progress = effect.progress
        
        # Flash effect for damage
        if progress < 0.2:  # Quick flash
            flash_intensity = (0.2 - progress) / 0.2
            flash_radius = int(25 * effect.intensity)
            
            flash_color = tuple(min(255, int(c * flash_intensity)) for c in effect.color)
            pygame.draw.circle(surface, flash_color, (int(x), int(y)), flash_radius)
    
    def _render_healing_effect(self, surface: pygame.Surface, effect: VisualEffect, alpha: int) -> None:
        """Render healing effect with upward energy."""
        x, y = effect.position
        progress = effect.progress
        
        # Upward energy streams
        stream_height = int(40 * progress)
        stream_y = y - stream_height
        
        if stream_height > 0:
            # Draw energy stream
            pygame.draw.line(surface, effect.color, (int(x), int(y)), (int(x), int(stream_y)), 3)
            
            # Draw energy orb at top
            pygame.draw.circle(surface, effect.color, (int(x), int(stream_y)), 5)
    
    def _render_turn_transition_effect(self, surface: pygame.Surface, effect: VisualEffect, alpha: int) -> None:
        """Render turn transition effect."""
        progress = effect.progress
        
        # Sweeping line across screen
        if progress < 0.8:
            line_progress = progress / 0.8
            line_x = int(self.screen_width * line_progress)
            
            # Draw sweeping line
            pygame.draw.line(surface, effect.color, 
                           (line_x, 0), (line_x, self.screen_height), 5)
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.active_effects.clear()
        self.particle_system.clear_all()
        self.screen_shake_intensity = 0
        self.screen_shake_duration = 0
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'active_effects': len(self.active_effects),
            'particle_count': self.particle_system.get_particle_count(),
            'screen_shake_active': self.screen_shake_intensity > 0,
            'effect_types': [effect.effect_type.value for effect in self.active_effects]
        }


# Global combat effects system
_combat_effects_system: Optional[CombatEffectsSystem] = None


def get_combat_effects_system() -> CombatEffectsSystem:
    """Get the global combat effects system instance."""
    global _combat_effects_system
    if _combat_effects_system is None:
        _combat_effects_system = CombatEffectsSystem()
    return _combat_effects_system


def initialize_combat_effects_system(screen_width: int = 1200, screen_height: int = 800) -> CombatEffectsSystem:
    """Initialize the global combat effects system."""
    global _combat_effects_system
    _combat_effects_system = CombatEffectsSystem(screen_width, screen_height)
    return _combat_effects_system