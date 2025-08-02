"""
ECS (Entity-Component-System) package for Sands of Duat
"""

from .entity import EntityManager, EntityBuilder, create_player_entity, create_scarab_enemy
from .components import *
from .systems import *

__all__ = [
    'EntityManager',
    'EntityBuilder', 
    'create_player_entity',
    'create_scarab_enemy',
    'System',
    'InputSystem',
    'MovementSystem',
    'AnimationSystem',
    'RenderSystem',
    'CameraSystem',
    'Transform',
    'SpriteRenderer',
    'InputController',
    'Movement',
    'Animation',
    'Health',
    'Combat',
    'PlayerTag',
    'EnemyTag',
    'Camera'
]