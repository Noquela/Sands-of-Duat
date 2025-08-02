"""
ECS (Entity-Component-System) package for Sands of Duat
"""

from .entity import EntityManager, EntityBuilder, create_player_entity, create_scarab_enemy, create_combat_dummy
from .components import *
from .systems import *

__all__ = [
    'EntityManager',
    'EntityBuilder', 
    'create_player_entity',
    'create_scarab_enemy',
    'create_combat_dummy',
    'System',
    'InputSystem',
    'MovementSystem',
    'AnimationSystem',
    'RenderSystem',
    'CameraSystem',
    'AttackSystem',
    'CollisionSystem',
    'AISystem',
    'HealthSystem',
    'Transform',
    'SpriteRenderer',
    'InputController',
    'Movement',
    'Animation',
    'Health',
    'Combat',
    'PlayerTag',
    'EnemyTag',
    'Camera',
    'Hitbox',
    'AttackHitbox',
    'AIController',
    'Particle',
    'ParticleEmitter'
]