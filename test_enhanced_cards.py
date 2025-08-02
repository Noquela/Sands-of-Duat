#!/usr/bin/env python3
"""
Enhanced Card System Test

Demonstrates the new visual effects, animations, and interactions
in the card system for Sands of Duat.

Features tested:
- Enhanced card visuals with rarity colors
- Smooth hover animations and effects
- Drag and drop card interactions
- Sand cost validation with Hour-Glass system
- Card play effects and animations
"""

import pygame
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "sands_duat"))

from core.hourglass import HourGlass
from content.starter_cards import get_starter_deck, create_starter_cards
from ui.combat_screen import CombatScreen
from ui.theme import init_theme


class EnhancedCardDemo:
    """Demo application for the enhanced card system."""
    
    def __init__(self):
        pygame.init()
        
        # Initialize display for ultrawide (demo can work on any resolution)
        self.screen_width = 1920  # Use standard resolution for demo
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sands of Duat - Enhanced Card System Demo")
        
        # Initialize game systems
        init_theme()
        create_starter_cards()
        
        # Create game components
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize Hour-Glass system
        self.player_hourglass = HourGlass()
        self.player_hourglass.set_sand(3)  # Start with some sand
        
        # Create combat screen with enhanced cards
        self.combat_screen = CombatScreen()
        self.combat_screen.player_hourglass = self.player_hourglass
        self.combat_screen.on_enter()
        
        # Setup demo hand
        self.setup_demo_hand()
        
        # Demo state
        self.last_sand_update = time.time()
        self.demo_info = []
        
        print("Enhanced Card System Demo Started")
        print("Controls:")
        print("- Hover over cards to see animations")
        print("- Drag cards up to play them")
        print("- Press SPACE to add sand")
        print("- Press R to reset hand")
        print("- Press ESC to quit")
    
    def setup_demo_hand(self):
        """Setup a demo hand with various card types and costs."""
        deck = get_starter_deck()
        
        # Draw a varied hand for demonstration
        hand_cards = []
        cost_targets = [0, 1, 2, 3, 4, 5]  # One card of each cost
        
        for target_cost in cost_targets:
            cards_of_cost = deck.get_cards_by_cost(target_cost)
            if cards_of_cost:
                hand_cards.append(cards_of_cost[0])
        
        # Add one more low cost card
        low_cost_cards = deck.get_cards_by_cost(1)
        if low_cost_cards and len(low_cost_cards) > 1:
            hand_cards.append(low_cost_cards[1])
        
        self.combat_screen.set_player_cards(hand_cards)
        print(f"Demo hand: {[f'{card.name}({card.sand_cost})' for card in hand_cards]}")
    
    def handle_events(self):
        """Handle demo events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_SPACE:
                    # Add sand for testing
                    current = self.player_hourglass.current_sand
                    if current < self.player_hourglass.max_sand:
                        self.player_hourglass.set_sand(current + 1)
                        print(f"Added sand: {current + 1}/{self.player_hourglass.max_sand}")
                
                elif event.key == pygame.K_r:
                    # Reset hand
                    self.setup_demo_hand()
                    print("Hand reset")
            
            # Let combat screen handle card interactions
            self.combat_screen.handle_event(event)
    
    def update(self, delta_time):
        """Update demo systems."""
        # Update Hour-Glass (with slower regeneration for demo)
        self.player_hourglass.update_sand()
        
        # Update combat screen
        self.combat_screen.update(delta_time)
        
        # Add demo information
        self.update_demo_info()
    
    def update_demo_info(self):
        """Update demo information display."""
        self.demo_info = [
            f"Sand: {self.player_hourglass.current_sand}/{self.player_hourglass.max_sand}",
            f"FPS: {self.clock.get_fps():.1f}",
            "",
            "Card System Features:",
            "✓ Rarity-based visual styling",
            "✓ Smooth hover animations",  
            "✓ Drag and drop interactions",
            "✓ Sand cost validation",
            "✓ Glow effects and rotation",
            "✓ Adaptive hand sizing",
            "",
            "Controls:",
            "SPACE - Add sand",
            "R - Reset hand",
            "ESC - Exit"
        ]
    
    def render(self):
        """Render the demo."""
        # Clear screen with dark background
        self.screen.fill((20, 15, 10))
        
        # Render combat screen
        self.combat_screen.render(self.screen)
        
        # Render demo information
        self.render_demo_info()
        
        # Update display
        pygame.display.flip()
    
    def render_demo_info(self):
        """Render demo information overlay."""
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 20)
        
        y_offset = 20
        for i, line in enumerate(self.demo_info):
            if line.startswith("Card System Features:") or line.startswith("Controls:"):
                color = (255, 215, 0)  # Gold
                text_font = font
            elif line.startswith("✓"):
                color = (0, 255, 0)   # Green
                text_font = small_font
            elif line == "":
                y_offset += 10
                continue
            else:
                color = (255, 255, 255)  # White
                text_font = small_font
            
            text_surface = text_font.render(line, True, color)
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += text_surface.get_height() + 3
    
    def run(self):
        """Run the demo."""
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Cap delta time to prevent spiral of death
            delta_time = min(delta_time, 0.05)
            
            self.handle_events()
            self.update(delta_time)
            self.render()
            
            # Limit FPS
            self.clock.tick(60)
        
        pygame.quit()
        print("Enhanced Card System Demo ended")


if __name__ == "__main__":
    try:
        demo = EnhancedCardDemo()
        demo.run()
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()