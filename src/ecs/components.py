"""
ECS Components for Sands of Duat
All game components using dataclass pattern for performance and clarity
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple, Set, List
import pygame


@dataclass
class Transform:
    """Position, rotation, and scale component."""
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    
    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    @position.setter
    def position(self, pos: Tuple[float, float]) -> None:
        self.x, self.y = pos


@dataclass
class SpriteRenderer:
    """Sprite rendering component with animation support."""
    sprite_sheet: Optional[pygame.Surface] = None
    current_frame: int = 0
    frame_width: int = 64
    frame_height: int = 64
    frames_per_row: int = 4
    total_frames: int = 1
    visible: bool = True
    flip_x: bool = False
    flip_y: bool = False
    color_tint: Tuple[int, int, int] = (255, 255, 255)
    alpha: int = 255
    
    def get_current_rect(self) -> pygame.Rect:
        """Get the source rectangle for the current frame."""
        if self.sprite_sheet is None:
            return pygame.Rect(0, 0, self.frame_width, self.frame_height)
        
        row = self.current_frame // self.frames_per_row
        col = self.current_frame % self.frames_per_row
        
        return pygame.Rect(
            col * self.frame_width,
            row * self.frame_height,
            self.frame_width,
            self.frame_height
        )


@dataclass
class InputController:
    """Input handling component for player characters."""
    move_up_key: int = pygame.K_w
    move_down_key: int = pygame.K_s
    move_left_key: int = pygame.K_a
    move_right_key: int = pygame.K_d
    attack_light_key: int = pygame.K_j
    attack_heavy_key: int = pygame.K_k
    dash_key: int = pygame.K_SPACE
    interact_key: int = pygame.K_e
    
    # Input state
    move_x: float = 0.0
    move_y: float = 0.0
    attack_light_pressed: bool = False
    attack_heavy_pressed: bool = False
    dash_pressed: bool = False
    interact_pressed: bool = False


@dataclass
class Movement:
    """Movement physics component."""
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    max_speed: float = 200.0  # pixels per second
    acceleration: float = 800.0
    friction: float = 600.0
    
    @property
    def velocity(self) -> Tuple[float, float]:
        return (self.velocity_x, self.velocity_y)
    
    @velocity.setter
    def velocity(self, vel: Tuple[float, float]) -> None:
        self.velocity_x, self.velocity_y = vel


@dataclass
class Animation:
    """Animation state component."""
    current_animation: str = "idle"
    animation_time: float = 0.0
    frame_duration: float = 0.1  # seconds per frame
    loop: bool = True
    playing: bool = True
    
    # Animation definitions
    animations: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.animations is None:
            self.animations = {
                "idle": {"frames": [0, 1, 2, 3], "duration": 0.2, "loop": True},
                "walk": {"frames": [4, 5, 6, 7], "duration": 0.15, "loop": True},
                "attack_light": {"frames": [8, 9, 10, 11], "duration": 0.1, "loop": False},
                "attack_heavy": {"frames": [12, 13, 14, 15], "duration": 0.12, "loop": False}
            }


@dataclass
class Health:
    """Health and damage component."""
    current_hp: int = 100
    max_hp: int = 100
    invulnerable: bool = False
    invulnerability_time: float = 0.0
    
    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    @property
    def health_percentage(self) -> float:
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0


@dataclass
class Combat:
    """Combat stats and state component."""
    attack_damage: int = 25
    attack_range: float = 50.0
    attack_cooldown: float = 0.5
    last_attack_time: float = 0.0
    is_attacking: bool = False
    
    def can_attack(self, current_time: float) -> bool:
        return current_time - self.last_attack_time >= self.attack_cooldown


@dataclass
class PlayerTag:
    """Marker component for player entities."""
    player_id: int = 0


@dataclass
class EnemyTag:
    """Marker component for enemy entities."""
    enemy_type: str = "scarab"
    aggro_range: float = 150.0
    patrol_radius: float = 100.0


@dataclass
class Camera:
    """Camera component for viewport management."""
    target_x: float = 0.0
    target_y: float = 0.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    follow_speed: float = 5.0
    bounds_left: Optional[float] = None
    bounds_right: Optional[float] = None
    bounds_top: Optional[float] = None
    bounds_bottom: Optional[float] = None


@dataclass
class Hitbox:
    """Collision hitbox component."""
    width: float = 32.0
    height: float = 32.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    active: bool = True
    
    def get_rect(self, transform: Transform) -> pygame.Rect:
        """Get the hitbox rectangle in world coordinates."""
        return pygame.Rect(
            transform.x + self.offset_x - self.width // 2,
            transform.y + self.offset_y - self.height // 2,
            self.width,
            self.height
        )


@dataclass
class AttackHitbox:
    """Attack hitbox component for dealing damage."""
    width: float = 60.0
    height: float = 60.0
    offset_x: float = 0.0
    offset_y: float = 30.0  # In front of character
    damage: int = 25
    active: bool = False
    duration: float = 0.0
    max_duration: float = 0.2
    hit_entities: Set[int] = None
    
    def __post_init__(self):
        if self.hit_entities is None:
            self.hit_entities = set()
    
    def get_rect(self, transform: Transform) -> pygame.Rect:
        """Get the attack hitbox rectangle in world coordinates."""
        return pygame.Rect(
            transform.x + self.offset_x - self.width // 2,
            transform.y + self.offset_y - self.height // 2,
            self.width,
            self.height
        )


@dataclass
class AIController:
    """AI controller component for enemies."""
    ai_type: str = "scarab"
    state: str = "idle"  # idle, patrol, chase, attack, dead
    target_entity: Optional[int] = None
    last_seen_x: float = 0.0
    last_seen_y: float = 0.0
    state_timer: float = 0.0
    patrol_center_x: float = 0.0
    patrol_center_y: float = 0.0
    patrol_angle: float = 0.0
    detection_range: float = 150.0
    attack_range: float = 40.0
    patrol_radius: float = 80.0
    chase_speed: float = 120.0
    patrol_speed: float = 60.0


@dataclass
class Particle:
    """Single particle component."""
    lifetime: float = 1.0
    max_lifetime: float = 1.0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    size: float = 4.0
    color: Tuple[int, int, int] = (255, 255, 255)
    alpha: float = 255.0
    gravity: float = 0.0
    fade_rate: float = 255.0


@dataclass
class ParticleEmitter:
    """Particle emitter component."""
    active: bool = True
    particles_per_second: float = 10.0
    spawn_timer: float = 0.0
    particle_lifetime: float = 1.0
    particle_speed_min: float = 50.0
    particle_speed_max: float = 100.0
    particle_size_min: float = 2.0
    particle_size_max: float = 6.0
    particle_color: Tuple[int, int, int] = (255, 255, 255)
    spread_angle: float = 45.0  # degrees
    direction: float = 0.0  # degrees
    burst_count: int = 0  # 0 = continuous, >0 = burst mode


@dataclass
class Artifact:
    """Artifact/item component for boons and upgrades."""
    name: str = "Unknown Artifact"
    description: str = "A mysterious artifact"
    rarity: str = "common"  # common, rare, epic, legendary
    artifact_type: str = "passive"  # passive, active, weapon_mod
    effects: Dict[str, float] = None
    active_cooldown: float = 0.0
    max_cooldown: float = 5.0
    stack_count: int = 1
    max_stacks: int = 1
    god_source: str = "unknown"  # Ra, Thoth, Isis, Ptah, etc.
    
    def __post_init__(self):
        if self.effects is None:
            self.effects = {}


@dataclass 
class ArtifactInventory:
    """Player's artifact collection component."""
    artifacts: List[str] = None  # List of artifact names
    max_artifacts: int = 10
    equipped_artifacts: Dict[str, int] = None  # artifact_name -> stack_count
    
    def __post_init__(self):
        if self.artifacts is None:
            self.artifacts = []
        if self.equipped_artifacts is None:
            self.equipped_artifacts = {}
    
    def add_artifact(self, artifact_name: str) -> bool:
        """Add artifact to inventory."""
        if len(self.artifacts) >= self.max_artifacts:
            return False
        
        if artifact_name in self.equipped_artifacts:
            # Stack if possible
            self.equipped_artifacts[artifact_name] += 1
        else:
            self.equipped_artifacts[artifact_name] = 1
            
        if artifact_name not in self.artifacts:
            self.artifacts.append(artifact_name)
        
        return True
    
    def remove_artifact(self, artifact_name: str) -> bool:
        """Remove artifact from inventory."""
        if artifact_name not in self.equipped_artifacts:
            return False
        
        self.equipped_artifacts[artifact_name] -= 1
        if self.equipped_artifacts[artifact_name] <= 0:
            del self.equipped_artifacts[artifact_name]
            if artifact_name in self.artifacts:
                self.artifacts.remove(artifact_name)
        
        return True


@dataclass
class Stats:
    """Entity stats component affected by artifacts."""
    base_damage: float = 25.0
    damage_multiplier: float = 1.0
    base_speed: float = 250.0
    speed_multiplier: float = 1.0
    base_health: float = 100.0
    health_multiplier: float = 1.0
    attack_speed_multiplier: float = 1.0
    critical_chance: float = 0.0
    critical_damage: float = 1.5
    
    # Resistances
    fire_resistance: float = 0.0
    ice_resistance: float = 0.0
    poison_resistance: float = 0.0
    
    # Special effects
    life_steal: float = 0.0
    thorns_damage: float = 0.0
    dodge_chance: float = 0.0
    
    def get_total_damage(self) -> float:
        """Calculate total damage including modifiers."""
        return self.base_damage * self.damage_multiplier
    
    def get_total_speed(self) -> float:
        """Calculate total movement speed."""
        return self.base_speed * self.speed_multiplier
    
    def get_total_health(self) -> float:
        """Calculate total health.""" 
        return self.base_health * self.health_multiplier


@dataclass
class Interactable:
    """Component for objects player can interact with."""
    interaction_type: str = "examine"  # examine, altar, npc, portal
    interaction_range: float = 80.0
    prompt_text: str = "Press E to interact"
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}