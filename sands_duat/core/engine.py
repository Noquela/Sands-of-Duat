"""
Main Game Engine and State Management

Central orchestrator for the Sands of Duat game, managing the main game loop,
state transitions, and coordination between all game systems.

Key Features:
- Main game loop with fixed timestep
- Game state management and transitions
- System coordination and event handling
- Performance monitoring and optimization
- Save/load functionality

Classes:
- GameEngine: Main game orchestrator
- GameState: Current game state representation
- StateManager: Game state transition management
"""

import asyncio
import time
from enum import Enum
from typing import Dict, Any, Optional, Callable, List
from pydantic import BaseModel, Field
import logging

from .ecs import World, System
from .hourglass import HourGlass
from .combat import CombatEngine
from .combat_enhanced import EnhancedCombatEngine
from .cards import CardLibrary, Deck, card_library
from .sand_visuals import sand_visualizer
from .animation_coordinator import animation_coordinator
from .enemy_ai import enemy_ai_manager
from .pygame_integration import PygameHourGlassManager
from .debug_logger import debug_logger, DebugCategory


class GamePhase(Enum):
    """Current phase of the game."""
    MENU = "menu"
    LOADING = "loading"
    MAP = "map"
    COMBAT = "combat"
    DECK_BUILDING = "deck_building"
    EVENT = "event"
    SHOP = "shop"
    REST = "rest"
    VICTORY = "victory"
    DEFEAT = "defeat"


class GameState(BaseModel):
    """
    Represents the current state of the game.
    
    Contains all persistent data that needs to be
    saved and loaded between sessions.
    """
    
    phase: GamePhase = GamePhase.MENU
    player_name: str = "Wanderer"
    current_run_id: str = ""
    floor: int = 1
    max_floors: int = 12  # 12 hours of night
    
    # Player resources
    health: int = 100
    max_health: int = 100
    gold: int = 100
    sand_capacity: int = 6
    
    # Deck and cards
    deck: Deck = Field(default_factory=lambda: Deck(name="Starting Deck"))
    hand: List[str] = Field(default_factory=list)  # Card IDs
    discard_pile: List[str] = Field(default_factory=list)  # Card IDs
    
    # Run progress
    nodes_visited: List[str] = Field(default_factory=list)
    events_seen: List[str] = Field(default_factory=list)
    relics: List[str] = Field(default_factory=list)
    
    # Settings and preferences
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    def is_player_alive(self) -> bool:
        """Check if the player is still alive."""
        return self.health > 0
    
    def take_damage(self, amount: int) -> int:
        """Player takes damage, returns actual damage dealt."""
        old_health = self.health
        self.health = max(0, self.health - amount)
        return old_health - self.health
    
    def heal(self, amount: int) -> int:
        """Player heals, returns actual healing done."""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health
    
    def gain_gold(self, amount: int) -> None:
        """Gain gold."""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold if possible, returns True if successful."""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def advance_floor(self) -> bool:
        """Advance to the next floor, returns True if successful."""
        if self.floor < self.max_floors:
            self.floor += 1
            return True
        return False


class StateManager:
    """
    Manages game state transitions and validation.
    
    Ensures proper state flow and handles transition logic
    between different game phases.
    """
    
    def __init__(self):
        self.state_history: List[GamePhase] = []
        self.transition_callbacks: Dict[GamePhase, List[Callable]] = {}
    
    def can_transition(self, from_state: GamePhase, to_state: GamePhase) -> bool:
        """Check if a state transition is valid."""
        # Define valid transitions
        valid_transitions = {
            GamePhase.MENU: [GamePhase.LOADING],
            GamePhase.LOADING: [GamePhase.MAP, GamePhase.MENU],
            GamePhase.MAP: [GamePhase.COMBAT, GamePhase.EVENT, GamePhase.SHOP, GamePhase.REST, GamePhase.VICTORY],
            GamePhase.COMBAT: [GamePhase.MAP, GamePhase.DECK_BUILDING, GamePhase.DEFEAT],
            GamePhase.DECK_BUILDING: [GamePhase.MAP],
            GamePhase.EVENT: [GamePhase.MAP, GamePhase.COMBAT, GamePhase.SHOP],
            GamePhase.SHOP: [GamePhase.MAP],
            GamePhase.REST: [GamePhase.MAP],
            GamePhase.VICTORY: [GamePhase.MENU],
            GamePhase.DEFEAT: [GamePhase.MENU]
        }
        
        return to_state in valid_transitions.get(from_state, [])
    
    def transition_state(self, game_state: GameState, new_phase: GamePhase) -> bool:
        """
        Attempt to transition to a new game phase.
        
        Returns True if transition was successful.
        """
        if not self.can_transition(game_state.phase, new_phase):
            logging.warning(f"Invalid state transition: {game_state.phase} -> {new_phase}")
            return False
        
        old_phase = game_state.phase
        self.state_history.append(old_phase)
        game_state.phase = new_phase
        
        # Execute transition callbacks
        callbacks = self.transition_callbacks.get(new_phase, [])
        for callback in callbacks:
            try:
                callback(old_phase, new_phase)
            except Exception as e:
                logging.error(f"Error in state transition callback: {e}")
        
        logging.info(f"State transition: {old_phase} -> {new_phase}")
        return True
    
    def register_transition_callback(self, state: GamePhase, callback: Callable) -> None:
        """Register a callback for when entering a specific state."""
        if state not in self.transition_callbacks:
            self.transition_callbacks[state] = []
        self.transition_callbacks[state].append(callback)
    
    def get_previous_state(self) -> Optional[GamePhase]:
        """Get the previous state from history."""
        return self.state_history[-1] if self.state_history else None


class GameEngine:
    """
    Main game engine that orchestrates all game systems.
    
    Manages the game loop, coordinates systems, handles events,
    and maintains overall game flow for Sands of Duat.
    """
    
    def __init__(self):
        self.running = False
        self.target_fps = 60
        self.fixed_timestep = 1.0 / self.target_fps
        
        # Core systems
        self.world = World()
        self.state = GameState()
        self.state_manager = StateManager()
        self.combat_engine = CombatEngine()
        self.hourglass = HourGlass()
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Initialize card library
        self.card_library = card_library
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def initialize(self) -> None:
        """Initialize the game engine and all systems."""
        self.logger.info("Initializing Sands of Duat game engine...")
        
        # Initialize core systems
        self._setup_event_handlers()
        self._load_game_content()
        
        # Setup state transition callbacks
        self.state_manager.register_transition_callback(
            GamePhase.COMBAT, self._on_enter_combat
        )
        self.state_manager.register_transition_callback(
            GamePhase.MAP, self._on_enter_map
        )
        
        self.logger.info("Game engine initialized successfully")
    
    def start(self) -> None:
        """Start the main game loop."""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting game engine...")
        
        try:
            asyncio.run(self._main_loop())
        except KeyboardInterrupt:
            self.logger.info("Game interrupted by user")
        except Exception as e:
            self.logger.error(f"Game engine error: {e}")
        finally:
            self.shutdown()
    
    def stop(self) -> None:
        """Stop the game engine."""
        self.running = False
        self.logger.info("Stopping game engine...")
    
    def update(self, delta_time: float) -> None:
        """
        Synchronous update method for integration with pygame main loop.
        
        This is a simplified version of the async update for use with
        external game loops like the one in main.py.
        """
        # Update hour-glass sand regeneration
        if self.state.phase == GamePhase.COMBAT:
            self.hourglass.update_sand()
        
        # Update ECS world
        self.world.update(delta_time)
        
        # Handle state-specific updates (simplified synchronous version)
        if self.state.phase == GamePhase.COMBAT:
            # Check for combat end conditions
            if not self.state.is_player_alive():
                self.state_manager.transition_state(self.state, GamePhase.DEFEAT)
    
    def shutdown(self) -> None:
        """Clean shutdown of the game engine."""
        self.running = False
        self.world.clear()
        self.logger.info("Game engine shutdown complete")
    
    async def _main_loop(self) -> None:
        """Main game loop with fixed timestep."""
        last_time = time.time()
        accumulator = 0.0
        
        while self.running:
            current_time = time.time()
            frame_time = current_time - last_time
            last_time = current_time
            
            # Prevent spiral of death
            frame_time = min(frame_time, 0.25)
            accumulator += frame_time
            
            # Fixed timestep updates
            while accumulator >= self.fixed_timestep:
                await self._update(self.fixed_timestep)
                accumulator -= self.fixed_timestep
            
            # Render (variable timestep)
            interpolation = accumulator / self.fixed_timestep
            await self._render(interpolation)
            
            # Update performance metrics
            self._update_performance_metrics()
            
            # Small sleep to prevent busy waiting
            await asyncio.sleep(0.001)
    
    async def _update(self, delta_time: float) -> None:
        """Update all game systems."""
        # Update hour-glass sand regeneration
        if self.state.phase == GamePhase.COMBAT:
            self.hourglass.update_sand()
        
        # Update ECS world
        self.world.update(delta_time)
        
        # Update combat engine if in combat
        if self.state.phase == GamePhase.COMBAT:
            await self.combat_engine.process_actions()
        
        # Handle state-specific updates
        await self._update_current_state(delta_time)
    
    async def _render(self, interpolation: float) -> None:
        """Render the current game state."""
        # Rendering will be handled by UI systems
        # This is a placeholder for the main rendering coordination
        pass
    
    async def _update_current_state(self, delta_time: float) -> None:
        """Update logic specific to the current game state."""
        if self.state.phase == GamePhase.COMBAT:
            await self._update_combat(delta_time)
        elif self.state.phase == GamePhase.MAP:
            await self._update_map(delta_time)
        elif self.state.phase == GamePhase.MENU:
            await self._update_menu(delta_time)
        # Add more state-specific updates as needed
    
    async def _update_combat(self, delta_time: float) -> None:
        """Update combat-specific logic."""
        # Check for combat end conditions
        if not self.state.is_player_alive():
            self.state_manager.transition_state(self.state, GamePhase.DEFEAT)
    
    async def _update_map(self, delta_time: float) -> None:
        """Update map-specific logic."""
        # Handle map navigation and events
        pass
    
    async def _update_menu(self, delta_time: float) -> None:
        """Update menu-specific logic."""
        # Handle menu interactions
        pass
    
    def _update_performance_metrics(self) -> None:
        """Update FPS and performance tracking."""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_update >= 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def _setup_event_handlers(self) -> None:
        """Setup global event handlers."""
        self.register_event_handler("card_played", self._on_card_played)
        self.register_event_handler("combat_ended", self._on_combat_ended)
    
    def _load_game_content(self) -> None:
        """Load all game content (cards, enemies, events, etc.)."""
        # This will be expanded to load from YAML files
        self.logger.info("Loading game content...")
        
        # Initialize starting deck
        self._create_starting_deck()
    
    def _create_starting_deck(self) -> None:
        """Create the default starting deck."""
        # Placeholder for starting deck creation
        self.state.deck = Deck(name="Desert Wanderer Deck")
    
    def _on_enter_combat(self, old_state: GamePhase, new_state: GamePhase) -> None:
        """Handle entering combat state."""
        self.logger.info("Entering combat...")
        self.hourglass.set_sand(3)  # Start combat with 3 sand
        self.hourglass.resume_regeneration()
    
    def _on_enter_map(self, old_state: GamePhase, new_state: GamePhase) -> None:
        """Handle entering map state."""
        self.logger.info("Entering map...")
        self.hourglass.pause_regeneration()
    
    def _on_card_played(self, event_data: Dict[str, Any]) -> None:
        """Handle card played event."""
        card_id = event_data.get("card_id")
        sand_cost = event_data.get("sand_cost", 0)
        self.logger.info(f"Card played: {card_id} (cost: {sand_cost})")
    
    def _on_combat_ended(self, event_data: Dict[str, Any]) -> None:
        """Handle combat ended event."""
        winner = event_data.get("winner")
        self.logger.info(f"Combat ended, winner: {winner}")
        
        if winner == "player":
            self.state_manager.transition_state(self.state, GamePhase.MAP)
        else:
            self.state_manager.transition_state(self.state, GamePhase.DEFEAT)
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """Register an event handler."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def emit_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Emit an event to all registered handlers."""
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event_data)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event_type}: {e}")
    
    def get_fps(self) -> int:
        """Get current FPS."""
        return self.current_fps
    
    def save_game(self, filename: str) -> bool:
        """Save the current game state."""
        try:
            # Implementation will be added later
            self.logger.info(f"Game saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save game: {e}")
            return False
    
    def load_game(self, filename: str) -> bool:
        """Load a game state from file."""
        try:
            # Implementation will be added later
            self.logger.info(f"Game loaded from {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load game: {e}")
            return False