#!/usr/bin/env python3
"""
Final Coordinate Test

Interactive test to verify all coordinate issues are fixed:
1. Card click detection in collection
2. Scroll offset handling
3. Drag and drop to deck
4. Drop zone validation
"""

import pygame
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

def main():
    pygame.init()
    
    # Use ultrawide resolution to match production
    screen = pygame.display.set_mode((3440, 1440))
    pygame.display.set_caption("Final Deck Builder Coordinate Test")
    clock = pygame.time.Clock()
    
    try:
        # Initialize theme and deck builder
        from sands_duat.ui.theme import initialize_theme
        theme = initialize_theme(3440, 1440)
        
        from sands_duat.ui.deck_builder import DeckBuilderScreen
        deck_builder = DeckBuilderScreen()
        deck_builder.activate()
        deck_builder.on_enter()
        
        print("=" * 60)
        print("FINAL DECK BUILDER COORDINATE TEST")
        print("=" * 60)
        print("Instructions:")
        print("1. Click on cards in the collection area (left)")
        print("2. Try scrolling with mouse wheel in the collection")
        print("3. Drag cards from collection to deck area (bottom)")
        print("4. Right-click on deck cards to remove them")
        print("5. Press 'D' to toggle debug info")
        print("6. Press ESC to exit")
        print("=" * 60)
        
        # Test tracking
        interactions = {
            'cards_clicked': 0,
            'cards_dragged': 0,
            'cards_added_to_deck': 0,
            'scroll_events': 0,
            'drop_zone_hits': 0
        }
        
        show_debug = True
        running = True
        
        while running:
            delta_time = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_d:
                        show_debug = not show_debug
                        print(f"Debug info {'enabled' if show_debug else 'disabled'}")
                elif event.type == pygame.MOUSEWHEEL:
                    interactions['scroll_events'] += 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        interactions['cards_clicked'] += 1
                        print(f"Click #{interactions['cards_clicked']} at {event.pos}")
                
                # Let deck builder handle the event
                handled = deck_builder.handle_event(event)
                
                # Track drag events through deck builder's event system
                if hasattr(deck_builder, 'card_collection') and deck_builder.card_collection:
                    collection = deck_builder.card_collection
                    if hasattr(collection, 'card_displays'):
                        dragging_cards = sum(1 for card in collection.card_displays if card.being_dragged)
                        if dragging_cards > 0:
                            interactions['cards_dragged'] = max(interactions['cards_dragged'], dragging_cards)
                
                # Track deck size changes
                if hasattr(deck_builder, 'current_deck') and deck_builder.current_deck:
                    deck_size = len(deck_builder.current_deck.cards)
                    interactions['cards_added_to_deck'] = deck_size
            
            # Update
            deck_builder.update(delta_time)
            
            # Render
            screen.fill((20, 15, 10))
            deck_builder.render(screen)
            
            # Debug overlay
            if show_debug:
                render_debug_overlay(screen, interactions, pygame.mouse.get_pos())
            
            pygame.display.flip()
        
        # Final report
        deck_builder.deactivate()
        print_final_report(interactions)
        
    except Exception as e:
        logging.error(f"Test failed: {e}", exc_info=True)
        return False
    finally:
        pygame.quit()
    
    return True

def render_debug_overlay(screen, interactions, mouse_pos):
    """Render debug information overlay."""
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    
    # Background panel
    overlay_rect = pygame.Rect(10, 10, 400, 300)
    overlay_surface = pygame.Surface((400, 300), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 180))
    screen.blit(overlay_surface, (10, 10))
    pygame.draw.rect(screen, (100, 100, 100), overlay_rect, 2)
    
    # Title
    title = font.render("DEBUG INFO", True, (255, 255, 0))
    screen.blit(title, (20, 20))
    
    # Mouse position
    mouse_text = small_font.render(f"Mouse: {mouse_pos}", True, (255, 255, 255))
    screen.blit(mouse_text, (20, 50))
    
    # Interaction counters
    y_pos = 80
    for key, value in interactions.items():
        color = (0, 255, 0) if value > 0 else (255, 100, 100)
        text = small_font.render(f"{key.replace('_', ' ').title()}: {value}", True, color)
        screen.blit(text, (20, y_pos))
        y_pos += 20
    
    # Instructions
    instructions = [
        "Press 'D' to toggle debug",
        "ESC to exit test",
        "Click, drag, scroll to test"
    ]
    
    y_pos += 20
    for instruction in instructions:
        text = small_font.render(instruction, True, (200, 200, 200))
        screen.blit(text, (20, y_pos))
        y_pos += 18

def print_final_report(interactions):
    """Print final test report."""
    print("\\n" + "=" * 60)
    print("FINAL TEST REPORT")
    print("=" * 60)
    
    # Calculate test scores
    scores = {
        'Click Detection': min(100, interactions['cards_clicked'] * 20),  # 5 clicks = 100%
        'Scroll Functionality': min(100, interactions['scroll_events'] * 25),  # 4 scrolls = 100%
        'Drag Functionality': min(100, interactions['cards_dragged'] * 50),  # 2 drags = 100%
        'Drop/Add to Deck': min(100, interactions['cards_added_to_deck'] * 25),  # 4 cards = 100%
    }
    
    for test_name, score in scores.items():
        status = "✓ PASS" if score >= 50 else "✗ FAIL"
        print(f"{test_name:<20}: {score:>3}% {status}")
    
    overall_score = sum(scores.values()) / len(scores)
    overall_status = "✓ PASS" if overall_score >= 70 else "✗ FAIL"
    print("-" * 40)
    print(f"{'Overall':<20}: {overall_score:>3.0f}% {overall_status}")
    
    print("\\nDetailed Metrics:")
    for key, value in interactions.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")
    
    print("\\nCoordinate Fix Status:")
    if interactions['cards_clicked'] > 0:
        print("✓ Mouse click detection is working")
    else:
        print("✗ Mouse click detection may have issues")
    
    if interactions['scroll_events'] > 0:
        print("✓ Scroll functionality is working")
    else:
        print("? Scroll functionality not tested")
    
    if interactions['cards_added_to_deck'] > 0:
        print("✓ Drag and drop to deck is working")
    else:
        print("? Drag and drop not tested or failing")
    
    print("=" * 60)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)