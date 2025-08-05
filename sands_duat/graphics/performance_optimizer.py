"""
Performance Optimizer for Parallax and Atmospheric Effects

Provides dynamic quality scaling and Level-of-Detail (LOD) management
to maintain 60fps performance across different hardware configurations.
"""

import pygame
import time
import math
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from collections import deque


class PerformanceLevel(Enum):
    """Performance quality levels."""
    ULTRA = "ultra"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class PerformanceMetric(Enum):
    """Types of performance metrics to track."""
    FRAME_TIME = "frame_time"
    RENDER_TIME = "render_time"
    UPDATE_TIME = "update_time"
    MEMORY_USAGE = "memory_usage"
    PARTICLE_COUNT = "particle_count"


@dataclass
class QualitySettings:
    """Quality settings for different performance levels."""
    parallax_layers: int
    parallax_resolution_scale: float
    particle_density_scale: float
    atmospheric_effects_enabled: bool
    interactive_effects_enabled: bool
    max_particles: int
    render_distance: float
    texture_resolution_scale: float
    shadow_quality: float
    post_processing_enabled: bool


class PerformanceOptimizer:
    """Dynamic performance optimizer for parallax and atmospheric systems."""
    
    def __init__(self, target_fps: float = 60.0):
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        
        # Performance tracking
        self.frame_times = deque(maxlen=60)  # Last 60 frames
        self.render_times = deque(maxlen=60)
        self.update_times = deque(maxlen=60)
        
        # Current performance state
        self.current_level = PerformanceLevel.HIGH
        self.quality_settings = self._initialize_quality_settings()
        
        # Adaptive settings
        self.auto_adjust_enabled = True
        self.performance_check_interval = 1.0  # Check every second
        self.last_performance_check = 0.0
        self.consecutive_drops = 0
        self.consecutive_good_frames = 0
        
        # LOD management
        self.lod_distances = [100, 300, 600, 1000, 2000]
        self.lod_particle_scales = [1.0, 0.8, 0.6, 0.4, 0.2]
        self.lod_effect_scales = [1.0, 0.9, 0.7, 0.5, 0.3]
        
        # Threading for performance monitoring
        self.performance_thread = None
        self.monitoring_active = False
        
        # Hardware detection
        self.hardware_info = self._detect_hardware()
        self._adjust_initial_quality()
    
    def _initialize_quality_settings(self) -> Dict[PerformanceLevel, QualitySettings]:
        """Initialize quality settings for each performance level."""
        return {
            PerformanceLevel.ULTRA: QualitySettings(
                parallax_layers=5,
                parallax_resolution_scale=1.0,
                particle_density_scale=1.0,
                atmospheric_effects_enabled=True,
                interactive_effects_enabled=True,
                max_particles=500,
                render_distance=2000.0,
                texture_resolution_scale=1.0,
                shadow_quality=1.0,
                post_processing_enabled=True
            ),
            PerformanceLevel.HIGH: QualitySettings(
                parallax_layers=4,
                parallax_resolution_scale=1.0,
                particle_density_scale=0.8,
                atmospheric_effects_enabled=True,
                interactive_effects_enabled=True,
                max_particles=300,
                render_distance=1500.0,
                texture_resolution_scale=1.0,
                shadow_quality=0.8,
                post_processing_enabled=True
            ),
            PerformanceLevel.MEDIUM: QualitySettings(
                parallax_layers=3,
                parallax_resolution_scale=0.8,
                particle_density_scale=0.6,
                atmospheric_effects_enabled=True,
                interactive_effects_enabled=True,
                max_particles=200,
                render_distance=1000.0,
                texture_resolution_scale=0.8,
                shadow_quality=0.6,
                post_processing_enabled=False
            ),
            PerformanceLevel.LOW: QualitySettings(
                parallax_layers=2,
                parallax_resolution_scale=0.6,
                particle_density_scale=0.4,
                atmospheric_effects_enabled=True,
                interactive_effects_enabled=False,
                max_particles=100,
                render_distance=600.0,
                texture_resolution_scale=0.6,
                shadow_quality=0.3,
                post_processing_enabled=False
            ),
            PerformanceLevel.MINIMAL: QualitySettings(
                parallax_layers=1,
                parallax_resolution_scale=0.5,
                particle_density_scale=0.2,
                atmospheric_effects_enabled=False,
                interactive_effects_enabled=False,
                max_particles=50,
                render_distance=300.0,
                texture_resolution_scale=0.5,
                shadow_quality=0.0,
                post_processing_enabled=False
            )
        }
    
    def _detect_hardware(self) -> Dict[str, Any]:
        """Detect basic hardware capabilities."""
        try:
            # Get display info
            display_info = pygame.display.Info()
            
            # Basic hardware detection
            hardware = {
                "screen_width": display_info.hw if hasattr(display_info, 'hw') else 1920,
                "screen_height": display_info.h if hasattr(display_info, 'h') else 1080,
                "video_mem": display_info.vid_mem if hasattr(display_info, 'vid_mem') else 0,
                "hardware_accelerated": display_info.hw if hasattr(display_info, 'hw') else False,
                "estimated_performance": "medium"  # Conservative default
            }
            
            # Estimate performance based on screen resolution
            total_pixels = hardware["screen_width"] * hardware["screen_height"]
            if total_pixels > 3840 * 2160:  # 4K+
                hardware["estimated_performance"] = "high_end"
            elif total_pixels > 2560 * 1440:  # 1440p+
                hardware["estimated_performance"] = "medium_high"
            elif total_pixels > 1920 * 1080:  # 1080p+
                hardware["estimated_performance"] = "medium"
            else:
                hardware["estimated_performance"] = "low_end"
            
            return hardware
            
        except Exception as e:
            # Fallback values
            return {
                "screen_width": 1920,
                "screen_height": 1080,
                "video_mem": 0,
                "hardware_accelerated": False,
                "estimated_performance": "medium"
            }
    
    def _adjust_initial_quality(self):
        """Adjust initial quality based on detected hardware."""
        performance = self.hardware_info["estimated_performance"]
        
        if performance == "high_end":
            self.current_level = PerformanceLevel.ULTRA
        elif performance == "medium_high":
            self.current_level = PerformanceLevel.HIGH
        elif performance == "medium":
            self.current_level = PerformanceLevel.MEDIUM
        elif performance == "low_end":
            self.current_level = PerformanceLevel.LOW
        else:
            self.current_level = PerformanceLevel.MEDIUM
    
    def start_monitoring(self):
        """Start background performance monitoring."""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.performance_thread = threading.Thread(target=self._performance_monitor_loop, daemon=True)
            self.performance_thread.start()
    
    def stop_monitoring(self):
        """Stop background performance monitoring."""
        self.monitoring_active = False
        if self.performance_thread:
            self.performance_thread.join(timeout=1.0)
    
    def _performance_monitor_loop(self):
        """Background performance monitoring loop."""
        while self.monitoring_active:
            try:
                time.sleep(0.1)  # Check 10 times per second
                self._check_performance_adjustment()
            except Exception as e:
                print(f"Performance monitor error: {e}")
                time.sleep(1.0)
    
    def record_frame_time(self, frame_time: float):
        """Record frame time for performance tracking."""
        self.frame_times.append(frame_time)
    
    def record_render_time(self, render_time: float):
        """Record render time for performance tracking."""
        self.render_times.append(render_time)
    
    def record_update_time(self, update_time: float):
        """Record update time for performance tracking."""
        self.update_times.append(update_time)
    
    def get_average_frame_time(self) -> float:
        """Get average frame time over recent frames."""
        if not self.frame_times:
            return self.target_frame_time
        return sum(self.frame_times) / len(self.frame_times)
    
    def get_current_fps(self) -> float:
        """Get current FPS based on recent frame times."""
        avg_frame_time = self.get_average_frame_time()
        if avg_frame_time <= 0:
            return self.target_fps
        return 1.0 / avg_frame_time
    
    def is_performance_good(self) -> bool:
        """Check if current performance meets target."""
        current_fps = self.get_current_fps()
        return current_fps >= (self.target_fps * 0.9)  # Allow 10% tolerance
    
    def _check_performance_adjustment(self):
        """Check if performance adjustment is needed."""
        current_time = time.time()
        if current_time - self.last_performance_check < self.performance_check_interval:
            return
        
        self.last_performance_check = current_time
        
        if not self.auto_adjust_enabled:
            return
        
        # Check if we need to adjust quality
        if self.is_performance_good():
            self.consecutive_good_frames += 1
            self.consecutive_drops = 0
            
            # Consider upgrading quality after sustained good performance
            if self.consecutive_good_frames >= 10:  # 10 seconds of good performance
                self._try_upgrade_quality()
                self.consecutive_good_frames = 0
        else:
            self.consecutive_drops += 1
            self.consecutive_good_frames = 0
            
            # Downgrade quality after consecutive poor performance
            if self.consecutive_drops >= 3:  # 3 seconds of poor performance
                self._downgrade_quality()
                self.consecutive_drops = 0
    
    def _try_upgrade_quality(self):
        """Try to upgrade quality level if performance allows."""
        current_index = list(PerformanceLevel).index(self.current_level)
        if current_index > 0:  # Can upgrade
            new_level = list(PerformanceLevel)[current_index - 1]
            self.set_performance_level(new_level)
            print(f"Performance optimizer: Upgraded to {new_level.value}")
    
    def _downgrade_quality(self):
        """Downgrade quality level to improve performance."""
        current_index = list(PerformanceLevel).index(self.current_level)
        if current_index < len(PerformanceLevel) - 1:  # Can downgrade
            new_level = list(PerformanceLevel)[current_index + 1]
            self.set_performance_level(new_level)
            print(f"Performance optimizer: Downgraded to {new_level.value}")
    
    def set_performance_level(self, level: PerformanceLevel):
        """Set performance level and update all systems."""
        self.current_level = level
        # Notify all systems that use the optimizer to update their settings
        self._notify_quality_change()
    
    def _notify_quality_change(self):
        """Notify registered systems of quality changes."""
        # This would notify parallax, atmospheric, and other systems
        # For now, systems will query the optimizer directly
        pass
    
    def get_current_settings(self) -> QualitySettings:
        """Get current quality settings."""
        return self.quality_settings[self.current_level]
    
    def get_lod_scale(self, distance: float, base_scale: float = 1.0) -> float:
        """Get Level-of-Detail scale based on distance."""
        for i, lod_distance in enumerate(self.lod_distances):
            if distance <= lod_distance:
                return base_scale * self.lod_effect_scales[i]
        return base_scale * self.lod_effect_scales[-1]  # Furthest LOD
    
    def get_particle_lod_scale(self, distance: float) -> float:
        """Get particle density scale based on distance."""
        for i, lod_distance in enumerate(self.lod_distances):
            if distance <= lod_distance:
                return self.lod_particle_scales[i]
        return self.lod_particle_scales[-1]  # Furthest LOD
    
    def should_render_effect(self, distance: float, effect_priority: float = 1.0) -> bool:
        """Determine if an effect should be rendered based on distance and priority."""
        settings = self.get_current_settings()
        
        # Always render high priority effects
        if effect_priority >= 0.9:
            return True
        
        # Check render distance
        if distance > settings.render_distance:
            return False
        
        # Scale render decision based on distance and quality
        distance_factor = 1.0 - (distance / settings.render_distance)
        quality_factor = settings.particle_density_scale
        
        render_threshold = effect_priority * distance_factor * quality_factor
        return render_threshold > 0.3  # Threshold for rendering
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        return {
            "current_level": self.current_level.value,
            "average_fps": self.get_current_fps(),
            "average_frame_time": self.get_average_frame_time() * 1000,  # in ms
            "target_fps": self.target_fps,
            "is_performance_good": self.is_performance_good(),
            "consecutive_good_frames": self.consecutive_good_frames,
            "consecutive_drops": self.consecutive_drops,
            "auto_adjust_enabled": self.auto_adjust_enabled
        }
    
    def enable_auto_adjust(self, enabled: bool = True):
        """Enable or disable automatic quality adjustment."""
        self.auto_adjust_enabled = enabled
    
    def set_target_fps(self, fps: float):
        """Set target FPS."""
        self.target_fps = fps
        self.target_frame_time = 1.0 / fps


# Global performance optimizer
_global_performance_optimizer = None

def get_performance_optimizer(target_fps: float = 60.0) -> PerformanceOptimizer:
    """Get global performance optimizer."""
    global _global_performance_optimizer
    if _global_performance_optimizer is None:
        _global_performance_optimizer = PerformanceOptimizer(target_fps)
        _global_performance_optimizer.start_monitoring()
    return _global_performance_optimizer


def optimize_for_performance(func: Callable) -> Callable:
    """Decorator for performance optimization of functions."""
    def wrapper(*args, **kwargs):
        optimizer = get_performance_optimizer()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            execution_time = time.time() - start_time
            
            # Record performance based on function name
            if 'render' in func.__name__.lower():
                optimizer.record_render_time(execution_time)
            elif 'update' in func.__name__.lower():
                optimizer.record_update_time(execution_time)
        
        return result
    
    return wrapper