#!/usr/bin/env python3
"""
SANDS OF DUAT - ASSET LOADING SYSTEM
===================================

Manages loading and caching of all Egyptian assets including:
- 71 high-quality Egyptian artwork pieces from final_dataset
- Card artwork, backgrounds, UI elements
- Proper memory management and performance optimization
"""

import pygame
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class AssetCategory(Enum):
    """Categories of Egyptian assets"""
    GODS = "egyptian_god"
    ARTIFACTS = "egyptian_artifact"
    OBJECTS = "egyptian_object"
    MYTHS = "egyptian_myth"
    STYLES = "egyptian_style"
    SCENES = "egyptian_god_scene"
    UNDERWORLD_LOCATIONS = "underworld_location"
    UNDERWORLD_SCENES = "underworld_scene"
    COMPLEX = "egyptian_complex"

class EgyptianAssetLoader:
    """
    Manages loading and caching of all Egyptian assets.
    
    Features:
    - Lazy loading for performance
    - Asset categorization by Egyptian theme
    - Memory management with LRU cache
    - Quality-based asset selection
    - Metadata integration
    """
    
    def __init__(self, assets_path: Optional[Path] = None):
        self.assets_path = assets_path or self._get_assets_path()
        self.final_dataset_path = self.assets_path / "images" / "lora_training" / "final_dataset"
        
        # Asset caches
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._metadata_cache: Dict[str, dict] = {}
        self._asset_registry: Dict[AssetCategory, List[str]] = {}
        
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
        logger.info("Initializing Egyptian Asset Loader...")
        
        # Check if assets exist
        if not self.final_dataset_path.exists():
            logger.error(f"Final dataset not found at: {self.final_dataset_path}")
            raise FileNotFoundError(f"Egyptian assets not found at {self.final_dataset_path}")
        
        # Load metadata if available
        self._load_metadata()
        
        # Scan and categorize assets
        self._scan_assets()
        
        logger.info(f"Asset loader initialized with {self.get_total_asset_count()} Egyptian assets")
    
    def _load_metadata(self):
        """Load metadata from the final dataset."""
        metadata_file = self.final_dataset_path / "metadata.jsonl"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            filename = data.get('file_name', '')
                            if filename:
                                self._metadata_cache[filename] = data
                logger.info(f"Loaded metadata for {len(self._metadata_cache)} assets")
            except Exception as e:
                logger.warning(f"Could not load metadata: {e}")
    
    def _scan_assets(self):
        """Scan and categorize all available Egyptian assets."""
        for category in AssetCategory:
            self._asset_registry[category] = []
        
        # Scan PNG files in final dataset
        png_files = list(self.final_dataset_path.glob("*.png"))
        
        for png_file in png_files:
            filename = png_file.name
            
            # Categorize by filename prefix
            for category in AssetCategory:
                if filename.startswith(category.value):
                    self._asset_registry[category].append(filename)
                    break
        
        # Log categorization results
        for category, files in self._asset_registry.items():
            if files:
                logger.info(f"{category.name}: {len(files)} assets")
    
    def get_total_asset_count(self) -> int:
        """Get total number of available assets."""
        return sum(len(files) for files in self._asset_registry.values())
    
    def get_assets_by_category(self, category: AssetCategory) -> List[str]:
        """Get all asset filenames for a specific category."""
        return self._asset_registry.get(category, []).copy()
    
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
        
        # Load from disk
        image_path = self.final_dataset_path / filename
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
    
    def load_card_art(self, category: AssetCategory, index: int = 0) -> Optional[pygame.Surface]:
        """
        Load card art from a specific category.
        
        Args:
            category: Asset category to load from
            index: Index within the category (0-based)
            
        Returns:
            Card-sized pygame Surface or None
        """
        assets = self.get_assets_by_category(category)
        if not assets or index >= len(assets):
            logger.warning(f"No asset at index {index} for category {category.name}")
            return None
        
        filename = assets[index]
        return self.load_image(filename, self.target_card_size)
    
    def get_random_card_art(self, category: AssetCategory) -> Optional[pygame.Surface]:
        """Get random card art from a category."""
        import random
        assets = self.get_assets_by_category(category)
        if not assets:
            return None
        
        filename = random.choice(assets)
        return self.load_image(filename, self.target_card_size)
    
    def get_highest_quality_asset(self, category: AssetCategory) -> Optional[pygame.Surface]:
        """Get the highest quality asset from a category based on filename quality indicators."""
        assets = self.get_assets_by_category(category)
        if not assets:
            return None
        
        # Sort by quality indicator in filename (higher q values = better quality)
        def extract_quality(filename: str) -> int:
            try:
                # Look for pattern like "_q84.png"
                parts = filename.split('_q')
                if len(parts) > 1:
                    quality_str = parts[-1].split('.')[0]
                    return int(quality_str)
            except (ValueError, IndexError):
                pass
            return 0
        
        best_asset = max(assets, key=extract_quality)
        return self.load_image(best_asset, self.target_card_size)
    
    def preload_essential_assets(self):
        """Preload essential assets for smooth gameplay."""
        logger.info("Preloading essential Egyptian assets...")
        
        # Preload one high-quality asset from each category for immediate use
        for category in AssetCategory:
            assets = self.get_assets_by_category(category)
            if assets:
                # Load the first asset from each category
                self.load_card_art(category, 0)
        
        logger.info("Essential assets preloaded")
    
    def get_asset_metadata(self, filename: str) -> Dict:
        """Get metadata for a specific asset."""
        return self._metadata_cache.get(filename, {})
    
    def clear_cache(self):
        """Clear the image cache to free memory."""
        self._image_cache.clear()
        logger.info("Asset cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cached_images': len(self._image_cache),
            'max_cache_size': self.max_cache_size,
            'total_categories': len(AssetCategory),
            'total_assets': self.get_total_asset_count()
        }

# Global asset loader instance
_asset_loader: Optional[EgyptianAssetLoader] = None

def get_asset_loader() -> EgyptianAssetLoader:
    """Get the global asset loader instance."""
    global _asset_loader
    if _asset_loader is None:
        _asset_loader = EgyptianAssetLoader()
    return _asset_loader

def initialize_assets():
    """Initialize the global asset loader."""
    global _asset_loader
    _asset_loader = EgyptianAssetLoader()
    _asset_loader.preload_essential_assets()
    return _asset_loader