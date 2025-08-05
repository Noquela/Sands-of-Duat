"""
Performance Integration System for Sands of Duat

Master integration system that coordinates all performance optimization systems
to deliver Hades-level visual quality while maintaining 60fps performance.

This system orchestrates:
- Enhanced Asset Streaming
- Parallax Background System  
- Dynamic Quality Management
- Advanced Memory Management
- Comprehensive Profiling
- Optimized Particle System

Features:
- Centralized performance coordination
- Automatic quality scaling based on performance
- Smart asset preloading and streaming
- Memory pressure response
- Real-time optimization adjustments
- Performance regression detection
"""

import pygame
import threading
import time
import logging
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Import all our optimization systems
from .enhanced_asset_streaming import get_asset_streaming_manager, LoadPriority
from .parallax_background_system import get_parallax_renderer
from .dynamic_quality_manager import get_quality_manager, QualityLevel, QualitySettings
from .advanced_memory_manager import get_memory_manager, MemoryType, MemoryPriority
from .comprehensive_profiler import get_comprehensive_profiler, ProfileCategory
from .lighting_system import get_lighting_system
from ..ui.optimized_particle_system import OptimizedParticleSystem


class PerformanceMode(Enum):
    """Overall performance modes."""
    QUALITY_FIRST = "quality_first"      # Prioritize visual quality
    BALANCED = "balanced"                # Balance quality and performance
    PERFORMANCE_FIRST = "performance_first"  # Prioritize frame rate
    ADAPTIVE = "adaptive"                # Automatically adapt based on hardware


class ScreenType(Enum):
    """Different screen types with different performance requirements."""
    MENU = "menu"
    COMBAT = "combat"
    DECK_BUILDER = "deck_builder"
    MAP = "map"
    PROGRESSION = "progression"


@dataclass
class PerformanceTarget:
    """Performance targets for different scenarios."""
    target_fps: float
    max_frame_time_ms: float
    memory_budget_mb: int
    quality_level: QualityLevel
    
    
class PerformanceCoordinator:
    """Coordinates all performance optimization systems."""
    
    def __init__(self, screen_width: int = 3440, screen_height: int = 1440):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize all subsystems
        self.asset_manager = get_asset_streaming_manager()
        self.parallax_renderer = get_parallax_renderer(screen_width, screen_height)
        self.quality_manager = get_quality_manager()
        self.memory_manager = get_memory_manager()
        self.profiler = get_comprehensive_profiler()
        self.lighting_system = get_lighting_system(screen_width, screen_height)
        
        # Particle system (will be integrated with existing systems)
        self.particle_system = OptimizedParticleSystem(screen_width, screen_height)
        
        # Current state
        self.current_screen: Optional[ScreenType] = None
        self.performance_mode = PerformanceMode.ADAPTIVE
        self.is_optimized = False
        
        # Performance targets for different screens
        self.performance_targets = self._initialize_performance_targets()
        
        # Integration callbacks
        self.screen_change_callbacks: List[Callable[[ScreenType], None]] = []
        self.performance_alert_callbacks: List[Callable[[str, Dict[str, Any]], None]] = []
        
        # Optimization state
        self.last_optimization_time = 0.0
        self.optimization_interval = 5.0  # Optimize every 5 seconds
        
        self.logger = logging.getLogger(__name__)
        
        # Setup integration
        self._setup_system_integration()
    
    def _initialize_performance_targets(self) -> Dict[ScreenType, PerformanceTarget]:
        """Initialize performance targets for different screen types."""
        return {
            ScreenType.MENU: PerformanceTarget(
                target_fps=60.0,
                max_frame_time_ms=16.67,
                memory_budget_mb=256,
                quality_level=QualityLevel.HIGH
            ),
            ScreenType.COMBAT: PerformanceTarget(
                target_fps=60.0,
                max_frame_time_ms=16.67,
                memory_budget_mb=512,
                quality_level=QualityLevel.HIGH
            ),
            ScreenType.DECK_BUILDER: PerformanceTarget(
                target_fps=60.0,
                max_frame_time_ms=16.67,
                memory_budget_mb=384,
                quality_level=QualityLevel.HIGH
            ),
            ScreenType.MAP: PerformanceTarget(
                target_fps=60.0,
                max_frame_time_ms=16.67,
                memory_budget_mb=300,
                quality_level=QualityLevel.MEDIUM
            ),
            ScreenType.PROGRESSION: PerformanceTarget(
                target_fps=60.0,
                max_frame_time_ms=16.67,
                memory_budget_mb=256,
                quality_level=QualityLevel.MEDIUM
            )
        }
    
    def _setup_system_integration(self):
        """Setup integration between all performance systems."""
        # Quality manager callbacks
        self.quality_manager.add_quality_change_callback(self._on_quality_change)
        
        # Profiler alert callbacks
        self.profiler.add_alert_callback(self._on_performance_alert)
        
        # Memory pressure callbacks (already setup in memory manager)
        
        self.logger.info("Performance integration system initialized")
    
    def _on_quality_change(self, new_settings: QualitySettings):
        """Handle quality setting changes."""
        self.logger.info(f"Quality changed - updating all systems")
        
        # Update particle system
        self.particle_system.max_particles = new_settings.max_particles
        
        # Update asset manager memory budget
        if hasattr(self.asset_manager.memory_manager, 'max_memory_bytes'):
            new_budget = new_settings.memory_budget_mb * 1024 * 1024
            self.asset_manager.memory_manager.max_memory_bytes = new_budget
        
        # Update lighting quality
        if hasattr(self.lighting_system, 'light_quality'):
            self.lighting_system.light_quality = new_settings.lighting_quality
        
        # Update parallax layers
        if hasattr(self.parallax_renderer, 'max_layers'):
            self.parallax_renderer.max_layers = new_settings.parallax_layers
    
    def _on_performance_alert(self, alert_type: str, data: Dict[str, Any]):
        """Handle performance alerts from profiler."""
        self.logger.warning(f"Performance alert: {alert_type} - {data}")
        
        # Trigger emergency optimization if needed
        if alert_type in ["frame_time_spike", "memory_pressure"]:
            self._emergency_optimization()
        
        # Notify external listeners
        for callback in self.performance_alert_callbacks:
            try:
                callback(alert_type, data)
            except Exception as e:
                self.logger.error(f"Error in performance alert callback: {e}")
    
    def _emergency_optimization(self):
        """Emergency optimization when performance issues detected."""
        self.logger.warning("Triggering emergency optimization")
        
        # Reduce particle count immediately
        current_particles = len(self.particle_system.active_particles)
        if current_particles > 500:
            # Remove lowest priority particles
            particles_to_remove = current_particles - 500
            removed = 0
            for particle in self.particle_system.active_particles[:]:
                if removed >= particles_to_remove:
                    break
                self.particle_system.particle_pool.release(particle)
                self.particle_system.active_particles.remove(particle)
                removed += 1
        
        # Clear non-critical assets
        self.asset_manager.clear_cache(preserve_protected=True)
        
        # Force garbage collection
        self.memory_manager.gc_optimizer.run_incremental_gc(10.0)
    
    def set_screen(self, screen_type: ScreenType, transition_time: float = 0.5):
        """Change current screen and optimize for it."""
        if self.current_screen == screen_type:
            return
        
        old_screen = self.current_screen
        self.current_screen = screen_type
        
        self.logger.info(f"Switching from {old_screen} to {screen_type}")
        
        # Get performance target for new screen
        target = self.performance_targets.get(screen_type)
        if target:
            # Adjust quality if in adaptive mode
            if self.performance_mode == PerformanceMode.ADAPTIVE:
                current_quality = self.quality_manager.current_quality_level
                if current_quality != target.quality_level:
                    self.quality_manager.set_quality_level(target.quality_level)
        
        # Optimize memory for screen change
        self.memory_manager.optimize_for_screen(screen_type.value)
        
        # Preload assets for new screen
        self._preload_screen_assets(screen_type)
        
        # Setup screen-specific rendering
        self._setup_screen_rendering(screen_type)
        
        # Notify callbacks
        for callback in self.screen_change_callbacks:
            try:
                callback(screen_type)
            except Exception as e:
                self.logger.error(f"Error in screen change callback: {e}")
    
    def _preload_screen_assets(self, screen_type: ScreenType):
        """Preload assets specific to screen type."""
        if screen_type == ScreenType.MENU:
            self.asset_manager.preload_for_screen("menu", LoadPriority.HIGH)
            
        elif screen_type == ScreenType.COMBAT:
            self.asset_manager.preload_for_screen("combat", LoadPriority.CRITICAL)
            
        elif screen_type == ScreenType.DECK_BUILDER:
            self.asset_manager.preload_for_screen("deck_builder", LoadPriority.HIGH)
            
        elif screen_type == ScreenType.MAP:
            # Preload map-specific assets
            pass
            
        elif screen_type == ScreenType.PROGRESSION:
            self.asset_manager.preload_for_screen("progression", LoadPriority.MEDIUM)
    
    def _setup_screen_rendering(self, screen_type: ScreenType):
        """Setup screen-specific rendering optimizations."""
        if screen_type == ScreenType.COMBAT:
            # Setup dramatic combat lighting
            self.lighting_system.clear_lights()
            self.lighting_system.create_combat_lighting(600, 400, 1200, 400)
            
            # Setup combat parallax
            self.parallax_renderer.load_background_for_environment("desert")
            
            # Setup combat weather
            weather_conditions = {
                "heat": 0.7,
                "sandstorm": 0.3,
                "wind_speed": 25.0
            }
            self.parallax_renderer.set_weather_conditions(weather_conditions)
            
        elif screen_type == ScreenType.MENU:
            # Setup atmospheric menu lighting
            self.lighting_system.clear_lights()
            self.lighting_system.set_ambient_lighting((50, 40, 30), 0.4)
            self.lighting_system.create_torch_light(200, 300, True)
            self.lighting_system.create_torch_light(1200, 300, True)
            
        elif screen_type == ScreenType.DECK_BUILDER:
            # Setup focused lighting for deck building
            self.lighting_system.clear_lights()
            self.lighting_system.set_ambient_lighting((60, 55, 45), 0.6)
            
        # Clear particles when changing screens
        self.particle_system.clear_all_particles()
    
    def update(self, delta_time: float):
        """Update all integrated systems."""
        # Start frame profiling
        self.profiler.start_frame()
        
        try:
            # Update quality manager (handles auto-adjustment)
            self.quality_manager.end_frame()
            
            # Update memory management
            frame_budget_ms = 16.67 if self.current_screen == ScreenType.COMBAT else 8.0
            self.memory_manager.update(frame_budget_ms)
            
            # Update particle system
            with self.profiler.profile_render_stage("particles"):
                self.particle_system.update(delta_time)
            
            # Update parallax system
            with self.profiler.profile_render_stage("parallax"):
                self.parallax_renderer.update(delta_time)
            
            # Update lighting system
            with self.profiler.profile_render_stage("lighting"):
                self.lighting_system.update(delta_time)
            
            # Record performance metrics
            self._record_performance_metrics()
            
            # Periodic optimization
            current_time = time.time()
            if current_time - self.last_optimization_time > self.optimization_interval:
                self._periodic_optimization()
                self.last_optimization_time = current_time
        
        finally:
            # End frame profiling
            self.profiler.end_frame()
    
    def _record_performance_metrics(self):
        """Record custom performance metrics."""
        # Record particle metrics
        particle_stats = self.particle_system.get_statistics()
        self.profiler.record_metric(
            "active_particles", 
            ProfileCategory.PARTICLES, 
            particle_stats["active_particles"]
        )
        
        # Record memory metrics
        memory_stats = self.memory_manager.get_memory_report()
        self.profiler.record_metric(
            "memory_usage_mb",
            ProfileCategory.MEMORY,
            memory_stats["process_memory"]["rss_mb"]
        )
        
        # Record asset streaming metrics
        streaming_stats = self.asset_manager.get_comprehensive_stats()
        self.profiler.record_metric(
            "cached_assets",
            ProfileCategory.ASSETS,
            streaming_stats["cache_stats"]["cached_assets"]
        )
    
    def _periodic_optimization(self):
        """Periodic optimization checks and adjustments."""
        # Get current performance summary
        perf_summary = self.profiler.get_performance_summary(180)  # Last 3 seconds
        
        if "frame_statistics" in perf_summary:
            avg_fps = perf_summary["frame_statistics"]["average_fps"]
            target_fps = self.performance_targets.get(self.current_screen, 
                                                    PerformanceTarget(60, 16.67, 512, QualityLevel.HIGH)).target_fps
            
            # Adjust if performance is consistently poor
            if avg_fps < target_fps * 0.9:  # Below 90% of target
                self.logger.info("Performance below target - triggering optimization")
                self._optimize_for_performance()
            elif avg_fps > target_fps * 1.1:  # Above 110% of target
                self.logger.info("Performance above target - can increase quality")
                self._optimize_for_quality()
    
    def _optimize_for_performance(self):
        """Optimize settings for better performance."""
        # Reduce particle count
        if self.particle_system.max_particles > 500:
            self.particle_system.max_particles = max(500, self.particle_system.max_particles - 200)
        
        # Clear some cached assets
        if len(self.asset_manager.stream_cache) > 50:
            self.asset_manager.clear_cache(preserve_protected=True)
    
    def _optimize_for_quality(self):
        """Optimize settings for better quality."""
        # Increase particle count if we have headroom
        quality_settings = self.quality_manager.get_current_settings()
        if self.particle_system.max_particles < quality_settings.max_particles:
            self.particle_system.max_particles = min(
                quality_settings.max_particles,
                self.particle_system.max_particles + 100
            )
    
    def render(self, target_surface: pygame.Surface, camera_rect: Optional[pygame.Rect] = None):
        """Render all integrated visual systems."""
        # Render parallax background
        with self.profiler.profile_render_stage("parallax_render"):
            self.parallax_renderer.render(target_surface, camera_rect)
        
        # Render particle effects
        with self.profiler.profile_render_stage("particles_render"):
            self.particle_system.render(target_surface, camera_rect)
        
        # Apply lighting effects
        with self.profiler.profile_render_stage("lighting_render"):
            self.lighting_system.render_lighting(target_surface)
    
    def set_performance_mode(self, mode: PerformanceMode):
        """Set overall performance mode."""
        if self.performance_mode == mode:
            return
        
        self.performance_mode = mode
        self.logger.info(f"Performance mode changed to {mode.value}")
        
        if mode == PerformanceMode.QUALITY_FIRST:
            # Force high quality
            self.quality_manager.set_quality_level(QualityLevel.HIGH, disable_auto_adjust=True)
        elif mode == PerformanceMode.PERFORMANCE_FIRST:
            # Force lower quality for performance
            self.quality_manager.set_quality_level(QualityLevel.LOW, disable_auto_adjust=True)
        elif mode == PerformanceMode.BALANCED:
            # Use medium quality
            self.quality_manager.set_quality_level(QualityLevel.MEDIUM, disable_auto_adjust=True)
        elif mode == PerformanceMode.ADAPTIVE:
            # Enable auto-adjustment
            self.quality_manager.auto_adjust = True
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive performance dashboard data."""
        return {
            "current_screen": self.current_screen.value if self.current_screen else None,
            "performance_mode": self.performance_mode.value,
            "real_time_metrics": self.profiler.get_real_time_metrics(),
            "quality_settings": self.quality_manager.get_current_settings().to_dict(),
            "memory_stats": self.memory_manager.get_memory_report()["tracked_memory"],
            "particle_stats": self.particle_system.get_statistics(),
            "asset_streaming": self.asset_manager.get_comprehensive_stats()["cache_stats"],
            "optimization_status": {
                "is_optimized": self.is_optimized,
                "last_optimization": self.last_optimization_time
            }
        }
    
    def add_screen_change_callback(self, callback: Callable[[ScreenType], None]):
        """Add callback for screen changes."""
        self.screen_change_callbacks.append(callback)
    
    def add_performance_alert_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add callback for performance alerts."""
        self.performance_alert_callbacks.append(callback)
    
    def generate_performance_report(self, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        if output_dir is None:
            output_dir = Path("reports")
        
        output_dir.mkdir(exist_ok=True)
        timestamp = int(time.time())
        
        # Generate individual system reports
        profiler_report = self.profiler.generate_performance_report(
            output_dir / f"profiler_report_{timestamp}.json"
        )
        
        # Generate integrated report
        integrated_report = {
            "timestamp": time.time(),
            "performance_coordinator": {
                "current_screen": self.current_screen.value if self.current_screen else None,
                "performance_mode": self.performance_mode.value,
                "optimization_history": []
            },
            "system_reports": {
                "profiler": profiler_report,
                "quality_manager": self.quality_manager.get_performance_report(),
                "memory_manager": self.memory_manager.get_memory_report(),
                "particle_system": self.particle_system.get_statistics(),
                "asset_streaming": self.asset_manager.get_comprehensive_stats()
            }
        }
        
        # Save integrated report
        report_path = output_dir / f"integrated_performance_report_{timestamp}.json"
        try:
            import json
            with open(report_path, 'w') as f:
                json.dump(integrated_report, f, indent=2)
            self.logger.info(f"Integrated performance report saved to {report_path}")
        except Exception as e:
            self.logger.error(f"Failed to save integrated report: {e}")
        
        return integrated_report


# Global performance coordinator
_global_coordinator = None

def get_performance_coordinator(screen_width: int = 3440, screen_height: int = 1440) -> PerformanceCoordinator:
    """Get global performance coordinator."""
    global _global_coordinator
    if _global_coordinator is None:
        _global_coordinator = PerformanceCoordinator(screen_width, screen_height)
    return _global_coordinator

def initialize_performance_systems(screen_width: int = 3440, screen_height: int = 1440) -> PerformanceCoordinator:
    """Initialize all performance optimization systems."""
    coordinator = get_performance_coordinator(screen_width, screen_height)
    
    # Establish performance baseline
    coordinator.profiler.establish_performance_baseline()
    
    # Optimize for detected hardware
    coordinator.asset_manager.optimize_for_hardware()
    
    logging.getLogger(__name__).info(
        f"Performance optimization systems initialized for {screen_width}x{screen_height}"
    )
    
    return coordinator

def set_current_screen(screen_type: ScreenType):
    """Set current screen type for optimization."""
    coordinator = get_performance_coordinator()
    coordinator.set_screen(screen_type)

def update_performance_systems(delta_time: float):
    """Update all performance systems - call once per frame."""
    coordinator = get_performance_coordinator()
    coordinator.update(delta_time)

def render_optimized_visuals(target_surface: pygame.Surface, camera_rect: Optional[pygame.Rect] = None):
    """Render all optimized visual systems."""
    coordinator = get_performance_coordinator()
    coordinator.render(target_surface, camera_rect)

def get_performance_dashboard() -> Dict[str, Any]:
    """Get real-time performance dashboard."""
    coordinator = get_performance_coordinator()
    return coordinator.get_performance_dashboard()