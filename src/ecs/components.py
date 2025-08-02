"""
ECS Components for Sands of Duat
All game components using dataclass pattern for performance and clarity
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple
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