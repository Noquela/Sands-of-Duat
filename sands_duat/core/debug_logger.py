"""
Debug Logger for Hour-Glass Initiative System

Provides comprehensive logging and debugging capabilities for the
Hour-Glass Initiative system, including timing precision analysis,
performance monitoring, and diagnostic tools.

Key Features:
- Detailed timing analysis and precision measurement
- Performance profiling and bottleneck detection
- Sand regeneration accuracy tracking
- Combat action timing verification
- Visual debugging tools and reports

Classes:
- TimingAnalyzer: Analyzes timing precision and accuracy
- PerformanceProfiler: Profiles system performance
- SandDebugger: Specialized debugging for sand mechanics
- HourGlassLogger: Main logging coordinator
"""

import logging
import time
import statistics
import json
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Tuple
from pydantic import BaseModel, Field
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import threading
from pathlib import Path

from .hourglass import HourGlass, TimingAccuracy
from .combat_enhanced import EnhancedCombatEngine, EnhancedCombatAction
from .animation_coordinator import AnimationCoordinator
from .enemy_ai import EnemyAIManager


class LogLevel(Enum):
    """Extended log levels for Hour-Glass debugging."""
    TIMING_CRITICAL = 5    # Critical timing issues
    TIMING_WARNING = 15    # Timing precision warnings
    SAND_TRACE = 25        # Detailed sand regeneration tracing
    PERFORMANCE = 35       # Performance monitoring
    AI_DECISION = 45       # AI decision tracing


class DebugCategory(Enum):
    """Categories of debugging information."""
    TIMING = "timing"
    SAND_REGEN = "sand_regeneration"
    COMBAT = "combat"
    ANIMATION = "animation"
    AI = "ai"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"


@dataclass
class TimingMeasurement:
    """A single timing measurement."""
    timestamp: float
    expected_time: float
    actual_time: float
    error: float
    category: str
    entity_id: str
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
        self.error = abs(self.actual_time - self.expected_time)
    
    @property
    def error_percentage(self) -> float:
        """Get error as percentage of expected time."""
        if self.expected_time == 0:
            return 0.0
        return (self.error / self.expected_time) * 100
    
    @property
    def is_within_tolerance(self) -> bool:
        """Check if measurement is within acceptable tolerance."""
        return self.error <= 0.05  # 50ms tolerance


@dataclass
class PerformanceSnapshot:
    """Snapshot of system performance at a point in time."""
    timestamp: float
    fps: float
    frame_time: float
    sand_update_time: float
    combat_update_time: float
    animation_update_time: float
    ai_update_time: float
    memory_usage: float
    active_entities: int
    active_animations: int
    queued_actions: int


class TimingAnalyzer(BaseModel):
    """Analyzes timing precision and accuracy."""
    
    measurements: List[TimingMeasurement] = Field(default_factory=list)
    max_measurements: int = Field(default=1000)
    tolerance_threshold: float = Field(default=0.05)  # 50ms
    
    def record_measurement(self, expected: float, actual: float, 
                         category: str, entity_id: str = "",
                         details: Optional[Dict[str, Any]] = None) -> TimingMeasurement:
        """Record a timing measurement."""
        measurement = TimingMeasurement(
            timestamp=time.time(),
            expected_time=expected,
            actual_time=actual,
            error=0,  # Will be calculated in __post_init__
            category=category,
            entity_id=entity_id,
            details=details or {}
        )
        
        self.measurements.append(measurement)
        
        # Keep only recent measurements
        if len(self.measurements) > self.max_measurements:
            self.measurements.pop(0)
        
        return measurement
    
    def analyze_timing_accuracy(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Analyze timing accuracy for a category or all measurements."""
        relevant_measurements = self.measurements
        if category:
            relevant_measurements = [m for m in self.measurements if m.category == category]
        
        if not relevant_measurements:
            return {"error": "No measurements available"}
        
        errors = [m.error for m in relevant_measurements]
        error_percentages = [m.error_percentage for m in relevant_measurements]
        within_tolerance = [m.is_within_tolerance for m in relevant_measurements]
        
        return {
            "total_measurements": len(relevant_measurements),
            "average_error": statistics.mean(errors),
            "median_error": statistics.median(errors),
            "max_error": max(errors),
            "min_error": min(errors),
            "std_deviation": statistics.stdev(errors) if len(errors) > 1 else 0,
            "average_error_percentage": statistics.mean(error_percentages),
            "measurements_within_tolerance": sum(within_tolerance),
            "tolerance_rate": sum(within_tolerance) / len(within_tolerance) * 100,
            "category": category or "all"
        }
    
    def get_problematic_entities(self) -> Dict[str, float]:
        """Get entities with the worst timing accuracy."""
        entity_errors = defaultdict(list)
        
        for measurement in self.measurements:
            if measurement.entity_id:
                entity_errors[measurement.entity_id].append(measurement.error)
        
        # Calculate average error per entity
        entity_averages = {}
        for entity_id, errors in entity_errors.items():
            entity_averages[entity_id] = statistics.mean(errors)
        
        # Sort by worst average error
        return dict(sorted(entity_averages.items(), key=lambda x: x[1], reverse=True))
    
    def generate_timing_report(self) -> str:
        """Generate a comprehensive timing analysis report."""
        report = ["=" * 60]
        report.append("HOUR-GLASS TIMING ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total measurements: {len(self.measurements)}")
        report.append("")
        
        # Overall analysis
        overall = self.analyze_timing_accuracy()
        report.append("OVERALL TIMING ACCURACY:")
        report.append(f"  Average Error: {overall['average_error']:.3f}s ({overall['average_error_percentage']:.1f}%)")
        report.append(f"  Median Error: {overall['median_error']:.3f}s")
        report.append(f"  Max Error: {overall['max_error']:.3f}s")
        report.append(f"  Tolerance Rate: {overall['tolerance_rate']:.1f}%")
        report.append("")
        
        # Category analysis
        categories = set(m.category for m in self.measurements)
        for category in categories:
            cat_analysis = self.analyze_timing_accuracy(category)
            report.append(f"CATEGORY: {category.upper()}")
            report.append(f"  Measurements: {cat_analysis['total_measurements']}")
            report.append(f"  Average Error: {cat_analysis['average_error']:.3f}s")
            report.append(f"  Tolerance Rate: {cat_analysis['tolerance_rate']:.1f}%")
            report.append("")
        
        # Problematic entities
        problematic = self.get_problematic_entities()
        if problematic:
            report.append("ENTITIES WITH WORST TIMING:")
            for entity_id, avg_error in list(problematic.items())[:5]:
                report.append(f"  {entity_id}: {avg_error:.3f}s average error")
            report.append("")
        
        return "\n".join(report)


class PerformanceProfiler(BaseModel):
    """Profiles system performance and identifies bottlenecks."""
    
    snapshots: List[PerformanceSnapshot] = Field(default_factory=list)
    max_snapshots: int = Field(default=300)  # 5 minutes at 1 snapshot per second
    profiling_enabled: bool = Field(default=False)
    
    def start_profiling(self) -> None:
        """Start performance profiling."""
        self.profiling_enabled = True
        logging.info("Performance profiling started")
    
    def stop_profiling(self) -> None:
        """Stop performance profiling."""
        self.profiling_enabled = False
        logging.info("Performance profiling stopped")
    
    def take_snapshot(self, fps: float, frame_time: float, 
                     sand_update_time: float = 0.0, combat_update_time: float = 0.0,
                     animation_update_time: float = 0.0, ai_update_time: float = 0.0,
                     memory_usage: float = 0.0, active_entities: int = 0,
                     active_animations: int = 0, queued_actions: int = 0) -> None:
        """Take a performance snapshot."""
        if not self.profiling_enabled:
            return
        
        snapshot = PerformanceSnapshot(
            timestamp=time.time(),
            fps=fps,
            frame_time=frame_time,
            sand_update_time=sand_update_time,
            combat_update_time=combat_update_time,
            animation_update_time=animation_update_time,
            ai_update_time=ai_update_time,
            memory_usage=memory_usage,
            active_entities=active_entities,
            active_animations=active_animations,
            queued_actions=queued_actions
        )
        
        self.snapshots.append(snapshot)
        
        # Keep only recent snapshots
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)
    
    def analyze_performance(self, time_window: float = 60.0) -> Dict[str, Any]:
        """Analyze performance over a time window."""
        cutoff_time = time.time() - time_window
        recent_snapshots = [s for s in self.snapshots if s.timestamp >= cutoff_time]
        
        if not recent_snapshots:
            return {"error": "No recent snapshots available"}
        
        # Calculate statistics
        fps_values = [s.fps for s in recent_snapshots]
        frame_times = [s.frame_time for s in recent_snapshots]
        sand_times = [s.sand_update_time for s in recent_snapshots if s.sand_update_time > 0]
        
        analysis = {
            "time_window": time_window,
            "snapshots_analyzed": len(recent_snapshots),
            "fps": {
                "average": statistics.mean(fps_values),
                "min": min(fps_values),
                "max": max(fps_values),
                "std_dev": statistics.stdev(fps_values) if len(fps_values) > 1 else 0
            },
            "frame_time": {
                "average": statistics.mean(frame_times),
                "min": min(frame_times),
                "max": max(frame_times)
            }
        }
        
        if sand_times:
            analysis["sand_update_time"] = {
                "average": statistics.mean(sand_times),
                "max": max(sand_times),
                "percentage_of_frame": (statistics.mean(sand_times) / statistics.mean(frame_times)) * 100
            }
        
        return analysis
    
    def detect_performance_issues(self) -> List[str]:
        """Detect potential performance issues."""
        issues = []
        
        if not self.snapshots:
            return issues
        
        recent_snapshots = self.snapshots[-30:]  # Last 30 snapshots
        
        # Check FPS stability
        fps_values = [s.fps for s in recent_snapshots]
        if fps_values:
            avg_fps = statistics.mean(fps_values)
            min_fps = min(fps_values)
            
            if avg_fps < 50:
                issues.append(f"Low average FPS: {avg_fps:.1f}")
            
            if min_fps < 30:
                issues.append(f"FPS drops detected: minimum {min_fps:.1f}")
            
            if len(fps_values) > 1:
                fps_variance = statistics.stdev(fps_values)
                if fps_variance > 10:
                    issues.append(f"Unstable FPS: variance {fps_variance:.1f}")
        
        # Check update times
        sand_times = [s.sand_update_time for s in recent_snapshots if s.sand_update_time > 0]
        if sand_times and max(sand_times) > 0.01:  # 10ms threshold
            issues.append(f"Slow sand updates: max {max(sand_times):.3f}s")
        
        return issues


class SandDebugger(BaseModel):
    """Specialized debugger for sand mechanics."""
    
    regeneration_events: List[Dict[str, Any]] = Field(default_factory=list)
    spending_events: List[Dict[str, Any]] = Field(default_factory=list)
    max_events: int = Field(default=500)
    
    def log_sand_regeneration(self, entity_id: str, old_sand: int, new_sand: int,
                             expected_time: float, actual_time: float,
                             hourglass_state: Dict[str, Any]) -> None:
        """Log a sand regeneration event."""
        event = {
            "timestamp": time.time(),
            "entity_id": entity_id,
            "old_sand": old_sand,
            "new_sand": new_sand,
            "sand_gained": new_sand - old_sand,
            "expected_time": expected_time,
            "actual_time": actual_time,
            "timing_error": abs(actual_time - expected_time),
            "hourglass_state": hourglass_state.copy()
        }
        
        self.regeneration_events.append(event)
        
        # Keep only recent events
        if len(self.regeneration_events) > self.max_events:
            self.regeneration_events.pop(0)
        
        # Log timing issues
        if event["timing_error"] > 0.1:  # 100ms threshold
            logging.warning(f"Sand regeneration timing issue for {entity_id}: "
                          f"expected {expected_time:.3f}s, actual {actual_time:.3f}s")
    
    def log_sand_spending(self, entity_id: str, amount: int, action_type: str,
                         sand_before: int, sand_after: int) -> None:
        """Log a sand spending event."""
        event = {
            "timestamp": time.time(),
            "entity_id": entity_id,
            "amount_spent": amount,
            "action_type": action_type,
            "sand_before": sand_before,
            "sand_after": sand_after,
            "expected_after": sand_before - amount,
            "correct_spending": sand_after == sand_before - amount
        }
        
        self.spending_events.append(event)
        
        # Keep only recent events
        if len(self.spending_events) > self.max_events:
            self.spending_events.pop(0)
        
        # Log spending errors
        if not event["correct_spending"]:
            logging.error(f"Sand spending error for {entity_id}: "
                        f"spent {amount}, before {sand_before}, after {sand_after}")
    
    def analyze_regeneration_accuracy(self, entity_id: Optional[str] = None) -> Dict[str, Any]:
        """Analyze sand regeneration accuracy."""
        events = self.regeneration_events
        if entity_id:
            events = [e for e in events if e["entity_id"] == entity_id]
        
        if not events:
            return {"error": "No regeneration events found"}
        
        timing_errors = [e["timing_error"] for e in events]
        sand_gains = [e["sand_gained"] for e in events]
        
        return {
            "total_events": len(events),
            "average_timing_error": statistics.mean(timing_errors),
            "max_timing_error": max(timing_errors),
            "events_with_major_errors": sum(1 for e in timing_errors if e > 0.1),
            "average_sand_gain": statistics.mean(sand_gains),
            "total_sand_regenerated": sum(sand_gains),
            "entity_id": entity_id or "all"
        }
    
    def get_sand_flow_summary(self, entity_id: str, time_window: float = 300.0) -> Dict[str, Any]:
        """Get sand flow summary for an entity over time window."""
        cutoff_time = time.time() - time_window
        
        recent_regen = [e for e in self.regeneration_events 
                       if e["entity_id"] == entity_id and e["timestamp"] >= cutoff_time]
        recent_spending = [e for e in self.spending_events 
                          if e["entity_id"] == entity_id and e["timestamp"] >= cutoff_time]
        
        total_regenerated = sum(e["sand_gained"] for e in recent_regen)
        total_spent = sum(e["amount_spent"] for e in recent_spending)
        
        return {
            "entity_id": entity_id,
            "time_window": time_window,
            "sand_regenerated": total_regenerated,
            "sand_spent": total_spent,
            "net_sand_change": total_regenerated - total_spent,
            "regeneration_events": len(recent_regen),
            "spending_events": len(recent_spending),
            "average_spending_per_action": total_spent / max(1, len(recent_spending))
        }


class HourGlassLogger:
    """
    Main logging coordinator for the Hour-Glass Initiative system.
    
    Provides comprehensive logging, debugging, and analysis capabilities
    for all aspects of the sand-based combat system.
    """
    
    def __init__(self, log_level: int = logging.INFO, log_file: Optional[str] = None):
        self.timing_analyzer = TimingAnalyzer()
        self.performance_profiler = PerformanceProfiler()
        self.sand_debugger = SandDebugger()
        
        # Logging configuration
        self.enabled_categories: set[DebugCategory] = set()
        self.log_file = log_file
        
        # Setup logging
        self._setup_logging(log_level, log_file)
        
        # Performance monitoring
        self._last_performance_check = time.time()
        self._performance_check_interval = 1.0  # Check every second
        
        logging.info("HourGlass Logger initialized")
    
    def _setup_logging(self, log_level: int, log_file: Optional[str]) -> None:
        """Setup logging configuration."""
        # Create custom log levels
        logging.addLevelName(LogLevel.TIMING_CRITICAL.value, "TIMING_CRITICAL")
        logging.addLevelName(LogLevel.TIMING_WARNING.value, "TIMING_WARNING")
        logging.addLevelName(LogLevel.SAND_TRACE.value, "SAND_TRACE")
        logging.addLevelName(LogLevel.PERFORMANCE.value, "PERFORMANCE")
        logging.addLevelName(LogLevel.AI_DECISION.value, "AI_DECISION")
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
    
    def enable_category(self, category: DebugCategory) -> None:
        """Enable logging for a specific category."""
        self.enabled_categories.add(category)
        logging.info(f"Enabled logging category: {category.value}")
    
    def disable_category(self, category: DebugCategory) -> None:
        """Disable logging for a specific category."""
        self.enabled_categories.discard(category)
        logging.info(f"Disabled logging category: {category.value}")
    
    def is_category_enabled(self, category: DebugCategory) -> bool:
        """Check if a category is enabled."""
        return category in self.enabled_categories
    
    def log_timing(self, message: str, expected: float, actual: float, 
                   entity_id: str = "", category: str = "general",
                   level: LogLevel = LogLevel.TIMING_WARNING) -> None:
        """Log timing information."""
        if not self.is_category_enabled(DebugCategory.TIMING):
            return
        
        measurement = self.timing_analyzer.record_measurement(
            expected, actual, category, entity_id
        )
        
        error_ms = measurement.error * 1000
        logging.log(level.value, f"TIMING - {message}: expected {expected:.3f}s, "
                   f"actual {actual:.3f}s, error {error_ms:.1f}ms ({entity_id})")
    
    def log_sand_regeneration(self, entity_id: str, hourglass: HourGlass,
                            old_sand: int, new_sand: int, expected_time: float) -> None:
        """Log sand regeneration event."""
        if not self.is_category_enabled(DebugCategory.SAND_REGEN):
            return
        
        actual_time = time.time()
        hourglass_state = hourglass.get_regeneration_status()
        
        self.sand_debugger.log_sand_regeneration(
            entity_id, old_sand, new_sand, expected_time, actual_time, hourglass_state
        )
        
        sand_gained = new_sand - old_sand
        logging.log(LogLevel.SAND_TRACE.value, 
                   f"SAND_REGEN - {entity_id}: {old_sand} -> {new_sand} (+{sand_gained})")
    
    def log_sand_spending(self, entity_id: str, amount: int, action_type: str,
                         sand_before: int, sand_after: int) -> None:
        """Log sand spending event."""
        if not self.is_category_enabled(DebugCategory.SAND_REGEN):
            return
        
        self.sand_debugger.log_sand_spending(
            entity_id, amount, action_type, sand_before, sand_after
        )
        
        logging.log(LogLevel.SAND_TRACE.value,
                   f"SAND_SPEND - {entity_id}: -{amount} for {action_type} "
                   f"({sand_before} -> {sand_after})")
    
    def log_combat_action(self, action: EnhancedCombatAction, status: str) -> None:
        """Log combat action."""
        if not self.is_category_enabled(DebugCategory.COMBAT):
            return
        
        logging.info(f"COMBAT - {status}: {action.action_type.value} by {action.actor_id} "
                    f"(cost: {action.sand_cost}, priority: {action.priority})")
    
    def log_ai_decision(self, entity_id: str, decision: str, reasoning: str,
                       confidence: float) -> None:
        """Log AI decision."""
        if not self.is_category_enabled(DebugCategory.AI):
            return
        
        logging.log(LogLevel.AI_DECISION.value,
                   f"AI_DECISION - {entity_id}: {decision} "
                   f"(confidence: {confidence:.2f}, reason: {reasoning})")
    
    def log_performance_snapshot(self, **kwargs) -> None:
        """Log performance snapshot."""
        if not self.is_category_enabled(DebugCategory.PERFORMANCE):
            return
        
        self.performance_profiler.take_snapshot(**kwargs)
        
        current_time = time.time()
        if current_time - self._last_performance_check >= self._performance_check_interval:
            issues = self.performance_profiler.detect_performance_issues()
            if issues:
                for issue in issues:
                    logging.log(LogLevel.PERFORMANCE.value, f"PERFORMANCE - {issue}")
            
            self._last_performance_check = current_time
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive debug report."""
        report = ["=" * 80]
        report.append("HOUR-GLASS INITIATIVE SYSTEM DEBUG REPORT")
        report.append("=" * 80)
        report.append(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Enabled categories: {[c.value for c in self.enabled_categories]}")
        report.append("")
        
        # Timing analysis
        report.append(self.timing_analyzer.generate_timing_report())
        report.append("")
        
        # Performance analysis
        perf_analysis = self.performance_profiler.analyze_performance()
        if "error" not in perf_analysis:
            report.append("PERFORMANCE ANALYSIS:")
            report.append(f"  Average FPS: {perf_analysis['fps']['average']:.1f}")
            report.append(f"  FPS Range: {perf_analysis['fps']['min']:.1f} - {perf_analysis['fps']['max']:.1f}")
            report.append(f"  Average Frame Time: {perf_analysis['frame_time']['average']:.3f}s")
            
            if "sand_update_time" in perf_analysis:
                sand_stats = perf_analysis["sand_update_time"]
                report.append(f"  Sand Update Time: {sand_stats['average']:.3f}s ({sand_stats['percentage_of_frame']:.1f}% of frame)")
            
            report.append("")
        
        # Sand regeneration analysis
        sand_analysis = self.sand_debugger.analyze_regeneration_accuracy()
        if "error" not in sand_analysis:
            report.append("SAND REGENERATION ANALYSIS:")
            report.append(f"  Total Events: {sand_analysis['total_events']}")
            report.append(f"  Average Timing Error: {sand_analysis['average_timing_error']:.3f}s")
            report.append(f"  Max Timing Error: {sand_analysis['max_timing_error']:.3f}s")
            report.append(f"  Events with Major Errors: {sand_analysis['events_with_major_errors']}")
            report.append("")
        
        # Performance issues
        issues = self.performance_profiler.detect_performance_issues()
        if issues:
            report.append("DETECTED PERFORMANCE ISSUES:")
            for issue in issues:
                report.append(f"  - {issue}")
            report.append("")
        
        return "\n".join(report)
    
    def save_report_to_file(self, filename: Optional[str] = None) -> str:
        """Save comprehensive report to file."""
        if not filename:
            filename = f"hourglass_debug_report_{int(time.time())}.txt"
        
        report = self.generate_comprehensive_report()
        
        try:
            with open(filename, 'w') as f:
                f.write(report)
            logging.info(f"Debug report saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Failed to save debug report: {e}")
            return ""
    
    def export_data(self, filename: Optional[str] = None) -> str:
        """Export all debug data to JSON file."""
        if not filename:
            filename = f"hourglass_debug_data_{int(time.time())}.json"
        
        data = {
            "timestamp": time.time(),
            "timing_measurements": [asdict(m) for m in self.timing_analyzer.measurements],
            "performance_snapshots": [asdict(s) for s in self.performance_profiler.snapshots],
            "regeneration_events": self.sand_debugger.regeneration_events,
            "spending_events": self.sand_debugger.spending_events,
            "enabled_categories": [c.value for c in self.enabled_categories]
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            logging.info(f"Debug data exported to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Failed to export debug data: {e}")
            return ""
    
    def start_performance_profiling(self) -> None:
        """Start performance profiling."""
        self.performance_profiler.start_profiling()
        self.enable_category(DebugCategory.PERFORMANCE)
    
    def stop_performance_profiling(self) -> None:
        """Stop performance profiling."""
        self.performance_profiler.stop_profiling()
    
    def enable_full_debugging(self) -> None:
        """Enable all debugging categories."""
        for category in DebugCategory:
            self.enable_category(category)
        logging.info("Full debugging enabled")
    
    def disable_all_debugging(self) -> None:
        """Disable all debugging categories."""
        self.enabled_categories.clear()
        logging.info("All debugging disabled")


# Global debug logger instance
debug_logger = HourGlassLogger()