"""
Arena Scene - Combat areas with procedural enemy encounters
Like Hades' various chambers with enemies and rewards
"""

import pygame
import random
import math
from typing import Optional, Dict, Any, List
from .scene import Scene
from ecs import (
    EntityManager, create_player_entity, create_scarab_enemy, create_combat_dummy,
    InputSystem, MovementSystem, AnimationSystem, RenderSystem,
    AttackSystem, CollisionSystem, AISystem, HealthSystem,
    Transform, SpriteRenderer, Health, PlayerTag, EnemyTag
)
from assets import get_sprite


class ArenaScene(Scene):
    """Arena scene - combat encounters with enemies."""
    
    def __init__(self, game):
        super().__init__(game)
        self.player_id: Optional[int] = None
        self.enemies: List[int] = []
        self.exit_portal_id: Optional[int] = None
        self.show_ui = True
        self.arena_cleared = False
        self.wave_count = 1
        self.max_waves = 3
        
        # Arena boundaries
        self.arena_width = 1400
        self.arena_height = 900
        self.center_x = self.arena_width // 2
        self.center_y = self.arena_height // 2
        
        # Arena state
        self.current_wave = 0
        self.wave_timer = 0.0
        self.wave_delay = 2.0  # Seconds between waves
    
    def initialize(self) -> None:
        """Initialize the Arena scene."""
        print("Entering Arena - Chamber of Trials...")
        
        # Setup ECS systems (including combat)
        self.systems = [
            InputSystem(self.entity_manager),
            AISystem(self.entity_manager),
            MovementSystem(self.entity_manager),
            AttackSystem(self.entity_manager),
            CollisionSystem(self.entity_manager),
            HealthSystem(self.entity_manager),
            AnimationSystem(self.entity_manager),
            RenderSystem(self.entity_manager, self.game.screen)
        ]
        
        # Create player
        self.create_player()
        
        # Start first wave
        self.start_wave(1)
        
        print(f"Arena initialized - Wave 1/{self.max_waves}")
    
    def create_player(self) -> None:
        """Create or restore player in arena."""
        # Get player data from hub
        transition_data = self.get_transition_data()
        player_health = transition_data.get('player_health', {'current': 100, 'max': 100})
        
        self.player_id = create_player_entity(
            self.entity_manager,
            x=self.center_x,
            y=self.center_y
        )
        
        # Restore health from hub
        health = self.entity_manager.get_component(self.player_id, Health)
        if health is not None:
            health.current_hp = player_health['current']
            health.max_hp = player_health['max']
        
        # Set player sprite
        player_sprite = self.entity_manager.get_component(self.player_id, SpriteRenderer)
        if player_sprite is not None:
            player_sprite.sprite_sheet = get_sprite("player_anubis")
    
    def start_wave(self, wave_number: int) -> None:
        """Start a new enemy wave."""
        self.current_wave = wave_number
        self.wave_timer = 0.0
        
        # Clear previous enemies
        self.clear_enemies()
        
        # Generate enemies based on wave
        enemy_count = min(2 + wave_number, 6)  # Scale enemy count
        
        print(f"Starting Wave {wave_number} with {enemy_count} enemies")
        
        # Spawn enemies in circle around player
        for i in range(enemy_count):
            angle = (i / enemy_count) * 2 * math.pi
            distance = 250 + random.randint(-50, 50)
            
            enemy_x = self.center_x + math.cos(angle) * distance
            enemy_y = self.center_y + math.sin(angle) * distance
            
            # Keep enemies within arena bounds
            enemy_x = max(50, min(self.arena_width - 50, enemy_x))
            enemy_y = max(50, min(self.arena_height - 50, enemy_y))
            
            enemy_id = create_scarab_enemy(self.entity_manager, enemy_x, enemy_y)
            self.enemies.append(enemy_id)
            
            # Set enemy sprite
            enemy_sprite = self.entity_manager.get_component(enemy_id, SpriteRenderer)
            if enemy_sprite is not None:
                enemy_sprite.sprite_sheet = get_sprite("scarab_enemy")
        
        # Add a combat dummy for testing (first wave only)
        if wave_number == 1:
            dummy_id = create_combat_dummy(
                self.entity_manager,
                x=self.center_x + 150,
                y=self.center_y + 150
            )
            dummy_sprite = self.entity_manager.get_component(dummy_id, SpriteRenderer)
            if dummy_sprite is not None:
                dummy_sprite.sprite_sheet = get_sprite("scarab_enemy")
                dummy_sprite.color_tint = (128, 128, 128)
    
    def clear_enemies(self) -> None:
        """Remove all enemies from the arena."""
        for enemy_id in self.enemies:
            if self.entity_manager.entity_exists(enemy_id):
                self.entity_manager.destroy_entity(enemy_id)
        self.enemies.clear()
    
    def check_wave_completion(self) -> bool:
        """Check if current wave is completed."""
        # Count living enemies
        living_enemies = 0
        for enemy_id in self.enemies[:]:  # Copy list to avoid modification during iteration
            if not self.entity_manager.entity_exists(enemy_id):
                self.enemies.remove(enemy_id)
                continue
            
            health = self.entity_manager.get_component(enemy_id, Health)
            if health is not None and health.current_hp > 0:
                living_enemies += 1
            else:
                # Remove dead enemy
                self.entity_manager.destroy_entity(enemy_id)
                self.enemies.remove(enemy_id)
        
        return living_enemies == 0
    
    def create_exit_portal(self) -> None:
        """Create exit portal when arena is cleared."""
        if self.exit_portal_id is not None:
            return
        
        self.exit_portal_id = (self.entity_manager.create_entity())
        
        # Add portal components
        from ecs.entity import EntityBuilder
        self.exit_portal_id = (EntityBuilder(self.entity_manager)
                              .with_component(Transform(
                                  x=self.center_x,
                                  y=self.center_y - 250
                              ))
                              .with_component(SpriteRenderer(
                                  frame_width=96,
                                  frame_height=96,
                                  frames_per_row=1,
                                  total_frames=1,
                                  color_tint=(0, 255, 0)  # Green exit portal
                              ))
                              .build())
        
        # Set portal sprite
        portal_sprite = self.entity_manager.get_component(self.exit_portal_id, SpriteRenderer)
        if portal_sprite is not None:
            portal_sprite.sprite_sheet = get_sprite("scarab_enemy")
            portal_sprite.color_tint = (0, 255, 0)
    
    def update(self, dt: float) -> Optional[str]:
        """Update arena logic."""
        # Update ECS systems
        for system in self.systems:
            system.update(dt)
        
        # Check player death
        if self.player_id is not None:
            player_health = self.entity_manager.get_component(self.player_id, Health)
            if player_health is not None and player_health.current_hp <= 0:
                print("Player died! Returning to Hub...")
                # Return to hub with reduced health
                self.set_transition_data({
                    'player_health': {'current': 50, 'max': 100},
                    'from_scene': 'arena',
                    'run_failed': True
                })
                return "hub"
        
        # Update wave timer
        self.wave_timer += dt
        
        # Check wave completion
        if not self.arena_cleared and self.check_wave_completion():
            if self.current_wave < self.max_waves:
                # Start next wave after delay
                if self.wave_timer >= self.wave_delay:
                    self.start_wave(self.current_wave + 1)
            else:
                # Arena cleared!
                self.arena_cleared = True
                self.create_exit_portal()
                print("Arena cleared! Exit portal appeared.")
        
        # Check exit portal interaction
        return self.check_exit_interaction()
    
    def check_exit_interaction(self) -> Optional[str]:
        """Check for exit portal interaction."""
        if not self.arena_cleared or self.exit_portal_id is None or self.player_id is None:
            return None
        
        player_transform = self.entity_manager.get_component(self.player_id, Transform)
        portal_transform = self.entity_manager.get_component(self.exit_portal_id, Transform)
        
        if player_transform is None or portal_transform is None:
            return None
        
        distance = math.sqrt(
            (player_transform.x - portal_transform.x) ** 2 +
            (player_transform.y - portal_transform.y) ** 2
        )
        
        # If close to portal and pressing E
        keys = pygame.key.get_pressed()
        if distance < 80 and keys[pygame.K_e]:
            # Return to hub with current health
            player_health = self.entity_manager.get_component(self.player_id, Health)
            health_data = {
                'current': player_health.current_hp if player_health else 100,
                'max': player_health.max_hp if player_health else 100
            }
            
            self.set_transition_data({
                'player_health': health_data,
                'from_scene': 'arena',
                'run_completed': True,
                'waves_cleared': self.max_waves
            })
            
            return "hub"
        
        return None
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the arena scene."""
        # Clear with arena background (darker, more ominous)
        screen.fill((35, 25, 20))  # Dark stone/sand
        
        # Draw arena boundaries
        border_color = (139, 69, 19)  # Brown border
        border_thickness = 5
        pygame.draw.rect(screen, border_color, 
                        (border_thickness, border_thickness, 
                         self.arena_width - 2*border_thickness, 
                         self.arena_height - 2*border_thickness), 
                        border_thickness)
        
        # Render all entities (handled by RenderSystem)
        
        # Draw arena UI
        if self.show_ui:
            self.draw_arena_ui(screen)
    
    def draw_arena_ui(self, screen: pygame.Surface) -> None:
        """Draw Arena-specific UI elements."""
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)
        
        # Title
        title = font.render("Chamber of Trials", True, (255, 69, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 30))
        screen.blit(title, title_rect)
        
        # Wave info
        if not self.arena_cleared:
            wave_text = f"Wave {self.current_wave}/{self.max_waves}"
            wave_color = (255, 215, 0)
            
            # Show enemies remaining
            living_enemies = len([e for e in self.enemies 
                                 if self.entity_manager.entity_exists(e) and
                                 self.entity_manager.get_component(e, Health) and
                                 self.entity_manager.get_component(e, Health).current_hp > 0])
            
            enemy_text = f"Enemies: {living_enemies}"
        else:
            wave_text = "ARENA CLEARED!"
            wave_color = (0, 255, 0)
            enemy_text = "Victory!"
        
        wave_surface = font.render(wave_text, True, wave_color)
        screen.blit(wave_surface, (20, 70))
        
        if not self.arena_cleared:
            enemy_surface = small_font.render(enemy_text, True, (255, 255, 255))
            screen.blit(enemy_surface, (20, 120))
        
        # Player health
        if self.player_id is not None:
            player_health = self.entity_manager.get_component(self.player_id, Health)
            if player_health is not None:
                health_text = f"Health: {player_health.current_hp}/{player_health.max_hp}"
                health_color = (255, 0, 0) if player_health.current_hp < 30 else (0, 255, 0)
                health_surface = small_font.render(health_text, True, health_color)
                screen.blit(health_surface, (screen.get_width() - 250, 20))
                
                # Health bar
                bar_width = 200
                bar_height = 20
                bar_x = screen.get_width() - 250
                bar_y = 55
                
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                
                if player_health.max_hp > 0:
                    fill_width = int((player_health.current_hp / player_health.max_hp) * bar_width)
                    pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))
                
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Exit portal prompt
        if self.arena_cleared and self.exit_portal_id is not None and self.player_id is not None:
            player_transform = self.entity_manager.get_component(self.player_id, Transform)
            portal_transform = self.entity_manager.get_component(self.exit_portal_id, Transform)
            
            if player_transform and portal_transform:
                distance = math.sqrt(
                    (player_transform.x - portal_transform.x) ** 2 +
                    (player_transform.y - portal_transform.y) ** 2
                )
                
                if distance < 80:
                    prompt = font.render("Press E to Return to Hub", True, (255, 255, 255))
                    prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
                    
                    pygame.draw.rect(screen, (0, 0, 0), prompt_rect.inflate(20, 10))
                    pygame.draw.rect(screen, (0, 255, 0), prompt_rect.inflate(20, 10), 3)
                    screen.blit(prompt, prompt_rect)
        
        # Controls
        controls = [
            "WASD: Move",
            "J: Light Attack",
            "K: Heavy Attack", 
            "ESC: Return to Hub"
        ]
        
        y_offset = screen.get_height() - 150
        for control in controls:
            text = small_font.render(control, True, (255, 215, 0))
            screen.blit(text, (20, y_offset))
            y_offset += 25
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle arena-specific events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.show_ui = not self.show_ui
            elif event.key == pygame.K_ESCAPE:
                # Emergency exit to hub
                player_health = None
                if self.player_id is not None:
                    player_health = self.entity_manager.get_component(self.player_id, Health)
                
                health_data = {
                    'current': player_health.current_hp if player_health else 50,
                    'max': player_health.max_hp if player_health else 100
                }
                
                self.set_transition_data({
                    'player_health': health_data,
                    'from_scene': 'arena',
                    'run_abandoned': True
                })
                
                # This will be handled by the scene manager
                print("Emergency exit to Hub (ESC pressed)")