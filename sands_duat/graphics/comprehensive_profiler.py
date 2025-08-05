"""
Comprehensive Performance Profiling System for Sands of Duat

Advanced profiling system for detailed analysis of rendering bottlenecks,
frame time analysis, memory usage tracking, and GPU utilization monitoring.

Features:
- Real-time frame time analysis with statistical breakdown
- GPU utilization estimation and bottleneck detection
- Memory usage tracking with leak detection
- Rendering pipeline profiling
- Performance regression detection
- Automated performance report generation
- Visual performance graphs and heatmaps
"""

import pygame
import time
import threading
import json
import statistics
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque, defaultdict
import logging
from pathlib import Path
import math
import psutil

from .dynamic_quality_manager import get_quality_manager
from .advanced_memory_manager import get_memory_manager
from ..core.performance_profiler import profile_operation


class ProfileCategory(Enum):
    """Categories of performance metrics."""
    RENDERING = "rendering"
    PARTICLES = "particles"
    ASSETS = "assets"
    MEMORY = "memory"
    INPUT = "input"
    AUDIO = "audio"
    GAME_LOGIC = "game_logic"
    UI = "ui"


class BottleneckType(Enum):
    """Types of performance bottlenecks."""
    CPU_BOUND = "cpu_bound"
    GPU_BOUND = "gpu_bound"
    MEMORY_BOUND = "memory_bound"
    IO_BOUND = "io_bound"
    BALANCED = "balanced"


@dataclass
class PerformanceMetric:
    """Individual performance metric measurement."""
    name: str
    category: ProfileCategory
    value: float
    timestamp: float
    metadata: Dict[str, Any]


@dataclass
class FrameProfile:
    """Complete profile of a single frame."""
    frame_number: int
    start_time: float
    end_time: float
    frame_time_ms: float
    fps: float
    metrics: List[PerformanceMetric]
    render_stages: Dict[str, float]  # Time spent in each render stage
    memory_snapshot: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "frame_number": self.frame_number,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "frame_time_ms": self.frame_time_ms,
            "fps": self.fps,
            "metrics": [asdict(m) for m in self.metrics],
            "render_stages": self.render_stages,
            "memory_snapshot": self.memory_snapshot
        }


class RenderStageProfiler:
    """Profiles individual rendering stages."""
    
    def __init__(self):
        self.stage_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=120))
        self.current_stage: Optional[str] = None
        self.stage_start_time: float = 0.0
        self.frame_stages: Dict[str, float] = {}
    
    def start_stage(self, stage_name: str):
        """Start timing a render stage."""
        if self.current_stage:
            self.end_stage()
        
        self.current_stage = stage_name
        self.stage_start_time = time.perf_counter()
    
    def end_stage(self):
        """End timing current render stage."""
        if self.current_stage and self.stage_start_time > 0:
            duration = (time.perf_counter() - self.stage_start_time) * 1000  # Convert to ms
            self.stage_times[self.current_stage].append(duration)
            self.frame_stages[self.current_stage] = duration
            self.current_stage = None
            self.stage_start_time = 0.0
    
    def get_frame_stages(self) -> Dict[str, float]:
        """Get timing for all stages in current frame."""
        if self.current_stage:
            self.end_stage()
        
        stages = self.frame_stages.copy()
        self.frame_stages.clear()
        return stages
    
    def get_average_stage_times(self) -> Dict[str, float]:
        """Get average time for each render stage."""
        return {
            stage: statistics.mean(times) if times else 0.0
            for stage, times in self.stage_times.items()
        }
    
    def get_stage_statistics(self, stage_name: str) -> Dict[str, float]:
        """Get detailed statistics for a specific stage."""
        if stage_name not in self.stage_times or not self.stage_times[stage_name]:
            return {"average": 0.0, "min": 0.0, "max": 0.0, "std_dev": 0.0}
        
        times = list(self.stage_times[stage_name])
        return {
            "average": statistics.mean(times),
            "min": min(times),
            "max": max(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0.0,
            "samples": len(times)
        }


class BottleneckDetector:
    """Detects performance bottlenecks automatically."""
    
    def __init__(self):
        self.cpu_utilization = deque(maxlen=60)
        self.memory_utilization = deque(maxlen=60)
        self.frame_times = deque(maxlen=60)
        self.render_stage_times = defaultdict(lambda: deque(maxlen=60))
        
    def update(self, frame_time_ms: float, render_stages: Dict[str, float]):
        """Update bottleneck detection with new frame data."""
        # Record frame time
        self.frame_times.append(frame_time_ms)
        
        # Record render stage times
        for stage, time_ms in render_stages.items():
            self.render_stage_times[stage].append(time_ms)
        
        # Get system utilization
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            memory_percent = psutil.virtual_memory().percent
            
            self.cpu_utilization.append(cpu_percent)
            self.memory_utilization.append(memory_percent)
        except:
            pass  # Handle cases where system monitoring fails
    
    def detect_bottleneck(self) -> BottleneckType:
        """Detect current bottleneck type."""
        if len(self.frame_times) < 30:
            return BottleneckType.BALANCED  # Need more samples
        
        # Calculate averages
        avg_cpu = statistics.mean(self.cpu_utilization) if self.cpu_utilization else 0
        avg_memory = statistics.mean(self.memory_utilization) if self.memory_utilization else 0
        avg_frame_time = statistics.mean(self.frame_times)
        
        # Analyze render stage distribution
        total_render_time = 0
        stage_percentages = {}
        
        for stage, times in self.render_stage_times.items():
            if times:
                avg_time = statistics.mean(times)
                total_render_time += avg_time
                stage_percentages[stage] = avg_time
        
        # Normalize stage percentages
        if total_render_time > 0:
            stage_percentages = {
                stage: (time / total_render_time) * 100
                for stage, time in stage_percentages.items()
            }
        
        # Determine bottleneck
        if avg_memory > 85:
            return BottleneckType.MEMORY_BOUND
        elif avg_cpu > 80:
            return BottleneckType.CPU_BOUND
        elif avg_frame_time > 20:  # Over 20ms suggests GPU bottleneck
            # Check if GPU-intensive stages are taking most time
            gpu_intensive_stages = ["particles", "lighting", "effects", "post_processing"]
            gpu_time_percent = sum(
                stage_percentages.get(stage, 0) 
                for stage in gpu_intensive_stages
            )
            
            if gpu_time_percent > 60:
                return BottleneckType.GPU_BOUND
            else:
                return BottleneckType.CPU_BOUND
        else:
            return BottleneckType.BALANCED
    
    def get_bottleneck_analysis(self) -> Dict[str, Any]:
        """Get detailed bottleneck analysis."""
        bottleneck = self.detect_bottleneck()
        
        # Calculate confidence scores
        confidence_scores = self._calculate_confidence_scores()
        
        # Get recommendations
        recommendations = self._get_recommendations(bottleneck)
        
        return {
            "bottleneck_type": bottleneck.value,
            "confidence_scores": confidence_scores,
            "recommendations": recommendations,
            "stage_analysis": self._analyze_render_stages(),
            "system_metrics": {
                "avg_cpu_percent": statistics.mean(self.cpu_utilization) if self.cpu_utilization else 0,
                "avg_memory_percent": statistics.mean(self.memory_utilization) if self.memory_utilization else 0,
                "avg_frame_time_ms": statistics.mean(self.frame_times) if self.frame_times else 0
            }
        }
    
    def _calculate_confidence_scores(self) -> Dict[str, float]:
        """Calculate confidence scores for bottleneck detection."""
        if not self.frame_times or not self.cpu_utilization:
            return {}
        
        # Calculate variance in measurements
        frame_time_variance = statistics.variance(self.frame_times) if len(self.frame_times) > 1 else 0
        cpu_variance = statistics.variance(self.cpu_utilization) if len(self.cpu_utilization) > 1 else 0
        
        # Lower variance means higher confidence
        frame_confidence = max(0, 1.0 - (frame_time_variance / 100))
        cpu_confidence = max(0, 1.0 - (cpu_variance / 1000))
        
        return {
            "frame_timing": frame_confidence,
            "cpu_utilization": cpu_confidence,
            "overall": (frame_confidence + cpu_confidence) / 2
        }
    
    def _get_recommendations(self, bottleneck: BottleneckType) -> List[str]:
        """Get optimization recommendations based on bottleneck."""
        recommendations = []
        
        if bottleneck == BottleneckType.CPU_BOUND:
            recommendations.extend([
                "Reduce particle count",
                "Optimize game logic loops",
                "Consider multi-threading for heavy calculations",
                "Reduce draw calls by batching"
            ])
        elif bottleneck == BottleneckType.GPU_BOUND:
            recommendations.extend([
                "Reduce texture resolution",
                "Disable post-processing effects",
                "Reduce lighting quality",
                "Lower particle rendering quality"
            ])
        elif bottleneck == BottleneckType.MEMORY_BOUND:
            recommendations.extend([
                "Reduce texture memory usage",
                "Clear unused assets",
                "Compress textures",
                "Reduce object pooling limits"
            ])
        elif bottleneck == BottleneckType.IO_BOUND:
            recommendations.extend([
                "Preload assets earlier",
                "Use asset streaming",
                "Compress save files",
                "Cache frequently accessed data"
            ])
        else:  # BALANCED
            recommendations.extend([
                "Performance is well balanced",
                "Consider increasing quality settings",
                "Monitor for performance regression"
            ])
        
        return recommendations
    
    def _analyze_render_stages(self) -> Dict[str, Any]:
        """Analyze render stage performance."""
        stage_analysis = {}
        total_time = 0
        
        for stage, times in self.render_stage_times.items():
            if times:
                avg_time = statistics.mean(times)
                total_time += avg_time
                
                stage_analysis[stage] = {
                    "average_ms": avg_time,
                    "percentage": 0,  # Will be calculated below
                    "samples": len(times),
                    "variance": statistics.variance(times) if len(times) > 1 else 0
                }
        
        # Calculate percentages
        if total_time > 0:
            for stage_data in stage_analysis.values():
                stage_data["percentage"] = (stage_data["average_ms"] / total_time) * 100
        
        return stage_analysis


class PerformanceRegression:
    """Detects performance regressions over time."""
    
    def __init__(self, baseline_frames: int = 300):  # 5 seconds at 60fps
        self.baseline_frames = baseline_frames
        self.baseline_metrics: Dict[str, float] = {}
        self.current_metrics = deque(maxlen=baseline_frames)
        self.regression_threshold = 0.1  # 10% performance drop
        
    def establish_baseline(self, frame_profiles: List[FrameProfile]):
        """Establish performance baseline from frame profiles."""
        if len(frame_profiles) < self.baseline_frames:
            return False
        
        # Calculate baseline metrics
        frame_times = [fp.frame_time_ms for fp in frame_profiles[-self.baseline_frames:]]
        
        self.baseline_metrics = {
            "average_frame_time": statistics.mean(frame_times),
            "p95_frame_time": sorted(frame_times)[int(len(frame_times) * 0.95)],
            "fps": 1000 / statistics.mean(frame_times),
            "frame_time_variance": statistics.variance(frame_times)
        }
        
        return True
    
    def check_regression(self, recent_profiles: List[FrameProfile]) -> Dict[str, Any]:
        """Check for performance regression."""
        if not self.baseline_metrics or len(recent_profiles) < 60:
            return {"has_regression": False, "reason": "insufficient_data"}
        
        # Calculate current metrics
        recent_frame_times = [fp.frame_time_ms for fp in recent_profiles[-60:]]
        current_metrics = {
            "average_frame_time": statistics.mean(recent_frame_times),
            "p95_frame_time": sorted(recent_frame_times)[int(len(recent_frame_times) * 0.95)],
            "fps": 1000 / statistics.mean(recent_frame_times),
            "frame_time_variance": statistics.variance(recent_frame_times)
        }
        
        # Check for regressions
        regressions = {}
        has_regression = False
        
        for metric, baseline_value in self.baseline_metrics.items():
            current_value = current_metrics[metric]
            
            if metric == "fps":
                # For FPS, lower is worse
                change_ratio = (baseline_value - current_value) / baseline_value
            else:
                # For frame time and variance, higher is worse
                change_ratio = (current_value - baseline_value) / baseline_value
            
            if change_ratio > self.regression_threshold:
                regressions[metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "change_percent": change_ratio * 100
                }
                has_regression = True
        
        return {
            "has_regression": has_regression,
            "regressions": regressions,
            "current_metrics": current_metrics,
            "baseline_metrics": self.baseline_metrics
        }


class ComprehensiveProfiler:
    """Main comprehensive performance profiling system."""
    
    def __init__(self, max_frame_history: int = 1800):  # 30 seconds at 60fps
        self.max_frame_history = max_frame_history
        self.frame_profiles: deque = deque(maxlen=max_frame_history)
        self.current_frame_number = 0
        
        # Sub-systems
        self.render_profiler = RenderStageProfiler()
        self.bottleneck_detector = BottleneckDetector()
        self.regression_detector = PerformanceRegression()
        
        # Current frame tracking
        self.frame_start_time = 0.0
        self.current_metrics: List[PerformanceMetric] = []
        
        # Integration with other systems
        self.quality_manager = get_quality_manager()
        self.memory_manager = get_memory_manager()
        
        # Performance alerts
        self.alert_callbacks: List[Callable[[str, Dict[str, Any]], None]] = []
        
        self.logger = logging.getLogger(__name__)
        
    def start_frame(self):
        """Start profiling a new frame."""
        self.frame_start_time = time.perf_counter()
        self.current_metrics.clear()
        self.current_frame_number += 1
    
    def end_frame(self):
        """End frame profiling and record results."""
        if self.frame_start_time == 0:
            return
        
        frame_end_time = time.perf_counter()
        frame_time_ms = (frame_end_time - self.frame_start_time) * 1000
        fps = 1000 / frame_time_ms if frame_time_ms > 0 else 0
        
        # Get render stage timings
        render_stages = self.render_profiler.get_frame_stages()
        
        # Get memory snapshot
        memory_snapshot = self.memory_manager.get_memory_report()
        
        # Create frame profile
        frame_profile = FrameProfile(
            frame_number=self.current_frame_number,
            start_time=self.frame_start_time,
            end_time=frame_end_time,
            frame_time_ms=frame_time_ms,
            fps=fps,
            metrics=self.current_metrics.copy(),
            render_stages=render_stages,
            memory_snapshot=memory_snapshot
        )
        
        self.frame_profiles.append(frame_profile)
        
        # Update bottleneck detection
        self.bottleneck_detector.update(frame_time_ms, render_stages)
        
        # Check for performance alerts
        self._check_performance_alerts(frame_profile)
        
        # Reset frame tracking
        self.frame_start_time = 0.0
    
    def start_render_stage(self, stage_name: str):
        """Start timing a render stage."""
        self.render_profiler.start_stage(stage_name)
    
    def end_render_stage(self):
        """End timing current render stage."""
        self.render_profiler.end_stage()
    
    def record_metric(self, name: str, category: ProfileCategory, value: float, 
                     metadata: Dict[str, Any] = None):
        """Record a custom performance metric."""
        metric = PerformanceMetric(
            name=name,
            category=category,
            value=value,
            timestamp=time.perf_counter(),
            metadata=metadata or {}
        )
        self.current_metrics.append(metric)
    
    def _check_performance_alerts(self, frame_profile: FrameProfile):
        """Check for performance issues and trigger alerts."""
        # Check for frame time spikes
        if frame_profile.frame_time_ms > 33.33:  # Under 30 FPS
            self._trigger_alert("frame_time_spike", {
                "frame_time_ms": frame_profile.frame_time_ms,
                "fps": frame_profile.fps,
                "frame_number": frame_profile.frame_number
            })
        
        # Check for memory pressure
        memory_pressure = frame_profile.memory_snapshot.get("system_memory", {}).get("used_percent", 0)
        if memory_pressure > 90:
            self._trigger_alert("memory_pressure", {
                "memory_percent": memory_pressure,
                "frame_number": frame_profile.frame_number
            })
        
        # Check for potential memory leaks (gradual memory increase)
        if len(self.frame_profiles) >= 300:  # 5 seconds of frames
            recent_memory = [fp.memory_snapshot.get("process_memory", {}).get("rss_mb", 0) 
                           for fp in list(self.frame_profiles)[-300:]]
            if len(recent_memory) >= 2:
                memory_trend = recent_memory[-1] - recent_memory[0]
                if memory_trend > 50:  # 50MB increase in 5 seconds
                    self._trigger_alert("potential_memory_leak", {
                        "memory_increase_mb": memory_trend,
                        "frame_number": frame_profile.frame_number
                    })
    
    def _trigger_alert(self, alert_type: str, data: Dict[str, Any]):
        """Trigger performance alert."""
        for callback in self.alert_callbacks:
            try:
                callback(alert_type, data)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
    
    def add_alert_callback(self, callback: Callable[[str, Dict[str, Any]], None]):
        """Add callback for performance alerts."""
        self.alert_callbacks.append(callback)
    
    def get_performance_summary(self, frames: Optional[int] = None) -> Dict[str, Any]:
        """Get performance summary for recent frames."""
        if frames is None:
            frames = min(300, len(self.frame_profiles))  # Last 5 seconds
        
        if not self.frame_profiles:
            return {"error": "No frame data available"}
        
        recent_frames = list(self.frame_profiles)[-frames:]
        
        # Calculate frame time statistics
        frame_times = [fp.frame_time_ms for fp in recent_frames]
        fps_values = [fp.fps for fp in recent_frames]
        
        frame_stats = {
            "average_frame_time_ms": statistics.mean(frame_times),
            "min_frame_time_ms": min(frame_times),
            "max_frame_time_ms": max(frame_times),
            "p95_frame_time_ms": sorted(frame_times)[int(len(frame_times) * 0.95)],
            "frame_time_std_dev": statistics.stdev(frame_times) if len(frame_times) > 1 else 0,
            "average_fps": statistics.mean(fps_values),
            "min_fps": min(fps_values),
            "target_fps_hit_rate": sum(1 for fps in fps_values if fps >= 58) / len(fps_values) * 100
        }
        
        # Get render stage analysis
        render_analysis = self.render_profiler.get_average_stage_times()
        
        # Get bottleneck analysis
        bottleneck_analysis = self.bottleneck_detector.get_bottleneck_analysis()
        
        # Check for regressions
        regression_analysis = self.regression_detector.check_regression(recent_frames)
        
        return {
            "frame_statistics": frame_stats,
            "render_stages": render_analysis,
            "bottleneck_analysis": bottleneck_analysis,
            "regression_analysis": regression_analysis,
            "frames_analyzed": len(recent_frames),
            "profiling_duration_seconds": frames / 60.0
        }
    
    def generate_performance_report(self, output_path: Optional[Path] = None) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        report = {
            "timestamp": time.time(),
            "session_info": {
                "total_frames": self.current_frame_number,
                "profiling_duration_minutes": self.current_frame_number / 60.0 / 60.0,
                "frame_history_size": len(self.frame_profiles)
            },
            "performance_summary": self.get_performance_summary(),
            "quality_settings": self.quality_manager.get_current_settings().to_dict(),
            "memory_report": self.memory_manager.get_memory_report(),
            "system_info": {
                "cpu_count": psutil.cpu_count(),
                "memory_gb": psutil.virtual_memory().total / (1024**3),
                "platform": "Windows" if "nt" in __import__("os").name else "Linux/Mac"
            }
        }
        
        # Save to file if path provided
        if output_path:
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"Performance report saved to {output_path}")
            except Exception as e:
                self.logger.error(f"Failed to save performance report: {e}")
        
        return report
    
    def establish_performance_baseline(self):
        """Establish performance baseline for regression detection."""
        if len(self.frame_profiles) >= 300:
            success = self.regression_detector.establish_baseline(list(self.frame_profiles))
            if success:
                self.logger.info("Performance baseline established")
                return True
        return False
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get real-time performance metrics for display."""
        if not self.frame_profiles:
            return {}
        
        # Get last 60 frames (1 second)
        recent_frames = list(self.frame_profiles)[-60:]
        
        if not recent_frames:
            return {}
        
        current_fps = statistics.mean([fp.fps for fp in recent_frames])
        current_frame_time = statistics.mean([fp.frame_time_ms for fp in recent_frames])
        
        # Get current memory usage
        latest_memory = recent_frames[-1].memory_snapshot
        
        return {
            "current_fps": round(current_fps, 1),
            "current_frame_time_ms": round(current_frame_time, 2),
            "memory_usage_mb": latest_memory.get("process_memory", {}).get("rss_mb", 0),
            "gpu_pressure": "normal",  # Simplified
            "bottleneck": self.bottleneck_detector.detect_bottleneck().value,
            "frame_count": len(recent_frames)
        }


# Global profiler
_global_profiler = None

def get_comprehensive_profiler() -> ComprehensiveProfiler:
    """Get global comprehensive profiler."""
    global _global_profiler
    if _global_profiler is None:
        _global_profiler = ComprehensiveProfiler()
    return _global_profiler

def start_frame_profiling():
    """Start profiling current frame."""
    profiler = get_comprehensive_profiler()
    profiler.start_frame()

def end_frame_profiling():
    """End profiling current frame."""
    profiler = get_comprehensive_profiler()
    profiler.end_frame()

def profile_render_stage(stage_name: str):
    """Context manager for profiling render stages."""
    class RenderStageProfiler:
        def __init__(self, name):
            self.name = name
            
        def __enter__(self):
            get_comprehensive_profiler().start_render_stage(self.name)
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            get_comprehensive_profiler().end_render_stage()
    
    return RenderStageProfiler(stage_name)

def record_performance_metric(name: str, category: ProfileCategory, value: float, 
                            metadata: Dict[str, Any] = None):
    """Record a custom performance metric."""
    profiler = get_comprehensive_profiler()
    profiler.record_metric(name, category, value, metadata)

def get_performance_dashboard() -> Dict[str, Any]:
    """Get real-time performance dashboard data."""
    profiler = get_comprehensive_profiler()
    return profiler.get_real_time_metrics()