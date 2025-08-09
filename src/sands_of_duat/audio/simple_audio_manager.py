"""
Simple Audio Manager - SPRINT 6: Reliable Egyptian Audio System
Provides basic sound effects without complex procedural generation.
"""

import pygame
import random
import time
from typing import Dict, Optional
from enum import Enum, auto

class AudioTrack(Enum):
    """Audio track categories."""
    MENU = auto()
    DECK_BUILDER = auto()
    COMBAT = auto()
    VICTORY = auto()
    DEFEAT = auto()
    AMBIENT = auto()

class SoundEffect(Enum):
    """Sound effect types."""
    BUTTON_HOVER = auto()
    BUTTON_CLICK = auto()
    CARD_PLAY = auto()
    CARD_HOVER = auto()
    DAMAGE_DEALT = auto()
    HEALING = auto()
    VICTORY_FANFARE = auto()
    DEFEAT_SOUND = auto()
    TRANSITION = auto()
    MANA_GAIN = auto()

class SimpleAudioManager:
    """
    Simple audio manager focused on reliability over complexity.
    Provides basic sound effects for Egyptian underworld atmosphere.
    """
    
    def __init__(self):
        """Initialize the simple audio system."""
        try:
            # Initialize pygame mixer with basic settings
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            
            # Audio state
            self.master_volume = 0.7
            self.music_volume = 0.6
            self.sfx_volume = 0.8
            self.ambient_volume = 0.4
            
            # Current tracks
            self.current_track: Optional[AudioTrack] = None
            self.is_playing = False
            
            # Simple sound effect placeholders
            self.sound_enabled = True
            
            # Dynamic audio
            self.ambient_timer = 0.0
            self.next_ambient_time = random.uniform(10.0, 25.0)
            
            print("Simple Audio Manager initialized successfully")
            
        except Exception as e:
            print(f"Audio initialization failed: {e}")
            self.sound_enabled = False
    
    def play_music(self, track: AudioTrack, fade_in: float = 1.0):
        """Play background music (simulated)."""
        if not self.sound_enabled:
            return
            
        if track == self.current_track:
            return
        
        self.current_track = track
        self.is_playing = True
        
        # Simulate different music tracks
        track_names = {
            AudioTrack.MENU: "Ancient Egyptian Menu Theme",
            AudioTrack.DECK_BUILDER: "Sacred Deck Building Atmosphere",
            AudioTrack.COMBAT: "Epic Egyptian God Battle Music",
            AudioTrack.VICTORY: "Divine Victory Fanfare",
            AudioTrack.DEFEAT: "Underworld Defeat Theme"
        }
        
        print(f"Playing: {track_names.get(track, track.name)}")
    
    def stop_music(self, fade_out: float = 1.0):
        """Stop background music."""
        if self.is_playing:
            self.is_playing = False
            self.current_track = None
    
    def play_sound(self, effect: SoundEffect, volume: Optional[float] = None):
        """Play a sound effect (simulated with console feedback)."""
        if not self.sound_enabled:
            return
        
        # Sound effect descriptions for feedback
        effect_descriptions = {
            SoundEffect.BUTTON_HOVER: "Soft sand whisper",
            SoundEffect.BUTTON_CLICK: "Temple bell chime",
            SoundEffect.CARD_PLAY: "Papyrus rustle + mystical energy",
            SoundEffect.CARD_HOVER: "Subtle mystical hum",
            SoundEffect.DAMAGE_DEALT: "Ancient magic impact",
            SoundEffect.HEALING: "Divine restoration chimes",
            SoundEffect.VICTORY_FANFARE: "Triumphant Egyptian fanfare",
            SoundEffect.DEFEAT_SOUND: "Somber underworld echo",
            SoundEffect.TRANSITION: "Mystical transition whoosh",
            SoundEffect.MANA_GAIN: "Sacred energy pulse"
        }
        
        # Calculate final volume
        final_volume = volume or self.sfx_volume
        final_volume *= self.master_volume
        
        # Provide audio feedback in debug mode
        if hasattr(self, 'debug_mode') and self.debug_mode:
            desc = effect_descriptions.get(effect, effect.name)
            print(f"Audio: {desc} (vol: {final_volume:.1f})")
    
    def play_ambient_sound(self):
        """Play a random ambient sound (simulated)."""
        if not self.sound_enabled or random.random() < 0.7:
            return
        
        ambient_sounds = [
            "Desert wind through ancient ruins",
            "Distant temple bells echoing",
            "Mystical energy pulses in the underworld",
            "Whispers of ancient Egyptian spirits"
        ]
        
        sound = random.choice(ambient_sounds)
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"Ambient: {sound}")
    
    def update(self, dt: float, current_screen: str = "menu"):
        """Update audio system."""
        if not self.sound_enabled:
            return
            
        self.ambient_timer += dt
        
        # Play ambient sounds periodically
        if self.ambient_timer >= self.next_ambient_time:
            self.play_ambient_sound()
            self.ambient_timer = 0.0
            self.next_ambient_time = random.uniform(15.0, 35.0)
        
        # Handle music transitions based on screen
        target_track = None
        if current_screen == "main_menu":
            target_track = AudioTrack.MENU
        elif current_screen == "deck_builder":
            target_track = AudioTrack.DECK_BUILDER
        elif current_screen == "combat":
            target_track = AudioTrack.COMBAT
        
        if target_track and target_track != self.current_track:
            self.play_music(target_track)
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_ambient_volume(self, volume: float):
        """Set ambient volume (0.0 to 1.0)."""
        self.ambient_volume = max(0.0, min(1.0, volume))
    
    def get_volume_settings(self) -> Dict[str, float]:
        """Get current volume settings."""
        return {
            "master": self.master_volume,
            "music": self.music_volume,
            "sfx": self.sfx_volume,
            "ambient": self.ambient_volume
        }
    
    def handle_combat_event(self, event_type: str, intensity: float = 1.0):
        """Handle combat events for dynamic audio feedback."""
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"Combat Audio Event: {event_type} (intensity: {intensity})")
    
    def shutdown(self):
        """Clean shutdown of audio system."""
        if self.sound_enabled:
            try:
                pygame.mixer.stop()
                pygame.mixer.quit()
                print("Audio system shutdown complete")
            except:
                pass

# Global audio manager instance
audio_manager = SimpleAudioManager()