#!/usr/bin/env python3
"""
Debug version of Sands of Duat to check what's happening
"""

import pygame
import sys

def main():
    print("Initializing pygame...")
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Debug - Sands of Duat")
    clock = pygame.time.Clock()
    running = True
    
    print("Game window created! Starting main loop...")
    
    frame_count = 0
    while running:
        frame_count += 1
        if frame_count % 60 == 0:  # Print every second at 60fps
            print(f"Frame {frame_count} - Game running...")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed - exiting")
                    running = False
        
        # Clear screen with background
        screen.fill((42, 35, 28))
        
        # Draw simple test
        pygame.draw.circle(screen, (255, 215, 0), (400, 300), 50)
        font = pygame.font.Font(None, 36)
        text = font.render("Sands of Duat - Press ESC to exit", True, (255, 255, 255))
        screen.blit(text, (200, 400))
        
        pygame.display.flip()
        clock.tick(60)
    
    print("Exiting game...")
    pygame.quit()

if __name__ == "__main__":
    main()