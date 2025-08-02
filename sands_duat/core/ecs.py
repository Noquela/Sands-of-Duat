"""
Entity Component System (ECS)

Flexible architecture for managing game objects, their properties,
and behaviors in a decoupled, data-driven manner.

Key Features:
- Entity: Unique identifiers for game objects
- Component: Data containers for entity properties
- System: Logic processors that operate on entities with specific components
- World: Container and manager for all entities, components, and systems

Classes:
- Entity: Game object identifier
- Component: Base class for data components
- System: Base class for logic systems
- World: ECS container and coordinator
"""

import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Type, TypeVar, Generic, Optional, Any
from collections import defaultdict
from pydantic import BaseModel, Field


EntityID = str
ComponentType = TypeVar('ComponentType', bound='Component')


class Entity:
    """
    Represents a unique game object identifier.
    
    Entities are lightweight identifiers that can have
    components attached to define their properties and behavior.
    """
    
    def __init__(self, entity_id: Optional[str] = None):
        self.id: EntityID = entity_id or str(uuid.uuid4())
    
    def __str__(self) -> str:
        return f"Entity({self.id})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Entity):
            return self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash(self.id)


class Component(BaseModel, ABC):
    """
    Base class for all components.
    
    Components are pure data containers that define properties
    of entities. They should not contain game logic.
    """
    
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_type_name(cls) -> str:
        """Get the component type name."""
        return cls.__name__


class System(ABC):
    """
    Base class for all systems.
    
    Systems contain the game logic and operate on entities
    that have specific component combinations.
    """
    
    def __init__(self, world: 'World'):
        self.world = world
        self.enabled = True
    
    @abstractmethod
    def get_required_components(self) -> List[Type[Component]]:
        """Return list of component types this system requires."""
        pass
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the system logic."""
        pass
    
    def get_entities(self) -> List[Entity]:
        """Get all entities that have the required components."""
        return self.world.get_entities_with_components(self.get_required_components())
    
    def enable(self) -> None:
        """Enable this system."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable this system."""
        self.enabled = False


class World:
    """
    ECS World that manages entities, components, and systems.
    
    The World is the central coordinator that maintains all
    game objects and their relationships.
    """
    
    def __init__(self):
        self.entities: Set[Entity] = set()
        self.components: Dict[EntityID, Dict[Type[Component], Component]] = defaultdict(dict)
        self.systems: List[System] = []
        self.component_entities: Dict[Type[Component], Set[EntityID]] = defaultdict(set)
    
    def create_entity(self, entity_id: Optional[str] = None) -> Entity:
        """Create a new entity."""
        entity = Entity(entity_id)
        self.entities.add(entity)
        return entity
    
    def destroy_entity(self, entity: Entity) -> None:
        """Remove an entity and all its components."""
        if entity not in self.entities:
            return
        
        # Remove all components
        for component_type in list(self.components[entity.id].keys()):
            self.remove_component(entity, component_type)
        
        # Remove entity
        self.entities.discard(entity)
        if entity.id in self.components:
            del self.components[entity.id]
    
    def add_component(self, entity: Entity, component: Component) -> None:
        """Add a component to an entity."""
        if entity not in self.entities:
            raise ValueError(f"Entity {entity} not found in world")
        
        component_type = type(component)
        self.components[entity.id][component_type] = component
        self.component_entities[component_type].add(entity.id)
    
    def remove_component(self, entity: Entity, component_type: Type[Component]) -> None:
        """Remove a component from an entity."""
        if entity.id in self.components and component_type in self.components[entity.id]:
            del self.components[entity.id][component_type]
            self.component_entities[component_type].discard(entity.id)
    
    def get_component(self, entity: Entity, component_type: Type[ComponentType]) -> Optional[ComponentType]:
        """Get a specific component from an entity."""
        if entity.id in self.components:
            return self.components[entity.id].get(component_type)
        return None
    
    def has_component(self, entity: Entity, component_type: Type[Component]) -> bool:
        """Check if an entity has a specific component."""
        return (entity.id in self.components and 
                component_type in self.components[entity.id])
    
    def has_components(self, entity: Entity, component_types: List[Type[Component]]) -> bool:
        """Check if an entity has all specified components."""
        return all(self.has_component(entity, comp_type) for comp_type in component_types)
    
    def get_entities_with_component(self, component_type: Type[Component]) -> List[Entity]:
        """Get all entities that have a specific component."""
        entity_ids = self.component_entities[component_type]
        return [entity for entity in self.entities if entity.id in entity_ids]
    
    def get_entities_with_components(self, component_types: List[Type[Component]]) -> List[Entity]:
        """Get all entities that have all specified components."""
        if not component_types:
            return list(self.entities)
        
        # Start with entities that have the first component type
        result_ids = self.component_entities[component_types[0]].copy()
        
        # Intersect with entities that have each additional component type
        for component_type in component_types[1:]:
            result_ids &= self.component_entities[component_type]
        
        return [entity for entity in self.entities if entity.id in result_ids]
    
    def add_system(self, system: System) -> None:
        """Add a system to the world."""
        self.systems.append(system)
    
    def remove_system(self, system: System) -> None:
        """Remove a system from the world."""
        if system in self.systems:
            self.systems.remove(system)
    
    def update(self, delta_time: float) -> None:
        """Update all enabled systems."""
        for system in self.systems:
            if system.enabled:
                system.update(delta_time)
    
    def get_entity_count(self) -> int:
        """Get the total number of entities."""
        return len(self.entities)
    
    def get_component_count(self, component_type: Type[Component]) -> int:
        """Get the number of entities with a specific component."""
        return len(self.component_entities[component_type])
    
    def clear(self) -> None:
        """Clear all entities, components, and systems."""
        self.entities.clear()
        self.components.clear()
        self.systems.clear()
        self.component_entities.clear()


# Common component examples for the game
class PositionComponent(Component):
    """Component for entity position."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class HealthComponent(Component):
    """Component for entity health."""
    current: int = 100
    maximum: int = 100
    
    def is_alive(self) -> bool:
        return self.current > 0
    
    def take_damage(self, amount: int) -> int:
        """Take damage and return actual damage dealt."""
        old_health = self.current
        self.current = max(0, self.current - amount)
        return old_health - self.current
    
    def heal(self, amount: int) -> int:
        """Heal and return actual healing done."""
        old_health = self.current
        self.current = min(self.maximum, self.current + amount)
        return self.current - old_health


class HourGlassComponent(Component):
    """Component for Hour-Glass sand management."""
    current_sand: int = 0
    max_sand: int = 6
    regeneration_rate: float = 1.0
    last_update: float = 0.0


class CardHolderComponent(Component):
    """Component for entities that can hold cards."""
    hand: List[str] = Field(default_factory=list)  # Card IDs
    deck: List[str] = Field(default_factory=list)  # Card IDs
    discard: List[str] = Field(default_factory=list)  # Card IDs
    max_hand_size: int = 7