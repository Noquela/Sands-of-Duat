"""
Scene management system for Sands of Duat
Supports Hub (lobby) and Arena (combat) scenes like Hades
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import pygame
from ecs import EntityManager


class Scene(ABC):
    """Base class for all game scenes."""
    
    def __init__(self, game):
        self.game = game
        self.entity_manager = EntityManager()
        self.systems = []
        self.initialized = False
        self.transition_data: Dict[str, Any] = {}
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the scene."""
        pass
    
    @abstractmethod
    def update(self, dt: float) -> Optional[str]:
        """Update scene logic. Return scene name to transition to, or None."""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene."""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        pass
    
    def cleanup(self) -> None:
        """Clean up scene resources."""
        self.entity_manager.clear_all()
        self.systems.clear()
    
    def set_transition_data(self, data: Dict[str, Any]) -> None:
        """Set data to pass to next scene."""
        self.transition_data = data
    
    def get_transition_data(self) -> Dict[str, Any]:
        """Get data from previous scene."""
        return self.transition_data


class SceneManager:
    """Manages scene transitions and state."""
    
    def __init__(self, game):
        self.game = game
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None
        self.transition_data: Dict[str, Any] = {}
    
    def register_scene(self, name: str, scene: Scene) -> None:
        """Register a scene with the manager."""
        self.scenes[name] = scene
    
    def transition_to(self, scene_name: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """Transition to a different scene."""
        if scene_name not in self.scenes:
            print(f"Warning: Scene '{scene_name}' not found")
            return False
        
        # Cleanup current scene
        if self.current_scene is not None:
            self.current_scene.cleanup()
        
        # Switch to new scene
        self.current_scene = self.scenes[scene_name]
        self.current_scene_name = scene_name
        
        # Pass transition data
        if data is not None:
            self.current_scene.set_transition_data(data)
        
        # Initialize if needed
        if not self.current_scene.initialized:
            self.current_scene.initialize()
            self.current_scene.initialized = True
        
        print(f"Transitioned to scene: {scene_name}")
        return True
    
    def update(self, dt: float) -> None:
        """Update current scene and handle transitions."""
        if self.current_scene is None:
            return
        
        # Update scene and check for transition
        next_scene = self.current_scene.update(dt)
        if next_scene is not None and next_scene != self.current_scene_name:
            self.transition_to(next_scene, self.current_scene.get_transition_data())
    
    def render(self, screen: pygame.Surface) -> None:
        """Render current scene."""
        if self.current_scene is not None:
            self.current_scene.render(screen)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Forward event to current scene."""
        if self.current_scene is not None:
            self.current_scene.handle_event(event)
    
    def get_current_scene_name(self) -> Optional[str]:
        """Get the name of the current scene."""
        return self.current_scene_name