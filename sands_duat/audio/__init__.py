"""
Audio System for Sands of Duat

Provides audio management including music, sound effects, and spatial audio
for an immersive Egyptian-themed gaming experience.
"""

from .audio_manager import AudioManager, SoundType
from .sound_effects import SoundEffectLibrary
from .music_manager import MusicManager

__all__ = ['AudioManager', 'SoundType', 'SoundEffectLibrary', 'MusicManager']