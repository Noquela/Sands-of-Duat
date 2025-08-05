#!/usr/bin/env python3
"""
Premium Asset Integration System for Sands of Duat

Complete high-performance asset integration system that delivers premium visual
quality while maintaining smooth 60fps performance through intelligent optimization.
"""

import pygame
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

# Import all performance systems
from .high_performance_asset_system import (
    HighPerformanceAssetSystem, PerformanceMode, get_hp_asset_system, initialize_hp_asset_system
)
from .optimized_parallax_renderer import (
    OptimizedParallaxRenderer, RenderTechnique, create_optimized_parallax_renderer
)
from .adaptive_performance_manager import (
    AdaptivePerformanceManager, QualityPreset, QualitySettings, get_performance_manager, initialize_performance_system
)
from .advanced_memory_system import (
    AdvancedMemoryManager, MemoryPriority, MemoryTier, get_memory_manager, initialize_memory_system
)
from .parallax_system import ParallaxSystem
from .asset_manager import AssetType, LoadingPriority


class IntegrationMode(Enum):
    """Integration system operating modes"""
    PERFORMANCE = "performance"    # Maximum performance, minimum quality
    BALANCED = "balanced"         # Balance performance and quality
    QUALITY = "quality"          # Maximum quality, performance secondary
    ADAPTIVE = "adaptive"        # Automatically adjust based on hardware


@dataclass
class SystemConfiguration:
    """Configuration for the integrated system"""
    # Performance targets
    target_fps: float = 60.0
    min_acceptable_fps: float = 30.0
    max_memory_mb: float = 1024.0
    
    # Quality settings
    default_quality: QualityPreset = QualityPreset.HIGH
    adaptive_quality: bool = True
    user_quality_lock: bool = False
    
    # Rendering
    parallax_technique: RenderTechnique = RenderTechnique.OPTIMIZED
    enable_texture_compression: bool = True
    enable_asset_streaming: bool = True
    
    # Memory management
    enable_aggressive_gc: bool = False
    memory_pressure_threshold: float = 0.8
    
    # Integration
    integration_mode: IntegrationMode = IntegrationMode.ADAPTIVE
    performance_monitoring: bool = True
    debug_mode: bool = False


class PremiumAssetIntegrator:
    """Main integration system for premium assets"""
    
    def __init__(self, config: Optional[SystemConfiguration] = None):
        self.config = config or SystemConfiguration()
        self.logger = logging.getLogger(__name__)
        
        # System components
        self.hp_system: Optional[HighPerformanceAssetSystem] = None
        self.performance_manager: Optional[AdaptivePerformanceManager] = None
        self.memory_manager: Optional[AdvancedMemoryManager] = None
        
        # Rendering components
        self.parallax_renderers: Dict[str, OptimizedParallaxRenderer] = {}
        self.active_screen: Optional[str] = None
        
        # State
        self.initialized = False
        self.current_quality: QualityPreset = self.config.default_quality
        
        # Performance tracking
        self.frame_count = 0
        self.initialization_time = 0.0
        
        # Callbacks
        self.quality_change_callbacks: List[Callable[[QualitySettings], None]] = []
        self.performance_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        self.logger.info("Premium Asset Integrator created")
    
    def initialize(self, screen_width: int = 1920, screen_height: int = 1080) -> bool:
        """Initialize the complete integration system"""
        if self.initialized:
            self.logger.warning("System already initialized")
            return True
        
        start_time = time.time()
        self.logger.info("Initializing Premium Asset Integration System")
        
        try:
            # Initialize core systems
            self._initialize_core_systems()
            
            # Initialize rendering systems
            self._initialize_rendering_systems(screen_width, screen_height)
            
            # Configure integration
            self._configure_integration()
            
            # Setup monitoring
            self._setup_monitoring()
            
            self.initialized = True
            self.initialization_time = time.time() - start_time
            
            self.logger.info(f"System initialized successfully in {self.initialization_time:.2f}s")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            return False
    
    def _initialize_core_systems(self):
        """Initialize core performance systems"""
        # High-performance asset system
        self.hp_system = initialize_hp_asset_system(
            max_memory_mb=self.config.max_memory_mb,
            target_fps=self.config.target_fps
        )
        
        # Performance manager
        self.performance_manager = initialize_performance_system(
            target_fps=self.config.target_fps,
            auto_detect=(self.config.integration_mode == IntegrationMode.ADAPTIVE)
        )
        
        # Memory manager
        from .advanced_memory_system import GCStrategy
        gc_strategy = GCStrategy.AGGRESSIVE if self.config.enable_aggressive_gc else GCStrategy.BALANCED
        self.memory_manager = initialize_memory_system(
            max_memory_mb=self.config.max_memory_mb,
            gc_strategy=gc_strategy
        )
        
        self.logger.info("Core systems initialized")
    
    def _initialize_rendering_systems(self, screen_width: int, screen_height: int):
        """Initialize rendering systems"""
        # Create parallax renderers for different screens
        screen_configs = {
            "menu": ("high", ["menu_background"]),
            "combat": ("optimized", ["combat_background", "desert_atmosphere"]),
            "deck_builder": ("optimized", ["library_background", "mystical_elements"]),
            "map": ("medium", ["map_background"])
        }
        
        for screen_name, (performance_mode, asset_tags) in screen_configs.items():
            renderer = create_optimized_parallax_renderer(
                screen_width, screen_height, performance_mode
            )
            self.parallax_renderers[screen_name] = renderer
        
        self.logger.info(f"Rendering systems initialized for {len(screen_configs)} screens")
    
    def _configure_integration(self):
        """Configure system integration"""
        # Connect performance manager to asset system
        self.performance_manager.add_quality_callback(self._on_quality_changed)
        
        # Connect memory pressure to asset cleanup
        self.memory_manager.pressure_detector.add_pressure_callback(self._on_memory_pressure)
        
        # Set initial quality
        if not self.config.adaptive_quality:
            self.performance_manager.set_quality_preset(
                self.config.default_quality, 
                lock=self.config.user_quality_lock
            )
        
        self.logger.info("System integration configured")
    
    def _setup_monitoring(self):
        """Setup performance monitoring"""
        if self.config.performance_monitoring:
            # Add performance callbacks
            self.performance_manager.add_fps_callback(self._on_fps_update)
            
            # Start monitoring
            self.memory_manager.start_monitoring()
    
    def _on_quality_changed(self, new_settings: QualitySettings):
        """Handle quality setting changes"""
        self.logger.info(f"Quality settings changed")
        
        # Update asset system compression
        if hasattr(self.hp_system, 'texture_compressor'):
            # Convert quality settings to performance mode
            if new_settings.render_scale >= 1.0:
                mode = PerformanceMode.ULTRA
            elif new_settings.render_scale >= 0.9:
                mode = PerformanceMode.HIGH
            elif new_settings.render_scale >= 0.75:
                mode = PerformanceMode.MEDIUM
            else:
                mode = PerformanceMode.LOW
            
            self.hp_system.set_quality_mode(mode)
        
        # Update parallax renderers
        for renderer in self.parallax_renderers.values():
            if new_settings.culling_enabled:
                renderer.enable_culling = True
            if new_settings.batching_enabled:
                renderer.enable_batching = True
            if new_settings.caching_enabled:
                renderer.enable_caching = True
        
        # Notify callbacks
        for callback in self.quality_change_callbacks:
            try:
                callback(new_settings)
            except Exception as e:
                self.logger.error(f"Error in quality change callback: {e}")
    
    def _on_memory_pressure(self, pressure: float):
        """Handle memory pressure changes"""
        if pressure > self.config.memory_pressure_threshold:
            self.logger.warning(f"High memory pressure: {pressure:.2f}")
            
            # Force asset cleanup
            if self.hp_system:
                self.hp_system.force_memory_optimization()
            
            # Clear render caches
            for renderer in self.parallax_renderers.values():
                renderer.clear_cache()
    
    def _on_fps_update(self, fps: float):
        """Handle FPS updates"""
        if self.config.debug_mode:
            self.logger.debug(f"FPS: {fps:.1f}")
        
        # Notify performance callbacks
        performance_data = {
            'fps': fps,
            'target_fps': self.config.target_fps,
            'frame_count': self.frame_count
        }
        
        for callback in self.performance_callbacks:
            try:
                callback(performance_data)
            except Exception as e:
                self.logger.error(f"Error in performance callback: {e}")
    
    def switch_screen(self, screen_name: str, assets_path: str = "game_assets"):
        """Switch to a different screen with optimized asset loading"""
        if not self.initialized:
            self.logger.error("System not initialized")
            return False
        
        start_time = time.time()
        self.logger.info(f"Switching to screen: {screen_name}")
        
        # Preload assets for new screen
        self.hp_system.preload_for_screen_transition(screen_name)
        
        # Setup parallax system for screen
        if screen_name in self.parallax_renderers:
            parallax = self.hp_system.setup_parallax_for_screen(screen_name, assets_path)
            renderer = self.parallax_renderers[screen_name]
            renderer.register_parallax_system(parallax)
        
        # Cleanup assets from previous screen if memory pressure exists
        if (self.active_screen and 
            self.memory_manager.pressure_detector.current_pressure > 0.5):
            self._cleanup_screen_assets(self.active_screen)
        
        self.active_screen = screen_name
        transition_time = time.time() - start_time
        
        self.logger.info(f"Screen transition completed in {transition_time:.2f}s")
        return True
    
    def _cleanup_screen_assets(self, screen_name: str):
        """Cleanup assets for a specific screen"""
        # Clear renderer cache
        if screen_name in self.parallax_renderers:
            self.parallax_renderers[screen_name].clear_cache()
        
        # Force memory cleanup
        self.memory_manager.cleanup_memory()
    
    def render_frame(self, surface: pygame.Surface, dt: float) -> Dict[str, Any]:
        """Render a complete frame with all optimizations"""
        if not self.initialized:
            return {'error': 'System not initialized'}
        
        frame_start = time.perf_counter()
        
        # Update systems
        self.hp_system.update(dt)
        self.performance_manager.update(dt)
        
        # Render current screen
        render_stats = {}
        if self.active_screen and self.active_screen in self.parallax_renderers:
            renderer = self.parallax_renderers[self.active_screen]
            parallax = self.hp_system.parallax_systems.get(self.active_screen)
            
            if parallax:
                render_stats = renderer.render_parallax_system(surface, parallax)
        
        self.frame_count += 1
        frame_time = time.perf_counter() - frame_start
        
        return {
            'frame_time_ms': frame_time * 1000,
            'frame_count': self.frame_count,
            'render_stats': render_stats,
            'active_screen': self.active_screen
        }
    
    def load_premium_asset(self, asset_id: str, asset_type: AssetType, 
                          priority: LoadingPriority = LoadingPriority.HIGH) -> Optional[Any]:
        """Load a premium asset with full optimization"""
        if not self.initialized:
            return None
        
        return self.hp_system.load_asset_optimized(asset_id, asset_type)
    
    def set_quality_mode(self, preset: QualityPreset, lock: bool = False):
        """Set quality mode manually"""
        self.performance_manager.set_quality_preset(preset, lock)
        self.current_quality = preset
    
    def set_adaptive_mode(self, enabled: bool):
        """Enable/disable adaptive quality"""
        self.performance_manager.set_adaptive_mode(enabled)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        if not self.initialized:
            return {'error': 'System not initialized'}
        
        return {
            'system_status': {
                'initialized': self.initialized,
                'active_screen': self.active_screen,
                'frame_count': self.frame_count,
                'initialization_time_s': self.initialization_time
            },
            'performance': self.performance_manager.get_status_summary(),
            'memory': self.memory_manager.get_memory_report(),
            'assets': self.hp_system.get_performance_stats(),
            'configuration': {
                'target_fps': self.config.target_fps,
                'max_memory_mb': self.config.max_memory_mb,
                'quality_preset': self.current_quality.value,
                'integration_mode': self.config.integration_mode.value
            }
        }
    
    def optimize_for_hardware(self):
        """Auto-optimize system for current hardware"""
        if not self.initialized:
            return
        
        hardware_info = self.performance_manager.get_hardware_info()
        
        # Adjust configuration based on hardware
        cpu_cores = hardware_info.get('cpu_count', 1)
        memory_gb = hardware_info.get('memory_total_gb', 4)
        
        if cpu_cores >= 8 and memory_gb >= 16:
            # High-end hardware
            self.config.max_memory_mb = min(2048, memory_gb * 256)  # Use up to 25% of RAM
            self.set_quality_mode(QualityPreset.ULTRA)
        elif cpu_cores >= 4 and memory_gb >= 8:
            # Mid-range hardware
            self.config.max_memory_mb = min(1024, memory_gb * 128)
            self.set_quality_mode(QualityPreset.HIGH)
        else:
            # Low-end hardware
            self.config.max_memory_mb = min(512, memory_gb * 64)
            self.set_quality_mode(QualityPreset.MEDIUM)
        
        self.logger.info(f"Optimized for hardware: {cpu_cores} cores, {memory_gb:.1f}GB RAM")
    
    def add_quality_callback(self, callback: Callable[[QualitySettings], None]):
        """Add callback for quality changes"""
        self.quality_change_callbacks.append(callback)
    
    def add_performance_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback for performance updates"""
        self.performance_callbacks.append(callback)
    
    def force_memory_cleanup(self) -> Dict[str, Any]:
        """Force immediate memory cleanup"""
        if not self.initialized:
            return {'error': 'System not initialized'}
        
        cleanup_results = {}
        
        # Cleanup asset system
        if self.hp_system:
            cleanup_results['assets'] = self.hp_system.force_memory_optimization()
        
        # Cleanup memory manager
        if self.memory_manager:
            cleanup_results['memory'] = self.memory_manager.cleanup_memory(force=True)
        
        # Clear render caches
        cleared_caches = 0
        for renderer in self.parallax_renderers.values():
            renderer.clear_cache()
            cleared_caches += 1
        
        cleanup_results['render_caches_cleared'] = cleared_caches
        
        return cleanup_results
    
    def benchmark_performance(self, duration_seconds: float = 10.0) -> Dict[str, Any]:
        """Run performance benchmark"""
        if not self.initialized:
            return {'error': 'System not initialized'}
        
        self.logger.info(f"Starting {duration_seconds}s performance benchmark")
        
        # Create test surface
        test_surface = pygame.Surface((1920, 1080))
        
        # Track performance
        frame_times = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            frame_start = time.perf_counter()
            
            # Render frame
            dt = 1.0 / self.config.target_fps
            self.render_frame(test_surface, dt)
            
            frame_end = time.perf_counter()
            frame_times.append(frame_end - frame_start)
        
        # Calculate statistics
        import statistics
        avg_frame_time = statistics.mean(frame_times)
        min_frame_time = min(frame_times)
        max_frame_time = max(frame_times)
        
        avg_fps = 1.0 / avg_frame_time
        min_fps = 1.0 / max_frame_time
        max_fps = 1.0 / min_frame_time
        
        target_met = avg_fps >= self.config.target_fps * 0.95  # Within 5% of target
        
        benchmark_result = {
            'duration_s': duration_seconds,
            'frames_rendered': len(frame_times),
            'avg_fps': avg_fps,
            'min_fps': min_fps,
            'max_fps': max_fps,
            'avg_frame_time_ms': avg_frame_time * 1000,
            'target_fps': self.config.target_fps,
            'target_met': target_met,
            'performance_score': min(100.0, (avg_fps / self.config.target_fps) * 100)
        }
        
        self.logger.info(f"Benchmark complete: {avg_fps:.1f} FPS average")
        return benchmark_result
    
    def shutdown(self):
        """Clean shutdown of all systems"""
        if not self.initialized:
            return
        
        self.logger.info("Shutting down Premium Asset Integration System")
        
        # Shutdown systems
        if self.hp_system:
            self.hp_system.shutdown()
        
        if self.performance_manager:
            self.performance_manager.shutdown()
        
        if self.memory_manager:
            self.memory_manager.shutdown()
        
        # Clear renderers
        for renderer in self.parallax_renderers.values():
            renderer.shutdown()
        
        self.parallax_renderers.clear()
        self.initialized = False
        
        self.logger.info("System shutdown complete")


# Global instance
_global_integrator = None

def get_premium_integrator() -> PremiumAssetIntegrator:
    """Get global premium asset integrator"""
    global _global_integrator
    if _global_integrator is None:
        _global_integrator = PremiumAssetIntegrator()
    return _global_integrator

def initialize_premium_system(config: Optional[SystemConfiguration] = None,
                            screen_width: int = 1920, screen_height: int = 1080) -> PremiumAssetIntegrator:
    """Initialize the complete premium asset integration system"""
    global _global_integrator
    _global_integrator = PremiumAssetIntegrator(config)
    
    if _global_integrator.initialize(screen_width, screen_height):
        return _global_integrator
    else:
        raise RuntimeError("Failed to initialize premium asset integration system")

def create_game_ready_config(hardware_tier: str = "auto") -> SystemConfiguration:
    """Create optimized configuration for game deployment"""
    config = SystemConfiguration()
    
    if hardware_tier == "auto":
        # Auto-detect based on system
        import psutil
        cpu_cores = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        if cpu_cores >= 8 and memory_gb >= 16:
            hardware_tier = "high_end"
        elif cpu_cores >= 4 and memory_gb >= 8:
            hardware_tier = "mid_range"
        else:
            hardware_tier = "low_end"
    
    if hardware_tier == "high_end":
        config.target_fps = 60.0
        config.max_memory_mb = 2048
        config.default_quality = QualityPreset.ULTRA
        config.parallax_technique = RenderTechnique.OPTIMIZED
        config.integration_mode = IntegrationMode.QUALITY
        
    elif hardware_tier == "mid_range":
        config.target_fps = 60.0
        config.max_memory_mb = 1024
        config.default_quality = QualityPreset.HIGH
        config.parallax_technique = RenderTechnique.OPTIMIZED
        config.integration_mode = IntegrationMode.BALANCED
        
    else:  # low_end
        config.target_fps = 60.0
        config.max_memory_mb = 512
        config.default_quality = QualityPreset.MEDIUM
        config.parallax_technique = RenderTechnique.CULLED
        config.integration_mode = IntegrationMode.PERFORMANCE
        config.enable_aggressive_gc = True
    
    return config