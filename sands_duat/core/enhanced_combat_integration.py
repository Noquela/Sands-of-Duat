"""
Enhanced Combat Integration System

Integrates all the enhanced systems together:
- Enhanced Enemy AI with personality-based decisions
- Visual effects with Egyptian theming
- Combat sound system with spatial audio
- Turn transition animations
- Player behavior analysis

This module provides a unified interface for the enhanced combat experience.
"""

import logging
import time
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from enum import Enum

# Import enhanced systems
from ..ai.enemy_ai_enhanced import enhanced_ai_manager, EnhancedEnemyAI
from ..ai.enemy_types import create_enemy_ai
from ..ui.combat_effects import get_combat_effects_system, CardType, EffectType
from ..audio.combat_sounds import get_combat_sound_system
from ..core.combat_enhanced import EnhancedCombatEngine, ActionType
from ..core.hourglass import HourGlass


class CombatEvent(Enum):
    """Types of combat events that trigger effects."""
    CARD_PLAYED = "card_played"
    DAMAGE_DEALT = "damage_dealt"
    HEALING_RECEIVED = "healing_received"
    TURN_START = "turn_start"
    TURN_END = "turn_end"
    STATUS_APPLIED = "status_applied"
    STATUS_REMOVED = "status_removed"
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"


@dataclass
class CombatEventData:
    """Data for a combat event."""
    event_type: CombatEvent
    actor_id: str
    target_id: Optional[str] = None
    position: Optional[Tuple[float, float]] = None
    value: int = 0
    card_type: Optional[str] = None
    damage_type: Optional[str] = None
    status_type: Optional[str] = None
    metadata: Dict[str, Any] = None


class EnhancedCombatCoordinator:
    """
    Coordinates all enhanced combat systems for seamless integration.
    
    This class serves as the central hub that connects AI, visual effects,
    audio, and combat mechanics for a cohesive experience.
    """
    
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize all systems
        self.effects_system = get_combat_effects_system()
        self.sound_system = get_combat_sound_system()
        self.ai_manager = enhanced_ai_manager
        
        # Combat state
        self.active_combat = False
        self.current_turn_player = True
        self.combat_participants: Dict[str, Dict[str, Any]] = {}
        
        # Event callbacks
        self.event_callbacks: Dict[CombatEvent, List[Callable]] = {}
        
        # Performance tracking
        self.events_processed = 0
        self.last_update_time = time.time()
        
        logging.info("Enhanced Combat Coordinator initialized")
    
    def start_combat(self, player_data: Dict[str, Any], enemy_data: Dict[str, Any],
                    location_type: str = "desert") -> None:
        """Start enhanced combat with all systems activated."""
        
        self.active_combat = True
        self.current_turn_player = True
        
        # Register participants
        self.combat_participants = {
            "player": player_data,
            "enemy": enemy_data
        }
        
        # Initialize enemy AI
        enemy_id = enemy_data.get("id", "unknown_enemy")
        enemy_type = enemy_data.get("type", "mummy_warrior")
        enemy_hourglass = enemy_data.get("hourglass")
        combat_engine = enemy_data.get("combat_engine")
        
        if enemy_hourglass and combat_engine:
            enemy_ai = create_enemy_ai(
                enemy_id=enemy_id,
                enemy_type=enemy_type,
                hourglass=enemy_hourglass,
                combat_engine=combat_engine
            )
            self.ai_manager.ais[enemy_id] = enemy_ai
        
        # Start ambient audio
        self.sound_system.start_combat_ambience(location_type)
        
        # Trigger combat start effects
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.COMBAT_START,
            actor_id="system",
            position=(self.screen_width // 2, self.screen_height // 2)
        ))
        
        logging.info(f"Enhanced combat started: {enemy_type} in {location_type}")
    
    def end_combat(self, winner: Optional[str] = None) -> None:
        """End combat and cleanup systems."""
        
        self.active_combat = False
        
        # Stop ambient audio
        self.sound_system.stop_combat_ambience()
        
        # Clear AI managers
        self.ai_manager.ais.clear()
        
        # Play victory/defeat effects
        if winner == "player":
            self.sound_system.play_victory_sound()
            self.effects_system.trigger_turn_transition(True)  # Celebratory effect
        elif winner == "enemy":
            self.sound_system.play_defeat_sound()
        
        # Trigger combat end effects
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.COMBAT_END,
            actor_id="system",
            metadata={"winner": winner}
        ))
        
        # Clear visual effects after delay
        time.sleep(2.0)
        self.effects_system.clear_all_effects()
        
        logging.info(f"Enhanced combat ended, winner: {winner}")
    
    def process_card_play(self, card_data: Dict[str, Any], player_position: Tuple[float, float],
                         target_position: Optional[Tuple[float, float]] = None) -> None:
        """Process card play with full audio-visual feedback."""
        
        card_name = card_data.get("name", "Unknown Card")
        card_type = card_data.get("type", "attack")
        sand_cost = card_data.get("sand_cost", 1)
        
        # Determine card visual type
        visual_card_type = CardType.ATTACK
        if card_type.lower() == "skill":
            visual_card_type = CardType.SKILL
        elif card_type.lower() == "power":
            visual_card_type = CardType.POWER
        elif card_type.lower() in ["status", "curse", "blessing"]:
            visual_card_type = CardType.STATUS
        
        # Trigger visual effects
        self.effects_system.trigger_card_play_effect(
            visual_card_type, player_position, intensity=sand_cost / 3.0
        )
        
        # Trigger audio effects
        self.sound_system.play_card_sound(
            card_type, player_position, intensity=sand_cost / 3.0
        )
        
        # Inform AI about player action
        self.ai_manager.observe_player_action(
            ActionType.PLAY_CARD, card_name, card_type, sand_cost,
            self.combat_participants.get("player", {}).get("health", 100)
        )
        
        # Trigger event
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.CARD_PLAYED,
            actor_id="player",
            position=player_position,
            card_type=card_type,
            value=sand_cost,
            metadata={"card_name": card_name}
        ))
        
        logging.debug(f"Processed card play: {card_name} ({card_type})")
    
    def process_damage(self, attacker_id: str, target_id: str, damage: int,
                      damage_type: str = "physical", position: Optional[Tuple[float, float]] = None,
                      is_critical: bool = False) -> None:
        """Process damage with enhanced feedback."""
        
        if not position:
            # Default position for target
            position = (self.screen_width // 2, self.screen_height // 2)
        
        is_player_damage = target_id == "player"
        
        # Enhanced visual feedback
        self.effects_system.trigger_damage_feedback(
            position, damage, damage_type, is_player_damage
        )
        
        # Audio feedback
        self.sound_system.play_combat_action_sound(
            "damage", position, is_critical, intensity=damage / 20.0
        )
        
        # Update health tracking
        if target_id in self.combat_participants:
            current_health = self.combat_participants[target_id].get("health", 100)
            new_health = max(0, current_health - damage)
            self.combat_participants[target_id]["health"] = new_health
        
        # Trigger event
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.DAMAGE_DEALT,
            actor_id=attacker_id,
            target_id=target_id,
            position=position,
            value=damage,
            damage_type=damage_type,
            metadata={"is_critical": is_critical}
        ))
        
        logging.debug(f"Processed damage: {attacker_id} -> {target_id}, {damage} {damage_type}")
    
    def process_healing(self, healer_id: str, target_id: str, healing: int,
                       healing_type: str = "divine", position: Optional[Tuple[float, float]] = None) -> None:
        """Process healing with enhanced feedback."""
        
        if not position:
            position = (self.screen_width // 2, self.screen_height // 2)
        
        # Enhanced visual feedback
        self.effects_system.trigger_healing_feedback(position, healing, healing_type)
        
        # Audio feedback
        self.sound_system.play_combat_action_sound(
            "healing", position, intensity=healing / 25.0
        )
        
        # Update health tracking
        if target_id in self.combat_participants:
            current_health = self.combat_participants[target_id].get("health", 100)
            max_health = self.combat_participants[target_id].get("max_health", 100)
            new_health = min(max_health, current_health + healing)
            self.combat_participants[target_id]["health"] = new_health
        
        # Trigger event
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.HEALING_RECEIVED,
            actor_id=healer_id,
            target_id=target_id,
            position=position,
            value=healing,
            metadata={"healing_type": healing_type}
        ))
        
        logging.debug(f"Processed healing: {healer_id} -> {target_id}, {healing} {healing_type}")
    
    def process_turn_change(self, is_now_player_turn: bool) -> None:
        """Process turn change with full effects."""
        
        self.current_turn_player = is_now_player_turn
        
        # Visual turn transition
        self.effects_system.trigger_turn_transition(is_now_player_turn)
        
        # Audio turn transition
        self.sound_system.play_turn_transition(is_now_player_turn)
        
        # Sand flow effect
        self.sound_system.play_sand_effect("timer_flip", 1.0)
        
        # Start AI turn timer if enemy turn
        if not is_now_player_turn:
            for ai in self.ai_manager.ais.values():
                if hasattr(ai.player_analyzer, 'start_turn_timing'):
                    ai.player_analyzer.start_turn_timing()
        else:
            # End AI turn timer
            for ai in self.ai_manager.ais.values():
                if hasattr(ai.player_analyzer, 'end_turn_timing'):
                    ai.player_analyzer.end_turn_timing()
        
        # Trigger event
        self._trigger_event(CombatEventData(
            event_type=CombatEvent.TURN_START,
            actor_id="player" if is_now_player_turn else "enemy",
            position=(self.screen_width // 2, self.screen_height // 2)
        ))
        
        logging.debug(f"Turn changed to: {'player' if is_now_player_turn else 'enemy'}")
    
    def process_status_effect(self, target_id: str, status_type: str, is_applied: bool,
                            position: Optional[Tuple[float, float]] = None) -> None:
        """Process status effect application/removal."""
        
        if not position:
            position = (self.screen_width // 2, self.screen_height // 2)
        
        # Visual status feedback
        self.effects_system.trigger_status_effect_feedback(position, status_type, is_applied)
        
        # Audio feedback (could add specific status sounds)
        
        # Trigger event
        event_type = CombatEvent.STATUS_APPLIED if is_applied else CombatEvent.STATUS_REMOVED
        self._trigger_event(CombatEventData(
            event_type=event_type,
            actor_id=target_id,
            position=position,
            status_type=status_type
        ))
        
        logging.debug(f"Status effect: {status_type} {'applied to' if is_applied else 'removed from'} {target_id}")
    
    def update(self, delta_time: float) -> None:
        """Update all systems."""
        
        if not self.active_combat:
            return
        
        # Update visual effects
        self.effects_system.update(delta_time)
        
        # Update AI systems
        player_sand = self.combat_participants.get("player", {}).get("sand", 0)
        self.ai_manager.update_all(player_sand)
        
        # Performance tracking
        current_time = time.time()
        if current_time - self.last_update_time > 1.0:  # Every second
            self.last_update_time = current_time
            # Could add performance metrics here
    
    def render(self, surface) -> None:
        """Render all visual effects."""
        if self.active_combat:
            self.effects_system.render(surface)
    
    def register_event_callback(self, event_type: CombatEvent, callback: Callable) -> None:
        """Register callback for combat events."""
        if event_type not in self.event_callbacks:
            self.event_callbacks[event_type] = []
        self.event_callbacks[event_type].append(callback)
    
    def _trigger_event(self, event_data: CombatEventData) -> None:
        """Trigger event callbacks."""
        self.events_processed += 1
        
        callbacks = self.event_callbacks.get(event_data.event_type, [])
        for callback in callbacks:
            try:
                callback(event_data)
            except Exception as e:
                logging.error(f"Error in event callback: {e}")
    
    def get_ai_status(self, enemy_id: str) -> Optional[Dict[str, Any]]:
        """Get AI status for debugging."""
        ai = self.ai_manager.get_ai(enemy_id)
        return ai.get_ai_status() if ai else None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'active_combat': self.active_combat,
            'current_turn_player': self.current_turn_player,
            'participants': list(self.combat_participants.keys()),
            'events_processed': self.events_processed,
            'effects_system': self.effects_system.get_system_status(),
            'sound_system': self.sound_system.get_system_status(),
            'ai_manager': self.ai_manager.get_system_status()
        }


# Global enhanced combat coordinator
_combat_coordinator: Optional[EnhancedCombatCoordinator] = None


def get_combat_coordinator() -> EnhancedCombatCoordinator:
    """Get the global combat coordinator instance."""
    global _combat_coordinator
    if _combat_coordinator is None:
        _combat_coordinator = EnhancedCombatCoordinator()
    return _combat_coordinator


def initialize_combat_coordinator(screen_width: int = 1200, screen_height: int = 800) -> EnhancedCombatCoordinator:
    """Initialize the global combat coordinator."""
    global _combat_coordinator
    _combat_coordinator = EnhancedCombatCoordinator(screen_width, screen_height)
    return _combat_coordinator


# Convenience functions for easy integration
def trigger_card_play(card_data: Dict[str, Any], position: Tuple[float, float]) -> None:
    """Convenience function to trigger card play effects."""
    coordinator = get_combat_coordinator()
    coordinator.process_card_play(card_data, position)


def trigger_damage(attacker_id: str, target_id: str, damage: int, damage_type: str = "physical",
                  position: Optional[Tuple[float, float]] = None, is_critical: bool = False) -> None:
    """Convenience function to trigger damage effects."""
    coordinator = get_combat_coordinator()
    coordinator.process_damage(attacker_id, target_id, damage, damage_type, position, is_critical)


def trigger_healing(healer_id: str, target_id: str, healing: int, healing_type: str = "divine",
                   position: Optional[Tuple[float, float]] = None) -> None:
    """Convenience function to trigger healing effects."""
    coordinator = get_combat_coordinator()
    coordinator.process_healing(healer_id, target_id, healing, healing_type, position)


def trigger_turn_change(is_player_turn: bool) -> None:
    """Convenience function to trigger turn change effects."""
    coordinator = get_combat_coordinator()
    coordinator.process_turn_change(is_player_turn)


def trigger_status_effect(target_id: str, status_type: str, is_applied: bool,
                         position: Optional[Tuple[float, float]] = None) -> None:
    """Convenience function to trigger status effect feedback."""
    coordinator = get_combat_coordinator()
    coordinator.process_status_effect(target_id, status_type, is_applied, position)