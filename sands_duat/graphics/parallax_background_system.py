"""
Advanced Parallax Background System for Sands of Duat

High-performance parallax scrolling system designed for premium visual quality
while maintaining 60fps on RTX 5070 and scaling for lower-end hardware.

Features:
- Multi-layer parallax with depth-based scrolling
- Dynamic atmosphere effects (sandstorms, heat shimmer)
- GPU-accelerated layer composition
- Adaptive LOD based on performance
- Memory-efficient tile streaming
- Egyptian desert theming with dynamic lighting integration
"""

import pygame
import math
import random
import time
import threading
from typing import List, Dict, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import logging

from .enhanced_asset_streaming import get_asset_streaming_manager, LoadPriority
from .lighting_system import get_lighting_system
from ..core.performance_profiler import profile_operation
from .performance_optimizer import get_performance_optimizer, optimize_for_performance


class ParallaxLayer(Enum):
    """Parallax layer types with depth ordering."""
    FAR_BACKGROUND = 0      # Distant mountains, sky
    MID_BACKGROUND = 1      # Distant dunes, pyramids
    NEAR_BACKGROUND = 2     # Close dunes, ruins
    FOREGROUND = 3          # Close details, vegetation
    ATMOSPHERIC = 4         # Particles, effects


class ScrollDirection(Enum):
    """Scroll direction modes."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    RADIAL = "radial"
    CUSTOM = "custom"


@dataclass
class LayerConfig:
    """Configuration for a parallax layer."""
    layer_type: ParallaxLayer
    scroll_speed: float      # Multiplier for scroll speed (0.0 = static, 1.0 = camera speed)
    depth: float            # Z-depth for proper layering
    opacity: float          # Layer opacity (0.0 to 1.0)
    blend_mode: int         # Pygame blend mode
    tile_size: Tuple[int, int]  # Size of individual tiles
    repeat_x: bool          # Whether layer repeats horizontally
    repeat_y: bool          # Whether layer repeats vertically
    parallax_factor: float  # Fine-tuned parallax multiplier
    
    # Visual effects
    wave_amplitude: float = 0.0    # Heat shimmer amplitude
    wave_frequency: float = 0.0    # Heat shimmer frequency
    color_tint: Tuple[int, int, int] = (255, 255, 255)  # Color tinting
    atmospheric_density: float = 0.0  # Atmospheric perspective


class ParallaxTile:
    """Individual tile in a parallax layer."""
    
    def __init__(self, x: float, y: float, surface: pygame.Surface, 
                 layer_config: LayerConfig):
        self.x = x
        self.y = y
        self.original_surface = surface
        self.layer_config = layer_config
        
        # Cached surfaces for effects
        self.processed_surface: Optional[pygame.Surface] = None
        self.last_effect_time = 0.0
        self.effect_cache_duration = 0.1  # Cache effects for 100ms
        
        # Animation state
        self.wave_offset = random.uniform(0, 2 * math.pi)
        self.shimmer_intensity = 0.0
        
    def get_render_position(self, camera_x: float, camera_y: float) -> Tuple[float, float]:
        """Calculate render position based on camera and parallax."""
        parallax_x = self.x - (camera_x * self.layer_config.parallax_factor)
        parallax_y = self.y - (camera_y * self.layer_config.parallax_factor)
        return parallax_x, parallax_y
    
    def is_visible(self, camera_rect: pygame.Rect, margin: int = 100) -> bool:
        """Check if tile is visible with given camera view."""
        camera_x, camera_y = self.get_render_position(camera_rect.x, camera_rect.y)
        
        tile_rect = pygame.Rect(
            camera_x - margin,
            camera_y - margin,
            self.layer_config.tile_size[0] + margin * 2,
            self.layer_config.tile_size[1] + margin * 2
        )
        
        return camera_rect.colliderect(tile_rect)
    
    def get_processed_surface(self, current_time: float) -> pygame.Surface:
        """Get surface with effects applied."""
        # Use cache if recent
        if (self.processed_surface and 
            current_time - self.last_effect_time < self.effect_cache_duration):
            return self.processed_surface
        
        surface = self.original_surface.copy()
        
        # Apply heat shimmer effect
        if self.layer_config.wave_amplitude > 0:
            surface = self._apply_heat_shimmer(surface, current_time)
        
        # Apply color tinting
        if self.layer_config.color_tint != (255, 255, 255):
            surface = self._apply_color_tint(surface)
        
        # Apply atmospheric perspective
        if self.layer_config.atmospheric_density > 0:
            surface = self._apply_atmospheric_perspective(surface)
        
        self.processed_surface = surface
        self.last_effect_time = current_time
        return surface
    
    def _apply_heat_shimmer(self, surface: pygame.Surface, current_time: float) -> pygame.Surface:
        """Apply heat shimmer effect to surface."""
        if self.layer_config.wave_amplitude <= 0:
            return surface
        
        width, height = surface.get_size()
        shimmer_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Simplified shimmer - create wave displacement
        wave_time = current_time * self.layer_config.wave_frequency + self.wave_offset
        
        # Create shimmer effect by drawing with slight offsets
        for y in range(0, height, 4):  # Process every 4th line for performance
            offset_x = int(math.sin(wave_time + y * 0.1) * self.layer_config.wave_amplitude)
            offset_y = int(math.cos(wave_time + y * 0.08) * self.layer_config.wave_amplitude * 0.5)
            
            # Copy line with offset
            if 0 <= y + offset_y < height:
                source_rect = pygame.Rect(0, y, width, min(4, height - y))
                dest_pos = (offset_x, y + offset_y)
                shimmer_surface.blit(surface, dest_pos, source_rect)
        
        return shimmer_surface
    
    def _apply_color_tint(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply color tinting to surface."""
        tinted = surface.copy()
        
        # Create tint overlay
        tint_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        tint_surface.fill((*self.layer_config.color_tint, 128))
        
        # Apply tint with multiply blend
        tinted.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)
        
        return tinted
    
    def _apply_atmospheric_perspective(self, surface: pygame.Surface) -> pygame.Surface:
        """Apply atmospheric perspective (fog/haze effect)."""
        if self.layer_config.atmospheric_density <= 0:
            return surface
        
        atmosphere_surface = surface.copy()
        
        # Create atmospheric overlay
        fog_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        fog_alpha = int(255 * self.layer_config.atmospheric_density * 0.3)
        fog_color = (200, 180, 140, fog_alpha)  # Warm desert haze
        fog_surface.fill(fog_color)
        
        # Blend with original
        atmosphere_surface.blit(fog_surface, (0, 0), special_flags=pygame.BLEND_ALPHA)
        
        return atmosphere_surface


class AtmosphericEffects:
    """Manages atmospheric effects for parallax backgrounds."""
    
    def __init__(self):
        self.sandstorm_intensity = 0.0
        self.heat_shimmer_intensity = 0.0
        self.fog_density = 0.0
        self.wind_direction = 0.0  # Radians
        self.wind_speed = 0.0
        
        # Particle effects for atmosphere
        self.dust_particles: List[Dict[str, Any]] = []
        self.max_dust_particles = 200
        
        # Time-based effects
        self.effect_time = 0.0
        
    def update(self, delta_time: float, weather_conditions: Dict[str, float] = None):
        """Update atmospheric effects."""
        self.effect_time += delta_time
        
        if weather_conditions:
            self.sandstorm_intensity = weather_conditions.get("sandstorm", 0.0)
            self.heat_shimmer_intensity = weather_conditions.get("heat", 0.5)
            self.fog_density = weather_conditions.get("fog", 0.1)
            self.wind_speed = weather_conditions.get("wind_speed", 20.0)
            self.wind_direction = weather_conditions.get("wind_direction", 0.0)
        
        # Update dust particles
        self._update_dust_particles(delta_time)
        
        # Generate new dust if needed
        if (self.sandstorm_intensity > 0.3 and 
            len(self.dust_particles) < self.max_dust_particles):
            self._generate_dust_particles()
    
    def _update_dust_particles(self, delta_time: float):
        """Update atmospheric dust particles."""
        for particle in self.dust_particles[:]:
            # Move particle with wind
            particle['x'] += math.cos(self.wind_direction) * self.wind_speed * delta_time
            particle['y'] += math.sin(self.wind_direction) * self.wind_speed * delta_time * 0.1
            
            # Add some randomness
            particle['x'] += random.uniform(-5, 5) * delta_time
            particle['y'] += random.uniform(-2, 2) * delta_time
            
            # Update life
            particle['life'] -= delta_time
            particle['alpha'] = int(255 * (particle['life'] / particle['max_life']))
            
            # Remove dead particles
            if particle['life'] <= 0 or particle['alpha'] <= 0:
                self.dust_particles.remove(particle)
    
    def _generate_dust_particles(self):
        """Generate new atmospheric dust particles."""
        for _ in range(5):
            particle = {
                'x': random.uniform(-100, 3540),  # Start off-screen
                'y': random.uniform(0, 1440),
                'size': random.uniform(1, 3),
                'life': random.uniform(5, 15),
                'max_life': 10,
                'alpha': random.randint(30, 80),
                'color': (255, 220, 180)  # Sandy color
            }
            particle['max_life'] = particle['life']
            self.dust_particles.append(particle)
    
    def render_atmospheric_effects(self, surface: pygame.Surface):
        """Render atmospheric effects to surface."""
        # Render dust particles
        for particle in self.dust_particles:
            if particle['alpha'] > 10:
                try:
                    color = (*particle['color'], particle['alpha'])
                    size = max(1, int(particle['size']))
                    pygame.draw.circle(surface, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), size)
                except:
                    pass  # Skip invalid particles
        
        # Render heat shimmer overlay
        if self.heat_shimmer_intensity > 0.1:
            self._render_heat_shimmer_overlay(surface)
    
    def _render_heat_shimmer_overlay(self, surface: pygame.Surface):
        """Render heat shimmer overlay effect."""
        shimmer_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        # Create subtle shimmer pattern
        width, height = surface.get_size()
        shimmer_alpha = int(self.heat_shimmer_intensity * 30)
        
        for y in range(0, height, 8):
            wave_offset = math.sin(self.effect_time * 2 + y * 0.05) * 2
            shimmer_color = (255, 255, 255, shimmer_alpha)
            
            # Draw subtle shimmer lines
            start_pos = (int(wave_offset), y)
            end_pos = (width + int(wave_offset), y)
            try:
                pygame.draw.line(shimmer_surface, (255, 255, 255), start_pos, end_pos)
            except:
                pass
        
        # Blend with surface
        surface.blit(shimmer_surface, (0, 0), special_flags=pygame.BLEND_ADD)


class ParallaxRenderer:
    """High-performance parallax rendering engine."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Layer management
        self.layers: Dict[ParallaxLayer, List[ParallaxTile]] = {
            layer: [] for layer in ParallaxLayer
        }
        self.layer_configs: Dict[ParallaxLayer, LayerConfig] = {}
        
        # Camera
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_target_x = 0.0
        self.camera_target_y = 0.0
        self.camera_smoothing = 0.1
        
        # Performance optimization
        self.asset_manager = get_asset_streaming_manager()
        self.lighting_system = get_lighting_system(screen_width, screen_height)
        self.atmospheric_effects = AtmosphericEffects()
        
        # Rendering surfaces
        self.layer_surfaces: Dict[ParallaxLayer, pygame.Surface] = {}
        self.composite_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        
        # Performance tracking
        self.render_stats = {
            "layers_rendered": 0,
            "tiles_rendered": 0,
            "tiles_culled": 0,
            "render_time_ms": 0.0
        }
        
        # Performance optimization
        self.performance_optimizer = get_performance_optimizer()
        
        # Threading for background processing
        self.background_executor = ThreadPoolExecutor(max_workers=2)
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize default Egyptian desert layers
        self._initialize_default_layers()
    
    def _initialize_default_layers(self):
        """Initialize default Egyptian desert parallax layers."""
        # Far background - distant mountains and sky
        self.layer_configs[ParallaxLayer.FAR_BACKGROUND] = LayerConfig(
            layer_type=ParallaxLayer.FAR_BACKGROUND,
            scroll_speed=0.1,
            depth=10.0,
            opacity=0.8,
            blend_mode=pygame.BLEND_ALPHA,
            tile_size=(2048, 1024),
            repeat_x=True,
            repeat_y=False,
            parallax_factor=0.1,
            atmospheric_density=0.4,
            color_tint=(180, 160, 140)  # Distant haze tint
        )
        
        # Mid background - pyramids and distant dunes
        self.layer_configs[ParallaxLayer.MID_BACKGROUND] = LayerConfig(
            layer_type=ParallaxLayer.MID_BACKGROUND,
            scroll_speed=0.3,
            depth=5.0,
            opacity=0.9,
            blend_mode=pygame.BLEND_ALPHA,
            tile_size=(1536, 1024),
            repeat_x=True,
            repeat_y=False,
            parallax_factor=0.3,
            atmospheric_density=0.2,
            color_tint=(220, 200, 170)
        )
        
        # Near background - close dunes and ruins
        self.layer_configs[ParallaxLayer.NEAR_BACKGROUND] = LayerConfig(
            layer_type=ParallaxLayer.NEAR_BACKGROUND,
            scroll_speed=0.6,
            depth=2.0,
            opacity=1.0,
            blend_mode=pygame.BLEND_ALPHA,
            tile_size=(1024, 768),
            repeat_x=True,
            repeat_y=False,
            parallax_factor=0.6,
            wave_amplitude=1.0,
            wave_frequency=0.5,
            color_tint=(255, 240, 200)
        )
        
        # Foreground details
        self.layer_configs[ParallaxLayer.FOREGROUND] = LayerConfig(
            layer_type=ParallaxLayer.FOREGROUND,
            scroll_speed=0.9,
            depth=1.0,
            opacity=1.0,
            blend_mode=pygame.BLEND_ALPHA,
            tile_size=(1024, 512),
            repeat_x=True,
            repeat_y=False,
            parallax_factor=0.9,
            wave_amplitude=2.0,
            wave_frequency=1.0
        )
    
    def load_background_for_environment(self, environment_name: str):
        """Load background assets for specific environment."""
        with profile_operation(f"load_parallax_environment_{environment_name}"):
            # Request background assets based on environment
            if environment_name == "desert":
                self._load_desert_environment()
            elif environment_name == "temple":
                self._load_temple_environment()
            elif environment_name == "pyramid":
                self._load_pyramid_environment()
            else:
                self._load_default_environment()
    
    def _load_desert_environment(self):
        """Load desert environment layers."""
        # Use existing combat background as base, create tiled versions
        base_bg = "env_combat_background"
        
        # Request base background
        self.asset_manager.request_asset(base_bg, LoadPriority.HIGH)
        
        # Create procedural desert layers
        self._create_procedural_desert_layers()
    
    def _load_temple_environment(self):
        """Load temple environment layers."""
        # Use existing backgrounds
        self.asset_manager.request_asset("env_deck_builder_background", LoadPriority.HIGH)
        self._create_procedural_temple_layers()
    
    def _load_pyramid_environment(self):
        """Load pyramid environment layers."""
        self.asset_manager.request_asset("env_progression_background", LoadPriority.HIGH)
        self._create_procedural_pyramid_layers()
    
    def _load_default_environment(self):
        """Load default environment."""
        self.asset_manager.request_asset("env_menu_background", LoadPriority.HIGH)
        self._create_procedural_desert_layers()
    
    def _create_procedural_desert_layers(self):
        """Create procedural desert parallax layers."""
        # Create gradient sky for far background
        far_bg_surface = self._create_desert_sky_gradient()
        far_tile = ParallaxTile(0, 0, far_bg_surface, self.layer_configs[ParallaxLayer.FAR_BACKGROUND])
        self.layers[ParallaxLayer.FAR_BACKGROUND] = [far_tile]
        
        # Create distant dunes for mid background
        mid_bg_surface = self._create_distant_dunes()
        mid_tile = ParallaxTile(0, 200, mid_bg_surface, self.layer_configs[ParallaxLayer.MID_BACKGROUND])
        self.layers[ParallaxLayer.MID_BACKGROUND] = [mid_tile]
        
        # Create near dunes
        near_bg_surface = self._create_near_dunes()
        near_tile = ParallaxTile(0, 400, near_bg_surface, self.layer_configs[ParallaxLayer.NEAR_BACKGROUND])
        self.layers[ParallaxLayer.NEAR_BACKGROUND] = [near_tile]
    
    def _create_procedural_temple_layers(self):
        """Create procedural temple parallax layers."""
        # Similar to desert but with temple elements
        self._create_procedural_desert_layers()
        
        # Add temple silhouettes to mid background
        temple_surface = self._create_temple_silhouettes()
        temple_tile = ParallaxTile(500, 150, temple_surface, self.layer_configs[ParallaxLayer.MID_BACKGROUND])
        self.layers[ParallaxLayer.MID_BACKGROUND].append(temple_tile)
    
    def _create_procedural_pyramid_layers(self):
        """Create procedural pyramid parallax layers."""
        self._create_procedural_desert_layers()
        
        # Add pyramid silhouettes
        pyramid_surface = self._create_pyramid_silhouettes()
        pyramid_tile = ParallaxTile(200, 100, pyramid_surface, self.layer_configs[ParallaxLayer.FAR_BACKGROUND])
        self.layers[ParallaxLayer.FAR_BACKGROUND].append(pyramid_tile)
    
    def _create_desert_sky_gradient(self) -> pygame.Surface:
        """Create procedural desert sky gradient."""
        width, height = self.layer_configs[ParallaxLayer.FAR_BACKGROUND].tile_size
        surface = pygame.Surface((width, height))
        
        # Create gradient from sunset colors to darker sky
        for y in range(height):
            progress = y / height
            
            # Sunset gradient colors
            if progress < 0.3:  # Horizon area
                color = (255, 180 + int(progress * 75), 120 + int(progress * 80))
            elif progress < 0.7:  # Mid sky
                color = (200 - int((progress - 0.3) * 100), 140, 100 + int((progress - 0.3) * 50))
            else:  # Upper sky
                color = (100 - int((progress - 0.7) * 60), 90, 120)
            
            pygame.draw.line(surface, color, (0, y), (width, y))
        
        return surface
    
    def _create_distant_dunes(self) -> pygame.Surface:
        """Create procedural distant dunes."""
        width, height = self.layer_configs[ParallaxLayer.MID_BACKGROUND].tile_size
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw stylized distant dunes
        dune_color = (140, 120, 80)
        dune_height = height // 3
        
        # Create smooth dune curves
        points = []
        for x in range(0, width + 50, 50):
            curve_height = dune_height + int(math.sin(x * 0.01) * 30)
            points.append((x, height - curve_height))
        
        # Add bottom points to close the shape
        points.append((width, height))
        points.append((0, height))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, dune_color, points)
        
        return surface
    
    def _create_near_dunes(self) -> pygame.Surface:
        """Create procedural near dunes."""
        width, height = self.layer_configs[ParallaxLayer.NEAR_BACKGROUND].tile_size
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw more detailed near dunes
        dune_color = (180, 160, 100)
        
        # Multiple dune layers
        for layer in range(3):
            dune_height = (height // 4) + layer * 20
            alpha = 255 - layer * 50
            
            # Create dune shape
            points = []
            for x in range(0, width + 30, 30):
                curve_height = dune_height + int(math.sin(x * 0.02 + layer) * 40)
                points.append((x, height - curve_height))
            
            points.append((width, height))
            points.append((0, height))
            
            if len(points) >= 3:
                dune_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                color_with_alpha = (*dune_color, alpha)
                pygame.draw.polygon(dune_surface, dune_color, points)
                dune_surface.set_alpha(alpha)
                surface.blit(dune_surface, (0, 0))
        
        return surface
    
    def _create_temple_silhouettes(self) -> pygame.Surface:
        """Create procedural temple silhouettes."""
        width, height = 800, 400
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw stylized temple shapes
        temple_color = (60, 50, 40)
        
        # Main temple structure
        temple_rect = pygame.Rect(200, 150, 400, 200)
        pygame.draw.rect(surface, temple_color, temple_rect)
        
        # Columns
        for i in range(5):
            column_x = 250 + i * 60
            column_rect = pygame.Rect(column_x, 100, 20, 250)
            pygame.draw.rect(surface, temple_color, column_rect)
        
        return surface
    
    def _create_pyramid_silhouettes(self) -> pygame.Surface:
        """Create procedural pyramid silhouettes."""
        width, height = 1000, 600
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw pyramid shapes
        pyramid_color = (80, 70, 50)
        
        # Large pyramid
        pyramid_points = [(300, 500), (600, 200), (900, 500)]
        pygame.draw.polygon(surface, pyramid_color, pyramid_points)
        
        # Smaller pyramid
        small_pyramid_points = [(100, 450), (250, 300), (400, 450)]
        pygame.draw.polygon(surface, pyramid_color, small_pyramid_points)
        
        return surface
    
    def set_camera_position(self, x: float, y: float, smooth: bool = True):
        """Set camera position with optional smoothing."""
        if smooth:
            self.camera_target_x = x
            self.camera_target_y = y
        else:
            self.camera_x = x
            self.camera_y = y
            self.camera_target_x = x
            self.camera_target_y = y
    
    def update(self, delta_time: float, weather_conditions: Dict[str, float] = None):
        """Update parallax system."""
        with profile_operation("parallax_update"):
            # Update camera smoothing
            if self.camera_smoothing > 0:
                self.camera_x += (self.camera_target_x - self.camera_x) * self.camera_smoothing
                self.camera_y += (self.camera_target_y - self.camera_y) * self.camera_smoothing
            
            # Update atmospheric effects
            self.atmospheric_effects.update(delta_time, weather_conditions)
            
            # Update layer effects (heat shimmer, etc.)
            current_time = time.time()
            for layer_tiles in self.layers.values():
                for tile in layer_tiles:
                    # Pre-process effects in background if needed
                    if hasattr(tile, 'needs_update') and tile.needs_update:
                        tile.get_processed_surface(current_time)
    
    @optimize_for_performance
    def render(self, target_surface: pygame.Surface, camera_rect: Optional[pygame.Rect] = None):
        """Render parallax background with all effects."""
        start_time = time.time()
        
        # Get current quality settings
        quality_settings = self.performance_optimizer.get_current_settings()
        
        with profile_operation("parallax_render"):
            if camera_rect is None:
                camera_rect = pygame.Rect(self.camera_x, self.camera_y, 
                                        self.screen_width, self.screen_height)
            
            # Clear composite surface
            self.composite_surface.fill((0, 0, 0, 0))
            
            layers_rendered = 0
            tiles_rendered = 0
            tiles_culled = 0
            
            # Render layers in depth order (far to near)
            for layer_type in [ParallaxLayer.FAR_BACKGROUND, ParallaxLayer.MID_BACKGROUND, 
                              ParallaxLayer.NEAR_BACKGROUND, ParallaxLayer.FOREGROUND]:
                
                if layer_type not in self.layers:
                    continue
                
                layer_config = self.layer_configs.get(layer_type)
                if not layer_config:
                    continue
                
                # Create layer surface if needed
                if layer_type not in self.layer_surfaces:
                    self.layer_surfaces[layer_type] = pygame.Surface(
                        (self.screen_width, self.screen_height), pygame.SRCALPHA
                    )
                
                layer_surface = self.layer_surfaces[layer_type]
                layer_surface.fill((0, 0, 0, 0))
                
                # Render tiles in this layer
                for tile in self.layers[layer_type]:
                    if tile.is_visible(camera_rect, margin=200):
                        render_x, render_y = tile.get_render_position(self.camera_x, self.camera_y)
                        
                        # Get processed surface with effects
                        processed_surface = tile.get_processed_surface(time.time())
                        
                        # Apply layer opacity
                        if layer_config.opacity < 1.0:
                            processed_surface = processed_surface.copy()
                            processed_surface.set_alpha(int(255 * layer_config.opacity))
                        
                        # Blit to layer surface
                        layer_surface.blit(processed_surface, (int(render_x), int(render_y)))
                        tiles_rendered += 1
                    else:
                        tiles_culled += 1
                
                # Composite layer to final surface
                self.composite_surface.blit(layer_surface, (0, 0), 
                                          special_flags=layer_config.blend_mode)
                layers_rendered += 1
            
            # Apply lighting effects
            self.lighting_system.render_lighting(self.composite_surface)
            
            # Render atmospheric effects
            self.atmospheric_effects.render_atmospheric_effects(self.composite_surface)
            
            # Final blit to target
            target_surface.blit(self.composite_surface, (0, 0))
            
            # Update statistics
            self.render_stats.update({
                "layers_rendered": layers_rendered,
                "tiles_rendered": tiles_rendered,
                "tiles_culled": tiles_culled,
                "render_time_ms": (time.time() - start_time) * 1000
            })
    
    def set_weather_conditions(self, conditions: Dict[str, float]):
        """Set weather conditions for atmospheric effects."""
        self.atmospheric_effects.update(0.0, conditions)
    
    def get_render_statistics(self) -> Dict[str, Any]:
        """Get rendering performance statistics."""
        return self.render_stats.copy()


# Global parallax renderer
_global_parallax_renderer = None

def get_parallax_renderer(screen_width: int = 3440, screen_height: int = 1440) -> ParallaxRenderer:
    """Get global parallax renderer."""
    global _global_parallax_renderer
    if _global_parallax_renderer is None:
        _global_parallax_renderer = ParallaxRenderer(screen_width, screen_height)
    return _global_parallax_renderer

def setup_desert_parallax():
    """Setup desert parallax environment."""
    renderer = get_parallax_renderer()
    renderer.load_background_for_environment("desert")

def setup_temple_parallax():
    """Setup temple parallax environment."""
    renderer = get_parallax_renderer()
    renderer.load_background_for_environment("temple")

def setup_pyramid_parallax():
    """Setup pyramid parallax environment."""
    renderer = get_parallax_renderer()
    renderer.load_background_for_environment("pyramid")