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
    
    regeneration_rate: float = Field(default=0.5, description="Sand grains per second (1 grain every 2 seconds)")
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
    
    Enhanced with strategic depth mechanics including resonance,
    momentum, and dynamic regeneration.
    """
    
    current_sand: int = Field(default=0, ge=0, description="Current sand amount")
    max_sand: int = Field(default=6, ge=1, le=8, description="Maximum sand capacity (expandable with buffs)")
    on_sand_change: Optional[Callable[[int], None]] = Field(default=None, exclude=True)
    
    # Enhanced strategic mechanics
    temporal_momentum_stacks: int = Field(default=0, description="Stacks of momentum for cost reduction")
    last_card_cost: int = Field(default=0, description="Cost of last card played for momentum tracking")
    divine_favor: int = Field(default=0, description="Moral alignment (-10 to +10)")
    resonance_multiplier: float = Field(default=1.0, description="Current resonance power multiplier")
    
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Initialize private attributes
        self._logger = logging.getLogger(__name__)
        self._sand_timing_errors = []
        self._regeneration_events = []
        self._fractional_sand = 0.0  # Accumulator for fractional sand
        
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
                    self._regeneration_rate = config.getfloat('timing', 'sand_regeneration_rate', fallback=0.5)
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
        self._regeneration_rate = 0.5
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
    
    def spend_sand(self, cost: int, card_cost: Optional[int] = None) -> bool:
        """
        Attempt to spend sand for a card or ability.
        
        Returns True if successful, False if insufficient sand.
        Includes overflow protection for costs exceeding max_sand.
        Enhanced with momentum tracking.
        """
        if cost < 0 or cost > self.max_sand:
            self._logger.warning(f"Invalid sand cost: {cost} (max: {self.max_sand})")
            return False
        
        if not self.can_afford(cost):
            return False
        
        self.current_sand -= cost
        
        # Update temporal momentum if this is a card play
        if card_cost is not None:
            self.update_temporal_momentum(card_cost)
        
        self._logger.debug(f"Spent {cost} sand, remaining: {self.current_sand}")
        
        if self.on_sand_change:
            self.on_sand_change(self.current_sand)
        return True
    
    def update_temporal_momentum(self, card_cost: int) -> None:
        """
        Update temporal momentum based on decreasing card costs.
        
        Momentum builds when playing cards with decreasing costs,
        providing cost reduction for future cards.
        """
        if card_cost < self.last_card_cost:
            self.temporal_momentum_stacks = min(self.temporal_momentum_stacks + 1, 5)
            self._logger.debug(f"Momentum increased to {self.temporal_momentum_stacks}")
        else:
            self.temporal_momentum_stacks = 0
            self._logger.debug("Momentum reset")
        
        self.last_card_cost = card_cost
    
    def get_momentum_reduction(self) -> int:
        """Get current cost reduction from temporal momentum."""
        return min(self.temporal_momentum_stacks, 3)  # Max 3 sand reduction
    
    def check_sand_resonance(self, card_cost: int) -> str:
        """
        Check resonance between current sand and card cost.
        
        Returns resonance level: 'perfect', 'minor', or 'none'
        """
        if card_cost == self.current_sand:
            return 'perfect'
        elif abs(card_cost - self.current_sand) <= 1:
            return 'minor'
        return 'none'
    
    def apply_divine_judgment(self, action_alignment: str) -> None:
        """
        Apply divine judgment based on action moral alignment.
        
        Args:
            action_alignment: 'order', 'chaos', or 'balance'
        """
        if action_alignment == 'order':
            self.divine_favor = min(self.divine_favor + 1, 10)
        elif action_alignment == 'chaos':
            self.divine_favor = max(self.divine_favor - 1, -10)
        # 'balance' actions don't change favor
        
        self._logger.debug(f"Divine favor: {self.divine_favor}")
    
    def update_sand(self, player_health_percentage: float = 1.0, has_divine_blessing: bool = False) -> None:
        """
        Update sand based on high-precision elapsed time.
        
        Uses time.perf_counter() for sub-millisecond accuracy and implements
        delta time clamping to prevent lag-induced acceleration.
        
        Enhanced with dynamic regeneration based on game state.
        """
        if self.current_sand >= self.max_sand:
            return
        
        # Get high-precision delta time
        delta_time = self.timer.get_delta_time()
        
        if delta_time <= 0:
            return
        
        # Calculate dynamic regeneration rate
        dynamic_rate = self.get_dynamic_regeneration_rate(player_health_percentage, has_divine_blessing)
        
        # Calculate fractional sand to add based on dynamic regeneration rate
        fractional_sand_to_add = delta_time * dynamic_rate
        
        # Add to fractional accumulator
        self._fractional_sand += fractional_sand_to_add
        
        # Convert whole grains from fractional accumulator
        grains_to_add = int(self._fractional_sand)
        if grains_to_add > 0:
            # Remove the whole grains from fractional accumulator, keeping remainder
            self._fractional_sand -= grains_to_add
            
            # Add grains to current sand
            old_sand = self.current_sand
            self.current_sand = min(self.max_sand, self.current_sand + grains_to_add)
            
            if self.current_sand > old_sand:
                self._regeneration_events.append(time.perf_counter())
                self._logger.debug(f"Sand regenerated: {old_sand} -> {self.current_sand} (+{self.current_sand - old_sand} grains)")
                
                if self.on_sand_change:
                    self.on_sand_change(self.current_sand)
    
    def get_dynamic_regeneration_rate(self, health_percentage: float, has_divine_blessing: bool) -> float:
        """
        Calculate dynamic sand regeneration rate based on game state.
        
        Args:
            health_percentage: Player's current health as percentage (0.0-1.0)
            has_divine_blessing: Whether player has divine blessing active
        
        Returns:
            Modified regeneration rate
        """
        base_rate = self.regeneration_rate
        
        # Accelerate when low on health (desperation)
        if health_percentage < 0.3:
            base_rate *= 1.5
        elif health_percentage < 0.6:
            base_rate *= 1.2
        
        # Slow when at max sand (prevent resource waste)
        if self.current_sand >= self.max_sand - 1:
            base_rate *= 0.5
        
        # Divine blessing influence
        if has_divine_blessing:
            base_rate *= 1.25
        
        # Divine favor affects regeneration
        if self.divine_favor > 5:
            base_rate *= 1.3  # High favor = faster regeneration
        elif self.divine_favor < -5:
            base_rate *= 0.7  # Low favor = slower regeneration
        
        return base_rate
    
    def get_time_to_next_sand(self) -> float:
        """
        Get time remaining until next sand grain is generated.
        
        Returns:
            Time in seconds until next sand grain (0.0 if at max capacity)
        """
        if self.current_sand >= self.max_sand:
            return 0.0
        
        # Calculate progress toward next sand grain using fractional accumulator
        time_for_one_grain = 1.0 / self.regeneration_rate
        fractional_progress = self._fractional_sand
        time_remaining = time_for_one_grain * (1.0 - fractional_progress)
        
        return max(0.0, time_remaining)
    
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