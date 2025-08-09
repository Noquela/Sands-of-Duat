"""
Professional Audio Manager - SPRINT 6: Egyptian Underworld Audio Experience
Provides immersive sound design with dynamic mixing and Egyptian atmosphere.
"""

import pygame
import numpy as np
import os
import random
import time
import math
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from pathlib import Path

from ..core.constants import Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT

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

class AudioManager:
    """
    Professional audio manager with Egyptian underworld atmosphere.
    Handles dynamic music transitions and immersive sound effects.
    """
    
    def __init__(self):
        """Initialize the audio system."""
        # Initialize pygame mixer with high quality settings
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        # Audio state
        self.master_volume = 0.7
        self.music_volume = 0.6
        self.sfx_volume = 0.8
        self.ambient_volume = 0.4
        
        # Current tracks
        self.current_track: Optional[AudioTrack] = None
        self.is_playing = False
        self.fade_in_progress = False
        
        # Sound effect cache
        self.sound_effects: Dict[SoundEffect, pygame.mixer.Sound] = {}
        self.ambient_sounds: List[pygame.mixer.Sound] = []
        
        # Dynamic audio
        self.ambient_timer = 0.0
        self.next_ambient_time = random.uniform(5.0, 15.0)
        
        # Combat audio state
        self.combat_intensity = 0.0  # 0.0 to 1.0
        self.last_combat_event = 0.0
        
        # Load audio assets
        self._create_procedural_audio()
        
        print("Egyptian Audio Manager initialized with underworld atmosphere")
    
    def _create_procedural_audio(self):
        """Create procedural audio since we don't have audio files."""
        try:
            # Create synthetic Egyptian-themed sound effects
            self._create_ui_sounds()
            self._create_combat_sounds()
            self._create_ambient_sounds()
            
            print("Procedural Egyptian audio assets created")
            
        except Exception as e:
            print(f"Audio creation failed: {e}")
    
    def _create_ui_sounds(self):
        """Create UI sound effects."""
        # Button hover - soft sand sound
        hover_sound = self._create_tone(220, 0.1, fade_out=True)
        self.sound_effects[SoundEffect.BUTTON_HOVER] = hover_sound
        
        # Button click - crisp temple bell
        click_sound = self._create_bell_sound(440, 0.2)
        self.sound_effects[SoundEffect.BUTTON_CLICK] = click_sound
        
        # Transition - mystical whoosh
        transition_sound = self._create_whoosh_sound(0.5)
        self.sound_effects[SoundEffect.TRANSITION] = transition_sound
    
    def _create_combat_sounds(self):
        """Create combat sound effects."""
        # Card play - papyrus rustle + mystical chime
        card_sound = self._create_layered_sound([
            self._create_noise_burst(0.1, pitch=800),
            self._create_bell_sound(660, 0.15)
        ])
        self.sound_effects[SoundEffect.CARD_PLAY] = card_sound
        
        # Card hover - subtle mystical hum
        hover_sound = self._create_tone(110, 0.08, fade_out=True)
        self.sound_effects[SoundEffect.CARD_HOVER] = hover_sound
        
        # Damage dealt - impact with decay
        damage_sound = self._create_impact_sound(0.3)
        self.sound_effects[SoundEffect.DAMAGE_DEALT] = damage_sound
        
        # Healing - ascending chimes
        healing_sound = self._create_healing_chimes()
        self.sound_effects[SoundEffect.HEALING] = healing_sound
        
        # Victory fanfare - triumphant Egyptian theme
        victory_sound = self._create_victory_fanfare()
        self.sound_effects[SoundEffect.VICTORY_FANFARE] = victory_sound
        
        # Defeat sound - somber underworld theme
        defeat_sound = self._create_defeat_sound()
        self.sound_effects[SoundEffect.DEFEAT_SOUND] = defeat_sound
        
        # Mana gain - mystical energy sound
        mana_sound = self._create_mana_sound()
        self.sound_effects[SoundEffect.MANA_GAIN] = mana_sound
    
    def _create_ambient_sounds(self):
        """Create ambient Egyptian underworld sounds."""
        # Desert wind
        wind_sound = self._create_wind_sound(2.0)
        self.ambient_sounds.append(wind_sound)
        
        # Distant temple bells
        bell_sound = self._create_distant_bells()
        self.ambient_sounds.append(bell_sound)
        
        # Mystical energy pulses
        energy_sound = self._create_energy_pulse()
        self.ambient_sounds.append(energy_sound)
    
    def _create_tone(self, frequency: float, duration: float, 
                    fade_out: bool = False) -> pygame.mixer.Sound:
        """Create a pure tone."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        # Generate sine wave using numpy for proper array
        time_array = np.arange(frames) / sample_rate
        wave = np.sin(frequency * 2 * np.pi * time_array)
        
        # Apply fade out if requested
        if fade_out:
            fade_factor = 1.0 - (time_array / duration)
            wave *= fade_factor
        
        # Convert to 16-bit stereo
        wave = (wave * 32767 * 0.3).astype(np.int16)
        stereo_wave = np.column_stack([wave, wave])
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def _create_bell_sound(self, frequency: float, duration: float) -> pygame.mixer.Sound:
        """Create a bell-like sound with harmonics."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        time_array = np.arange(frames) / sample_rate
        
        # Bell harmonics
        fundamental = np.sin(frequency * 2 * np.pi * time_array)
        harmonic2 = 0.5 * np.sin(frequency * 2.76 * 2 * np.pi * time_array)
        harmonic3 = 0.25 * np.sin(frequency * 5.4 * 2 * np.pi * time_array)
        
        # Combine harmonics
        wave = fundamental + harmonic2 + harmonic3
        
        # Exponential decay for bell-like sound
        decay = np.exp(-3 * time_array / duration)
        wave *= decay
        
        # Convert to 16-bit stereo
        wave = (wave * 32767 * 0.2).astype(np.int16)
        stereo_wave = np.column_stack([wave, wave])
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def _create_noise_burst(self, duration: float, pitch: float = 1000) -> pygame.mixer.Sound:
        """Create a noise burst for papyrus-like sounds."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            # White noise
            noise = random.uniform(-1, 1)
            
            # High-pass filter for papyrus effect
            if i > 0:
                noise = 0.7 * noise + 0.3 * arr[-1][0] / 32767
            
            # Exponential decay
            decay = math.exp(-10 * i / frames)
            noise *= decay
            
            # Convert to 16-bit
            noise = int(noise * 32767 * 0.15)
            arr.append([noise, noise])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_whoosh_sound(self, duration: float) -> pygame.mixer.Sound:
        """Create a whoosh sound for transitions."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Swept frequency for whoosh effect
            freq = 100 + 200 * (i / frames)
            wave = math.sin(freq * 2 * math.pi * time_point)
            
            # Add noise component
            noise = random.uniform(-0.3, 0.3)
            wave = 0.7 * wave + 0.3 * noise
            
            # Envelope - start and end quiet
            envelope = math.sin(math.pi * i / frames)
            wave *= envelope
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.25)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_impact_sound(self, duration: float) -> pygame.mixer.Sound:
        """Create an impact sound for damage."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            # Sharp attack with quick decay
            attack_phase = min(1.0, i / (frames * 0.05))  # Quick attack
            decay_phase = math.exp(-8 * i / frames)  # Exponential decay
            
            # Low frequency thump with harmonics
            wave = math.sin(80 * 2 * math.pi * i / sample_rate)
            wave += 0.3 * math.sin(160 * 2 * math.pi * i / sample_rate)
            
            # Add noise for impact texture
            noise = random.uniform(-0.5, 0.5)
            wave = 0.8 * wave + 0.2 * noise
            
            # Apply envelope
            wave *= attack_phase * decay_phase
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.4)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_healing_chimes(self) -> pygame.mixer.Sound:
        """Create ascending chimes for healing."""
        sample_rate = 44100
        duration = 0.8
        frames = int(duration * sample_rate)
        
        # Ascending frequencies
        frequencies = [523, 659, 784, 1047]  # C, E, G, C (major chord)
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            wave = 0
            
            # Play chimes in sequence
            for j, freq in enumerate(frequencies):
                start_time = j * 0.15
                if time_point >= start_time:
                    chime_time = time_point - start_time
                    chime_wave = math.sin(freq * 2 * math.pi * chime_time)
                    chime_wave *= math.exp(-3 * chime_time)  # Decay
                    wave += chime_wave * 0.25
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.3)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_victory_fanfare(self) -> pygame.mixer.Sound:
        """Create a victory fanfare."""
        sample_rate = 44100
        duration = 2.0
        frames = int(duration * sample_rate)
        
        # Victory chord progression
        chord_times = [0.0, 0.5, 1.0, 1.5]
        chords = [
            [262, 330, 392],  # C major
            [294, 370, 440],  # D major
            [330, 415, 494],  # E major
            [523, 659, 784]   # C major octave
        ]
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            wave = 0
            
            # Play appropriate chord
            chord_index = min(3, int(time_point * 2))
            chord = chords[chord_index]
            
            for freq in chord:
                note_wave = math.sin(freq * 2 * math.pi * time_point)
                wave += note_wave * 0.2
            
            # Add brightness with harmonics
            wave += 0.1 * math.sin(523 * 4 * 2 * math.pi * time_point)
            
            # Envelope
            envelope = 1.0 - (time_point / duration) * 0.3  # Slight fade
            wave *= envelope
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.4)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_defeat_sound(self) -> pygame.mixer.Sound:
        """Create a defeat sound."""
        sample_rate = 44100
        duration = 1.5
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Descending minor chord
            freq1 = 220 * (1 - 0.3 * time_point / duration)  # Descending fundamental
            freq2 = 262 * (1 - 0.3 * time_point / duration)  # Minor third
            freq3 = 330 * (1 - 0.3 * time_point / duration)  # Fifth
            
            wave = (math.sin(freq1 * 2 * math.pi * time_point) +
                   0.7 * math.sin(freq2 * 2 * math.pi * time_point) +
                   0.5 * math.sin(freq3 * 2 * math.pi * time_point)) / 3
            
            # Fade out
            envelope = 1.0 - (time_point / duration)
            wave *= envelope
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.3)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_mana_sound(self) -> pygame.mixer.Sound:
        """Create a mana gain sound."""
        sample_rate = 44100
        duration = 0.6
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Ascending mystical tone
            base_freq = 440
            freq = base_freq * (1 + 0.5 * time_point / duration)
            
            wave = math.sin(freq * 2 * math.pi * time_point)
            
            # Add sparkle with higher harmonics
            sparkle = 0.3 * math.sin(freq * 3 * 2 * math.pi * time_point)
            wave += sparkle
            
            # Bell-like decay
            envelope = math.exp(-2 * time_point / duration)
            wave *= envelope
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.25)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_wind_sound(self, duration: float) -> pygame.mixer.Sound:
        """Create a wind sound for ambience."""
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            # Filtered noise for wind effect
            noise = random.uniform(-1, 1)
            
            # Low-pass filter
            if i > 0:
                noise = 0.95 * arr[-1][0] / 32767 + 0.05 * noise
            
            # Slow amplitude modulation
            mod = 0.7 + 0.3 * math.sin(2 * math.pi * i / (sample_rate * 3))
            noise *= mod
            
            # Convert to 16-bit
            noise = int(noise * 32767 * 0.1)
            arr.append([noise, noise])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_distant_bells(self) -> pygame.mixer.Sound:
        """Create distant temple bells."""
        sample_rate = 44100
        duration = 3.0
        frames = int(duration * sample_rate)
        
        bell_times = [0.0, 1.2, 2.1]
        bell_freqs = [220, 330, 275]
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            wave = 0
            
            for bell_time, freq in zip(bell_times, bell_freqs):
                if time_point >= bell_time:
                    bell_age = time_point - bell_time
                    bell_wave = self._create_bell_sound(freq, 2.0)
                    # This is simplified - in practice we'd properly mix the bell
                    if bell_age < 2.0:
                        wave += 0.1 * math.sin(freq * 2 * math.pi * bell_age) * math.exp(-bell_age)
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.15)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_energy_pulse(self) -> pygame.mixer.Sound:
        """Create mystical energy pulse."""
        sample_rate = 44100
        duration = 1.5
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Pulsing low frequency
            pulse_freq = 60
            pulse = math.sin(pulse_freq * 2 * math.pi * time_point)
            
            # Modulate with higher frequency
            mod_freq = 440
            modulation = 0.3 * math.sin(mod_freq * 2 * math.pi * time_point)
            
            wave = pulse * (1 + modulation)
            
            # Fade in and out
            envelope = math.sin(math.pi * time_point / duration)
            wave *= envelope
            
            # Convert to 16-bit
            wave = int(wave * 32767 * 0.08)
            arr.append([wave, wave])
        
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _create_layered_sound(self, sounds: List[pygame.mixer.Sound]) -> pygame.mixer.Sound:
        """Layer multiple sounds together."""
        if not sounds:
            return self._create_tone(440, 0.1)
        
        # For simplicity, return the first sound
        # In a full implementation, we'd properly mix the audio arrays
        return sounds[0]
    
    def play_music(self, track: AudioTrack, fade_in: float = 1.0):
        """Play background music with fade in."""
        if track == self.current_track:
            return
        
        # Stop current music
        if self.is_playing:
            pygame.mixer.music.fadeout(int(fade_in * 500))
        
        # Since we don't have actual music files, we simulate music
        self.current_track = track
        self.is_playing = True
        
        print(f"🎵 Playing {track.name} music (simulated)")
    
    def stop_music(self, fade_out: float = 1.0):
        """Stop background music with fade out."""
        if self.is_playing:
            pygame.mixer.music.fadeout(int(fade_out * 1000))
            self.is_playing = False
            self.current_track = None
    
    def play_sound(self, effect: SoundEffect, volume: Optional[float] = None):
        """Play a sound effect."""
        if effect not in self.sound_effects:
            return
        
        sound = self.sound_effects[effect]
        
        # Set volume
        if volume is None:
            volume = self.sfx_volume
        else:
            volume = min(1.0, volume * self.sfx_volume)
        
        sound.set_volume(volume * self.master_volume)
        sound.play()
    
    def play_ambient_sound(self):
        """Play a random ambient sound."""
        if self.ambient_sounds and random.random() < 0.3:
            sound = random.choice(self.ambient_sounds)
            sound.set_volume(self.ambient_volume * self.master_volume * 0.5)
            sound.play()
    
    def update(self, dt: float, current_screen: str = "menu"):
        """Update audio system."""
        self.ambient_timer += dt
        
        # Play ambient sounds periodically
        if self.ambient_timer >= self.next_ambient_time:
            self.play_ambient_sound()
            self.ambient_timer = 0.0
            self.next_ambient_time = random.uniform(8.0, 20.0)
        
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
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    
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
        """Handle combat events for dynamic audio."""
        self.combat_intensity = min(1.0, self.combat_intensity + intensity * 0.1)
        self.last_combat_event = time.time()
        
        # Decay combat intensity over time
        time_since_event = time.time() - self.last_combat_event
        if time_since_event > 2.0:
            self.combat_intensity *= 0.95
    
    def shutdown(self):
        """Clean shutdown of audio system."""
        pygame.mixer.stop()
        pygame.mixer.quit()
        print("🎵 Audio system shutdown complete")

# Global audio manager instance
audio_manager = AudioManager()