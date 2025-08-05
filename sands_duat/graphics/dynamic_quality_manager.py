"""
Dynamic Quality Management System for Sands of Duat

Real-time performance monitoring and quality adjustment system that maintains 
60fps while preserving artistic vision. Adapts visual quality based on hardware 
capability and current performance metrics.

Features:
- Real-time frame time monitoring
- GPU utilization tracking
- Memory usage monitoring
- Intelligent quality scaling
- Performance prediction
- Quality presets for different hardware tiers
- Graceful degradation that preserves visual appeal
"""

import pygame
import time
import psutil
import threading
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque
import statistics
import logging
import json
from pathlib import Path

from ..core.performance_profiler import profile_operation


class QualityLevel(Enum):
    """Visual quality levels."""
    ULTRA = "ultra"        # Maximum quality, RTX 4080+ level
    HIGH = "high"          # High quality, RTX 3070+ level
    MEDIUM = "medium"      # Balanced quality, GTX 1660+ level
    LOW = "low"           # Performance focused, GTX 1050+ level
    MINIMAL = "minimal"    # Bare minimum, integrated graphics


class PerformanceMetric(Enum):
    """Performance metrics to track."""
    FRAME_TIME = "frame_time"
    FPS = "fps"
    GPU_MEMORY = "gpu_memory"
    SYSTEM_MEMORY = "system_memory"
    CPU_USAGE = "cpu_usage"
    PARTICLE_COUNT = "particle_count"
    DRAW_CALLS = "draw_calls"


@dataclass
class QualitySettings:
    """Quality settings for different visual aspects."""
    # Particle system
    max_particles: int
    particle_quality_multiplier: float
    particle_lod_distance: float
    
    # Asset quality
    texture_quality: float  # 0.5 = half resolution, 1.0 = full resolution
    asset_compression: bool
    mipmap_levels: int
    
    # Visual effects
    lighting_quality: str   # "low", "medium", "high"
    shadow_quality: str
    parallax_layers: int
    post_processing: bool
    
    # Performance limits
    target_fps: float
    max_draw_calls: int
    memory_budget_mb: int
    
    # Specific effects
    heat_shimmer: bool
    atmospheric_particles: bool
    dynamic_lighting: bool
    screen_effects: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class HardwareTier(Enum):
    """Hardware capability tiers."""
    ENTHUSIAST = "enthusiast"    # RTX 4080+, 32GB+ RAM
    HIGH_END = "high_end"        # RTX 3080+, 16GB+ RAM  
    MID_RANGE = "mid_range"      # RTX 3060+, 8GB+ RAM
    BUDGET = "budget"            # GTX 1660+, 8GB+ RAM
    LOW_END = "low_end"          # GTX 1050+, 4GB+ RAM


class PerformanceProfiler:
    """Profiles system performance in real-time."""
    
    def __init__(self, sample_window: int = 120):  # 2 seconds at 60fps
        self.sample_window = sample_window
        self.metrics: Dict[PerformanceMetric, deque] = {
            metric: deque(maxlen=sample_window) for metric in PerformanceMetric
        }
        
        # Performance tracking
        self.frame_start_time = 0.0
        self.last_frame_time = 0.0
        self.frame_count = 0
        
        # System monitoring
        self.process = psutil.Process()
        self.system_monitor_interval = 1.0  # Check system stats every second
        self.last_system_check = 0.0
        
        # GPU monitoring (simplified)
        self.gpu_memory_usage = 0.0
        self.estimated_gpu_usage = 0.0
        
    def start_frame(self):
        """Mark the start of a frame for timing."""
        self.frame_start_time = time.perf_counter()
    
    def end_frame(self):
        """Mark the end of a frame and record metrics."""
        if self.frame_start_time > 0:
            frame_time = time.perf_counter() - self.frame_start_time
            fps = 1.0 / frame_time if frame_time > 0 else 0.0
            
            self.metrics[PerformanceMetric.FRAME_TIME].append(frame_time)
            self.metrics[PerformanceMetric.FPS].append(fps)
            
            self.last_frame_time = frame_time
            self.frame_count += 1
            
            # Update system metrics periodically
            current_time = time.time()
            if current_time - self.last_system_check > self.system_monitor_interval:
                self._update_system_metrics()
                self.last_system_check = current_time
    
    def _update_system_metrics(self):
        """Update system performance metrics."""
        try:
            # CPU usage
            cpu_percent = self.process.cpu_percent()
            self.metrics[PerformanceMetric.CPU_USAGE].append(cpu_percent)
            
            # Memory usage
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            self.metrics[PerformanceMetric.SYSTEM_MEMORY].append(memory_mb)
            
            # Estimate GPU usage based on rendering complexity
            self._estimate_gpu_metrics()
            
        except Exception as e:
            # Handle cases where system monitoring fails
            pass
    
    def _estimate_gpu_metrics(self):
        """Estimate GPU metrics based on rendering load."""
        # Simplified GPU usage estimation
        frame_time = self.last_frame_time
        
        # Higher frame times suggest higher GPU load
        if frame_time > 0.020:  # Over 20ms (under 50fps)
            estimated_usage = min(100.0, 70.0 + (frame_time - 0.020) * 1000)
        elif frame_time > 0.016:  # Over 16ms (under 60fps)
            estimated_usage = 50.0 + (frame_time - 0.016) * 5000
        else:
            estimated_usage = frame_time * 3000  # Linear scaling for good performance
        
        self.estimated_gpu_usage = estimated_usage
    
    def record_draw_calls(self, count: int):
        """Record number of draw calls for current frame."""
        self.metrics[PerformanceMetric.DRAW_CALLS].append(count)
    
    def record_particle_count(self, count: int):
        """Record active particle count."""
        self.metrics[PerformanceMetric.PARTICLE_COUNT].append(count)
    
    def get_average_metric(self, metric: PerformanceMetric, window: Optional[int] = None) -> float:
        """Get average value for a metric over specified window."""
        data = list(self.metrics[metric])
        if not data:
            return 0.0
        
        if window and len(data) > window:
            data = data[-window:]
        
        return statistics.mean(data)
    
    def get_percentile_metric(self, metric: PerformanceMetric, percentile: float) -> float:
        """Get percentile value for a metric (e.g., 95th percentile frame time)."""
        data = list(self.metrics[metric])
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = int(len(sorted_data) * (percentile / 100.0))
        index = min(index, len(sorted_data) - 1)
        
        return sorted_data[index]
    
    def is_performance_stable(self, target_fps: float = 60.0, tolerance: float = 0.1) -> bool:
        """Check if performance is stable around target FPS."""
        if len(self.metrics[PerformanceMetric.FPS]) < 30:
            return False  # Need sufficient samples
        
        recent_fps = list(self.metrics[PerformanceMetric.FPS])[-30:]  # Last 30 frames
        avg_fps = statistics.mean(recent_fps)
        
        # Check if average FPS is within tolerance
        fps_diff = abs(avg_fps - target_fps) / target_fps
        return fps_diff <= tolerance
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            "average_fps": self.get_average_metric(PerformanceMetric.FPS),
            "average_frame_time_ms": self.get_average_metric(PerformanceMetric.FRAME_TIME) * 1000,
            "fps_95th_percentile": self.get_percentile_metric(PerformanceMetric.FPS, 5),  # 5th percentile = worst 5%
            "frame_time_95th_percentile_ms": self.get_percentile_metric(PerformanceMetric.FRAME_TIME, 95) * 1000,
            "cpu_usage_percent": self.get_average_metric(PerformanceMetric.CPU_USAGE),
            "memory_usage_mb": self.get_average_metric(PerformanceMetric.SYSTEM_MEMORY),
            "estimated_gpu_usage": self.estimated_gpu_usage,
            "average_particles": self.get_average_metric(PerformanceMetric.PARTICLE_COUNT),
            "average_draw_calls": self.get_average_metric(PerformanceMetric.DRAW_CALLS),
            "frame_count": self.frame_count,
            "is_stable": self.is_performance_stable()
        }


class QualityPresetManager:
    """Manages quality presets for different hardware tiers."""
    
    def __init__(self):
        self.presets = self._initialize_quality_presets()
        self.custom_preset: Optional[QualitySettings] = None
    
    def _initialize_quality_presets(self) -> Dict[QualityLevel, QualitySettings]:
        """Initialize predefined quality presets."""
        return {
            QualityLevel.ULTRA: QualitySettings(
                max_particles=3000,
                particle_quality_multiplier=1.0,
                particle_lod_distance=1000.0,
                texture_quality=1.0,
                asset_compression=False,
                mipmap_levels=4,
                lighting_quality="high",
                shadow_quality="high",
                parallax_layers=5,
                post_processing=True,
                target_fps=60.0,
                max_draw_calls=1000,
                memory_budget_mb=1024,
                heat_shimmer=True,
                atmospheric_particles=True,
                dynamic_lighting=True,
                screen_effects=True
            ),
            
            QualityLevel.HIGH: QualitySettings(
                max_particles=2000,
                particle_quality_multiplier=0.8,
                particle_lod_distance=800.0,
                texture_quality=1.0,
                asset_compression=False,
                mipmap_levels=3,
                lighting_quality="high",
                shadow_quality="medium",
                parallax_layers=4,
                post_processing=True,
                target_fps=60.0,
                max_draw_calls=800,
                memory_budget_mb=512,
                heat_shimmer=True,
                atmospheric_particles=True,
                dynamic_lighting=True,
                screen_effects=True
            ),
            
            QualityLevel.MEDIUM: QualitySettings(
                max_particles=1200,
                particle_quality_multiplier=0.6,
                particle_lod_distance=600.0,
                texture_quality=0.8,
                asset_compression=True,
                mipmap_levels=2,
                lighting_quality="medium",
                shadow_quality="medium",
                parallax_layers=3,
                post_processing=False,
                target_fps=60.0,
                max_draw_calls=600,
                memory_budget_mb=384,
                heat_shimmer=True,
                atmospheric_particles=False,
                dynamic_lighting=True,
                screen_effects=False
            ),
            
            QualityLevel.LOW: QualitySettings(
                max_particles=600,
                particle_quality_multiplier=0.4,
                particle_lod_distance=400.0,
                texture_quality=0.6,
                asset_compression=True,
                mipmap_levels=1,
                lighting_quality="low",
                shadow_quality="low",
                parallax_layers=2,
                post_processing=False,
                target_fps=60.0,
                max_draw_calls=400,
                memory_budget_mb=256,
                heat_shimmer=False,
                atmospheric_particles=False,
                dynamic_lighting=False,
                screen_effects=False
            ),
            
            QualityLevel.MINIMAL: QualitySettings(
                max_particles=300,
                particle_quality_multiplier=0.2,
                particle_lod_distance=200.0,
                texture_quality=0.4,
                asset_compression=True,
                mipmap_levels=1,
                lighting_quality="low",
                shadow_quality="low",
                parallax_layers=1,
                post_processing=False,
                target_fps=30.0,  # Lower target for very weak hardware
                max_draw_calls=200,
                memory_budget_mb=128,
                heat_shimmer=False,
                atmospheric_particles=False,
                dynamic_lighting=False,
                screen_effects=False
            )
        }
    
    def get_preset(self, quality_level: QualityLevel) -> QualitySettings:
        """Get quality settings for specified level."""
        return self.presets[quality_level]
    
    def create_custom_preset(self, base_level: QualityLevel, overrides: Dict[str, Any]) -> QualitySettings:
        """Create custom preset based on base level with overrides."""
        base_settings = self.get_preset(base_level)
        custom_dict = base_settings.to_dict()
        custom_dict.update(overrides)
        
        # Convert back to QualitySettings
        self.custom_preset = QualitySettings(**custom_dict)
        return self.custom_preset


class HardwareDetector:
    """Detects and classifies hardware capabilities."""
    
    def __init__(self):
        self.hardware_tier = self._detect_hardware_tier()
        self.recommended_quality = self._get_recommended_quality()
        self.logger = logging.getLogger(__name__)
    
    def _detect_hardware_tier(self) -> HardwareTier:
        """Detect hardware tier based on system specifications."""
        # Get system memory
        total_memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Estimate GPU tier (simplified heuristic)
        gpu_tier = self._estimate_gpu_tier()
        cpu_score = self._estimate_cpu_score()
        
        # Classify hardware tier
        if gpu_tier >= 4 and total_memory_gb >= 16 and cpu_score >= 0.8:
            return HardwareTier.ENTHUSIAST
        elif gpu_tier >= 3 and total_memory_gb >= 12 and cpu_score >= 0.7:
            return HardwareTier.HIGH_END
        elif gpu_tier >= 2 and total_memory_gb >= 8 and cpu_score >= 0.6:
            return HardwareTier.MID_RANGE
        elif gpu_tier >= 1 and total_memory_gb >= 6 and cpu_score >= 0.4:
            return HardwareTier.BUDGET
        else:
            return HardwareTier.LOW_END
    
    def _estimate_gpu_tier(self) -> int:
        """Estimate GPU tier (0-5, higher is better)."""
        # This is a simplified estimation
        # In practice, would query actual GPU information
        total_memory_gb = psutil.virtual_memory().total / (1024**3)
        
        if total_memory_gb >= 32:
            return 5  # Assume high-end GPU with lots of system RAM
        elif total_memory_gb >= 16:
            return 3  # Assume mid-high end GPU
        elif total_memory_gb >= 8:
            return 2  # Assume mid-range GPU
        else:
            return 1  # Assume budget GPU
    
    def _estimate_cpu_score(self) -> float:
        """Estimate CPU performance score (0.0-1.0)."""
        cpu_count = psutil.cpu_count(logical=False)  # Physical cores
        logical_count = psutil.cpu_count(logical=True)
        
        # Simple heuristic based on core count
        if cpu_count >= 8:
            return 1.0
        elif cpu_count >= 6:
            return 0.8
        elif cpu_count >= 4:
            return 0.6
        else:
            return 0.4
    
    def _get_recommended_quality(self) -> QualityLevel:
        """Get recommended quality level for detected hardware."""
        tier_to_quality = {
            HardwareTier.ENTHUSIAST: QualityLevel.ULTRA,
            HardwareTier.HIGH_END: QualityLevel.HIGH,
            HardwareTier.MID_RANGE: QualityLevel.MEDIUM,
            HardwareTier.BUDGET: QualityLevel.LOW,
            HardwareTier.LOW_END: QualityLevel.MINIMAL
        }
        
        return tier_to_quality[self.hardware_tier]
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get comprehensive hardware information."""
        return {
            "hardware_tier": self.hardware_tier.value,
            "recommended_quality": self.recommended_quality.value,
            "total_memory_gb": psutil.virtual_memory().total / (1024**3),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "estimated_gpu_tier": self._estimate_gpu_tier(),
            "estimated_cpu_score": self._estimate_cpu_score()
        }


class DynamicQualityManager:
    """Main dynamic quality management system."""
    
    def __init__(self, auto_adjust: bool = True):
        self.profiler = PerformanceProfiler()
        self.preset_manager = QualityPresetManager()
        self.hardware_detector = HardwareDetector()
        
        # Current state
        self.current_quality_level = self.hardware_detector.recommended_quality
        self.current_settings = self.preset_manager.get_preset(self.current_quality_level)
        self.auto_adjust = auto_adjust
        
        # Adjustment logic
        self.adjustment_interval = 3.0  # Adjust every 3 seconds
        self.last_adjustment_time = 0.0
        self.stability_threshold = 2.0  # Require 2 seconds of stable performance before upgrading
        self.last_stable_time = 0.0
        
        # Callbacks for quality changes
        self.quality_change_callbacks: List[Callable[[QualitySettings], None]] = []
        
        self.logger = logging.getLogger(__name__)
        
        # Load saved settings if available
        self._load_user_preferences()
        
        self.logger.info(f"Dynamic Quality Manager initialized: "
                        f"Hardware={self.hardware_detector.hardware_tier.value}, "
                        f"Quality={self.current_quality_level.value}")
    
    def _load_user_preferences(self):
        """Load user quality preferences from file."""
        try:
            config_path = Path("config/quality_settings.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    user_prefs = json.load(f)
                
                if "quality_level" in user_prefs:
                    quality_name = user_prefs["quality_level"]
                    try:
                        self.current_quality_level = QualityLevel(quality_name)
                        self.current_settings = self.preset_manager.get_preset(self.current_quality_level)
                        self.logger.info(f"Loaded user quality preference: {quality_name}")
                    except ValueError:
                        self.logger.warning(f"Invalid quality level in config: {quality_name}")
                
                self.auto_adjust = user_prefs.get("auto_adjust", self.auto_adjust)
        except Exception as e:
            self.logger.warning(f"Failed to load user preferences: {e}")
    
    def save_user_preferences(self):
        """Save current quality preferences to file."""
        try:
            config_path = Path("config/quality_settings.json")
            config_path.parent.mkdir(exist_ok=True)
            
            user_prefs = {
                "quality_level": self.current_quality_level.value,
                "auto_adjust": self.auto_adjust,
                "hardware_tier": self.hardware_detector.hardware_tier.value,
                "timestamp": time.time()
            }
            
            with open(config_path, 'w') as f:
                json.dump(user_prefs, f, indent=2)
                
        except Exception as e:
            self.logger.warning(f"Failed to save user preferences: {e}")
    
    def start_frame(self):
        """Start frame timing."""
        self.profiler.start_frame()
    
    def end_frame(self):
        """End frame timing and potentially adjust quality."""
        self.profiler.end_frame()
        
        if self.auto_adjust:
            current_time = time.time()
            if current_time - self.last_adjustment_time >= self.adjustment_interval:
                self._evaluate_quality_adjustment()
                self.last_adjustment_time = current_time
    
    def _evaluate_quality_adjustment(self):
        """Evaluate whether quality should be adjusted."""
        current_fps = self.profiler.get_average_metric(PerformanceMetric.FPS)
        target_fps = self.current_settings.target_fps
        
        # Get 95th percentile frame time (worst 5% of frames)
        worst_frame_time = self.profiler.get_percentile_metric(PerformanceMetric.FRAME_TIME, 95)
        target_frame_time = 1.0 / target_fps
        
        performance_ratio = current_fps / target_fps
        
        # Determine if adjustment is needed
        if performance_ratio < 0.85:  # Performance is poor (below 85% of target)
            self._downgrade_quality()
        elif (performance_ratio > 1.1 and  # Performance is good (above 110% of target)
              worst_frame_time < target_frame_time * 0.8 and  # Even worst frames are fast
              self.profiler.is_performance_stable(target_fps * 1.1)):  # Performance is stable
            
            current_time = time.time()
            if self.last_stable_time == 0:
                self.last_stable_time = current_time
            elif current_time - self.last_stable_time >= self.stability_threshold:
                self._upgrade_quality()
                self.last_stable_time = 0
        else:
            self.last_stable_time = 0  # Reset stability timer
    
    def _downgrade_quality(self):
        """Downgrade to lower quality level."""
        quality_levels = list(QualityLevel)
        current_index = quality_levels.index(self.current_quality_level)
        
        if current_index < len(quality_levels) - 1:
            new_quality = quality_levels[current_index + 1]
            self._apply_quality_level(new_quality)
            self.logger.info(f"Quality downgraded to {new_quality.value} due to performance")
    
    def _upgrade_quality(self):
        """Upgrade to higher quality level."""
        quality_levels = list(QualityLevel)
        current_index = quality_levels.index(self.current_quality_level)
        
        if current_index > 0:
            new_quality = quality_levels[current_index - 1]
            self._apply_quality_level(new_quality)
            self.logger.info(f"Quality upgraded to {new_quality.value} due to good performance")
    
    def _apply_quality_level(self, quality_level: QualityLevel):
        """Apply new quality level."""
        old_level = self.current_quality_level
        self.current_quality_level = quality_level
        self.current_settings = self.preset_manager.get_preset(quality_level)
        
        # Notify callbacks
        for callback in self.quality_change_callbacks:
            try:
                callback(self.current_settings)
            except Exception as e:
                self.logger.error(f"Error in quality change callback: {e}")
        
        # Save preferences
        self.save_user_preferences()
    
    def set_quality_level(self, quality_level: QualityLevel, disable_auto_adjust: bool = False):
        """Manually set quality level."""
        if disable_auto_adjust:
            self.auto_adjust = False
        
        self._apply_quality_level(quality_level)
        self.logger.info(f"Quality manually set to {quality_level.value}")
    
    def add_quality_change_callback(self, callback: Callable[[QualitySettings], None]):
        """Add callback for quality changes."""
        self.quality_change_callbacks.append(callback)
    
    def record_draw_calls(self, count: int):
        """Record draw calls for performance tracking."""
        self.profiler.record_draw_calls(count)
    
    def record_particle_count(self, count: int):
        """Record particle count for performance tracking."""
        self.profiler.record_particle_count(count)
    
    def get_current_settings(self) -> QualitySettings:
        """Get current quality settings."""
        return self.current_settings
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        return {
            "current_quality_level": self.current_quality_level.value,
            "auto_adjust_enabled": self.auto_adjust,
            "hardware_info": self.hardware_detector.get_hardware_info(),
            "performance_stats": self.profiler.get_performance_summary(),
            "current_settings": self.current_settings.to_dict()
        }
    
    def optimize_for_screen(self, screen_name: str):
        """Apply screen-specific optimizations."""
        if screen_name in ["combat", "dynamic_combat"]:
            # Combat scenes are performance critical
            if not self.profiler.is_performance_stable(self.current_settings.target_fps):
                # Temporarily reduce particle count for combat
                pass
        elif screen_name == "menu":
            # Menu can afford higher quality
            pass
    
    def get_quality_recommendations(self) -> Dict[str, Any]:
        """Get quality recommendations based on current performance."""
        current_fps = self.profiler.get_average_metric(PerformanceMetric.FPS)
        target_fps = self.current_settings.target_fps
        
        recommendations = []
        
        if current_fps < target_fps * 0.9:
            recommendations.append("Consider reducing particle count")
            recommendations.append("Disable atmospheric effects")
            recommendations.append("Reduce texture quality")
        elif current_fps > target_fps * 1.2:
            recommendations.append("Can increase particle count")
            recommendations.append("Enable post-processing effects")
            recommendations.append("Increase texture quality")
        
        return {
            "current_performance_ratio": current_fps / target_fps,
            "recommendations": recommendations,
            "can_upgrade": current_fps > target_fps * 1.2,
            "should_downgrade": current_fps < target_fps * 0.85
        }


# Global quality manager
_global_quality_manager = None

def get_quality_manager(auto_adjust: bool = True) -> DynamicQualityManager:
    """Get global quality manager."""
    global _global_quality_manager
    if _global_quality_manager is None:
        _global_quality_manager = DynamicQualityManager(auto_adjust)
    return _global_quality_manager

def initialize_quality_system():
    """Initialize the dynamic quality system."""
    manager = get_quality_manager()
    manager.logger.info("Dynamic quality system initialized")
    return manager

def get_recommended_settings() -> QualitySettings:
    """Get recommended quality settings for current hardware."""
    manager = get_quality_manager()
    return manager.get_current_settings()

def apply_quality_to_systems(quality_settings: QualitySettings):
    """Apply quality settings to all visual systems."""
    # This would be called by the quality manager callbacks
    # to update particle systems, asset managers, etc.
    pass