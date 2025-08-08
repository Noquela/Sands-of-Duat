#!/usr/bin/env python3
"""
INTEGRATED COMBAT SYSTEM
========================

Complete integration of all Egyptian combat systems into a functional
gameplay experience. This is the master combat controller that orchestrates
all the individual systems working together.
"""

import pygame
import logging
import random
import uuid
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

# Import all our combat systems
from .initiative_system import HourGlassInitiative, TimePhase
from .thirteen_phase_system import ThirteenPhaseManager, CombatPhase
from .ba_ka_system import BaKaManager, SoulState, BaAbility, KaAbility
from .divine_judgment import DivineJudgmentSystem, MoralAction, JudgmentOutcome
from .underworld_passage import UnderworldPassageSystem, UnderworldHour
from .resurrection_system import EgyptianResurrectionSystem, ResurrectionType
from .combat_ui import EgyptianCombatUI, UIState, UIAction

# Import card systems
from ..cards.egyptian_gods import get_all_god_cards, get_god_card_by_id

logger = logging.getLogger(__name__)

class GameState(Enum):
    """Overall game states."""
    MENU = "menu"
    COMBAT_PREPARATION = "combat_preparation"
    ACTIVE_COMBAT = "active_combat"
    UNDERWORLD_JOURNEY = "underworld_journey"
    RESURRECTION_ATTEMPT = "resurrection_attempt"
    VICTORY = "victory"
    DEFEAT = "defeat"

@dataclass
class CombatEntity:
    """Entity participating in combat."""
    entity_id: str
    name: str
    controller: str  # 'player' or 'enemy'
    is_alive: bool = True
    current_health: int = 100
    max_health: int = 100
    attack: int = 10
    defense: int = 5
    
    # Egyptian-specific attributes
    divine_favor: int = 0
    mana: int = 5
    sand: int = 2  # Egyptian resource
    
    # Combat state
    position: Tuple[int, int] = (0, 0)
    can_act: bool = True
    status_effects: Dict[str, Any] = field(default_factory=dict)
    
    # Cards and abilities
    hand: List[Dict[str, Any]] = field(default_factory=list)
    deck: List[Dict[str, Any]] = field(default_factory=list)
    played_cards: List[Dict[str, Any]] = field(default_factory=list)
    
    # Moral tracking for divine judgment
    moral_actions: List[MoralAction] = field(default_factory=list)
    
    def take_damage(self, amount: int) -> bool:
        """Take damage, return True if entity dies."""
        self.current_health = max(0, self.current_health - amount)
        if self.current_health <= 0 and self.is_alive:
            self.is_alive = False
            return True
        return False
    
    def heal(self, amount: int):
        """Heal the entity."""
        self.current_health = min(self.max_health, self.current_health + amount)

class IntegratedCombatSystem:
    """
    Master combat system that integrates all Egyptian combat mechanics
    into a single, cohesive gameplay experience.
    """
    
    def __init__(self, screen_width: int = 1400, screen_height: int = 900):
        # Core systems
        self.initiative_system = HourGlassInitiative()
        self.phase_manager = ThirteenPhaseManager()
        self.ba_ka_manager = BaKaManager()
        self.judgment_system = DivineJudgmentSystem()
        self.underworld_system = UnderworldPassageSystem()
        self.resurrection_system = EgyptianResurrectionSystem()
        self.ui_system = EgyptianCombatUI(screen_width, screen_height)
        
        # Game state
        self.game_state = GameState.MENU
        self.combat_id = str(uuid.uuid4())
        self.turn_number = 0
        self.active_player = "player"
        
        # Entities
        self.entities: Dict[str, CombatEntity] = {}
        self.player_entities: List[str] = []
        self.enemy_entities: List[str] = []
        
        # Combat flow
        self.initiative_order: List[str] = []
        self.current_entity_index = 0
        self.phase_results: Dict[str, Any] = {}
        
        # Game events and messages
        self.event_log: List[str] = []
        self.current_status_message = ""
        
        # Victory/defeat conditions
        self.victory_conditions: List[Callable] = []
        self.defeat_conditions: List[Callable] = []
        
        # Initialize with demo combat
        self._setup_demo_combat()
    
    def _setup_demo_combat(self):
        """Set up a demonstration combat scenario."""
        # Create player entity
        player = CombatEntity(
            entity_id="player_hero",
            name="Egyptian Hero",
            controller="player",
            current_health=80,
            max_health=80,
            attack=12,
            defense=8,
            divine_favor=3,
            mana=6,
            sand=3
        )
        
        # Give player some cards
        god_cards = get_all_god_cards()
        player.hand = [
            self._card_to_dict(god_cards[0]),  # Ra
            self._card_to_dict(god_cards[1]),  # Anubis
            self._card_to_dict(god_cards[2]),  # Isis
        ]
        
        # Create enemy
        enemy = CombatEntity(
            entity_id="chaos_serpent",
            name="Chaos Serpent",
            controller="enemy",
            current_health=60,
            max_health=60,
            attack=15,
            defense=4,
            divine_favor=-2,
            mana=4,
            sand=1
        )
        
        self.entities["player_hero"] = player
        self.entities["chaos_serpent"] = enemy
        self.player_entities.append("player_hero")
        self.enemy_entities.append("chaos_serpent")
        
        # Initialize soul states
        self.ba_ka_manager.initialize_soul("player_hero", 1.0)
        self.ba_ka_manager.initialize_soul("chaos_serpent", 0.8)
        
        # Initialize moral records
        self.judgment_system.initialize_moral_record("player_hero")
        self.judgment_system.initialize_moral_record("chaos_serpent")
        
        logger.info("Demo combat setup complete")
    
    def _card_to_dict(self, card) -> Dict[str, Any]:
        """Convert card object to dictionary for UI display."""
        return {
            'name': card.name,
            'mana_cost': card.stats.mana_cost,
            'sand_cost': card.stats.sand_cost,
            'divine_favor': card.stats.divine_favor,
            'element': card.element.value if hasattr(card, 'element') else 'neutral',
            'description': card.description,
            'card_id': card.card_id
        }
    
    def start_combat(self):
        """Begin combat sequence."""
        self.game_state = GameState.ACTIVE_COMBAT
        self.turn_number = 1
        
        # Calculate initial initiative order
        self.initiative_order = self.initiative_system.calculate_initiative_order(self.entities)
        self.current_entity_index = 0
        
        # Start with preparation phase
        self.phase_manager.current_phase = CombatPhase.DAWN_PREPARATION
        
        # Execute preparation phase
        self.phase_results = self.phase_manager.execute_phase(self.entities, {
            'turn_number': self.turn_number,
            'combat_id': self.combat_id
        })
        
        self.current_status_message = "Combat begins! The journey through the underworld starts..."
        self._log_event("Combat initiated - entering the realm of the gods")
        
        logger.info("Combat started - Phase: Dawn Preparation")
    
    def process_turn(self) -> bool:
        """
        Process a complete combat turn through all 13 phases.
        Returns True if combat should continue, False if it ends.
        """
        if self.game_state != GameState.ACTIVE_COMBAT:
            return False
        
        # Get current entity
        if self.current_entity_index >= len(self.initiative_order):
            # All entities have acted, advance to next phase
            return self._advance_phase()
        
        current_entity_id = self.initiative_order[self.current_entity_index]
        current_entity = self.entities.get(current_entity_id)
        
        if not current_entity or not current_entity.is_alive:
            # Skip dead entities
            self.current_entity_index += 1
            return True
        
        # Process entity turn based on controller
        if current_entity.controller == "player":
            return self._process_player_turn(current_entity)
        else:
            return self._process_ai_turn(current_entity)
    
    def _process_player_turn(self, entity: CombatEntity) -> bool:
        """Process player's turn - wait for UI input."""
        # Player turn is handled through UI interactions
        self.current_status_message = f"{entity.name}'s turn - Select an action"
        return True
    
    def _process_ai_turn(self, entity: CombatEntity) -> bool:
        """Process AI enemy turn."""
        # Simple AI: attack if possible, otherwise pass
        if entity.can_act and entity.is_alive:
            # Find valid targets
            targets = [eid for eid in self.entities.keys() 
                      if self.entities[eid].controller != entity.controller 
                      and self.entities[eid].is_alive]
            
            if targets:
                target_id = random.choice(targets)
                damage = max(1, entity.attack - self.entities[target_id].defense)
                
                # Apply damage and record moral action
                killed = self.entities[target_id].take_damage(damage)
                
                if killed:
                    moral_action = MoralAction.MURDER_INNOCENT if entity.controller == "enemy" else MoralAction.UPHOLD_JUSTICE
                    self.judgment_system.record_action(entity.entity_id, moral_action, f"Combat against {target_id}")
                    self._log_event(f"{entity.name} defeats {self.entities[target_id].name}!")
                else:
                    self._log_event(f"{entity.name} attacks {self.entities[target_id].name} for {damage} damage")
        
        # End AI turn
        self.current_entity_index += 1
        return True
    
    def _advance_phase(self) -> bool:
        """Advance to the next combat phase."""
        # Reset entity turn order
        self.current_entity_index = 0
        
        # Execute current phase effects
        phase_results = self.phase_manager.execute_phase(self.entities, {
            'turn_number': self.turn_number,
            'combat_id': self.combat_id
        })
        
        # Process phase-specific effects
        self._process_phase_effects(phase_results)
        
        # Advance time and phase
        new_time_phase = self.initiative_system.advance_time()
        new_combat_phase = self.phase_manager.advance_phase()
        
        # Check if combat is complete (all 13 phases done)
        if self.phase_manager.is_combat_complete():
            return self._end_combat()
        
        # Recalculate initiative for new phase
        self.initiative_order = self.initiative_system.calculate_initiative_order(self.entities)
        
        self.current_status_message = f"Phase: {new_combat_phase.description}"
        self._log_event(f"Entering {new_combat_phase.description}")
        
        return True
    
    def _process_phase_effects(self, phase_results: Dict[str, Any]):
        """Process the effects of the current phase."""
        if not phase_results or "effects" not in phase_results:
            return
        
        for effect_desc in phase_results["effects"]:
            self._log_event(effect_desc)
            
            # Apply specific effects based on phase
            phase = phase_results.get("phase", "")
            
            if phase == "divine_judgment":
                # Conduct judgment on all entities
                for entity_id in self.entities.keys():
                    if self.entities[entity_id].is_alive:
                        outcome = self.judgment_system.conduct_judgment(entity_id)
                        self._apply_judgment_effects(entity_id, outcome)
            
            elif phase == "ba_separation":
                # Attempt Ba separation for entities with high divine favor
                for entity_id, entity in self.entities.items():
                    if entity.is_alive and entity.divine_favor > 5:
                        if self.ba_ka_manager.separate_ba(entity_id):
                            self._log_event(f"{entity.name}'s Ba separates - gaining spiritual power")
            
            elif phase == "afterlife_transition":
                # Handle death and potential resurrection
                for entity_id, entity in self.entities.items():
                    if not entity.is_alive:
                        self._attempt_automatic_resurrection(entity_id)
    
    def _apply_judgment_effects(self, entity_id: str, outcome: JudgmentOutcome):
        """Apply divine judgment effects to an entity."""
        entity = self.entities.get(entity_id)
        if not entity:
            return
        
        if outcome == JudgmentOutcome.PURE_HEART:
            entity.divine_favor += 3
            entity.heal(20)
            self._log_event(f"{entity.name} judged pure - blessed with divine favor")
        elif outcome == JudgmentOutcome.RIGHTEOUS:
            entity.divine_favor += 2
            entity.heal(10)
            self._log_event(f"{entity.name} judged righteous - receives divine blessing")
        elif outcome == JudgmentOutcome.CORRUPT:
            entity.divine_favor -= 3
            entity.take_damage(15)
            self._log_event(f"{entity.name} judged corrupt - suffers divine punishment")
        elif outcome == JudgmentOutcome.DEVOURED:
            entity.take_damage(entity.current_health)  # Instant death
            self._log_event(f"{entity.name} devoured by Ammit - true death!")
    
    def _attempt_automatic_resurrection(self, entity_id: str):
        """Attempt automatic resurrection for dead entities."""
        entity = self.entities.get(entity_id)
        if not entity or entity.is_alive:
            return
        
        # Record death
        self.resurrection_system.record_death(
            entity_id, 
            "combat_death",
            self.judgment_system.moral_records[entity_id].maat_balance
        )
        
        # Automatic resurrection attempts based on divine favor
        if entity.divine_favor > 8:
            # High divine favor gets divine intervention attempt
            attempt = self.resurrection_system.attempt_resurrection(
                entity_id,
                ResurrectionType.DIVINE_INTERVENTION,
                divine_interventions=["Ra", "Osiris"]
            )
            
            if attempt.result == "success":
                entity.is_alive = True
                entity.current_health = max(1, entity.max_health // 3)
                self._log_event(f"{entity.name} resurrected by divine intervention!")
    
    def handle_ui_action(self, action_data: Dict[str, Any]) -> bool:
        """Handle action from the UI system."""
        action = action_data.get('action', '')
        
        if action == 'select_card':
            # Card selection handled by UI
            return True
        
        elif action == 'play_card':
            return self._handle_play_card(action_data)
        
        elif action == 'separate_ba':
            return self._handle_separate_ba()
        
        elif action == 'manifest_ka':
            return self._handle_manifest_ka()
        
        elif action == 'divine_intervention':
            return self._handle_divine_intervention(action_data)
        
        elif action == 'end_turn':
            return self._handle_end_turn()
        
        elif action == 'show_divine_intervention':
            # UI state change, no game logic needed
            return True
        
        return True
    
    def _handle_play_card(self, action_data: Dict[str, Any]) -> bool:
        """Handle playing a card."""
        current_entity_id = self.initiative_order[self.current_entity_index] if self.initiative_order else None
        if not current_entity_id or current_entity_id not in self.entities:
            return False
        
        entity = self.entities[current_entity_id]
        if entity.controller != "player":
            return False
        
        card_index = action_data.get('card_index', -1)
        if card_index < 0 or card_index >= len(entity.hand):
            return False
        
        card_data = entity.hand[card_index]
        
        # Check if player can afford the card
        mana_cost = card_data.get('mana_cost', 0)
        sand_cost = card_data.get('sand_cost', 0)
        
        if entity.mana < mana_cost or entity.sand < sand_cost:
            self.current_status_message = "Not enough resources to play this card"
            return False
        
        # Pay costs
        entity.mana -= mana_cost
        entity.sand -= sand_cost
        
        # Apply card effects (simplified - would be more complex in full game)
        self._apply_card_effects(entity, card_data)
        
        # Move card from hand to played cards
        entity.played_cards.append(entity.hand.pop(card_index))
        
        # Record moral action if applicable
        if "divine" in card_data.get('name', '').lower():
            self.judgment_system.record_action(entity.entity_id, MoralAction.HONOR_GODS, f"Played {card_data['name']}")
        
        self._log_event(f"{entity.name} plays {card_data['name']}")
        self.current_entity_index += 1  # End turn after playing card
        
        return True
    
    def _apply_card_effects(self, caster: CombatEntity, card_data: Dict[str, Any]):
        """Apply the effects of a played card."""
        card_name = card_data.get('name', '')
        
        # Simplified card effects - real implementation would be much more complex
        if 'Ra' in card_name:
            # Ra deals damage to all enemies
            damage = 8
            for entity_id, entity in self.entities.items():
                if entity.controller != caster.controller and entity.is_alive:
                    entity.take_damage(damage)
                    self._log_event(f"Ra's solar radiance burns {entity.name} for {damage} damage")
        
        elif 'Isis' in card_name:
            # Isis heals all allies
            heal_amount = 15
            for entity_id, entity in self.entities.items():
                if entity.controller == caster.controller and entity.is_alive:
                    entity.heal(heal_amount)
                    self._log_event(f"Isis heals {entity.name} for {heal_amount} health")
        
        elif 'Anubis' in card_name:
            # Anubis provides death resistance
            caster.status_effects['death_resistance'] = 3
            self._log_event(f"{caster.name} gains Anubis's protection against death")
    
    def _handle_separate_ba(self) -> bool:
        """Handle Ba separation attempt."""
        current_entity_id = self.initiative_order[self.current_entity_index] if self.initiative_order else None
        if not current_entity_id:
            return False
        
        if self.ba_ka_manager.separate_ba(current_entity_id):
            self._log_event(f"{self.entities[current_entity_id].name}'s Ba separates from body")
            self.current_status_message = "Ba separation successful - spiritual powers enhanced"
        else:
            self.current_status_message = "Ba separation failed - insufficient spiritual strength"
        
        return True
    
    def _handle_manifest_ka(self) -> bool:
        """Handle Ka manifestation attempt."""
        current_entity_id = self.initiative_order[self.current_entity_index] if self.initiative_order else None
        if not current_entity_id:
            return False
        
        if self.ba_ka_manager.manifest_ka(current_entity_id):
            self._log_event(f"{self.entities[current_entity_id].name}'s Ka manifests as life force double")
            self.current_status_message = "Ka manifestation successful - life force empowered"
        else:
            self.current_status_message = "Ka manifestation failed - insufficient sustenance"
        
        return True
    
    def _handle_divine_intervention(self, action_data: Dict[str, Any]) -> bool:
        """Handle divine intervention request."""
        god_name = action_data.get('god_name', '')
        intervention_type = action_data.get('intervention_type', 'guidance')
        
        current_entity_id = self.initiative_order[self.current_entity_index] if self.initiative_order else None
        if not current_entity_id:
            return False
        
        # Add divine intervention to time system
        self.initiative_system.add_divine_intervention(god_name, 0.2, 3)
        
        # Apply intervention effects
        entity = self.entities[current_entity_id]
        if god_name == "Ra":
            entity.divine_favor += 2
            # Deal damage to enemies
            for enemy_id, enemy in self.entities.items():
                if enemy.controller != entity.controller and enemy.is_alive:
                    enemy.take_damage(10)
        elif god_name == "Isis":
            entity.heal(25)
            entity.mana += 2
        elif god_name == "Anubis":
            # Death protection
            entity.status_effects['divine_protection'] = 5
        
        self._log_event(f"{god_name} intervenes on behalf of {entity.name}")
        return True
    
    def _handle_end_turn(self) -> bool:
        """Handle ending the current entity's turn."""
        self.current_entity_index += 1
        return True
    
    def _end_combat(self) -> bool:
        """End combat and determine outcome."""
        # Determine victory/defeat
        player_alive = any(self.entities[eid].is_alive for eid in self.player_entities)
        enemy_alive = any(self.entities[eid].is_alive for eid in self.enemy_entities)
        
        if player_alive and not enemy_alive:
            self.game_state = GameState.VICTORY
            self.current_status_message = "Victory! The forces of chaos are defeated!"
            self._log_event("VICTORY: Heroes triumph over darkness!")
        elif enemy_alive and not player_alive:
            self.game_state = GameState.DEFEAT
            self.current_status_message = "Defeat... The underworld claims another soul."
            self._log_event("DEFEAT: Heroes fall to the forces of chaos")
        else:
            # Draw or special ending
            self.game_state = GameState.VICTORY  # Treat draw as victory for surviving
            self.current_status_message = "The cosmic balance is maintained."
            self._log_event("Balance achieved - neither order nor chaos prevails")
        
        logger.info(f"Combat ended: {self.game_state}")
        return False  # Combat should end
    
    def _log_event(self, message: str):
        """Log an event to the game log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.append(f"[{timestamp}] {message}")
        if len(self.event_log) > 50:  # Keep log manageable
            self.event_log.pop(0)
    
    def get_game_state_for_ui(self) -> Dict[str, Any]:
        """Get current game state formatted for UI display."""
        current_entity_id = None
        if (self.initiative_order and 
            self.current_entity_index < len(self.initiative_order)):
            current_entity_id = self.initiative_order[self.current_entity_index]
        
        # Get player entity data
        player_hand = []
        for entity_id in self.player_entities:
            if entity_id in self.entities:
                player_hand = self.entities[entity_id].hand
                break
        
        # Get soul status for UI
        soul_status = {}
        if current_entity_id and current_entity_id in self.entities:
            soul_powers = self.ba_ka_manager.get_soul_power_modifiers(current_entity_id)
            if current_entity_id in self.ba_ka_manager.entity_souls:
                soul_state = self.ba_ka_manager.entity_souls[current_entity_id]
                soul_status = {
                    'state': soul_state.soul_state.value,
                    'ba_strength': soul_state.ba.strength,
                    'ka_strength': soul_state.ka.vital_force,
                    'divine_judgment': self.judgment_system.moral_records.get(current_entity_id, type('', (), {'maat_balance': 0})).maat_balance,
                    'abilities': [ability.key for ability in soul_state.ba.active_abilities + soul_state.ka.active_abilities]
                }
        
        # Get initiative data
        initiative_data = {
            'sand_position': self.initiative_system.sand_flow.current_position,
            'time_phase': self.initiative_system.time_phase.value
        }
        
        return {
            'entities': {eid: {
                'name': entity.name,
                'controller': entity.controller,
                'is_alive': entity.is_alive,
                'current_health': entity.current_health,
                'max_health': entity.max_health,
                'divine_favor': entity.divine_favor,
                'mana': entity.mana,
                'sand': entity.sand,
                'status_effects': entity.status_effects
            } for eid, entity in self.entities.items()},
            'player_hand': player_hand,
            'current_phase': self.phase_manager.current_phase.key,
            'initiative_data': initiative_data,
            'soul_status': soul_status,
            'status_message': self.current_status_message,
            'game_state': self.game_state.value,
            'turn_number': self.turn_number,
            'current_entity': current_entity_id
        }
    
    def update(self) -> bool:
        """Update the combat system. Returns True if combat continues."""
        if self.game_state != GameState.ACTIVE_COMBAT:
            return False
        
        # Auto-advance AI turns, wait for player input
        if (self.initiative_order and 
            self.current_entity_index < len(self.initiative_order)):
            current_entity_id = self.initiative_order[self.current_entity_index]
            current_entity = self.entities.get(current_entity_id)
            
            if (current_entity and 
                current_entity.is_alive and 
                current_entity.controller == "enemy"):
                # Process AI turn automatically
                return self.process_turn()
        
        return True
    
    def render(self, screen: pygame.Surface):
        """Render the combat system using the UI."""
        game_state = self.get_game_state_for_ui()
        self.ui_system.render(screen, game_state)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle mouse click events."""
        game_state = self.get_game_state_for_ui()
        action_data = self.ui_system.handle_click(pos, game_state)
        
        if action_data:
            return self.handle_ui_action(action_data)
        
        return True
    
    def handle_keypress(self, key: int) -> bool:
        """Handle keyboard input."""
        if key == pygame.K_SPACE:  # Space to end turn
            return self._handle_end_turn()
        elif key == pygame.K_1:   # Number keys for quick actions
            return self._handle_separate_ba()
        elif key == pygame.K_2:
            return self._handle_manifest_ka()
        
        return True