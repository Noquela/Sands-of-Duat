"""
Assets Management System

Handles loading, caching, and management of game assets including
AI-generated art, audio files, and fonts for Sands of Duat.

Key Features:
- Asset loading and caching
- AI-generated art pipeline integration
- Audio management and sound effects
- Font loading for Egyptian-themed typography
- Asset hot-reloading for development

Directory Structure:
- art_raw/: AI-generated base images from ComfyUI
- art_clean/: Upscaled and processed final artwork
- audio/: Sound effects, music, and ambient audio
- fonts/: Egyptian-themed fonts and typography assets

The assets system is designed to work with the AI art generation
pipeline while providing fast loading and efficient memory usage
during gameplay.
"""

from .manager import AssetManager, AssetType
from .loader import AssetLoader
from .cache import AssetCache

__all__ = [
    'AssetManager',
    'AssetType',
    'AssetLoader', 
    'AssetCache'
]