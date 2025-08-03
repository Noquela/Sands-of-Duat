#!/usr/bin/env python3
"""
Debug test for deck builder interactions.
Creates a minimal setup to test the deck builder screen.
"""

import sys
import os
import pygame
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_deck_builder_interactions():
    """Test deck builder interactions to identify issues."""
    try:
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Deck Builder Debug Test")
        
        # Initialize theme system
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(1920, 1080)
        print(f"Theme initialized: {theme.display.display_mode.value}")
        
        # Create deck builder screen
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        deck_builder = DeckBuilderScreen()
        deck_builder.on_enter()
        
        print(f"Deck builder components: {len(deck_builder.components)}")
        for i, comp in enumerate(deck_builder.components):
            print(f"  Component {i}: {type(comp).__name__} at {comp.rect}")
        
        # Test event handling setup
        running = True
        clock = pygame.time.Clock()
        frame_count = 0
        
        print("\nStarting interaction test...")
        print("Move mouse around and click to test interactions")
        print("Press ESC to exit test")
        
        while running and frame_count < 3000:  # Max 50 seconds at 60fps
            delta_time = clock.tick(60) / 1000.0
            frame_count += 1
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Mouse click at {event.pos}, button {event.button}")
                    
                    # Test if any component receives the event
                    handled = deck_builder.handle_event(event)
                    print(f"  Event handled by deck builder: {handled}")
                    
                    # Test individual components
                    for i, comp in enumerate(deck_builder.components):
                        if comp.rect.collidepoint(event.pos):
                            print(f"  Click hits component {i}: {type(comp).__name__}")
                            comp_handled = comp.handle_event(event)
                            print(f"    Component handled event: {comp_handled}")
                
                elif event.type == pygame.MOUSEMOTION:
                    # Test hover on first few frames to see if it works
                    if frame_count < 10:
                        for i, comp in enumerate(deck_builder.components):
                            if comp.rect.collidepoint(event.pos):
                                print(f"  Mouse over component {i}: {type(comp).__name__}")
            
            # Update
            deck_builder.update(delta_time)
            
            # Render
            screen.fill((20, 15, 10))
            deck_builder.render(screen)
            pygame.display.flip()
            
            # Print status every 5 seconds
            if frame_count % 300 == 0:
                print(f"Test running... {frame_count//60} seconds")
        
        print("Test completed successfully")
        return True
        
    except Exception as e:
        print(f"Error during deck builder test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("DECK BUILDER INTERACTION DEBUG TEST")
    print("=" * 60)
    
    success = test_deck_builder_interactions()
    
    print("=" * 60)
    if success:
        print("Test completed - check output above for interaction issues")
    else:
        print("Test failed - see error details above")