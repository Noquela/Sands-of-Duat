#!/usr/bin/env python3
"""
Sands of Duat - Main game entry point
Egyptian mythology roguelike inspired by Hades
"""

import pygame
import sys
from typing import Optional


class Game:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 60
        self.clock: Optional[pygame.time.Clock] = None
        self.screen: Optional[pygame.Surface] = None
        self.running = False

    def initialize(self) -> bool:
        """Initialize pygame and create game window."""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Sands of Duat")
            self.clock = pygame.time.Clock()
            self.running = True
            print(f"Game initialized: {self.screen_width}x{self.screen_height} @ {self.fps}fps")
            return True
        except pygame.error as e:
            print(f"Failed to initialize pygame: {e}")
            return False

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
        pass

    def render(self) -> None:
        """Render game frame."""
        if self.screen is None:
            return
        
        # Clear screen with dark sand color
        self.screen.fill((42, 35, 28))
        
        # TODO: Render game objects here
        
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        if not self.initialize():
            return

        print("Starting Sands of Duat...")
        
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