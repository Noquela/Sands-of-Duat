"""
Hour-Glass Initiative System

Implements the core sand management and timing mechanics that define
the unique combat system of Sands of Duat.

Key Features:
- Real-time sand regeneration (1 grain per second)
- Sand cost validation for card plays
- Animation timing synchronization
- Visible enemy sand tracking for tactical decisions

Classes:
- HourGlass: Main sand container and regeneration logic
- SandTimer: High-precision timing for sand regeneration
"""

import asyncio
import time
import logging
from typing import Optional, Callable, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import configparser
from pathlib import Path


class TimingAccuracy(Enum):
    """Timing accuracy levels for sand regeneration."""
    STANDARD = 0.1  # 100ms accuracy
    HIGH = 0.05     # 50ms accuracy (default)
    ULTRA = 0.01    # 10ms accuracy (for testing)


class PrecisionTimer:
    """
    High-precision timer using time.perf_counter() for sub-millisecond accuracy.
    
    Implements delta time clamping and frame-rate independence as specified
    in the enhanced development plan.
    """
    
    def __init__(self, regeneration_rate: float = 1.0, max_delta_clamp: float = 0.05):
        self.regeneration_rate = regeneration_rate
        self.max_delta_clamp = max_delta_clamp
        self.last_update = time.perf_counter()
        self.is_paused = False
        self.time_scale = 1.0  # For debug/testing
        self.accumulated_time = 0.0
        
        # Performance monitoring
        self.timing_errors = []
        self.frame_times = []
        
        self.logger = logging.getLogger(__name__)
    
    def get_delta_time(self) -> float:
        """
        Get high-precision delta time with clamping to prevent lag acceleration.
        
        Returns:
            Delta time in seconds, clamped to max_delta_clamp
        """
        if self.is_paused:
            return 0.0
        
        current_time = time.perf_counter()
        raw_delta = current_time - self.last_update
        self.last_update = current_time
        
        # Clamp delta time to prevent spiral of death during lag
        clamped_delta = min(raw_delta, self.max_delta_clamp)
        
        # Apply debug time scale
        scaled_delta = clamped_delta * self.time_scale
        
        # Track performance metrics
        self.frame_times.append(raw_delta)
        if len(self.frame_times) > 60:  # Keep last 60 frames
            self.frame_times.pop(0)
        
        # Log timing errors if delta was clamped
        if raw_delta != clamped_delta:
            error_ms = (raw_delta - clamped_delta) * 1000
            self.timing_errors.append(error_ms)
            if error_ms > 50:  # 50ms threshold
                self.logger.warning(f"Large timing correction: {error_ms:.1f}ms")
        
        return scaled_delta
    
    def set_time_scale(self, scale: float):
        """Set debug time scale for testing different speeds."""
        self.time_scale = scale
        self.logger.info(f"Time scale set to {scale}x")
    
    def pause(self):
        """Pause timing updates."""
        self.is_paused = True
    
    def resume(self):
        """Resume timing updates and reset reference time."""
        self.is_paused = False
        self.last_update = time.perf_counter()
    
    def get_average_fps(self) -> float:
        """Get average FPS from recent frame times."""
        if not self.frame_times:
            return 0.0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0


class SandTimer(BaseModel):
    """High-precision timer for sand regeneration with frame-rate independence."""
    
    regeneration_rate: float = Field(default=1.0, description="Sand grains per second")
    is_paused: bool = Field(default=False)
    timing_accuracy: float = Field(default=TimingAccuracy.HIGH.value, description="Timing precision in seconds")
    frame_accumulator: float = Field(default=0.0, description="Frame time accumulator for consistency")
    debug_mode: bool = Field(default=False, description="Enable detailed timing logs")
    
    def __init__(self, **data):
        super().__init__(**data)
        self._precision_timer = PrecisionTimer(self.regeneration_rate)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since last update with high precision."""
        return self._precision_timer.get_delta_time()
        
        # Apply timing accuracy threshold to prevent micro-updates
        if elapsed < self.timing_accuracy:
            return 0.0
        
        if self.debug_mode:
            logging.debug(f"SandTimer elapsed: {elapsed:.3f}s (accuracy: {self.timing_accuracy:.3f}s)")
        
        return elapsed
    
    def update_timestamp(self) -> None:
        """Update the last update timestamp."""
        self.last_update = time.time()
    
    def pause(self) -> None:
        """Pause sand regeneration (during animations)."""
        self.is_paused = True
    
    def resume(self) -> None:
        """Resume sand regeneration and reset accumulator."""
        self.is_paused = False
        self.frame_accumulator = 0.0  # Reset accumulator to prevent time jumps
        self.update_timestamp()
        
        if self.debug_mode:
            logging.debug("SandTimer resumed, accumulator reset")


class HourGlass(BaseModel):
    """
    Core Hour-Glass sand management system with enhanced precision timing.
    
    Manages sand storage, regeneration, and spending mechanics
    for the unique Initiative system using time.perf_counter() for
    sub-millisecond accuracy.
    """
    
    current_sand: int = Field(default=0, ge=0, description="Current sand amount")
    max_sand: int = Field(default=6, ge=1, le=8, description="Maximum sand capacity (expandable with buffs)")
    on_sand_change: Optional[Callable[[int], None]] = Field(default=None, exclude=True)
    
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Initialize private attributes
        self._logger = logging.getLogger(__name__)
        self._sand_timing_errors = []
        self._regeneration_events = []
        
        # Load configuration
        self._load_config()
        
        # Initialize precision timer
        self._timer = PrecisionTimer(
            regeneration_rate=self.regeneration_rate,
            max_delta_clamp=self.max_delta_clamp
        )
        
        self._logger.info("HourGlass initialized with precision timing")
    
    @property
    def timer(self) -> PrecisionTimer:
        return self._timer
    
    @property
    def sand_timing_errors(self) -> List[float]:
        return self._sand_timing_errors
    
    @property
    def regeneration_events(self) -> List[float]:
        return self._regeneration_events
    
    def _load_config(self):
        """Load configuration from config.ini."""
        try:
            config = configparser.ConfigParser()
            config_path = Path("config/config.ini")
            
            if config_path.exists():
                config.read(config_path)
                
                # Use correct ConfigParser syntax
                if config.has_section('timing'):
                    self._regeneration_rate = config.getfloat('timing', 'sand_regeneration_rate', fallback=1.0)
                    self._max_delta_clamp = config.getfloat('timing', 'max_delta_clamp', fallback=0.05)
                    self._timing_precision = config.getfloat('timing', 'timing_precision', fallback=0.001)
                    self._debug_time_scale = config.getfloat('timing', 'debug_time_scale', fallback=1.0)
                else:
                    self._set_default_values()
            else:
                self._set_default_values()
        except Exception as e:
            if hasattr(self, '_logger'):
                self._logger.warning(f"Could not load config, using defaults: {e}")
            self._set_default_values()
    
    def _set_default_values(self):
        """Set default configuration values."""
        self._regeneration_rate = 1.0
        self._max_delta_clamp = 0.05
        self._timing_precision = 0.001
        self._debug_time_scale = 1.0
    
    @property
    def regeneration_rate(self) -> float:
        return getattr(self, '_regeneration_rate', 1.0)
    
    @property
    def max_delta_clamp(self) -> float:
        return getattr(self, '_max_delta_clamp', 0.05)
    
    @property
    def timing_precision(self) -> float:
        return getattr(self, '_timing_precision', 0.001)
    
    @property
    def debug_time_scale(self) -> float:
        return getattr(self, '_debug_time_scale', 1.0)
    
    def can_afford(self, cost: int) -> bool:
        """Check if the hourglass has enough sand for a given cost."""
        return self.current_sand >= cost
    
    def spend_sand(self, cost: int) -> bool:
        """
        Attempt to spend sand for a card or ability.
        
        Returns True if successful, False if insufficient sand.
        Includes overflow protection for costs exceeding max_sand.
        """
        if cost < 0 or cost > self.max_sand:
            self._logger.warning(f"Invalid sand cost: {cost} (max: {self.max_sand})")
            return False
        
        if not self.can_afford(cost):
            return False
        
        self.current_sand -= cost
        self._logger.debug(f"Spent {cost} sand, remaining: {self.current_sand}")
        
        if self.on_sand_change:
            self.on_sand_change(self.current_sand)
        return True
    
    def update_sand(self) -> None:
        """
        Update sand based on high-precision elapsed time.
        
        Uses time.perf_counter() for sub-millisecond accuracy and implements
        delta time clamping to prevent lag-induced acceleration.
        """
        if self.current_sand >= self.max_sand:
            return
        
        # Get high-precision delta time
        delta_time = self.timer.get_delta_time()
        
        if delta_time <= 0:
            return
        
        # Calculate sand to add based on regeneration rate
        sand_to_add = delta_time * self.regeneration_rate
        
        # Track timing accuracy
        expected_time = 1.0 / self.regeneration_rate  # Time per sand grain
        if sand_to_add >= 1.0:
            actual_time = delta_time / int(sand_to_add)
            timing_error = abs(expected_time - actual_time)
            
            if timing_error > self.timing_precision:
                self._sand_timing_errors.append(timing_error * 1000)  # Convert to ms
                if timing_error > 0.05:  # 50ms threshold
                    self._logger.warning(f"Sand timing drift: {timing_error*1000:.1f}ms")
        
        # Add sand grains (integer only)
        grains_added = int(sand_to_add)
        if grains_added > 0:
            old_sand = self.current_sand
            self.current_sand = min(self.max_sand, self.current_sand + grains_added)
            
            if self.current_sand > old_sand:
                self._regeneration_events.append(time.perf_counter())
                self._logger.debug(f"Sand regenerated: {old_sand} -> {self.current_sand}")
                
                if self.on_sand_change:
                    self.on_sand_change(self.current_sand)
    
    def get_time_to_next_sand(self) -> float:
        """
        Get time remaining until next sand grain is generated.
        
        Returns:
            Time in seconds until next sand grain (0.0 if at max capacity)
        """
        if self.current_sand >= self.max_sand:
            return 0.0
        
        # Calculate progress toward next sand grain
        time_for_one_grain = 1.0 / self.regeneration_rate
        elapsed = self.timer.accumulated_time
        progress = elapsed % time_for_one_grain
        
        return time_for_one_grain - progress
    
    def get_time_until_next_sand(self) -> float:
        """Alias for get_time_to_next_sand() for backward compatibility."""
        return self.get_time_to_next_sand()
    
    def set_sand(self, amount: int) -> None:
        """
        Set sand to a specific amount (for initialization/testing).
        
        Args:
            amount: Sand amount to set (clamped to valid range)
        """
        old_sand = self.current_sand
        self.current_sand = max(0, min(self.max_sand, amount))
        
        self._logger.debug(f"Sand set: {old_sand} -> {self.current_sand}")
        
        if self.on_sand_change:
            self.on_sand_change(self.current_sand)
    
    def increase_max_sand(self, amount: int) -> bool:
        """
        Increase maximum sand capacity (for buff effects).
        
        Args:
            amount: Amount to increase max sand by
            
        Returns:
            True if successful, False if would exceed absolute limit (8)
        """
        new_max = self.max_sand + amount
        if new_max > 8:  # Absolute maximum to prevent overflow
            return False
        
        old_max = self.max_sand
        self.max_sand = new_max
        
        self._logger.info(f"Max sand increased: {old_max} -> {self.max_sand}")
        return True
    
    def pause_regeneration(self) -> None:
        """Pause sand regeneration (during animations)."""
        self.timer.pause()
        self._logger.debug("Sand regeneration paused")
    
    def resume_regeneration(self) -> None:
        """Resume sand regeneration."""
        self.timer.resume()
        self._logger.debug("Sand regeneration resumed")
    
    def set_debug_time_scale(self, scale: float) -> None:
        """Set debug time scale for testing different speeds."""
        self.timer.set_time_scale(scale)
        self._logger.info(f"Debug time scale set to {scale}x")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring."""
        return {
            'average_fps': self.timer.get_average_fps(),
            'timing_errors_count': len(self._sand_timing_errors),
            'max_timing_error_ms': max(self._sand_timing_errors) if self._sand_timing_errors else 0,
            'regeneration_events': len(self._regeneration_events),
            'current_sand': self.current_sand,
            'max_sand': self.max_sand,
            'regeneration_rate': self.regeneration_rate
        }


# Global hourglass instance for convenience
_hourglass_instance: Optional[HourGlass] = None


def get_hourglass() -> HourGlass:
    """Get the global hourglass instance."""
    global _hourglass_instance
    if _hourglass_instance is None:
        _hourglass_instance = HourGlass()
    return _hourglass_instance


def create_hourglass(max_sand: int = 6, **kwargs) -> HourGlass:
    """Create a new hourglass instance with specified parameters."""
    return HourGlass(max_sand=max_sand, **kwargs)