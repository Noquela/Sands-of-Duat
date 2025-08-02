"""
Asset Loader

Low-level asset loading functionality for images, sounds, and fonts.
"""

import pygame
from pathlib import Path
from typing import Optional, Union
import logging


class AssetLoader:
    """
    Low-level asset loading functionality.
    
    Handles the actual file I/O and pygame-specific loading
    for different asset types.
    """
    
    def __init__(self, assets_root: Path):
        self.assets_root = assets_root
        self.logger = logging.getLogger(__name__)
    
    def load_image(self, image_path: Union[str, Path]) -> Optional[pygame.Surface]:
        """Load an image file."""
        try:
            # Convert to absolute path if relative
            if not Path(image_path).is_absolute():
                image_path = self.assets_root / image_path
            
            if not Path(image_path).exists():
                self.logger.warning(f"Image file not found: {image_path}")
                return None
            
            surface = pygame.image.load(str(image_path))
            
            # Convert to display format for better performance
            if surface.get_alpha() is not None:
                surface = surface.convert_alpha()
            else:
                surface = surface.convert()
            
            self.logger.debug(f"Loaded image: {image_path}")
            return surface
            
        except pygame.error as e:
            self.logger.error(f"Failed to load image {image_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error loading image {image_path}: {e}")
            return None
    
    def load_sound(self, sound_path: Union[str, Path]) -> Optional[pygame.mixer.Sound]:
        """Load a sound file."""
        try:
            # Convert to absolute path if relative
            if not Path(sound_path).is_absolute():
                sound_path = self.assets_root / sound_path
            
            if not Path(sound_path).exists():
                self.logger.warning(f"Sound file not found: {sound_path}")
                return None
            
            sound = pygame.mixer.Sound(str(sound_path))
            self.logger.debug(f"Loaded sound: {sound_path}")
            return sound
            
        except pygame.error as e:
            self.logger.error(f"Failed to load sound {sound_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error loading sound {sound_path}: {e}")
            return None
    
    def load_font(self, font_path: Union[str, Path], size: int) -> Optional[pygame.font.Font]:
        """Load a font file."""
        try:
            # Convert to absolute path if relative
            if not Path(font_path).is_absolute():
                font_path = self.assets_root / font_path
            
            if not Path(font_path).exists():
                # Fall back to system default font
                self.logger.warning(f"Font file not found: {font_path}, using default")
                return pygame.font.Font(None, size)
            
            font = pygame.font.Font(str(font_path), size)
            self.logger.debug(f"Loaded font: {font_path} (size: {size})")
            return font
            
        except pygame.error as e:
            self.logger.error(f"Failed to load font {font_path}: {e}")
            # Return default font as fallback
            return pygame.font.Font(None, size)
        except Exception as e:
            self.logger.error(f"Unexpected error loading font {font_path}: {e}")
            return pygame.font.Font(None, size)