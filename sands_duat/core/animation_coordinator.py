"""
Animation Coordinator for Hour-Glass Initiative System

Manages animation timing and coordination with sand regeneration,
ensuring smooth visual feedback while maintaining accurate timing
for the Hour-Glass Initiative mechanics.

Key Features:
- Centralized animation management
- Sand regeneration pause/resume coordination
- Frame-rate independent animation timing
- Visual feedback synchronization
- Combat action animation sequencing

Classes:
- AnimationCoordinator: Main animation management system
- AnimationSequence: Manages sequences of related animations
- TimingController: Controls timing precision during animations
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Tuple
from pydantic import BaseModel, Field
from dataclasses import dataclass
from collections import defaultdict, deque

from .hourglass import HourGlass
from .sand_visuals import sand_visualizer


class AnimationType(Enum):
    """Types of animations that can occur."""
    CARD_PLAY = "card_play"
    ABILITY_USE = "ability_use"
    SAND_REGENERATION = "sand_regeneration"
    SAND_SPENDING = "sand_spending"
    DAMAGE_EFFECT = "damage_effect"
    HEALING_EFFECT = "healing_effect"
    UI_TRANSITION = "ui_transition"
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"


class AnimationPriority(Enum):
    """Animation priority levels."""
    CRITICAL = 100   # Combat resolution, damage
    HIGH = 50        # Card plays, abilities
    NORMAL = 25      # Sand regeneration, UI updates
    LOW = 10         # Ambient effects, particles
    BACKGROUND = 0   # Background animations


@dataclass
class AnimationEvent:
    """Represents a single animation event."""
    animation_id: str
    animation_type: AnimationType
    entity_id: str  # Which entity this animation belongs to
    duration: float
    priority: AnimationPriority
    start_time: float
    end_time: float
    blocks_sand_regen: bool = True
    blocks_input: bool = False
    callback: Optional[Callable[[], None]] = None
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.end_time == 0:
            self.end_time = self.start_time + self.duration
    
    def is_active(self) -> bool:
        """Check if animation is currently active."""
        current_time = time.time()
        return self.start_time <= current_time <= self.end_time
    
    def is_finished(self) -> bool:
        """Check if animation has finished."""
        return time.time() > self.end_time
    
    def get_progress(self) -> float:
        """Get animation progress (0.0 to 1.0)."""
        if not self.is_active():
            return 1.0 if self.is_finished() else 0.0
        
        elapsed = time.time() - self.start_time
        return min(1.0, elapsed / self.duration)


class AnimationSequence(BaseModel):
    """Manages a sequence of related animations."""
    
    sequence_id: str
    events: List[AnimationEvent] = Field(default_factory=list)
    is_parallel: bool = Field(default=False, description="Whether animations play in parallel")
    current_index: int = Field(default=0)
    completion_callback: Optional[Callable[[], None]] = Field(default=None, exclude=True)
    
    def add_animation(self, event: AnimationEvent) -> None:
        """Add an animation to the sequence."""
        if self.is_parallel:
            # All animations start at the same time
            event.start_time = time.time()
        else:
            # Sequential animations
            if self.events:
                last_event = self.events[-1]
                event.start_time = last_event.end_time
            else:
                event.start_time = time.time()
        
        event.end_time = event.start_time + event.duration
        self.events.append(event)
    
    def get_active_animations(self) -> List[AnimationEvent]:
        """Get currently active animations in the sequence."""
        current_time = time.time()
        return [event for event in self.events if event.is_active()]
    
    def is_complete(self) -> bool:
        """Check if the entire sequence is complete."""
        return all(event.is_finished() for event in self.events)
    
    def get_total_duration(self) -> float:
        """Get total duration of the sequence."""
        if not self.events:
            return 0.0
        
        if self.is_parallel:
            return max(event.duration for event in self.events)
        else:
            return sum(event.duration for event in self.events)
    
    def should_block_sand_regen(self) -> bool:
        """Check if any active animation blocks sand regeneration."""
        active = self.get_active_animations()
        return any(event.blocks_sand_regen for event in active)


class TimingController(BaseModel):
    """Controls precise timing during animations."""
    
    precision_mode: bool = Field(default=True, description="Whether to use high precision timing")
    timing_tolerance: float = Field(default=0.016, description="Timing tolerance in seconds (60fps)")
    frame_accumulator: float = Field(default=0.0)
    last_update: float = Field(default_factory=time.time)
    
    def update(self, target_fps: int = 60) -> Tuple[bool, float]:
        """
        Update timing controller.
        
        Returns (should_update, delta_time) tuple.
        """
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time
        
        if not self.precision_mode:
            return True, delta_time
        
        # Accumulate frame time for consistent updates
        self.frame_accumulator += delta_time
        target_frame_time = 1.0 / target_fps
        
        if self.frame_accumulator >= target_frame_time:
            # Time for an update
            actual_delta = self.frame_accumulator
            self.frame_accumulator = 0.0
            return True, actual_delta
        
        return False, 0.0
    
    def reset(self) -> None:
        """Reset timing accumulator."""
        self.frame_accumulator = 0.0
        self.last_update = time.time()


class AnimationCoordinator(BaseModel):
    """
    Main animation coordination system for Hour-Glass Initiative.
    
    Manages all animations and their interaction with sand regeneration,
    ensuring precise timing and smooth visual feedback.
    """
    
    # Active animations
    active_animations: Dict[str, AnimationEvent] = Field(default_factory=dict)
    animation_sequences: Dict[str, AnimationSequence] = Field(default_factory=dict)
    
    # Registered hourglasses for coordination
    hourglasses: Dict[str, HourGlass] = Field(default_factory=dict)
    
    # Timing control
    timing_controller: TimingController = Field(default_factory=TimingController)
    global_animation_paused: bool = Field(default=False)
    
    # Settings
    max_concurrent_animations: int = Field(default=10)
    animation_quality: float = Field(default=1.0, ge=0.1, le=2.0, description="Animation quality multiplier")
    
    # Callbacks
    on_animation_start: Optional[Callable[[AnimationEvent], None]] = Field(default=None, exclude=True)
    on_animation_complete: Optional[Callable[[AnimationEvent], None]] = Field(default=None, exclude=True)
    on_sequence_complete: Optional[Callable[[AnimationSequence], None]] = Field(default=None, exclude=True)
    
    def register_hourglass(self, entity_id: str, hourglass: HourGlass) -> None:
        """Register an hourglass for animation coordination."""
        self.hourglasses[entity_id] = hourglass
        logging.debug(f"Registered hourglass for animation coordination: {entity_id}")
    
    def unregister_hourglass(self, entity_id: str) -> None:
        """Unregister an hourglass."""
        if entity_id in self.hourglasses:
            del self.hourglasses[entity_id]
            logging.debug(f"Unregistered hourglass: {entity_id}")
    
    def start_animation(self, animation_type: AnimationType, entity_id: str, 
                       duration: float, priority: AnimationPriority = AnimationPriority.NORMAL,
                       blocks_sand_regen: bool = True, blocks_input: bool = False,
                       animation_data: Optional[Dict[str, Any]] = None,
                       callback: Optional[Callable[[], None]] = None) -> str:
        """
        Start a new animation.
        
        Returns the animation ID for tracking.
        """
        # Check if we're at max capacity
        if len(self.active_animations) >= self.max_concurrent_animations:
            # Remove lowest priority finished animations
            self._cleanup_finished_animations()
            
            if len(self.active_animations) >= self.max_concurrent_animations:
                logging.warning("Max concurrent animations reached, skipping new animation")
                return ""
        
        # Adjust duration based on quality settings
        adjusted_duration = duration * self.animation_quality
        
        # Create animation event
        animation_id = f"{entity_id}_{animation_type.value}_{int(time.time() * 1000)}"
        event = AnimationEvent(
            animation_id=animation_id,
            animation_type=animation_type,
            entity_id=entity_id,
            duration=adjusted_duration,
            priority=priority,
            start_time=time.time(),
            end_time=0,  # Will be calculated in __post_init__
            blocks_sand_regen=blocks_sand_regen,
            blocks_input=blocks_input,
            callback=callback,
            data=animation_data or {}
        )
        
        # Start the animation
        self.active_animations[animation_id] = event
        
        # Handle sand regeneration coordination
        if blocks_sand_regen:
            self._pause_sand_regeneration(entity_id)
        
        # Notify callbacks
        if self.on_animation_start:
            self.on_animation_start(event)
        
        logging.debug(f"Started animation: {animation_id} ({animation_type.value}, duration: {adjusted_duration:.2f}s)")
        return animation_id
    
    def create_animation_sequence(self, sequence_id: str, is_parallel: bool = False,
                                completion_callback: Optional[Callable[[], None]] = None) -> AnimationSequence:
        """Create a new animation sequence."""
        sequence = AnimationSequence(
            sequence_id=sequence_id,
            is_parallel=is_parallel,
            completion_callback=completion_callback
        )
        self.animation_sequences[sequence_id] = sequence
        
        logging.debug(f"Created animation sequence: {sequence_id} (parallel: {is_parallel})")
        return sequence
    
    def add_to_sequence(self, sequence_id: str, animation_type: AnimationType, 
                       entity_id: str, duration: float, 
                       priority: AnimationPriority = AnimationPriority.NORMAL,
                       blocks_sand_regen: bool = True, blocks_input: bool = False,
                       animation_data: Optional[Dict[str, Any]] = None,
                       callback: Optional[Callable[[], None]] = None) -> bool:
        """Add an animation to an existing sequence."""
        sequence = self.animation_sequences.get(sequence_id)
        if not sequence:
            logging.warning(f"Animation sequence not found: {sequence_id}")
            return False
        
        # Create animation event
        animation_id = f"{sequence_id}_{entity_id}_{animation_type.value}_{len(sequence.events)}"
        event = AnimationEvent(
            animation_id=animation_id,
            animation_type=animation_type,
            entity_id=entity_id,
            duration=duration * self.animation_quality,
            priority=priority,
            start_time=0,  # Will be set by sequence
            end_time=0,
            blocks_sand_regen=blocks_sand_regen,
            blocks_input=blocks_input,
            callback=callback,
            data=animation_data or {}
        )
        
        sequence.add_animation(event)
        return True
    
    def start_sequence(self, sequence_id: str) -> bool:
        """Start an animation sequence."""
        sequence = self.animation_sequences.get(sequence_id)
        if not sequence:
            logging.warning(f"Animation sequence not found: {sequence_id}")
            return False
        
        # Add all sequence animations to active animations
        for event in sequence.events:
            self.active_animations[event.animation_id] = event
            
            # Handle sand regeneration for each animation
            if event.blocks_sand_regen:
                self._pause_sand_regeneration(event.entity_id)
        
        logging.debug(f"Started animation sequence: {sequence_id} ({len(sequence.events)} animations)")
        return True
    
    def stop_animation(self, animation_id: str) -> bool:
        """Stop a specific animation."""
        if animation_id in self.active_animations:
            event = self.active_animations[animation_id]
            
            # Resume sand regeneration if needed
            if event.blocks_sand_regen:
                self._resume_sand_regeneration(event.entity_id)
            
            # Execute callback if present
            if event.callback:
                try:
                    event.callback()
                except Exception as e:
                    logging.error(f"Error in animation callback: {e}")
            
            del self.active_animations[animation_id]
            logging.debug(f"Stopped animation: {animation_id}")
            return True
        
        return False
    
    def stop_all_animations_for_entity(self, entity_id: str) -> int:
        """Stop all animations for a specific entity."""
        stopped_count = 0
        to_remove = []
        
        for animation_id, event in self.active_animations.items():
            if event.entity_id == entity_id:
                to_remove.append(animation_id)
        
        for animation_id in to_remove:
            if self.stop_animation(animation_id):
                stopped_count += 1
        
        return stopped_count
    
    def pause_all_animations(self) -> None:
        """Pause all animations globally."""
        self.global_animation_paused = True
        
        # Pause all sand regeneration
        for hourglass in self.hourglasses.values():
            hourglass.pause_regeneration()
        
        logging.debug("Paused all animations globally")
    
    def resume_all_animations(self) -> None:
        """Resume all animations globally."""
        self.global_animation_paused = False
        
        # Resume sand regeneration for entities without blocking animations
        for entity_id, hourglass in self.hourglasses.items():
            if not self._entity_has_blocking_animation(entity_id):
                hourglass.resume_regeneration()
        
        logging.debug("Resumed all animations globally")
    
    def update(self, target_fps: int = 60) -> None:
        """Update animation system."""
        if self.global_animation_paused:
            return
        
        # Update timing controller
        should_update, delta_time = self.timing_controller.update(target_fps)
        if not should_update:
            return
        
        # Update active animations
        finished_animations = []
        current_time = time.time()
        
        for animation_id, event in self.active_animations.items():
            if event.is_finished():
                finished_animations.append(animation_id)
        
        # Clean up finished animations
        for animation_id in finished_animations:
            self._finish_animation(animation_id)
        
        # Update animation sequences
        self._update_sequences()
        
        # Update visual system
        sand_visualizer.update_all()
    
    def _finish_animation(self, animation_id: str) -> None:
        """Finish an animation and handle cleanup."""
        event = self.active_animations.get(animation_id)
        if not event:
            return
        
        # Resume sand regeneration if this was blocking it
        if event.blocks_sand_regen:
            self._resume_sand_regeneration(event.entity_id)
        
        # Execute callback
        if event.callback:
            try:
                event.callback()
            except Exception as e:
                logging.error(f"Error in animation callback: {e}")
        
        # Notify completion
        if self.on_animation_complete:
            self.on_animation_complete(event)
        
        # Remove from active animations
        del self.active_animations[animation_id]
        
        logging.debug(f"Finished animation: {animation_id}")
    
    def _update_sequences(self) -> None:
        """Update animation sequences and check for completion."""
        completed_sequences = []
        
        for sequence_id, sequence in self.animation_sequences.items():
            if sequence.is_complete():
                completed_sequences.append(sequence_id)
        
        # Handle completed sequences
        for sequence_id in completed_sequences:
            sequence = self.animation_sequences[sequence_id]
            
            # Execute completion callback
            if sequence.completion_callback:
                try:
                    sequence.completion_callback()
                except Exception as e:
                    logging.error(f"Error in sequence completion callback: {e}")
            
            # Notify completion
            if self.on_sequence_complete:
                self.on_sequence_complete(sequence)
            
            # Remove sequence
            del self.animation_sequences[sequence_id]
            logging.debug(f"Completed animation sequence: {sequence_id}")
    
    def _pause_sand_regeneration(self, entity_id: str) -> None:
        """Pause sand regeneration for a specific entity."""
        hourglass = self.hourglasses.get(entity_id)
        if hourglass:
            hourglass.pause_regeneration()
            logging.debug(f"Paused sand regeneration for {entity_id}")
    
    def _resume_sand_regeneration(self, entity_id: str) -> None:
        """Resume sand regeneration for a specific entity if no blocking animations."""
        if self._entity_has_blocking_animation(entity_id):
            return  # Still has blocking animations
        
        hourglass = self.hourglasses.get(entity_id)
        if hourglass:
            hourglass.resume_regeneration()
            logging.debug(f"Resumed sand regeneration for {entity_id}")
    
    def _entity_has_blocking_animation(self, entity_id: str) -> bool:
        """Check if entity has any active animations that block sand regeneration."""
        for event in self.active_animations.values():
            if event.entity_id == entity_id and event.blocks_sand_regen and event.is_active():
                return True
        
        # Check sequences too
        for sequence in self.animation_sequences.values():
            if sequence.should_block_sand_regen():
                active_events = sequence.get_active_animations()
                if any(event.entity_id == entity_id for event in active_events):
                    return True
        
        return False
    
    def _cleanup_finished_animations(self) -> None:
        """Clean up finished animations to make room for new ones."""
        finished = []
        for animation_id, event in self.active_animations.items():
            if event.is_finished():
                finished.append(animation_id)
        
        for animation_id in finished:
            self._finish_animation(animation_id)
    
    def get_animation_status(self) -> Dict[str, Any]:
        """Get comprehensive animation system status."""
        active_by_type = defaultdict(int)
        active_by_entity = defaultdict(int)
        
        for event in self.active_animations.values():
            active_by_type[event.animation_type.value] += 1
            active_by_entity[event.entity_id] += 1
        
        return {
            'active_animations': len(self.active_animations),
            'active_sequences': len(self.animation_sequences),
            'max_concurrent': self.max_concurrent_animations,
            'global_paused': self.global_animation_paused,
            'animation_quality': self.animation_quality,
            'active_by_type': dict(active_by_type),
            'active_by_entity': dict(active_by_entity),
            'registered_hourglasses': list(self.hourglasses.keys())
        }
    
    def set_animation_quality(self, quality: float) -> None:
        """Set animation quality (affects duration and detail)."""
        self.animation_quality = max(0.1, min(2.0, quality))
        logging.info(f"Animation quality set to {self.animation_quality}")
    
    def get_estimated_completion_time(self) -> float:
        """Get estimated time until all animations complete."""
        if not self.active_animations and not self.animation_sequences:
            return 0.0
        
        max_end_time = 0.0
        current_time = time.time()
        
        # Check active animations
        for event in self.active_animations.values():
            max_end_time = max(max_end_time, event.end_time)
        
        # Check sequences
        for sequence in self.animation_sequences.values():
            if sequence.events:
                sequence_end = max(event.end_time for event in sequence.events)
                max_end_time = max(max_end_time, sequence_end)
        
        return max(0.0, max_end_time - current_time)


# Global animation coordinator instance
animation_coordinator = AnimationCoordinator()