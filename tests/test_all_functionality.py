#!/usr/bin/env python3
"""
Comprehensive functionality test script for Sands of Duat

This script tests all major game functionality systematically to identify bugs and missing features.
"""

import sys
import logging
import pygame
from typing import List, Dict, Any

# Add the game directory to the path
sys.path.insert(0, '.')

from sands_duat.ui.ui_manager import UIManager
from sands_duat.ui.theme import initialize_theme
from sands_duat.content.starter_cards import get_starter_deck
from sands_duat.core.engine import GameEngine

class SystemTester:
    """Automated testing system for game functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results: Dict[str, Dict[str, Any]] = {}
        self.ui_manager = None
        
    def setup_test_environment(self) -> bool:
        """Setup the test environment."""
        try:
            # Initialize pygame
            pygame.init()
            screen = pygame.display.set_mode((1920, 1080))
            pygame.display.set_caption("Sands of Duat - System Test")
            
            # Initialize game systems
            initialize_theme(1920, 1080)
            
            # Initialize UI Manager
            self.ui_manager = UIManager(screen)
            
            # Add all screens
            from sands_duat.ui.ui_manager import get_menu_screen, get_combat_screen, get_deck_builder_screen
            from sands_duat.ui.ui_manager import get_tutorial_screen, get_progression_screen
            
            self.ui_manager.add_screen(get_menu_screen()())
            self.ui_manager.add_screen(get_combat_screen()())
            self.ui_manager.add_screen(get_deck_builder_screen()())
            self.ui_manager.add_screen(get_tutorial_screen()())
            self.ui_manager.add_screen(get_progression_screen()())
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup test environment: {e}")
            return False
    
    def test_menu_functionality(self) -> Dict[str, Any]:
        """Test menu screen functionality."""
        results = {"name": "Menu System", "tests": [], "passed": 0, "failed": 0}
        
        try:
            # Test menu screen exists
            menu_screen = self.ui_manager.get_screen("menu")
            if menu_screen:
                results["tests"].append({"name": "Menu screen exists", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Menu screen exists", "status": "FAIL", "error": "Menu screen not found"})
                results["failed"] += 1
            
            # Test menu components
            if hasattr(menu_screen, 'buttons'):
                button_names = [btn.text for btn in menu_screen.buttons] if menu_screen.buttons else []
                expected_buttons = ["New Game", "Continue", "Temple Map", "Tutorial", "Deck Builder", "Settings", "Credits", "Exit"]
                
                for expected in expected_buttons:
                    if expected in button_names:
                        results["tests"].append({"name": f"Button '{expected}' exists", "status": "PASS"})
                        results["passed"] += 1
                    else:
                        results["tests"].append({"name": f"Button '{expected}' exists", "status": "FAIL", "error": "Button not found"})
                        results["failed"] += 1
            
        except Exception as e:
            results["tests"].append({"name": "Menu system test", "status": "ERROR", "error": str(e)})
            results["failed"] += 1
        
        return results
    
    def test_card_system(self) -> Dict[str, Any]:
        """Test card system functionality."""
        results = {"name": "Card System", "tests": [], "passed": 0, "failed": 0}
        
        try:
            # Test deck creation
            deck = get_starter_deck()
            if deck and len(deck) > 0:
                results["tests"].append({"name": f"Starter deck created ({len(deck)} cards)", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Starter deck creation", "status": "FAIL", "error": "Empty or no deck"})
                results["failed"] += 1
            
            # Test Egyptian card loading
            from sands_duat.content.egyptian_card_loader import initialize_egyptian_cards
            egyptian_cards = initialize_egyptian_cards()
            if egyptian_cards and len(egyptian_cards) > 0:
                results["tests"].append({"name": f"Egyptian cards loaded ({len(egyptian_cards)} cards)", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Egyptian cards loading", "status": "FAIL", "error": "No Egyptian cards loaded"})
                results["failed"] += 1
            
            # Test card library
            from sands_duat.core.cards import card_library
            if card_library and len(card_library._cards) > 0:
                results["tests"].append({"name": f"Card library populated ({len(card_library._cards)} cards)", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Card library population", "status": "FAIL", "error": "Card library empty"})
                results["failed"] += 1
                
        except Exception as e:
            results["tests"].append({"name": "Card system test", "status": "ERROR", "error": str(e)})
            results["failed"] += 1
        
        return results
    
    def test_combat_system(self) -> Dict[str, Any]:
        """Test combat system functionality."""
        results = {"name": "Combat System", "tests": [], "passed": 0, "failed": 0}
        
        try:
            # Test combat manager initialization
            from sands_duat.core.combat_manager import CombatManager
            combat_manager = CombatManager()
            
            results["tests"].append({"name": "Combat manager initialization", "status": "PASS"})
            results["passed"] += 1
            
            # Test combat setup
            deck = get_starter_deck()
            hand_cards = deck.cards[:5] if len(deck.cards) >= 5 else deck.cards
            
            combat_manager.setup_combat(
                player_health=50,
                player_max_health=50,
                enemy_name="Test Enemy",
                enemy_health=30,
                enemy_max_health=30,
                player_cards=hand_cards
            )
            
            if combat_manager.player and combat_manager.enemy:
                results["tests"].append({"name": "Combat setup", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Combat setup", "status": "FAIL", "error": "Player or enemy not created"})
                results["failed"] += 1
            
            # Test effect types
            from sands_duat.core.cards import EffectType
            required_effects = ["DAMAGE", "HEAL", "BLOCK", "APPLY_VULNERABLE", "APPLY_WEAK", "APPLY_STRENGTH"]
            for effect in required_effects:
                if hasattr(EffectType, effect):
                    results["tests"].append({"name": f"Effect type {effect} exists", "status": "PASS"})
                    results["passed"] += 1
                else:
                    results["tests"].append({"name": f"Effect type {effect} exists", "status": "FAIL", "error": "Effect type missing"})
                    results["failed"] += 1
                    
        except Exception as e:
            results["tests"].append({"name": "Combat system test", "status": "ERROR", "error": str(e)})
            results["failed"] += 1
        
        return results
    
    def test_screen_transitions(self) -> Dict[str, Any]:
        """Test screen transition functionality."""
        results = {"name": "Screen Transitions", "tests": [], "passed": 0, "failed": 0}
        
        try:
            # Test all screens exist
            expected_screens = ["menu", "combat", "deck_builder", "tutorial", "progression"]
            for screen_name in expected_screens:
                screen = self.ui_manager.get_screen(screen_name)
                if screen:
                    results["tests"].append({"name": f"Screen '{screen_name}' exists", "status": "PASS"})
                    results["passed"] += 1
                else:
                    results["tests"].append({"name": f"Screen '{screen_name}' exists", "status": "FAIL", "error": "Screen not found"})
                    results["failed"] += 1
            
            # Test current screen
            if self.ui_manager.current_screen:
                results["tests"].append({"name": "Current screen accessible", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Current screen accessible", "status": "FAIL", "error": "No current screen"})
                results["failed"] += 1
                
        except Exception as e:
            results["tests"].append({"name": "Screen transitions test", "status": "ERROR", "error": str(e)})
            results["failed"] += 1
        
        return results
    
    def test_hourglass_system(self) -> Dict[str, Any]:
        """Test Hour-Glass Initiative system."""
        results = {"name": "Hour-Glass System", "tests": [], "passed": 0, "failed": 0}
        
        try:
            from sands_duat.core.hourglass import HourGlass
            
            # Test hourglass creation
            hourglass = HourGlass()
            results["tests"].append({"name": "HourGlass initialization", "status": "PASS"})
            results["passed"] += 1
            
            # Test sand operations
            hourglass.set_sand(3)
            if hourglass.current_sand == 3:
                results["tests"].append({"name": "Sand setting", "status": "PASS"})
                results["passed"] += 1
            else:
                results["tests"].append({"name": "Sand setting", "status": "FAIL", "error": f"Expected 3 sand, got {hourglass.current_sand}"})
                results["failed"] += 1
            
            # Test sand spending
            if hourglass.can_afford(2):
                if hourglass.spend_sand(2):
                    if hourglass.current_sand == 1:
                        results["tests"].append({"name": "Sand spending", "status": "PASS"})
                        results["passed"] += 1
                    else:
                        results["tests"].append({"name": "Sand spending", "status": "FAIL", "error": f"Expected 1 sand after spending 2, got {hourglass.current_sand}"})
                        results["failed"] += 1
                else:
                    results["tests"].append({"name": "Sand spending", "status": "FAIL", "error": "spend_sand returned False"})
                    results["failed"] += 1
            else:
                results["tests"].append({"name": "Sand affordability check", "status": "FAIL", "error": "can_afford returned False for affordable amount"})
                results["failed"] += 1
                
        except Exception as e:
            results["tests"].append({"name": "Hour-Glass system test", "status": "ERROR", "error": str(e)})
            results["failed"] += 1
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all system tests."""
        print("Starting comprehensive system test...")
        
        if not self.setup_test_environment():
            return {"error": "Failed to setup test environment"}
        
        # Run all test suites
        test_suites = [
            self.test_menu_functionality,
            self.test_card_system,
            self.test_combat_system,
            self.test_screen_transitions,
            self.test_hourglass_system
        ]
        
        all_results = []
        total_passed = 0
        total_failed = 0
        
        for test_suite in test_suites:
            try:
                results = test_suite()
                all_results.append(results)
                total_passed += results["passed"]
                total_failed += results["failed"]
                
                print(f"\n{results['name']}:")
                print(f"  Passed: {results['passed']}")
                print(f"  Failed: {results['failed']}")
                
                for test in results["tests"]:
                    status_symbol = "✓" if test["status"] == "PASS" else "✗" if test["status"] == "FAIL" else "⚠"
                    error_info = f" - {test.get('error', '')}" if test["status"] != "PASS" else ""
                    print(f"    {status_symbol} {test['name']}{error_info}")
                    
            except Exception as e:
                print(f"Error running test suite: {e}")
                total_failed += 1
        
        print(f"\n{'='*50}")
        print(f"TOTAL RESULTS:")
        print(f"  Passed: {total_passed}")
        print(f"  Failed: {total_failed}")
        print(f"  Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "N/A")
        
        return {
            "total_passed": total_passed,
            "total_failed": total_failed,
            "test_suites": all_results
        }

def main():
    """Main test runner function."""
    logging.basicConfig(level=logging.INFO)
    
    tester = SystemTester()
    results = tester.run_all_tests()
    
    pygame.quit()
    
    # Return exit code based on test results
    if results.get("total_failed", 1) == 0:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()