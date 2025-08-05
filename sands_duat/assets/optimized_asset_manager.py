"""
Optimized Asset Manager for High-Quality Game Assets

Performance-focused asset management system designed for:
- High-quality 1024x1024 backgrounds
- 512x768 card images
- Sprite animations and UI elements
- RTX 5070 GPU optimization with fallbacks

Key features:
- Intelligent caching with LRU eviction
- Background asset loading
- GPU texture compression
- LOD (Level of Detail) system
- Memory pool management
- Asset streaming for large collections
"""

import pygame
import threading
import time
import hashlib
import json
import gc
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import OrderedDict
import pickle
import zlib
from concurrent.futures import ThreadPoolExecutor, Future
import weakref

from ..core.performance_profiler import profile_operation


class AssetType(Enum):
    """Types of game assets with different optimization strategies."""
    BACKGROUND = "background"      # Large 1024x1024+ images
    CARD_ART = "card_art"         # 512x768 card images
    CHARACTER = "character"        # Character sprites
    UI_ELEMENT = "ui_element"     # UI components
    PARTICLE = "particle"         # Small particle textures
    AUDIO = "audio"               # Sound files
    FONT = "font"                 # Font files


class QualityLevel(Enum):
    """Asset quality levels for LOD system."""
    ULTRA = "ultra"      # Original resolution
    HIGH = "high"        # 75% resolution
    MEDIUM = "medium"    # 50% resolution
    LOW = "low"          # 25% resolution


@dataclass
class AssetMetadata:
    """Metadata for asset management."""
    path: str
    asset_type: AssetType
    file_size: int
    width: int
    height: int
    last_accessed: float
    access_count: int
    memory_usage: int
    compressed_size: int = 0
    quality_variants: Dict[QualityLevel, str] = field(default_factory=dict)
    load_time_ms: float = 0.0
    checksum: str = ""


class AssetCache:
    """LRU cache with memory management for game assets."""
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory = 0
        
        # OrderedDict for LRU behavior
        self.cache: OrderedDict[str, pygame.Surface] = OrderedDict()
        self.metadata: Dict[str, AssetMetadata] = {}
        
        # Weak references for automatic cleanup
        self.weak_refs: Dict[str, weakref.ref] = {}
        
        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "memory_usage_mb": 0.0
        }
    
    def get(self, key: str) -> Optional[pygame.Surface]:
        """Get asset from cache, updating LRU order."""
        if key in self.cache:
            # Move to end (most recently used)
            surface = self.cache.pop(key)
            self.cache[key] = surface
            
            # Update metadata
            if key in self.metadata:
                self.metadata[key].last_accessed = time.time()
                self.metadata[key].access_count += 1
            
            self.stats["hits"] += 1
            return surface
        
        self.stats["misses"] += 1
        return None
    
    def put(self, key: str, surface: pygame.Surface, metadata: AssetMetadata):
        """Add asset to cache with memory management."""
        # Calculate memory usage
        if hasattr(surface, 'get_size'):
            width, height = surface.get_size()
            memory_usage = width * height * 4  # Assume RGBA
        else:
            memory_usage = 1024  # Default estimate
        
        # Ensure we have space
        self._ensure_space(memory_usage)
        
        # Add to cache
        self.cache[key] = surface
        metadata.memory_usage = memory_usage
        metadata.last_accessed = time.time()
        self.metadata[key] = metadata
        
        self.current_memory += memory_usage
        self._update_stats()
    
    def _ensure_space(self, required_bytes: int):
        """Ensure cache has space for new asset."""
        while (self.current_memory + required_bytes > self.max_memory_bytes and 
               len(self.cache) > 0):
            # Remove least recently used item
            oldest_key = next(iter(self.cache))
            self.remove(oldest_key)
            self.stats["evictions"] += 1
    
    def remove(self, key: str):
        """Remove asset from cache."""
        if key in self.cache:
            surface = self.cache.pop(key)
            if key in self.metadata:
                self.current_memory -= self.metadata[key].memory_usage
                del self.metadata[key]
            self._update_stats()
    
    def clear(self):
        """Clear entire cache."""
        self.cache.clear()
        self.metadata.clear()
        self.current_memory = 0
        self._update_stats()
    
    def _update_stats(self):
        """Update cache statistics."""
        self.stats["memory_usage_mb"] = self.current_memory / (1024 * 1024)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        hit_rate = 0.0
        total_requests = self.stats["hits"] + self.stats["misses"]
        if total_requests > 0:
            hit_rate = self.stats["hits"] / total_requests
        
        return {
            **self.stats,
            "hit_rate": hit_rate,
            "cached_assets": len(self.cache),
            "current_memory_mb": self.current_memory / (1024 * 1024),
            "max_memory_mb": self.max_memory_bytes / (1024 * 1024)
        }


class BackgroundLoader:
    """Background asset loading system."""
    
    def __init__(self, max_workers: int = 3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loading_futures: Dict[str, Future] = {}
        self.load_queue: List[Tuple[str, AssetType, Callable]] = []
        self.loading_callbacks: Dict[str, List[Callable]] = {}
    
    def load_async(self, asset_path: str, asset_type: AssetType, 
                   loader_func: Callable, callback: Optional[Callable] = None) -> Future:
        """Load asset asynchronously."""
        if asset_path in self.loading_futures:
            # Already loading, add callback if provided
            if callback:
                if asset_path not in self.loading_callbacks:
                    self.loading_callbacks[asset_path] = []
                self.loading_callbacks[asset_path].append(callback)
            return self.loading_futures[asset_path]
        
        # Submit loading task
        future = self.executor.submit(self._load_asset, asset_path, loader_func)
        self.loading_futures[asset_path] = future
        
        if callback:
            self.loading_callbacks[asset_path] = [callback]
        
        # Add completion callback
        future.add_done_callback(lambda f: self._on_load_complete(asset_path, f))
        
        return future
    
    def _load_asset(self, asset_path: str, loader_func: Callable) -> Any:
        """Load asset in background thread."""
        start_time = time.time()
        try:
            result = loader_func()
            load_time = (time.time() - start_time) * 1000
            return {"asset": result, "load_time_ms": load_time, "error": None}
        except Exception as e:
            load_time = (time.time() - start_time) * 1000
            return {"asset": None, "load_time_ms": load_time, "error": str(e)}
    
    def _on_load_complete(self, asset_path: str, future: Future):
        """Handle completed asset loading."""
        # Remove from loading futures
        if asset_path in self.loading_futures:
            del self.loading_futures[asset_path]
        
        # Call callbacks
        if asset_path in self.loading_callbacks:
            callbacks = self.loading_callbacks.pop(asset_path)
            result = future.result()
            
            for callback in callbacks:
                try:
                    callback(asset_path, result)
                except Exception as e:
                    print(f"Error in loading callback for {asset_path}: {e}")
    
    def is_loading(self, asset_path: str) -> bool:
        """Check if asset is currently loading."""
        return asset_path in self.loading_futures
    
    def wait_for_asset(self, asset_path: str, timeout: float = 5.0) -> Optional[Any]:
        """Wait for asset to complete loading."""
        if asset_path in self.loading_futures:
            try:
                future = self.loading_futures[asset_path]
                result = future.result(timeout=timeout)
                return result["asset"]
            except Exception:
                return None
        return None
    
    def shutdown(self):
        """Shutdown background loader."""
        self.executor.shutdown(wait=True)


class LODManager:
    """Level of Detail manager for asset optimization."""
    
    def __init__(self, base_quality: QualityLevel = QualityLevel.HIGH):
        self.base_quality = base_quality
        self.quality_settings = {
            QualityLevel.ULTRA: 1.0,
            QualityLevel.HIGH: 0.75,
            QualityLevel.MEDIUM: 0.5,
            QualityLevel.LOW: 0.25
        }
        
        # Dynamic quality adjustment
        self.performance_threshold_fps = 45.0
        self.current_fps = 60.0
        self.fps_history = []
        self.auto_adjust = True
    
    def get_quality_scale(self, asset_type: AssetType, distance: float = 0.0) -> float:
        """Get quality scale factor based on type and distance."""
        base_scale = self.quality_settings[self.base_quality]
        
        # Apply distance-based LOD for certain asset types
        if asset_type in [AssetType.BACKGROUND, AssetType.CHARACTER]:
            if distance > 500:
                base_scale *= 0.5
            elif distance > 200:
                base_scale *= 0.75
        
        return base_scale
    
    def should_use_compressed(self, asset_type: AssetType) -> bool:
        """Determine if asset should use compression."""
        if self.base_quality in [QualityLevel.LOW, QualityLevel.MEDIUM]:
            return True
        
        # Always compress backgrounds in lower quality modes
        if asset_type == AssetType.BACKGROUND and self.base_quality != QualityLevel.ULTRA:
            return True
        
        return False
    
    def update_performance_metrics(self, fps: float):
        """Update performance metrics for dynamic quality adjustment."""
        self.current_fps = fps
        self.fps_history.append(fps)
        
        # Keep only recent history
        if len(self.fps_history) > 60:  # Last 60 frames
            self.fps_history.pop(0)
        
        # Auto-adjust quality if enabled
        if self.auto_adjust and len(self.fps_history) >= 30:
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            
            if avg_fps < self.performance_threshold_fps:
                self._decrease_quality()
            elif avg_fps > 55 and self.base_quality != QualityLevel.ULTRA:
                self._increase_quality()
    
    def _decrease_quality(self):
        """Decrease quality level."""
        quality_levels = [QualityLevel.ULTRA, QualityLevel.HIGH, QualityLevel.MEDIUM, QualityLevel.LOW]
        current_index = quality_levels.index(self.base_quality)
        
        if current_index < len(quality_levels) - 1:
            self.base_quality = quality_levels[current_index + 1]
    
    def _increase_quality(self):
        """Increase quality level."""
        quality_levels = [QualityLevel.ULTRA, QualityLevel.HIGH, QualityLevel.MEDIUM, QualityLevel.LOW]
        current_index = quality_levels.index(self.base_quality)
        
        if current_index > 0:
            self.base_quality = quality_levels[current_index - 1]


class OptimizedAssetManager:
    """
    High-performance asset manager for Sands of Duat.
    
    Features:
    - Intelligent caching with memory management
    - Background loading with thread pool
    - LOD system for performance optimization
    - Asset compression and variants
    - Preloading strategies
    - GPU memory optimization
    """
    
    def __init__(self, cache_size_mb: int = 512, enable_compression: bool = True):
        self.cache = AssetCache(cache_size_mb)
        self.background_loader = BackgroundLoader()
        self.lod_manager = LODManager()
        
        # Asset storage
        self.asset_registry: Dict[str, AssetMetadata] = {}
        self.preload_sets: Dict[str, List[str]] = {}
        
        # Configuration
        self.enable_compression = enable_compression
        self.enable_background_loading = True
        
        # Performance tracking
        self.load_times: Dict[str, float] = {}
        self.memory_warnings = []
        
        # Asset processing pipelines
        self.processors: Dict[AssetType, Callable] = {
            AssetType.BACKGROUND: self._process_background_asset,
            AssetType.CARD_ART: self._process_card_asset,
            AssetType.CHARACTER: self._process_character_asset,
            AssetType.UI_ELEMENT: self._process_ui_asset,
            AssetType.PARTICLE: self._process_particle_asset
        }
        
        # Cache persistence
        self.cache_dir = Path("cache/assets")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize
        self._load_asset_registry()
    
    def load_asset(self, asset_path: str, asset_type: AssetType, 
                  force_reload: bool = False) -> Optional[pygame.Surface]:
        """Load asset with caching and optimization."""
        # Normalize path
        asset_path = str(Path(asset_path).resolve())
        cache_key = self._get_cache_key(asset_path, asset_type)
        
        # Check cache first
        if not force_reload:
            cached_asset = self.cache.get(cache_key)
            if cached_asset:
                return cached_asset
        
        # Load asset
        with profile_operation("asset_loading", {"path": asset_path, "type": asset_type.value}):
            try:
                return self._load_and_process_asset(asset_path, asset_type)
            except Exception as e:
                print(f"Error loading asset {asset_path}: {e}")
                return None
    
    def load_asset_async(self, asset_path: str, asset_type: AssetType,
                        callback: Optional[Callable] = None) -> Future:
        """Load asset asynchronously."""
        asset_path = str(Path(asset_path).resolve())
        
        def loader():
            return self.load_asset(asset_path, asset_type)
        
        return self.background_loader.load_async(asset_path, asset_type, loader, callback)
    
    def _load_and_process_asset(self, asset_path: str, asset_type: AssetType) -> Optional[pygame.Surface]:
        """Load and process asset with optimizations."""
        start_time = time.time()
        
        # Check if file exists
        path_obj = Path(asset_path)
        if not path_obj.exists():
            return None
        
        # Load base asset
        try:
            if asset_type == AssetType.AUDIO:
                # Handle audio separately
                return None  # Audio not handled by this system
            
            # Load image
            surface = pygame.image.load(str(path_obj)).convert_alpha()
            
            # Process asset based on type
            if asset_type in self.processors:
                surface = self.processors[asset_type](surface, asset_path)
            
            # Create metadata
            metadata = AssetMetadata(
                path=asset_path,
                asset_type=asset_type,
                file_size=path_obj.stat().st_size,
                width=surface.get_width(),
                height=surface.get_height(),
                last_accessed=time.time(),
                access_count=1,
                memory_usage=0,  # Will be set by cache
                load_time_ms=(time.time() - start_time) * 1000,
                checksum=self._calculate_checksum(path_obj)
            )
            
            # Cache the asset
            cache_key = self._get_cache_key(asset_path, asset_type)
            self.cache.put(cache_key, surface, metadata)
            
            # Update registry
            self.asset_registry[cache_key] = metadata
            
            # Track load time
            self.load_times[asset_path] = metadata.load_time_ms
            
            return surface
            
        except Exception as e:
            print(f"Error processing asset {asset_path}: {e}")
            return None
    
    def _process_background_asset(self, surface: pygame.Surface, asset_path: str) -> pygame.Surface:
        """Process background asset with optimizations."""
        original_size = surface.get_size()
        
        # Apply LOD scaling
        scale_factor = self.lod_manager.get_quality_scale(AssetType.BACKGROUND)
        
        if scale_factor < 1.0:
            new_width = int(original_size[0] * scale_factor)
            new_height = int(original_size[1] * scale_factor)
            
            # Use smooth scaling for backgrounds
            surface = pygame.transform.smoothscale(surface, (new_width, new_height))
        
        # Apply compression if needed
        if self.lod_manager.should_use_compressed(AssetType.BACKGROUND):
            surface = self._compress_surface(surface)
        
        return surface
    
    def _process_card_asset(self, surface: pygame.Surface, asset_path: str) -> pygame.Surface:
        """Process card asset with optimizations."""
        # Cards should maintain quality for readability
        scale_factor = self.lod_manager.get_quality_scale(AssetType.CARD_ART)
        
        # Only scale if quality is significantly reduced
        if scale_factor < 0.75:
            original_size = surface.get_size()
            new_width = int(original_size[0] * scale_factor)
            new_height = int(original_size[1] * scale_factor)
            surface = pygame.transform.smoothscale(surface, (new_width, new_height))
        
        return surface
    
    def _process_character_asset(self, surface: pygame.Surface, asset_path: str) -> pygame.Surface:
        """Process character asset with optimizations."""
        scale_factor = self.lod_manager.get_quality_scale(AssetType.CHARACTER)
        
        if scale_factor < 1.0:
            original_size = surface.get_size()
            new_width = int(original_size[0] * scale_factor)
            new_height = int(original_size[1] * scale_factor)
            
            # Use smooth scaling for characters
            surface = pygame.transform.smoothscale(surface, (new_width, new_height))
        
        return surface
    
    def _process_ui_asset(self, surface: pygame.Surface, asset_path: str) -> pygame.Surface:
        """Process UI asset - maintain quality for usability."""
        # UI elements should generally maintain quality
        return surface
    
    def _process_particle_asset(self, surface: pygame.Surface, asset_path: str) -> pygame.Surface:
        """Process particle asset - can be heavily optimized."""
        scale_factor = self.lod_manager.get_quality_scale(AssetType.PARTICLE)
        
        # Particles can be aggressively scaled
        if scale_factor < 1.0:
            original_size = surface.get_size()
            new_width = max(1, int(original_size[0] * scale_factor))
            new_height = max(1, int(original_size[1] * scale_factor))
            surface = pygame.transform.scale(surface, (new_width, new_height))
        
        return surface
    
    def _compress_surface(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply compression to surface for memory savings."""
        if not self.enable_compression:
            return surface
        
        # Convert to a more memory-efficient format
        # This is a simplified compression - in practice, you might use
        # more sophisticated texture compression
        
        # Reduce color depth for non-critical assets
        return surface.convert(16)  # 16-bit color
    
    def _get_cache_key(self, asset_path: str, asset_type: AssetType) -> str:
        """Generate cache key for asset."""
        quality_suffix = f"_{self.lod_manager.base_quality.value}"
        compression_suffix = "_compressed" if self.enable_compression else ""
        return f"{asset_path}_{asset_type.value}{quality_suffix}{compression_suffix}"
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum for cache validation."""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
                return file_hash.hexdigest()
        except:
            return ""
    
    def preload_asset_set(self, set_name: str, asset_paths: List[Tuple[str, AssetType]]):
        """Preload a set of assets in the background."""
        self.preload_sets[set_name] = []
        
        for asset_path, asset_type in asset_paths:
            self.preload_sets[set_name].append(asset_path)
            
            if self.enable_background_loading:
                self.load_asset_async(asset_path, asset_type)
            else:
                self.load_asset(asset_path, asset_type)
    
    def is_asset_set_loaded(self, set_name: str) -> bool:
        """Check if all assets in a set are loaded."""
        if set_name not in self.preload_sets:
            return False
        
        for asset_path in self.preload_sets[set_name]:
            if self.background_loader.is_loading(asset_path):
                return False
        
        return True
    
    def wait_for_asset_set(self, set_name: str, timeout: float = 10.0) -> bool:
        """Wait for asset set to finish loading."""
        if set_name not in self.preload_sets:
            return False
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_asset_set_loaded(set_name):
                return True
            time.sleep(0.1)
        
        return False
    
    def update_performance_metrics(self, fps: float):
        """Update performance metrics for dynamic optimization."""
        self.lod_manager.update_performance_metrics(fps)
    
    def optimize_memory_usage(self):
        """Optimize memory usage by clearing unused assets."""
        with profile_operation("memory_optimization"):
            # Force garbage collection
            gc.collect()
            
            # Get current memory usage
            cache_stats = self.cache.get_stats()
            
            if cache_stats["memory_usage_mb"] > cache_stats["max_memory_mb"] * 0.8:
                # Memory usage is high, clean up
                self._cleanup_least_used_assets()
    
    def _cleanup_least_used_assets(self):
        """Clean up least used assets to free memory."""
        # Sort assets by last access time and access count
        sorted_assets = sorted(
            self.cache.metadata.items(),
            key=lambda x: (x[1].last_accessed, x[1].access_count)
        )
        
        # Remove 25% of least used assets
        cleanup_count = len(sorted_assets) // 4
        
        for i in range(cleanup_count):
            asset_key = sorted_assets[i][0]
            self.cache.remove(asset_key)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive asset management statistics."""
        cache_stats = self.cache.get_stats()
        
        # Calculate average load times
        avg_load_time = 0.0
        if self.load_times:
            avg_load_time = sum(self.load_times.values()) / len(self.load_times)
        
        # Get slowest loading assets
        slowest_assets = sorted(
            self.load_times.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "cache_statistics": cache_stats,
            "lod_quality": self.lod_manager.base_quality.value,
            "current_fps": self.lod_manager.current_fps,
            "total_assets_loaded": len(self.asset_registry),
            "average_load_time_ms": avg_load_time,
            "slowest_assets": slowest_assets,
            "preload_sets": {
                name: self.is_asset_set_loaded(name)
                for name in self.preload_sets.keys()
            },
            "memory_warnings": len(self.memory_warnings),
            "background_loading_active": len(self.background_loader.loading_futures)
        }
    
    def _load_asset_registry(self):
        """Load asset registry from cache."""
        registry_path = self.cache_dir / "asset_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path, 'r') as f:
                    data = json.load(f)
                    # Reconstruct metadata objects
                    for key, metadata_dict in data.items():
                        self.asset_registry[key] = AssetMetadata(**metadata_dict)
            except Exception as e:
                print(f"Error loading asset registry: {e}")
    
    def save_asset_registry(self):
        """Save asset registry to cache."""
        registry_path = self.cache_dir / "asset_registry.json"
        try:
            # Convert metadata to dict
            data = {}
            for key, metadata in self.asset_registry.items():
                data[key] = {
                    "path": metadata.path,
                    "asset_type": metadata.asset_type.value,
                    "file_size": metadata.file_size,
                    "width": metadata.width,
                    "height": metadata.height,
                    "last_accessed": metadata.last_accessed,
                    "access_count": metadata.access_count,
                    "memory_usage": metadata.memory_usage,
                    "load_time_ms": metadata.load_time_ms,
                    "checksum": metadata.checksum
                }
            
            with open(registry_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving asset registry: {e}")
    
    def shutdown(self):
        """Shutdown asset manager and save state."""
        self.background_loader.shutdown()
        self.save_asset_registry()
        self.cache.clear()


# Global asset manager instance
_global_asset_manager: Optional[OptimizedAssetManager] = None


def get_asset_manager() -> OptimizedAssetManager:
    """Get or create the global asset manager."""
    global _global_asset_manager
    if _global_asset_manager is None:
        _global_asset_manager = OptimizedAssetManager()
    return _global_asset_manager


def initialize_asset_manager(cache_size_mb: int = 512, enable_compression: bool = True) -> OptimizedAssetManager:
    """Initialize the global asset manager."""
    global _global_asset_manager
    _global_asset_manager = OptimizedAssetManager(cache_size_mb, enable_compression)
    return _global_asset_manager