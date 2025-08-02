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
    EntityManager, create_player_entity, create_scarab_enemy,
    InputSystem, MovementSystem, AnimationSystem, RenderSystem,
    Transform, SpriteRenderer
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
            
            # Create player
            self.create_player()
            
            print(f"Game initialized: {self.screen_width}x{self.screen_height} @ {self.fps}fps")
            print(f"Player entity created: {self.player_id}")
            return True
        except pygame.error as e:
            print(f"Failed to initialize pygame: {e}")
            return False

    def setup_ecs(self) -> None:
        """Initialize ECS systems."""
        self.systems = [
            InputSystem(self.entity_manager),
            MovementSystem(self.entity_manager),
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
        
        # Draw controls
        controls = [
            "WASD: Move",
            "J: Light Attack", 
            "K: Heavy Attack",
            "SPACE: Dash",
            "ESC: Quit"
        ]
        
        y_offset = 50
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