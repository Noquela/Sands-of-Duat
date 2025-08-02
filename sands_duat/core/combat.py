"""
Combat Engine and Action Queue System

Manages the tactical combat system with Hour-Glass Initiative timing,
action resolution, and combat state management.

Key Features:
- Action queue with timing-based resolution
- Combat state management
- Integration with Hour-Glass sand costs
- Animation and effect coordination

Classes:
- CombatEngine: Main combat orchestrator
- ActionQueue: Manages queued actions and timing
- CombatAction: Individual combat actions
- CombatState: Current combat status and participants
"""

import asyncio
from enum import Enum
from typing import List, Dict, Optional, Any, Callable
from pydantic import BaseModel, Field
from dataclasses import dataclass
import time


class ActionType(Enum):
    """Types of combat actions."""
    PLAY_CARD = "play_card"
    ABILITY = "ability"
    END_TURN = "end_turn"
    FLEE = "flee"


class CombatPhase(Enum):
    """Combat phases."""
    SETUP = "setup"
    ACTIVE = "active"
    RESOLUTION = "resolution"
    ENDED = "ended"


@dataclass
class CombatAction:
    """Represents a single combat action."""
    action_type: ActionType
    actor_id: str
    target_id: Optional[str] = None
    card_id: Optional[str] = None
    data: Dict[str, Any] = None
    timestamp: float = 0.0
    sand_cost: int = 0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class ActionQueue(BaseModel):
    """
    Manages the queue of combat actions with timing considerations.
    """
    
    actions: List[CombatAction] = Field(default_factory=list)
    processing: bool = Field(default=False)
    
    def add_action(self, action: CombatAction) -> None:
        """Add an action to the queue."""
        self.actions.append(action)
    
    def get_next_action(self) -> Optional[CombatAction]:
        """Get the next action to process (FIFO)."""
        if not self.actions:
            return None
        return self.actions.pop(0)
    
    def has_actions(self) -> bool:
        """Check if there are actions in the queue."""
        return len(self.actions) > 0
    
    def clear(self) -> None:
        """Clear all actions from the queue."""
        self.actions.clear()
    
    def get_actions_by_actor(self, actor_id: str) -> List[CombatAction]:
        """Get all actions by a specific actor."""
        return [action for action in self.actions if action.actor_id == actor_id]


class CombatState(BaseModel):
    """
    Represents the current state of combat.
    """
    
    phase: CombatPhase = Field(default=CombatPhase.SETUP)
    participants: List[str] = Field(default_factory=list)
    current_actor: Optional[str] = Field(default=None)
    turn_count: int = Field(default=0)
    combat_id: str = Field(default="")
    start_time: float = Field(default_factory=time.time)
    
    def add_participant(self, participant_id: str) -> None:
        """Add a participant to combat."""
        if participant_id not in self.participants:
            self.participants.append(participant_id)
    
    def remove_participant(self, participant_id: str) -> None:
        """Remove a participant from combat."""
        if participant_id in self.participants:
            self.participants.remove(participant_id)
    
    def get_combat_duration(self) -> float:
        """Get the duration of the current combat in seconds."""
        return time.time() - self.start_time
    
    def is_active(self) -> bool:
        """Check if combat is currently active."""
        return self.phase == CombatPhase.ACTIVE


class CombatEngine(BaseModel):
    """
    Main combat engine that orchestrates Hour-Glass Initiative combat.
    
    Manages action queues, combat state, and coordinates with
    other systems like cards and hour-glass timers.
    """
    
    state: CombatState = Field(default_factory=CombatState)
    action_queue: ActionQueue = Field(default_factory=ActionQueue)
    on_combat_event: Optional[Callable[[str, Dict[str, Any]], None]] = Field(default=None, exclude=True)
    
    def start_combat(self, participants: List[str], combat_id: str = "") -> None:
        """Initialize a new combat encounter."""
        self.state = CombatState(
            phase=CombatPhase.ACTIVE,
            participants=participants.copy(),
            combat_id=combat_id or f"combat_{int(time.time())}"
        )
        self.action_queue.clear()
        
        if self.on_combat_event:
            self.on_combat_event("combat_started", {
                "participants": participants,
                "combat_id": self.state.combat_id
            })
    
    def end_combat(self, winner: Optional[str] = None) -> None:
        """End the current combat encounter."""
        self.state.phase = CombatPhase.ENDED
        self.action_queue.clear()
        
        if self.on_combat_event:
            self.on_combat_event("combat_ended", {
                "winner": winner,
                "duration": self.state.get_combat_duration(),
                "turn_count": self.state.turn_count
            })
    
    def queue_action(self, action: CombatAction) -> bool:
        """
        Queue a combat action for processing.
        
        Returns True if action was successfully queued.
        """
        if not self.state.is_active():
            return False
        
        # Validate that the actor is a participant
        if action.actor_id not in self.state.participants:
            return False
        
        self.action_queue.add_action(action)
        
        if self.on_combat_event:
            self.on_combat_event("action_queued", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id,
                "sand_cost": action.sand_cost
            })
        
        return True
    
    async def process_actions(self) -> None:
        """
        Process all queued actions.
        
        This is an async method to allow for animation timing
        and other async operations during action resolution.
        """
        if self.action_queue.processing:
            return
        
        self.action_queue.processing = True
        
        try:
            while self.action_queue.has_actions() and self.state.is_active():
                action = self.action_queue.get_next_action()
                if action:
                    await self._resolve_action(action)
        finally:
            self.action_queue.processing = False
    
    async def _resolve_action(self, action: CombatAction) -> None:
        """
        Resolve a single combat action.
        
        This method handles the actual game logic for different
        types of actions and coordinates with other systems.
        """
        if self.on_combat_event:
            self.on_combat_event("action_resolving", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id
            })
        
        # Basic action resolution - to be expanded
        if action.action_type == ActionType.PLAY_CARD:
            await self._resolve_card_play(action)
        elif action.action_type == ActionType.ABILITY:
            await self._resolve_ability(action)
        elif action.action_type == ActionType.END_TURN:
            await self._resolve_end_turn(action)
        elif action.action_type == ActionType.FLEE:
            await self._resolve_flee(action)
        
        if self.on_combat_event:
            self.on_combat_event("action_resolved", {
                "action_type": action.action_type.value,
                "actor_id": action.actor_id
            })
    
    async def _resolve_card_play(self, action: CombatAction) -> None:
        """Resolve playing a card."""
        # Placeholder for card resolution logic
        await asyncio.sleep(0.1)  # Simulate animation time
    
    async def _resolve_ability(self, action: CombatAction) -> None:
        """Resolve using an ability."""
        # Placeholder for ability resolution logic
        await asyncio.sleep(0.1)  # Simulate animation time
    
    async def _resolve_end_turn(self, action: CombatAction) -> None:
        """Resolve ending a turn."""
        self.state.turn_count += 1
        # Placeholder for end turn logic
    
    async def _resolve_flee(self, action: CombatAction) -> None:
        """Resolve fleeing from combat."""
        self.end_combat(winner=None)
    
    def get_valid_actions(self, actor_id: str) -> List[ActionType]:
        """Get list of valid actions for an actor."""
        if not self.state.is_active() or actor_id not in self.state.participants:
            return []
        
        # Basic action validation - to be expanded
        valid_actions = [ActionType.END_TURN, ActionType.FLEE]
        
        # Add more actions based on game state
        valid_actions.extend([ActionType.PLAY_CARD, ActionType.ABILITY])
        
        return valid_actions