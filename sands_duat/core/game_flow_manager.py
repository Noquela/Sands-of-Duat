"""
Game Flow Manager

Orchestrates the main game loop and screen transitions for the complete
Sands of Duat gameplay experience. Handles run progression, state management,
and transitions between different game phases.

Key Features:
- Run initialization and progression
- Screen transition management
- Game state persistence
- Victory/defeat condition handling
- Node progression through the 12 hours of night
"""

import logging
from enum import Enum
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
import random

from .hourglass import HourGlass
from .cards import Card, CardLibrary, Deck
from .combat_manager import CombatManager
from .save_system import SaveSystem
from .player_collection import PlayerCollection
from .game_progression_manager import GameProgressionManager


class GameScreen(Enum):
    """Available game screens."""
    MENU = "menu"
    MAP = "map"
    COMBAT = "combat"
    DYNAMIC_COMBAT = "dynamic_combat"
    DECK_BUILDER = "deck_builder"
    SHOP = "shop"
    REST = "rest"
    EVENT = "event"
    TUTORIAL = "tutorial"
    PROGRESSION = "progression"
    VICTORY = "victory"
    DEFEAT = "defeat"


class RunPhase(Enum):
    """Current phase of the run."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class GameState:
    """Current state of the game session."""
    current_screen: GameScreen = GameScreen.MENU
    run_phase: RunPhase = RunPhase.NOT_STARTED
    current_hour: int = 1  # Current hour of the night (1-12)
    current_node: int = 0  # Current node in the hour
    
    # Player state
    player_health: int = 75
    player_max_health: int = 75
    player_gold: int = 100
    
    # Run progress
    nodes_completed: int = 0
    bosses_defeated: int = 0
    hours_completed: int = 0
    
    # Collections
    deck: List[Card] = field(default_factory=list)
    collection: List[Card] = field(default_factory=list)
    
    # Combat state
    in_combat: bool = False
    current_enemy: Optional[str] = None
    
    # Event state
    pending_rewards: Dict[str, Any] = field(default_factory=dict)
    

class GameFlowManager:
    """
    Manages the main game flow and screen transitions.
    
    Coordinates between all game systems to provide a seamless
    gameplay experience from menu to victory/defeat.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.state = GameState()
        self.ui_manager = None  # Will be set by main
        
        # Game systems
        self.save_system = SaveSystem()
        self.player_collection = PlayerCollection()
        self.progression_manager = GameProgressionManager()
        self.combat_manager = None
        
        # Event handlers
        self.screen_handlers: Dict[GameScreen, Callable] = {}
        self.transition_callbacks: List[Callable] = []
        
        # Run configuration
        self.nodes_per_hour = 8  # 8 nodes per hour of night
        self.total_hours = 12
        
        self.logger.info("Game Flow Manager initialized")
    
    def set_ui_manager(self, ui_manager) -> None:
        """Set the UI manager reference."""
        self.ui_manager = ui_manager
    
    def set_combat_manager(self, combat_manager: CombatManager) -> None:
        """Set the combat manager reference."""
        self.combat_manager = combat_manager
    
    def register_screen_handler(self, screen: GameScreen, handler: Callable) -> None:
        """Register a handler for screen-specific events."""
        self.screen_handlers[screen] = handler
    
    def add_transition_callback(self, callback: Callable) -> None:
        """Add a callback to be called on screen transitions."""
        self.transition_callbacks.append(callback)
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.state
    
    def start_new_run(self, starting_deck_type: str = "wanderer") -> bool:
        """
        Start a new run with the specified starting deck.
        
        Args:
            starting_deck_type: Type of starting deck (wanderer, mystic, warrior)
            
        Returns:
            True if run started successfully
        """
        try:
            self.logger.info(f"Starting new run with {starting_deck_type} deck")
            
            # Reset state
            self.state = GameState()
            self.state.run_phase = RunPhase.IN_PROGRESS
            
            # Load starting deck
            self._setup_starting_deck(starting_deck_type)
            
            # Initialize player stats
            self.state.player_health = 75
            self.state.player_max_health = 75
            self.state.player_gold = 100
            
            # Transition to progression screen (temple map)
            self.transition_to_screen(GameScreen.PROGRESSION)
            
            self.logger.info("New run started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start new run: {e}")
            return False
    
    def continue_run(self) -> bool:
        """
        Continue an existing run from save data.
        
        Returns:
            True if run continued successfully
        """
        try:
            # Load save data
            save_data = self.save_system.load_save("quicksave")
            if not save_data:
                self.logger.warning("No save data found")
                return False
            
            # Restore game state
            self._restore_state_from_save(save_data)
            
            # Transition to appropriate screen based on state
            if self.state.in_combat:
                self.transition_to_screen(GameScreen.COMBAT)
            else:
                self.transition_to_screen(GameScreen.PROGRESSION)
            
            self.logger.info("Run continued successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to continue run: {e}")
            return False
    
    def transition_to_screen(self, target_screen: GameScreen, 
                           transition_type: str = "fade", 
                           context: Optional[Dict[str, Any]] = None) -> None:
        """
        Transition to a new screen with optional context data.
        
        Args:
            target_screen: Screen to transition to
            transition_type: Type of transition animation
            context: Additional context data for the screen
        """
        self.logger.info(f"Transitioning from {self.state.current_screen.value} to {target_screen.value}")
        
        # Save current state
        self._save_current_state()
        
        # Prepare screen-specific data
        screen_context = context or {}
        self._prepare_screen_context(target_screen, screen_context)
        
        # Update state
        self.state.current_screen = target_screen
        
        # Notify UI manager of transition
        if self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition(
                target_screen.value, 
                transition_type,
                screen_context
            )
        
        # Call screen handler if registered
        if target_screen in self.screen_handlers:
            self.screen_handlers[target_screen](screen_context)
        
        # Notify transition callbacks
        for callback in self.transition_callbacks:
            callback(target_screen, screen_context)
    
    def handle_combat_victory(self, rewards: Dict[str, Any]) -> None:
        """
        Handle victory in combat.
        
        Args:
            rewards: Rewards earned from combat
        """
        self.logger.info("Combat victory - processing rewards")
        
        # Process rewards
        self._process_combat_rewards(rewards)
        
        # Mark node as completed
        self.state.nodes_completed += 1
        self.state.in_combat = False
        
        # Check if hour is completed (boss defeated)
        if self._is_hour_boss_defeated():
            self.state.hours_completed += 1
            self.state.current_hour += 1
            
            # Check for run completion
            if self.state.current_hour > self.total_hours:
                self.handle_run_victory()
                return
        
        # Prepare victory data with progress information
        victory_data = {
            'gold_earned': rewards.get('gold', 0),
            'total_gold': self.state.player_gold,
            'nodes_completed': self.state.nodes_completed,
            'hours_completed': self.state.hours_completed,
            'run_completed': False
        }
        
        # Show victory screen first, then they can continue to map
        context = {'victory_data': victory_data}
        self.transition_to_screen(GameScreen.VICTORY, context=context)
    
    def handle_combat_defeat(self) -> None:
        """Handle defeat in combat."""
        self.logger.info("Combat defeat - ending run")
        
        self.state.run_phase = RunPhase.FAILED
        self.transition_to_screen(GameScreen.DEFEAT)
    
    def handle_run_victory(self) -> None:
        """Handle successful completion of the run."""
        self.logger.info("Run completed successfully!")
        
        self.state.run_phase = RunPhase.COMPLETED
        
        # Process final rewards and unlock progression
        self._process_run_completion_rewards()
        
        self.transition_to_screen(GameScreen.VICTORY)
    
    def handle_node_selection(self, node_type: str, node_data: Dict[str, Any]) -> None:
        """
        Handle selection of a node on the map.
        
        Args:
            node_type: Type of node (combat, event, shop, rest, boss)
            node_data: Additional data about the node
        """
        self.logger.info(f"Selected {node_type} node")
        
        if node_type == "combat":
            self._initiate_combat(node_data)
        elif node_type == "event":
            self._initiate_event(node_data)
        elif node_type == "shop":
            self.transition_to_screen(GameScreen.SHOP, context=node_data)
        elif node_type == "rest":
            self.transition_to_screen(GameScreen.REST, context=node_data)
        elif node_type == "boss":
            self._initiate_boss_combat(node_data)
        else:
            self.logger.warning(f"Unknown node type: {node_type}")
    
    def _setup_starting_deck(self, deck_type: str) -> None:
        """Set up the starting deck based on chosen class."""
        # Load starting deck from content system
        from ..content.starter_cards import get_starter_deck
        
        starter_deck = get_starter_deck(deck_type)
        starter_cards = starter_deck.cards if hasattr(starter_deck, 'cards') else list(starter_deck)
        self.state.deck = starter_cards.copy()
        self.state.collection = starter_cards.copy()
        
        self.logger.info(f"Loaded {len(starter_cards)} cards for {deck_type} deck")
    
    def _save_current_state(self) -> None:
        """Save the current game state."""
        try:
            # For now, just trigger a basic save
            # In a full implementation, this would store the actual game state
            self.save_system.save_game("quicksave")
            self.logger.info("Game state saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save game state: {e}")
    
    def _restore_state_from_save(self, save_data) -> None:
        """Restore game state from save data."""
        # For now, just create a basic restored state
        # In a full implementation, this would parse the save_data object
        self.state = GameState()
        self.state.run_phase = RunPhase.IN_PROGRESS
        
        self.logger.info("Game state restored from save (basic implementation)")
    
    def _prepare_screen_context(self, screen: GameScreen, context: Dict[str, Any]) -> None:
        """Prepare context data for the target screen."""
        # Add common game state to context
        context['game_state'] = self.state
        context['player_health'] = self.state.player_health
        context['player_gold'] = self.state.player_gold
        context['current_hour'] = self.state.current_hour
        
        # Screen-specific context preparation
        if screen == GameScreen.COMBAT:
            context['player_deck'] = self.state.deck
            context['player_health'] = self.state.player_health
        
        elif screen == GameScreen.MAP:
            context['current_node'] = self.state.current_node
            context['nodes_completed'] = self.state.nodes_completed
            context['current_hour'] = self.state.current_hour
        
        elif screen == GameScreen.DECK_BUILDER:
            context['deck'] = self.state.deck
            context['collection'] = self.state.collection
    
    def _initiate_combat(self, node_data: Dict[str, Any]) -> None:
        """Initiate combat with specified enemy."""
        enemy_id = node_data.get('enemy_id', 'desert_mummy')
        
        self.state.in_combat = True
        self.state.current_enemy = enemy_id
        
        # Set up combat manager if available
        if self.combat_manager:
            # Combat manager will be configured by the combat screen
            pass
        
        context = {
            'enemy_id': enemy_id,
            'player_deck': self.state.deck,
            'player_health': self.state.player_health
        }
        
        print(f"TRANSITIONING TO DYNAMIC_COMBAT WITH ENEMY: {enemy_id}")  # DEBUG
        self.transition_to_screen(GameScreen.DYNAMIC_COMBAT, context=context)
    
    def _initiate_boss_combat(self, node_data: Dict[str, Any]) -> None:
        """Initiate boss combat."""
        boss_id = node_data.get('boss_id', f'hour_{self.state.current_hour}_boss')
        
        self.logger.info(f"Initiating boss combat: {boss_id}")
        
        context = {
            'enemy_id': boss_id,
            'is_boss': True,
            'player_deck': self.state.deck,
            'player_health': self.state.player_health
        }
        
        self._initiate_combat(context)
    
    def _initiate_event(self, node_data: Dict[str, Any]) -> None:
        """Initiate an event."""
        event_id = node_data.get('event_id', 'random')
        
        context = {
            'event_id': event_id,
            'player_gold': self.state.player_gold
        }
        
        self.transition_to_screen(GameScreen.EVENT, context=context)
    
    def _process_combat_rewards(self, rewards: Dict[str, Any]) -> None:
        """Process rewards from combat victory."""
        # Add gold
        gold_reward = rewards.get('gold', 0)
        self.state.player_gold += gold_reward
        
        # Add cards to collection
        card_rewards = rewards.get('cards', [])
        if card_rewards:
            self.state.collection.extend(card_rewards)
            self.logger.info(f"Added {len(card_rewards)} cards to collection")
        
        # Process other rewards
        if 'health' in rewards:
            healing = rewards['health']
            self.state.player_health = min(
                self.state.player_max_health,
                self.state.player_health + healing
            )
        
        self.logger.info(f"Processed combat rewards: {rewards}")
    
    def _process_run_completion_rewards(self) -> None:
        """Process rewards for completing the entire run."""
        # Unlock progression rewards
        self.progression_manager.complete_run(
            hours_completed=self.state.hours_completed,
            final_score=self._calculate_final_score()
        )
        
        # Add run completion card rewards to collection
        self.player_collection.add_run_completion_rewards()
        
        self.logger.info("Processed run completion rewards")
    
    def _calculate_final_score(self) -> int:
        """Calculate final score for the run."""
        base_score = self.state.hours_completed * 1000
        bonus_score = self.state.nodes_completed * 100
        health_bonus = self.state.player_health * 10
        
        return base_score + bonus_score + health_bonus
    
    def _is_hour_boss_defeated(self) -> bool:
        """Check if the current hour's boss has been defeated."""
        # Check if this was a boss combat
        return (self.state.current_enemy and 
                'boss' in self.state.current_enemy.lower())
    
    def update(self, delta_time: float) -> None:
        """Update the game flow manager."""
        # Update underlying systems
        if self.progression_manager:
            self.progression_manager.update(delta_time)
        
        # Handle any pending state changes
        if self.state.run_phase == RunPhase.FAILED:
            # Handle run failure cleanup
            pass
        elif self.state.run_phase == RunPhase.COMPLETED:
            # Handle run completion cleanup
            pass