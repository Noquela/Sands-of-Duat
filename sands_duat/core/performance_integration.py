"""
Performance Integration Module
Integrates all performance optimizations for Sands of Duat.

This module provides a unified interface for:
- Performance profiling
- Optimized particle systems
- Hades theme rendering
- Asset management
- Adaptive quality control
"""

import pygame
import time
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

from .performance_profiler import get_profiler, initialize_profiler, profile_frame_start, profile_frame_end
from ..ui.optimized_particle_system import OptimizedParticleSystem, ParticleType
from ..ui.optimized_hades_theme import OptimizedHadesEgyptianTheme
from ..assets.optimized_asset_manager import get_asset_manager, initialize_asset_manager, AssetType


class PerformanceManager:
    """
    Centralized performance management system.
    
    Coordinates all performance optimizations and provides
    unified interface for the game engine.
    """
    
    def __init__(self, display_size: Tuple[int, int], target_fps: float = 60.0):
        self.display_size = display_size
        self.target_fps = target_fps
        self.frame_budget_ms = 1000.0 / target_fps
        
        # Initialize subsystems
        self.profiler = initialize_profiler(max_samples=1000)
        self.asset_manager = initialize_asset_manager(cache_size_mb=512, enable_compression=True)
        self.particle_system = OptimizedParticleSystem(display_size[0], display_size[1], max_particles=2000)
        self.theme = OptimizedHadesEgyptianTheme(display_size)
        
        # Performance tracking
        self.current_fps = target_fps
        self.performance_history = []
        self.adaptive_quality_enabled = True
        
        # Quality control
        self.quality_adjustment_timer = 0.0
        self.quality_adjustment_interval = 2.0  # Adjust every 2 seconds
        
        # Statistics
        self.session_stats = {
            "frames_rendered": 0,
            "total_particles_created": 0,
            "cache_hits": 0,
            "performance_adjustments": 0
        }
        
        # Start continuous profiling
        self.profiler.start_continuous_profiling(interval=1.0)
    
    def start_frame(self):
        """Start a new frame with profiling."""
        profile_frame_start()
        self.profiler.start_frame()
        return time.perf_counter()
    
    def end_frame(self, frame_start_time: float):
        """End frame and calculate performance metrics."""
        frame_end_time = time.perf_counter()
        frame_time_ms = (frame_end_time - frame_start_time) * 1000
        
        # Calculate current FPS
        self.current_fps = 1000.0 / frame_time_ms if frame_time_ms > 0 else self.target_fps
        
        # Get particle count for profiling
        particle_stats = self.particle_system.get_statistics()
        particle_count = particle_stats["active_particles"]
        
        # End frame profiling
        profile_frame_end(particle_count=particle_count, draw_calls=10)
        self.profiler.end_frame(particle_count=particle_count, draw_calls=10)
        
        # Update performance history
        self.performance_history.append(self.current_fps)
        if len(self.performance_history) > 60:  # Keep last 60 frames
            self.performance_history.pop(0)
        
        # Update session stats
        self.session_stats["frames_rendered"] += 1
        
        return frame_time_ms
    
    def update(self, delta_time: float):
        """Update all performance systems."""
        # Update particle system
        with self.profiler.time_operation("particles"):
            self.particle_system.update(delta_time)
        
        # Update theme animations
        with self.profiler.time_operation("theme_update"):
            self.theme.update_animation_time(delta_time)
        
        # Update asset manager performance metrics
        self.asset_manager.update_performance_metrics(self.current_fps)
        
        # Adaptive quality control
        if self.adaptive_quality_enabled:
            self.quality_adjustment_timer += delta_time
            if self.quality_adjustment_timer >= self.quality_adjustment_interval:
                self._adjust_quality_based_on_performance()
                self.quality_adjustment_timer = 0.0
        
        # Periodic memory optimization
        if self.session_stats["frames_rendered"] % 3600 == 0:  # Every minute at 60fps
            self._optimize_memory_usage()
    
    def render_particles(self, surface: pygame.Surface, camera_rect: Optional[pygame.Rect] = None):
        """Render particles with profiling."""
        with self.profiler.time_operation("particle_render"):
            self.particle_system.render(surface, camera_rect)
    
    def render_ui_element(self, surface: pygame.Surface, element_type: str, *args, **kwargs):
        """Render UI element with profiling."""
        with self.profiler.time_operation("ui_render"):
            if element_type == "button":
                return self.theme.draw_ornate_button(surface, *args, **kwargs)
            elif element_type == "card_frame":
                return self.theme.draw_card_frame(surface, *args, **kwargs)
            elif element_type == "health_orb":
                return self.theme.draw_health_orb(surface, *args, **kwargs)
            elif element_type == "title_text":
                return self.theme.draw_title_text(surface, *args, **kwargs)
            elif element_type == "background_overlay":
                return self.theme.draw_background_overlay(surface, *args, **kwargs)
    
    def load_asset(self, asset_path: str, asset_type: AssetType, force_reload: bool = False) -> Optional[pygame.Surface]:
        """Load asset with profiling."""
        return self.asset_manager.load_asset(asset_path, asset_type, force_reload)
    
    def load_asset_async(self, asset_path: str, asset_type: AssetType, callback=None):
        """Load asset asynchronously."""
        return self.asset_manager.load_asset_async(asset_path, asset_type, callback)
    
    def create_particle_effect(self, effect_type: str, x: float, y: float, **kwargs):
        """Create particle effect with automatic tracking."""
        intensity = kwargs.get('intensity', 1.0)
        
        if effect_type == "sand_flow":
            end_x = kwargs.get('end_x', x + 100)
            end_y = kwargs.get('end_y', y + 100)
            count = self.particle_system.create_sand_flow_effect(x, y, end_x, end_y, intensity)
        elif effect_type == "combat_hit":
            damage = kwargs.get('damage', 10)
            count = self.particle_system.create_combat_hit_effect(x, y, damage)
        elif effect_type == "card_effect":
            card_type = kwargs.get('card_type', 'attack')
            count = self.particle_system.create_card_effect(card_type, x, y, intensity)
        else:
            # Generic particle burst
            particle_type = getattr(ParticleType, effect_type.upper(), ParticleType.SAND_GRAIN)
            particle_count = kwargs.get('count', 10)
            count = self.particle_system.create_particle_burst(x, y, particle_type, particle_count, intensity)
        
        self.session_stats["total_particles_created"] += count
        return count
    
    def _adjust_quality_based_on_performance(self):
        """Adjust quality settings based on recent performance."""
        if len(self.performance_history) < 30:
            return  # Need more data
        
        # Calculate average FPS over recent frames
        recent_fps = sum(self.performance_history[-30:]) / 30
        
        # Performance thresholds
        poor_performance_threshold = self.target_fps * 0.85  # 15% below target
        good_performance_threshold = self.target_fps * 1.05  # 5% above target
        
        if recent_fps < poor_performance_threshold:
            # Performance is poor, reduce quality
            self._reduce_quality()
            self.session_stats["performance_adjustments"] += 1
        elif recent_fps > good_performance_threshold:
            # Performance is good, potentially increase quality
            self._increase_quality()
            self.session_stats["performance_adjustments"] += 1
    
    def _reduce_quality(self):
        """Reduce quality settings to improve performance."""
        # Reduce theme detail level
        if self.theme.current_detail_level > 0:
            self.theme.set_detail_level(self.theme.current_detail_level - 1)
        
        # Reduce particle system quality
        quality_config = self.particle_system.quality_manager.get_quality_config()
        if quality_config["particle_multiplier"] > 0.2:
            # Trigger quality reduction in particle system
            self.particle_system.quality_manager._adjust_quality(self.frame_budget_ms * 1.5)
        
        # Adjust asset manager LOD
        if self.asset_manager.lod_manager.base_quality.value != "low":
            self.asset_manager.lod_manager._decrease_quality()
    
    def _increase_quality(self):
        """Increase quality settings when performance allows."""
        # Increase theme detail level
        if self.theme.current_detail_level < self.theme.max_detail_level:
            self.theme.set_detail_level(self.theme.current_detail_level + 1)
        
        # Increase particle system quality
        quality_config = self.particle_system.quality_manager.get_quality_config()
        if quality_config["particle_multiplier"] < 1.0:
            # Trigger quality increase in particle system
            self.particle_system.quality_manager._adjust_quality(self.frame_budget_ms * 0.5)
        
        # Adjust asset manager LOD
        if self.asset_manager.lod_manager.base_quality.value != "ultra":
            self.asset_manager.lod_manager._increase_quality()
    
    def _optimize_memory_usage(self):
        """Optimize memory usage across all systems."""
        with self.profiler.time_operation("memory_optimization"):
            # Clear theme caches
            self.theme.clear_cache()
            
            # Optimize asset manager memory
            self.asset_manager.optimize_memory_usage()
            
            # Clear old particles
            if len(self.particle_system.active_particles) > self.particle_system.max_particles * 0.8:
                self.particle_system.clear_all_particles()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        # Get individual system stats
        profiler_summary = self.profiler.get_performance_summary()
        particle_stats = self.particle_system.get_statistics()
        theme_stats = self.theme.get_performance_stats()
        asset_stats = self.asset_manager.get_statistics()
        
        # Calculate overall performance metrics
        avg_fps = sum(self.performance_history) / len(self.performance_history) if self.performance_history else self.target_fps
        
        return {
            "overall_performance": {
                "current_fps": self.current_fps,
                "average_fps": avg_fps,
                "target_fps": self.target_fps,
                "performance_stability": self._calculate_performance_stability(),
                "quality_adjustments": self.session_stats["performance_adjustments"]
            },
            "profiler_data": profiler_summary,
            "particle_system": particle_stats,
            "theme_rendering": theme_stats,
            "asset_management": asset_stats,
            "session_statistics": self.session_stats.copy(),
            "recommendations": self._generate_performance_recommendations()
        }
    
    def _calculate_performance_stability(self) -> float:
        """Calculate performance stability metric (0-1)."""
        if len(self.performance_history) < 10:
            return 1.0
        
        # Calculate coefficient of variation
        import statistics
        avg_fps = statistics.mean(self.performance_history)
        std_fps = statistics.stdev(self.performance_history)
        
        if avg_fps == 0:
            return 0.0
        
        cv = std_fps / avg_fps
        # Convert to stability score (lower CV = higher stability)
        stability = max(0.0, 1.0 - cv)
        return stability
    
    def _generate_performance_recommendations(self) -> list[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        # Analyze current performance
        if len(self.performance_history) >= 30:
            recent_fps = sum(self.performance_history[-30:]) / 30
            
            if recent_fps < self.target_fps * 0.9:
                recommendations.append("Consider reducing visual quality settings for better performance")
            
            if recent_fps < self.target_fps * 0.7:
                recommendations.append("CRITICAL: Performance significantly below target. Reduce particle count and detail levels")
        
        # Check particle system
        particle_stats = self.particle_system.get_statistics()
        if particle_stats["active_particles"] > 1500:
            recommendations.append("High particle count detected. Consider particle LOD or reduced emission rates")
        
        # Check theme rendering
        theme_stats = self.theme.get_performance_stats()
        if theme_stats["cache_efficiency"] < 0.7:
            recommendations.append("Low UI cache efficiency. Consider optimizing UI element variety")
        
        # Check asset management
        asset_stats = self.asset_manager.get_statistics()
        if asset_stats["cache_statistics"]["memory_usage_mb"] > 400:
            recommendations.append("High asset memory usage. Consider texture compression or LOD")
        
        if not recommendations:
            recommendations.append("Performance is optimal. All systems running efficiently.")
        
        return recommendations
    
    def export_performance_data(self, filepath: str):
        """Export detailed performance data for analysis."""
        report = self.get_performance_report()
        
        # Add detailed frame data
        detailed_data = {
            "performance_report": report,
            "export_timestamp": time.time(),
            "configuration": {
                "display_size": self.display_size,
                "target_fps": self.target_fps,
                "adaptive_quality": self.adaptive_quality_enabled
            }
        }
        
        return self.profiler.export_profile_data(filepath, include_detailed=True)
    
    def set_adaptive_quality(self, enabled: bool):
        """Enable or disable adaptive quality control."""
        self.adaptive_quality_enabled = enabled
    
    def force_quality_level(self, detail_level: int):
        """Force specific quality level (disables adaptive quality)."""
        self.adaptive_quality_enabled = False
        self.theme.set_detail_level(detail_level)
        
        # Set corresponding quality levels for other systems
        quality_map = {0: "minimal", 1: "low", 2: "medium", 3: "high"}
        if detail_level in quality_map:
            quality_name = quality_map[detail_level]
            self.particle_system.quality_manager.current_quality = quality_name
    
    def shutdown(self):
        """Shutdown performance manager and all subsystems."""
        self.profiler.stop_continuous_profiling()
        self.asset_manager.shutdown()
        
        # Export final performance report
        self.export_performance_data("performance_final_report.json")


# Global performance manager instance
_global_performance_manager: Optional[PerformanceManager] = None


def initialize_performance_manager(display_size: Tuple[int, int], target_fps: float = 60.0) -> PerformanceManager:
    """Initialize the global performance manager."""
    global _global_performance_manager
    _global_performance_manager = PerformanceManager(display_size, target_fps)
    return _global_performance_manager


def get_performance_manager() -> Optional[PerformanceManager]:
    """Get the global performance manager instance."""
    return _global_performance_manager


def shutdown_performance_manager():
    """Shutdown the global performance manager."""
    global _global_performance_manager
    if _global_performance_manager:
        _global_performance_manager.shutdown()
        _global_performance_manager = None