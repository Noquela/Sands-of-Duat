"""
Entity management for Sands of Duat ECS
Handles entity creation, destruction, and component management
"""

from typing import Dict, List, Set, Type, TypeVar, Optional, Any
from dataclasses import is_dataclass
import itertools


T = TypeVar('T')


class EntityManager:
    """Manages all entities and their components."""
    
    def __init__(self):
        self._next_entity_id = 1
        self._entities: Set[int] = set()
        self._components: Dict[Type, Dict[int, Any]] = {}
        self._component_entities: Dict[Type, Set[int]] = {}
    
    def create_entity(self) -> int:
        """Create a new entity and return its ID."""
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self._entities.add(entity_id)
        return entity_id
    
    def destroy_entity(self, entity_id: int) -> None:
        """Destroy an entity and remove all its components."""
        if entity_id not in self._entities:
            return
        
        # Remove from all component mappings
        for component_type in list(self._component_entities.keys()):
            if entity_id in self._component_entities[component_type]:
                self.remove_component(entity_id, component_type)
        
        self._entities.remove(entity_id)
    
    def entity_exists(self, entity_id: int) -> bool:
        """Check if an entity exists."""
        return entity_id in self._entities
    
    def add_component(self, entity_id: int, component: Any) -> None:
        """Add a component to an entity."""
        if entity_id not in self._entities:
            raise ValueError(f"Entity {entity_id} does not exist")
        
        if not is_dataclass(component):
            raise TypeError(f"Component {type(component)} must be a dataclass")
        
        component_type = type(component)
        
        # Initialize component storage if needed
        if component_type not in self._components:
            self._components[component_type] = {}
            self._component_entities[component_type] = set()
        
        # Add component
        self._components[component_type][entity_id] = component
        self._component_entities[component_type].add(entity_id)
    
    def remove_component(self, entity_id: int, component_type: Type[T]) -> None:
        """Remove a component from an entity."""
        if component_type in self._components and entity_id in self._components[component_type]:
            del self._components[component_type][entity_id]
            self._component_entities[component_type].discard(entity_id)
    
    def get_component(self, entity_id: int, component_type: Type[T]) -> Optional[T]:
        """Get a component from an entity."""
        if component_type in self._components:
            return self._components[component_type].get(entity_id)
        return None
    
    def has_component(self, entity_id: int, component_type: Type[T]) -> bool:
        """Check if an entity has a specific component."""
        return (component_type in self._components and 
                entity_id in self._components[component_type])
    
    def get_entities_with_component(self, component_type: Type[T]) -> Set[int]:
        """Get all entities that have a specific component."""
        return self._component_entities.get(component_type, set()).copy()
    
    def get_entities_with_components(self, *component_types: Type) -> Set[int]:
        """Get all entities that have ALL of the specified components."""
        if not component_types:
            return set()
        
        entity_sets = []
        for component_type in component_types:
            entities = self._component_entities.get(component_type, set())
            if not entities:  # If any component type has no entities, return empty set
                return set()
            entity_sets.append(entities)
        
        # Return intersection of all sets
        result = entity_sets[0]
        for entity_set in entity_sets[1:]:
            result = result.intersection(entity_set)
        
        return result
    
    def get_all_entities(self) -> Set[int]:
        """Get all active entities."""
        return self._entities.copy()
    
    def get_entity_count(self) -> int:
        """Get the total number of active entities."""
        return len(self._entities)
    
    def get_component_count(self, component_type: Type[T]) -> int:
        """Get the number of entities with a specific component."""
        return len(self._component_entities.get(component_type, set()))
    
    def clear_all(self) -> None:
        """Clear all entities and components."""
        self._entities.clear()
        self._components.clear()
        self._component_entities.clear()
        self._next_entity_id = 1


class EntityBuilder:
    """Helper class for fluently building entities with components."""
    
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager
        self.entity_id = entity_manager.create_entity()
    
    def with_component(self, component: Any) -> 'EntityBuilder':
        """Add a component to the entity being built."""
        self.entity_manager.add_component(self.entity_id, component)
        return self
    
    def build(self) -> int:
        """Finish building and return the entity ID."""
        return self.entity_id


def create_player_entity(entity_manager: EntityManager, x: float = 0.0, y: float = 0.0) -> int:
    """Create a player entity with standard components."""
    from .components import (Transform, SpriteRenderer, InputController, 
                           Movement, Animation, Health, Combat, PlayerTag,
                           Hitbox, AttackHitbox, ArtifactInventory, Stats)
    
    return (EntityBuilder(entity_manager)
            .with_component(Transform(x=x, y=y))
            .with_component(SpriteRenderer(
                frame_width=64, 
                frame_height=64, 
                frames_per_row=4, 
                total_frames=16
            ))
            .with_component(InputController())
            .with_component(Movement(max_speed=250.0))
            .with_component(Animation())
            .with_component(Health(current_hp=100, max_hp=100))
            .with_component(Combat(attack_damage=30, attack_range=60.0))
            .with_component(Hitbox(width=40.0, height=40.0))
            .with_component(AttackHitbox(width=80.0, height=60.0, offset_y=30.0))
            .with_component(ArtifactInventory(max_artifacts=10))
            .with_component(Stats(base_damage=30.0, base_speed=250.0, base_health=100.0))
            .with_component(PlayerTag())
            .build())


def create_scarab_enemy(entity_manager: EntityManager, x: float = 0.0, y: float = 0.0) -> int:
    """Create a scarab enemy entity."""
    from .components import (Transform, SpriteRenderer, Movement, Animation, 
                           Health, Combat, EnemyTag, Hitbox, AIController)
    
    return (EntityBuilder(entity_manager)
            .with_component(Transform(x=x, y=y))
            .with_component(SpriteRenderer(
                frame_width=48, 
                frame_height=48, 
                frames_per_row=4, 
                total_frames=8
            ))
            .with_component(Movement(max_speed=120.0))
            .with_component(Animation())
            .with_component(Health(current_hp=50, max_hp=50))
            .with_component(Combat(attack_damage=15, attack_range=30.0))
            .with_component(Hitbox(width=30.0, height=30.0))
            .with_component(AIController(
                ai_type="scarab",
                detection_range=150.0,
                attack_range=35.0,
                chase_speed=140.0,
                patrol_speed=60.0
            ))
            .with_component(EnemyTag(enemy_type="scarab", aggro_range=150.0))
            .build())


def create_combat_dummy(entity_manager: EntityManager, x: float = 0.0, y: float = 0.0) -> int:
    """Create a combat dummy for testing."""
    from .components import (Transform, SpriteRenderer, Health, Hitbox)
    
    return (EntityBuilder(entity_manager)
            .with_component(Transform(x=x, y=y))
            .with_component(SpriteRenderer(
                frame_width=48, 
                frame_height=64, 
                frames_per_row=1, 
                total_frames=1
            ))
            .with_component(Health(current_hp=9999, max_hp=9999))
            .with_component(Hitbox(width=40.0, height=60.0))
            .build())