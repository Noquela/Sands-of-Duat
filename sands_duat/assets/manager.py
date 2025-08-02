"""
Asset Manager

Central management system for all game assets with loading,
caching, and hot-reload capabilities.
"""

import pygame
from pathlib import Path
from typing import Dict, Optional, Any, Union
from enum import Enum
import logging

from .loader import AssetLoader
from .cache import AssetCache


class AssetType(Enum):
    """Types of assets that can be managed."""
    IMAGE = "image"
    SOUND = "sound"
    MUSIC = "music"
    FONT = "font"


class AssetManager:
    """
    Central asset manager for loading and caching game resources.
    
    Provides unified interface for accessing all game assets
    with automatic loading, caching, and memory management.
    """
    
    def __init__(self, assets_root: Optional[Path] = None):
        self.assets_root = assets_root or Path(__file__).parent
        self.loader = AssetLoader(self.assets_root)
        self.cache = AssetCache()
        self.logger = logging.getLogger(__name__)
        
        # Initialize pygame subsystems as needed
        if not pygame.get_init():
            pygame.init()
    
    def load_image(self, image_path: Union[str, Path], use_cache: bool = True) -> Optional[pygame.Surface]:
        """Load an image asset."""
        if use_cache:
            cached = self.cache.get(str(image_path), AssetType.IMAGE)
            if cached:
                return cached
        
        image = self.loader.load_image(image_path)
        if image and use_cache:
            self.cache.store(str(image_path), image, AssetType.IMAGE)
        
        return image
    
    def load_sound(self, sound_path: Union[str, Path], use_cache: bool = True) -> Optional[pygame.mixer.Sound]:
        """Load a sound effect asset."""
        if use_cache:
            cached = self.cache.get(str(sound_path), AssetType.SOUND)
            if cached:
                return cached
        
        sound = self.loader.load_sound(sound_path)
        if sound and use_cache:
            self.cache.store(str(sound_path), sound, AssetType.SOUND)
        
        return sound
    
    def load_font(self, font_path: Union[str, Path], size: int, use_cache: bool = True) -> Optional[pygame.font.Font]:
        """Load a font asset."""
        cache_key = f"{font_path}_{size}"
        
        if use_cache:
            cached = self.cache.get(cache_key, AssetType.FONT)
            if cached:
                return cached
        
        font = self.loader.load_font(font_path, size)
        if font and use_cache:
            self.cache.store(cache_key, font, AssetType.FONT)
        
        return font
    
    def get_card_art(self, card_id: str) -> Optional[pygame.Surface]:
        """Get processed card artwork by card ID."""
        # Look for processed art first
        clean_path = self.assets_root / "art_clean" / f"{card_id}.png"
        if clean_path.exists():
            return self.load_image(clean_path)
        
        # Fall back to raw art if available
        raw_path = self.assets_root / "art_raw" / f"{card_id}.png"
        if raw_path.exists():
            return self.load_image(raw_path)
        
        # Return placeholder if no art found
        return self.get_placeholder_image("card")
    
    def get_enemy_art(self, enemy_id: str) -> Optional[pygame.Surface]:
        """Get processed enemy artwork by enemy ID."""
        clean_path = self.assets_root / "art_clean" / f"enemy_{enemy_id}.png"
        if clean_path.exists():
            return self.load_image(clean_path)
        
        raw_path = self.assets_root / "art_raw" / f"enemy_{enemy_id}.png"
        if raw_path.exists():
            return self.load_image(raw_path)
        
        return self.get_placeholder_image("enemy")
    
    def get_placeholder_image(self, asset_type: str) -> pygame.Surface:
        """Get a placeholder image for missing assets."""
        placeholder_path = self.assets_root / "placeholders" / f"{asset_type}_placeholder.png"
        
        if placeholder_path.exists():
            return self.load_image(placeholder_path, use_cache=True)
        
        # Generate simple colored rectangle as fallback
        surface = pygame.Surface((64, 64))
        surface.fill((128, 128, 128))  # Gray placeholder
        return surface
    
    def preload_card_assets(self, card_ids: list[str]) -> None:
        """Preload card assets for better performance."""
        for card_id in card_ids:
            self.get_card_art(card_id)
    
    def preload_enemy_assets(self, enemy_ids: list[str]) -> None:
        """Preload enemy assets for better performance."""
        for enemy_id in enemy_ids:
            self.get_enemy_art(enemy_id)
    
    def clear_cache(self) -> None:
        """Clear all cached assets."""
        self.cache.clear()
        self.logger.info("Asset cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()
    
    def shutdown(self) -> None:
        """Clean shutdown of asset manager."""
        self.clear_cache()
        pygame.quit()