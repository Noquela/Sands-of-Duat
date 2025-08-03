#!/usr/bin/env python3
"""
MCP Comprehensive Test System for Sands of Duat

This script tests all game functionality using MCP tools and automated testing
without needing to manually launch the game repeatedly.
"""

import sys
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
import traceback

# Add the game directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class MCPTestSuite:
    """Comprehensive MCP-based testing system for all game functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results: Dict[str, Dict[str, Any]] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test_result(self, test_name: str, status: str, details: str = "", error: str = ""):
        """Log a test result."""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"[PASS] {test_name}: {status}")
        elif status == "FAIL":
            self.failed_tests += 1
            print(f"[FAIL] {test_name}: {status}")
            if details:
                print(f"   Details: {details}")
        else:  # ERROR
            self.failed_tests += 1
            print(f"[ERROR] {test_name}: {status}")
            if error:
                print(f"   Error: {error}")
        
        self.test_results[test_name] = {
            "status": status,
            "details": details,
            "error": error
        }
    
    def test_imports_and_modules(self):
        """Test all critical module imports."""
        print("\n[TEST] TESTING MODULE IMPORTS")
        print("=" * 50)
        
        critical_modules = [
            "sands_duat.core.cards",
            "sands_duat.core.hourglass", 
            "sands_duat.core.combat_manager",
            "sands_duat.core.player_collection",
            "sands_duat.ui.menu_screen",
            "sands_duat.ui.combat_screen",
            "sands_duat.ui.deck_builder",
            "sands_duat.content.egyptian_card_loader",
            "sands_duat.content.starter_cards",
            "sands_duat.audio.audio_manager"
        ]
        
        for module_name in critical_modules:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is None:
                    self.log_test_result(f"Import {module_name}", "FAIL", "Module not found")
                    continue
                    
                module = importlib.import_module(module_name)
                self.log_test_result(f"Import {module_name}", "PASS")
                
            except Exception as e:
                self.log_test_result(f"Import {module_name}", "ERROR", error=str(e))
    
    def test_card_system(self):
        """Test Egyptian card system and loading."""
        print("\n[TEST] TESTING CARD SYSTEM")
        print("=" * 50)
        
        try:
            # Test card library - first initialize cards
            from sands_duat.content.starter_cards import create_starter_cards
            from sands_duat.core.cards import card_library, Card, CardType, CardRarity, EffectType
            
            # Force card creation to populate library
            create_starter_cards()
            
            if hasattr(card_library, '_cards') and len(card_library._cards) > 0:
                self.log_test_result("Card Library Populated", "PASS", f"{len(card_library._cards)} cards loaded")
            else:
                self.log_test_result("Card Library Populated", "FAIL", "No cards in library")
            
            # Test Egyptian card loader
            from sands_duat.content.egyptian_card_loader import initialize_egyptian_cards
            egyptian_cards = initialize_egyptian_cards()
            
            if egyptian_cards and len(egyptian_cards) >= 19:
                self.log_test_result("Egyptian Cards Loading", "PASS", f"{len(egyptian_cards)} Egyptian cards loaded")
            else:
                self.log_test_result("Egyptian Cards Loading", "FAIL", f"Only {len(egyptian_cards) if egyptian_cards else 0} cards loaded")
            
            # Test starter deck
            from sands_duat.content.starter_cards import get_starter_deck
            starter_deck = get_starter_deck()
            
            if starter_deck and len(starter_deck) > 0:
                self.log_test_result("Starter Deck Creation", "PASS", f"{len(starter_deck)} cards in starter deck")
            else:
                self.log_test_result("Starter Deck Creation", "FAIL", "Empty starter deck")
            
            # Test card effects
            effect_types = ["DAMAGE", "HEAL", "BLOCK", "APPLY_VULNERABLE", "APPLY_WEAK", "APPLY_STRENGTH"]
            missing_effects = []
            for effect in effect_types:
                if not hasattr(EffectType, effect):
                    missing_effects.append(effect)
            
            if not missing_effects:
                self.log_test_result("Card Effect Types", "PASS", "All required effect types present")
            else:
                self.log_test_result("Card Effect Types", "FAIL", f"Missing: {missing_effects}")
                
        except Exception as e:
            self.log_test_result("Card System", "ERROR", error=str(e))
    
    def test_combat_system(self):
        """Test combat manager and battle mechanics."""
        print("\n[TEST] TESTING COMBAT SYSTEM")
        print("=" * 50)
        
        try:
            from sands_duat.core.combat_manager import CombatManager, CombatEntity
            from sands_duat.core.hourglass import HourGlass
            from sands_duat.content.starter_cards import get_starter_deck
            
            # Test combat manager initialization
            combat_manager = CombatManager()
            self.log_test_result("Combat Manager Init", "PASS")
            
            # Test combat setup
            deck = get_starter_deck()
            hand_cards = deck.cards[:5] if len(deck.cards) >= 5 else deck.cards
            
            combat_manager.setup_combat(
                player_health=50,
                player_max_health=50,
                enemy_name="Test Mummy",
                enemy_health=30,
                enemy_max_health=30,
                player_cards=hand_cards
            )
            
            if combat_manager.player and combat_manager.enemy:
                self.log_test_result("Combat Setup", "PASS", "Player and enemy created")
            else:
                self.log_test_result("Combat Setup", "FAIL", "Missing player or enemy")
            
            # Test card playing
            if hand_cards:
                test_card = hand_cards[0]
                initial_sand = combat_manager.player.hourglass.current_sand
                
                # Try to play a card
                card_played = combat_manager.play_card(test_card)
                
                if card_played:
                    self.log_test_result("Card Playing", "PASS", f"Card '{test_card.name}' played successfully")
                else:
                    self.log_test_result("Card Playing", "FAIL", "Card could not be played")
            
            # Test combat state
            combat_state = combat_manager.get_combat_state()
            if combat_state and "player" in combat_state and "enemy" in combat_state:
                self.log_test_result("Combat State", "PASS", "Combat state properly structured")
            else:
                self.log_test_result("Combat State", "FAIL", "Invalid combat state")
                
        except Exception as e:
            self.log_test_result("Combat System", "ERROR", error=str(e))
    
    def test_hourglass_system(self):
        """Test Hour-Glass Initiative system."""
        print("\n[TEST] TESTING HOUR-GLASS SYSTEM")
        print("=" * 50)
        
        try:
            from sands_duat.core.hourglass import HourGlass
            
            # Test hourglass creation
            hourglass = HourGlass()
            self.log_test_result("HourGlass Creation", "PASS")
            
            # Test sand operations
            hourglass.set_sand(5)
            if hourglass.current_sand == 5:
                self.log_test_result("Sand Setting", "PASS", f"Sand set to {hourglass.current_sand}")
            else:
                self.log_test_result("Sand Setting", "FAIL", f"Expected 5, got {hourglass.current_sand}")
            
            # Test sand spending
            if hourglass.can_afford(3):
                spent = hourglass.spend_sand(3)
                if spent and hourglass.current_sand == 2:
                    self.log_test_result("Sand Spending", "PASS", f"Sand spent correctly, remaining: {hourglass.current_sand}")
                else:
                    self.log_test_result("Sand Spending", "FAIL", f"Expected 2 sand, got {hourglass.current_sand}")
            else:
                self.log_test_result("Sand Affordability", "FAIL", "Cannot afford 3 sand when having 5")
            
            # Test sand regeneration timing
            if hasattr(hourglass, 'update_sand'):
                hourglass.update_sand()
                self.log_test_result("Sand Regeneration", "PASS", "Sand regeneration method exists")
            else:
                self.log_test_result("Sand Regeneration", "FAIL", "Missing update_sand method")
                
        except Exception as e:
            self.log_test_result("HourGlass System", "ERROR", error=str(e))
    
    def test_player_collection_system(self):
        """Test player collection and deck building."""
        print("\n[TEST] TESTING PLAYER COLLECTION")
        print("=" * 50)
        
        try:
            from sands_duat.core.player_collection import PlayerCollection
            from sands_duat.core.cards import card_library
            
            # Test player collection creation
            collection = PlayerCollection()
            self.log_test_result("PlayerCollection Creation", "PASS")
            
            # Debug: Check what cards are in library and collection
            from sands_duat.core.cards import card_library
            library_cards = list(card_library._cards.keys())
            collection_cards = list(collection.owned_cards.keys())
            
            # Test card discovery
            available_cards = collection.get_available_cards()
            if available_cards and len(available_cards) > 0:
                self.log_test_result("Available Cards", "PASS", f"{len(available_cards)} cards available")
            else:
                self.log_test_result("Available Cards", "FAIL", f"No available cards. Library has {len(library_cards)} cards, Collection has {len(collection_cards)} cards. First library card: {library_cards[0] if library_cards else 'None'}, First collection card: {collection_cards[0] if collection_cards else 'None'}")
            
            # Test filtering
            filtered_cards = collection.filter_cards(rarity=None, card_type=None)
            if filtered_cards is not None:
                self.log_test_result("Card Filtering", "PASS", f"{len(filtered_cards)} cards after filtering")
            else:
                self.log_test_result("Card Filtering", "FAIL", "Filtering returned None")
                
        except Exception as e:
            self.log_test_result("Player Collection", "ERROR", error=str(e))
    
    def test_ui_components(self):
        """Test UI component initialization."""
        print("\n[TEST] TESTING UI COMPONENTS")
        print("=" * 50)
        
        try:
            # Test theme system
            from sands_duat.ui.theme import initialize_theme, get_theme
            
            initialize_theme(1920, 1080)
            theme = get_theme()
            if theme:
                self.log_test_result("Theme System", "PASS", "Theme initialized successfully")
            else:
                self.log_test_result("Theme System", "FAIL", "Theme not initialized")
            
            # Test screen classes exist
            from sands_duat.ui.menu_screen import MenuScreen
            from sands_duat.ui.combat_screen import CombatScreen
            from sands_duat.ui.deck_builder import DeckBuilderScreen
            
            self.log_test_result("Screen Classes", "PASS", "All screen classes importable")
            
        except Exception as e:
            self.log_test_result("UI Components", "ERROR", error=str(e))
    
    def test_audio_system(self):
        """Test audio system functionality."""
        print("\n[TEST] TESTING AUDIO SYSTEM")
        print("=" * 50)
        
        try:
            from sands_duat.audio.audio_manager import AudioManager
            
            # Test audio manager creation
            audio_manager = AudioManager()
            self.log_test_result("Audio Manager Creation", "PASS")
            
            # Test sound effects
            if hasattr(audio_manager, 'sounds') and len(audio_manager.sounds) > 0:
                self.log_test_result("Sound Effects", "PASS", f"{len(audio_manager.sounds)} sound effects loaded")
            else:
                self.log_test_result("Sound Effects", "FAIL", "No sound effects loaded")
            
            # Test procedural generation
            if hasattr(audio_manager, '_create_procedural_sound'):
                self.log_test_result("Procedural Audio", "PASS", "Procedural audio generation available")
            else:
                self.log_test_result("Procedural Audio", "FAIL", "No procedural audio generation")
                
        except Exception as e:
            self.log_test_result("Audio System", "ERROR", error=str(e))
    
    def test_integration_points(self):
        """Test critical integration points between systems."""
        print("\n[TEST] TESTING SYSTEM INTEGRATION")
        print("=" * 50)
        
        try:
            # Test card library integration with player collection
            from sands_duat.core.cards import card_library
            from sands_duat.core.player_collection import PlayerCollection
            
            collection = PlayerCollection()
            
            # Test if cards can be retrieved from library
            if len(card_library._cards) > 0:
                first_card_id = list(card_library._cards.keys())[0]
                retrieved_card = card_library.get_card_by_id(first_card_id)
                
                if retrieved_card:
                    self.log_test_result("Card Library Integration", "PASS", "Cards retrievable from library")
                else:
                    self.log_test_result("Card Library Integration", "FAIL", "Cannot retrieve cards from library")
            
            # Test combat manager with card system
            from sands_duat.core.combat_manager import CombatManager
            from sands_duat.content.starter_cards import get_starter_deck
            
            combat_manager = CombatManager()
            deck = get_starter_deck()
            
            if deck and len(deck) > 0 and combat_manager:
                self.log_test_result("Combat-Card Integration", "PASS", "Combat manager can work with card deck")
            else:
                self.log_test_result("Combat-Card Integration", "FAIL", "Integration broken")
                
        except Exception as e:
            self.log_test_result("System Integration", "ERROR", error=str(e))
    
    def run_all_tests(self):
        """Run all test suites."""
        print("SANDS OF DUAT - COMPREHENSIVE MCP TEST SUITE")
        print("=" * 60)
        print("Testing all game functionality systematically...")
        
        # Run all test suites
        self.test_imports_and_modules()
        self.test_card_system()
        self.test_combat_system()
        self.test_hourglass_system()
        self.test_player_collection_system()
        self.test_ui_components()
        self.test_audio_system()
        self.test_integration_points()
        
        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"[PASS] Passed: {self.passed_tests}")
        print(f"[FAIL] Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\nFAILED TESTS REQUIRE ATTENTION:")
            for test_name, result in self.test_results.items():
                if result["status"] in ["FAIL", "ERROR"]:
                    print(f"   - {test_name}: {result.get('details', result.get('error', 'Unknown issue'))}")
        
        return self.failed_tests == 0

def main():
    """Main test runner."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    try:
        test_suite = MCPTestSuite()
        success = test_suite.run_all_tests()
        
        if success:
            print("\nALL TESTS PASSED! Game systems are working correctly.")
            sys.exit(0)
        else:
            print(f"\n{test_suite.failed_tests} TESTS FAILED. See details above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nCRITICAL ERROR in test suite: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()