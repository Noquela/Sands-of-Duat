"""
ECS Components for Sands of Duat
Egyptian-themed roguelike components following Hades design patterns
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
import pygame


@dataclass
class Transform:
    """Position, rotation, and scale component."""
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0


@dataclass  
class SpriteRenderer:
    """Sprite rendering component with animation support."""
    sprite_sheet: Optional[pygame.Surface] = None
    frame_width: int = 64
    frame_height: int = 64
    frames_per_row: int = 4
    total_frames: int = 1
    current_frame: int = 0
    visible: bool = True
    flip_x: bool = False
    flip_y: bool = False
    color_tint: Tuple[int, int, int] = (255, 255, 255)
    alpha: int = 255
    
    def get_current_rect(self) -> pygame.Rect:
        """Get the source rectangle for the current frame."""
        if self.sprite_sheet is None:
            return pygame.Rect(0, 0, self.frame_width, self.frame_height)
        
        # Ensure current_frame is within bounds
        safe_frame = max(0, min(self.current_frame, self.total_frames - 1))
        
        row = safe_frame // self.frames_per_row
        col = safe_frame % self.frames_per_row
        
        # Calculate sprite sheet dimensions
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()
        
        # Calculate position and ensure it's within bounds
        x = col * self.frame_width
        y = row * self.frame_height
        
        # Ensure the rect doesn't exceed sprite sheet bounds
        x = min(x, sheet_width - self.frame_width)
        y = min(y, sheet_height - self.frame_height)
        x = max(0, x)
        y = max(0, y)
        
        return pygame.Rect(x, y, self.frame_width, self.frame_height)


@dataclass
class InputController:
    """Input handling component."""
    # Movement inputs (normalized -1 to 1)
    move_x: float = 0.0
    move_y: float = 0.0
    
    # Action inputs (pressed this frame)
    attack_light_pressed: bool = False
    attack_heavy_pressed: bool = False
    interact_pressed: bool = False
    dash_pressed: bool = False
    
    # Key mappings
    move_left_key: int = pygame.K_a
    move_right_key: int = pygame.K_d
    move_up_key: int = pygame.K_w
    move_down_key: int = pygame.K_s
    attack_light_key: int = pygame.K_j
    attack_heavy_key: int = pygame.K_k
    interact_key: int = pygame.K_e
    dash_key: int = pygame.K_SPACE


@dataclass
class Movement:
    """Movement physics component."""
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    max_speed: float = 200.0
    acceleration: float = 800.0
    friction: float = 0.85
    dash_speed: float = 500.0
    dash_duration: float = 0.2
    dash_cooldown: float = 1.0
    dash_timer: float = 0.0
    dash_cooldown_timer: float = 0.0


@dataclass
class Animation:
    """Animation state component."""
    current_animation: str = "idle"
    animation_time: float = 0.0
    playing: bool = True
    
    # Animation definitions with frame sequences
    animations: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "idle": {"frames": [0, 1, 2, 3], "duration": 0.2, "loop": True},
        "walk": {"frames": [0, 1, 2, 3], "duration": 0.15, "loop": True},
        "attack_light": {"frames": [0, 1, 2, 3], "duration": 0.1, "loop": False},
        "attack_heavy": {"frames": [0, 1, 2, 3], "duration": 0.15, "loop": False},
        "death": {"frames": [0, 1, 2, 3], "duration": 0.3, "loop": False}
    })


@dataclass
class Health:
    """Health and damage component."""
    current_hp: float = 100.0
    max_hp: float = 100.0
    invulnerable: bool = False
    invulnerability_timer: float = 0.0
    invulnerability_duration: float = 1.0
    regeneration_rate: float = 0.0
    
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    def heal(self, amount: float) -> None:
        self.current_hp = min(self.current_hp + amount, self.max_hp)
    
    def take_damage(self, amount: float) -> bool:
        if self.invulnerable:
            return False
        self.current_hp = max(0, self.current_hp - amount)
        self.invulnerable = True
        self.invulnerability_timer = self.invulnerability_duration
        return True


@dataclass
class Combat:
    """Combat and attack component."""
    attack_damage: float = 25.0
    attack_range: float = 50.0
    attack_speed: float = 1.0
    attack_cooldown: float = 1.0  # Cooldown duration in seconds
    last_attack_time: float = 0.0
    is_attacking: bool = False
    crit_chance: float = 0.1
    crit_multiplier: float = 2.0
    
    def can_attack(self, current_time: float) -> bool:
        """Check if entity can attack based on cooldown."""
        return current_time - self.last_attack_time >= self.attack_cooldown


@dataclass
class Hitbox:
    """Collision detection component."""
    width: float = 32.0
    height: float = 32.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    active: bool = True  # Whether hitbox is active for collision
    
    def get_rect(self, transform: Transform) -> pygame.Rect:
        return pygame.Rect(
            transform.x - self.width // 2 + self.offset_x,
            transform.y - self.height // 2 + self.offset_y,
            self.width,
            self.height
        )


@dataclass
class AttackHitbox:
    """Attack collision component."""
    width: float = 60.0
    height: float = 40.0
    offset_x: float = 0.0
    offset_y: float = 20.0
    active: bool = False
    duration: float = 0.0  # Current duration
    max_duration: float = 0.2  # How long attack stays active
    damage: float = 25.0
    hit_entities: Set[int] = field(default_factory=set)  # Entities already hit
    
    def get_rect(self, transform: Transform) -> pygame.Rect:
        return pygame.Rect(
            transform.x - self.width // 2 + self.offset_x,
            transform.y - self.height // 2 + self.offset_y,
            self.width,
            self.height
        )


@dataclass
class AIController:
    """AI behavior component."""
    ai_type: str = "basic"
    state: str = "idle"
    target_entity: Optional[int] = None
    detection_range: float = 100.0
    attack_range: float = 40.0
    chase_speed: float = 150.0
    patrol_speed: float = 50.0
    state_timer: float = 0.0
    
    # Last seen position tracking
    last_seen_x: float = 0.0
    last_seen_y: float = 0.0
    
    # Patrol behavior
    patrol_center_x: float = 0.0
    patrol_center_y: float = 0.0
    patrol_radius: float = 50.0
    patrol_angle: float = 0.0


@dataclass
class Artifact:
    """Egyptian artifact/boon component (like Hades divine gifts)."""
    name: str = "Unknown Artifact"
    description: str = "A mysterious artifact of the gods"
    rarity: str = "common"  # common, rare, epic, legendary
    artifact_type: str = "passive"  # passive, active, weapon_mod
    effects: Dict[str, float] = field(default_factory=dict)
    god_source: str = "unknown"  # Ra, Thoth, Isis, Ptah, etc.
    level: int = 1
    max_level: int = 3
    stack_count: int = 1
    
    def get_description_with_effects(self) -> str:
        """Get artifact description with current effect values."""
        desc = self.description
        for effect, value in self.effects.items():
            desc += f"\n{effect.replace('_', ' ').title()}: {value:+.0%}" if abs(value) < 1 else f"\n{effect.replace('_', ' ').title()}: {value:+.0f}"
        return desc


@dataclass
class ArtifactInventory:
    """Inventory for artifacts and boons."""
    equipped_artifacts: List[str] = field(default_factory=list)
    max_artifacts: int = 12
    artifact_effects: Dict[str, float] = field(default_factory=dict)
    
    def add_artifact(self, artifact_name: str) -> bool:
        """Add artifact to inventory."""
        if len(self.equipped_artifacts) < self.max_artifacts:
            self.equipped_artifacts.append(artifact_name)
            return True
        return False
    
    def remove_artifact(self, artifact_name: str) -> bool:
        """Remove artifact from inventory."""
        if artifact_name in self.equipped_artifacts:
            self.equipped_artifacts.remove(artifact_name)
            return True
        return False
    
    def has_artifact(self, artifact_name: str) -> bool:
        """Check if artifact is equipped."""
        return artifact_name in self.equipped_artifacts


@dataclass
class Stats:
    """Character stats modified by artifacts."""
    base_damage: float = 25.0
    base_speed: float = 200.0
    base_health: float = 100.0
    base_crit_chance: float = 0.1
    
    # Multipliers from artifacts
    damage_multiplier: float = 1.0
    speed_multiplier: float = 1.0
    health_multiplier: float = 1.0
    crit_chance_bonus: float = 0.0
    
    def get_total_damage(self) -> float:
        return self.base_damage * self.damage_multiplier
    
    def get_total_speed(self) -> float:
        return self.base_speed * self.speed_multiplier
    
    def get_total_health(self) -> float:
        return self.base_health * self.health_multiplier
    
    def get_total_crit_chance(self) -> float:
        return min(1.0, self.base_crit_chance + self.crit_chance_bonus)


@dataclass
class Interactable:
    """Component for objects that can be interacted with."""
    interaction_type: str = "generic"  # altar, npc, portal, chest
    prompt_text: str = "Press E to interact"
    can_interact: bool = True
    interaction_range: float = 80.0
    god_type: str = ""  # For altars: Ra, Thoth, Isis, Ptah
    
    def is_in_range(self, player_pos: Tuple[float, float], object_pos: Tuple[float, float]) -> bool:
        """Check if player is in interaction range."""
        distance = ((player_pos[0] - object_pos[0]) ** 2 + (player_pos[1] - object_pos[1]) ** 2) ** 0.5
        return distance <= self.interaction_range


@dataclass
class Portal:
    """Portal component for scene transitions."""
    destination_scene: str = "arena"
    portal_type: str = "arena"  # arena, exit, secret
    unlock_condition: str = ""  # Empty means always unlocked
    energy_color: Tuple[int, int, int] = (138, 43, 226)  # Purple
    

@dataclass
class EgyptianGod:
    """Component for Egyptian god NPCs and altars."""
    god_name: str = "Ra"
    domain: str = "Sun"
    color_scheme: Tuple[int, int, int] = (255, 215, 0)  # Gold
    artifact_pool: List[str] = field(default_factory=list)
    blessing_count: int = 0
    favor_level: int = 1
    
    # God-specific artifact pools
    god_artifacts: Dict[str, List[str]] = field(default_factory=lambda: {
        "Ra": ["Solar Blessing", "Pharaoh's Crown", "Desert Storm"],
        "Thoth": ["Wisdom of Ages", "Scribe's Quill", "Knowledge Keeper"],
        "Isis": ["Mother's Protection", "Magic Ward", "Healing Touch"],
        "Ptah": ["Creator's Hammer", "Divine Craft", "Builder's Strength"]
    })


# Tag components for entity identification
@dataclass
class PlayerTag:
    """Tag for player entity."""
    pass


@dataclass
class EnemyTag:
    """Tag for enemy entities."""
    enemy_type: str = "basic"
    aggro_range: float = 120.0
    reward_experience: int = 10
    
    
@dataclass
class NPCTag:
    """Tag for NPC entities."""
    npc_type: str = "merchant"
    dialogue_key: str = ""


@dataclass
class AltarTag:
    """Tag for altar entities."""
    god_type: str = "Ra"
    offering_cost: int = 0
    blessing_tier: int = 1


@dataclass
class ProjectileTag:
    """Tag for projectile entities."""
    damage: float = 10.0
    speed: float = 300.0
    lifetime: float = 2.0
    piercing: bool = False