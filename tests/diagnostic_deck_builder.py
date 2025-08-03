#!/usr/bin/env python3
"""
Deck Builder Coordinate Diagnostic Tool

This script creates a specialized diagnostic version of the deck builder to help
identify and fix coordinate issues with mouse clicks and drag-and-drop functionality.

Features:
- Visual coordinate debug overlay
- Mouse position tracking
- Card position verification
- Click vs visual position comparison
- Scroll offset debugging
"""

import pygame
import sys
import logging
from typing import List, Tuple, Optional

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

def init_pygame():
    """Initialize pygame and create display."""
    pygame.init()
    
    # Use ultrawide resolution for testing
    width, height = 3440, 1440
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Deck Builder Coordinate Diagnostic")
    
    return screen

class DiagnosticCardDisplay:
    """
    Simplified card display for coordinate debugging.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, card_id: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = pygame.Rect(x, y, width, height)
        self.card_id = card_id
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.hovered = False
        self.clicked = False
        
        # Visual debugging
        self.last_click_pos = None
        self.last_hover_pos = None
        
    def handle_event(self, event: pygame.event.Event, scroll_offset: int = 0) -> bool:
        """Handle events with debugging."""
        logger = logging.getLogger(f"Card_{self.card_id}")
        
        # Adjust event position for scroll offset
        adjusted_pos = None
        if hasattr(event, 'pos'):
            adjusted_pos = (event.pos[0], event.pos[1] + scroll_offset)
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check collision with both original and adjusted positions
            original_collision = self.rect.collidepoint(event.pos)
            adjusted_collision = self.rect.collidepoint(adjusted_pos) if adjusted_pos else False
            
            logger.debug(f"Click at {event.pos}, adjusted to {adjusted_pos}")
            logger.debug(f"Card rect: {self.rect}")
            logger.debug(f"Original collision: {original_collision}, Adjusted collision: {adjusted_collision}")
            
            if adjusted_collision:
                self.being_dragged = True
                self.drag_offset_x = adjusted_pos[0] - self.rect.x
                self.drag_offset_y = adjusted_pos[1] - self.rect.y
                self.last_click_pos = event.pos
                self.clicked = True
                logger.info(f"Card {self.card_id} clicked successfully")
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.being_dragged:
                self.being_dragged = False
                logger.info(f"Card {self.card_id} drag ended at {event.pos}")
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            # Check hover
            hover_collision = self.rect.collidepoint(adjusted_pos) if adjusted_pos else False
            if hover_collision != self.hovered:
                self.hovered = hover_collision
                if hover_collision:
                    self.last_hover_pos = event.pos
                    logger.debug(f"Card {self.card_id} hover started at {event.pos}")
                    
            # Handle dragging
            if self.being_dragged and adjusted_pos:
                self.rect.x = adjusted_pos[0] - self.drag_offset_x
                self.rect.y = adjusted_pos[1] - self.drag_offset_y
                return True
                
        return False
    
    def render(self, surface: pygame.Surface):
        """Render card with debugging info."""
        # Card background
        bg_color = (100, 100, 200) if self.hovered else (60, 60, 120)
        if self.being_dragged:
            bg_color = (200, 100, 100)
        elif self.clicked:
            bg_color = (100, 200, 100)
            
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Card ID
        font = pygame.font.Font(None, 24)
        text = font.render(self.card_id, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        
        # Debug position info
        debug_font = pygame.font.Font(None, 16)
        pos_text = debug_font.render(f"({self.rect.x},{self.rect.y})", True, (255, 255, 0))
        surface.blit(pos_text, (self.rect.x, self.rect.y - 20))
        
        # Click indicator
        if self.last_click_pos:
            pygame.draw.circle(surface, (255, 0, 0), self.last_click_pos, 5)
            click_text = debug_font.render(f"Click: {self.last_click_pos}", True, (255, 0, 0))
            surface.blit(click_text, (self.last_click_pos[0] + 10, self.last_click_pos[1]))

class DiagnosticDeckBuilder:
    """
    Simplified deck builder for coordinate testing.
    """
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create theme zones similar to real implementation
        from sands_duat.ui.theme import initialize_theme, get_theme
        self.theme = initialize_theme(screen.get_width(), screen.get_height())
        
        # Get layout zones
        collection_zone = self.theme.get_zone('deck_collection')
        deck_zone = self.theme.get_zone('deck_view')
        
        # Card collection setup
        self.collection_rect = pygame.Rect(collection_zone.x, collection_zone.y, 
                                         collection_zone.width, collection_zone.height)
        self.deck_rect = pygame.Rect(deck_zone.x, deck_zone.y, 
                                   deck_zone.width, deck_zone.height)
        
        # Create test cards
        self.cards: List[DiagnosticCardDisplay] = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Mouse tracking
        self.mouse_pos = (0, 0)
        self.mouse_history: List[Tuple[int, int]] = []
        
        # Debug info
        self.show_debug_overlay = True
        self.click_history: List[Tuple[int, int]] = []
        
        self._create_test_cards()
        
    def _create_test_cards(self):
        """Create test cards for coordinate debugging."""
        cards_per_row = 8
        card_width = 130
        card_height = 180
        card_spacing = 15
        
        for i in range(40):  # Create enough cards to test scrolling
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.collection_rect.x + col * (card_width + card_spacing) + card_spacing
            y = self.collection_rect.y + row * (card_height + card_spacing) + card_spacing
            
            card = DiagnosticCardDisplay(x, y, card_width, card_height, f"Card_{i}")
            self.cards.append(card)
        
        # Calculate max scroll
        total_rows = (len(self.cards) + cards_per_row - 1) // cards_per_row
        total_height = total_rows * (card_height + card_spacing) + card_spacing
        self.max_scroll = max(0, total_height - self.collection_rect.height)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_d:
                    self.show_debug_overlay = not self.show_debug_overlay
                elif event.key == pygame.K_r:
                    # Reset all cards to original positions
                    self._reset_cards()
                    
            elif event.type == pygame.MOUSEWHEEL:
                if self.collection_rect.collidepoint(pygame.mouse.get_pos()):
                    self._scroll(-event.y * 30)
                    
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                # Keep history of last 10 mouse positions
                self.mouse_history.append(event.pos)
                if len(self.mouse_history) > 10:
                    self.mouse_history.pop(0)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_history.append(event.pos)
                if len(self.click_history) > 20:
                    self.click_history.pop(0)
            
            # Forward events to cards
            mouse_in_collection = self.collection_rect.collidepoint(self.mouse_pos)
            any_dragging = any(card.being_dragged for card in self.cards)
            
            if mouse_in_collection or any_dragging:
                # Forward event to cards with scroll adjustment
                for card in reversed(self.cards):  # Top-most first
                    if card.handle_event(event, self.scroll_offset):
                        break
    
    def _scroll(self, delta: int):
        """Handle scrolling."""
        old_offset = self.scroll_offset
        self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset + delta))
        
        if old_offset != self.scroll_offset:
            logging.debug(f"Scroll offset changed: {old_offset} -> {self.scroll_offset}")
    
    def _reset_cards(self):
        """Reset all cards to original positions."""
        for card in self.cards:
            card.rect = card.original_rect.copy()
            card.being_dragged = False
            card.clicked = False
            card.last_click_pos = None
            card.last_hover_pos = None
        self.scroll_offset = 0
    
    def render(self):
        """Render the diagnostic display."""
        self.screen.fill((30, 25, 20))  # Dark background
        
        # Draw collection area
        pygame.draw.rect(self.screen, (40, 35, 30), self.collection_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.collection_rect, 2)
        
        # Draw deck area
        pygame.draw.rect(self.screen, (25, 20, 15), self.deck_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.deck_rect, 2)
        
        # Create clipping surface for collection
        collection_surface = self.screen.subsurface(self.collection_rect)
        
        # Render cards with scroll offset
        for card in self.cards:
            if self._is_card_visible(card):
                # Adjust card position for rendering
                adjusted_rect = card.rect.copy()
                adjusted_rect.y -= self.scroll_offset
                
                # Temporarily adjust card rect for rendering
                original_rect = card.rect
                card.rect = adjusted_rect
                card.render(collection_surface)
                card.rect = original_rect
        
        # Debug overlay
        if self.show_debug_overlay:
            self._render_debug_overlay()
        
        # Labels
        font = pygame.font.Font(None, 32)
        collection_label = font.render("Collection (with scroll)", True, (255, 255, 255))
        self.screen.blit(collection_label, (self.collection_rect.x, self.collection_rect.y - 40))
        
        deck_label = font.render("Deck Drop Zone", True, (255, 255, 255))
        self.screen.blit(deck_label, (self.deck_rect.x, self.deck_rect.y - 40))
    
    def _is_card_visible(self, card: DiagnosticCardDisplay) -> bool:
        """Check if card is visible in scrolled area."""
        adjusted_y = card.rect.y - self.scroll_offset
        return (adjusted_y + card.rect.height >= self.collection_rect.y and 
                adjusted_y <= self.collection_rect.bottom)
    
    def _render_debug_overlay(self):
        """Render debug information overlay."""
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        debug_y = 10
        line_height = 25
        
        # Current mouse position
        mouse_text = font.render(f"Mouse: {self.mouse_pos}", True, (255, 255, 0))
        self.screen.blit(mouse_text, (10, debug_y))
        debug_y += line_height
        
        # Scroll offset
        scroll_text = font.render(f"Scroll Offset: {self.scroll_offset}/{self.max_scroll}", True, (255, 255, 0))
        self.screen.blit(scroll_text, (10, debug_y))
        debug_y += line_height
        
        # Collection area bounds
        bounds_text = small_font.render(f"Collection: {self.collection_rect}", True, (255, 255, 0))
        self.screen.blit(bounds_text, (10, debug_y))
        debug_y += line_height
        
        # Deck area bounds
        deck_bounds_text = small_font.render(f"Deck: {self.deck_rect}", True, (255, 255, 0))
        self.screen.blit(deck_bounds_text, (10, debug_y))
        debug_y += line_height
        
        # Mouse trail
        if len(self.mouse_history) > 1:
            for i in range(1, len(self.mouse_history)):
                start_pos = self.mouse_history[i-1]
                end_pos = self.mouse_history[i]
                alpha = int(255 * i / len(self.mouse_history))
                color = (255, alpha, alpha)
                pygame.draw.line(self.screen, color, start_pos, end_pos, 2)
        
        # Click history
        for i, click_pos in enumerate(self.click_history[-5:]):  # Last 5 clicks
            alpha = int(255 * (i + 1) / 5)
            color = (alpha, 255, alpha)
            pygame.draw.circle(self.screen, color, click_pos, 8, 2)
        
        # Instructions
        instructions = [
            "Controls:",
            "ESC - Exit",
            "D - Toggle debug overlay",
            "R - Reset cards",
            "Mouse wheel - Scroll collection"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (self.screen.get_width() - 300, 10 + i * 20))
    
    def run(self):
        """Main diagnostic loop."""
        logging.info("Starting deck builder coordinate diagnostic")
        logging.info("Collection area: %s", self.collection_rect)
        logging.info("Deck area: %s", self.deck_rect)
        
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            self.render()
            
            pygame.display.flip()
        
        logging.info("Diagnostic completed")

def main():
    """Main function."""
    try:
        screen = init_pygame()
        diagnostic = DiagnosticDeckBuilder(screen)
        diagnostic.run()
        
    except Exception as e:
        logging.error(f"Diagnostic failed: {e}", exc_info=True)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()