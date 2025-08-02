"""
Enhanced Combat Engine with Sand-Based Action Scheduling

Extends the basic combat system with sophisticated Hour-Glass Initiative
mechanics, including sand-based action queuing, strategic timing, and
advanced combat AI coordination.

Key Features:
- Priority-based action scheduling with sand costs
- Frame-rate independent timing
- Visual feedback integration
- Enemy AI sand management
- Animation-aware action execution

Classes:
- EnhancedCombatAction: Action with sand scheduling
- SandBasedActionQueue: Priority queue for sand-based actions
- EnhancedCombatEngine: Main combat orchestrator with sand integration
"""

import asyncio
import logging
import heapq
import time
from enum import Enum
from typing import List, Dict, Optional, Any, Callable, Tuple
from pydantic import BaseModel, Field
from dataclasses import dataclass
from collections import defaultdict

from .combat import ActionType, CombatPhase, CombatState, CombatEngine
from .hourglass import HourGlass
from .sand_visuals import sand_visualizer


@dataclass
class EnhancedCombatAction:
    """Enhanced combat action with sand scheduling and priority."""
    action_type: ActionType
    actor_id: str
    target_id: Optional[str] = None
    card_id: Optional[str] = None
    data: Dict[str, Any] = None
    timestamp: float = 0.0
    sand_cost: int = 0
    priority: int = 0  # Higher priority = executed first for same timestamp
    scheduled_time: Optional[float] = None  # When action can be executed
    is_queued: bool = False
    validation_callback: Optional[Callable[[], bool]] = None
    animation_duration: float = 0.5  # Expected animation time
    interrupts_regeneration: bool = True  # Whether this action pauses sand regen
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def __lt__(self, other):
        """Comparison for priority queue ordering."""
        if self.scheduled_time != other.scheduled_time:
            return (self.scheduled_time or 0) < (other.scheduled_time or 0)
        return self.priority > other.priority  # Higher priority first
    
    def can_execute(self, hourglass: HourGlass) -> bool:
        """Check if action can be executed now."""
        # Check sand cost
        if not hourglass.can_afford(self.sand_cost):
            return False
        
        # Check scheduled time
        if self.scheduled_time and time.time() < self.scheduled_time:
            return False
        
        # Check custom validation
        if self.validation_callback and not self.validation_callback():
            return False
        
        return True
    
    def get_execution_delay(self, hourglass: HourGlass) -> float:
        """Get time until action can be executed."""
        current_time = time.time()
        
        # Check sand availability timing
        if not hourglass.can_afford(self.sand_cost):
            needed_sand = self.sand_cost - hourglass.current_sand
            sand_delay = needed_sand / hourglass.timer.regeneration_rate
        else:
            sand_delay = 0.0
        
        # Check scheduled time delay
        schedule_delay = max(0.0, (self.scheduled_time or 0) - current_time)
        
        return max(sand_delay, schedule_delay)
    
    def estimate_total_time(self, hourglass: HourGlass) -> float:
        """Estimate total time including execution delay and animation."""
        return self.get_execution_delay(hourglass) + self.animation_duration


class ActionPriority(Enum):
    """Standard action priorities."""
    INTERRUPT = 100      # Immediate interrupts (flee, emergency)
    REACTION = 50        # Reaction abilities
    STANDARD = 10        # Normal actions
    PASSIVE = 0          # End turn, wait actions


class SandBasedActionQueue(BaseModel):
    """
    Advanced action queue that schedules actions based on sand availability.
    
    Uses priority queue for efficient scheduling and supports both
    immediate and delayed execution based on sand costs.
    """
    
    # Priority queue for scheduled actions
    action_heap: List[EnhancedCombatAction] = Field(default_factory=list, exclude=True)
    immediate_actions: List[EnhancedCombatAction] = Field(default_factory=list)
    processing: bool = Field(default=False)
    hourglasses: Dict[str, HourGlass] = Field(default_factory=dict)
    action_history: List[EnhancedCombatAction] = Field(default_factory=list)
    max_history_size: int = Field(default=100)
    animation_queue: List[EnhancedCombatAction] = Field(default_factory=list)
    
    def register_hourglass(self, entity_id: str, hourglass: HourGlass) -> None:
        """Register an hourglass for sand-based scheduling."""
        self.hourglasses[entity_id] = hourglass
        logging.info(f"Registered hourglass for {entity_id}")
    
    def unregister_hourglass(self, entity_id: str) -> None:
        """Remove hourglass from scheduling."""
        if entity_id in self.hourglasses:
            del self.hourglasses[entity_id]
            logging.info(f"Unregistered hourglass for {entity_id}")
    
    def add_action(self, action: EnhancedCombatAction) -> bool:
        """
        Add an action to the queue with sand-based scheduling.
        
        Returns True if action was successfully queued.
        """
        hourglass = self.hourglasses.get(action.actor_id)
        if not hourglass:
            logging.warning(f"No hourglass registered for actor {action.actor_id}")
            return False
        
        # Check if action can be executed immediately
        if action.can_execute(hourglass):
            self.immediate_actions.append(action)
            action.is_queued = True
            logging.debug(f"Action queued immediately: {action.action_type.value} by {action.actor_id}")
        else:
            # Schedule for future execution
            delay = action.get_execution_delay(hourglass)
            action.scheduled_time = time.time() + delay
            heapq.heappush(self.action_heap, action)
            action.is_queued = True
            logging.debug(f"Action scheduled for {delay:.2f}s: {action.action_type.value} by {action.actor_id}")
        
        return True
    
    def get_next_action(self) -> Optional[EnhancedCombatAction]:
        """
        Get the next executable action from the queue.
        
        Checks both immediate actions and scheduled actions
        that are now ready for execution.
        """
        current_time = time.time()
        
        # First, check immediate actions (highest priority)
        if self.immediate_actions:
            # Sort by priority
            self.immediate_actions.sort(key=lambda a: a.priority, reverse=True)
            return self.immediate_actions.pop(0)
        
        # Then check scheduled actions that are ready
        while self.action_heap:
            action = self.action_heap[0]  # Peek at next scheduled action
            
            if action.scheduled_time and action.scheduled_time <= current_time:
                # Action is ready
                heapq.heappop(self.action_heap)
                
                # Validate action can still be executed
                hourglass = self.hourglasses.get(action.actor_id)
                if hourglass and action.can_execute(hourglass):
                    return action
                else:
                    # Reschedule if still valid
                    if hourglass:
                        delay = action.get_execution_delay(hourglass)
                        if delay > 0:
                            action.scheduled_time = current_time + delay
                            heapq.heappush(self.action_heap, action)
                            logging.debug(f"Action rescheduled: {action.action_type.value} by {action.actor_id}")
            else:
                # No more ready actions
                break
        
        return None
    
    def has_actions(self) -> bool:
        """Check if there are actions in the queue."""
        return len(self.immediate_actions) > 0 or len(self.action_heap) > 0
    
    def clear(self) -> None:
        """Clear all actions from the queue."""
        self.immediate_actions.clear()
        self.action_heap.clear()
        self.animation_queue.clear()
    
    def get_actions_by_actor(self, actor_id: str) -> List[EnhancedCombatAction]:
        """Get all actions by a specific actor."""
        actions = [action for action in self.immediate_actions if action.actor_id == actor_id]
        actions.extend([action for action in self.action_heap if action.actor_id == actor_id])
        return actions
    
    def get_next_action_time(self, actor_id: str) -> Optional[float]:
        """Get when the next action by this actor will be executable."""
        actor_actions = self.get_actions_by_actor(actor_id)
        if not actor_actions:
            return None
        
        # Find earliest executable action
        current_time = time.time()
        earliest_time = float('inf')
        
        for action in actor_actions:
            if action in self.immediate_actions:
                return current_time  # Immediate action available
            elif action.scheduled_time:
                earliest_time = min(earliest_time, action.scheduled_time)
        
        return earliest_time if earliest_time != float('inf') else None
    
    def cancel_actions_by_actor(self, actor_id: str) -> int:
        """Cancel all actions by a specific actor. Returns number cancelled."""
        cancelled = 0
        
        # Cancel immediate actions
        original_count = len(self.immediate_actions)
        self.immediate_actions = [a for a in self.immediate_actions if a.actor_id != actor_id]
        cancelled += original_count - len(self.immediate_actions)
        
        # Cancel scheduled actions
        new_heap = [a for a in self.action_heap if a.actor_id != actor_id]
        cancelled += len(self.action_heap) - len(new_heap)
        self.action_heap = new_heap
        heapq.heapify(self.action_heap)
        
        if cancelled > 0:
            logging.info(f"Cancelled {cancelled} actions for actor {actor_id}")
        
        return cancelled
    
    def peek_next_scheduled_time(self) -> Optional[float]:
        """Get the time of the next scheduled action without removing it."""
        if self.immediate_actions:
            return time.time()  # Immediate actions are ready now
        
        if self.action_heap:
            return self.action_heap[0].scheduled_time
        
        return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get detailed queue status for debugging."""
        return {
            'immediate_actions': len(self.immediate_actions),
            'scheduled_actions': len(self.action_heap),
            'animation_queue': len(self.animation_queue),
            'processing': self.processing,
            'registered_hourglasses': list(self.hourglasses.keys()),
            'next_scheduled_time': self.peek_next_scheduled_time(),
            'history_size': len(self.action_history)
        }
    
    def _add_to_history(self, action: EnhancedCombatAction) -> None:
        """Add action to history for analysis."""
        self.action_history.append(action)
        if len(self.action_history) > self.max_history_size:
            self.action_history.pop(0)
    
    def get_action_statistics(self) -> Dict[str, Any]:
        """Get statistics about action execution."""
        if not self.action_history:
            return {}
        
        stats = defaultdict(int)
        total_actions = len(self.action_history)
        
        for action in self.action_history:
            stats[f"{action.action_type.value}_count"] += 1
            stats[f"{action.actor_id}_actions"] += 1
        
        # Convert to percentages
        for key in list(stats.keys()):
            if key.endswith('_count'):
                stats[key.replace('_count', '_percentage')] = (stats[key] / total_actions) * 100
        
        return dict(stats)


class EnhancedCombatEngine(CombatEngine):
    """
    Enhanced combat engine with sophisticated Hour-Glass Initiative mechanics.
    
    Extends the basic combat engine with sand-based scheduling,
    animation coordination, and strategic timing management.
    """
    
    # Additional fields for enhanced functionality
    animation_manager: Optional[Any] = Field(default=None, exclude=True)
    strategic_ai: Optional[Any] = Field(default=None, exclude=True)
    
    def __init__(self, **data):
        super().__init__(**data)
        # Replace the basic action queue with enhanced version
        self.action_queue = SandBasedActionQueue()
        self.animation_manager = AnimationManager()
        self.strategic_ai = None  # Will be set later
    
    def register_combatant_hourglass(self, actor_id: str, hourglass: HourGlass) -> None:
        """Register an hourglass for a combat participant."""
        self.action_queue.register_hourglass(actor_id, hourglass)
        
        # Register with visual system
        is_enemy = actor_id != "player"  # Assume player is the main participant
        sand_visualizer.register_hourglass(actor_id, hourglass, is_enemy=is_enemy)
        
        logging.info(f"Registered combatant {actor_id} with hourglass")
    
    def queue_action(self, action: EnhancedCombatAction) -> bool:
        """
        Queue an enhanced combat action with sand-based scheduling.
        
        Returns True if action was successfully queued.
        """
        if not self.state.is_active():
            return False
        
        # Validate that the actor is a participant
        if action.actor_id not in self.state.participants:
            return False
        
        # Queue action with sand scheduling
        success = self.action_queue.add_action(action)
        
        if success and self.on_combat_event:
            self.on_combat_event("action_queued", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id,
                "sand_cost": action.sand_cost,
                "scheduled_time": action.scheduled_time,
                "immediate": action in self.action_queue.immediate_actions,
                "priority": action.priority
            })
        
        return success
    
    async def process_actions(self) -> None:
        """
        Process all queued actions with animation coordination.
        """
        if self.action_queue.processing:
            return
        
        self.action_queue.processing = True
        
        try:
            while self.action_queue.has_actions() and self.state.is_active():
                action = self.action_queue.get_next_action()
                if action:
                    await self._resolve_enhanced_action(action)
                    
                    # Handle animation timing
                    if action.interrupts_regeneration:
                        await self._handle_animation_timing(action)
        finally:
            self.action_queue.processing = False
    
    async def _resolve_enhanced_action(self, action: EnhancedCombatAction) -> None:
        """
        Resolve an enhanced combat action with sand cost handling.
        """
        if self.on_combat_event:
            self.on_combat_event("action_resolving", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id,
                "sand_cost": action.sand_cost
            })
        
        # Get actor's hourglass
        hourglass = self.action_queue.hourglasses.get(action.actor_id)
        
        # Spend sand for the action
        if hourglass and action.sand_cost > 0:
            if not hourglass.spend_sand(action.sand_cost):
                logging.warning(f"Action failed - insufficient sand: {action.action_type.value} by {action.actor_id}")
                return
            
            # Trigger visual spending animation
            sand_visualizer.trigger_sand_spending(action.actor_id, action.sand_cost)
        
        # Pause sand regeneration if action interrupts it
        if action.interrupts_regeneration and hourglass:
            hourglass.pause_regeneration()
        
        # Resolve action based on type
        try:
            if action.action_type == ActionType.PLAY_CARD:
                await self._resolve_card_play_enhanced(action)
            elif action.action_type == ActionType.ABILITY:
                await self._resolve_ability_enhanced(action)
            elif action.action_type == ActionType.END_TURN:
                await self._resolve_end_turn_enhanced(action)
            elif action.action_type == ActionType.FLEE:
                await self._resolve_flee_enhanced(action)
        except Exception as e:
            logging.error(f"Error resolving action {action.action_type.value}: {e}")
            # Refund sand on error
            if hourglass and action.sand_cost > 0:
                hourglass.set_sand(hourglass.current_sand + action.sand_cost)
            return
        finally:
            # Resume sand regeneration after action
            if action.interrupts_regeneration and hourglass:
                hourglass.resume_regeneration()
        
        # Add to action history
        self.action_queue._add_to_history(action)
        
        if self.on_combat_event:
            self.on_combat_event("action_resolved", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id,
                "sand_spent": action.sand_cost,
                "animation_duration": action.animation_duration
            })
    
    async def _handle_animation_timing(self, action: EnhancedCombatAction) -> None:
        """Handle animation timing and sand regeneration coordination."""
        if action.animation_duration > 0:
            # Pause all sand regeneration during animations
            for hourglass in self.action_queue.hourglasses.values():
                hourglass.pause_regeneration()
            
            # Wait for animation to complete
            await asyncio.sleep(action.animation_duration)
            
            # Resume sand regeneration
            for hourglass in self.action_queue.hourglasses.values():
                hourglass.resume_regeneration()
    
    async def _resolve_card_play_enhanced(self, action: EnhancedCombatAction) -> None:
        """Enhanced card play resolution with sand mechanics."""
        # Placeholder for enhanced card resolution
        await asyncio.sleep(action.animation_duration)
        logging.debug(f"Card played: {action.card_id} by {action.actor_id}")
    
    async def _resolve_ability_enhanced(self, action: EnhancedCombatAction) -> None:
        """Enhanced ability resolution with sand mechanics."""
        # Placeholder for enhanced ability resolution
        await asyncio.sleep(action.animation_duration)
        logging.debug(f"Ability used by {action.actor_id}")
    
    async def _resolve_end_turn_enhanced(self, action: EnhancedCombatAction) -> None:
        """Enhanced end turn resolution."""
        self.state.turn_count += 1
        logging.debug(f"Turn ended by {action.actor_id}, turn count: {self.state.turn_count}")
    
    async def _resolve_flee_enhanced(self, action: EnhancedCombatAction) -> None:
        """Enhanced flee resolution."""
        self.end_combat(winner=None)
        logging.info(f"Combat ended - {action.actor_id} fled")
    
    def get_valid_actions(self, actor_id: str) -> List[ActionType]:
        """Get list of valid actions for an actor based on sand availability."""
        if not self.state.is_active() or actor_id not in self.state.participants:
            return []
        
        hourglass = self.action_queue.hourglasses.get(actor_id)
        if not hourglass:
            return []
        
        valid_actions = []
        
        # Always available actions (no sand cost)
        valid_actions.extend([ActionType.END_TURN, ActionType.FLEE])
        
        # Sand-dependent actions
        if hourglass.current_sand >= 1:  # Minimum sand for card play
            valid_actions.append(ActionType.PLAY_CARD)
        
        if hourglass.current_sand >= 2:  # Abilities cost more
            valid_actions.append(ActionType.ABILITY)
        
        return valid_actions
    
    def get_action_costs(self, actor_id: str) -> Dict[ActionType, int]:
        """Get sand costs for different action types."""
        # Default sand costs - can be customized per actor
        return {
            ActionType.PLAY_CARD: 1,
            ActionType.ABILITY: 2,
            ActionType.END_TURN: 0,
            ActionType.FLEE: 0
        }
    
    def can_actor_afford_action(self, actor_id: str, action_type: ActionType) -> bool:
        """Check if actor can afford a specific action type."""
        hourglass = self.action_queue.hourglasses.get(actor_id)
        if not hourglass:
            return False
        
        costs = self.get_action_costs(actor_id)
        cost = costs.get(action_type, 0)
        return hourglass.can_afford(cost)
    
    def get_time_until_affordable(self, actor_id: str, action_type: ActionType) -> float:
        """Get time until actor can afford a specific action."""
        hourglass = self.action_queue.hourglasses.get(actor_id)
        if not hourglass:
            return float('inf')
        
        costs = self.get_action_costs(actor_id)
        cost = costs.get(action_type, 0)
        
        if hourglass.can_afford(cost):
            return 0.0
        
        needed_sand = cost - hourglass.current_sand
        return needed_sand / hourglass.timer.regeneration_rate
    
    def get_combat_status(self) -> Dict[str, Any]:
        """Get comprehensive combat status including sand information."""
        status = {
            'phase': self.state.phase.value,
            'participants': self.state.participants,
            'turn_count': self.state.turn_count,
            'queue_status': self.action_queue.get_queue_status(),
            'action_statistics': self.action_queue.get_action_statistics(),
            'hourglasses': {}
        }
        
        # Add hourglass status for each participant
        for actor_id in self.state.participants:
            hourglass = self.action_queue.hourglasses.get(actor_id)
            if hourglass:
                status['hourglasses'][actor_id] = hourglass.get_regeneration_status()
        
        return status
    
    def predict_action_execution_time(self, action: EnhancedCombatAction) -> float:
        """Predict when an action will be executed if queued now."""
        hourglass = self.action_queue.hourglasses.get(action.actor_id)
        if not hourglass:
            return float('inf')
        
        return time.time() + action.estimate_total_time(hourglass)


class AnimationManager:
    """
    Manages animation timing and coordination with sand regeneration.
    
    Ensures that sand regeneration is properly paused during animations
    and provides smooth visual feedback.
    """
    
    def __init__(self):
        self.active_animations: Dict[str, float] = {}  # entity_id -> end_time
        self.global_pause = False
    
    def start_animation(self, entity_id: str, duration: float) -> None:
        """Start an animation for an entity."""
        end_time = time.time() + duration
        self.active_animations[entity_id] = end_time
        logging.debug(f"Started animation for {entity_id}, duration: {duration:.2f}s")
    
    def is_animating(self, entity_id: str = None) -> bool:
        """Check if animations are active."""
        current_time = time.time()
        
        if entity_id:
            return entity_id in self.active_animations and self.active_animations[entity_id] > current_time
        
        # Check if any animations are active
        return any(end_time > current_time for end_time in self.active_animations.values()) or self.global_pause
    
    def update(self) -> None:
        """Update animation state and clean up finished animations."""
        current_time = time.time()
        
        # Remove finished animations
        finished = [entity_id for entity_id, end_time in self.active_animations.items() if end_time <= current_time]
        for entity_id in finished:
            del self.active_animations[entity_id]
            logging.debug(f"Animation finished for {entity_id}")
    
    def pause_all(self) -> None:
        """Pause all sand regeneration globally."""
        self.global_pause = True
    
    def resume_all(self) -> None:
        """Resume all sand regeneration globally."""
        self.global_pause = False
    
    def get_remaining_time(self, entity_id: str) -> float:
        """Get remaining animation time for an entity."""
        if entity_id not in self.active_animations:
            return 0.0
        
        return max(0.0, self.active_animations[entity_id] - time.time())