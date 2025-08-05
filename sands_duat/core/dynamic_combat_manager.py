"""
Dynamic Combat Manager with Initiative Queue System

Replaces turn-based combat with dynamic Hour-Glass timing where actions
execute based on sand accumulation rather than discrete turns.

Features:
- Initiative Queue System integration
- Real-time action timing
- Reaction windows for instant responses
- Continuous sand regeneration mechanics
- Dynamic enemy AI that responds to timing
"""

import logging
import random
import time
from enum import Enum
from typing import List, Dict, Optional, Any, Callable, Union
from dataclasses import dataclass, field

from .hourglass import HourGlass
from .cards import Card, CardEffect, EffectType, TargetType, CardType
from .action_queue import InitiativeQueue, ActionType, ActionPriority, QueuedAction


class CombatState(Enum):
    """Current state of dynamic combat."""
    SETUP = "setup"
    ACTIVE = "active"           # Continuous action/reaction flow
    REACTION_WINDOW = "reaction_window"
    RESOLUTION = "resolution"
    VICTORY = "victory"
    DEFEAT = "defeat"


@dataclass
class CombatEntity:
    """Represents a participant in dynamic combat."""
    id: str
    name: str
    health: int
    max_health: int
    hourglass: HourGlass
    deck: List[Card] = field(default_factory=list)
    hand: List[Card] = field(default_factory=list)
    discard_pile: List[Card] = field(default_factory=list)
    temporary_effects: List[Dict[str, Any]] = field(default_factory=list)
    
    def draw_card(self) -> Optional[Card]:
        """Draw a card from deck to hand."""
        if not self.deck and self.discard_pile:
            # Shuffle discard pile back into deck
            self.deck = self.discard_pile.copy()
            self.discard_pile.clear()
            random.shuffle(self.deck)
        
        if self.deck:
            card = self.deck.pop()
            self.hand.append(card)
            return card
        return None
    
    def discard_card(self, card: Card) -> None:
        """Move a card from hand to discard pile."""
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)


class DynamicCombatManager:
    """
    Manages dynamic combat using Initiative Queue System.
    
    No more discrete turns - actions execute when sand is available
    and timing conditions are met.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Combat state
        self.state = CombatState.SETUP
        self.player: Optional[CombatEntity] = None
        self.enemy: Optional[CombatEntity] = None
        self.initiative_queue: Optional[InitiativeQueue] = None
        
        # Combat metrics
        self.combat_start_time = 0.0
        self.actions_executed = 0
        self.total_sand_spent = 0
        
        # Event callbacks
        self.on_state_changed: Optional[Callable[[CombatState], None]] = None
        self.on_action_executed: Optional[Callable[[QueuedAction, str], None]] = None
        self.on_reaction_window: Optional[Callable[[QueuedAction], None]] = None
        self.on_health_changed: Optional[Callable[[str, int, int], None]] = None
        self.on_combat_ended: Optional[Callable[[bool], None]] = None
        
        # Enemy AI timing
        self.enemy_action_cooldown = 0.0
        self.enemy_action_base_delay = 4.0  # Base delay between enemy actions (slower!)
        
        self.logger.info("Dynamic Combat Manager initialized")
    
    def setup_combat(self, player_deck: List[Card], enemy_id: str) -> None:
        """Initialize combat with dynamic timing."""
        self.logger.info(f"Setting up dynamic combat vs {enemy_id}")
        
        # Create combat entities
        self.player = CombatEntity(
            id="player",
            name="Player",
            health=50,
            max_health=50,
            hourglass=HourGlass(current_sand=0, max_sand=6),
            deck=player_deck.copy()
        )
        
        # Create enemy (simplified for now)
        enemy_deck = self._create_enemy_deck(enemy_id)
        self.enemy = CombatEntity(
            id=enemy_id,
            name=enemy_id.replace('_', ' ').title(),
            health=25,  # Lower enemy health
            max_health=25,
            hourglass=HourGlass(current_sand=0, max_sand=6),
            deck=enemy_deck
        )
        
        # Initialize Initiative Queue
        self.initiative_queue = InitiativeQueue(
            self.player.hourglass,
            self.enemy.hourglass
        )
        
        # Set up queue callbacks
        self.initiative_queue.on_action_executed = self._handle_action_executed
        self.initiative_queue.on_reaction_window_opened = self._handle_reaction_window
        self.initiative_queue.on_queue_changed = self._handle_queue_changed
        
        # Initial draws
        for _ in range(5):  # Draw starting hand
            self.player.draw_card()
            self.enemy.draw_card()
        
        self.combat_start_time = time.perf_counter()
        self.state = CombatState.ACTIVE
        
        # Start enemy AI
        self.enemy_action_cooldown = self.enemy_action_base_delay
        
        self.logger.info("Dynamic combat setup complete")
        
        if self.on_state_changed:
            self.on_state_changed(self.state)
    
    def update(self, delta_time: float) -> None:
        """Update dynamic combat state."""
        if self.state not in [CombatState.ACTIVE, CombatState.REACTION_WINDOW]:
            return
        
        if not self.initiative_queue:
            return
        
        # Update initiative queue (handles sand regeneration and action execution)
        executed_actions = self.initiative_queue.update(delta_time)
        
        # Process executed actions
        for action in executed_actions:
            self._process_executed_action(action)
        
        # Update reaction window state
        if self.initiative_queue.is_reaction_window_open():
            if self.state != CombatState.REACTION_WINDOW:
                self.state = CombatState.REACTION_WINDOW
                if self.on_state_changed:
                    self.on_state_changed(self.state)
        else:
            if self.state == CombatState.REACTION_WINDOW:
                self.state = CombatState.ACTIVE
                if self.on_state_changed:
                    self.on_state_changed(self.state)
        
        # Update enemy AI
        self._update_enemy_ai(delta_time)
        
        # Check win/loss conditions
        self._check_combat_end()
    
    def queue_player_card(self, card: Card, target: Optional[Any] = None) -> bool:
        """Queue a player card for execution when sand is available."""
        if not self.initiative_queue or not self.player:
            return False
        
        if card not in self.player.hand:
            self.logger.warning(f"Player tried to play card not in hand: {card.name}")
            return False
        
        # Determine action priority based on card properties
        priority = ActionPriority.NORMAL
        if hasattr(card, 'keywords'):
            if 'instant' in card.keywords:
                priority = ActionPriority.INSTANT
            elif 'fast' in card.keywords:
                priority = ActionPriority.HIGH
        
        # Queue the action
        success = self.initiative_queue.queue_player_action(
            ActionType.PLAY_CARD,
            card.sand_cost,
            card,
            target,
            priority
        )
        
        if success:
            self.logger.info(f"Queued player card: {card.name} (cost: {card.sand_cost})")
        else:
            self.logger.info(f"Failed to queue player card: {card.name} (insufficient sand or queue full)")
        
        return success
    
    def queue_player_reaction(self, reaction_card: Card, target: Optional[Any] = None) -> bool:
        """Queue a player reaction during a reaction window."""
        if not self.initiative_queue:
            return False
        
        return self.initiative_queue.queue_reaction("player", reaction_card, target)
    
    def _process_executed_action(self, action: QueuedAction) -> None:
        """Process an action that was executed by the queue."""
        self.actions_executed += 1
        self.total_sand_spent += action.sand_cost
        
        if action.action_type == ActionType.PLAY_CARD and action.card:
            self._execute_card_effects(action)
        
        # Draw replacement card for played cards
        owner = "player" if action.action_id.startswith("player") else "enemy"
        entity = self.player if owner == "player" else self.enemy
        
        if entity and action.card and action.card in entity.hand:
            entity.discard_card(action.card)
            entity.draw_card()
    
    def _execute_card_effects(self, action: QueuedAction) -> None:
        """Execute the effects of a played card."""
        if not action.card:
            return
        
        owner = "player" if action.action_id.startswith("player") else "enemy"
        caster = self.player if owner == "player" else self.enemy
        target_entity = self.enemy if owner == "player" else self.player
        
        if not caster or not target_entity:
            return
        
        self.logger.info(f"{caster.name} plays {action.card.name}")
        
        # Apply card effects (simplified implementation)
        for effect in action.card.effects:
            self._apply_effect(effect, caster, target_entity)
    
    def _apply_effect(self, effect: CardEffect, caster: CombatEntity, target: CombatEntity) -> None:
        """Apply a single card effect."""
        if effect.effect_type == EffectType.DAMAGE:
            old_health = target.health
            target.health = max(0, target.health - effect.value)
            
            self.logger.info(f"{effect.value} damage to {target.name}: {old_health} -> {target.health}")
            
            if self.on_health_changed:
                self.on_health_changed(target.id, old_health, target.health)
        
        elif effect.effect_type == EffectType.HEAL:
            old_health = caster.health
            caster.health = min(caster.max_health, caster.health + effect.value)
            
            self.logger.info(f"{effect.value} healing to {caster.name}: {old_health} -> {caster.health}")
            
            if self.on_health_changed:
                self.on_health_changed(caster.id, old_health, caster.health)
        
        elif effect.effect_type == EffectType.GAIN_SAND:
            old_sand = caster.hourglass.current_sand
            caster.hourglass.current_sand = min(
                caster.hourglass.max_sand,
                caster.hourglass.current_sand + effect.value
            )
            
            self.logger.info(f"{effect.value} sand to {caster.name}: {old_sand} -> {caster.hourglass.current_sand}")
    
    def _update_enemy_ai(self, delta_time: float) -> None:
        """Update enemy AI decision making."""
        if not self.enemy or not self.initiative_queue:
            return
        
        self.enemy_action_cooldown -= delta_time
        
        # Enemy tries to queue actions when cooldown expires
        if self.enemy_action_cooldown <= 0:
            self._enemy_consider_action()
            self.enemy_action_cooldown = self.enemy_action_base_delay + random.uniform(-0.5, 0.5)
    
    def _enemy_consider_action(self) -> None:
        """Enemy AI considers what action to take."""
        if not self.enemy or not self.initiative_queue:
            return
        
        # Simple AI: play a random affordable card
        affordable_cards = [
            card for card in self.enemy.hand 
            if self.enemy.hourglass.can_afford(card.sand_cost)
        ]
        
        if affordable_cards:
            card_to_play = random.choice(affordable_cards)
            
            success = self.initiative_queue.queue_enemy_action(
                ActionType.PLAY_CARD,
                card_to_play.sand_cost,
                card_to_play,
                self.player,
                ActionPriority.NORMAL
            )
            
            if success:
                self.logger.info(f"Enemy queued: {card_to_play.name}")
        else:
            # If no cards are affordable, queue a "wait" action or pass
            pass
    
    def _check_combat_end(self) -> None:
        """Check if combat should end."""
        if not self.player or not self.enemy:
            return
        
        if self.player.health <= 0:
            self.state = CombatState.DEFEAT
            self.logger.info("Combat ended - Player defeated")
            if self.on_state_changed:
                self.on_state_changed(self.state)
            if self.on_combat_ended:
                self.on_combat_ended(False)
        
        elif self.enemy.health <= 0:
            self.state = CombatState.VICTORY
            self.logger.info("Combat ended - Player victory")
            if self.on_state_changed:
                self.on_state_changed(self.state)
            if self.on_combat_ended:
                self.on_combat_ended(True)
    
    def _create_enemy_deck(self, enemy_id: str) -> List[Card]:
        """Create a simple enemy deck."""
        # Simplified enemy deck creation
        enemy_deck = []
        
        # Add some basic attack cards
        for i in range(8):
            # Lower damage and add cast time for balance
            damage_value = 2 + (i % 3)  # 2-4 damage instead of 2-5
            cast_time = 0.5 + (i % 2) * 0.5  # 0.5-1.0s cast time
            
            attack_card = Card(
                id=f"enemy_attack_{i}",
                name=f"Enemy Strike {i+1}",
                sand_cost=1 + (i % 3),
                cast_time=cast_time,  # Add casting time
                card_type=CardType.ATTACK,
                description=f"Enemy attack dealing damage",
                effects=[
                    CardEffect(
                        effect_type=EffectType.DAMAGE,
                        value=damage_value,
                        target_type=TargetType.ENEMY
                    )
                ]
            )
            enemy_deck.append(attack_card)
        
        random.shuffle(enemy_deck)
        return enemy_deck
    
    def _handle_action_executed(self, action: QueuedAction, owner: str) -> None:
        """Handle queue callback for action execution."""
        if self.on_action_executed:
            self.on_action_executed(action, owner)
    
    def _handle_reaction_window(self, triggering_action: QueuedAction) -> None:
        """Handle queue callback for reaction window opening."""
        if self.on_reaction_window:
            self.on_reaction_window(triggering_action)
    
    def _handle_queue_changed(self) -> None:
        """Handle queue callback for queue changes."""
        # Can be used to update UI displays
        pass
    
    def get_combat_statistics(self) -> Dict[str, Any]:
        """Get current combat statistics."""
        current_time = time.perf_counter()
        combat_duration = current_time - self.combat_start_time
        
        return {
            'duration': combat_duration,
            'actions_executed': self.actions_executed,
            'total_sand_spent': self.total_sand_spent,
            'player_health': self.player.health if self.player else 0,
            'enemy_health': self.enemy.health if self.enemy else 0,
            'state': self.state.value
        }
    
    def get_queue_preview(self, owner: str) -> List[Dict[str, Any]]:
        """Get preview of queued actions for UI."""
        if not self.initiative_queue:
            return []
        
        return self.initiative_queue.get_queue_preview(owner)
    
    def is_reaction_window_open(self) -> bool:
        """Check if reaction window is open."""
        if not self.initiative_queue:
            return False
        
        return self.initiative_queue.is_reaction_window_open()
    
    def get_reaction_time_remaining(self) -> float:
        """Get remaining reaction window time."""
        if not self.initiative_queue:
            return 0.0
        
        return self.initiative_queue.get_reaction_window_time_remaining()