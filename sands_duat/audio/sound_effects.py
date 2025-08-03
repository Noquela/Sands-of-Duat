"""
Sound Effects Library for Sands of Duat

Provides themed sound effect collections and management for
enhanced audio experience in the Egyptian-themed game.
"""

import pygame
import random
import math
from typing import Dict, List, Optional, Tuple
from enum import Enum
from .audio_manager import SoundType, get_audio_manager

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class SoundEffectLibrary:
    """
    Library of thematic sound effects for the game.
    
    Provides easy access to sound effect collections organized
    by game context and theme.
    """
    
    def __init__(self):
        self.audio_manager = get_audio_manager()
        self._setup_sound_collections()
    
    def _setup_sound_collections(self) -> None:
        """Set up organized sound effect collections."""
        # UI Sound Collections
        self.ui_sounds = {
            "button_hover": SoundType.UI_BUTTON_HOVER,
            "button_click": SoundType.UI_BUTTON_CLICK,
            "screen_transition": SoundType.UI_SCREEN_TRANSITION
        }
        
        # Card Sound Collections
        self.card_sounds = {
            "hover": SoundType.CARD_HOVER,
            "play": SoundType.CARD_PLAY,
            "draw": SoundType.CARD_DRAW,
            "shuffle": SoundType.CARD_SHUFFLE
        }
        
        # Combat Sound Collections
        self.combat_sounds = {
            "damage": SoundType.COMBAT_DAMAGE,
            "heal": SoundType.COMBAT_HEAL,
            "block": SoundType.COMBAT_BLOCK,
            "victory": SoundType.COMBAT_VICTORY,
            "defeat": SoundType.COMBAT_DEFEAT
        }
        
        # Sand/Hourglass Sound Collections
        self.sand_sounds = {
            "flow": SoundType.SAND_FLOW,
            "gain": SoundType.SAND_GAIN,
            "spend": SoundType.SAND_SPEND
        }
        
        # Ambient Sound Collections
        self.ambient_sounds = {
            "wind": SoundType.AMBIENT_WIND,
            "temple": SoundType.AMBIENT_TEMPLE,
            "desert": SoundType.AMBIENT_DESERT
        }
    
    def play_ui_sound(self, sound_name: str, volume: float = 1.0) -> bool:
        """Play a UI sound effect."""
        if sound_name in self.ui_sounds:
            return self.audio_manager.play_sound(
                self.ui_sounds[sound_name], 
                volume, 
                "ui_sfx"
            )
        return False
    
    def play_card_sound(self, sound_name: str, volume: float = 1.0) -> bool:
        """Play a card-related sound effect."""
        if sound_name in self.card_sounds:
            return self.audio_manager.play_sound(
                self.card_sounds[sound_name], 
                volume, 
                "card_sfx"
            )
        return False
    
    def play_combat_sound(self, sound_name: str, volume: float = 1.0) -> bool:
        """Play a combat sound effect."""
        if sound_name in self.combat_sounds:
            return self.audio_manager.play_sound(
                self.combat_sounds[sound_name], 
                volume, 
                "combat_sfx"
            )
        return False
    
    def play_sand_sound(self, sound_name: str, volume: float = 1.0) -> bool:
        """Play a sand/hourglass sound effect."""
        if sound_name in self.sand_sounds:
            return self.audio_manager.play_sound(
                self.sand_sounds[sound_name], 
                volume, 
                "sand_sfx"
            )
        return False
    
    def play_random_combat_hit(self, damage_amount: int) -> bool:
        """Play a random combat hit sound based on damage amount."""
        # Vary volume and pitch based on damage
        base_volume = 0.5
        volume_multiplier = min(2.0, 1.0 + (damage_amount / 20.0))
        final_volume = min(1.0, base_volume * volume_multiplier)
        
        return self.play_combat_sound("damage", final_volume)
    
    def play_card_play_sequence(self, card_type: str = "attack") -> None:
        """Play a sequence of sounds for card play."""
        # Quick card play sound
        self.play_card_sound("play", 0.8)
        
        # Add themed sound based on card type
        if card_type.lower() == "attack":
            pygame.time.set_timer(pygame.USEREVENT + 1, 200)  # Delay for impact sound
        elif card_type.lower() == "skill":
            self.play_sand_sound("flow", 0.6)
        elif card_type.lower() == "power":
            self.play_combat_sound("heal", 0.5)
    
    def play_hourglass_sequence(self, sand_gained: int) -> None:
        """Play themed sound sequence for sand gain."""
        # Base sand flow sound
        self.play_sand_sound("flow", 0.4)
        
        # Additional effects based on amount
        if sand_gained > 1:
            # Multiple sand grains - slightly longer effect
            pygame.time.set_timer(pygame.USEREVENT + 2, 100)
        
        if sand_gained >= 3:
            # Significant sand gain - add completion sound
            pygame.time.set_timer(pygame.USEREVENT + 3, 300)


class ThemedAudioPlayer:
    """
    Provides themed audio experiences for different game contexts.
    """
    
    def __init__(self):
        self.audio_manager = get_audio_manager()
        self.sound_library = SoundEffectLibrary()
        self.current_theme = "desert"
        self.theme_configs = self._setup_theme_configs()
    
    def _setup_theme_configs(self) -> Dict[str, Dict]:
        """Set up audio theme configurations."""
        return {
            "desert": {
                "ambient": "desert",
                "music": "menu",
                "ui_pitch": 1.0,
                "combat_reverb": 0.3
            },
            "temple": {
                "ambient": "temple", 
                "music": "temple_ambient",
                "ui_pitch": 0.8,
                "combat_reverb": 0.7
            },
            "combat": {
                "ambient": None,
                "music": "combat",
                "ui_pitch": 1.2,
                "combat_reverb": 0.1
            }
        }
    
    def set_audio_theme(self, theme_name: str) -> bool:
        """Set the current audio theme."""
        if theme_name not in self.theme_configs:
            return False
        
        self.current_theme = theme_name
        theme_config = self.theme_configs[theme_name]
        
        # Switch music if specified
        if theme_config.get("music"):
            self.audio_manager.play_music(theme_config["music"])
        
        # Switch ambient if specified
        if theme_config.get("ambient"):
            self.audio_manager.play_ambient(theme_config["ambient"])
        
        return True
    
    def play_themed_ui_sound(self, sound_name: str) -> bool:
        """Play UI sound with current theme modifications."""
        theme_config = self.theme_configs.get(self.current_theme, {})
        volume_modifier = theme_config.get("ui_pitch", 1.0)
        
        return self.sound_library.play_ui_sound(sound_name, volume_modifier)
    
    def play_combat_impact(self, damage: int, target_type: str = "enemy") -> bool:
        """Play themed combat impact sound."""
        base_volume = 0.7
        
        # Modify based on target type
        if target_type == "player":
            base_volume *= 1.2  # Player hits are more impactful
        
        # Modify based on damage amount
        damage_multiplier = min(1.5, 0.5 + (damage / 15.0))
        final_volume = min(1.0, base_volume * damage_multiplier)
        
        return self.sound_library.play_combat_sound("damage", final_volume)
    
    def play_sand_event(self, event_type: str, intensity: int = 1) -> bool:
        """Play themed sand/hourglass events."""
        volume = min(1.0, 0.3 + (intensity * 0.2))
        
        if event_type == "regeneration":
            return self.sound_library.play_sand_sound("gain", volume)
        elif event_type == "spending":
            return self.sound_library.play_sand_sound("spend", volume)
        elif event_type == "flowing":
            return self.sound_library.play_sand_sound("flow", volume)
        
        return False


# Convenience functions for easy integration
def play_button_sound(button_type: str = "click") -> None:
    """Quick function to play button sounds."""
    try:
        library = SoundEffectLibrary()
        if button_type == "hover":
            library.play_ui_sound("button_hover", 0.3)
        else:
            library.play_ui_sound("button_click", 0.5)
    except Exception as e:
        # Silently handle audio initialization errors during testing
        pass


def play_card_interaction_sound(interaction_type: str) -> None:
    """Quick function to play card interaction sounds."""
    try:
        library = SoundEffectLibrary()
        if interaction_type == "hover":
            library.play_card_sound("hover", 0.2)
        elif interaction_type == "play":
            library.play_card_sound("play", 0.7)
        elif interaction_type == "draw":
            library.play_card_sound("draw", 0.4)
    except Exception:
        pass


def play_combat_feedback_sound(feedback_type: str, intensity: int = 1) -> None:
    """Quick function to play combat feedback sounds."""
    try:
        library = SoundEffectLibrary()
        volume = min(1.0, 0.5 + (intensity * 0.1))
        
        if feedback_type == "damage":
            library.play_combat_sound("damage", volume)
        elif feedback_type == "heal":
            library.play_combat_sound("heal", volume)
        elif feedback_type == "block":
            library.play_combat_sound("block", volume)
    except Exception:
        pass


def play_sand_feedback_sound(sand_event: str, amount: int = 1) -> None:
    """Quick function to play sand-related feedback sounds."""
    try:
        library = SoundEffectLibrary()
        volume = min(1.0, 0.3 + (amount * 0.15))
        
        if sand_event == "gain":
            library.play_sand_sound("gain", volume)
        elif sand_event == "spend":
            library.play_sand_sound("spend", volume)
        elif sand_event == "flow":
            library.play_sand_sound("flow", volume)
    except Exception:
        pass