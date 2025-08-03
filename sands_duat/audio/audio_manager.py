"""
Audio Manager for Sands of Duat

Centralized audio system managing music, sound effects, and audio settings.
Provides themed audio experiences for different game states and actions.
"""

import pygame
import os
import logging
import json
import math
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Any
from enum import Enum
import threading
import time


class SoundType(Enum):
    """Types of sound effects."""
    UI_BUTTON_HOVER = "ui_button_hover"
    UI_BUTTON_CLICK = "ui_button_click"
    UI_SCREEN_TRANSITION = "ui_screen_transition"
    
    CARD_HOVER = "card_hover"
    CARD_PLAY = "card_play"
    CARD_DRAW = "card_draw"
    CARD_SHUFFLE = "card_shuffle"
    
    COMBAT_DAMAGE = "combat_damage"
    COMBAT_HEAL = "combat_heal"
    COMBAT_BLOCK = "combat_block"
    COMBAT_VICTORY = "combat_victory"
    COMBAT_DEFEAT = "combat_defeat"
    
    SAND_FLOW = "sand_flow"
    SAND_GAIN = "sand_gain"
    SAND_SPEND = "sand_spend"
    
    AMBIENT_WIND = "ambient_wind"
    AMBIENT_TEMPLE = "ambient_temple"
    AMBIENT_DESERT = "ambient_desert"


class AudioChannel:
    """Represents an audio channel for organized sound management."""
    
    def __init__(self, name: str, max_volume: float = 1.0):
        self.name = name
        self.max_volume = max_volume
        self.current_volume = max_volume
        self.muted = False
        self.pygame_channel = None
        self.reserved_channel = False
    
    def set_volume(self, volume: float) -> None:
        """Set the channel volume (0.0 to 1.0)."""
        self.current_volume = max(0.0, min(1.0, volume))
        if self.pygame_channel and not self.muted:
            self.pygame_channel.set_volume(self.current_volume * self.max_volume)
    
    def mute(self) -> None:
        """Mute this channel."""
        self.muted = True
        if self.pygame_channel:
            self.pygame_channel.set_volume(0.0)
    
    def unmute(self) -> None:
        """Unmute this channel."""
        self.muted = False
        if self.pygame_channel:
            self.pygame_channel.set_volume(self.current_volume * self.max_volume)


class AudioManager:
    """
    Comprehensive audio management system.
    
    Handles music, sound effects, audio channels, and provides
    themed audio experiences for the Egyptian setting.
    """
    
    def __init__(self, audio_config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        
        # Audio settings
        self.master_volume = 1.0
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.ambient_volume = 0.6
        self.ui_volume = 0.5
        
        # Audio channels
        self.channels: Dict[str, AudioChannel] = {}
        self._setup_audio_channels()
        
        # Sound libraries
        self.sounds: Dict[SoundType, pygame.mixer.Sound] = {}
        self.music_tracks: Dict[str, str] = {}
        self.ambient_tracks: Dict[str, str] = {}
        
        # Current state
        self.current_music = None
        self.current_ambient = None
        self.music_fade_thread = None
        
        # Load audio configuration
        self.audio_config = self._load_audio_config(audio_config_path)
        
        # Create placeholder audio directory
        self.audio_dir = Path(__file__).parent.parent / "assets" / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize sound libraries
        self._initialize_sound_library()
        
        self.logger.info("Audio Manager initialized")
    
    def _setup_audio_channels(self) -> None:
        """Set up organized audio channels."""
        # Reserve pygame channels
        pygame.mixer.set_num_channels(16)
        
        # Create logical channels
        channel_configs = [
            ("music", 1.0),
            ("ambient", 0.8),
            ("ui_sfx", 0.7),
            ("card_sfx", 0.8),
            ("combat_sfx", 0.9),
            ("sand_sfx", 0.6),
            ("voice", 1.0),
            ("master_sfx", 0.8)
        ]
        
        for i, (name, max_vol) in enumerate(channel_configs):
            channel = AudioChannel(name, max_vol)
            if i < pygame.mixer.get_num_channels():
                channel.pygame_channel = pygame.mixer.Channel(i)
                channel.reserved_channel = True
            self.channels[name] = channel
        
        self.logger.debug(f"Set up {len(self.channels)} audio channels")
    
    def _load_audio_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load audio configuration from file."""
        default_config = {
            "sound_mappings": {
                "ui_button_hover": "ui/button_hover.wav",
                "ui_button_click": "ui/button_click.wav",
                "ui_screen_transition": "ui/screen_transition.wav",
                "card_hover": "cards/card_hover.wav",
                "card_play": "cards/card_play.wav",
                "card_draw": "cards/card_draw.wav",
                "card_shuffle": "cards/card_shuffle.wav",
                "combat_damage": "combat/hit.wav",
                "combat_heal": "combat/heal.wav",
                "combat_block": "combat/block.wav",
                "combat_victory": "combat/victory.wav",
                "combat_defeat": "combat/defeat.wav",
                "sand_flow": "sand/flow.wav",
                "sand_gain": "sand/gain.wav",
                "sand_spend": "sand/spend.wav",
                "ambient_wind": "ambient/wind.wav",
                "ambient_temple": "ambient/temple.wav",
                "ambient_desert": "ambient/desert.wav"
            },
            "music_tracks": {
                "menu": "music/desert_winds.ogg",
                "combat": "music/battle_drums.ogg",
                "victory": "music/triumph.ogg"
            },
            "ambient_tracks": {
                "desert": "ambient/desert_wind.ogg",
                "temple": "ambient/temple_atmosphere.ogg"
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
                self.logger.info(f"Loaded audio configuration from {config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load audio config: {e}, using defaults")
        
        return default_config
    
    def _initialize_sound_library(self) -> None:
        """Initialize the sound effect library with placeholder sounds."""
        # Create procedural sounds for missing audio files
        sound_configs = {
            SoundType.UI_BUTTON_HOVER: (220, 0.1, 0.3),  # frequency, duration, volume
            SoundType.UI_BUTTON_CLICK: (440, 0.15, 0.4),
            SoundType.CARD_HOVER: (330, 0.08, 0.2),
            SoundType.CARD_PLAY: (550, 0.2, 0.5),
            SoundType.CARD_DRAW: (660, 0.12, 0.3),
            SoundType.COMBAT_DAMAGE: (110, 0.3, 0.6),
            SoundType.COMBAT_HEAL: (880, 0.25, 0.4),
            SoundType.SAND_FLOW: (150, 0.5, 0.3),
            SoundType.SAND_GAIN: (200, 0.2, 0.4),
        }
        
        for sound_type, (freq, duration, volume) in sound_configs.items():
            try:
                # Try to load from file first
                sound_filename = self.audio_config["sound_mappings"].get(sound_type.value, "")
                if sound_filename:
                    sound_path = self.audio_dir / sound_filename
                    if sound_path.exists():
                        sound = pygame.mixer.Sound(str(sound_path))
                        self.logger.debug(f"Loaded sound file for {sound_type.value}: {sound_path}")
                    else:
                        # Create procedural sound as fallback
                        sound = self._create_procedural_sound(freq, duration, volume)
                        self.logger.debug(f"Created procedural sound for {sound_type.value}")
                else:
                    # No mapping found, create procedural sound
                    sound = self._create_procedural_sound(freq, duration, volume)
                    self.logger.debug(f"No mapping found, created procedural sound for {sound_type.value}")
                
                self.sounds[sound_type] = sound
            except Exception as e:
                self.logger.warning(f"Failed to create sound for {sound_type.value}: {e}")
                # Create a silent placeholder to prevent further errors
                try:
                    self.sounds[sound_type] = self._create_procedural_sound(440, 0.01, 0.0)  # Silent placeholder
                except:
                    pass  # If even this fails, just skip
        
        self.logger.info(f"Initialized {len(self.sounds)} sound effects")
    
    def _create_procedural_sound(self, frequency: float, duration: float, volume: float) -> pygame.mixer.Sound:
        """Create a simple procedural sound wave."""
        try:
            import numpy as np
            
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Create a simple sine wave with fade in/out
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                time_point = i / sample_rate
                # Sine wave
                wave = np.sin(2 * np.pi * frequency * time_point)
                
                # Apply fade in/out envelope
                fade_frames = min(frames // 10, 1000)  # 10% fade or 1000 frames max
                if i < fade_frames:
                    envelope = i / fade_frames
                elif i > frames - fade_frames:
                    envelope = (frames - i) / fade_frames
                else:
                    envelope = 1.0
                
                # Apply volume and envelope
                wave *= volume * envelope
                
                # Stereo
                arr[i][0] = wave
                arr[i][1] = wave
            
            # Convert to int16 and create sound
            arr = (arr * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(arr)
            
            return sound
            
        except ImportError:
            # Fallback: create a simple sound using pygame's built-in capabilities
            try:
                # Create a simple beep sound
                sample_rate = 22050
                frames = int(duration * sample_rate)
                arr = []
                
                for i in range(frames):
                    time_point = i / sample_rate
                    wave = math.sin(2 * math.pi * frequency * time_point)
                    
                    # Apply fade in/out envelope
                    fade_frames = min(frames // 10, 1000)
                    if i < fade_frames:
                        envelope = i / fade_frames
                    elif i > frames - fade_frames:
                        envelope = (frames - i) / fade_frames
                    else:
                        envelope = 1.0
                    
                    wave *= volume * envelope
                    # Convert to int16 and append both stereo channels
                    sample = int(wave * 32767)
                    arr.extend([sample, sample])
                
                # Create pygame Sound from raw data
                sound_array = bytes([(sample + 32768) % 65536 for sample in arr])
                sound = pygame.mixer.Sound(buffer=sound_array)
                
                return sound
                
            except Exception as fallback_error:
                # Ultimate fallback - create minimal silent sound
                try:
                    # Create a very short silent sound as absolute fallback
                    silent_frames = 1024  # Very short
                    silent_array = bytes([128] * (silent_frames * 2))  # Neutral middle values
                    return pygame.mixer.Sound(buffer=silent_array)
                except Exception:
                    # If even this fails, return None and handle in caller
                    raise RuntimeError(f"Unable to create any sound: {fallback_error}")
    
    def play_sound(self, sound_type: SoundType, volume_override: Optional[float] = None, 
                   channel_name: str = "master_sfx") -> bool:
        """
        Play a sound effect.
        
        Args:
            sound_type: Type of sound to play
            volume_override: Override the default volume (0.0 to 1.0)
            channel_name: Audio channel to use
            
        Returns:
            True if sound was played successfully
        """
        if sound_type not in self.sounds:
            self.logger.warning(f"Sound not found: {sound_type.value}")
            return False
        
        try:
            sound = self.sounds[sound_type]
            
            # Set volume
            if volume_override is not None:
                sound.set_volume(volume_override * self.master_volume)
            else:
                # Use channel-appropriate volume
                if "ui" in sound_type.value:
                    sound.set_volume(self.ui_volume * self.master_volume)
                elif "card" in sound_type.value:
                    sound.set_volume(self.sfx_volume * self.master_volume * 0.7)
                elif "combat" in sound_type.value:
                    sound.set_volume(self.sfx_volume * self.master_volume)
                elif "sand" in sound_type.value:
                    sound.set_volume(self.sfx_volume * self.master_volume * 0.8)
                else:
                    sound.set_volume(self.sfx_volume * self.master_volume)
            
            # Play on appropriate channel
            channel = self.channels.get(channel_name)
            if channel and channel.pygame_channel:
                channel.pygame_channel.play(sound)
            else:
                # Use any available channel
                pygame.mixer.Sound.play(sound)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to play sound {sound_type.value}: {e}")
            return False
    
    def play_music(self, track_name: str, loop: bool = True, fade_in_ms: int = 1000) -> bool:
        """
        Play background music.
        
        Args:
            track_name: Name of music track
            loop: Whether to loop the music
            fade_in_ms: Fade in duration in milliseconds
            
        Returns:
            True if music started successfully
        """
        track_path = self.audio_dir / "music" / f"{track_name}.ogg"
        
        try:
            if track_path.exists():
                pygame.mixer.music.load(str(track_path))
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops, fade_ms=fade_in_ms)
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                self.current_music = track_name
                self.logger.info(f"Started music track: {track_name}")
                return True
            else:
                self.logger.warning(f"Music track not found: {track_path}")
                # For demo purposes, continue without music
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to play music {track_name}: {e}")
            return False
    
    def stop_music(self, fade_out_ms: int = 1000) -> None:
        """Stop background music with fade out."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_out_ms)
            self.current_music = None
    
    def play_ambient(self, ambient_name: str, loop: bool = True, channel_name: str = "ambient") -> bool:
        """
        Play ambient background sounds.
        
        Args:
            ambient_name: Name of ambient track
            loop: Whether to loop the ambient sound
            channel_name: Channel to play on
            
        Returns:
            True if ambient started successfully
        """
        ambient_path = self.audio_dir / "ambient" / f"{ambient_name}.ogg"
        
        try:
            if ambient_path.exists():
                ambient_sound = pygame.mixer.Sound(str(ambient_path))
                ambient_sound.set_volume(self.ambient_volume * self.master_volume)
                
                channel = self.channels.get(channel_name)
                if channel and channel.pygame_channel:
                    loops = -1 if loop else 0
                    channel.pygame_channel.play(ambient_sound, loops)
                    self.current_ambient = ambient_name
                    self.logger.info(f"Started ambient track: {ambient_name}")
                    return True
            else:
                self.logger.warning(f"Ambient track not found: {ambient_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to play ambient {ambient_name}: {e}")
            return False
    
    def set_master_volume(self, volume: float) -> None:
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        
        # Update all channel volumes
        for channel in self.channels.values():
            channel.set_volume(channel.current_volume)
        
        # Update music volume
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        
        self.logger.debug(f"Set master volume to {self.master_volume}")
    
    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def set_sfx_volume(self, volume: float) -> None:
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_ui_volume(self, volume: float) -> None:
        """Set UI sounds volume (0.0 to 1.0)."""
        self.ui_volume = max(0.0, min(1.0, volume))
    
    def mute_all(self) -> None:
        """Mute all audio."""
        for channel in self.channels.values():
            channel.mute()
        pygame.mixer.music.set_volume(0.0)
    
    def unmute_all(self) -> None:
        """Unmute all audio."""
        for channel in self.channels.values():
            channel.unmute()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
    def get_audio_info(self) -> Dict[str, Any]:
        """Get current audio system information."""
        return {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "ui_volume": self.ui_volume,
            "current_music": self.current_music,
            "current_ambient": self.current_ambient,
            "mixer_frequency": pygame.mixer.get_freq(),
            "mixer_channels": pygame.mixer.get_num_channels(),
            "sounds_loaded": len(self.sounds),
            "channels_configured": len(self.channels)
        }
    
    def cleanup(self) -> None:
        """Clean up audio resources."""
        self.stop_music(0)
        
        for channel in self.channels.values():
            if channel.pygame_channel:
                channel.pygame_channel.stop()
        
        pygame.mixer.quit()
        self.logger.info("Audio Manager cleaned up")


# Global audio manager instance
_audio_manager: Optional[AudioManager] = None


def get_audio_manager() -> AudioManager:
    """Get the global audio manager instance."""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager


def initialize_audio_manager(config_path: Optional[str] = None) -> AudioManager:
    """Initialize the global audio manager."""
    global _audio_manager
    _audio_manager = AudioManager(config_path)
    return _audio_manager