"""
ECS (Entity-Component-System) package for Sands of Duat
"""

from .entity import (EntityManager, EntityBuilder, create_player_entity, create_scarab_enemy, 
                     create_combat_dummy, create_egyptian_altar, create_egyptian_npc, create_arena_portal)
from .components import *
from .systems import *

__all__ = [
    'EntityManager',
    'EntityBuilder', 
    'create_player_entity',
    'create_scarab_enemy',
    'create_combat_dummy',
    'create_egyptian_altar',
    'create_egyptian_npc', 
    'create_arena_portal',
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
    'ArtifactSystem',
    'InteractionSystem',
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
    'Artifact',
    'ArtifactInventory',
    'Stats',
    'Interactable',
    'Portal',
    'EgyptianGod',
    'NPCTag',
    'AltarTag',
    'Particle',
    'ParticleEmitter'
]