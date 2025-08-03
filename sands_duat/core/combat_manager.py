"""
Enhanced Combat Manager

Full turn-based combat system with Hour-Glass Initiative integration,
enemy AI, and complete combat flow management.

Features:
- Turn-based combat with sand regeneration timing
- Enemy AI with Hour-Glass awareness
- Combat state management and resolution
- Win/loss condition handling
- Visual effect coordination
"""

import logging
import random
import time
from enum import Enum
from typing import List, Dict, Optional, Any, Callable, Union
from dataclasses import dataclass

from .hourglass import HourGlass
from .cards import Card, CardEffect, EffectType, TargetType


class CombatPhase(Enum):
    """Current phase of combat."""
    SETUP = "setup"
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    RESOLUTION = "resolution"
    VICTORY = "victory"
    DEFEAT = "defeat"


class TurnPhase(Enum):
    """Current phase of a turn."""
    START = "start"
    MAIN = "main"
    END = "end"


@dataclass
class CombatEntity:
    """Represents a participant in combat."""
    id: str
    name: str
    health: int
    max_health: int
    hourglass: HourGlass
    is_player: bool = False
    
    # Status effects
    block: int = 0  # Damage reduction this turn
    buffs: Dict[str, int] = None  # Buff effects with duration
    debuffs: Dict[str, int] = None  # Debuff effects with duration
    
    def __post_init__(self):
        if self.buffs is None:
            self.buffs = {}
        if self.debuffs is None:
            self.debuffs = {}
    
    def take_damage(self, amount: int) -> int:
        """Take damage, applying block and debuffs. Returns actual damage taken."""
        # Apply vulnerable debuff (increases damage by 50%)
        modified_damage = amount
        if "vulnerable" in self.debuffs:
            modified_damage = int(amount * 1.5)
        
        # Apply block
        blocked = min(self.block, modified_damage)
        actual_damage = modified_damage - blocked
        self.block = max(0, self.block - modified_damage)
        
        # Apply damage
        old_health = self.health
        self.health = max(0, self.health - actual_damage)
        
        return old_health - self.health
    
    def heal(self, amount: int) -> int:
        """Heal health. Returns actual healing done."""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health
    
    def add_block(self, amount: int) -> None:
        """Add block for damage reduction."""
        self.block += amount
    
    def is_alive(self) -> bool:
        """Check if entity is still alive."""
        return self.health > 0
    
    def start_turn(self) -> None:
        """Reset turn-based effects."""
        self.block = 0  # Block resets each turn
        
        # Update buff/debuff durations
        for effect in list(self.buffs.keys()):
            if effect == "blessings":
                # Handle blessings specially (nested dict)
                for blessing_name in list(self.buffs[effect].keys()):
                    self.buffs[effect][blessing_name] -= 1
                    if self.buffs[effect][blessing_name] <= 0:
                        del self.buffs[effect][blessing_name]
                # Remove blessings category if empty
                if not self.buffs[effect]:
                    del self.buffs[effect]
            elif isinstance(self.buffs[effect], int):
                self.buffs[effect] -= 1
                if self.buffs[effect] <= 0:
                    del self.buffs[effect]
        
        for effect in list(self.debuffs.keys()):
            if isinstance(self.debuffs[effect], int):
                self.debuffs[effect] -= 1
                if self.debuffs[effect] <= 0:
                    del self.debuffs[effect]


@dataclass
class EnemyAction:
    """Represents an action an enemy can take."""
    name: str
    sand_cost: int
    effects: List[CardEffect]
    description: str
    probability: float = 1.0  # Chance of choosing this action
    
    def can_afford(self, hourglass: HourGlass) -> bool:
        """Check if enemy can afford this action."""
        return hourglass.can_afford(self.sand_cost)


class CombatManager:
    """
    Enhanced combat manager with full turn resolution and enemy AI.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Combat state
        self.phase = CombatPhase.SETUP
        self.turn_phase = TurnPhase.START
        self.turn_number = 0
        
        # Participants
        self.player: Optional[CombatEntity] = None
        self.enemy: Optional[CombatEntity] = None
        
        # Player's hand and deck
        self.player_hand: List[Card] = []
        self.player_deck: List[Card] = []
        self.player_discard: List[Card] = []
        
        # Enemy AI
        self.enemy_actions: List[EnemyAction] = []
        self.enemy_intent: Optional[EnemyAction] = None
        
        # Combat events
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Visual effects queue
        self.pending_effects: List[Dict[str, Any]] = []
        
        self.logger.info("Combat Manager initialized")
    
    def setup_combat(self, player_health: int, player_max_health: int, 
                    enemy_name: str, enemy_health: int, enemy_max_health: int,
                    player_cards: List[Card]) -> None:
        """
        Setup a new combat encounter.
        
        Args:
            player_health: Player's current health
            player_max_health: Player's maximum health
            enemy_name: Name of the enemy
            enemy_health: Enemy's current health
            enemy_max_health: Enemy's maximum health
            player_cards: Player's starting hand
        """
        self.logger.info(f"Setting up combat: Player vs {enemy_name}")
        
        # Create player entity
        player_hourglass = HourGlass()
        player_hourglass.set_sand(3)  # Start with some sand
        
        self.player = CombatEntity(
            id="player",
            name="Player",
            health=player_health,
            max_health=player_max_health,
            hourglass=player_hourglass,
            is_player=True
        )
        
        # Create enemy entity
        enemy_hourglass = HourGlass()
        enemy_hourglass.set_sand(2)  # Enemies start with less sand
        
        self.enemy = CombatEntity(
            id="enemy",
            name=enemy_name,
            health=enemy_health,
            max_health=enemy_max_health,
            hourglass=enemy_hourglass,
            is_player=False
        )
        
        # Setup player's cards
        self.player_hand = player_cards.copy()
        self.player_deck = []
        self.player_discard = []
        
        # Setup enemy actions
        self._setup_enemy_actions(enemy_name)
        
        # Start combat
        self.phase = CombatPhase.PLAYER_TURN
        self.turn_phase = TurnPhase.START
        self.turn_number = 1
        
        self._trigger_event("combat_started", {
            "player": self.player,
            "enemy": self.enemy
        })
        
        self._start_player_turn()
    
    def _setup_enemy_actions(self, enemy_name: str) -> None:
        """Setup actions for the specific enemy type."""
        # Basic enemy actions - would be loaded from enemy data files
        self.enemy_actions = [
            EnemyAction(
                name="Claw Strike",
                sand_cost=1,
                effects=[
                    CardEffect(effect_type=EffectType.DAMAGE, value=8, target=TargetType.ENEMY)
                ],
                description="A quick claw attack dealing 8 damage.",
                probability=0.6
            ),
            EnemyAction(
                name="Guard Stance",
                sand_cost=2,
                effects=[
                    CardEffect(effect_type=EffectType.BLOCK, value=12, target=TargetType.SELF)
                ],
                description="Defensive stance, gaining 12 block.",
                probability=0.3
            ),
            EnemyAction(
                name="Fury Swipe",
                sand_cost=3,
                effects=[
                    CardEffect(effect_type=EffectType.DAMAGE, value=15, target=TargetType.ENEMY)
                ],
                description="A powerful attack dealing 15 damage.",
                probability=0.4
            )
        ]
        
        self.logger.info(f"Setup {len(self.enemy_actions)} actions for {enemy_name}")
    
    def update(self, delta_time: float) -> None:
        """Update combat state and timing."""
        if self.phase in [CombatPhase.VICTORY, CombatPhase.DEFEAT]:
            return
        
        # Update hourglasses
        if self.player and self.player.hourglass:
            self.player.hourglass.update_sand()
        
        if self.enemy and self.enemy.hourglass:
            self.enemy.hourglass.update_sand()
        
        # Check for combat end conditions
        self._check_combat_end()
    
    def play_card(self, card: Card, target: Optional[CombatEntity] = None) -> bool:
        """
        Player plays a card.
        
        Args:
            card: The card to play
            target: Target entity (if required)
            
        Returns:
            True if card was successfully played
        """
        if self.phase != CombatPhase.PLAYER_TURN or self.turn_phase != TurnPhase.MAIN:
            self.logger.warning("Cannot play card - not player's main phase")
            return False
        
        # Calculate effective cost (considering buffs like sand cost reduction)
        effective_cost = card.sand_cost
        if "sand_cost_reduction" in self.player.buffs:
            effective_cost = max(0, effective_cost - self.player.buffs["sand_cost_reduction"])
        
        if not self.player or not self.player.hourglass.can_afford(effective_cost):
            self.logger.warning(f"Cannot afford card {card.name} (cost: {effective_cost})")
            return False
        
        # Spend sand
        self.player.hourglass.spend_sand(effective_cost)
        
        # Remove card from hand
        if card in self.player_hand:
            self.player_hand.remove(card)
            self.player_discard.append(card)
        
        # Apply card effects
        self._apply_card_effects(card, self.player, target or self.enemy)
        
        # Trigger events
        self._trigger_event("card_played", {
            "card": card,
            "player": self.player,
            "target": target
        })
        
        self.logger.info(f"Player played {card.name} for {card.sand_cost} sand")
        return True
    
    def end_player_turn(self) -> None:
        """End the player's turn and start enemy turn."""
        if self.phase != CombatPhase.PLAYER_TURN:
            return
        
        self.logger.info("Player ended turn")
        
        # End player turn
        self.turn_phase = TurnPhase.END
        self._trigger_event("player_turn_ended", {"player": self.player})
        
        # Start enemy turn
        self.phase = CombatPhase.ENEMY_TURN
        self._start_enemy_turn()
    
    def _start_player_turn(self) -> None:
        """Start a new player turn."""
        self.logger.info(f"Starting player turn {self.turn_number}")
        
        if self.player:
            self.player.start_turn()
        
        self.turn_phase = TurnPhase.START
        
        # Draw cards if needed (simplified)
        # In a full implementation, this would handle deck management
        
        self.turn_phase = TurnPhase.MAIN
        
        self._trigger_event("player_turn_started", {
            "player": self.player,
            "turn": self.turn_number
        })
    
    def _start_enemy_turn(self) -> None:
        """Start a new enemy turn with AI decision making."""
        self.logger.info(f"Starting enemy turn {self.turn_number}")
        
        if not self.enemy:
            return
        
        self.enemy.start_turn()
        self.turn_phase = TurnPhase.START
        
        # Enemy AI: choose action
        self.enemy_intent = self._choose_enemy_action()
        
        self.turn_phase = TurnPhase.MAIN
        
        # Execute enemy action after a brief delay (for visual clarity)
        self._execute_enemy_action()
        
        self._trigger_event("enemy_turn_started", {
            "enemy": self.enemy,
            "intent": self.enemy_intent,
            "turn": self.turn_number
        })
    
    def _choose_enemy_action(self) -> Optional[EnemyAction]:
        """AI logic to choose enemy action."""
        if not self.enemy or not self.enemy_actions:
            return None
        
        # Filter affordable actions
        affordable_actions = [
            action for action in self.enemy_actions 
            if action.can_afford(self.enemy.hourglass)
        ]
        
        if not affordable_actions:
            # If no actions are affordable, wait (do nothing)
            return None
        
        # Simple AI: choose based on probability and health
        weights = []
        for action in affordable_actions:
            weight = action.probability
            
            # Adjust weights based on health
            if self.enemy.health < self.enemy.max_health * 0.3:
                # Low health: prefer defensive actions
                if any(effect.effect_type == EffectType.BLOCK for effect in action.effects):
                    weight *= 1.5
            else:
                # Higher health: prefer aggressive actions
                if any(effect.effect_type == EffectType.DAMAGE for effect in action.effects):
                    weight *= 1.2
            
            weights.append(weight)
        
        # Weighted random choice
        return random.choices(affordable_actions, weights=weights)[0]
    
    def _execute_enemy_action(self) -> None:
        """Execute the chosen enemy action."""
        if not self.enemy or not self.enemy_intent:
            self._end_enemy_turn()
            return
        
        action = self.enemy_intent
        
        # Spend sand
        if not self.enemy.hourglass.spend_sand(action.sand_cost):
            self.logger.warning(f"Enemy couldn't afford action {action.name}")
            self._end_enemy_turn()
            return
        
        # Apply action effects
        self._apply_action_effects(action, self.enemy, self.player)
        
        self.logger.info(f"Enemy used {action.name} for {action.sand_cost} sand")
        
        self._trigger_event("enemy_action_executed", {
            "enemy": self.enemy,
            "action": action,
            "target": self.player
        })
        
        self._end_enemy_turn()
    
    def _end_enemy_turn(self) -> None:
        """End enemy turn and return to player."""
        self.turn_phase = TurnPhase.END
        
        self._trigger_event("enemy_turn_ended", {"enemy": self.enemy})
        
        # Start next player turn
        self.turn_number += 1
        self.phase = CombatPhase.PLAYER_TURN
        self._start_player_turn()
    
    def _apply_card_effects(self, card: Card, source: CombatEntity, target: CombatEntity) -> None:
        """Apply the effects of a played card."""
        for effect in card.effects:
            self._apply_effect(effect, source, target)
    
    def _apply_action_effects(self, action: EnemyAction, source: CombatEntity, target: CombatEntity) -> None:
        """Apply the effects of an enemy action."""
        for effect in action.effects:
            self._apply_effect(effect, source, target)
    
    def _apply_effect(self, effect: CardEffect, source: CombatEntity, target: CombatEntity) -> None:
        """Apply a single effect."""
        # Determine actual target based on effect target type
        actual_target = source if effect.target == TargetType.SELF else target
        
        if effect.effect_type == EffectType.DAMAGE:
            # Apply strength buff (increases damage) and weak debuff (decreases damage)
            modified_damage = effect.value
            if "strength" in source.buffs:
                modified_damage += source.buffs["strength"]
            if "weak" in source.debuffs:
                modified_damage = max(0, modified_damage - source.debuffs["weak"])
            
            damage_dealt = actual_target.take_damage(modified_damage)
            self._add_visual_effect("damage", {
                "target": actual_target,
                "amount": damage_dealt,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.HEAL:
            healing_done = actual_target.heal(effect.value)
            self._add_visual_effect("heal", {
                "target": actual_target,
                "amount": healing_done,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.BLOCK:
            # Apply dexterity buff (increases block)
            modified_block = effect.value
            if "dexterity" in source.buffs:
                modified_block += source.buffs["dexterity"]
            
            actual_target.add_block(modified_block)
            self._add_visual_effect("block", {
                "target": actual_target,
                "amount": modified_block,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.GAIN_SAND:
            current_sand = source.hourglass.current_sand
            max_sand = source.hourglass.max_sand
            new_sand = min(max_sand, current_sand + effect.value)
            source.hourglass.set_sand(new_sand)
            
        elif effect.effect_type == EffectType.GAIN_ENERGY:
            # GAIN_ENERGY is an alias for GAIN_SAND
            current_sand = source.hourglass.current_sand
            max_sand = source.hourglass.max_sand
            new_sand = min(max_sand, current_sand + effect.value)
            source.hourglass.set_sand(new_sand)
            
        elif effect.effect_type == EffectType.DRAW_CARDS:
            # Draw cards from deck into hand
            cards_to_draw = effect.value
            cards_drawn = 0
            max_hand_size = 10  # Standard hand size limit
            
            # Check if we can draw cards
            if len(self.player_hand) >= max_hand_size:
                self.logger.info(f"Cannot draw cards - hand is full ({len(self.player_hand)}/{max_hand_size})")
                return
            
            # Draw from deck, reshuffling discard if needed
            for _ in range(cards_to_draw):
                if len(self.player_hand) >= max_hand_size:
                    break
                
                # If deck is empty, shuffle discard pile into deck
                if not self.player_deck and self.player_discard:
                    self.player_deck = self.player_discard.copy()
                    self.player_discard.clear()
                    # Shuffle the deck
                    import random
                    random.shuffle(self.player_deck)
                    self.logger.info("Reshuffled discard pile into deck")
                
                # Draw a card if deck has cards
                if self.player_deck:
                    drawn_card = self.player_deck.pop(0)
                    self.player_hand.append(drawn_card)
                    cards_drawn += 1
                    self.logger.debug(f"Drew card: {drawn_card.name}")
                else:
                    # No more cards to draw
                    break
            
            if cards_drawn > 0:
                self.logger.info(f"Drew {cards_drawn} cards")
                self._add_visual_effect("draw_cards", {
                    "target": source,
                    "amount": cards_drawn,
                    "position": "center"
                })
            else:
                self.logger.info("No cards were drawn")
            
        elif effect.effect_type == EffectType.APPLY_VULNERABLE:
            # Apply vulnerable debuff
            actual_target.debuffs["vulnerable"] = effect.value
            self._add_visual_effect("debuff", {
                "target": actual_target,
                "type": "vulnerable",
                "duration": effect.value,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.APPLY_WEAK:
            # Apply weak debuff
            actual_target.debuffs["weak"] = effect.value
            self._add_visual_effect("debuff", {
                "target": actual_target,
                "type": "weak",
                "duration": effect.value,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.APPLY_STRENGTH:
            # Apply strength buff
            actual_target.buffs["strength"] = effect.value
            self._add_visual_effect("buff", {
                "target": actual_target,
                "type": "strength",
                "amount": effect.value,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.APPLY_DEXTERITY:
            # Apply dexterity buff
            actual_target.buffs["dexterity"] = effect.value
            self._add_visual_effect("buff", {
                "target": actual_target,
                "type": "dexterity",
                "amount": effect.value,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.MAX_HEALTH_INCREASE:
            # Increase max health
            actual_target.max_health += effect.value
            actual_target.health += effect.value  # Also heal for the amount
            self._add_visual_effect("max_health_increase", {
                "target": actual_target,
                "amount": effect.value,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.PERMANENT_SAND_INCREASE:
            # Permanently increase maximum sand capacity
            if actual_target.hourglass.increase_max_sand(effect.value):
                self.logger.info(f"Permanently increased max sand by {effect.value} for {actual_target.name}")
                self._add_visual_effect("permanent_sand_increase", {
                    "target": actual_target,
                    "amount": effect.value,
                    "position": "center"
                })
            else:
                self.logger.warning(f"Could not increase max sand - would exceed limit")
            
        elif effect.effect_type == EffectType.BLESSING:
            # Apply Egyptian-themed persistent blessing effects
            blessing_type = effect.metadata.get("blessing_type", "divine_favor")
            duration = effect.metadata.get("duration", 5)
            
            # Store blessing in a special buffs category
            if "blessings" not in actual_target.buffs:
                actual_target.buffs["blessings"] = {}
            actual_target.buffs["blessings"][blessing_type] = duration
            
            self.logger.info(f"Applied {blessing_type} blessing for {duration} turns to {actual_target.name}")
            self._add_visual_effect("blessing", {
                "target": actual_target,
                "type": blessing_type,
                "duration": duration,
                "position": "center"
            })
            
        elif effect.effect_type == EffectType.CHANNEL_DIVINITY:
            # Unique legendary effect for duat_master card
            divinity_effect = effect.metadata.get("effect", "sand_mastery")
            
            if divinity_effect == "sand_mastery":
                # Grant special sand-related powers
                actual_target.buffs["divine_sand_mastery"] = 999  # Permanent for combat
                # Reduce all sand costs by 1 (minimum 0) for rest of combat
                actual_target.buffs["sand_cost_reduction"] = 1
                
                self.logger.info(f"Channeled divinity: {divinity_effect} for {actual_target.name}")
                self._add_visual_effect("channel_divinity", {
                    "target": actual_target,
                    "effect": divinity_effect,
                    "position": "center"
                })
            
        else:
            self.logger.warning(f"Unhandled effect type: {effect.effect_type}")
    
    def _add_visual_effect(self, effect_type: str, data: Dict[str, Any]) -> None:
        """Add a visual effect to the queue."""
        self.pending_effects.append({
            "type": effect_type,
            "data": data,
            "timestamp": time.time()
        })
    
    def get_pending_effects(self) -> List[Dict[str, Any]]:
        """Get and clear pending visual effects."""
        effects = self.pending_effects.copy()
        self.pending_effects.clear()
        return effects
    
    def _check_combat_end(self) -> None:
        """Check for combat end conditions."""
        if not self.player or not self.enemy:
            return
        
        if not self.player.is_alive():
            self._end_combat(False)
        elif not self.enemy.is_alive():
            self._end_combat(True)
    
    def _end_combat(self, player_victory: bool) -> None:
        """End combat with the specified result."""
        if player_victory:
            self.phase = CombatPhase.VICTORY
            self.logger.info("Combat ended - Player Victory!")
        else:
            self.phase = CombatPhase.DEFEAT
            self.logger.info("Combat ended - Player Defeat!")
        
        self._trigger_event("combat_ended", {
            "victory": player_victory,
            "player": self.player,
            "enemy": self.enemy,
            "turns": self.turn_number
        })
    
    def add_event_handler(self, event_type: str, handler: Callable) -> None:
        """Add an event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def _trigger_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Trigger an event."""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler for {event_type}: {e}")
    
    def get_combat_state(self) -> Dict[str, Any]:
        """Get current combat state for UI display."""
        return {
            "phase": self.phase.value,
            "turn_phase": self.turn_phase.value,
            "turn_number": self.turn_number,
            "player": {
                "health": self.player.health if self.player else 0,
                "max_health": self.player.max_health if self.player else 0,
                "sand": self.player.hourglass.current_sand if self.player else 0,
                "max_sand": self.player.hourglass.max_sand if self.player else 0,
                "block": self.player.block if self.player else 0,
                "buffs": self.player.buffs if self.player else {},
                "debuffs": self.player.debuffs if self.player else {},
                "blessings": self.player.buffs.get("blessings", {}) if self.player else {},
            },
            "enemy": {
                "name": self.enemy.name if self.enemy else "",
                "health": self.enemy.health if self.enemy else 0,
                "max_health": self.enemy.max_health if self.enemy else 0,
                "sand": self.enemy.hourglass.current_sand if self.enemy else 0,
                "max_sand": self.enemy.hourglass.max_sand if self.enemy else 0,
                "block": self.enemy.block if self.enemy else 0,
                "buffs": self.enemy.buffs if self.enemy else {},
                "debuffs": self.enemy.debuffs if self.enemy else {},
                "intent": self.enemy_intent.name if self.enemy_intent else None,
            },
            "hand_size": len(self.player_hand)
        }