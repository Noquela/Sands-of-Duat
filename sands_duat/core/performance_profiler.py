"""
Performance Profiler for Sands of Duat
Comprehensive performance monitoring and optimization toolkit.
"""

import time
import statistics
import pygame
import psutil
import gc
import cProfile
import pstats
import io
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from contextlib import contextmanager
from pathlib import Path
import json
import threading
from collections import defaultdict, deque


@dataclass
class PerformanceMetric:
    """Individual performance measurement."""
    name: str
    duration_ms: float
    timestamp: float
    memory_usage_mb: float
    gpu_usage_percent: float = 0.0
    custom_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FrameProfile:
    """Complete profile data for a single frame."""
    frame_number: int
    total_frame_time_ms: float
    update_time_ms: float
    render_time_ms: float
    particle_time_ms: float
    theme_time_ms: float
    asset_time_ms: float
    memory_usage_mb: float
    particle_count: int
    draw_calls: int
    timestamp: float


class PerformanceProfiler:
    """
    Advanced performance profiler for game optimization.
    
    Features:
    - Real-time frame timing analysis
    - Memory usage tracking
    - Particle system optimization
    - Theme rendering profiling
    - Asset loading performance
    - Statistical analysis and reporting
    """
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_samples))
        self.frame_profiles: deque = deque(maxlen=max_samples)
        self.current_frame = 0
        self.start_time = time.time()
        
        # Performance tracking
        self.active_timers: Dict[str, float] = {}
        self.memory_baseline = self._get_memory_usage()
        
        # Frame timing
        self.frame_start_time = 0.0
        self.last_frame_time = 0.0
        self.target_fps = 60
        self.frame_budget_ms = 1000.0 / self.target_fps
        
        # Particle system tracking
        self.particle_counts = deque(maxlen=max_samples)
        
        # Threading for background profiling
        self._stop_profiling = threading.Event()
        self._profiling_thread: Optional[threading.Thread] = None
        
        # Asset loading tracking
        self.asset_load_times: Dict[str, float] = {}
        
        # GPU memory estimation (if available)
        self.estimated_gpu_memory_mb = 0.0
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def _get_gpu_usage(self) -> float:
        """Estimate GPU usage (placeholder for actual GPU monitoring)."""
        # This would require nvidia-ml-py or similar for real GPU monitoring
        # For now, return estimated usage based on rendering complexity
        return min(100.0, self.estimated_gpu_memory_mb / 1024 * 100)
    
    @contextmanager
    def time_operation(self, operation_name: str, custom_data: Optional[Dict] = None):
        """Context manager for timing operations."""
        start_time = time.perf_counter()
        start_memory = self._get_memory_usage()
        
        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = self._get_memory_usage()
            
            duration_ms = (end_time - start_time) * 1000
            metric = PerformanceMetric(
                name=operation_name,
                duration_ms=duration_ms,
                timestamp=time.time(),
                memory_usage_mb=end_memory,
                gpu_usage_percent=self._get_gpu_usage(),
                custom_data=custom_data or {}
            )
            
            self.metrics[operation_name].append(metric)
    
    def start_frame(self):
        """Mark the start of a new frame."""
        self.frame_start_time = time.perf_counter()
        self.current_frame += 1
    
    def end_frame(self, particle_count: int = 0, draw_calls: int = 0):
        """Mark the end of a frame and calculate metrics."""
        frame_end_time = time.perf_counter()
        total_frame_time = (frame_end_time - self.frame_start_time) * 1000
        
        # Get component timing from metrics
        update_time = self._get_last_metric_duration("update") or 0.0
        render_time = self._get_last_metric_duration("render") or 0.0
        particle_time = self._get_last_metric_duration("particles") or 0.0
        theme_time = self._get_last_metric_duration("hades_theme") or 0.0
        asset_time = self._get_last_metric_duration("asset_loading") or 0.0
        
        profile = FrameProfile(
            frame_number=self.current_frame,
            total_frame_time_ms=total_frame_time,
            update_time_ms=update_time,
            render_time_ms=render_time,
            particle_time_ms=particle_time,
            theme_time_ms=theme_time,
            asset_time_ms=asset_time,
            memory_usage_mb=self._get_memory_usage(),
            particle_count=particle_count,
            draw_calls=draw_calls,
            timestamp=time.time()
        )
        
        self.frame_profiles.append(profile)
        self.particle_counts.append(particle_count)
        self.last_frame_time = total_frame_time
    
    def _get_last_metric_duration(self, metric_name: str) -> Optional[float]:
        """Get the duration of the last metric with the given name."""
        if metric_name in self.metrics and self.metrics[metric_name]:
            return self.metrics[metric_name][-1].duration_ms
        return None
    
    def profile_particle_system(self, particle_system) -> Dict[str, Any]:
        """Profile particle system performance."""
        with self.time_operation("particles") as timer:
            if hasattr(particle_system, 'get_particle_count'):
                particle_count = particle_system.get_particle_count()
            else:
                particle_count = 0
            
            # Estimate GPU memory usage for particles
            estimated_particle_memory = particle_count * 0.1  # 0.1 KB per particle estimate
            self.estimated_gpu_memory_mb += estimated_particle_memory / 1024
            
            return {
                "particle_count": particle_count,
                "estimated_memory_kb": estimated_particle_memory
            }
    
    def profile_hades_theme(self, theme_operations: List[Callable]) -> Dict[str, Any]:
        """Profile Hades theme rendering operations."""
        operation_times = {}
        
        with self.time_operation("hades_theme") as timer:
            for i, operation in enumerate(theme_operations):
                op_name = f"theme_op_{i}"
                op_start = time.perf_counter()
                
                try:
                    result = operation()
                    op_end = time.perf_counter()
                    operation_times[op_name] = (op_end - op_start) * 1000
                except Exception as e:
                    operation_times[op_name] = {"error": str(e)}
        
        return operation_times
    
    def profile_asset_loading(self, asset_path: str, load_function: Callable) -> Any:
        """Profile asset loading performance."""
        with self.time_operation("asset_loading", {"asset": asset_path}) as timer:
            start_time = time.perf_counter()
            result = load_function()
            end_time = time.perf_counter()
            
            load_time = (end_time - start_time) * 1000
            self.asset_load_times[asset_path] = load_time
            
            # Estimate asset memory usage
            if hasattr(result, 'get_size') and callable(result.get_size):
                try:
                    size = result.get_size()
                    memory_estimate = (size[0] * size[1] * 4) / 1024 / 1024  # RGBA estimate
                    self.estimated_gpu_memory_mb += memory_estimate
                except:
                    pass
            
            return result
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.frame_profiles:
            return {"error": "No frame data available"}
        
        # Frame timing analysis
        frame_times = [f.total_frame_time_ms for f in self.frame_profiles]
        fps_values = [1000.0 / ft if ft > 0 else 0 for ft in frame_times]
        
        # Component timing analysis
        update_times = [f.update_time_ms for f in self.frame_profiles if f.update_time_ms]
        render_times = [f.render_time_ms for f in self.frame_profiles if f.render_time_ms]
        particle_times = [f.particle_time_ms for f in self.frame_profiles if f.particle_time_ms]
        theme_times = [f.theme_time_ms for f in self.frame_profiles if f.theme_time_ms]
        
        # Memory analysis
        memory_values = [f.memory_usage_mb for f in self.frame_profiles]
        particle_counts = [f.particle_count for f in self.frame_profiles]
        
        summary = {
            "session_info": {
                "duration_seconds": time.time() - self.start_time,
                "total_frames": self.current_frame,
                "target_fps": self.target_fps,
                "frame_budget_ms": self.frame_budget_ms
            },
            "frame_performance": {
                "avg_fps": statistics.mean(fps_values) if fps_values else 0,
                "min_fps": min(fps_values) if fps_values else 0,
                "max_fps": max(fps_values) if fps_values else 0,
                "fps_95th_percentile": self._percentile(fps_values, 0.95) if fps_values else 0,
                "avg_frame_time_ms": statistics.mean(frame_times) if frame_times else 0,
                "frame_time_std_ms": statistics.stdev(frame_times) if len(frame_times) > 1 else 0,
                "frames_over_budget": sum(1 for ft in frame_times if ft > self.frame_budget_ms),
                "budget_violation_rate": sum(1 for ft in frame_times if ft > self.frame_budget_ms) / len(frame_times) if frame_times else 0
            },
            "component_performance": {
                "update": self._analyze_component_times(update_times),
                "render": self._analyze_component_times(render_times),
                "particles": self._analyze_component_times(particle_times),
                "hades_theme": self._analyze_component_times(theme_times)
            },
            "memory_analysis": {
                "baseline_mb": self.memory_baseline,
                "current_mb": self._get_memory_usage(),
                "avg_usage_mb": statistics.mean(memory_values) if memory_values else 0,
                "peak_usage_mb": max(memory_values) if memory_values else 0,
                "estimated_gpu_mb": self.estimated_gpu_memory_mb
            },
            "particle_analysis": {
                "avg_count": statistics.mean(particle_counts) if particle_counts else 0,
                "max_count": max(particle_counts) if particle_counts else 0,
                "particle_performance_impact": self._analyze_particle_impact()
            },
            "asset_performance": {
                "total_assets_loaded": len(self.asset_load_times),
                "avg_load_time_ms": statistics.mean(self.asset_load_times.values()) if self.asset_load_times else 0,
                "slowest_assets": self._get_slowest_assets(5)
            }
        }
        
        return summary
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(percentile * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def _analyze_component_times(self, times: List[float]) -> Dict[str, float]:
        """Analyze timing data for a component."""
        if not times:
            return {"avg_ms": 0, "max_ms": 0, "std_ms": 0, "budget_percent": 0}
        
        avg_time = statistics.mean(times)
        return {
            "avg_ms": avg_time,
            "max_ms": max(times),
            "std_ms": statistics.stdev(times) if len(times) > 1 else 0,
            "budget_percent": (avg_time / self.frame_budget_ms) * 100
        }
    
    def _analyze_particle_impact(self) -> Dict[str, Any]:
        """Analyze performance impact of particles."""
        if not self.frame_profiles or not self.particle_counts:
            return {"correlation": 0, "impact": "unknown"}
        
        # Calculate correlation between particle count and frame time
        frame_times = [f.total_frame_time_ms for f in self.frame_profiles[-len(self.particle_counts):]]
        
        if len(frame_times) >= len(self.particle_counts):
            # Simple correlation calculation
            correlation = self._calculate_correlation(list(self.particle_counts), frame_times[:len(self.particle_counts)])
            
            impact_level = "low"
            if correlation > 0.7:
                impact_level = "high"
            elif correlation > 0.4:
                impact_level = "medium"
            
            return {
                "correlation": correlation,
                "impact": impact_level,
                "avg_particles": statistics.mean(self.particle_counts),
                "max_particles": max(self.particle_counts)
            }
        
        return {"correlation": 0, "impact": "insufficient_data"}
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _get_slowest_assets(self, count: int) -> List[Tuple[str, float]]:
        """Get the slowest loading assets."""
        if not self.asset_load_times:
            return []
        
        sorted_assets = sorted(self.asset_load_times.items(), key=lambda x: x[1], reverse=True)
        return sorted_assets[:count]
    
    def generate_optimization_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations."""
        summary = self.get_performance_summary()
        recommendations = []
        
        # Frame rate analysis
        frame_perf = summary.get("frame_performance", {})
        avg_fps = frame_perf.get("avg_fps", 0)
        budget_violation_rate = frame_perf.get("budget_violation_rate", 0)
        
        if avg_fps < 50:
            recommendations.append("CRITICAL: Average FPS below 50. Immediate optimization required.")
        elif avg_fps < 55:
            recommendations.append("WARNING: Average FPS below target. Performance optimization recommended.")
        
        if budget_violation_rate > 0.1:
            recommendations.append(f"Frame budget exceeded in {budget_violation_rate*100:.1f}% of frames. Optimize critical path.")
        
        # Component analysis
        components = summary.get("component_performance", {})
        for component, stats in components.items():
            if stats.get("budget_percent", 0) > 30:
                recommendations.append(f"OPTIMIZE: {component} using {stats['budget_percent']:.1f}% of frame budget")
        
        # Particle system analysis
        particle_analysis = summary.get("particle_analysis", {})
        max_particles = particle_analysis.get("max_particles", 0)
        if max_particles > 1000:
            recommendations.append("Consider particle pooling or LOD system for high particle counts")
        
        # Memory analysis
        memory = summary.get("memory_analysis", {})
        gpu_memory = memory.get("estimated_gpu_mb", 0)
        if gpu_memory > 512:
            recommendations.append("High GPU memory usage detected. Consider texture compression or LOD")
        
        # Asset loading analysis
        asset_perf = summary.get("asset_performance", {})
        avg_load_time = asset_perf.get("avg_load_time_ms", 0)
        if avg_load_time > 50:
            recommendations.append("Slow asset loading detected. Implement asset caching or background loading")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable parameters. Continue monitoring.")
        
        return recommendations
    
    def export_profile_data(self, filepath: str, include_detailed: bool = False):
        """Export profile data to JSON file."""
        data = {
            "summary": self.get_performance_summary(),
            "recommendations": self.generate_optimization_recommendations(),
            "export_timestamp": time.time()
        }
        
        if include_detailed:
            data["detailed_frames"] = [
                {
                    "frame": f.frame_number,
                    "total_ms": f.total_frame_time_ms,
                    "update_ms": f.update_time_ms,
                    "render_ms": f.render_time_ms,
                    "particles": f.particle_count,
                    "memory_mb": f.memory_usage_mb
                } for f in list(self.frame_profiles)[-100:]  # Last 100 frames
            ]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def start_continuous_profiling(self, interval: float = 1.0):
        """Start background profiling thread."""
        if self._profiling_thread and self._profiling_thread.is_alive():
            return
        
        self._stop_profiling.clear()
        self._profiling_thread = threading.Thread(
            target=self._continuous_profiling_loop,
            args=(interval,),
            daemon=True
        )
        self._profiling_thread.start()
    
    def stop_continuous_profiling(self):
        """Stop background profiling thread."""
        self._stop_profiling.set()
        if self._profiling_thread:
            self._profiling_thread.join(timeout=5.0)
    
    def _continuous_profiling_loop(self, interval: float):
        """Background profiling loop."""
        while not self._stop_profiling.wait(interval):
            # Collect system metrics
            memory_usage = self._get_memory_usage()
            
            # Store continuous metrics
            metric = PerformanceMetric(
                name="system_monitoring",
                duration_ms=0,
                timestamp=time.time(),
                memory_usage_mb=memory_usage,
                gpu_usage_percent=self._get_gpu_usage()
            )
            
            self.metrics["system_monitoring"].append(metric)
            
            # Trigger garbage collection periodically to prevent memory buildup
            if self.current_frame % 1800 == 0:  # Every 30 seconds at 60fps
                gc.collect()


# Global profiler instance
_global_profiler: Optional[PerformanceProfiler] = None


def get_profiler() -> PerformanceProfiler:
    """Get or create the global profiler instance."""
    global _global_profiler
    if _global_profiler is None:
        _global_profiler = PerformanceProfiler()
    return _global_profiler


def initialize_profiler(max_samples: int = 1000) -> PerformanceProfiler:
    """Initialize the global profiler."""
    global _global_profiler
    _global_profiler = PerformanceProfiler(max_samples)
    return _global_profiler


@contextmanager
def profile_operation(operation_name: str, custom_data: Optional[Dict] = None):
    """Convenience context manager for profiling operations."""
    profiler = get_profiler()
    with profiler.time_operation(operation_name, custom_data):
        yield


def profile_frame_start():
    """Mark frame start for profiling."""
    get_profiler().start_frame()


def profile_frame_end(particle_count: int = 0, draw_calls: int = 0):
    """Mark frame end for profiling."""
    get_profiler().end_frame(particle_count, draw_calls)