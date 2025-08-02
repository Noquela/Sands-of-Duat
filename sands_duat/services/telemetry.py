"""
Performance Monitoring and Telemetry Service

Real-time performance tracking with CSV logging for CI regression detection
and runtime performance optimization.

Features:
- FPS monitoring with percentile tracking
- Memory usage tracking
- Sand timing accuracy measurement
- CSV export for trend analysis
- Alert thresholds for performance regression
"""

import time
import csv
import psutil
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Deque
from collections import deque
from dataclasses import dataclass, asdict
import logging


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    timestamp: str
    fps: float
    frame_time_ms: float
    memory_usage_mb: float
    memory_percent: float
    sand_timing_error_ms: float
    cpu_percent: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for CSV export."""
        return asdict(self)


class PerformanceMonitor:
    """
    Real-time performance monitoring with regression detection.
    
    Implements the performance monitoring strategy from the enhanced
    development plan with CSV logging and alert thresholds.
    """
    
    def __init__(self, 
                 csv_file: Path = Path("performance_metrics.csv"),
                 fps_warning_threshold: float = 45.0,
                 memory_growth_threshold: float = 1.2,
                 sand_error_threshold_ms: float = 50.0):
        
        self.csv_file = csv_file
        self.fps_warning_threshold = fps_warning_threshold
        self.memory_growth_threshold = memory_growth_threshold
        self.sand_error_threshold_ms = sand_error_threshold_ms
        
        # Performance tracking
        self.frame_times: Deque[float] = deque(maxlen=60)  # 1 second at 60fps
        self.sand_timing_errors: Deque[float] = deque(maxlen=100)
        self.memory_samples: Deque[float] = deque(maxlen=300)  # 5 minutes at 1 sample/sec
        
        # Baseline measurements
        self.initial_memory = psutil.virtual_memory().used / (1024 * 1024)  # MB
        self.start_time = time.perf_counter()
        
        # Metrics history
        self.metrics_history: List[PerformanceMetrics] = []
        self.last_csv_write = time.time()
        self.csv_write_interval = 5.0  # Write to CSV every 5 seconds
        
        # Thread safety
        self._lock = threading.Lock()
        
        self.logger = logging.getLogger(__name__)
        self._initialize_csv()
        
        self.logger.info("Performance monitor initialized")
    
    def _initialize_csv(self) -> None:
        """Initialize CSV file with headers."""
        try:
            if not self.csv_file.exists():
                self.csv_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(self.csv_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'timestamp', 'fps', 'frame_time_ms', 'memory_usage_mb',
                        'memory_percent', 'sand_timing_error_ms', 'cpu_percent'
                    ])
                
                self.logger.info(f"Initialized performance CSV: {self.csv_file}")
        except Exception as e:
            self.logger.error(f"Failed to initialize performance CSV: {e}")
    
    def log_frame(self, delta_time: float) -> None:
        """
        Log a frame's performance metrics.
        
        Args:
            delta_time: Frame time in seconds
        """
        with self._lock:
            self.frame_times.append(delta_time)
            
            # Check for performance regression
            if len(self.frame_times) == 60:  # Full second of data
                avg_fps = self._calculate_fps()
                if avg_fps < self.fps_warning_threshold:
                    self.logger.warning(f"Performance regression detected: {avg_fps:.1f} FPS")
            
            # Periodic CSV writing
            current_time = time.time()
            if current_time - self.last_csv_write >= self.csv_write_interval:
                self._write_to_csv()
                self.last_csv_write = current_time
    
    def log_sand_timing_error(self, expected_time: float, actual_time: float) -> None:
        """
        Log sand timing accuracy.
        
        Args:
            expected_time: Expected time for sand regeneration
            actual_time: Actual time measured
        """
        error_ms = abs(expected_time - actual_time) * 1000
        
        with self._lock:
            self.sand_timing_errors.append(error_ms)
            
            if error_ms > self.sand_error_threshold_ms:
                self.logger.warning(f"Sand timing drift: {error_ms:.1f}ms")
    
    def log_memory_usage(self) -> None:
        """Log current memory usage."""
        try:
            memory_info = psutil.virtual_memory()
            current_memory_mb = memory_info.used / (1024 * 1024)
            
            with self._lock:
                self.memory_samples.append(current_memory_mb)
                
                # Check for memory growth
                memory_growth = current_memory_mb / self.initial_memory
                if memory_growth > self.memory_growth_threshold:
                    self.logger.warning(f"Memory growth detected: {memory_growth:.2f}x initial")
        
        except Exception as e:
            self.logger.error(f"Failed to log memory usage: {e}")
    
    def _calculate_fps(self) -> float:
        """Calculate average FPS from recent frame times."""
        if not self.frame_times:
            return 0.0
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def _get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics snapshot."""
        try:
            # FPS and frame time
            fps = self._calculate_fps()
            avg_frame_time = sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0.0
            frame_time_ms = avg_frame_time * 1000
            
            # Memory usage
            memory_info = psutil.virtual_memory()
            memory_usage_mb = memory_info.used / (1024 * 1024)
            memory_percent = memory_info.percent
            
            # Sand timing error
            avg_sand_error = sum(self.sand_timing_errors) / len(self.sand_timing_errors) if self.sand_timing_errors else 0.0
            
            # CPU usage
            cpu_percent = psutil.cpu_percent()
            
            return PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                fps=fps,
                frame_time_ms=frame_time_ms,
                memory_usage_mb=memory_usage_mb,
                memory_percent=memory_percent,
                sand_timing_error_ms=avg_sand_error,
                cpu_percent=cpu_percent
            )
        
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                fps=0.0, frame_time_ms=0.0, memory_usage_mb=0.0,
                memory_percent=0.0, sand_timing_error_ms=0.0, cpu_percent=0.0
            )
    
    def _write_to_csv(self) -> None:
        """Write current metrics to CSV file."""
        try:
            metrics = self._get_current_metrics()
            self.metrics_history.append(metrics)
            
            # Keep history limited
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-500:]
            
            # Append to CSV
            with open(self.csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    metrics.timestamp,
                    f"{metrics.fps:.1f}",
                    f"{metrics.frame_time_ms:.2f}",
                    f"{metrics.memory_usage_mb:.1f}",
                    f"{metrics.memory_percent:.1f}",
                    f"{metrics.sand_timing_error_ms:.2f}",
                    f"{metrics.cpu_percent:.1f}"
                ])
        
        except Exception as e:
            self.logger.error(f"Failed to write performance metrics to CSV: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of current performance statistics."""
        with self._lock:
            fps = self._calculate_fps()
            
            # Frame time percentiles
            if self.frame_times:
                sorted_times = sorted(self.frame_times)
                p95_time = sorted_times[int(len(sorted_times) * 0.95)]
                p99_time = sorted_times[int(len(sorted_times) * 0.99)]
            else:
                p95_time = p99_time = 0.0
            
            # Memory stats
            current_memory = self.memory_samples[-1] if self.memory_samples else 0.0
            memory_growth = current_memory / self.initial_memory if self.initial_memory > 0 else 1.0
            
            # Sand timing stats
            sand_errors = list(self.sand_timing_errors)
            max_sand_error = max(sand_errors) if sand_errors else 0.0
            avg_sand_error = sum(sand_errors) / len(sand_errors) if sand_errors else 0.0
            
            return {
                'uptime_seconds': time.perf_counter() - self.start_time,
                'fps': {
                    'current': fps,
                    'is_below_threshold': fps < self.fps_warning_threshold,
                    'threshold': self.fps_warning_threshold
                },
                'frame_time': {
                    'p95_ms': p95_time * 1000,
                    'p99_ms': p99_time * 1000
                },
                'memory': {
                    'current_mb': current_memory,
                    'growth_factor': memory_growth,
                    'is_above_threshold': memory_growth > self.memory_growth_threshold,
                    'threshold': self.memory_growth_threshold
                },
                'sand_timing': {
                    'max_error_ms': max_sand_error,
                    'avg_error_ms': avg_sand_error,
                    'error_count': len(sand_errors),
                    'threshold_ms': self.sand_error_threshold_ms
                },
                'metrics_collected': len(self.metrics_history)
            }
    
    def export_metrics(self, output_file: Path) -> None:
        """Export all collected metrics to a file."""
        try:
            with open(output_file, 'w', newline='') as f:
                if self.metrics_history:
                    writer = csv.DictWriter(f, fieldnames=self.metrics_history[0].to_dict().keys())
                    writer.writeheader()
                    
                    for metrics in self.metrics_history:
                        writer.writerow(metrics.to_dict())
            
            self.logger.info(f"Exported {len(self.metrics_history)} metrics to {output_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
    
    def reset_metrics(self) -> None:
        """Reset all collected metrics."""
        with self._lock:
            self.frame_times.clear()
            self.sand_timing_errors.clear()
            self.memory_samples.clear()
            self.metrics_history.clear()
            self.initial_memory = psutil.virtual_memory().used / (1024 * 1024)
            self.start_time = time.perf_counter()
        
        self.logger.info("Performance metrics reset")
    
    def shutdown(self) -> None:
        """Clean shutdown with final metrics write."""
        try:
            self._write_to_csv()
            self.logger.info("Performance monitor shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during performance monitor shutdown: {e}")


# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def init_performance_monitor(**kwargs) -> PerformanceMonitor:
    """Initialize the global performance monitor."""
    global _performance_monitor
    _performance_monitor = PerformanceMonitor(**kwargs)
    return _performance_monitor