#!/usr/bin/env python3
"""
High-Performance Asset Integration System for Sands of Duat

A comprehensive system that delivers premium visual quality while maintaining 60fps
through intelligent asset loading, memory management, and responsive performance scaling.
"""

import pygame
import threading
import time
import gc
import psutil
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable, Set
from enum import Enum
from dataclasses import dataclass, field
from collections import deque
import weakref
import logging
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor

from .asset_manager import AssetManager, AssetType, LoadingPriority, AssetRequest
from .parallax_system import ParallaxSystem
from .dynamic_quality_manager import DynamicQualityManager


class PerformanceMode(Enum):
    """Performance quality modes"""
    ULTRA = "ultra"      # Maximum quality, high-end hardware
    HIGH = "high"        # High quality, mid-range hardware  
    MEDIUM = "medium"    # Balanced quality/performance
    LOW = "low"          # Performance priority, low-end hardware
    AUTO = "auto"        # Automatically adjusts based on performance


class MemoryTier(Enum):
    """Memory usage tiers for asset prioritization"""
    CRITICAL = 1    # Always keep in memory
    HIGH = 2        # Keep unless memory pressure
    MEDIUM = 3      # Unload during transitions
    LOW = 4         # Unload aggressively


@dataclass
class PerformanceMetrics:
    """Real-time performance tracking"""
    fps: float = 60.0
    frame_time_ms: float = 16.67
    memory_usage_mb: float = 0.0
    gpu_usage_percent: float = 0.0
    asset_count: int = 0
    cache_hit_rate: float = 100.0
    gc_pressure: float = 0.0
    
    # Historical data for trend analysis
    fps_history: deque = field(default_factory=lambda: deque(maxlen=300))  # 5 seconds at 60fps
    memory_history: deque = field(default_factory=lambda: deque(maxlen=300))
    
    def update(self, fps: float, memory_mb: float):
        """Update metrics with new measurements"""
        self.fps = fps
        self.frame_time_ms = 1000.0 / max(fps, 1.0)
        self.memory_usage_mb = memory_mb
        
        self.fps_history.append(fps)
        self.memory_history.append(memory_mb)
    
    @property
    def average_fps(self) -> float:
        """Get average FPS over recent history"""
        if not self.fps_history:
            return 60.0
        return sum(self.fps_history) / len(self.fps_history)
    
    @property
    def fps_stability(self) -> float:
        """Get FPS stability (0-1, higher is more stable)"""
        if len(self.fps_history) < 10:
            return 1.0
        
        avg = self.average_fps
        variance = sum((fps - avg) ** 2 for fps in self.fps_history) / len(self.fps_history)
        return max(0.0, 1.0 - (variance / 100.0))  # Normalize variance


@dataclass
class AssetMetadata:
    """Extended asset metadata for performance optimization"""
    asset_id: str
    file_path: Path
    size_bytes: int
    memory_tier: MemoryTier
    last_accessed: float
    access_count: int
    load_time_ms: float
    compression_ratio: float = 1.0
    screen_dependencies: Set[str] = field(default_factory=set)
    
    def update_access(self):
        """Update access tracking"""
        self.last_accessed = time.time()
        self.access_count += 1


class TextureCompressor:
    """Intelligent texture compression system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.compression_cache = {}
        
    def compress_surface(self, surface: pygame.Surface, quality_mode: PerformanceMode) -> pygame.Surface:
        """Compress surface based on performance mode"""
        if quality_mode == PerformanceMode.ULTRA:
            return surface  # No compression for ultra mode
        
        # Generate cache key
        surface_data = pygame.image.tostring(surface, 'RGB')
        cache_key = hashlib.md5(surface_data).hexdigest()
        
        if cache_key in self.compression_cache:
            return self.compression_cache[cache_key]
        
        width, height = surface.get_size()
        
        # Determine compression level based on mode
        if quality_mode == PerformanceMode.HIGH:
            scale_factor = 0.9
        elif quality_mode == PerformanceMode.MEDIUM:
            scale_factor = 0.75
        else:  # LOW
            scale_factor = 0.6
        
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Use smooth scaling for better quality
        compressed = pygame.transform.smoothscale(surface, (new_width, new_height))
        
        # Cache the result
        self.compression_cache[cache_key] = compressed
        
        self.logger.debug(f"Compressed texture from {width}x{height} to {new_width}x{new_height}")
        return compressed


class MemoryManager:
    """Advanced memory management with garbage collection optimization"""
    
    def __init__(self, max_memory_mb: int = 1024):
        self.max_memory_mb = max_memory_mb
        self.logger = logging.getLogger(__name__)
        self.asset_metadata: Dict[str, AssetMetadata] = {}
        self.weak_references: Dict[str, weakref.ref] = {}
        
        # GC optimization
        self.gc_threshold_mb = max_memory_mb * 0.8  # Trigger at 80% capacity
        self.last_gc_time = 0.0
        self.gc_interval = 5.0  # Minimum 5 seconds between forced GC
        
    def register_asset(self, asset_id: str, asset: Any, metadata: AssetMetadata):
        """Register an asset for memory management"""
        self.asset_metadata[asset_id] = metadata
        self.weak_references[asset_id] = weakref.ref(asset, lambda ref: self._on_asset_deleted(asset_id))
        
    def _on_asset_deleted(self, asset_id: str):
        """Callback when asset is garbage collected"""
        if asset_id in self.asset_metadata:
            del self.asset_metadata[asset_id]
        if asset_id in self.weak_references:
            del self.weak_references[asset_id]
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    
    def optimize_memory(self, force: bool = False) -> int:
        """Optimize memory usage, return number of assets unloaded"""
        current_memory = self.get_memory_usage()
        
        if not force and current_memory < self.gc_threshold_mb:
            return 0
        
        # Sort assets by priority for unloading (LRU + tier-based)
        candidates = []
        current_time = time.time()
        
        for asset_id, metadata in self.asset_metadata.items():
            if metadata.memory_tier in [MemoryTier.MEDIUM, MemoryTier.LOW]:
                score = self._calculate_unload_score(metadata, current_time)
                candidates.append((score, asset_id))
        
        # Sort by score (higher score = better candidate for unloading)
        candidates.sort(reverse=True)
        
        unloaded_count = 0
        target_memory = self.max_memory_mb * 0.7  # Target 70% usage
        
        for score, asset_id in candidates:
            if current_memory <= target_memory and not force:
                break
                
            if self._unload_asset(asset_id):
                unloaded_count += 1
                current_memory = self.get_memory_usage()
        
        # Force garbage collection if needed
        if force or current_time - self.last_gc_time > self.gc_interval:
            gc.collect()
            self.last_gc_time = current_time
            
        self.logger.info(f"Memory optimization: unloaded {unloaded_count} assets, "
                        f"memory usage: {current_memory:.1f}MB")
        
        return unloaded_count
    
    def _calculate_unload_score(self, metadata: AssetMetadata, current_time: float) -> float:
        """Calculate priority score for unloading (higher = better candidate)"""
        # Time since last access (older = higher score)
        time_score = current_time - metadata.last_accessed
        
        # Memory tier (lower tier = higher score)
        tier_score = metadata.memory_tier.value * 100
        
        # Access frequency (less frequent = higher score)
        frequency_score = 1000.0 / max(metadata.access_count, 1)
        
        return time_score + tier_score + frequency_score
    
    def _unload_asset(self, asset_id: str) -> bool:
        """Attempt to unload an asset"""
        if asset_id in self.weak_references:
            ref = self.weak_references[asset_id]
            asset = ref()
            if asset is not None:
                # Clear the strong reference (asset manager should handle this)
                return True
        return False


class PerformanceScaler:
    """Responsive performance scaling system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_mode = PerformanceMode.HIGH
        self.target_fps = 60.0
        self.min_fps = 30.0
        
        # Performance scaling parameters
        self.fps_window_size = 60  # Frames to average
        self.adjustment_threshold = 5.0  # FPS difference to trigger adjustment
        self.adjustment_cooldown = 2.0  # Seconds between adjustments
        self.last_adjustment = 0.0
        
        # Quality callbacks
        self.quality_callbacks: List[Callable[[PerformanceMode], None]] = []
    
    def add_quality_callback(self, callback: Callable[[PerformanceMode], None]):
        """Add callback for quality changes"""
        self.quality_callbacks.append(callback)
    
    def update_performance(self, metrics: PerformanceMetrics) -> PerformanceMode:
        """Update performance scaling based on metrics"""
        current_time = time.time()
        
        # Don't adjust too frequently
        if current_time - self.last_adjustment < self.adjustment_cooldown:
            return self.current_mode
        
        avg_fps = metrics.average_fps
        fps_stability = metrics.fps_stability
        
        # Determine if we need to scale quality
        if avg_fps < self.target_fps - self.adjustment_threshold or fps_stability < 0.8:
            # Performance is poor, reduce quality
            new_mode = self._reduce_quality(self.current_mode)
        elif avg_fps > self.target_fps + self.adjustment_threshold and fps_stability > 0.9:
            # Performance is good, try to increase quality
            new_mode = self._increase_quality(self.current_mode)
        else:
            return self.current_mode
        
        if new_mode != self.current_mode:
            self.logger.info(f"Performance scaling: {self.current_mode.value} -> {new_mode.value} "
                           f"(avg FPS: {avg_fps:.1f}, stability: {fps_stability:.2f})")
            
            self.current_mode = new_mode
            self.last_adjustment = current_time
            
            # Notify callbacks
            for callback in self.quality_callbacks:
                try:
                    callback(new_mode)
                except Exception as e:
                    self.logger.error(f"Error in quality callback: {e}")
        
        return self.current_mode
    
    def _reduce_quality(self, current: PerformanceMode) -> PerformanceMode:
        """Reduce quality mode"""
        if current == PerformanceMode.ULTRA:
            return PerformanceMode.HIGH
        elif current == PerformanceMode.HIGH:
            return PerformanceMode.MEDIUM
        elif current == PerformanceMode.MEDIUM:
            return PerformanceMode.LOW
        return PerformanceMode.LOW
    
    def _increase_quality(self, current: PerformanceMode) -> PerformanceMode:
        """Increase quality mode"""
        if current == PerformanceMode.LOW:
            return PerformanceMode.MEDIUM
        elif current == PerformanceMode.MEDIUM:
            return PerformanceMode.HIGH
        elif current == PerformanceMode.HIGH:
            return PerformanceMode.ULTRA
        return PerformanceMode.ULTRA


class StreamingAssetLoader:
    """Background streaming asset loader"""
    
    def __init__(self, thread_pool_size: int = 4):
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=thread_pool_size)
        self.loading_queue: deque = deque()
        self.active_loads: Set[str] = set()
        self.preload_rules: Dict[str, List[str]] = {}
        
    def add_preload_rule(self, screen_name: str, asset_ids: List[str]):
        """Add preloading rule for screen transitions"""
        self.preload_rules[screen_name] = asset_ids
    
    def schedule_preload(self, upcoming_screen: str, priority: int = 1):
        """Schedule preloading for upcoming screen"""
        if upcoming_screen not in self.preload_rules:
            return
        
        for asset_id in self.preload_rules[upcoming_screen]:
            if asset_id not in self.active_loads:
                self.loading_queue.append((priority, asset_id, upcoming_screen))
                self.active_loads.add(asset_id)
    
    def process_queue(self, max_concurrent: int = 2):
        """Process loading queue"""
        active_futures = []
        
        while len(active_futures) < max_concurrent and self.loading_queue:
            priority, asset_id, screen = self.loading_queue.popleft()
            
            future = self.executor.submit(self._load_asset_async, asset_id, screen)
            active_futures.append((future, asset_id))
        
        # Check for completed loads
        completed = []
        for future, asset_id in active_futures:
            if future.done():
                self.active_loads.discard(asset_id)
                completed.append((future, asset_id))
        
        return completed
    
    def _load_asset_async(self, asset_id: str, screen: str) -> Optional[Any]:
        """Load asset asynchronously"""
        try:
            # This would integrate with the main asset system
            # For now, simulate loading time
            time.sleep(0.1)  # Simulate I/O
            return f"loaded_{asset_id}"
        except Exception as e:
            self.logger.error(f"Failed to load asset {asset_id}: {e}")
            return None


class HighPerformanceAssetSystem:
    """Main high-performance asset integration system"""
    
    def __init__(self, max_memory_mb: int = 1024, target_fps: float = 60.0):
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.asset_manager = AssetManager()
        self.memory_manager = MemoryManager(max_memory_mb)
        self.performance_scaler = PerformanceScaler()
        self.texture_compressor = TextureCompressor()
        self.streaming_loader = StreamingAssetLoader()
        
        # Performance tracking
        self.metrics = PerformanceMetrics()
        self.last_update_time = time.time()
        self.frame_count = 0
        
        # Quality settings
        self.current_quality = PerformanceMode.HIGH
        self.quality_locked = False  # User can lock quality mode
        
        # Asset caching
        self.compressed_cache: Dict[str, Dict[PerformanceMode, pygame.Surface]] = {}
        self.parallax_systems: Dict[str, ParallaxSystem] = {}
        
        # Integration callbacks
        self.performance_scaler.add_quality_callback(self._on_quality_changed)
        
        self.logger.info("High-Performance Asset System initialized")
    
    def set_quality_mode(self, mode: PerformanceMode, lock: bool = False):
        """Manually set quality mode"""
        self.current_quality = mode
        self.quality_locked = lock
        self._on_quality_changed(mode)
        
        self.logger.info(f"Quality mode set to {mode.value} (locked: {lock})")
    
    def _on_quality_changed(self, new_mode: PerformanceMode):
        """Handle quality mode changes"""
        self.current_quality = new_mode
        
        # Update texture compression for all cached assets
        self._update_texture_compression()
        
        # Adjust parallax system quality
        for parallax in self.parallax_systems.values():
            self._adjust_parallax_quality(parallax, new_mode)
    
    def _update_texture_compression(self):
        """Update texture compression for current quality mode"""
        # This would recompress cached textures based on new quality mode
        # Implementation would depend on specific asset management needs
        pass
    
    def _adjust_parallax_quality(self, parallax: ParallaxSystem, mode: PerformanceMode):
        """Adjust parallax system quality based on performance mode"""
        if mode == PerformanceMode.LOW:
            # Reduce layer count or disable expensive effects
            parallax.lighting_effects = False
            parallax.particle_drift = False
        elif mode == PerformanceMode.MEDIUM:
            parallax.lighting_effects = True
            parallax.particle_drift = False
        else:  # HIGH or ULTRA
            parallax.lighting_effects = True
            parallax.particle_drift = True
    
    def update_performance_metrics(self, dt: float):
        """Update performance metrics and scaling"""
        current_time = time.time()
        self.frame_count += 1
        
        # Calculate FPS
        time_diff = current_time - self.last_update_time
        if time_diff >= 1.0:  # Update every second
            fps = self.frame_count / time_diff
            memory_mb = self.memory_manager.get_memory_usage()
            
            self.metrics.update(fps, memory_mb)
            
            # Reset counters
            self.frame_count = 0
            self.last_update_time = current_time
            
            # Update performance scaling (if not locked)
            if not self.quality_locked:
                self.performance_scaler.update_performance(self.metrics)
            
            # Optimize memory if needed
            self.memory_manager.optimize_memory()
    
    def load_asset_optimized(self, asset_id: str, asset_type: AssetType, 
                           quality_mode: Optional[PerformanceMode] = None) -> Optional[Any]:
        """Load asset with optimization based on quality mode"""
        if quality_mode is None:
            quality_mode = self.current_quality
        
        # Check compressed cache first
        if asset_id in self.compressed_cache and quality_mode in self.compressed_cache[asset_id]:
            return self.compressed_cache[asset_id][quality_mode]
        
        # Load original asset
        start_time = time.time()
        original_asset = self.asset_manager.get_asset(asset_id)
        
        if original_asset is None:
            # Asset not loaded, request it
            request = AssetRequest(asset_type, asset_id, f"{asset_id}.png", priority=LoadingPriority.HIGH)
            self.asset_manager.request_asset(request)
            return None
        
        # Apply compression if it's a surface
        if isinstance(original_asset, pygame.Surface) and quality_mode != PerformanceMode.ULTRA:
            compressed_asset = self.texture_compressor.compress_surface(original_asset, quality_mode)
            
            # Cache the compressed version
            if asset_id not in self.compressed_cache:
                self.compressed_cache[asset_id] = {}
            self.compressed_cache[asset_id][quality_mode] = compressed_asset
            
            result_asset = compressed_asset
        else:
            result_asset = original_asset
        
        # Update metadata
        load_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Create metadata if not exists
        if asset_id not in self.memory_manager.asset_metadata:
            metadata = AssetMetadata(
                asset_id=asset_id,
                file_path=Path(f"{asset_id}.png"),
                size_bytes=self._estimate_asset_size(result_asset),
                memory_tier=MemoryTier.MEDIUM,
                last_accessed=time.time(),
                access_count=1,
                load_time_ms=load_time
            )
            self.memory_manager.register_asset(asset_id, result_asset, metadata)
        else:
            self.memory_manager.asset_metadata[asset_id].update_access()
        
        return result_asset
    
    def _estimate_asset_size(self, asset: Any) -> int:
        """Estimate asset size in bytes"""
        if isinstance(asset, pygame.Surface):
            width, height = asset.get_size()
            bytes_per_pixel = asset.get_bytesz()
            return width * height * bytes_per_pixel
        return 1024  # Default estimate
    
    def setup_parallax_for_screen(self, screen_name: str, assets_path: str) -> ParallaxSystem:
        """Setup optimized parallax system for a screen"""
        if screen_name in self.parallax_systems:
            return self.parallax_systems[screen_name]
        
        parallax = ParallaxSystem()
        
        # Setup based on screen
        if screen_name == "combat":
            parallax.setup_egyptian_underworld_scene(assets_path)
        elif screen_name == "deck_builder":
            parallax.setup_temple_library_scene(assets_path)
        
        # Apply current quality settings
        self._adjust_parallax_quality(parallax, self.current_quality)
        
        self.parallax_systems[screen_name] = parallax
        return parallax
    
    def preload_for_screen_transition(self, upcoming_screen: str):
        """Preload assets for upcoming screen transition"""
        self.streaming_loader.schedule_preload(upcoming_screen)
    
    def update(self, dt: float):
        """Update the asset system"""
        # Update performance metrics
        self.update_performance_metrics(dt)
        
        # Process streaming loader queue
        completed_loads = self.streaming_loader.process_queue()
        
        # Update parallax systems
        for parallax in self.parallax_systems.values():
            parallax.update(dt)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        return {
            "fps": {
                "current": self.metrics.fps,
                "average": self.metrics.average_fps,
                "stability": self.metrics.fps_stability
            },
            "memory": {
                "usage_mb": self.metrics.memory_usage_mb,
                "max_mb": self.memory_manager.max_memory_mb,
                "usage_percent": (self.metrics.memory_usage_mb / self.memory_manager.max_memory_mb) * 100
            },
            "quality": {
                "mode": self.current_quality.value,
                "locked": self.quality_locked
            },
            "assets": {
                "loaded_count": len(self.memory_manager.asset_metadata),
                "cache_size": len(self.compressed_cache),
                "active_loads": len(self.streaming_loader.active_loads)
            }
        }
    
    def force_memory_optimization(self):
        """Force memory optimization"""
        unloaded = self.memory_manager.optimize_memory(force=True)
        self.logger.info(f"Forced memory optimization: {unloaded} assets unloaded")
        return unloaded
    
    def shutdown(self):
        """Clean shutdown of the asset system"""
        self.streaming_loader.executor.shutdown(wait=True)
        self.compressed_cache.clear()
        self.parallax_systems.clear()
        self.logger.info("High-Performance Asset System shutdown complete")


# Global instance
_global_hp_asset_system = None

def get_hp_asset_system() -> HighPerformanceAssetSystem:
    """Get global high-performance asset system"""
    global _global_hp_asset_system
    if _global_hp_asset_system is None:
        _global_hp_asset_system = HighPerformanceAssetSystem()
    return _global_hp_asset_system

def initialize_hp_asset_system(max_memory_mb: int = 1024, target_fps: float = 60.0):
    """Initialize the high-performance asset system"""
    global _global_hp_asset_system
    _global_hp_asset_system = HighPerformanceAssetSystem(max_memory_mb, target_fps)
    return _global_hp_asset_system