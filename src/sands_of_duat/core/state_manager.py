"""
Game State Manager - Handles smooth transitions between game states.
Provides Hades-level polish for state changes.
"""

from enum import Enum, auto
from typing import Dict, Optional, Any, Callable
import pygame
import time
from dataclasses import dataclass

from .constants import Timing, Colors

class GameState(Enum):
    """All possible game states."""
    SPLASH = auto()
    MAIN_MENU = auto()
    DECK_BUILDER = auto()
    COMBAT = auto()
    SETTINGS = auto()
    COLLECTION = auto()
    ANIMATION_GENERATOR = auto()
    VICTORY = auto()
    DEFEAT = auto()
    LOADING = auto()
    PAUSED = auto()
    QUIT = auto()

@dataclass
class StateTransition:
    """Represents a state transition with animation data."""
    from_state: GameState
    to_state: GameState
    transition_type: str = "fade"
    duration: float = Timing.FADE_DURATION
    start_time: float = 0.0
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}

class StateManager:
    """
    Manages game states with smooth Hades-style transitions.
    Handles state changes, transition animations, and data passing.
    """
    
    def __init__(self):
        self.current_state = GameState.SPLASH
        self.previous_state = None
        self.target_state = None
        
        # Transition system
        self.transitioning = False
        self.current_transition: Optional[StateTransition] = None
        self.transition_progress = 0.0
        
        # State stack for pause/resume functionality
        self.state_stack = []
        
        # State data storage
        self.state_data: Dict[GameState, Dict[str, Any]] = {}
        
        # Callbacks for state changes
        self.enter_callbacks: Dict[GameState, Callable] = {}
        self.exit_callbacks: Dict[GameState, Callable] = {}
        self.update_callbacks: Dict[GameState, Callable] = {}
        self.render_callbacks: Dict[GameState, Callable] = {}
        
        # Initialize state data
        for state in GameState:
            self.state_data[state] = {}
    
    def register_state_callbacks(self, state: GameState, 
                                enter_callback: Callable = None,
                                exit_callback: Callable = None,
                                update_callback: Callable = None,
                                render_callback: Callable = None):
        """Register callbacks for a specific game state."""
        if enter_callback:
            self.enter_callbacks[state] = enter_callback
        if exit_callback:
            self.exit_callbacks[state] = exit_callback
        if update_callback:
            self.update_callbacks[state] = update_callback
        if render_callback:
            self.render_callbacks[state] = render_callback
    
    def change_state(self, new_state: GameState, 
                    transition_type: str = "fade",
                    duration: float = None,
                    data: Dict[str, Any] = None):
        """
        Initiate a smooth transition to a new state.
        
        Args:
            new_state: Target game state
            transition_type: Type of transition ("fade", "slide_left", "slide_right", etc.)
            duration: Transition duration in seconds
            data: Data to pass to the new state
        """
        if new_state == self.current_state and not self.transitioning:
            return
        
        if duration is None:
            duration = Timing.FADE_DURATION
        
        # Create transition object
        self.current_transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            transition_type=transition_type,
            duration=duration,
            start_time=time.time(),
            data=data or {}
        )
        
        self.target_state = new_state
        self.transitioning = True
        self.transition_progress = 0.0
    
    def push_state(self, new_state: GameState, data: Dict[str, Any] = None):
        """
        Push current state to stack and change to new state.
        Used for pause menus, modal dialogs, etc.
        """
        self.state_stack.append(self.current_state)
        self.change_state(new_state, data=data)
    
    def pop_state(self, data: Dict[str, Any] = None):
        """
        Pop the most recent state from stack and return to it.
        """
        if self.state_stack:
            previous_state = self.state_stack.pop()
            self.change_state(previous_state, data=data)
    
    def update(self, dt: float):
        """
        Update the state manager and handle transitions.
        
        Args:
            dt: Delta time in seconds
        """
        if self.transitioning and self.current_transition:
            # Update transition progress
            elapsed = time.time() - self.current_transition.start_time
            self.transition_progress = min(1.0, elapsed / self.current_transition.duration)
            
            # Check if transition is complete
            if self.transition_progress >= 1.0:
                self._complete_transition()
        
        # Update current state
        if self.current_state in self.update_callbacks:
            self.update_callbacks[self.current_state](dt)
    
    def render(self, screen: pygame.Surface):
        """
        Render current state with transition effects.
        
        Args:
            screen: Pygame surface to render to
        """
        if self.transitioning and self.current_transition:
            self._render_transition(screen)
        else:
            # Render current state normally
            if self.current_state in self.render_callbacks:
                self.render_callbacks[self.current_state](screen)
    
    def _complete_transition(self):
        """Complete the current state transition."""
        if not self.current_transition:
            return
        
        # Call exit callback for old state
        if self.current_state in self.exit_callbacks:
            self.exit_callbacks[self.current_state]()
        
        # Update states
        self.previous_state = self.current_state
        self.current_state = self.target_state
        
        # Pass data to new state
        if self.current_transition.data:
            self.state_data[self.current_state].update(self.current_transition.data)
        
        # Call enter callback for new state
        if self.current_state in self.enter_callbacks:
            self.enter_callbacks[self.current_state]()
        
        # Reset transition state
        self.transitioning = False
        self.current_transition = None
        self.transition_progress = 0.0
        self.target_state = None
    
    def _render_transition(self, screen: pygame.Surface):
        """
        Render transition effects between states.
        
        Args:
            screen: Pygame surface to render to
        """
        if not self.current_transition:
            return
        
        transition_type = self.current_transition.transition_type
        progress = self.transition_progress
        
        # Create surfaces for old and new states
        old_surface = pygame.Surface(screen.get_size())
        new_surface = pygame.Surface(screen.get_size())
        
        # Render old state
        if self.current_state in self.render_callbacks:
            self.render_callbacks[self.current_state](old_surface)
        
        # Render new state
        if self.target_state in self.render_callbacks:
            self.render_callbacks[self.target_state](new_surface)
        
        # Apply transition effect
        if transition_type == "fade":
            self._render_fade_transition(screen, old_surface, new_surface, progress)
        elif transition_type == "slide_left":
            self._render_slide_transition(screen, old_surface, new_surface, progress, -1)
        elif transition_type == "slide_right":
            self._render_slide_transition(screen, old_surface, new_surface, progress, 1)
        elif transition_type == "slide_up":
            self._render_slide_transition(screen, old_surface, new_surface, progress, 0, -1)
        elif transition_type == "slide_down":
            self._render_slide_transition(screen, old_surface, new_surface, progress, 0, 1)
        else:
            # Default to fade
            self._render_fade_transition(screen, old_surface, new_surface, progress)
    
    def _render_fade_transition(self, screen: pygame.Surface, 
                              old_surface: pygame.Surface, 
                              new_surface: pygame.Surface, 
                              progress: float):
        """Render a smooth fade transition."""
        # Draw old state
        screen.blit(old_surface, (0, 0))
        
        # Draw new state with alpha
        alpha = int(255 * progress)
        new_surface.set_alpha(alpha)
        screen.blit(new_surface, (0, 0))
    
    def _render_slide_transition(self, screen: pygame.Surface,
                               old_surface: pygame.Surface,
                               new_surface: pygame.Surface,
                               progress: float,
                               x_dir: int = 0,
                               y_dir: int = 0):
        """Render a sliding transition."""
        screen_width, screen_height = screen.get_size()
        
        # Calculate positions
        offset_x = int(screen_width * progress * x_dir)
        offset_y = int(screen_height * progress * y_dir)
        
        # Draw old state (moving out)
        screen.blit(old_surface, (offset_x, offset_y))
        
        # Draw new state (moving in)
        new_x = offset_x - (screen_width * x_dir if x_dir != 0 else 0)
        new_y = offset_y - (screen_height * y_dir if y_dir != 0 else 0)
        screen.blit(new_surface, (new_x, new_y))
    
    def get_state_data(self, state: GameState = None) -> Dict[str, Any]:
        """
        Get data for a specific state (or current state if None).
        
        Args:
            state: State to get data for, or None for current state
            
        Returns:
            Dictionary of state data
        """
        target_state = state or self.current_state
        return self.state_data.get(target_state, {})
    
    def set_state_data(self, key: str, value: Any, state: GameState = None):
        """
        Set data for a specific state (or current state if None).
        
        Args:
            key: Data key
            value: Data value
            state: State to set data for, or None for current state
        """
        target_state = state or self.current_state
        if target_state not in self.state_data:
            self.state_data[target_state] = {}
        self.state_data[target_state][key] = value
    
    def is_transitioning(self) -> bool:
        """Check if currently transitioning between states."""
        return self.transitioning
    
    def get_current_state(self) -> GameState:
        """Get the current game state."""
        return self.current_state
    
    def get_transition_progress(self) -> float:
        """Get current transition progress (0.0 to 1.0)."""
        return self.transition_progress if self.transitioning else 1.0