"""
Enhanced Asset Streaming System for Sands of Duat

Advanced asset loading and streaming system designed for premium visual quality
while maintaining 60fps performance on RTX 5070 and scaling for lower-end hardware.

Key Features:
- Smart preloading with priority queuing
- Texture streaming for large backgrounds
- Memory-efficient asset caching
- Hardware-adaptive quality scaling
- GPU texture compression
- Async loading with progress tracking
"""

import pygame
import asyncio
import threading
import time
import json
import os
import gc
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, Future
import logging
from collections import OrderedDict
import psutil
import weakref

from .professional_asset_manager import AssetQuality, AssetCategory, get_professional_asset_manager
from ..core.performance_profiler import profile_operation


class LoadPriority(Enum):
    """Asset loading priority levels."""
    CRITICAL = 1      # Must be loaded before screen shows
    HIGH = 2          # Should be loaded quickly
    MEDIUM = 3        # Can be loaded in background
    LOW = 4           # Load when system is idle
    PRELOAD = 5       # Speculative loading


class CompressionFormat(Enum):
    """Texture compression formats."""
    NONE = "none"
    DXT1 = "dxt1"      # Good for textures without alpha
    DXT5 = "dxt5"      # Good for textures with alpha
    ETC2 = "etc2"      # Mobile-friendly compression
    ASTC = "astc"      # High-quality compression


@dataclass
class AssetRequest:
    """Request for asset loading with metadata."""
    asset_id: str
    priority: LoadPriority
    size: Optional[Tuple[int, int]] = None
    quality: Optional[AssetQuality] = None
    callback: Optional[Callable] = None
    context: Dict[str, Any] = None
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
        if self.context is None:
            self.context = {}


@dataclass
class HardwareProfile:
    """Hardware capability profile for quality adaptation."""
    gpu_memory_mb: int
    system_memory_mb: int
    gpu_compute_score: float  # Normalized 0-1 score
    supports_compression: bool
    max_texture_size: int
    quality_preference: AssetQuality


class MemoryBudgetManager:
    """Manages memory usage and asset eviction."""
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.current_memory_bytes = 0
        self.asset_memory_map: Dict[str, int] = {}
        self.lru_order: OrderedDict = OrderedDict()
        self.protected_assets: set = set()  # Assets that shouldn't be evicted
        
    def register_asset(self, asset_id: str, memory_size: int, protected: bool = False):
        """Register asset memory usage."""
        if asset_id in self.asset_memory_map:
            self.current_memory_bytes -= self.asset_memory_map[asset_id]
        
        self.asset_memory_map[asset_id] = memory_size
        self.current_memory_bytes += memory_size
        self.lru_order[asset_id] = time.time()
        
        if protected:
            self.protected_assets.add(asset_id)
        
        # Trigger cleanup if over budget
        if self.current_memory_bytes > self.max_memory_bytes:
            self._evict_assets()
    
    def access_asset(self, asset_id: str):
        """Mark asset as recently used."""
        if asset_id in self.lru_order:
            self.lru_order.move_to_end(asset_id)
    
    def _evict_assets(self) -> List[str]:
        """Evict assets to free memory."""
        evicted = []
        target_bytes = self.max_memory_bytes * 0.8  # Free to 80% capacity
        
        for asset_id in list(self.lru_order.keys()):
            if self.current_memory_bytes <= target_bytes:
                break
            
            if asset_id not in self.protected_assets:
                memory_size = self.asset_memory_map.get(asset_id, 0)
                self.current_memory_bytes -= memory_size
                del self.asset_memory_map[asset_id]
                del self.lru_order[asset_id]
                evicted.append(asset_id)
        
        return evicted
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            "current_memory_mb": self.current_memory_bytes / (1024 * 1024),
            "max_memory_mb": self.max_memory_bytes / (1024 * 1024),
            "utilization_percent": (self.current_memory_bytes / self.max_memory_bytes) * 100,
            "asset_count": len(self.asset_memory_map),
            "protected_assets": len(self.protected_assets)
        }


class TextureCompressor:
    """Handles texture compression for different hardware capabilities."""
    
    def __init__(self):
        self.compression_cache: Dict[str, pygame.Surface] = {}
        self.supported_formats = self._detect_compression_support()
    
    def _detect_compression_support(self) -> List[CompressionFormat]:
        """Detect which compression formats are supported."""
        # Simplified detection - in practice, would check OpenGL/Vulkan capabilities
        return [CompressionFormat.NONE]  # Default to no compression
    
    def compress_texture(self, surface: pygame.Surface, format: CompressionFormat, 
                        quality_level: float = 0.8) -> pygame.Surface:
        """Compress texture using specified format."""
        cache_key = f"{id(surface)}_{format.value}_{quality_level}"
        
        if cache_key in self.compression_cache:
            return self.compression_cache[cache_key]
        
        # For now, implement lossy compression via scaling and color reduction
        if format == CompressionFormat.NONE:
            compressed = surface
        else:
            # Simulate compression by reducing color depth and slightly scaling
            if quality_level < 1.0:
                # Reduce bit depth to simulate compression
                compressed = surface.convert(16)  # 16-bit color
                # Convert back to 32-bit for consistency
                compressed = compressed.convert_alpha()
            else:
                compressed = surface
        
        self.compression_cache[cache_key] = compressed
        return compressed
    
    def estimate_compressed_size(self, width: int, height: int, format: CompressionFormat) -> int:
        """Estimate compressed texture size in bytes."""
        if format == CompressionFormat.NONE:
            return width * height * 4  # RGBA
        elif format == CompressionFormat.DXT1:
            return max(8, (width + 3) // 4 * (height + 3) // 4 * 8)
        elif format == CompressionFormat.DXT5:
            return max(16, (width + 3) // 4 * (height + 3) // 4 * 16)
        else:
            return width * height * 2  # Estimate 50% compression


class HardwareProfiler:
    """Profiles hardware capabilities for optimal settings."""
    
    def __init__(self):
        self.profile = self._detect_hardware_profile()
        self.logger = logging.getLogger(__name__)
    
    def _detect_hardware_profile(self) -> HardwareProfile:
        """Detect and profile hardware capabilities."""
        # Get system memory
        system_memory = psutil.virtual_memory().total // (1024 * 1024)
        
        # Estimate GPU memory (simplified)
        gpu_memory = self._estimate_gpu_memory()
        
        # Calculate GPU compute score based on available information
        gpu_score = self._calculate_gpu_score(gpu_memory)
        
        # Determine optimal quality based on hardware
        if gpu_memory >= 8192 and system_memory >= 16384:  # High-end
            quality = AssetQuality.HADES
        elif gpu_memory >= 4096 and system_memory >= 8192:  # Mid-range
            quality = AssetQuality.HADES
        else:  # Lower-end
            quality = AssetQuality.STANDARD
        
        profile = HardwareProfile(
            gpu_memory_mb=gpu_memory,
            system_memory_mb=system_memory,
            gpu_compute_score=gpu_score,
            supports_compression=True,
            max_texture_size=4096,
            quality_preference=quality
        )
        
        self.logger.info(f"Hardware profile: GPU={gpu_memory}MB, RAM={system_memory}MB, "
                        f"Score={gpu_score:.2f}, Quality={quality.value}")
        
        return profile
    
    def _estimate_gpu_memory(self) -> int:
        """Estimate GPU memory (simplified heuristic)."""
        try:
            # Try to get actual GPU info if available
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return int(result.stdout.strip())
        except:
            pass
        
        # Fallback estimation based on system memory
        system_memory = psutil.virtual_memory().total // (1024 * 1024)
        if system_memory >= 32768:
            return 8192  # Assume high-end GPU
        elif system_memory >= 16384:
            return 4096  # Assume mid-range GPU
        else:
            return 2048  # Assume lower-end GPU
    
    def _calculate_gpu_score(self, gpu_memory: int) -> float:
        """Calculate normalized GPU performance score."""
        # Simplified scoring based on memory
        if gpu_memory >= 8192:
            return 1.0
        elif gpu_memory >= 4096:
            return 0.8
        elif gpu_memory >= 2048:
            return 0.6
        else:
            return 0.4


class AssetStreamingManager:
    """Main asset streaming system with advanced optimizations."""
    
    def __init__(self, max_memory_mb: int = 512, max_workers: int = 4):
        self.professional_manager = get_professional_asset_manager()
        self.memory_manager = MemoryBudgetManager(max_memory_mb)
        self.texture_compressor = TextureCompressor()
        self.hardware_profiler = HardwareProfiler()
        
        # Loading queue and workers
        self.load_queue: List[AssetRequest] = []
        self.load_queue_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_loads: Dict[str, Future] = {}
        
        # Caching system
        self.stream_cache: Dict[str, pygame.Surface] = {}
        self.cache_metadata: Dict[str, Dict[str, Any]] = {}
        
        # Progress tracking
        self.loading_progress: Dict[str, float] = {}
        self.load_callbacks: Dict[str, List[Callable]] = {}
        
        # Statistics
        self.stats = {
            "assets_loaded": 0,
            "assets_evicted": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_load_time": 0.0,
            "average_load_time": 0.0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background processing
        self._start_background_processing()
    
    def _start_background_processing(self):
        """Start background asset processing thread."""
        def process_queue():
            while True:
                try:
                    with self.load_queue_lock:
                        if self.load_queue:
                            # Sort by priority and timestamp
                            self.load_queue.sort(key=lambda req: (req.priority.value, req.timestamp))
                            request = self.load_queue.pop(0)
                        else:
                            request = None
                    
                    if request:
                        self._process_load_request(request)
                    else:
                        time.sleep(0.1)  # No work available
                        
                except Exception as e:
                    self.logger.error(f"Error in background processing: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=process_queue, daemon=True)
        thread.start()
    
    def request_asset(self, asset_id: str, priority: LoadPriority = LoadPriority.MEDIUM,
                     size: Optional[Tuple[int, int]] = None, 
                     quality: Optional[AssetQuality] = None,
                     callback: Optional[Callable] = None) -> bool:
        """Request asset loading with specified priority."""
        with profile_operation(f"asset_request_{asset_id}"):
            # Check if already loaded
            cache_key = self._get_cache_key(asset_id, size, quality)
            if cache_key in self.stream_cache:
                self.stats["cache_hits"] += 1
                self.memory_manager.access_asset(cache_key)
                if callback:
                    callback(self.stream_cache[cache_key])
                return True
            
            self.stats["cache_misses"] += 1
            
            # Check if already in queue or loading
            if asset_id in [req.asset_id for req in self.load_queue] or asset_id in self.active_loads:
                if callback:
                    if asset_id not in self.load_callbacks:
                        self.load_callbacks[asset_id] = []
                    self.load_callbacks[asset_id].append(callback)
                return True
            
            # Add to load queue
            request = AssetRequest(
                asset_id=asset_id,
                priority=priority,
                size=size,
                quality=quality or self.hardware_profiler.profile.quality_preference,
                callback=callback
            )
            
            with self.load_queue_lock:
                self.load_queue.append(request)
            
            return True
    
    def _get_cache_key(self, asset_id: str, size: Optional[Tuple[int, int]], 
                      quality: Optional[AssetQuality]) -> str:
        """Generate cache key for asset."""
        key_parts = [asset_id]
        if size:
            key_parts.append(f"{size[0]}x{size[1]}")
        if quality:
            key_parts.append(quality.value)
        return "_".join(key_parts)
    
    def _process_load_request(self, request: AssetRequest):
        """Process individual load request."""
        start_time = time.time()
        
        try:
            # Start loading
            future = self.executor.submit(self._load_asset_sync, request)
            self.active_loads[request.asset_id] = future
            
            # Wait for completion
            surface = future.result()
            
            if surface:
                cache_key = self._get_cache_key(request.asset_id, request.size, request.quality)
                
                # Apply compression if beneficial
                compressed_surface = self._apply_optimal_compression(surface)
                
                # Cache the asset
                self.stream_cache[cache_key] = compressed_surface
                self.cache_metadata[cache_key] = {
                    "original_size": (surface.get_width(), surface.get_height()),
                    "compressed_size": (compressed_surface.get_width(), compressed_surface.get_height()),
                    "load_time": time.time() - start_time,
                    "quality": request.quality.value if request.quality else "auto"
                }
                
                # Update memory tracking
                memory_size = compressed_surface.get_width() * compressed_surface.get_height() * 4
                is_protected = request.priority in [LoadPriority.CRITICAL, LoadPriority.HIGH]
                self.memory_manager.register_asset(cache_key, memory_size, is_protected)
                
                # Execute callbacks
                if request.callback:
                    request.callback(compressed_surface)
                
                if request.asset_id in self.load_callbacks:
                    for callback in self.load_callbacks[request.asset_id]:
                        callback(compressed_surface)
                    del self.load_callbacks[request.asset_id]
                
                # Update statistics
                load_time = time.time() - start_time
                self.stats["assets_loaded"] += 1
                self.stats["total_load_time"] += load_time
                self.stats["average_load_time"] = self.stats["total_load_time"] / self.stats["assets_loaded"]
                
                self.logger.debug(f"Loaded asset {request.asset_id} in {load_time:.3f}s")
        
        except Exception as e:
            self.logger.error(f"Failed to load asset {request.asset_id}: {e}")
        
        finally:
            # Clean up
            if request.asset_id in self.active_loads:
                del self.active_loads[request.asset_id]
    
    def _load_asset_sync(self, request: AssetRequest) -> Optional[pygame.Surface]:
        """Synchronously load asset."""
        return self.professional_manager.get_asset(request.asset_id, request.size)
    
    def _apply_optimal_compression(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply optimal compression based on hardware profile."""
        if not self.hardware_profiler.profile.supports_compression:
            return surface
        
        # Determine optimal compression format
        has_alpha = surface.get_flags() & pygame.SRCALPHA
        if has_alpha:
            format = CompressionFormat.DXT5
        else:
            format = CompressionFormat.DXT1
        
        # Apply compression based on GPU score
        quality_level = self.hardware_profiler.profile.gpu_compute_score
        
        return self.texture_compressor.compress_texture(surface, format, quality_level)
    
    def get_asset_immediate(self, asset_id: str, size: Optional[Tuple[int, int]] = None,
                           quality: Optional[AssetQuality] = None) -> Optional[pygame.Surface]:
        """Get asset immediately if available in cache."""
        cache_key = self._get_cache_key(asset_id, size, quality)
        
        if cache_key in self.stream_cache:
            self.memory_manager.access_asset(cache_key)
            self.stats["cache_hits"] += 1
            return self.stream_cache[cache_key]
        
        self.stats["cache_misses"] += 1
        return None
    
    def preload_for_screen(self, screen_name: str, priority: LoadPriority = LoadPriority.MEDIUM):
        """Preload assets for a specific screen."""
        with profile_operation(f"preload_screen_{screen_name}"):
            if screen_name in ["menu", "main_menu"]:
                self.request_asset("env_menu_background", priority)
                self.request_asset("ui_ornate_button", priority)
            
            elif screen_name in ["combat", "dynamic_combat"]:
                self.request_asset("env_combat_background", priority)
                # Preload character sprites
                for character in ["player_character", "anubis_guardian", "desert_scorpion"]:
                    self.request_asset(f"char_{character}", priority)
                
                # Preload common cards
                starter_cards = ["sand_grain", "desert_whisper", "tomb_strike", "ankh_blessing"]
                for card in starter_cards:
                    self.request_asset(f"card_{card}", priority, (300, 420))
            
            elif screen_name == "deck_builder":
                self.request_asset("env_deck_builder_background", priority)
                # Preload all cards at deck builder size
                card_names = [
                    "sand_strike", "anubis_judgment", "ra_solar_flare", "isis_grace",
                    "tomb_strike", "scarab_swarm", "ankh_blessing", "pyramid_power",
                    "papyrus_scroll", "desert_whisper", "thoths_wisdom", 
                    "pharaohs_resurrection", "mummys_wrath", "sand_grain"
                ]
                for card in card_names:
                    self.request_asset(f"card_{card}", LoadPriority.LOW, (220, 300))
            
            elif screen_name == "progression":
                self.request_asset("env_progression_background", priority)
    
    def clear_cache(self, preserve_protected: bool = True):
        """Clear asset cache with optional protection for critical assets."""
        if preserve_protected:
            # Only clear unprotected assets
            to_remove = []
            for cache_key in self.stream_cache.keys():
                if cache_key not in self.memory_manager.protected_assets:
                    to_remove.append(cache_key)
            
            for cache_key in to_remove:
                del self.stream_cache[cache_key]
                if cache_key in self.cache_metadata:
                    del self.cache_metadata[cache_key]
                if cache_key in self.memory_manager.asset_memory_map:
                    memory_size = self.memory_manager.asset_memory_map[cache_key]
                    self.memory_manager.current_memory_bytes -= memory_size
                    del self.memory_manager.asset_memory_map[cache_key]
                    del self.memory_manager.lru_order[cache_key]
        else:
            # Clear everything
            self.stream_cache.clear()
            self.cache_metadata.clear()
            self.memory_manager.asset_memory_map.clear()
            self.memory_manager.lru_order.clear()
            self.memory_manager.protected_assets.clear()
            self.memory_manager.current_memory_bytes = 0
        
        # Force garbage collection
        gc.collect()
    
    def get_loading_progress(self, asset_id: str) -> float:
        """Get loading progress for specific asset (0.0 to 1.0)."""
        if asset_id in self.stream_cache:
            return 1.0
        elif asset_id in self.active_loads:
            return 0.5  # Simplified - in practice would track actual progress
        elif asset_id in [req.asset_id for req in self.load_queue]:
            return 0.0
        else:
            return -1.0  # Not requested
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return {
            "loading_stats": self.stats.copy(),
            "memory_stats": self.memory_manager.get_memory_stats(),
            "hardware_profile": asdict(self.hardware_profiler.profile),
            "cache_stats": {
                "cached_assets": len(self.stream_cache),
                "cache_metadata_count": len(self.cache_metadata),
                "active_loads": len(self.active_loads),
                "queue_length": len(self.load_queue)
            },
            "compression_stats": {
                "compressed_textures": len(self.texture_compressor.compression_cache),
                "supported_formats": [f.value for f in self.texture_compressor.supported_formats]
            }
        }
    
    def optimize_for_hardware(self) -> Dict[str, Any]:
        """Optimize settings based on detected hardware."""
        profile = self.hardware_profiler.profile
        
        # Adjust memory budget based on GPU memory
        if profile.gpu_memory_mb >= 8192:
            new_budget = 1024  # 1GB for high-end
        elif profile.gpu_memory_mb >= 4096:
            new_budget = 512   # 512MB for mid-range
        else:
            new_budget = 256   # 256MB for lower-end
        
        if new_budget != self.memory_manager.max_memory_bytes // (1024 * 1024):
            self.memory_manager.max_memory_bytes = new_budget * 1024 * 1024
            self.logger.info(f"Adjusted memory budget to {new_budget}MB based on hardware")
        
        # Update professional manager quality preference
        self.professional_manager.set_quality_preference(profile.quality_preference == AssetQuality.HADES)
        
        return {
            "memory_budget_mb": new_budget,
            "quality_preference": profile.quality_preference.value,
            "gpu_score": profile.gpu_compute_score,
            "optimizations_applied": True
        }


# Global streaming manager
_global_streaming_manager = None

def get_asset_streaming_manager(max_memory_mb: int = 512) -> AssetStreamingManager:
    """Get global asset streaming manager."""
    global _global_streaming_manager
    if _global_streaming_manager is None:
        _global_streaming_manager = AssetStreamingManager(max_memory_mb)
        # Auto-optimize for detected hardware
        _global_streaming_manager.optimize_for_hardware()
    return _global_streaming_manager

def preload_critical_assets():
    """Preload critical game assets with high priority."""
    manager = get_asset_streaming_manager()
    
    # Critical menu assets
    manager.request_asset("env_menu_background", LoadPriority.CRITICAL)
    
    # Critical combat assets
    manager.request_asset("env_combat_background", LoadPriority.HIGH)
    manager.request_asset("char_player_character", LoadPriority.HIGH)
    
    # Essential card art
    essential_cards = ["sand_grain", "desert_whisper", "tomb_strike"]
    for card in essential_cards:
        manager.request_asset(f"card_{card}", LoadPriority.HIGH, (300, 420))

def request_screen_assets(screen_name: str, priority: LoadPriority = LoadPriority.MEDIUM):
    """Request all assets for a specific screen."""
    manager = get_asset_streaming_manager()
    manager.preload_for_screen(screen_name, priority)

def get_asset_with_fallback(asset_id: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
    """Get asset with automatic fallback to professional manager if not cached."""
    manager = get_asset_streaming_manager()
    
    # Try streaming cache first
    surface = manager.get_asset_immediate(asset_id, size)
    if surface:
        return surface
    
    # Fallback to professional manager for immediate needs
    return manager.professional_manager.get_asset(asset_id, size)