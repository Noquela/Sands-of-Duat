#!/usr/bin/env python3
"""
Optimized Parallax Renderer for Sands of Duat

High-performance parallax rendering system with layer culling, texture batching,
and GPU-accelerated transformations for smooth 60fps performance.
"""

import pygame
import numpy as np
import math
from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path
import weakref

from .parallax_system import ParallaxLayer, ParallaxSystem


class RenderTechnique(Enum):
    """Rendering optimization techniques"""
    BASIC = "basic"              # Standard pygame blitting
    BATCHED = "batched"          # Batch similar operations
    CULLED = "culled"            # Frustum culling enabled  
    CACHED = "cached"            # Cache rendered layers
    OPTIMIZED = "optimized"      # All optimizations enabled


@dataclass
class ViewFrustum:
    """View frustum for culling calculations"""
    left: float
    right: float
    top: float
    bottom: float
    
    def contains_rect(self, x: float, y: float, width: float, height: float) -> bool:
        """Check if rectangle intersects with frustum"""
        return not (x + width < self.left or x > self.right or 
                   y + height < self.top or y > self.bottom)
    
    def expand(self, margin: float) -> 'ViewFrustum':
        """Expand frustum by margin for preloading"""
        return ViewFrustum(
            self.left - margin,
            self.right + margin, 
            self.top - margin,
            self.bottom + margin
        )


@dataclass  
class RenderBatch:
    """Batch of similar rendering operations"""
    surfaces: List[pygame.Surface] = field(default_factory=list)
    positions: List[Tuple[int, int]] = field(default_factory=list)
    blend_mode: int = pygame.BLEND_ALPHA_SDL2
    alpha: int = 255
    
    def add(self, surface: pygame.Surface, position: Tuple[int, int]):
        """Add surface to batch"""
        self.surfaces.append(surface)
        self.positions.append(position)
    
    def clear(self):
        """Clear batch"""
        self.surfaces.clear()
        self.positions.clear()
    
    def is_empty(self) -> bool:
        """Check if batch is empty"""
        return len(self.surfaces) == 0


class LayerCache:
    """Cache system for pre-rendered layer sections"""
    
    def __init__(self, max_cache_mb: int = 256):
        self.max_cache_mb = max_cache_mb
        self.cache: Dict[str, pygame.Surface] = {}
        self.cache_usage: Dict[str, float] = {}  # Last access time
        self.cache_size_mb = 0.0
        self.logger = logging.getLogger(__name__)
    
    def get_cache_key(self, layer_id: str, x_offset: float, y_offset: float, 
                     width: int, height: int) -> str:
        """Generate cache key for layer section"""
        return f"{layer_id}_{int(x_offset)}_{int(y_offset)}_{width}_{height}"
    
    def get_cached_section(self, cache_key: str) -> Optional[pygame.Surface]:
        """Get cached layer section"""
        if cache_key in self.cache:
            self.cache_usage[cache_key] = pygame.time.get_ticks() / 1000.0
            return self.cache[cache_key]
        return None
    
    def cache_section(self, cache_key: str, surface: pygame.Surface):
        """Cache a layer section"""
        # Estimate surface size in MB
        width, height = surface.get_size()
        bytes_per_pixel = surface.get_bytesz()
        size_mb = (width * height * bytes_per_pixel) / (1024 * 1024)
        
        # Check if we need to free space
        while self.cache_size_mb + size_mb > self.max_cache_mb and self.cache:
            self._evict_oldest()
        
        self.cache[cache_key] = surface
        self.cache_usage[cache_key] = pygame.time.get_ticks() / 1000.0
        self.cache_size_mb += size_mb
    
    def _evict_oldest(self):
        """Evict oldest cached surface"""
        if not self.cache:
            return
            
        oldest_key = min(self.cache_usage.keys(), key=lambda k: self.cache_usage[k])
        
        # Estimate removed size
        surface = self.cache[oldest_key]
        width, height = surface.get_size()
        bytes_per_pixel = surface.get_bytesz()
        size_mb = (width * height * bytes_per_pixel) / (1024 * 1024)
        
        del self.cache[oldest_key]
        del self.cache_usage[oldest_key]
        self.cache_size_mb -= size_mb
        
        self.logger.debug(f"Evicted cached section: {oldest_key}")
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_usage.clear()
        self.cache_size_mb = 0.0


class OptimizedParallaxLayer:
    """Enhanced parallax layer with optimization features"""
    
    def __init__(self, layer: ParallaxLayer):
        self.layer = layer
        self.layer_id = f"layer_{id(layer)}"
        
        # Optimization state
        self.is_visible = True
        self.is_static = False  # True if layer doesn't change
        self.last_render_hash = None
        
        # Culling optimization
        self.tile_size = 512  # Size of tiles for culling
        self.visible_tiles: Set[Tuple[int, int]] = set()
        
        # Performance tracking
        self.render_count = 0
        self.total_render_time = 0.0
        self.last_render_time = 0.0
    
    def calculate_visible_tiles(self, frustum: ViewFrustum) -> Set[Tuple[int, int]]:
        """Calculate which tiles are visible in the frustum"""
        if not self.layer.image:
            return set()
        
        layer_width = self.layer.image.get_width()
        layer_height = self.layer.image.get_height()
        
        # Expand frustum for this layer's scroll speed
        expanded_frustum = ViewFrustum(
            frustum.left / max(self.layer.scroll_speed, 0.001),
            frustum.right / max(self.layer.scroll_speed, 0.001),
            frustum.top / max(self.layer.scroll_speed, 0.001),
            frustum.bottom / max(self.layer.scroll_speed, 0.001)
        )
        
        visible_tiles = set()
        
        # Calculate tile range
        tile_start_x = int(expanded_frustum.left // self.tile_size)
        tile_end_x = int(expanded_frustum.right // self.tile_size) + 1
        tile_start_y = int(expanded_frustum.top // self.tile_size) 
        tile_end_y = int(expanded_frustum.bottom // self.tile_size) + 1
        
        for tile_y in range(tile_start_y, tile_end_y):
            for tile_x in range(tile_start_x, tile_end_x):
                # Check if tile intersects with actual layer bounds
                tile_world_x = tile_x * self.tile_size
                tile_world_y = tile_y * self.tile_size
                
                if expanded_frustum.contains_rect(tile_world_x, tile_world_y, 
                                                self.tile_size, self.tile_size):
                    visible_tiles.add((tile_x, tile_y))
        
        return visible_tiles
    
    def should_render(self, frustum: ViewFrustum) -> bool:
        """Determine if layer should be rendered"""
        if not self.is_visible or not self.layer.image:
            return False
        
        # Update visible tiles
        new_visible_tiles = self.calculate_visible_tiles(frustum)
        
        # If no tiles are visible, skip rendering
        if not new_visible_tiles:
            return False
        
        # Check if visibility changed (for caching optimization)
        tiles_changed = new_visible_tiles != self.visible_tiles
        self.visible_tiles = new_visible_tiles
        
        return True
    
    def get_render_hash(self, frustum: ViewFrustum) -> str:
        """Get hash for render state (for caching)"""
        return f"{self.layer_id}_{self.layer.x_offset:.1f}_{self.layer.y_offset:.1f}_{len(self.visible_tiles)}"


class BatchRenderer:
    """Batch rendering system for similar operations"""
    
    def __init__(self):
        self.batches: Dict[str, RenderBatch] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_to_batch(self, batch_key: str, surface: pygame.Surface, 
                    position: Tuple[int, int], blend_mode: int = pygame.BLEND_ALPHA_SDL2,
                    alpha: int = 255):
        """Add surface to appropriate batch"""
        if batch_key not in self.batches:
            self.batches[batch_key] = RenderBatch(blend_mode=blend_mode, alpha=alpha)
        
        batch = self.batches[batch_key]
        
        # Verify batch compatibility
        if batch.blend_mode == blend_mode and batch.alpha == alpha:
            batch.add(surface, position)
        else:
            # Create new batch with different parameters
            new_key = f"{batch_key}_{blend_mode}_{alpha}"
            if new_key not in self.batches:
                self.batches[new_key] = RenderBatch(blend_mode=blend_mode, alpha=alpha)
            self.batches[new_key].add(surface, position)
    
    def render_batches(self, target_surface: pygame.Surface):
        """Render all batches to target surface"""
        total_operations = 0
        
        for batch_key, batch in self.batches.items():
            if batch.is_empty():
                continue
            
            # Render batch efficiently
            if batch.blend_mode == pygame.BLEND_ALPHA_SDL2 and batch.alpha == 255:
                # Standard blitting - can be optimized further
                for surface, position in zip(batch.surfaces, batch.positions):
                    target_surface.blit(surface, position)
            else:
                # Special blend modes or alpha
                for surface, position in zip(batch.surfaces, batch.positions):
                    if batch.alpha != 255:
                        surface.set_alpha(batch.alpha)
                    target_surface.blit(surface, position, special_flags=batch.blend_mode)
            
            total_operations += len(batch.surfaces)
        
        # Clear batches for next frame
        for batch in self.batches.values():
            batch.clear()
        
        return total_operations


class OptimizedParallaxRenderer:
    """High-performance parallax renderer with advanced optimizations"""
    
    def __init__(self, screen_width: int = 1920, screen_height: int = 1080,
                 technique: RenderTechnique = RenderTechnique.OPTIMIZED):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.technique = technique
        self.logger = logging.getLogger(__name__)
        
        # Rendering components
        self.batch_renderer = BatchRenderer()
        self.layer_cache = LayerCache()
        
        # Camera and view frustum
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.frustum = ViewFrustum(0, screen_width, 0, screen_height)
        
        # Optimization settings
        self.enable_culling = technique in [RenderTechnique.CULLED, RenderTechnique.OPTIMIZED]
        self.enable_batching = technique in [RenderTechnique.BATCHED, RenderTechnique.OPTIMIZED]
        self.enable_caching = technique in [RenderTechnique.CACHED, RenderTechnique.OPTIMIZED]
        
        # Performance tracking
        self.frame_count = 0
        self.total_render_time = 0.0
        self.culled_layers_count = 0
        self.cached_renders_count = 0
        
        # Layer optimization wrappers
        self.optimized_layers: Dict[int, OptimizedParallaxLayer] = {}
        
        self.logger.info(f"Optimized Parallax Renderer initialized with technique: {technique.value}")
    
    def update_camera(self, x: float, y: float):
        """Update camera position and view frustum"""
        self.camera_x = x
        self.camera_y = y
        
        # Update view frustum
        self.frustum = ViewFrustum(
            x, x + self.screen_width,
            y, y + self.screen_height
        )
    
    def register_parallax_system(self, parallax: ParallaxSystem):
        """Register parallax system for optimization"""
        for layer in parallax.layers:
            layer_id = id(layer)
            if layer_id not in self.optimized_layers:
                self.optimized_layers[layer_id] = OptimizedParallaxLayer(layer)
    
    def render_parallax_system(self, surface: pygame.Surface, parallax: ParallaxSystem) -> Dict[str, Any]:
        """Render parallax system with optimizations"""
        start_time = pygame.time.get_ticks()
        
        # Ensure layers are registered
        self.register_parallax_system(parallax)
        
        # Statistics
        rendered_layers = 0
        culled_layers = 0
        cached_renders = 0
        total_operations = 0
        
        # Render each layer with optimizations
        for layer in parallax.layers:
            layer_id = id(layer)
            opt_layer = self.optimized_layers[layer_id]
            
            # Culling check
            if self.enable_culling and not opt_layer.should_render(self.frustum):
                culled_layers += 1
                continue
            
            # Cache check
            cache_key = opt_layer.get_render_hash(self.frustum)
            cached_surface = None
            
            if self.enable_caching:
                cached_surface = self.layer_cache.get_cached_section(cache_key)
                if cached_surface:
                    cached_renders += 1
            
            # Render layer
            if cached_surface:
                # Use cached render
                if self.enable_batching:
                    batch_key = f"cached_{layer.blend_mode}_{layer.alpha}"
                    self.batch_renderer.add_to_batch(batch_key, cached_surface, (0, 0),
                                                   layer.blend_mode, layer.alpha)
                else:
                    surface.blit(cached_surface, (0, 0))
                total_operations += 1
            else:
                # Render fresh
                operations = self._render_layer_optimized(surface, layer, opt_layer)
                total_operations += operations
                
                # Cache the result if beneficial
                if self.enable_caching and not opt_layer.is_static:
                    self._cache_layer_render(cache_key, surface, layer)
            
            rendered_layers += 1
        
        # Render batches if batching is enabled
        if self.enable_batching:
            batch_operations = self.batch_renderer.render_batches(surface)
            total_operations += batch_operations
        
        # Update statistics
        render_time = pygame.time.get_ticks() - start_time
        self.frame_count += 1
        self.total_render_time += render_time
        self.culled_layers_count += culled_layers
        self.cached_renders_count += cached_renders
        
        return {
            "rendered_layers": rendered_layers,
            "culled_layers": culled_layers,
            "cached_renders": cached_renders,
            "total_operations": total_operations,
            "render_time_ms": render_time
        }
    
    def _render_layer_optimized(self, surface: pygame.Surface, layer: ParallaxLayer,
                              opt_layer: OptimizedParallaxLayer) -> int:
        """Render single layer with optimizations"""
        if not layer.image:
            return 0
        
        layer_width = layer.image.get_width()
        layer_height = layer.image.get_height()
        operations = 0
        
        # Calculate render bounds with culling
        if self.enable_culling:
            # Only render tiles that are visible
            for tile_x, tile_y in opt_layer.visible_tiles:
                tile_world_x = tile_x * opt_layer.tile_size
                tile_world_y = tile_y * opt_layer.tile_size
                
                # Calculate screen position for this tile
                screen_x = tile_world_x - (layer.x_offset * layer.scroll_speed)
                screen_y = tile_world_y - (layer.y_offset * layer.scroll_speed)
                
                # Wrap tile coordinates to layer bounds
                tile_layer_x = tile_world_x % layer_width
                tile_layer_y = tile_world_y % layer_height
                
                # Create tile rect
                tile_rect = pygame.Rect(tile_layer_x, tile_layer_y, 
                                      min(opt_layer.tile_size, layer_width - tile_layer_x),
                                      min(opt_layer.tile_size, layer_height - tile_layer_y))
                
                # Extract tile from layer
                if tile_rect.width > 0 and tile_rect.height > 0:
                    tile_surface = layer.image.subsurface(tile_rect)
                    
                    if self.enable_batching:
                        batch_key = f"layer_{opt_layer.layer_id}_{layer.blend_mode}"
                        self.batch_renderer.add_to_batch(batch_key, tile_surface, 
                                                       (int(screen_x), int(screen_y)),
                                                       layer.blend_mode, layer.alpha)
                    else:
                        if layer.blend_mode == pygame.BLEND_ALPHA_SDL2:
                            surface.blit(tile_surface, (int(screen_x), int(screen_y)))
                        else:
                            surface.blit(tile_surface, (int(screen_x), int(screen_y)),
                                       special_flags=layer.blend_mode)
                    
                    operations += 1
        else:
            # Standard tiled rendering (fallback)
            operations = self._render_layer_standard(surface, layer)
        
        return operations
    
    def _render_layer_standard(self, surface: pygame.Surface, layer: ParallaxLayer) -> int:
        """Standard layer rendering (fallback)"""
        if not layer.image:
            return 0
        
        layer_width = layer.image.get_width()
        layer_height = layer.image.get_height()
        operations = 0
        
        # Calculate how many tiles we need
        tiles_x = math.ceil(self.screen_width / layer_width) + 1
        tiles_y = math.ceil(self.screen_height / layer_height) + 1
        
        # Calculate starting positions with wrapping
        start_x = -(layer.x_offset % layer_width)
        start_y = -(layer.y_offset % layer_height)
        
        # Render tiled background
        for y in range(tiles_y):
            for x in range(tiles_x):
                pos_x = start_x + (x * layer_width)
                pos_y = start_y + (y * layer_height)
                
                if self.enable_batching:
                    batch_key = f"standard_{layer.blend_mode}"
                    self.batch_renderer.add_to_batch(batch_key, layer.image, 
                                                   (int(pos_x), int(pos_y)),
                                                   layer.blend_mode, layer.alpha)
                else:
                    if layer.blend_mode == pygame.BLEND_ALPHA_SDL2:
                        surface.blit(layer.image, (pos_x, pos_y))
                    else:
                        surface.blit(layer.image, (pos_x, pos_y), special_flags=layer.blend_mode)
                
                operations += 1
        
        return operations
    
    def _cache_layer_render(self, cache_key: str, surface: pygame.Surface, layer: ParallaxLayer):
        """Cache layer render result"""
        # Create surface copy for caching
        # This is simplified - in practice, you'd cache specific regions
        cache_surface = surface.copy()
        self.layer_cache.cache_section(cache_key, cache_surface)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get detailed performance statistics"""
        avg_render_time = self.total_render_time / max(self.frame_count, 1)
        
        return {
            "technique": self.technique.value,
            "frame_count": self.frame_count,
            "average_render_time_ms": avg_render_time,
            "total_render_time_ms": self.total_render_time,
            "culled_layers_total": self.culled_layers_count,
            "cached_renders_total": self.cached_renders_count,
            "culling_enabled": self.enable_culling,
            "batching_enabled": self.enable_batching,
            "caching_enabled": self.enable_caching,
            "cache_size_mb": self.layer_cache.cache_size_mb,
            "optimized_layers_count": len(self.optimized_layers)
        }
    
    def optimize_for_performance_mode(self, mode: str):
        """Optimize renderer for specific performance mode"""
        if mode == "ultra":
            self.technique = RenderTechnique.OPTIMIZED
            self.enable_culling = True
            self.enable_batching = True
            self.enable_caching = True
        elif mode == "high":
            self.technique = RenderTechnique.CULLED
            self.enable_culling = True
            self.enable_batching = True
            self.enable_caching = False
        elif mode == "medium":
            self.technique = RenderTechnique.BATCHED
            self.enable_culling = True
            self.enable_batching = True
            self.enable_caching = False
        else:  # low
            self.technique = RenderTechnique.BASIC
            self.enable_culling = False
            self.enable_batching = False
            self.enable_caching = False
        
        self.logger.info(f"Renderer optimized for {mode} performance mode")
    
    def clear_cache(self):
        """Clear all cached data"""
        self.layer_cache.clear()
        self.logger.info("Parallax renderer cache cleared")
    
    def shutdown(self):
        """Clean shutdown"""
        self.clear_cache()
        self.optimized_layers.clear()


# Integration functions
def create_optimized_parallax_renderer(screen_width: int, screen_height: int,
                                     performance_mode: str = "high") -> OptimizedParallaxRenderer:
    """Create optimized parallax renderer for given performance mode"""
    technique_map = {
        "ultra": RenderTechnique.OPTIMIZED,
        "high": RenderTechnique.CULLED,
        "medium": RenderTechnique.BATCHED,
        "low": RenderTechnique.BASIC
    }
    
    technique = technique_map.get(performance_mode, RenderTechnique.OPTIMIZED)
    return OptimizedParallaxRenderer(screen_width, screen_height, technique)


def benchmark_parallax_performance(parallax: ParallaxSystem, frames: int = 300) -> Dict[str, Any]:
    """Benchmark parallax rendering performance"""
    import time
    
    # Test different techniques
    techniques = [RenderTechnique.BASIC, RenderTechnique.BATCHED, 
                 RenderTechnique.CULLED, RenderTechnique.OPTIMIZED]
    
    results = {}
    
    for technique in techniques:
        renderer = OptimizedParallaxRenderer(1920, 1080, technique)
        renderer.register_parallax_system(parallax)
        
        # Create test surface
        test_surface = pygame.Surface((1920, 1080))
        
        # Benchmark rendering
        start_time = time.time()
        for frame in range(frames):
            # Simulate camera movement
            renderer.update_camera(frame * 2, 0)
            renderer.render_parallax_system(test_surface, parallax)
        
        end_time = time.time()
        
        total_time = end_time - start_time
        fps = frames / total_time
        
        results[technique.value] = {
            "total_time_s": total_time,
            "fps": fps,
            "avg_frame_time_ms": (total_time / frames) * 1000,
            "stats": renderer.get_performance_stats()
        }
        
        renderer.shutdown()
    
    return results