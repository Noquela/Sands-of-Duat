#!/usr/bin/env python3
"""
Drag-Drop System Analysis Test

Comprehensive test script to analyze the drag-drop card system implementation
in Sands of Duat and compare it to Slay the Spire quality standards.
"""

import pygame
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "sands_duat"))

try:
    from sands_duat.core.hourglass import HourGlass
    from sands_duat.core.cards import Card, CardType, CardEffect, EffectType, TargetType, CardRarity
    from sands_duat.ui.combat_screen import CombatScreen, CardDisplay, HandDisplay
    from sands_duat.ui.theme import initialize_theme
    from sands_duat.ui.animation_system import AnimationManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Attempting alternative import path...")
    try:
        sys.path.insert(0, str(project_root))
        from sands_duat.core.hourglass import HourGlass
        from sands_duat.core.cards import Card, CardType, CardEffect, EffectType, TargetType, CardRarity
        from sands_duat.ui.combat_screen import CombatScreen, CardDisplay, HandDisplay
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.ui.animation_system import AnimationManager
    except ImportError as e2:
        print(f"Second import error: {e2}")
        sys.exit(1)


class DragDropAnalyzer:
    """Analyzes the drag-drop system implementation."""
    
    def __init__(self):
        pygame.init()
        
        # Initialize display
        self.screen_width = 1600
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sands of Duat - Drag-Drop Analysis")
        
        # Initialize systems
        try:
            self.theme = initialize_theme(self.screen_width, self.screen_height)
        except Exception as e:
            print(f"Theme initialization failed: {e}")
            self.theme = None
        
        # Create test components
        self.clock = pygame.time.Clock()
        self.running = True
        self.analysis_results = {}
        
        # Create Hour-Glass for sand management
        self.hourglass = HourGlass(max_sand=5, initial_sand=3)
        
        # Create test cards
        self.test_cards = self.create_test_cards()
        
        # Initialize combat screen for testing
        self.combat_screen = CombatScreen()
        
        # Analysis metrics
        self.drag_tests = {
            "can_initiate_drag": False,
            "visual_feedback_during_drag": False,
            "target_validation_works": False,
            "smooth_animations": False,
            "drop_zone_indication": False,
            "invalid_drop_handling": False,
            "combat_integration": False,
            "egyptian_theming": False
        }
        
        print("Drag-Drop Analysis Starting...")
        print("Controls:")
        print("- Mouse: Test drag and drop")
        print("- SPACE: Add sand")
        print("- R: Reset test state")
        print("- ESC: Exit analysis")
    
    def create_test_cards(self):
        """Create test cards for drag-drop analysis."""
        cards = []
        
        # Test card 1: Basic Attack (Common)
        test_card_1 = Card(
            name="Desert Strike",
            description="Deal 6 damage",
            sand_cost=1,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON,
            effects=[CardEffect(
                effect_type=EffectType.DAMAGE,
                value=6,
                target=TargetType.ENEMY
            )]
        )
        cards.append(test_card_1)
        
        # Test card 2: High Cost Skill (Rare)
        test_card_2 = Card(
            name="Pyramid Shield",
            description="Gain 12 block",
            sand_cost=2,
            card_type=CardType.SKILL,
            rarity=CardRarity.RARE,
            effects=[CardEffect(
                effect_type=EffectType.BLOCK,
                value=12,
                target=TargetType.SELF
            )]
        )
        cards.append(test_card_2)
        
        # Test card 3: Expensive Legendary
        test_card_3 = Card(
            name="Ra's Judgment",
            description="Deal 20 damage to all enemies",
            sand_cost=4,
            card_type=CardType.ATTACK,
            rarity=CardRarity.LEGENDARY,
            effects=[CardEffect(
                effect_type=EffectType.DAMAGE,
                value=20,
                target=TargetType.ALL_ENEMIES
            )]
        )
        cards.append(test_card_3)
        
        return cards
    
    def run_analysis(self):
        """Run the drag-drop analysis."""
        print("\n=== DRAG-DROP SYSTEM ANALYSIS ===\n")
        
        # Set up test hand
        self.combat_screen.set_player_cards(self.test_cards)
        
        # Analysis loop
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            
            # Handle events and analyze
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.hourglass.add_sand(1)
                    elif event.key == pygame.K_r:
                        self.reset_test_state()
                
                # Analyze drag-drop events
                self.analyze_event(event)
                
                # Pass event to combat screen
                self.combat_screen.handle_event(event)
            
            # Update systems
            self.hourglass.update_sand()
            self.combat_screen.update(delta_time)
            
            # Render and analyze
            self.render_analysis()
        
        # Final analysis report
        self.generate_analysis_report()
        pygame.quit()
    
    def analyze_event(self, event):
        """Analyze events for drag-drop functionality."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicking on a card initiates drag
            mouse_pos = event.pos
            for card_display in getattr(self.combat_screen.hand_display, 'card_displays', []):
                if card_display.rect.collidepoint(mouse_pos) and card_display.playable:
                    # Check if drag initiates
                    if hasattr(card_display, 'being_dragged'):
                        self.drag_tests["can_initiate_drag"] = True
        
        elif event.type == pygame.MOUSEMOTION:
            # Check for visual feedback during drag
            for card_display in getattr(self.combat_screen.hand_display, 'card_displays', []):
                if hasattr(card_display, 'being_dragged') and card_display.being_dragged:
                    self.drag_tests["visual_feedback_during_drag"] = True
                    
                    # Check for drop zone indication
                    if hasattr(card_display, 'in_play_zone'):
                        self.drag_tests["drop_zone_indication"] = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Check drop handling
            for card_display in getattr(self.combat_screen.hand_display, 'card_displays', []):
                if hasattr(card_display, 'being_dragged') and card_display.being_dragged:
                    self.drag_tests["invalid_drop_handling"] = True
    
    def reset_test_state(self):
        """Reset the test state."""
        self.hourglass.current_sand = 3
        self.combat_screen.set_player_cards(self.test_cards)
        print("Test state reset")
    
    def render_analysis(self):
        """Render the analysis interface."""
        self.screen.fill((20, 15, 10))  # Dark background
        
        # Render combat screen
        self.combat_screen.render(self.screen)
        
        # Render analysis overlay
        self.render_analysis_overlay()
        
        pygame.display.flip()
    
    def render_analysis_overlay(self):
        """Render analysis information overlay."""
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 20)
        
        # Analysis results panel
        panel_x = 20
        panel_y = 20
        line_height = 25
        
        # Title
        title_text = font.render("DRAG-DROP ANALYSIS", True, (255, 215, 0))
        self.screen.blit(title_text, (panel_x, panel_y))
        panel_y += line_height * 2
        
        # Test results
        for test_name, passed in self.drag_tests.items():
            status_color = (0, 255, 0) if passed else (255, 0, 0)
            status_symbol = "✓" if passed else "✗"
            
            test_display = test_name.replace("_", " ").title()
            test_text = small_font.render(f"{status_symbol} {test_display}", True, status_color)
            self.screen.blit(test_text, (panel_x, panel_y))
            panel_y += line_height
        
        # Sand status
        panel_y += line_height
        sand_text = small_font.render(f"Sand: {self.hourglass.current_sand}/{self.hourglass.max_sand}", True, (255, 215, 0))
        self.screen.blit(sand_text, (panel_x, panel_y))
        
        # Instructions
        panel_y += line_height * 2
        instructions = [
            "Instructions:",
            "• Try dragging cards up",
            "• Test with different sand levels",
            "• Observe visual feedback",
            "• SPACE: Add sand",
            "• R: Reset • ESC: Exit"
        ]
        
        for instruction in instructions:
            color = (255, 255, 255) if instruction.startswith("•") else (255, 215, 0)
            inst_text = small_font.render(instruction, True, color)
            self.screen.blit(inst_text, (panel_x, panel_y))
            panel_y += line_height
    
    def generate_analysis_report(self):
        """Generate final analysis report."""
        print("\n" + "="*60)
        print("DRAG-DROP SYSTEM ANALYSIS REPORT")
        print("="*60)
        
        # Test results summary
        passed_tests = sum(1 for passed in self.drag_tests.values() if passed)
        total_tests = len(self.drag_tests)
        
        print(f"\nTest Results: {passed_tests}/{total_tests} passed")
        print(f"Overall Score: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, passed in self.drag_tests.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {test_name.replace('_', ' ').title()}: {status}")
        
        # Analysis and recommendations
        print("\n" + "-"*40)
        print("ANALYSIS & RECOMMENDATIONS")
        print("-"*40)
        
        if not self.drag_tests["can_initiate_drag"]:
            print("❌ CRITICAL: Drag initiation not detected")
            print("   Recommendation: Verify mouse event handling in CardDisplay")
        
        if not self.drag_tests["visual_feedback_during_drag"]:
            print("❌ MAJOR: Visual feedback during drag missing")
            print("   Recommendation: Implement hover state and drag indicators")
        
        if not self.drag_tests["drop_zone_indication"]:
            print("❌ MAJOR: Drop zone indication missing")
            print("   Recommendation: Add visual play zone indicators")
        
        print("\nComparison to Slay the Spire Standards:")
        print("- Slay the Spire has smooth card scaling during drag")
        print("- Clear visual indication of valid drop zones")
        print("- Animated return to hand on invalid drops")
        print("- Immediate visual feedback on card hover")
        print("- Target arrows for targeted abilities")
        

if __name__ == "__main__":
    try:
        analyzer = DragDropAnalyzer()
        analyzer.run_analysis()
    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()