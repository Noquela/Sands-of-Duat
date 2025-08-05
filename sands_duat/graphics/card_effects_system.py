"""
Advanced Card Visual Effects System

Creates cinematic card animations, hover effects, play animations,
and rarity-based visual treatments that respond to user interaction.
"""

import pygame
import math
import random
import time
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import colorsys


class CardRarity(Enum):
    """Card rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class CardType(Enum):
    """Card types for different effect styles."""
    ATTACK = "attack"
    SKILL = "skill"
    POWER = "power"
    STATUS = "status"
    CURSE = "curse"
    BLESSING = "blessing"


class EffectState(Enum):
    """Current state of card effects."""
    IDLE = "idle"
    HOVER = "hover"
    SELECTED = "selected"
    PLAYING = "playing"
    RETURNING = "returning"


@dataclass
class CardEffectProperties:
    """Visual effect properties for a card."""
    # Base properties
    glow_intensity: float = 0.0
    glow_color: Tuple[int, int, int] = (255, 255, 255)
    glow_radius: float = 0.0
    
    # Animation properties
    scale: float = 1.0
    rotation: float = 0.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    alpha: int = 255
    
    # Particle effects
    particle_emission_rate: float = 0.0
    particle_color: Tuple[int, int, int] = (255, 255, 255)
    particle_size_range: Tuple[float, float] = (1.0, 3.0)
    
    # Magical aura
    aura_layers: List[Dict[str, Any]] = field(default_factory=list)
    energy_trails: List[Dict[str, Any]] = field(default_factory=list)
    
    # Animation state
    animation_time: float = 0.0
    state_transition_progress: float = 0.0
    
    # Egyptian mystical effects
    ankh_symbols: List[Dict[str, Any]] = field(default_factory=list)
    hieroglyph_effects: List[Dict[str, Any]] = field(default_factory=list)
    
    # Screen effects
    screen_distortion: float = 0.0
    chromatic_aberration: float = 0.0
    bloom_intensity: float = 0.0


class CardEffectsSystem:
    """Main system for managing card visual effects."""
    
    def __init__(self):
        self.card_effects: Dict[str, CardEffectProperties] = {}
        self.global_particle_system = None  # Will be set externally
        
        # Effect presets by rarity
        self.rarity_presets = self._create_rarity_presets()
        self.type_presets = self._create_type_presets()
        
        # Animation settings
        self.hover_scale_target = 1.05
        self.hover_glow_intensity = 0.8
        self.play_scale_target = 1.2
        self.play_glow_intensity = 1.5
        
        # Timing settings
        self.hover_transition_speed = 3.0
        self.play_animation_duration = 1.0
        self.return_animation_duration = 0.5
        
        # Performance settings
        self.max_active_effects = 50
        self.effect_quality = "high"  # low, medium, high
    
    def _create_rarity_presets(self) -> Dict[CardRarity, Dict[str, Any]]:
        """Create visual presets for each rarity level."""
        return {
            CardRarity.COMMON: {
                "glow_color": (200, 200, 200),
                "glow_intensity": 0.3,
                "particle_count": 5,
                "aura_layers": 1,
                "mystical_effects": False
            },
            CardRarity.UNCOMMON: {
                "glow_color": (100, 255, 100),
                "glow_intensity": 0.5,
                "particle_count": 10,
                "aura_layers": 2,
                "mystical_effects": False
            },
            CardRarity.RARE: {
                "glow_color": (100, 150, 255),
                "glow_intensity": 0.7,
                "particle_count": 15,
                "aura_layers": 3,
                "mystical_effects": True,
                "screen_effects": True
            },
            CardRarity.EPIC: {
                "glow_color": (200, 100, 255),
                "glow_intensity": 1.0,
                "particle_count": 25,
                "aura_layers": 4,
                "mystical_effects": True,
                "screen_effects": True,
                "chromatic_aberration": True
            },
            CardRarity.LEGENDARY: {
                "glow_color": (255, 215, 0),
                "glow_intensity": 1.5,
                "particle_count": 40,
                "aura_layers": 5,
                "mystical_effects": True,
                "screen_effects": True,
                "chromatic_aberration": True,
                "bloom_effect": True
            }
        }
    
    def _create_type_presets(self) -> Dict[CardType, Dict[str, Any]]:
        """Create visual presets for each card type."""
        return {
            CardType.ATTACK: {
                "primary_color": (255, 100, 50),
                "particle_type": "fire_spark",
                "energy_color": (255, 150, 0),
                "mystical_symbol": "flame"
            },
            CardType.SKILL: {
                "primary_color": (100, 150, 255),
                "particle_type": "lightning_bolt",
                "energy_color": (150, 200, 255),
                "mystical_symbol": "lightning"
            },
            CardType.POWER: {
                "primary_color": (255, 215, 0),
                "particle_type": "golden_aura",
                "energy_color": (255, 235, 100),
                "mystical_symbol": "ankh"
            },
            CardType.STATUS: {
                "primary_color": (150, 50, 200),
                "particle_type": "mystical_rune",
                "energy_color": (200, 100, 255),
                "mystical_symbol": "hieroglyph"
            },
            CardType.CURSE: {
                "primary_color": (150, 50, 50),
                "particle_type": "shadow_tendril",
                "energy_color": (200, 80, 80),
                "mystical_symbol": "curse_mark"
            },
            CardType.BLESSING: {
                "primary_color": (255, 255, 150),
                "particle_type": "spirit_wisp",
                "energy_color": (255, 255, 200),
                "mystical_symbol": "blessing_light"
            }
        }
    
    def register_card(self, card_id: str, card_type: CardType, rarity: CardRarity) -> None:
        """Register a card with the effects system."""
        if card_id not in self.card_effects:
            effects = CardEffectProperties()
            
            # Apply rarity preset
            rarity_preset = self.rarity_presets[rarity]
            effects.glow_color = rarity_preset["glow_color"]
            effects.glow_intensity = 0.0  # Start with no glow
            
            # Apply type preset
            type_preset = self.type_presets[card_type]
            effects.particle_color = type_preset["primary_color"]
            
            # Initialize mystical effects for higher rarities
            if rarity in [CardRarity.RARE, CardRarity.EPIC, CardRarity.LEGENDARY]:
                self._initialize_mystical_effects(effects, card_type, rarity)
            
            self.card_effects[card_id] = effects
    
    def _initialize_mystical_effects(self, effects: CardEffectProperties, card_type: CardType, rarity: CardRarity) -> None:
        """Initialize mystical effects for high-rarity cards."""
        type_preset = self.type_presets[card_type]
        rarity_preset = self.rarity_presets[rarity]
        
        # Initialize aura layers
        for i in range(rarity_preset["aura_layers"]):
            aura_layer = {
                "radius": 20 + i * 15,
                "alpha": 100 - i * 20,
                "color": type_preset["primary_color"],
                "pulse_speed": 2.0 + i * 0.5,
                "rotation_speed": 1.0 + i * 0.3
            }
            effects.aura_layers.append(aura_layer)
        
        # Initialize Egyptian mystical symbols
        if card_type == CardType.POWER:
            # Ankh symbols for power cards
            for _ in range(3):
                ankh = {
                    "x": random.uniform(-30, 30),
                    "y": random.uniform(-40, 40),
                    "size": random.uniform(8, 15),
                    "rotation": random.uniform(0, 2 * math.pi),
                    "rotation_speed": random.uniform(-1, 1),
                    "alpha": random.randint(100, 200),
                    "pulse_speed": random.uniform(1, 3)
                }
                effects.ankh_symbols.append(ankh)
        
        elif card_type in [CardType.STATUS, CardType.BLESSING]:
            # Hieroglyph effects for mystical cards
            for _ in range(4):
                hieroglyph = {
                    "x": random.uniform(-25, 25),
                    "y": random.uniform(-35, 35),
                    "pattern_type": random.choice(["circle", "triangle", "lines"]),
                    "size": random.uniform(6, 12),
                    "rotation": random.uniform(0, 2 * math.pi),
                    "float_amplitude": random.uniform(2, 8),
                    "float_speed": random.uniform(0.5, 2.0),
                    "alpha": random.randint(80, 150)
                }
                effects.hieroglyph_effects.append(hieroglyph)
    
    def set_card_state(self, card_id: str, state: EffectState, transition_speed: float = None) -> None:
        """Set the visual state of a card."""
        if card_id not in self.card_effects:
            return
        
        effects = self.card_effects[card_id]
        speed = transition_speed or self.hover_transition_speed
        
        if state == EffectState.HOVER:
            effects.state_transition_progress = 0.0
            self._animate_to_hover_state(effects, speed)
        
        elif state == EffectState.SELECTED:
            self._animate_to_selected_state(effects, speed)
        
        elif state == EffectState.PLAYING:
            self._animate_to_playing_state(effects)
        
        elif state == EffectState.RETURNING:
            self._animate_to_idle_state(effects, self.return_animation_duration)
        
        else:  # IDLE
            self._animate_to_idle_state(effects, speed)
    
    def _animate_to_hover_state(self, effects: CardEffectProperties, speed: float) -> None:
        """Animate card to hover state."""
        # Target values for hover state
        effects.scale = self.hover_scale_target
        effects.glow_intensity = self.hover_glow_intensity
        effects.glow_radius = 20.0
        effects.offset_y = -5.0  # Slight lift
        
        # Start particle emission
        effects.particle_emission_rate = 5.0
    
    def _animate_to_selected_state(self, effects: CardEffectProperties, speed: float) -> None:
        """Animate card to selected state."""
        effects.scale = 1.08
        effects.glow_intensity = 1.0
        effects.glow_radius = 25.0
        effects.offset_y = -8.0
        
        # Increase particle emission
        effects.particle_emission_rate = 10.0
        
        # Add pulsing effect
        for aura in effects.aura_layers:
            aura["pulse_speed"] *= 1.5
    
    def _animate_to_playing_state(self, effects: CardEffectProperties) -> None:
        """Animate card to playing state with dramatic effects."""
        effects.scale = self.play_scale_target
        effects.glow_intensity = self.play_glow_intensity
        effects.glow_radius = 40.0
        effects.offset_y = -15.0
        
        # Maximum particle emission
        effects.particle_emission_rate = 30.0
        
        # Screen effects for rare+ cards
        if len(effects.aura_layers) >= 3:
            effects.screen_distortion = 0.1
            effects.bloom_intensity = 0.3
        
        if len(effects.aura_layers) >= 4:
            effects.chromatic_aberration = 0.05
        
        # Enhance mystical effects
        for ankh in effects.ankh_symbols:
            ankh["rotation_speed"] *= 2.0
            ankh["pulse_speed"] *= 1.5
        
        for hieroglyph in effects.hieroglyph_effects:
            hieroglyph["float_amplitude"] *= 2.0
            hieroglyph["float_speed"] *= 1.5
    
    def _animate_to_idle_state(self, effects: CardEffectProperties, duration: float) -> None:
        """Animate card back to idle state."""
        effects.scale = 1.0
        effects.glow_intensity = 0.0
        effects.glow_radius = 0.0
        effects.offset_x = 0.0
        effects.offset_y = 0.0
        effects.particle_emission_rate = 0.0
        
        # Reset screen effects
        effects.screen_distortion = 0.0
        effects.chromatic_aberration = 0.0
        effects.bloom_intensity = 0.0
        
        # Reset mystical effects to base state
        for aura in effects.aura_layers:
            aura["pulse_speed"] = 2.0
        
        for ankh in effects.ankh_symbols:
            ankh["rotation_speed"] = random.uniform(-1, 1)
            ankh["pulse_speed"] = random.uniform(1, 3)
        
        for hieroglyph in effects.hieroglyph_effects:
            hieroglyph["float_amplitude"] = random.uniform(2, 8)
            hieroglyph["float_speed"] = random.uniform(0.5, 2.0)
    
    def update(self, delta_time: float) -> None:
        """Update all card effects."""
        current_time = time.time()
        
        for card_id, effects in self.card_effects.items():
            self._update_card_effects(effects, delta_time, current_time)
    
    def _update_card_effects(self, effects: CardEffectProperties, delta_time: float, current_time: float) -> None:
        """Update individual card effects."""
        effects.animation_time += delta_time
        
        # Update aura layers
        for aura in effects.aura_layers:
            # Pulsing effect
            pulse = math.sin(current_time * aura["pulse_speed"]) * 0.3 + 0.7
            aura["current_alpha"] = int(aura["alpha"] * pulse)
            
            # Rotation
            aura["rotation"] = (aura.get("rotation", 0) + aura["rotation_speed"] * delta_time) % (2 * math.pi)
        
        # Update ankh symbols
        for ankh in effects.ankh_symbols:
            ankh["rotation"] += ankh["rotation_speed"] * delta_time
            
            # Pulsing alpha
            pulse = math.sin(current_time * ankh["pulse_speed"]) * 0.4 + 0.6
            ankh["current_alpha"] = int(ankh["alpha"] * pulse)
        
        # Update hieroglyph effects
        for hieroglyph in effects.hieroglyph_effects:
            # Floating motion
            hieroglyph["float_time"] = hieroglyph.get("float_time", 0) + hieroglyph["float_speed"] * delta_time
            hieroglyph["current_y"] = hieroglyph["y"] + math.sin(hieroglyph["float_time"]) * hieroglyph["float_amplitude"]
            
            # Rotation
            hieroglyph["rotation"] += 0.5 * delta_time  # Slow rotation
            
            # Pulsing alpha
            pulse = math.sin(current_time * 2 + hieroglyph["float_time"]) * 0.3 + 0.7
            hieroglyph["current_alpha"] = int(hieroglyph["alpha"] * pulse)
    
    def render_card_effects(self, surface: pygame.Surface, card_rect: pygame.Rect, card_id: str) -> None:
        """Render visual effects for a specific card."""
        if card_id not in self.card_effects:
            return
        
        effects = self.card_effects[card_id]
        center_x = card_rect.centerx + effects.offset_x
        center_y = card_rect.centery + effects.offset_y
        
        # Render aura layers (back to front)
        for aura in reversed(effects.aura_layers):
            self._render_aura_layer(surface, center_x, center_y, aura, effects)
        
        # Render glow effect
        if effects.glow_intensity > 0:
            self._render_glow_effect(surface, card_rect, effects)
        
        # Render mystical effects
        self._render_mystical_effects(surface, center_x, center_y, effects)
        
        # Generate particles if needed
        if effects.particle_emission_rate > 0 and self.global_particle_system:
            self._emit_card_particles(center_x, center_y, effects)
    
    def _render_aura_layer(self, surface: pygame.Surface, center_x: float, center_y: float, 
                          aura: Dict[str, Any], effects: CardEffectProperties) -> None:
        """Render individual aura layer."""
        if "current_alpha" not in aura or aura["current_alpha"] <= 0:
            return
        
        try:
            # Create aura surface
            aura_size = int(aura["radius"] * 2)
            if aura_size <= 0:
                return
            
            aura_surface = pygame.Surface((aura_size, aura_size), pygame.SRCALPHA)
            
            # Draw aura with gradient effect
            color = (*aura["color"], min(255, aura["current_alpha"]))
            
            # Multiple circles for smooth gradient
            steps = 8 if self.effect_quality == "high" else 4
            for i in range(steps):
                radius_factor = (steps - i) / steps
                current_radius = int(aura["radius"] * radius_factor)
                alpha_factor = radius_factor * radius_factor  # Quadratic falloff
                circle_alpha = int(aura["current_alpha"] * alpha_factor)
                
                if circle_alpha > 0 and current_radius > 0:
                    circle_color = (*aura["color"], circle_alpha)
                    pygame.draw.circle(aura_surface, circle_color, 
                                     (aura_size // 2, aura_size // 2), current_radius)
            
            # Apply rotation if present
            if "rotation" in aura and aura["rotation"] != 0:
                aura_surface = pygame.transform.rotate(aura_surface, math.degrees(aura["rotation"]))
            
            # Blit to main surface
            aura_rect = aura_surface.get_rect(center=(int(center_x), int(center_y)))
            surface.blit(aura_surface, aura_rect, special_flags=pygame.BLEND_ADD)
            
        except Exception:
            # Fail silently for aura rendering errors
            pass
    
    def _render_glow_effect(self, surface: pygame.Surface, card_rect: pygame.Rect, effects: CardEffectProperties) -> None:
        """Render card glow effect."""
        if effects.glow_radius <= 0:
            return
        
        try:
            glow_size = int(effects.glow_radius * 2)
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Create glow gradient
            alpha = int(255 * effects.glow_intensity * 0.5)
            if alpha <= 0:
                return
            
            color = (*effects.glow_color, alpha)
            pygame.draw.circle(glow_surface, color, (glow_size // 2, glow_size // 2), int(effects.glow_radius))
            
            # Blit glow behind card
            glow_rect = glow_surface.get_rect(center=card_rect.center)
            surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
            
        except Exception:
            # Fail silently for glow rendering errors
            pass
    
    def _render_mystical_effects(self, surface: pygame.Surface, center_x: float, center_y: float, effects: CardEffectProperties) -> None:
        """Render Egyptian mystical effects."""
        # Render ankh symbols
        for ankh in effects.ankh_symbols:
            if "current_alpha" in ankh and ankh["current_alpha"] > 0:
                self._render_ankh_symbol(surface, center_x + ankh["x"], center_y + ankh["y"], ankh)
        
        # Render hieroglyph effects
        for hieroglyph in effects.hieroglyph_effects:
            if "current_alpha" in hieroglyph and hieroglyph["current_alpha"] > 0:
                hiero_y = center_y + hieroglyph.get("current_y", hieroglyph["y"])
                self._render_hieroglyph(surface, center_x + hieroglyph["x"], hiero_y, hieroglyph)
    
    def _render_ankh_symbol(self, surface: pygame.Surface, x: float, y: float, ankh: Dict[str, Any]) -> None:
        """Render ankh symbol."""
        try:
            size = int(ankh["size"])
            alpha = ankh["current_alpha"]
            color = (255, 215, 0, alpha)  # Golden ankh
            
            # Draw ankh shape
            center_x, center_y = int(x), int(y)
            
            # Cross part
            pygame.draw.line(surface, color[:3], 
                           (center_x, center_y - size), (center_x, center_y + size), 2)
            pygame.draw.line(surface, color[:3], 
                           (center_x - size//2, center_y - size//3), 
                           (center_x + size//2, center_y - size//3), 2)
            
            # Loop part
            loop_radius = size // 3
            pygame.draw.circle(surface, color[:3], (center_x, center_y - size//2), loop_radius, 1)
            
        except Exception:
            pass
    
    def _render_hieroglyph(self, surface: pygame.Surface, x: float, y: float, hieroglyph: Dict[str, Any]) -> None:
        """Render hieroglyph symbol."""
        try:
            size = int(hieroglyph["size"])
            alpha = hieroglyph["current_alpha"]
            color = (138, 43, 226)  # Purple mystical color
            
            center_x, center_y = int(x), int(y)
            
            # Draw based on pattern type
            if hieroglyph["pattern_type"] == "circle":
                pygame.draw.circle(surface, color, (center_x, center_y), size, 2)
                pygame.draw.circle(surface, color, (center_x, center_y), size // 2)
            
            elif hieroglyph["pattern_type"] == "triangle":
                points = [
                    (center_x, center_y - size),
                    (center_x - size, center_y + size),
                    (center_x + size, center_y + size)
                ]
                pygame.draw.polygon(surface, color, points, 2)
            
            else:  # lines
                pygame.draw.line(surface, color, 
                               (center_x - size, center_y), (center_x + size, center_y), 2)
                pygame.draw.line(surface, color, 
                               (center_x, center_y - size), (center_x, center_y + size), 2)
        
        except Exception:
            pass
    
    def _emit_card_particles(self, x: float, y: float, effects: CardEffectProperties) -> None:
        """Emit particles for card effects."""
        if not self.global_particle_system:
            return
        
        # Emit particles based on emission rate
        particle_count = int(effects.particle_emission_rate * 0.016)  # 60 FPS assumption
        
        for _ in range(particle_count):
            # Create particle around card area
            particle_x = x + random.uniform(-50, 50)
            particle_y = y + random.uniform(-70, 70)
            
            # Use the particle system to create appropriate effect
            if hasattr(self.global_particle_system, 'create_cinematic_card_effect'):
                self.global_particle_system.create_cinematic_card_effect(
                    "power", particle_x, particle_y, "rare", 0.5
                )
    
    def set_particle_system(self, particle_system) -> None:
        """Set the global particle system reference."""
        self.global_particle_system = particle_system
    
    def create_play_effect(self, card_id: str, card_rect: pygame.Rect, target_pos: Tuple[int, int]) -> None:
        """Create dramatic effect when card is played."""
        if card_id not in self.card_effects:
            return
        
        effects = self.card_effects[card_id]
        
        # Set playing state
        self.set_card_state(card_id, EffectState.PLAYING)
        
        # Create screen-wide effects for rare+ cards
        if len(effects.aura_layers) >= 3 and self.global_particle_system:
            # Screen shake for epic+ cards
            if len(effects.aura_layers) >= 4:
                # Trigger screen shake in particle system if available
                pass
            
            # Create particle trail from card to target
            start_x, start_y = card_rect.center
            end_x, end_y = target_pos
            
            if hasattr(self.global_particle_system, 'create_enhanced_sand_effect'):
                self.global_particle_system.create_enhanced_sand_effect(
                    start_x, start_y, end_x, end_y, 2.0
                )
    
    def get_card_effect_properties(self, card_id: str) -> Optional[CardEffectProperties]:
        """Get effect properties for a card."""
        return self.card_effects.get(card_id)
    
    def remove_card(self, card_id: str) -> None:
        """Remove card from effects system."""
        if card_id in self.card_effects:
            del self.card_effects[card_id]
    
    def clear_all_effects(self) -> None:
        """Clear all card effects."""
        self.card_effects.clear()


# Global card effects system
_global_card_effects_system = None

def get_card_effects_system() -> CardEffectsSystem:
    """Get global card effects system."""
    global _global_card_effects_system
    if _global_card_effects_system is None:
        _global_card_effects_system = CardEffectsSystem()
    return _global_card_effects_system