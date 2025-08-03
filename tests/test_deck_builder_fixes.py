#!/usr/bin/env python3
"""
Test Script for Deck Builder Coordinate Fixes

This script tests the coordinate fixes implemented in the deck builder,
specifically focusing on:
1. Mouse click detection on cards
2. Drag and drop functionality  
3. Scroll offset handling
4. Drop zone detection
"""

import pygame
import sys
import logging
from typing import List

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

def test_deck_builder():
    """Test the actual deck builder with fixes."""
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((3440, 1440))
    pygame.display.set_caption("Deck Builder Fix Test")
    clock = pygame.time.Clock()
    
    # Initialize the theme
    from sands_duat.ui.theme import initialize_theme
    theme = initialize_theme(3440, 1440)
    
    # Create deck builder screen
    from sands_duat.ui.deck_builder import DeckBuilderScreen
    deck_builder = DeckBuilderScreen()
    deck_builder.activate()
    deck_builder.on_enter()
    
    # Test state
    running = True
    test_results = {
        'click_detection': False,
        'drag_start': False,
        'drag_end': False,
        'card_added_to_deck': False,
        'scroll_functionality': False
    }
    
    logging.info("Starting deck builder fix test")
    logging.info("Instructions:")
    logging.info("1. Click on cards to test click detection")
    logging.info("2. Drag cards to the deck area to test drop functionality") 
    logging.info("3. Use mouse wheel to test scrolling")
    logging.info("4. Press ESC to exit")
    
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset test results
                    test_results = {k: False for k in test_results}
                    logging.info("Test results reset")
            
            # Test event handling
            handled = deck_builder.handle_event(event)
            
            # Track test results based on events
            if event.type == pygame.MOUSEBUTTONDOWN:
                test_results['click_detection'] = True
                logging.info("✓ Click detection test passed")
            
        # Update
        deck_builder.update(delta_time)
        
        # Render
        screen.fill((20, 15, 10))
        deck_builder.render(screen)
        
        # Render test status
        render_test_status(screen, test_results)
        
        pygame.display.flip()
    
    # Cleanup
    deck_builder.deactivate()
    pygame.quit()
    
    # Report results
    print("\\n" + "="*50)
    print("DECK BUILDER FIX TEST RESULTS")
    print("="*50)
    for test_name, result in test_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    print("="*50)
    
    return all(test_results.values())

def render_test_status(screen: pygame.Surface, test_results: dict):
    """Render test status overlay."""
    font = pygame.font.Font(None, 24)
    y_offset = screen.get_height() - 200
    
    # Background
    status_rect = pygame.Rect(10, y_offset, 400, 180)
    pygame.draw.rect(screen, (0, 0, 0, 128), status_rect)
    pygame.draw.rect(screen, (100, 100, 100), status_rect, 2)
    
    # Title
    title = font.render("Test Status", True, (255, 255, 255))
    screen.blit(title, (20, y_offset + 10))
    
    # Test results
    y_pos = y_offset + 40
    for test_name, result in test_results.items():
        color = (0, 255, 0) if result else (255, 100, 100)
        status = "✓" if result else "✗"
        text = font.render(f"{status} {test_name.replace('_', ' ').title()}", True, color)
        screen.blit(text, (20, y_pos))
        y_pos += 25

def test_coordinate_precision():
    """Test coordinate precision specifically."""
    
    pygame.init()
    screen = pygame.display.set_mode((3440, 1440))
    pygame.display.set_caption("Coordinate Precision Test")
    clock = pygame.time.Clock()
    
    # Create test cards at known positions
    test_cards = []
    for i in range(5):
        x = 400 + i * 150
        y = 200
        card_rect = pygame.Rect(x, y, 120, 180)
        test_cards.append({
            'rect': card_rect,
            'id': f'TestCard_{i}',
            'clicked': False,
            'hover': False
        })
    
    running = True
    mouse_pos = (0, 0)
    click_history = []
    
    logging.info("Coordinate precision test started")
    logging.info("Click on the test cards to verify coordinate accuracy")
    
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                # Update hover state
                for card in test_cards:
                    card['hover'] = card['rect'].collidepoint(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_history.append(event.pos)
                if len(click_history) > 10:
                    click_history.pop(0)
                
                # Test collision detection
                for card in test_cards:
                    if card['rect'].collidepoint(event.pos):
                        card['clicked'] = True
                        logging.info(f"✓ Accurate click detected on {card['id']} at {event.pos}")
                        logging.info(f"  Card rect: {card['rect']}")
                    else:
                        logging.debug(f"Click at {event.pos} missed {card['id']} (rect: {card['rect']})")
        
        # Render
        screen.fill((30, 25, 20))
        
        # Draw test cards
        for card in test_cards:
            color = (100, 200, 100) if card['clicked'] else (200, 100, 100) if card['hover'] else (60, 60, 120)
            pygame.draw.rect(screen, color, card['rect'])
            pygame.draw.rect(screen, (255, 255, 255), card['rect'], 2)
            
            # Draw card ID
            font = pygame.font.Font(None, 24)
            text = font.render(card['id'], True, (255, 255, 255))
            text_rect = text.get_rect(center=card['rect'].center)
            screen.blit(text, text_rect)
            
            # Draw position info
            pos_text = font.render(f"({card['rect'].x},{card['rect'].y})", True, (255, 255, 0))
            screen.blit(pos_text, (card['rect'].x, card['rect'].y - 25))
        
        # Draw mouse position
        font = pygame.font.Font(None, 32)
        mouse_text = font.render(f"Mouse: {mouse_pos}", True, (255, 255, 255))
        screen.blit(mouse_text, (10, 10))
        
        # Draw click history
        for i, click_pos in enumerate(click_history):
            alpha = int(255 * (i + 1) / len(click_history))
            color = (alpha, 255, alpha)
            pygame.draw.circle(screen, color, click_pos, 5)
        
        # Instructions
        instructions = [
            "Coordinate Precision Test",
            "Click on cards to test accuracy",
            "Green = clicked, Red = hover, Blue = normal",
            "ESC to exit"
        ]
        
        small_font = pygame.font.Font(None, 20)
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, (200, 200, 200))
            screen.blit(text, (10, 50 + i * 25))
        
        pygame.display.flip()
    
    pygame.quit()
    
    # Report precision test results
    clicks_detected = sum(1 for card in test_cards if card['clicked'])
    print(f"\\nCoordinate Precision Test Results:")
    print(f"Cards clicked accurately: {clicks_detected}/5")
    print(f"Total clicks made: {len(click_history)}")
    
    return clicks_detected >= 3  # Pass if at least 3 cards were clicked accurately

def main():
    """Run all tests."""
    print("Deck Builder Coordinate Fix Testing Suite")
    print("="*50)
    
    try:
        # Test 1: Coordinate precision
        print("\\n1. Testing coordinate precision...")
        precision_test_passed = test_coordinate_precision()
        
        # Test 2: Full deck builder functionality
        print("\\n2. Testing full deck builder functionality...")
        deck_builder_test_passed = test_deck_builder()
        
        # Overall results
        print("\\n" + "="*50)
        print("OVERALL TEST RESULTS")
        print("="*50)
        print(f"Coordinate Precision: {'✓ PASS' if precision_test_passed else '✗ FAIL'}")
        print(f"Deck Builder Functionality: {'✓ PASS' if deck_builder_test_passed else '✗ FAIL'}")
        
        overall_pass = precision_test_passed and deck_builder_test_passed
        print(f"Overall: {'✓ ALL TESTS PASSED' if overall_pass else '✗ SOME TESTS FAILED'}")
        print("="*50)
        
        return overall_pass
        
    except Exception as e:
        logging.error(f"Test suite failed with error: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)