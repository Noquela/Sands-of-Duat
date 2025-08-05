"""
Initiative Queue System

Implements the Hour-Glass based action queue where actions execute based on
sand accumulation timing rather than traditional turns.

Key Features:
- Actions queue when sand is available
- Execution happens automatically when timing is met
- Reaction windows for instant responses
- Continuous flow without discrete turns
"""

import time
import logging
from typing import List, Dict, Any, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel, Field

from .cards import Card
from .hourglass import HourGlass


class ActionType(Enum):
    """Types of actions that can be queued."""
    PLAY_CARD = "play_card"
    END_TURN = "end_turn"
    REACTION = "reaction"
    ABILITY = "ability"


class ActionPriority(Enum):
    """Priority levels for action execution."""
    INSTANT = 0      # Interrupts, reactions (execute immediately)
    HIGH = 1         # Fast actions, cheap cards
    NORMAL = 2       # Standard card plays
    LOW = 3          # Expensive abilities, end turn


@dataclass
class QueuedAction:
    """Represents an action waiting to be executed."""
    action_id: str
    action_type: ActionType
    priority: ActionPriority
    sand_cost: int
    cast_time: float = 0.0  # Time required to cast this action
    card: Optional[Card] = None
    target: Optional[Any] = None
    metadata: Dict[str, Any] = None
    queued_at: float = 0.0
    cast_started_at: Optional[float] = None  # When casting began
    
    def __post_init__(self):
        if self.queued_at == 0.0:
            self.queued_at = time.perf_counter()
        if self.metadata is None:
            self.metadata = {}
        # Set cast time from card if available
        if self.card and hasattr(self.card, 'cast_time'):
            self.cast_time = self.card.cast_time


class InitiativeQueue:
    """
    Manages the queue of actions based on Hour-Glass sand timing.
    
    Actions are queued when players have intent, but execute only when
    sand requirements are met and timing allows.
    """
    
    def __init__(self, player_hourglass: HourGlass, enemy_hourglass: HourGlass):
        self.player_hourglass = player_hourglass
        self.enemy_hourglass = enemy_hourglass
        
        # Separate queues for each participant
        self.player_queue: List[QueuedAction] = []
        self.enemy_queue: List[QueuedAction] = []
        
        # Reaction window timing
        self.reaction_window_duration = 1.5  # seconds
        self.current_reaction_window: Optional[Dict[str, Any]] = None
        
        # Callbacks for action execution
        self.on_action_executed: Optional[Callable[[QueuedAction, str], None]] = None
        self.on_reaction_window_opened: Optional[Callable[[QueuedAction], None]] = None
        self.on_queue_changed: Optional[Callable[[], None]] = None
        
        self.logger = logging.getLogger(__name__)
    
    def queue_player_action(self, action_type: ActionType, sand_cost: int, 
                           card: Optional[Card] = None, target: Optional[Any] = None,
                           priority: ActionPriority = ActionPriority.NORMAL) -> bool:
        """
        Queue a player action if they have sufficient sand or can wait for it.
        
        Returns:
            True if action was queued, False if rejected
        """
        if not self._can_queue_action(self.player_hourglass, sand_cost):
            return False
        
        action = QueuedAction(
            action_id=f"player_{len(self.player_queue)}_{int(time.perf_counter() * 1000)}",
            action_type=action_type,
            priority=priority,
            sand_cost=sand_cost,
            card=card,
            target=target
        )
        
        self.player_queue.append(action)
        self._sort_queue(self.player_queue)
        
        self.logger.info(f"Queued player action: {action_type.value} (cost: {sand_cost})")
        
        if self.on_queue_changed:
            self.on_queue_changed()
        
        return True
    
    def queue_enemy_action(self, action_type: ActionType, sand_cost: int,
                          card: Optional[Card] = None, target: Optional[Any] = None,
                          priority: ActionPriority = ActionPriority.NORMAL) -> bool:
        """Queue an enemy action."""
        if not self._can_queue_action(self.enemy_hourglass, sand_cost):
            return False
        
        action = QueuedAction(
            action_id=f"enemy_{len(self.enemy_queue)}_{int(time.perf_counter() * 1000)}",
            action_type=action_type,
            priority=priority,
            sand_cost=sand_cost,
            card=card,
            target=target
        )
        
        self.enemy_queue.append(action)
        self._sort_queue(self.enemy_queue)
        
        self.logger.info(f"Queued enemy action: {action_type.value} (cost: {sand_cost})")
        
        if self.on_queue_changed:
            self.on_queue_changed()
        
        return True
    
    def update(self, delta_time: float) -> List[QueuedAction]:
        """
        Update the queue system and return any actions ready to execute.
        
        Returns:
            List of actions that should be executed this frame
        """
        executed_actions = []
        
        # Update hourglasses
        self.player_hourglass.update_sand()
        self.enemy_hourglass.update_sand()
        
        # Update reaction window
        if self.current_reaction_window:
            self.current_reaction_window['time_remaining'] -= delta_time
            if self.current_reaction_window['time_remaining'] <= 0:
                self.current_reaction_window = None
                self.logger.debug("Reaction window closed")
        
        # Process ready actions
        executed_actions.extend(self._process_queue(self.player_queue, self.player_hourglass, "player"))
        executed_actions.extend(self._process_queue(self.enemy_queue, self.enemy_hourglass, "enemy"))
        
        return executed_actions
    
    def _process_queue(self, queue: List[QueuedAction], hourglass: HourGlass, owner: str) -> List[QueuedAction]:
        """Process a specific queue and return executed actions."""
        executed_actions = []
        
        # Check actions in priority order
        i = 0
        while i < len(queue):
            action = queue[i]
            current_time = time.perf_counter()
            
            # Check if action can start casting (has required sand and isn't casting)
            if self._can_start_casting(action, hourglass, current_time):
                # Start casting process
                action.cast_started_at = current_time
                # Spend sand immediately when casting starts
                if hourglass.spend_sand(action.sand_cost):
                    self.logger.info(f"{owner} started casting: {action.action_type.value} (cast time: {action.cast_time}s)")
                    i += 1
                else:
                    # Shouldn't happen, but handle gracefully
                    self.logger.warning(f"Failed to spend sand for {owner} action: {action.action_type.value}")
                    i += 1
            
            # Check if action finished casting and can execute
            elif self._is_cast_complete(action, current_time):
                # Remove from queue and execute
                queue.pop(i)
                
                # Open reaction window for non-instant actions
                if action.priority != ActionPriority.INSTANT and action.action_type == ActionType.PLAY_CARD:
                    self._open_reaction_window(action)
                
                executed_actions.append(action)
                self.logger.info(f"Executed {owner} action: {action.action_type.value}")
                
                if self.on_action_executed:
                    self.on_action_executed(action, owner)
            else:
                i += 1
        
        return executed_actions
    
    def _can_queue_action(self, hourglass: HourGlass, sand_cost: int) -> bool:
        """Check if an action can be queued (not necessarily executed immediately)."""
        # Allow queueing if will be affordable within reasonable time
        if hourglass.can_afford(sand_cost):
            return True
        
        # Allow queueing if action will be affordable within 10 seconds
        max_wait_time = 10.0
        time_to_afford = (sand_cost - hourglass.current_sand) / hourglass.regeneration_rate
        
        return time_to_afford <= max_wait_time
    
    def _can_start_casting(self, action: QueuedAction, hourglass: HourGlass, current_time: float) -> bool:
        """Check if an action can start casting."""
        # Already casting
        if action.cast_started_at is not None:
            return False
        
        # Must have sufficient sand
        if not hourglass.can_afford(action.sand_cost):
            return False
        
        # Instant actions bypass casting
        if action.priority == ActionPriority.INSTANT:
            return True
        
        # Other actions respect reaction window
        if self.current_reaction_window and action.priority != ActionPriority.INSTANT:
            return False
        
        return True
    
    def _is_cast_complete(self, action: QueuedAction, current_time: float) -> bool:
        """Check if an action has finished casting and is ready to execute."""
        if action.cast_started_at is None:
            return False
        
        # Instant actions execute immediately
        if action.priority == ActionPriority.INSTANT or action.cast_time <= 0:
            return True
        
        # Check if cast time has elapsed
        time_elapsed = current_time - action.cast_started_at
        return time_elapsed >= action.cast_time
    
    def _can_execute_action(self, action: QueuedAction, hourglass: HourGlass) -> bool:
        """Check if an action is ready to execute (legacy method for compatibility)."""
        current_time = time.perf_counter()
        return self._is_cast_complete(action, current_time)
    
    def _sort_queue(self, queue: List[QueuedAction]) -> None:
        """Sort queue by priority (instant first, then by queue time)."""
        queue.sort(key=lambda x: (x.priority.value, x.queued_at))
    
    def _open_reaction_window(self, triggering_action: QueuedAction) -> None:
        """Open a reaction window for responding to an action."""
        self.current_reaction_window = {
            'triggering_action': triggering_action,
            'time_remaining': self.reaction_window_duration
        }
        
        self.logger.debug(f"Opened reaction window for: {triggering_action.action_type.value}")
        
        if self.on_reaction_window_opened:
            self.on_reaction_window_opened(triggering_action)
    
    def queue_reaction(self, reacting_player: str, reaction_card: Card, target: Optional[Any] = None) -> bool:
        """
        Queue a reaction during a reaction window.
        
        Args:
            reacting_player: "player" or "enemy"
            reaction_card: Card with instant/reaction ability
            target: Optional target for the reaction
        """
        if not self.current_reaction_window:
            return False
        
        if not hasattr(reaction_card, 'keywords') or 'instant' not in reaction_card.keywords:
            return False
        
        # Determine which queue to use
        if reacting_player == "player":
            return self.queue_player_action(
                ActionType.REACTION,
                reaction_card.sand_cost,
                reaction_card,
                target,
                ActionPriority.INSTANT
            )
        else:
            return self.queue_enemy_action(
                ActionType.REACTION,
                reaction_card.sand_cost,
                reaction_card,
                target,
                ActionPriority.INSTANT
            )
    
    def clear_queue(self, owner: str) -> None:
        """Clear all queued actions for a participant."""
        if owner == "player":
            self.player_queue.clear()
        elif owner == "enemy":
            self.enemy_queue.clear()
        
        if self.on_queue_changed:
            self.on_queue_changed()
    
    def get_queue_preview(self, owner: str) -> List[Dict[str, Any]]:
        """Get a preview of queued actions for UI display."""
        queue = self.player_queue if owner == "player" else self.enemy_queue
        hourglass = self.player_hourglass if owner == "player" else self.enemy_hourglass
        current_time = time.perf_counter()
        
        preview = []
        for action in queue:
            # Determine action status
            if action.cast_started_at is not None:
                # Currently casting
                if self._is_cast_complete(action, current_time):
                    status = "READY"
                    time_remaining = 0.0
                else:
                    status = "CASTING"
                    time_remaining = action.cast_time - (current_time - action.cast_started_at)
            elif hourglass.can_afford(action.sand_cost):
                # Can start casting
                status = "READY TO CAST"
                time_remaining = action.cast_time
            else:
                # Waiting for sand
                status = "WAITING FOR SAND"
                sand_needed = action.sand_cost - hourglass.current_sand
                time_to_afford = sand_needed / hourglass.regeneration_rate
                time_remaining = time_to_afford + action.cast_time
            
            preview.append({
                'action_type': action.action_type.value,
                'card_name': action.card.name if action.card else None,
                'sand_cost': action.sand_cost,
                'cast_time': action.cast_time,
                'time_remaining': time_remaining,
                'status': status,
                'priority': action.priority.value,
                'is_casting': action.cast_started_at is not None
            })
        
        return preview
    
    def is_reaction_window_open(self) -> bool:
        """Check if a reaction window is currently open."""
        return self.current_reaction_window is not None
    
    def get_reaction_window_time_remaining(self) -> float:
        """Get remaining time for current reaction window."""
        if not self.current_reaction_window:
            return 0.0
        return max(0.0, self.current_reaction_window['time_remaining'])