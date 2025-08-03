"""
Combat Sound Effects System

Egyptian-themed audio system for combat actions, providing immersive
sound effects that match the visual effects and enhance gameplay.

Features:
- Card-specific sound effects
- Egyptian instrument sounds (sistrum, drums, etc.)
- Combat feedback audio
- Layered ambient soundscapes
- Dynamic volume and spatial audio
"""

import pygame
import random
import math
import logging
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass

from .audio_manager import get_audio_manager, SoundType


class CombatSoundType(Enum):
    """Combat-specific sound effect types."""
    # Card sounds
    CARD_ATTACK = "card_attack"
    CARD_SKILL = "card_skill"
    CARD_POWER = "card_power"
    CARD_STATUS = "card_status"
    
    # Combat actions
    SWORD_STRIKE = "sword_strike"
    MAGIC_BLAST = "magic_blast"
    SHIELD_BLOCK = "shield_block"
    CRITICAL_HIT = "critical_hit"
    
    # Egyptian themed sounds
    SISTRUM_SHAKE = "sistrum_shake"        # Ancient Egyptian rattle
    TEMPLE_BELL = "temple_bell"            # Sacred bell sound
    SAND_WHISPER = "sand_whisper"          # Flowing sand sound
    PHARAOH_HORN = "pharaoh_horn"          # Royal horn blast
    
    # Damage and healing
    FLESH_IMPACT = "flesh_impact"
    BONE_CRACK = "bone_crack"
    DIVINE_HEAL = "divine_heal"
    POISON_BUBBLE = "poison_bubble"
    
    # Turn transitions
    HOURGLASS_FLIP = "hourglass_flip"
    SAND_TIMER = "sand_timer"
    GONG_ECHO = "gong_echo"
    
    # Victory/defeat
    TRIUMPH_FANFARE = "triumph_fanfare"
    DEFEAT_WAIL = "defeat_wail"
    
    # Ambient layers
    DESERT_WIND = "desert_wind"
    TEMPLE_CHANT = "temple_chant"
    TOMB_ECHO = "tomb_echo"


@dataclass
class SoundEffect:
    """Individual sound effect with metadata."""
    sound_type: CombatSoundType
    volume: float = 1.0
    pitch: float = 1.0
    spatial_position: Optional[Tuple[float, float]] = None
    layer_priority: int = 0  # Higher priority sounds can interrupt lower ones
    loop: bool = False
    fade_in: float = 0.0
    fade_out: float = 0.0


class CombatSoundSystem:
    """
    Advanced combat sound system with Egyptian theming.
    
    Manages layered audio, spatial positioning, and dynamic
    mixing for an immersive combat experience.
    """
    
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Core audio system
        self.audio_manager = get_audio_manager()
        
        # Sound configuration
        self.sound_configs = self._initialize_sound_configs()
        
        # Active ambient layers
        self.ambient_layers: Dict[str, pygame.mixer.Channel] = {}
        
        # Sound queue for layering
        self.sound_queue: List[SoundEffect] = []
        
        # Egyptian music instruments
        self.egyptian_instruments = {
            'sistrum': 0.7,     # Volume multiplier for sistrum sounds
            'drums': 0.8,       # Egyptian drums
            'flute': 0.6,       # Reed flute
            'lyre': 0.5,        # Ancient lyre
            'bells': 0.4        # Temple bells
        }
        
        # Spatial audio settings
        self.listener_position = (screen_width // 2, screen_height // 2)
        self.max_distance = 400  # Maximum distance for spatial audio
        
        logging.info("Combat Sound System initialized")
    
    def _initialize_sound_configs(self) -> Dict[CombatSoundType, Dict[str, Any]]:
        """Initialize sound effect configurations."""
        return {
            # Card sounds with Egyptian instruments
            CombatSoundType.CARD_ATTACK: {
                'base_frequency': 220,
                'duration': 0.3,
                'volume': 0.7,
                'instrument': 'drums',
                'reverb': 0.2
            },
            CombatSoundType.CARD_SKILL: {
                'base_frequency': 440,
                'duration': 0.4,
                'volume': 0.6,
                'instrument': 'sistrum',
                'reverb': 0.4
            },
            CombatSoundType.CARD_POWER: {
                'base_frequency': 330,
                'duration': 0.6,
                'volume': 0.8,
                'instrument': 'bells',
                'reverb': 0.6
            },
            CombatSoundType.CARD_STATUS: {
                'base_frequency': 550,
                'duration': 0.5,
                'volume': 0.5,
                'instrument': 'flute',
                'reverb': 0.3
            },
            
            # Combat action sounds
            CombatSoundType.SWORD_STRIKE: {
                'base_frequency': 180,
                'duration': 0.2,
                'volume': 0.8,
                'sharpness': 0.9  # Sharp attack sound
            },
            CombatSoundType.MAGIC_BLAST: {
                'base_frequency': 660,
                'duration': 0.5,
                'volume': 0.7,
                'sparkle': 0.8    # Magical sparkle effect
            },
            CombatSoundType.SHIELD_BLOCK: {
                'base_frequency': 150,
                'duration': 0.3,
                'volume': 0.6,
                'metallic': 0.7   # Metallic ring
            },
            CombatSoundType.CRITICAL_HIT: {
                'base_frequency': 880,
                'duration': 0.4,
                'volume': 0.9,
                'impact': 1.0     # Maximum impact
            },
            
            # Egyptian themed sounds
            CombatSoundType.SISTRUM_SHAKE: {
                'base_frequency': 1200,
                'duration': 0.8,
                'volume': 0.5,
                'rattle': 0.9     # Distinctive rattle sound
            },
            CombatSoundType.TEMPLE_BELL: {
                'base_frequency': 800,
                'duration': 2.0,
                'volume': 0.6,
                'resonance': 0.8  # Long resonance
            },
            CombatSoundType.SAND_WHISPER: {
                'base_frequency': 100,
                'duration': 1.5,
                'volume': 0.3,
                'whisper': 0.9    # Soft whisper effect
            },
            CombatSoundType.PHARAOH_HORN: {
                'base_frequency': 110,
                'duration': 1.2,
                'volume': 0.8,
                'brass': 0.9      # Brass horn sound
            },
            
            # Damage and healing
            CombatSoundType.FLESH_IMPACT: {
                'base_frequency': 120,
                'duration': 0.2,
                'volume': 0.6,
                'thud': 0.8       # Dull impact
            },
            CombatSoundType.DIVINE_HEAL: {
                'base_frequency': 1000,
                'duration': 1.0,
                'volume': 0.5,
                'ethereal': 0.9   # Ethereal healing sound
            },
            CombatSoundType.POISON_BUBBLE: {
                'base_frequency': 300,
                'duration': 0.6,
                'volume': 0.4,
                'bubble': 0.7     # Bubbling poison
            },
            
            # Turn transitions
            CombatSoundType.HOURGLASS_FLIP: {
                'base_frequency': 200,
                'duration': 0.8,
                'volume': 0.6,
                'granular': 0.8   # Sand flowing sound
            },
            CombatSoundType.GONG_ECHO: {
                'base_frequency': 80,
                'duration': 3.0,
                'volume': 0.7,
                'metallic_echo': 0.9  # Deep gong with echo
            }
        }
    
    def play_card_sound(self, card_type: str, position: Optional[Tuple[float, float]] = None,
                       intensity: float = 1.0) -> None:
        """Play sound effect for card being played."""
        
        # Map card types to sound types
        sound_mapping = {
            'attack': CombatSoundType.CARD_ATTACK,
            'skill': CombatSoundType.CARD_SKILL,
            'power': CombatSoundType.CARD_POWER,
            'status': CombatSoundType.CARD_STATUS
        }
        
        sound_type = sound_mapping.get(card_type.lower(), CombatSoundType.CARD_ATTACK)
        
        # Create layered sound effect
        self._play_layered_effect(sound_type, position, intensity)
        
        # Add Egyptian instrument accent
        self._play_egyptian_accent(card_type, intensity)
    
    def play_combat_action_sound(self, action_type: str, position: Optional[Tuple[float, float]] = None,
                               is_critical: bool = False, intensity: float = 1.0) -> None:
        """Play sound for combat action."""
        
        if is_critical:
            self._play_layered_effect(CombatSoundType.CRITICAL_HIT, position, intensity * 1.5)
            # Add dramatic pause before regular sound
            pygame.time.wait(100)
        
        # Map action types to sounds
        action_mapping = {
            'sword_attack': CombatSoundType.SWORD_STRIKE,
            'magic_attack': CombatSoundType.MAGIC_BLAST,
            'block': CombatSoundType.SHIELD_BLOCK,
            'damage': CombatSoundType.FLESH_IMPACT,
            'healing': CombatSoundType.DIVINE_HEAL,
            'poison': CombatSoundType.POISON_BUBBLE
        }
        
        sound_type = action_mapping.get(action_type.lower())
        if sound_type:
            self._play_layered_effect(sound_type, position, intensity)
    
    def play_sand_effect(self, effect_type: str, intensity: float = 1.0) -> None:
        """Play sand-related sound effects."""
        
        if effect_type == "flow":
            self._play_layered_effect(CombatSoundType.SAND_WHISPER, None, intensity)
        elif effect_type == "timer_flip":
            self._play_layered_effect(CombatSoundType.HOURGLASS_FLIP, None, intensity)
        elif effect_type == "gain":
            # Use sistrum for sand gain
            self._play_layered_effect(CombatSoundType.SISTRUM_SHAKE, None, intensity * 0.7)
    
    def play_turn_transition(self, is_player_turn: bool) -> None:
        """Play turn transition sound with Egyptian theme."""
        
        if is_player_turn:
            # Player turn - hopeful temple bell
            self._play_layered_effect(CombatSoundType.TEMPLE_BELL, None, 1.0)
        else:
            # Enemy turn - ominous gong
            self._play_layered_effect(CombatSoundType.GONG_ECHO, None, 0.8)
    
    def play_victory_sound(self) -> None:
        """Play victory fanfare with Egyptian instruments."""
        self._play_layered_effect(CombatSoundType.PHARAOH_HORN, None, 1.0)
        
        # Layer multiple Egyptian instruments for fanfare
        pygame.time.wait(200)
        self._play_layered_effect(CombatSoundType.SISTRUM_SHAKE, None, 0.8)
        pygame.time.wait(100) 
        self._play_layered_effect(CombatSoundType.TEMPLE_BELL, None, 0.6)
    
    def play_defeat_sound(self) -> None:
        """Play defeat sound with mournful tone."""
        # Low, mournful horn sound
        self._create_and_play_sound(80, 2.0, 0.7, effect_type="mournful")
    
    def start_combat_ambience(self, location_type: str = "desert") -> None:
        """Start ambient background sounds for combat."""
        
        ambient_mapping = {
            'desert': CombatSoundType.DESERT_WIND,
            'temple': CombatSoundType.TEMPLE_CHANT,
            'tomb': CombatSoundType.TOMB_ECHO
        }
        
        sound_type = ambient_mapping.get(location_type, CombatSoundType.DESERT_WIND)
        
        # Start looping ambient sound at low volume
        self._start_ambient_layer(sound_type, 0.3)
    
    def stop_combat_ambience(self) -> None:
        """Stop all ambient sounds."""
        for channel in self.ambient_layers.values():
            if channel:
                channel.fadeout(1000)  # 1 second fade out
        self.ambient_layers.clear()
    
    def _play_layered_effect(self, sound_type: CombatSoundType, 
                           position: Optional[Tuple[float, float]], 
                           intensity: float) -> None:
        """Play a sound effect with spatial and intensity modifications."""
        
        config = self.sound_configs.get(sound_type, {})
        
        # Calculate spatial volume if position given
        volume = config.get('volume', 0.5) * intensity
        
        if position:
            spatial_volume = self._calculate_spatial_volume(position)
            volume *= spatial_volume
        
        # Create and play the sound
        frequency = config.get('base_frequency', 440)
        duration = config.get('duration', 0.5)
        
        # Add random variation for naturalness
        frequency += random.uniform(-20, 20)
        volume += random.uniform(-0.1, 0.1)
        volume = max(0.0, min(1.0, volume))
        
        self._create_and_play_sound(frequency, duration, volume, sound_type)
    
    def _play_egyptian_accent(self, card_type: str, intensity: float) -> None:
        """Add Egyptian instrument accent to card sounds."""
        
        # Map card types to Egyptian instruments
        instrument_mapping = {
            'attack': ('drums', 180, 0.2),      # War drums
            'skill': ('sistrum', 1200, 0.3),    # Mystical sistrum  
            'power': ('bells', 800, 0.4),       # Sacred bells
            'status': ('flute', 550, 0.3)       # Reed flute
        }
        
        if card_type.lower() in instrument_mapping:
            instrument, freq, dur = instrument_mapping[card_type.lower()]
            volume = self.egyptian_instruments.get(instrument, 0.5) * intensity * 0.6
            
            # Small delay to layer over card sound
            pygame.time.wait(50)
            self._create_and_play_sound(freq, dur, volume, effect_type=instrument)
    
    def _calculate_spatial_volume(self, position: Tuple[float, float]) -> float:
        """Calculate volume based on spatial position."""
        
        # Calculate distance from listener
        dx = position[0] - self.listener_position[0]
        dy = position[1] - self.listener_position[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Apply distance attenuation
        if distance >= self.max_distance:
            return 0.0
        
        # Linear falloff (could use other curves)
        return 1.0 - (distance / self.max_distance)
    
    def _create_and_play_sound(self, frequency: float, duration: float, 
                             volume: float, sound_type: CombatSoundType = None,
                             effect_type: str = None) -> None:
        """Create and play a procedural sound with specified parameters."""
        
        try:
            # Create a more sophisticated procedural sound
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            if frames <= 0:
                return
            
            # Create sound array
            arr = []
            
            for i in range(frames):
                time_point = i / sample_rate
                
                # Base wave with harmonics for richer sound
                wave = math.sin(2 * math.pi * frequency * time_point)
                
                # Add harmonics based on sound type/effect
                if effect_type == "drums":
                    # Add percussive harmonics
                    wave += 0.3 * math.sin(2 * math.pi * frequency * 2 * time_point)
                    wave += 0.1 * math.sin(2 * math.pi * frequency * 4 * time_point)
                    
                elif effect_type == "sistrum":
                    # Add rattling harmonics
                    wave += 0.4 * math.sin(2 * math.pi * frequency * 1.5 * time_point)
                    wave += 0.2 * random.uniform(-0.3, 0.3)  # Random rattle
                    
                elif effect_type == "bells":
                    # Add bell-like resonance
                    wave += 0.2 * math.sin(2 * math.pi * frequency * 3 * time_point)
                    wave += 0.1 * math.sin(2 * math.pi * frequency * 5 * time_point)
                    
                elif effect_type == "mournful":
                    # Low, mournful tone with vibrato
                    vibrato = 1.0 + 0.1 * math.sin(2 * math.pi * 5 * time_point)
                    wave = math.sin(2 * math.pi * frequency * vibrato * time_point)
                
                # Apply envelope (fade in/out)
                fade_frames = min(frames // 10, 1000)
                if i < fade_frames:
                    envelope = i / fade_frames
                elif i > frames - fade_frames:
                    envelope = (frames - i) / fade_frames
                else:
                    envelope = 1.0
                
                # Apply volume and envelope
                wave *= volume * envelope
                
                # Convert to int16 and append stereo
                sample = int(wave * 32767)
                sample = max(-32767, min(32767, sample))  # Clamp
                arr.extend([sample, sample])
            
            # Create pygame Sound from array
            if arr:
                sound_array = bytes([(sample + 32768) % 65536 for sample in arr])
                sound = pygame.mixer.Sound(buffer=sound_array)
                
                # Play the sound
                pygame.mixer.Sound.play(sound)
                
        except Exception as e:
            logging.warning(f"Failed to create procedural sound: {e}")
            # Fallback to simpler sound
            try:
                fallback_sound = self.audio_manager.sounds.get(SoundType.CARD_PLAY)
                if fallback_sound:
                    fallback_sound.set_volume(volume)
                    pygame.mixer.Sound.play(fallback_sound)
            except:
                pass  # Silent failure if all else fails
    
    def _start_ambient_layer(self, sound_type: CombatSoundType, volume: float) -> None:
        """Start a looping ambient sound layer."""
        
        config = self.sound_configs.get(sound_type, {})
        frequency = config.get('base_frequency', 200)
        
        # Create longer ambient sound (will loop)
        try:
            self._create_and_play_sound(frequency, 5.0, volume, sound_type, effect_type="ambient")
        except Exception as e:
            logging.warning(f"Failed to start ambient layer: {e}")
    
    def set_listener_position(self, x: float, y: float) -> None:
        """Set the listener position for spatial audio."""
        self.listener_position = (x, y)
    
    def update_volume_settings(self, master_volume: float, sfx_volume: float) -> None:
        """Update volume settings from audio manager."""
        # Update internal volume multipliers
        for instrument in self.egyptian_instruments:
            self.egyptian_instruments[instrument] *= sfx_volume
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status for debugging."""
        return {
            'active_ambient_layers': len(self.ambient_layers),
            'sound_queue_length': len(self.sound_queue),
            'listener_position': self.listener_position,
            'egyptian_instruments': self.egyptian_instruments
        }


# Global combat sound system
_combat_sound_system: Optional[CombatSoundSystem] = None


def get_combat_sound_system() -> CombatSoundSystem:
    """Get the global combat sound system instance."""
    global _combat_sound_system
    if _combat_sound_system is None:
        _combat_sound_system = CombatSoundSystem()
    return _combat_sound_system


def initialize_combat_sound_system(screen_width: int = 1200, screen_height: int = 800) -> CombatSoundSystem:
    """Initialize the global combat sound system."""
    global _combat_sound_system
    _combat_sound_system = CombatSoundSystem(screen_width, screen_height)
    return _combat_sound_system