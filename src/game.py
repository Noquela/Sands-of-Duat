#!/usr/bin/env python3
"""
Sands of Duat - Main game entry point
Egyptian mythology roguelike inspired by Hades
"""

import pygame
import sys
from typing import Optional, List

# Import scenes and ECS
from scenes import SceneManager, HubScene, ArenaScene
from assets import load_assets


class Game:
    def __init__(self):
        # Support both ultrawide and standard resolutions as per CLAUDE.md
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 60
        self.clock: Optional[pygame.time.Clock] = None
        self.screen: Optional[pygame.Surface] = None
        self.running = False
        
        # Scene management (Hades-style)
        self.scene_manager: Optional[SceneManager] = None

    def initialize(self) -> bool:
        """Initialize pygame and create game window."""
        try:
            pygame.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Sands of Duat - Egyptian Roguelike")
            self.clock = pygame.time.Clock()
            self.running = True
            
            # Load assets
            load_assets()
            
            # Initialize scene system (Hades-style Hub/Arena)
            self.setup_scenes()
            
            print(f"Game initialized: {self.screen_width}x{self.screen_height} @ {self.fps}fps")
            print("Starting in Hub (Hall of Anubis)...")
            return True
        except pygame.error as e:
            print(f"Failed to initialize pygame: {e}")
            return False

    def setup_scenes(self) -> None:
        """Initialize scene system with Hub and Arena."""
        self.scene_manager = SceneManager(self)
        
        # Register scenes
        hub_scene = HubScene(self)
        arena_scene = ArenaScene(self)
        
        self.scene_manager.register_scene("hub", hub_scene)
        self.scene_manager.register_scene("arena", arena_scene)
        
        # Start in Hub (like Hades starts in Hall of Styx)
        self.scene_manager.transition_to("hub")
        
        print("Scene system initialized: Hub and Arena ready")

    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Let scenes handle ESC first, then quit if needed
                    if self.scene_manager and self.scene_manager.get_current_scene_name() == "arena":
                        # In arena, ESC returns to hub (handled by arena scene)
                        pass
                    else:
                        # In hub or no scene, quit game
                        self.running = False
            
            # Forward event to current scene
            if self.scene_manager:
                self.scene_manager.handle_event(event)

    def update(self, dt: float) -> None:
        """Update game logic."""
        if self.scene_manager:
            self.scene_manager.update(dt)

    def render(self) -> None:
        """Render game frame."""
        if self.screen is None:
            return
        
        # Clear screen
        self.screen.fill((42, 35, 28))
        
        # Render current scene
        if self.scene_manager:
            self.scene_manager.render(self.screen)
        
        # Draw global UI
        self.draw_global_ui()
        
        pygame.display.flip()

    def draw_global_ui(self) -> None:
        """Draw global UI elements (FPS, etc)."""
        if self.screen is None or self.clock is None:
            return
        
        # Draw FPS counter
        fps = self.clock.get_fps()
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 215, 0))
        fps_rect = fps_text.get_rect()
        fps_rect.topright = (self.screen.get_width() - 10, 10)
        
        # Semi-transparent background
        bg_rect = fps_rect.inflate(10, 4)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(self.screen, (255, 215, 0), bg_rect, 1)
        
        self.screen.blit(fps_text, fps_rect)
        
        # Current scene indicator
        if self.scene_manager:
            scene_name = self.scene_manager.get_current_scene_name()
            if scene_name:
                scene_text = font.render(f"Scene: {scene_name.title()}", True, (255, 215, 0))
                scene_rect = scene_text.get_rect()
                scene_rect.topright = (self.screen.get_width() - 10, 40)
                
                bg_rect = scene_rect.inflate(10, 4)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                pygame.draw.rect(self.screen, (255, 215, 0), bg_rect, 1)
                
                self.screen.blit(scene_text, scene_rect)

    def run(self) -> None:
        """Main game loop."""
        if not self.initialize():
            return

        print("🏺 Starting Sands of Duat - Egyptian Roguelike...")
        print("Welcome to the Hall of Anubis! Use WASD to explore, E to interact with portals.")
        
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