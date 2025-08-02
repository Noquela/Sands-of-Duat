"""
Asset Cache

Memory management and caching system for loaded assets.
"""

import pygame
from typing import Dict, Any, Optional
from enum import Enum
import weakref
import gc
import logging

from .manager import AssetType


class AssetCache:
    """
    Asset caching system with memory management.
    
    Provides intelligent caching of loaded assets with
    memory usage tracking and cleanup capabilities.
    """
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: Dict[str, Dict[AssetType, Any]] = {}
        self.memory_usage: Dict[str, int] = {}
        self.access_count: Dict[str, int] = {}
        self.logger = logging.getLogger(__name__)
    
    def store(self, key: str, asset: Any, asset_type: AssetType) -> None:
        """Store an asset in the cache."""
        if key not in self.cache:
            self.cache[key] = {}
            self.access_count[key] = 0
        
        self.cache[key][asset_type] = asset
        self.access_count[key] += 1
        
        # Estimate memory usage
        memory_size = self._estimate_asset_size(asset, asset_type)
        self.memory_usage[key] = memory_size
        
        # Check if we need to clean up memory
        if self.get_total_memory_usage() > self.max_memory_bytes:
            self._cleanup_memory()
    
    def get(self, key: str, asset_type: AssetType) -> Optional[Any]:
        """Retrieve an asset from the cache."""
        if key in self.cache and asset_type in self.cache[key]:
            self.access_count[key] += 1
            return self.cache[key][asset_type]
        return None
    
    def remove(self, key: str, asset_type: Optional[AssetType] = None) -> None:
        """Remove an asset or all assets for a key from the cache."""
        if key not in self.cache:
            return
        
        if asset_type:
            # Remove specific asset type
            if asset_type in self.cache[key]:
                del self.cache[key][asset_type]
                if not self.cache[key]:  # If no assets left for this key
                    del self.cache[key]
                    del self.memory_usage[key]
                    del self.access_count[key]
        else:
            # Remove all assets for this key
            del self.cache[key]
            del self.memory_usage[key]
            del self.access_count[key]
    
    def clear(self) -> None:
        """Clear all cached assets."""
        self.cache.clear()
        self.memory_usage.clear()
        self.access_count.clear()
        
        # Force garbage collection
        gc.collect()
        
        self.logger.info("Asset cache cleared")
    
    def get_total_memory_usage(self) -> int:
        """Get total estimated memory usage in bytes."""
        return sum(self.memory_usage.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "total_assets": sum(len(assets) for assets in self.cache.values()),
            "total_keys": len(self.cache),
            "memory_usage_mb": self.get_total_memory_usage() / (1024 * 1024),
            "max_memory_mb": self.max_memory_bytes / (1024 * 1024),
            "memory_utilization": (self.get_total_memory_usage() / self.max_memory_bytes) * 100
        }
    
    def _estimate_asset_size(self, asset: Any, asset_type: AssetType) -> int:
        """Estimate the memory size of an asset."""
        if asset_type == AssetType.IMAGE and isinstance(asset, pygame.Surface):
            # Estimate image size: width * height * bytes_per_pixel
            return asset.get_width() * asset.get_height() * asset.get_bytesize()
        
        elif asset_type == AssetType.SOUND and isinstance(asset, pygame.mixer.Sound):
            # Rough estimate for sound size
            try:
                # This is an approximation - pygame doesn't provide exact size
                return asset.get_length() * 44100 * 2 * 2  # seconds * sample_rate * channels * bytes_per_sample
            except:
                return 1024 * 1024  # Default 1MB estimate
        
        elif asset_type == AssetType.FONT and isinstance(asset, pygame.font.Font):
            # Fonts are relatively small
            return 64 * 1024  # 64KB estimate
        
        else:
            # Default estimate
            return 1024 * 1024  # 1MB
    
    def _cleanup_memory(self) -> None:
        """Clean up memory by removing least-accessed assets."""
        if not self.cache:
            return
        
        # Sort by access count (ascending) to remove least-used assets first
        sorted_keys = sorted(self.access_count.keys(), key=lambda k: self.access_count[k])
        
        removed_count = 0
        for key in sorted_keys:
            if self.get_total_memory_usage() <= self.max_memory_bytes * 0.8:  # Target 80% usage
                break
            
            self.remove(key)
            removed_count += 1
        
        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} assets from cache")
            gc.collect()  # Force garbage collection