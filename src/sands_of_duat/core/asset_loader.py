#!/usr/bin/env python3
"""
SANDS OF DUAT - ASSET LOADING SYSTEM
===================================

Manages loading and caching of all Egyptian assets including:
- 44 high-quality AI-generated game assets from generated_art
- Card artwork, backgrounds, character portraits, UI elements
- Proper memory management and performance optimization
"""

import pygame
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class AssetType(Enum):
    """Types of generated game assets"""
    CARD_LEGENDARY = "legendary"
    CARD_EPIC = "epic" 
    CARD_RARE = "rare"
    CARD_COMMON = "common"
    BACKGROUND = "bg_"
    CHARACTER = "char_"
    UI_FRAME = "ui_card_frame_"
    UI_ICON = "ui_"
    UI_BUTTON = "ui_"

class GeneratedAssetLoader:
    """
    Manages loading and caching of AI-generated game assets.
    
    Features:
    - Lazy loading for performance
    - Asset categorization by game function
    - Memory management with LRU cache
    - Direct access to generated artwork
    - Card rarity mapping
    """
    
    def __init__(self, assets_path: Optional[Path] = None):
        self.assets_path = assets_path or self._get_assets_path()
        self.generated_art_path = self.assets_path / "generated_art"
        self.approved_art_path = self.assets_path / "approved_hades_quality"
        
        # Asset caches
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._asset_registry: Dict[AssetType, List[str]] = {}
        
        # Game-specific asset mappings
        self.card_art_mapping = self._create_card_mapping()
        self.background_mapping = self._create_background_mapping()
        self.character_mapping = self._create_character_mapping()
        self.ui_mapping = self._create_ui_mapping()
        
        # Performance settings
        self.max_cache_size = 100  # Maximum cached images
        self.target_card_size = (300, 420)  # Standard card dimensions
        
        # Initialize the asset system
        self._initialize()
    
    def _get_assets_path(self) -> Path:
        """Get the assets directory path."""
        current_dir = Path(__file__).parent
        return current_dir.parent.parent.parent / "assets"
    
    def _initialize(self):
        """Initialize the asset loading system."""
        logger.info("Initializing Generated Asset Loader...")
        
        # Check if approved assets exist (priority), fallback to generated
        if self.approved_art_path.exists():
            logger.info(f"Using approved Hades-quality assets from: {self.approved_art_path}")
        elif not self.generated_art_path.exists():
            logger.error(f"No assets found at: {self.generated_art_path} or {self.approved_art_path}")
            raise FileNotFoundError(f"No assets found")
        
        # Scan and categorize assets
        self._scan_generated_assets()
        
        logger.info(f"Asset loader initialized with {self.get_total_asset_count()} generated assets")
    
    def _create_card_mapping(self) -> Dict[str, str]:
        """Create mapping of card names to their artwork files."""
        return {
            # Legendary Cards - Using actual generated assets
            'Ra - Sun God': 'hades_egyptian_characters_legendary_ra_sun_god_legendary_20250809_145810_20250809.png',
            'Anubis - Judgment': 'hades_egyptian_characters_legendary_anubis_deity_legendary_20250809_145745_20250809.png', 
            'Isis - Protection': 'hades_egyptian_characters_legendary_isis_goddess_legendary_20250809_145834_20250809.png',
            'Set - Chaos Storm': 'hades_egyptian_characters_legendary_set_chaos_god_legendary_20250809_145857_20250809.png',
            
            # Epic Cards - Using actual generated assets
            'Egyptian Warrior': 'hades_egyptian_characters_epic_egyptian_warrior_epic_20250809_145921_20250809.png',
            
            # Rare Cards - Using actual generated assets
            'Mummy Guardian': 'hades_egyptian_characters_rare_mummy_guardian_rare_20250809_150008_20250809.png',
            'Sphinx Guardian': 'hades_egyptian_characters_rare_sphinx_guardian_rare_20250809_145944_20250809.png',
            
            # Common Cards - Will use fallback artwork for now
        }
    
    def _create_background_mapping(self) -> Dict[str, str]:
        """Create mapping of game screens to background files."""
        return {
            'combat': 'hades_egyptian_environments_epic_temple_interior_epic_20250809_150032_20250809.png',
            'menu': 'hades_egyptian_environments_epic_temple_interior_epic_20250809_150032_20250809.png', 
            'deck_builder': 'hades_egyptian_environments_epic_temple_interior_epic_20250809_150032_20250809.png'
        }
    
    def _create_character_mapping(self) -> Dict[str, str]:
        """Create mapping of characters to portrait files."""
        return {
            'player_hero': 'hades_egyptian_characters_epic_egyptian_warrior_epic_20250809_145921_20250809.png',
            'anubis_boss': 'hades_egyptian_characters_legendary_anubis_deity_legendary_20250809_145745_20250809.png',
            'mummy_guardian': 'hades_egyptian_characters_rare_mummy_guardian_rare_20250809_150008_20250809.png',
            'sphinx_guardian': 'hades_egyptian_characters_rare_sphinx_guardian_rare_20250809_145944_20250809.png',
            'ra_deity': 'hades_egyptian_characters_legendary_ra_sun_god_legendary_20250809_145810_20250809.png',
            'isis_goddess': 'hades_egyptian_characters_legendary_isis_goddess_legendary_20250809_145834_20250809.png',
            'set_god': 'hades_egyptian_characters_legendary_set_chaos_god_legendary_20250809_145857_20250809.png'
        }
    
    def _create_ui_mapping(self) -> Dict[str, str]:
        """Create mapping of UI elements to their files."""
        return {
            # Card Frames
            'frame_legendary': 'ui_card_frame_legendary.png',
            'frame_epic': 'ui_card_frame_epic.png',
            'frame_rare': 'ui_card_frame_rare.png',
            'frame_common': 'ui_card_frame_common.png',
            
            # Icons
            'health_icon': 'ui_ankh_health_icon.png',
            'energy_icon': 'ui_scarab_energy_icon.png',
            'time_icon': 'ui_hourglass_icon.png',
            'victory_icon': 'ui_pyramid_victory_icon.png',
            
            # Buttons
            'play_button': 'ui_play_button.png',
            'deck_button': 'ui_deck_button.png',
            'settings_button': 'ui_settings_button.png',
            'exit_button': 'ui_exit_button.png'
        }
    
    def _scan_generated_assets(self):
        """Scan and categorize all generated game assets."""
        for asset_type in AssetType:
            self._asset_registry[asset_type] = []
        
        # First scan approved assets if they exist
        png_files = []
        if self.approved_art_path.exists():
            # Scan all subdirectories in approved assets
            for subdir in ['characters', 'environments', 'ui', 'cards']:
                subdir_path = self.approved_art_path / subdir
                if subdir_path.exists():
                    png_files.extend(list(subdir_path.glob("*.png")))
        
        # Also scan generated_art directory
        if self.generated_art_path.exists():
            png_files.extend(list(self.generated_art_path.glob("*.png")))
        
        for png_file in png_files:
            filename = png_file.name
            
            # Categorize by filename patterns
            if filename.startswith('bg_'):
                self._asset_registry[AssetType.BACKGROUND].append(filename)
            elif filename.startswith('char_'):
                self._asset_registry[AssetType.CHARACTER].append(filename)
            elif filename.startswith('ui_card_frame_'):
                self._asset_registry[AssetType.UI_FRAME].append(filename)
            elif filename.startswith('ui_') and ('button' in filename or 'icon' in filename):
                if 'button' in filename:
                    self._asset_registry[AssetType.UI_BUTTON].append(filename)
                else:
                    self._asset_registry[AssetType.UI_ICON].append(filename)
            else:
                # Card artwork - categorize by card name mapping
                for card_name, card_file in self.card_art_mapping.items():
                    if filename == card_file:
                        if 'ra_sun_god' in filename or 'anubis_judgment' in filename or 'osiris_resurrection' in filename or 'horus_divine_sight' in filename or 'isis_protection' in filename:
                            self._asset_registry[AssetType.CARD_LEGENDARY].append(filename)
                        elif 'thoth_wisdom' in filename or 'bastet_feline_grace' in filename or 'set_chaos_storm' in filename or 'sekhmet_war_cry' in filename or 'pharaoh_divine_mandate' in filename or 'pyramid_power' in filename or 'ankh_blessing' in filename:
                            self._asset_registry[AssetType.CARD_EPIC].append(filename)
                        elif 'mummy_wrath' in filename or 'scarab_swarm' in filename or 'desert_whisper' in filename or 'temple_offering' in filename or 'canopic_jar_ritual' in filename:
                            self._asset_registry[AssetType.CARD_RARE].append(filename)
                        else:
                            self._asset_registry[AssetType.CARD_COMMON].append(filename)
                        break
        
        # Log categorization results
        for asset_type, files in self._asset_registry.items():
            if files:
                logger.info(f"{asset_type.name}: {len(files)} assets")
    
    def get_total_asset_count(self) -> int:
        """Get total number of available assets."""
        return sum(len(files) for files in self._asset_registry.values())
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[str]:
        """Get all asset filenames for a specific type."""
        return self._asset_registry.get(asset_type, []).copy()
    
    def load_image(self, filename: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """
        Load an image asset with optional resizing.
        
        Args:
            filename: Name of the image file
            size: Optional target size (width, height)
            
        Returns:
            Loaded pygame Surface or None if not found
        """
        cache_key = f"{filename}_{size}" if size else filename
        
        # Check cache first
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # Try approved assets first, then fallback to generated
        image_path = None
        
        # Check approved assets directory structure
        if self.approved_art_path.exists():
            # Check characters directory
            char_path = self.approved_art_path / "characters" / filename
            if char_path.exists():
                image_path = char_path
            else:
                # Check environments directory
                env_path = self.approved_art_path / "environments" / filename
                if env_path.exists():
                    image_path = env_path
        
        # Fallback to generated art
        if not image_path:
            image_path = self.generated_art_path / filename
            
        if not image_path.exists():
            logger.warning(f"Asset not found: {filename}")
            return None
        
        try:
            # Load image
            surface = pygame.image.load(str(image_path))
            
            # Resize if requested
            if size:
                surface = pygame.transform.scale(surface, size)
            
            # Cache the image (with LRU management)
            self._cache_image(cache_key, surface)
            
            logger.debug(f"Loaded asset: {filename}")
            return surface
            
        except Exception as e:
            logger.error(f"Failed to load asset {filename}: {e}")
            return None
    
    def _cache_image(self, cache_key: str, surface: pygame.Surface):
        """Cache an image with LRU management."""
        # Simple LRU: remove oldest if cache is full
        if len(self._image_cache) >= self.max_cache_size:
            # Remove the first (oldest) item
            oldest_key = next(iter(self._image_cache))
            del self._image_cache[oldest_key]
        
        self._image_cache[cache_key] = surface
    
    def load_card_art_by_name(self, card_name: str) -> Optional[pygame.Surface]:
        """
        Load card art by card name.
        
        Args:
            card_name: Name of the card to load art for
            
        Returns:
            Card-sized pygame Surface or None
        """
        filename = self.card_art_mapping.get(card_name)
        if not filename:
            logger.warning(f"No artwork mapped for card: {card_name}")
            return None
        
        return self.load_image(filename, self.target_card_size)
    
    def load_background(self, screen_name: str) -> Optional[pygame.Surface]:
        """
        Load background for a specific screen.
        
        Args:
            screen_name: Name of the screen (combat, menu, deck_builder, etc.)
            
        Returns:
            Full-sized pygame Surface or None
        """
        filename = self.background_mapping.get(screen_name)
        if not filename:
            logger.warning(f"No background mapped for screen: {screen_name}")
            return None
        
        return self.load_image(filename)
    
    def load_character_portrait(self, character_name: str) -> Optional[pygame.Surface]:
        """
        Load character portrait by name.
        
        Args:
            character_name: Name of the character
            
        Returns:
            Portrait-sized pygame Surface or None
        """
        filename = self.character_mapping.get(character_name)
        if not filename:
            logger.warning(f"No portrait mapped for character: {character_name}")
            return None
        
        return self.load_image(filename, (512, 768))  # Portrait aspect ratio
    
    def load_ui_element(self, element_name: str) -> Optional[pygame.Surface]:
        """
        Load UI element by name.
        
        Args:
            element_name: Name of the UI element
            
        Returns:
            UI-sized pygame Surface or None
        """
        filename = self.ui_mapping.get(element_name)
        if not filename:
            logger.warning(f"No UI element mapped for: {element_name}")
            return None
        
        return self.load_image(filename)
    
    def get_random_card_art_by_rarity(self, rarity: str) -> Optional[pygame.Surface]:
        """Get random card art by rarity level."""
        import random
        
        rarity_mapping = {
            'legendary': AssetType.CARD_LEGENDARY,
            'epic': AssetType.CARD_EPIC, 
            'rare': AssetType.CARD_RARE,
            'common': AssetType.CARD_COMMON
        }
        
        asset_type = rarity_mapping.get(rarity.lower())
        if not asset_type:
            return None
            
        assets = self.get_assets_by_type(asset_type)
        if not assets:
            return None
        
        filename = random.choice(assets)
        return self.load_image(filename, self.target_card_size)
    
    def get_card_frame_by_rarity(self, rarity: str) -> Optional[pygame.Surface]:
        """Get card frame by rarity level."""
        frame_name = f"frame_{rarity.lower()}"
        return self.load_ui_element(frame_name)
    
    def preload_essential_assets(self):
        """Preload essential assets for smooth gameplay."""
        logger.info("Preloading essential Egyptian assets...")
        
        # Preload essential assets for immediate use
        # Preload one asset from each type
        for asset_type in AssetType:
            assets = self.get_assets_by_type(asset_type)
            if assets:
                # Load the first asset from each type
                self.load_image(assets[0])
        
        # Preload key backgrounds
        self.load_background('menu')
        self.load_background('combat')
        
        logger.info("Essential assets preloaded")
    
    def get_all_card_names(self) -> List[str]:
        """Get all available card names."""
        return list(self.card_art_mapping.keys())
    
    def get_all_backgrounds(self) -> List[str]:
        """Get all available background screen names."""
        return list(self.background_mapping.keys())
    
    def get_all_characters(self) -> List[str]:
        """Get all available character names."""
        return list(self.character_mapping.keys())
    
    def get_all_ui_elements(self) -> List[str]:
        """Get all available UI element names."""
        return list(self.ui_mapping.keys())
    
    def clear_cache(self):
        """Clear the image cache to free memory."""
        self._image_cache.clear()
        logger.info("Asset cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cached_images': len(self._image_cache),
            'max_cache_size': self.max_cache_size,
            'total_types': len(AssetType),
            'total_assets': self.get_total_asset_count()
        }

# Global asset loader instance
_asset_loader: Optional[GeneratedAssetLoader] = None

def get_asset_loader() -> GeneratedAssetLoader:
    """Get the global asset loader instance."""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = GeneratedAssetLoader()
    return _asset_loader

def initialize_assets():
    """Initialize the global asset loader."""
    global _asset_loader
    _asset_loader = GeneratedAssetLoader()
    _asset_loader.preload_essential_assets()
    return _asset_loader