#!/usr/bin/env python3
"""
Sands of Duat - Main game entry point
Egyptian mythology roguelike inspired by Hades
"""

import pygame
import sys
from typing import Optional, List

# Import ECS components
from ecs import (
    EntityManager, create_player_entity, create_scarab_enemy, create_combat_dummy,
    InputSystem, MovementSystem, AnimationSystem, RenderSystem,
    AttackSystem, CollisionSystem, AISystem, HealthSystem,
    Transform, SpriteRenderer, Health
)
from assets import load_assets, get_sprite


class Game:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 60
        self.clock: Optional[pygame.time.Clock] = None
        self.screen: Optional[pygame.Surface] = None
        self.running = False
        
        # ECS
        self.entity_manager = EntityManager()
        self.systems: List = []
        self.player_id: Optional[int] = None
        self.enemies: List[int] = []
        self.dummy_id: Optional[int] = None

    def initialize(self) -> bool:
        """Initialize pygame and create game window."""
        try:
            pygame.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Sands of Duat")
            self.clock = pygame.time.Clock()
            self.running = True
            
            # Load assets
            load_assets()
            
            # Initialize ECS systems
            self.setup_ecs()
            
            # Create entities
            self.create_player()
            self.create_test_enemies()
            
            print(f"Game initialized: {self.screen_width}x{self.screen_height} @ {self.fps}fps")
            print(f"Player entity created: {self.player_id}")
            print(f"Test entities created: {len(self.enemies)} enemies, 1 dummy")
            return True
        except pygame.error as e:
            print(f"Failed to initialize pygame: {e}")
            return False

    def setup_ecs(self) -> None:
        """Initialize ECS systems."""
        self.systems = [
            InputSystem(self.entity_manager),
            AISystem(self.entity_manager),
            MovementSystem(self.entity_manager),
            AttackSystem(self.entity_manager),
            CollisionSystem(self.entity_manager),
            HealthSystem(self.entity_manager),
            AnimationSystem(self.entity_manager),
            RenderSystem(self.entity_manager, self.screen)
        ]
        print(f"Initialized {len(self.systems)} ECS systems")

    def create_player(self) -> None:
        """Create the player entity."""
        # Create player at center of screen
        self.player_id = create_player_entity(
            self.entity_manager, 
            x=self.screen_width // 2, 
            y=self.screen_height // 2
        )
        
        # Set player sprite
        player_sprite = self.entity_manager.get_component(self.player_id, SpriteRenderer)
        if player_sprite is not None:
            player_sprite.sprite_sheet = get_sprite("player_anubis")
            print("Player sprite loaded")

    def create_test_enemies(self) -> None:
        """Create test enemies and combat dummy."""
        # Create combat dummy for testing attacks
        self.dummy_id = create_combat_dummy(
            self.entity_manager,
            x=self.screen_width // 2 + 200,
            y=self.screen_height // 2
        )
        
        # Set dummy sprite
        dummy_sprite = self.entity_manager.get_component(self.dummy_id, SpriteRenderer)
        if dummy_sprite is not None:
            dummy_sprite.sprite_sheet = get_sprite("scarab_enemy")  # Reuse for now
            dummy_sprite.color_tint = (128, 128, 128)  # Gray tint for dummy
        
        # Create a few scarab enemies
        enemy_positions = [
            (self.screen_width // 2 - 300, self.screen_height // 2 - 200),
            (self.screen_width // 2 + 300, self.screen_height // 2 + 200),
            (self.screen_width // 2, self.screen_height // 2 - 300)
        ]
        
        for x, y in enemy_positions:
            enemy_id = create_scarab_enemy(self.entity_manager, x, y)
            self.enemies.append(enemy_id)
            
            # Set enemy sprite
            enemy_sprite = self.entity_manager.get_component(enemy_id, SpriteRenderer)
            if enemy_sprite is not None:
                enemy_sprite.sprite_sheet = get_sprite("scarab_enemy")
        
        print(f"Created {len(self.enemies)} scarab enemies and 1 combat dummy")

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt: float) -> None:
        """Update game logic."""
        # Update all ECS systems
        for system in self.systems:
            system.update(dt)

    def render(self) -> None:
        """Render game frame."""
        if self.screen is None:
            return
        
        # Clear screen with dark sand color
        self.screen.fill((42, 35, 28))
        
        # Render systems handle drawing
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()

    def draw_ui(self) -> None:
        """Draw UI elements."""
        if self.screen is None:
            return
        
        # Draw FPS
        fps = self.clock.get_fps()
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 215, 0))
        self.screen.blit(fps_text, (10, 10))
        
        # Draw player health
        if self.player_id is not None:
            player_health = self.entity_manager.get_component(self.player_id, Health)
            if player_health is not None:
                health_text = f"Health: {player_health.current_hp}/{player_health.max_hp}"
                health_surface = font.render(health_text, True, (255, 0, 0) if player_health.current_hp < 30 else (255, 215, 0))
                self.screen.blit(health_surface, (10, 50))
                
                # Health bar
                bar_width = 200
                bar_height = 20
                bar_x = 10
                bar_y = 85
                
                # Background
                pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                
                # Health fill
                if player_health.max_hp > 0:
                    fill_width = int((player_health.current_hp / player_health.max_hp) * bar_width)
                    health_color = (255, 0, 0) if player_health.current_hp < 30 else (0, 255, 0)
                    pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, fill_width, bar_height))
                
                # Border
                pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw controls
        controls = [
            "WASD: Move",
            "J: Light Attack", 
            "K: Heavy Attack",
            "SPACE: Dash",
            "ESC: Quit"
        ]
        
        y_offset = 120
        for control in controls:
            text = font.render(control, True, (255, 215, 0))
            self.screen.blit(text, (10, y_offset))
            y_offset += 30

    def run(self) -> None:
        """Main game loop."""
        if not self.initialize():
            return

        print("Starting Sands of Duat...")
        print("Controls: WASD to move, J/K to attack, SPACE to dash, ESC to quit")
        
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources."""
        pygame.quit()
        print("Game shutdown complete")


def main() -> int:
    """Main entry point."""
    game = Game()
    try:
        game.run()
        return 0
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        return 1
    except Exception as e:
        print(f"Game crashed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())