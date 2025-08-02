"""
Scenes package for Sands of Duat
Manages Hub and Arena scenes like Hades
"""

from .scene import Scene, SceneManager
from .hub_scene import HubScene
from .arena_scene import ArenaScene

__all__ = [
    'Scene',
    'SceneManager',
    'HubScene', 
    'ArenaScene'
]