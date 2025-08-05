#!/usr/bin/env python3
"""
Adaptive Performance Manager for Sands of Duat

Real-time performance monitoring and automatic quality adjustment system that maintains
smooth 60fps gameplay while maximizing visual quality based on hardware capabilities.
"""

import pygame
import time
import threading
import psutil
import platform
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import logging
import json
from pathlib import Path

try:
    import GPUtil
    GPU_MONITORING_AVAILABLE = True
except ImportError:
    GPU_MONITORING_AVAILABLE = False


class PerformanceProfile(Enum):
    """Hardware performance profiles"""
    POTATO = "potato"        # Very low-end hardware
    LOW_END = "low_end"      # Low-end hardware
    MID_RANGE = "mid_range"  # Mid-range hardware
    HIGH_END = "high_end"    # High-end hardware
    ENTHUSIAST = "enthusiast" # Top-tier hardware


class QualityPreset(Enum):
    """Visual quality presets"""
    MINIMAL = "minimal"      # Maximum performance
    LOW = "low"             # Performance priority
    MEDIUM = "medium"       # Balanced
    HIGH = "high"           # Quality priority
    ULTRA = "ultra"         # Maximum quality


@dataclass
class QualitySettings:
    """Comprehensive quality settings"""
    # Rendering
    render_scale: float = 1.0           # Global render scale
    texture_quality: float = 1.0       # Texture resolution scale
    parallax_layers: int = 5            # Number of parallax layers
    particle_density: float = 1.0      # Particle system density
    
    # Effects
    bloom_enabled: bool = True
    shadows_enabled: bool = True
    reflections_enabled: bool = True
    atmospheric_effects: bool = True
    screen_space_effects: bool = True
    
    # Animation
    animation_quality: float = 1.0     # Animation smoothness
    interpolation_enabled: bool = True
    motion_blur: bool = False
    
    # Performance
    culling_enabled: bool = True
    batching_enabled: bool = True
    caching_enabled: bool = True
    compression_enabled: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'render_scale': self.render_scale,
            'texture_quality': self.texture_quality,
            'parallax_layers': self.parallax_layers,
            'particle_density': self.particle_density,
            'bloom_enabled': self.bloom_enabled,
            'shadows_enabled': self.shadows_enabled,
            'reflections_enabled': self.reflections_enabled,
            'atmospheric_effects': self.atmospheric_effects,
            'screen_space_effects': self.screen_space_effects,
            'animation_quality': self.animation_quality,
            'interpolation_enabled': self.interpolation_enabled,
            'motion_blur': self.motion_blur,
            'culling_enabled': self.culling_enabled,
            'batching_enabled': self.batching_enabled,
            'caching_enabled': self.caching_enabled,
            'compression_enabled': self.compression_enabled
        }
    
    @classmethod
    def from_preset(cls, preset: QualityPreset) -> 'QualitySettings':
        """Create settings from preset"""
        presets = {
            QualityPreset.MINIMAL: cls(
                render_scale=0.5, texture_quality=0.5, parallax_layers=2,
                particle_density=0.3, bloom_enabled=False, shadows_enabled=False,
                reflections_enabled=False, atmospheric_effects=False,
                screen_space_effects=False, animation_quality=0.7,
                interpolation_enabled=False, motion_blur=False,
                compression_enabled=True
            ),
            QualityPreset.LOW: cls(
                render_scale=0.75, texture_quality=0.7, parallax_layers=3,
                particle_density=0.5, bloom_enabled=False, shadows_enabled=True,
                reflections_enabled=False, atmospheric_effects=True,
                screen_space_effects=False, animation_quality=0.8,
                interpolation_enabled=True, motion_blur=False,
                compression_enabled=True
            ),
            QualityPreset.MEDIUM: cls(
                render_scale=0.9, texture_quality=0.85, parallax_layers=4,
                particle_density=0.75, bloom_enabled=True, shadows_enabled=True,
                reflections_enabled=True, atmospheric_effects=True,
                screen_space_effects=True, animation_quality=0.9,
                interpolation_enabled=True, motion_blur=False,
                compression_enabled=False
            ),
            QualityPreset.HIGH: cls(
                render_scale=1.0, texture_quality=1.0, parallax_layers=5,
                particle_density=1.0, bloom_enabled=True, shadows_enabled=True,
                reflections_enabled=True, atmospheric_effects=True,
                screen_space_effects=True, animation_quality=1.0,
                interpolation_enabled=True, motion_blur=True
            ),
            QualityPreset.ULTRA: cls(
                render_scale=1.2, texture_quality=1.2, parallax_layers=6,
                particle_density=1.5, bloom_enabled=True, shadows_enabled=True,
                reflections_enabled=True, atmospheric_effects=True,
                screen_space_effects=True, animation_quality=1.0,
                interpolation_enabled=True, motion_blur=True
            )
        }
        return presets.get(preset, presets[QualityPreset.MEDIUM])


@dataclass
class PerformanceMetrics:
    """Real-time performance metrics"""
    # Core metrics
    fps: float = 60.0
    frame_time_ms: float = 16.67
    target_fps: float = 60.0
    
    # System resources
    cpu_usage: float = 0.0
    memory_usage_mb: float = 0.0
    memory_available_mb: float = 0.0
    gpu_usage: float = 0.0
    gpu_memory_mb: float = 0.0
    
    # Game-specific metrics
    draw_calls: int = 0
    triangles: int = 0
    texture_switches: int = 0
    
    # Historical data
    fps_history: deque = field(default_factory=lambda: deque(maxlen=300))      # 5 seconds at 60fps
    frame_time_history: deque = field(default_factory=lambda: deque(maxlen=300))
    
    def update(self, fps: float, frame_time_ms: float):
        """Update metrics with new measurements"""
        self.fps = fps
        self.frame_time_ms = frame_time_ms
        
        self.fps_history.append(fps)
        self.frame_time_history.append(frame_time_ms)
    
    @property
    def average_fps(self) -> float:
        """Average FPS over recent history"""
        if not self.fps_history:
            return self.target_fps
        return sum(self.fps_history) / len(self.fps_history)
    
    @property
    def fps_stability(self) -> float:
        """FPS stability (0-1, 1 = perfectly stable)"""
        if len(self.fps_history) < 10:
            return 1.0
        
        avg = self.average_fps
        variance = sum((fps - avg) ** 2 for fps in self.fps_history) / len(self.fps_history)
        return max(0.0, 1.0 - (variance / (self.target_fps ** 2)))
    
    @property
    def performance_score(self) -> float:
        """Overall performance score (0-1)"""
        fps_score = min(1.0, self.average_fps / self.target_fps)
        stability_score = self.fps_stability
        return (fps_score * 0.7) + (stability_score * 0.3)


class HardwareProfiler:
    """Hardware detection and profiling system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_info = self._gather_system_info()
        self.performance_profile = self._determine_performance_profile()
    
    def _gather_system_info(self) -> Dict[str, Any]:
        """Gather comprehensive system information"""
        info = {
            'platform': platform.system(),
            'cpu_count': psutil.cpu_count(),
            'cpu_freq_max': psutil.cpu_freq().max if psutil.cpu_freq() else 0,
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'python_version': platform.python_version(),
            'pygame_version': pygame.version.ver
        }
        
        # GPU information
        if GPU_MONITORING_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Primary GPU
                    info['gpu_name'] = gpu.name
                    info['gpu_memory_mb'] = gpu.memoryTotal
                    info['gpu_driver'] = gpu.driver
                else:
                    info['gpu_name'] = 'Unknown'
                    info['gpu_memory_mb'] = 0
            except Exception as e:
                self.logger.warning(f"Failed to get GPU info: {e}")
                info['gpu_name'] = 'Unknown'
                info['gpu_memory_mb'] = 0
        else:
            info['gpu_name'] = 'Unknown'
            info['gpu_memory_mb'] = 0
        
        return info
    
    def _determine_performance_profile(self) -> PerformanceProfile:
        """Determine hardware performance profile"""
        # Score based on hardware specs
        score = 0
        
        # CPU scoring
        cpu_cores = self.system_info.get('cpu_count', 1)
        cpu_freq = self.system_info.get('cpu_freq_max', 0)
        
        if cpu_cores >= 8 and cpu_freq >= 3000:
            score += 40
        elif cpu_cores >= 6 and cpu_freq >= 2500:
            score += 30
        elif cpu_cores >= 4 and cpu_freq >= 2000:
            score += 20
        else:
            score += 10
        
        # Memory scoring
        memory_gb = self.system_info.get('memory_total_gb', 0)
        if memory_gb >= 16:
            score += 30
        elif memory_gb >= 8:
            score += 20
        elif memory_gb >= 4:
            score += 10
        else:
            score += 5
        
        # GPU scoring (simplified)
        gpu_memory = self.system_info.get('gpu_memory_mb', 0)
        if gpu_memory >= 8000:  # 8GB+ GPU
            score += 30
        elif gpu_memory >= 4000:  # 4GB+ GPU
            score += 20
        elif gpu_memory >= 2000:  # 2GB+ GPU
            score += 10
        else:
            score += 5
        
        # Determine profile based on score
        if score >= 90:
            return PerformanceProfile.ENTHUSIAST
        elif score >= 70:
            return PerformanceProfile.HIGH_END
        elif score >= 50:
            return PerformanceProfile.MID_RANGE
        elif score >= 30:
            return PerformanceProfile.LOW_END
        else:
            return PerformanceProfile.POTATO
    
    def get_recommended_quality_preset(self) -> QualityPreset:
        """Get recommended quality preset for this hardware"""
        profile_to_preset = {
            PerformanceProfile.ENTHUSIAST: QualityPreset.ULTRA,
            PerformanceProfile.HIGH_END: QualityPreset.HIGH,
            PerformanceProfile.MID_RANGE: QualityPreset.MEDIUM,
            PerformanceProfile.LOW_END: QualityPreset.LOW,
            PerformanceProfile.POTATO: QualityPreset.MINIMAL
        }
        return profile_to_preset[self.performance_profile]


class PerformanceMonitor:
    """Real-time performance monitoring system"""
    
    def __init__(self, target_fps: float = 60.0, monitoring_interval: float = 0.1):
        self.target_fps = target_fps
        self.monitoring_interval = monitoring_interval
        
        self.metrics = PerformanceMetrics(target_fps=target_fps)
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.last_time = time.time()
        self.frame_count = 0
        self.last_fps_update = time.time()
        
        # Background monitoring
        self.monitoring_thread = None
        self.monitoring_active = False
        
        # Performance callbacks
        self.fps_callbacks: List[Callable[[float], None]] = []
        self.performance_callbacks: List[Callable[[PerformanceMetrics], None]] = []
    
    def start_monitoring(self):
        """Start background performance monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop background performance monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
        self.logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                self._update_system_metrics()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
    
    def _update_system_metrics(self):
        """Update system resource metrics"""
        # CPU usage
        self.metrics.cpu_usage = psutil.cpu_percent(interval=None)
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.metrics.memory_usage_mb = (memory.total - memory.available) / (1024 * 1024)
        self.metrics.memory_available_mb = memory.available / (1024 * 1024)
        
        # GPU usage (if available)
        if GPU_MONITORING_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    self.metrics.gpu_usage = gpu.load * 100
                    self.metrics.gpu_memory_mb = gpu.memoryUsed
            except Exception:
                pass  # GPU monitoring not critical
    
    def update_frame_metrics(self, dt: float):
        """Update frame-based metrics (call once per frame)"""
        current_time = time.time()
        self.frame_count += 1
        
        # Update FPS every second
        time_since_update = current_time - self.last_fps_update
        if time_since_update >= 1.0:
            fps = self.frame_count / time_since_update
            frame_time_ms = (time_since_update / self.frame_count) * 1000
            
            self.metrics.update(fps, frame_time_ms)
            
            # Reset counters
            self.frame_count = 0
            self.last_fps_update = current_time
            
            # Notify callbacks
            for callback in self.fps_callbacks:
                try:
                    callback(fps)
                except Exception as e:
                    self.logger.error(f"Error in FPS callback: {e}")
            
            for callback in self.performance_callbacks:
                try:
                    callback(self.metrics)
                except Exception as e:
                    self.logger.error(f"Error in performance callback: {e}")
    
    def add_fps_callback(self, callback: Callable[[float], None]):
        """Add callback for FPS updates"""
        self.fps_callbacks.append(callback)
    
    def add_performance_callback(self, callback: Callable[[PerformanceMetrics], None]):
        """Add callback for performance metric updates"""
        self.performance_callbacks.append(callback)


class AdaptiveQualityController:
    """Adaptive quality adjustment controller"""
    
    def __init__(self, target_fps: float = 60.0, adjustment_sensitivity: float = 1.0):
        self.target_fps = target_fps
        self.adjustment_sensitivity = adjustment_sensitivity
        self.logger = logging.getLogger(__name__)
        
        # Current state
        self.current_settings = QualitySettings.from_preset(QualityPreset.MEDIUM)
        self.adaptive_mode = True
        self.user_locked = False
        
        # Adjustment parameters
        self.adjustment_cooldown = 3.0  # Seconds between adjustments
        self.last_adjustment = 0.0
        self.fps_threshold_low = target_fps * 0.85  # Reduce quality below this
        self.fps_threshold_high = target_fps * 0.95  # Increase quality above this
        self.stability_threshold = 0.8  # Minimum stability required
        
        # Quality adjustment callbacks
        self.quality_callbacks: List[Callable[[QualitySettings], None]] = []
        
        # Performance history for trend analysis
        self.performance_trend: deque = deque(maxlen=10)
    
    def set_adaptive_mode(self, enabled: bool):
        """Enable/disable adaptive quality adjustment"""
        self.adaptive_mode = enabled
        self.logger.info(f"Adaptive quality {'enabled' if enabled else 'disabled'}")
    
    def set_quality_preset(self, preset: QualityPreset, lock: bool = False):
        """Set quality preset manually"""
        self.current_settings = QualitySettings.from_preset(preset)
        self.user_locked = lock
        
        self._notify_quality_change()
        self.logger.info(f"Quality set to {preset.value} (locked: {lock})")
    
    def update_quality(self, metrics: PerformanceMetrics) -> bool:
        """Update quality based on performance metrics"""
        if not self.adaptive_mode or self.user_locked:
            return False
        
        current_time = time.time()
        
        # Don't adjust too frequently
        if current_time - self.last_adjustment < self.adjustment_cooldown:
            return False
        
        # Add current performance to trend
        self.performance_trend.append(metrics.performance_score)
        
        # Need enough data for trend analysis
        if len(self.performance_trend) < 5:
            return False
        
        # Analyze performance trend
        avg_performance = sum(self.performance_trend) / len(self.performance_trend)
        fps_stable = metrics.fps_stability >= self.stability_threshold
        
        # Determine if adjustment is needed
        adjustment_made = False
        
        if metrics.average_fps < self.fps_threshold_low or not fps_stable:
            # Performance is poor, reduce quality
            if self._reduce_quality():
                adjustment_made = True
                self.logger.info(f"Reduced quality due to poor performance "
                               f"(FPS: {metrics.average_fps:.1f}, Stability: {metrics.fps_stability:.2f})")
        
        elif (metrics.average_fps > self.fps_threshold_high and 
              fps_stable and avg_performance > 0.9):
            # Performance is excellent, try to increase quality
            if self._increase_quality():
                adjustment_made = True
                self.logger.info(f"Increased quality due to excellent performance "
                               f"(FPS: {metrics.average_fps:.1f}, Stability: {metrics.fps_stability:.2f})")
        
        if adjustment_made:
            self.last_adjustment = current_time
            self._notify_quality_change()
        
        return adjustment_made
    
    def _reduce_quality(self) -> bool:
        """Reduce quality settings"""
        settings = self.current_settings
        adjusted = False
        
        # Reduce in priority order (most impactful first)
        if settings.render_scale > 0.5:
            settings.render_scale = max(0.5, settings.render_scale - 0.1)
            adjusted = True
        elif settings.parallax_layers > 2:
            settings.parallax_layers = max(2, settings.parallax_layers - 1)
            adjusted = True
        elif settings.particle_density > 0.3:
            settings.particle_density = max(0.3, settings.particle_density - 0.2)
            adjusted = True
        elif settings.texture_quality > 0.5:
            settings.texture_quality = max(0.5, settings.texture_quality - 0.1)
            adjusted = True
        elif settings.screen_space_effects:
            settings.screen_space_effects = False
            adjusted = True
        elif settings.bloom_enabled:
            settings.bloom_enabled = False
            adjusted = True
        elif settings.reflections_enabled:
            settings.reflections_enabled = False
            adjusted = True
        elif settings.shadows_enabled:
            settings.shadows_enabled = False
            adjusted = True
        elif not settings.compression_enabled:
            settings.compression_enabled = True
            adjusted = True
        
        return adjusted
    
    def _increase_quality(self) -> bool:
        """Increase quality settings"""
        settings = self.current_settings
        adjusted = False
        
        # Increase in reverse priority order
        if settings.compression_enabled:
            settings.compression_enabled = False
            adjusted = True
        elif not settings.shadows_enabled:
            settings.shadows_enabled = True
            adjusted = True
        elif not settings.reflections_enabled:
            settings.reflections_enabled = True
            adjusted = True
        elif not settings.bloom_enabled:
            settings.bloom_enabled = True
            adjusted = True
        elif not settings.screen_space_effects:
            settings.screen_space_effects = True
            adjusted = True
        elif settings.texture_quality < 1.0:
            settings.texture_quality = min(1.0, settings.texture_quality + 0.1)
            adjusted = True
        elif settings.particle_density < 1.0:
            settings.particle_density = min(1.0, settings.particle_density + 0.2)
            adjusted = True
        elif settings.parallax_layers < 5:
            settings.parallax_layers = min(5, settings.parallax_layers + 1)
            adjusted = True
        elif settings.render_scale < 1.0:
            settings.render_scale = min(1.0, settings.render_scale + 0.1)
            adjusted = True
        
        return adjusted
    
    def _notify_quality_change(self):
        """Notify callbacks of quality changes"""
        for callback in self.quality_callbacks:
            try:
                callback(self.current_settings)
            except Exception as e:
                self.logger.error(f"Error in quality callback: {e}")
    
    def add_quality_callback(self, callback: Callable[[QualitySettings], None]):
        """Add callback for quality changes"""
        self.quality_callbacks.append(callback)


class AdaptivePerformanceManager:
    """Main adaptive performance management system"""
    
    def __init__(self, target_fps: float = 60.0, config_file: Optional[str] = None):
        self.target_fps = target_fps
        self.config_file = Path(config_file) if config_file else None
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.hardware_profiler = HardwareProfiler()
        self.performance_monitor = PerformanceMonitor(target_fps)
        self.quality_controller = AdaptiveQualityController(target_fps)
        
        # State
        self.initialized = False
        self.user_preferences = {}
        
        # Load user preferences
        self._load_preferences()
        
        # Connect components
        self.performance_monitor.add_performance_callback(
            self.quality_controller.update_quality
        )
        
        self.logger.info("Adaptive Performance Manager initialized")
    
    def initialize(self, auto_detect: bool = True):
        """Initialize the performance manager"""
        if self.initialized:
            return
        
        # Auto-detect optimal settings if requested
        if auto_detect:
            recommended_preset = self.hardware_profiler.get_recommended_quality_preset()
            self.quality_controller.set_quality_preset(recommended_preset)
            self.logger.info(f"Auto-detected hardware profile: {self.hardware_profiler.performance_profile.value}")
            self.logger.info(f"Recommended quality preset: {recommended_preset.value}")
        
        # Start performance monitoring
        self.performance_monitor.start_monitoring()
        
        self.initialized = True
        self.logger.info("Adaptive Performance Manager ready")
    
    def update(self, dt: float):
        """Update performance manager (call once per frame)"""
        if not self.initialized:
            return
        
        self.performance_monitor.update_frame_metrics(dt)
    
    def get_current_quality_settings(self) -> QualitySettings:
        """Get current quality settings"""
        return self.quality_controller.current_settings
    
    def set_quality_preset(self, preset: QualityPreset, lock: bool = False):
        """Set quality preset"""
        self.quality_controller.set_quality_preset(preset, lock)
        
        # Save user preference
        self.user_preferences['quality_preset'] = preset.value
        self.user_preferences['quality_locked'] = lock
        self._save_preferences()
    
    def set_adaptive_mode(self, enabled: bool):
        """Enable/disable adaptive quality"""
        self.quality_controller.set_adaptive_mode(enabled)
        
        # Save user preference
        self.user_preferences['adaptive_mode'] = enabled
        self._save_preferences()
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        return self.performance_monitor.metrics
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get hardware information"""
        return self.hardware_profiler.system_info
    
    def add_quality_callback(self, callback: Callable[[QualitySettings], None]):
        """Add callback for quality changes"""
        self.quality_controller.add_quality_callback(callback)
    
    def add_fps_callback(self, callback: Callable[[float], None]):
        """Add callback for FPS updates"""
        self.performance_monitor.add_fps_callback(callback)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary"""
        metrics = self.performance_monitor.metrics
        settings = self.quality_controller.current_settings
        
        return {
            'performance': {
                'fps': metrics.fps,
                'average_fps': metrics.average_fps,
                'stability': metrics.fps_stability,
                'performance_score': metrics.performance_score,
                'cpu_usage': metrics.cpu_usage,
                'memory_usage_mb': metrics.memory_usage_mb
            },
            'quality': {
                'preset_equivalent': self._determine_current_preset(),
                'adaptive_mode': self.quality_controller.adaptive_mode,
                'user_locked': self.quality_controller.user_locked,
                'settings': settings.to_dict()
            },
            'hardware': {
                'profile': self.hardware_profiler.performance_profile.value,
                'cpu_cores': self.hardware_profiler.system_info.get('cpu_count'),
                'memory_gb': round(self.hardware_profiler.system_info.get('memory_total_gb', 0), 1),
                'gpu_name': self.hardware_profiler.system_info.get('gpu_name', 'Unknown')
            }
        }
    
    def _determine_current_preset(self) -> str:
        """Determine which preset best matches current settings"""
        current = self.quality_controller.current_settings
        
        presets = [
            (QualityPreset.MINIMAL, QualitySettings.from_preset(QualityPreset.MINIMAL)),
            (QualityPreset.LOW, QualitySettings.from_preset(QualityPreset.LOW)),
            (QualityPreset.MEDIUM, QualitySettings.from_preset(QualityPreset.MEDIUM)),
            (QualityPreset.HIGH, QualitySettings.from_preset(QualityPreset.HIGH)),
            (QualityPreset.ULTRA, QualitySettings.from_preset(QualityPreset.ULTRA))
        ]
        
        best_match = QualityPreset.MEDIUM
        best_distance = float('inf')
        
        for preset, settings in presets:
            # Calculate "distance" between current and preset settings
            distance = (
                abs(current.render_scale - settings.render_scale) +
                abs(current.texture_quality - settings.texture_quality) +
                abs(current.parallax_layers - settings.parallax_layers) +
                abs(current.particle_density - settings.particle_density)
            )
            
            if distance < best_distance:
                best_distance = distance
                best_match = preset
        
        return best_match.value
    
    def _load_preferences(self):
        """Load user preferences from file"""
        if not self.config_file or not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                self.user_preferences = json.load(f)
            self.logger.info("User preferences loaded")
        except Exception as e:
            self.logger.warning(f"Failed to load preferences: {e}")
            self.user_preferences = {}
    
    def _save_preferences(self):
        """Save user preferences to file"""
        if not self.config_file:
            return
        
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
            self.logger.debug("User preferences saved")
        except Exception as e:
            self.logger.warning(f"Failed to save preferences: {e}")
    
    def shutdown(self):
        """Clean shutdown"""
        if self.initialized:
            self.performance_monitor.stop_monitoring()
            self._save_preferences()
            self.logger.info("Adaptive Performance Manager shutdown")


# Global instance
_global_performance_manager = None

def get_performance_manager() -> AdaptivePerformanceManager:
    """Get global performance manager"""
    global _global_performance_manager
    if _global_performance_manager is None:
        config_path = Path("config/performance_preferences.json")
        _global_performance_manager = AdaptivePerformanceManager(config_file=str(config_path))
    return _global_performance_manager

def initialize_performance_system(target_fps: float = 60.0, auto_detect: bool = True) -> AdaptivePerformanceManager:
    """Initialize the adaptive performance system"""
    manager = get_performance_manager()
    manager.initialize(auto_detect)
    return manager