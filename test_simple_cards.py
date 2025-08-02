#!/usr/bin/env python3
"""
Simple Card System Test

Basic test of the enhanced card visual system without
complex content validation dependencies.
"""

import pygame
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "sands_duat"))

from core.hourglass import HourGlass
from core.cards import Card, CardEffect, CardType, CardRarity, EffectType, TargetType
from ui.combat_screen import CombatScreen
from ui.theme import initialize_theme


class SimpleCardDemo:
    """Simple demo for the enhanced card system."""
    
    def __init__(self):
        pygame.init()
        
        # Initialize display
        self.screen_width = 1600
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sands of Duat - Simple Card Demo")
        
        # Initialize systems
        initialize_theme(self.screen_width, self.screen_height)
        
        # Create game components
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize Hour-Glass system
        self.player_hourglass = HourGlass()
        self.player_hourglass.set_sand(4)  # Start with some sand
        
        # Create simple demo cards
        self.demo_cards = self.create_demo_cards()
        
        # Create combat screen
        self.combat_screen = CombatScreen()
        self.combat_screen.player_hourglass = self.player_hourglass
        self.combat_screen.on_enter()
        
        # Set up demo hand
        self.combat_screen.set_player_cards(self.demo_cards)
        
        print("Simple Card Demo Started")
        print("Controls:")
        print("- Hover over cards to see animations")
        print("- Drag cards up to play them")
        print("- Press SPACE to add sand")
        print("- Press ESC to quit")
    
    def create_demo_cards(self):
        """Create simple demo cards without complex dependencies."""
        cards = []
        
        # Simple attack card (1 cost)
        strike = Card(
            name="Desert Strike",
            description="Deal 6 damage to an enemy.",
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[
                CardEffect(effect_type=EffectType.DAMAGE, value=6, target=TargetType.ENEMY)
            ]
        )
        cards.append(strike)
        
        # Simple heal card (2 cost)
        heal = Card(
            name="Oasis Water",
            description="Restore 8 health.",
            sand_cost=2,
            card_type=CardType.SKILL,
            rarity=CardRarity.COMMON,
            effects=[
                CardEffect(effect_type=EffectType.HEAL, value=8, target=TargetType.SELF)
            ]
        )
        cards.append(heal)
        
        # Powerful attack (3 cost)
        power_attack = Card(
            name="Sandstorm Fury",
            description="Deal 14 damage with the fury of the desert.",
            sand_cost=3,
            card_type=CardType.ATTACK,
            rarity=CardRarity.UNCOMMON,
            effects=[
                CardEffect(effect_type=EffectType.DAMAGE, value=14, target=TargetType.ENEMY)
            ]
        )
        cards.append(power_attack)
        
        # Utility card (1 cost)
        draw = Card(
            name="Ancient Wisdom",
            description="Draw 2 cards from the sands of time.",
            sand_cost=1,
            card_type=CardType.SKILL,
            rarity=CardRarity.COMMON,
            effects=[
                CardEffect(effect_type=EffectType.DRAW_CARDS, value=2, target=TargetType.SELF)
            ]
        )
        cards.append(draw)
        
        # Expensive finisher (5 cost)
        finisher = Card(
            name="Ra's Judgment",
            description="Unleash the sun god's wrath for massive damage.",
            sand_cost=5,
            card_type=CardType.ATTACK,
            rarity=CardRarity.RARE,
            effects=[
                CardEffect(effect_type=EffectType.DAMAGE, value=25, target=TargetType.ENEMY)
            ]
        )
        cards.append(finisher)
        
        # Free card (0 cost)
        free_card = Card(
            name="Desert Breeze",
            description="A gentle breeze carries ancient power.",
            sand_cost=0,
            card_type=CardType.SKILL,
            rarity=CardRarity.COMMON,
            effects=[
                CardEffect(effect_type=EffectType.GAIN_SAND, value=1, target=TargetType.SELF)
            ]
        )
        cards.append(free_card)
        
        return cards
    
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
            
            # Let combat screen handle card interactions
            self.combat_screen.handle_event(event)
    
    def update(self, delta_time):
        """Update demo systems."""
        # Update Hour-Glass
        self.player_hourglass.update_sand()
        
        # Update combat screen
        self.combat_screen.update(delta_time)
    
    def render(self):
        """Render the demo."""
        # Clear screen
        self.screen.fill((20, 15, 10))
        
        # Render combat screen
        self.combat_screen.render(self.screen)
        
        # Render info
        self.render_info()
        
        # Update display
        pygame.display.flip()
    
    def render_info(self):
        """Render demo information."""
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            f"Sand: {self.player_hourglass.current_sand}/{self.player_hourglass.max_sand}",
            f"FPS: {self.clock.get_fps():.1f}",
            "",
            "Enhanced Card Features:",
            "✓ Rarity-based borders",
            "✓ Hover animations",
            "✓ Drag and drop",
            "✓ Sand cost validation",
            "✓ Glow effects",
            "",
            "SPACE - Add sand, ESC - Exit"
        ]
        
        y = 20
        for line in info_lines:
            if line.startswith("✓"):
                color = (0, 255, 0)
            elif line == "":
                y += 10
                continue
            elif line.startswith("Enhanced"):
                color = (255, 215, 0)
            else:
                color = (255, 255, 255)
            
            text = font.render(line, True, color)
            self.screen.blit(text, (20, y))
            y += text.get_height() + 3
    
    def run(self):
        """Run the demo."""
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Cap delta time
            delta_time = min(delta_time, 0.05)
            
            self.handle_events()
            self.update(delta_time)
            self.render()
            
            self.clock.tick(60)
        
        pygame.quit()
        print("Simple Card Demo ended")


if __name__ == "__main__":
    try:
        demo = SimpleCardDemo()
        demo.run()
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()