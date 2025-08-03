#!/usr/bin/env python3
"""
Comprehensive Card Effects System Test

Tests all card effect types used in the Egyptian cards YAML file
to verify proper implementation and identify any missing functionality.

Usage:
    python comprehensive_card_effects_test.py
"""

import sys
import os
import logging
from typing import Dict, List, Set, Any, Optional
from pathlib import Path

# Add the sands_duat package to the path
sys.path.insert(0, str(Path(__file__).parent / "sands_duat"))

try:
    from sands_duat.core.cards import Card, CardEffect, EffectType, TargetType, CardType, CardRarity
    from sands_duat.core.combat_manager import CombatManager, CombatEntity
    from sands_duat.core.hourglass import HourGlass
    from sands_duat.content.egyptian_card_loader import EgyptianCardLoader
    import yaml
except ImportError as e:
    print(f"Error importing sands_duat modules: {e}")
    print("Please ensure you're running this from the correct directory.")
    sys.exit(1)


class CardEffectsTestSuite:
    """Comprehensive test suite for card effect system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.combat_manager = CombatManager()
        self.loader = EgyptianCardLoader()
        
        # Track test results
        self.test_results: Dict[str, Dict[str, Any]] = {}
        self.missing_implementations: List[str] = []
        self.working_effects: List[str] = []
        self.broken_effects: List[str] = []
        
        # Load Egyptian cards
        self.egyptian_cards_file = Path("sands_duat/content/cards/egyptian_cards.yaml")
        self.egyptian_cards_data = self._load_egyptian_cards_yaml()
        
    def _load_egyptian_cards_yaml(self) -> Dict[str, Any]:
        """Load the Egyptian cards YAML file directly."""
        try:
            with open(self.egyptian_cards_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Failed to load Egyptian cards YAML: {e}")
            return {}
    
    def extract_all_effect_types_from_yaml(self) -> Set[str]:
        """Extract all unique effect types used in Egyptian cards."""
        effect_types = set()
        
        for card_id, card_data in self.egyptian_cards_data.items():
            if 'effects' in card_data:
                for effect in card_data['effects']:
                    if 'effect_type' in effect:
                        effect_types.add(effect['effect_type'])
        
        return effect_types
    
    def get_effect_type_coverage(self) -> Dict[str, List[str]]:
        """Get which cards use each effect type."""
        effect_usage = {}
        
        for card_id, card_data in self.egyptian_cards_data.items():
            if 'effects' in card_data:
                for effect in card_data['effects']:
                    effect_type = effect.get('effect_type')
                    if effect_type:
                        if effect_type not in effect_usage:
                            effect_usage[effect_type] = []
                        effect_usage[effect_type].append(card_id)
        
        return effect_usage
    
    def test_damage_effects(self) -> Dict[str, Any]:
        """Test DAMAGE effect implementation."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=100, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            # Create test damage effect
            damage_effect = CardEffect(
                effect_type=EffectType.DAMAGE,
                value=10,
                target=TargetType.ENEMY
            )
            
            # Apply effect
            initial_health = self.combat_manager.enemy.health
            self.combat_manager._apply_effect(damage_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_health = self.combat_manager.enemy.health
            
            # Verify damage was applied
            damage_dealt = initial_health - final_health
            if damage_dealt == 10:
                test_results["details"].append("Basic damage effect works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"Expected 10 damage, dealt {damage_dealt}")
            
            # Test with vulnerable
            self.combat_manager.enemy.debuffs["vulnerable"] = 2
            self.combat_manager.enemy.health = 50  # Reset health
            initial_health = self.combat_manager.enemy.health
            self.combat_manager._apply_effect(damage_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_health = self.combat_manager.enemy.health
            
            # Vulnerable should increase damage by 50%
            expected_damage = int(10 * 1.5)  # 15
            actual_damage = initial_health - final_health
            if actual_damage == expected_damage:
                test_results["details"].append("Vulnerable interaction works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"With vulnerable: expected {expected_damage} damage, dealt {actual_damage}")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during damage test: {e}")
        
        return test_results
    
    def test_heal_effects(self) -> Dict[str, Any]:
        """Test HEAL effect implementation."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=50, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            # Create test heal effect
            heal_effect = CardEffect(
                effect_type=EffectType.HEAL,
                value=20,
                target=TargetType.SELF
            )
            
            # Apply effect
            initial_health = self.combat_manager.player.health
            self.combat_manager._apply_effect(heal_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_health = self.combat_manager.player.health
            
            # Verify healing was applied
            healing_done = final_health - initial_health
            if healing_done == 20:
                test_results["details"].append("Basic heal effect works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"Expected 20 healing, healed {healing_done}")
            
            # Test max health cap
            self.combat_manager.player.health = 95  # Near max
            initial_health = self.combat_manager.player.health
            self.combat_manager._apply_effect(heal_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_health = self.combat_manager.player.health
            
            # Should cap at max health (100)
            if final_health == 100:
                test_results["details"].append("Heal capping at max health works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"Heal should cap at 100, got {final_health}")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during heal test: {e}")
        
        return test_results
    
    def test_block_effects(self) -> Dict[str, Any]:
        """Test BLOCK effect implementation."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=100, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            # Create test block effect
            block_effect = CardEffect(
                effect_type=EffectType.BLOCK,
                value=12,
                target=TargetType.SELF
            )
            
            # Apply effect
            initial_block = self.combat_manager.player.block
            self.combat_manager._apply_effect(block_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_block = self.combat_manager.player.block
            
            # Verify block was applied
            block_gained = final_block - initial_block
            if block_gained == 12:
                test_results["details"].append("Basic block effect works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"Expected 12 block, gained {block_gained}")
            
            # Test dexterity buff interaction
            self.combat_manager.player.buffs["dexterity"] = 3
            self.combat_manager.player.block = 0  # Reset block
            initial_block = self.combat_manager.player.block
            self.combat_manager._apply_effect(block_effect, self.combat_manager.player, self.combat_manager.enemy)
            final_block = self.combat_manager.player.block
            
            # Should get 12 + 3 = 15 block
            expected_block = 15
            if final_block == expected_block:
                test_results["details"].append("Dexterity buff interaction works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"With dexterity: expected {expected_block} block, got {final_block}")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during block test: {e}")
        
        return test_results
    
    def test_status_effects(self) -> Dict[str, Any]:
        """Test status effects (VULNERABLE, WEAK, STRENGTH, DEXTERITY)."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=100, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            # Test APPLY_VULNERABLE
            vulnerable_effect = CardEffect(
                effect_type=EffectType.APPLY_VULNERABLE,
                value=2,
                target=TargetType.ENEMY
            )
            self.combat_manager._apply_effect(vulnerable_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            if "vulnerable" in self.combat_manager.enemy.debuffs and self.combat_manager.enemy.debuffs["vulnerable"] == 2:
                test_results["details"].append("APPLY_VULNERABLE works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append("APPLY_VULNERABLE not working")
            
            # Test APPLY_WEAK
            weak_effect = CardEffect(
                effect_type=EffectType.APPLY_WEAK,
                value=2,
                target=TargetType.ENEMY
            )
            self.combat_manager._apply_effect(weak_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            if "weak" in self.combat_manager.enemy.debuffs and self.combat_manager.enemy.debuffs["weak"] == 2:
                test_results["details"].append("APPLY_WEAK works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append("APPLY_WEAK not working")
            
            # Test APPLY_STRENGTH
            strength_effect = CardEffect(
                effect_type=EffectType.APPLY_STRENGTH,
                value=3,
                target=TargetType.SELF
            )
            self.combat_manager._apply_effect(strength_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            if "strength" in self.combat_manager.player.buffs and self.combat_manager.player.buffs["strength"] == 3:
                test_results["details"].append("APPLY_STRENGTH works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append("APPLY_STRENGTH not working")
            
            # Test APPLY_DEXTERITY
            dexterity_effect = CardEffect(
                effect_type=EffectType.APPLY_DEXTERITY,
                value=2,
                target=TargetType.SELF
            )
            self.combat_manager._apply_effect(dexterity_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            if "dexterity" in self.combat_manager.player.buffs and self.combat_manager.player.buffs["dexterity"] == 2:
                test_results["details"].append("APPLY_DEXTERITY works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append("APPLY_DEXTERITY not working")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during status effects test: {e}")
        
        return test_results
    
    def test_sand_effects(self) -> Dict[str, Any]:
        """Test sand-related effects (GAIN_SAND, GAIN_ENERGY)."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=100, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            # Test GAIN_SAND
            initial_sand = self.combat_manager.player.hourglass.current_sand
            self.combat_manager.player.hourglass.set_sand(2)  # Set to known value
            
            gain_sand_effect = CardEffect(
                effect_type=EffectType.GAIN_SAND,
                value=2,
                target=TargetType.SELF
            )
            self.combat_manager._apply_effect(gain_sand_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            expected_sand = min(6, 2 + 2)  # Should be 4, capped at max
            actual_sand = self.combat_manager.player.hourglass.current_sand
            
            if actual_sand == expected_sand:
                test_results["details"].append("GAIN_SAND works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"GAIN_SAND: expected {expected_sand}, got {actual_sand}")
            
            # Test GAIN_ENERGY (alias for GAIN_SAND)
            self.combat_manager.player.hourglass.set_sand(1)  # Reset
            gain_energy_effect = CardEffect(
                effect_type=EffectType.GAIN_ENERGY,
                value=3,
                target=TargetType.SELF
            )
            self.combat_manager._apply_effect(gain_energy_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            expected_sand = min(6, 1 + 3)  # Should be 4
            actual_sand = self.combat_manager.player.hourglass.current_sand
            
            if actual_sand == expected_sand:
                test_results["details"].append("GAIN_ENERGY works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"GAIN_ENERGY: expected {expected_sand}, got {actual_sand}")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during sand effects test: {e}")
        
        return test_results
    
    def test_max_health_increase(self) -> Dict[str, Any]:
        """Test MAX_HEALTH_INCREASE effect."""
        test_results = {"passed": True, "details": [], "errors": []}
        
        try:
            # Setup test combat
            self.combat_manager.setup_combat(
                player_health=100, player_max_health=100,
                enemy_name="Test Enemy", enemy_health=50, enemy_max_health=50,
                player_cards=[]
            )
            
            initial_max_health = self.combat_manager.player.max_health
            initial_health = self.combat_manager.player.health
            
            max_health_effect = CardEffect(
                effect_type=EffectType.MAX_HEALTH_INCREASE,
                value=5,
                target=TargetType.SELF
            )
            self.combat_manager._apply_effect(max_health_effect, self.combat_manager.player, self.combat_manager.enemy)
            
            final_max_health = self.combat_manager.player.max_health
            final_health = self.combat_manager.player.health
            
            # Should increase both max health and current health
            if final_max_health == initial_max_health + 5 and final_health == initial_health + 5:
                test_results["details"].append("MAX_HEALTH_INCREASE works correctly")
            else:
                test_results["passed"] = False
                test_results["errors"].append(f"MAX_HEALTH_INCREASE failed: max {final_max_health}, current {final_health}")
            
        except Exception as e:
            test_results["passed"] = False
            test_results["errors"].append(f"Exception during max health test: {e}")
        
        return test_results
    
    def test_unimplemented_effects(self) -> Dict[str, Any]:
        """Test effects that are used in YAML but not implemented."""
        test_results = {"passed": True, "details": [], "missing": [], "errors": []}
        
        yaml_effects = self.extract_all_effect_types_from_yaml()
        
        # Map YAML effects to their expected EffectType
        effect_mapping = {
            'damage': EffectType.DAMAGE,
            'heal': EffectType.HEAL,
            'block': EffectType.BLOCK,
            'draw_cards': EffectType.DRAW_CARDS,
            'gain_sand': EffectType.GAIN_ENERGY,
            'apply_vulnerable': EffectType.APPLY_VULNERABLE,
            'apply_weak': EffectType.APPLY_WEAK,
            'apply_strength': EffectType.APPLY_STRENGTH,
            'apply_dexterity': EffectType.APPLY_DEXTERITY,
            'max_health_increase': EffectType.MAX_HEALTH_INCREASE
        }
        
        # Check for unimplemented effects
        unimplemented = [
            'permanent_sand_increase',
            'channel_divinity',
            'blessing',
            'discover_card',
            'gain_card',
            'lose_gold',
            'upgrade_card'
        ]
        
        for effect in yaml_effects:
            if effect in unimplemented:
                test_results["missing"].append(effect)
                test_results["details"].append(f"Effect '{effect}' is used in YAML but has no specific implementation")
            elif effect not in effect_mapping:
                test_results["missing"].append(effect)
                test_results["details"].append(f"Unknown effect '{effect}' found in YAML")
        
        if test_results["missing"]:
            test_results["passed"] = False
        
        return test_results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all tests and compile results."""
        print("Starting Comprehensive Card Effects System Test...")
        print("=" * 60)
        
        # Extract effect types from YAML
        yaml_effects = self.extract_all_effect_types_from_yaml()
        effect_usage = self.get_effect_type_coverage()
        
        print(f"Found {len(yaml_effects)} unique effect types in Egyptian cards:")
        for effect in sorted(yaml_effects):
            card_count = len(effect_usage.get(effect, []))
            print(f"  * {effect} (used in {card_count} cards)")
        print()
        
        # Run individual tests
        test_suite = {
            'damage_effects': self.test_damage_effects,
            'heal_effects': self.test_heal_effects,
            'block_effects': self.test_block_effects,
            'status_effects': self.test_status_effects,
            'sand_effects': self.test_sand_effects,
            'max_health_increase': self.test_max_health_increase,
            'unimplemented_effects': self.test_unimplemented_effects
        }
        
        results = {}
        for test_name, test_func in test_suite.items():
            print(f"Running {test_name.replace('_', ' ').title()}...")
            results[test_name] = test_func()
            
            if results[test_name]["passed"]:
                print(f"  [PASS] PASSED")
            else:
                print(f"  [FAIL] FAILED")
            
            for detail in results[test_name]["details"]:
                print(f"    * {detail}")
            
            for error in results[test_name].get("errors", []):
                print(f"    ! ERROR: {error}")
            
            if "missing" in results[test_name]:
                for missing in results[test_name]["missing"]:
                    print(f"    ! Missing: {missing}")
            print()
        
        # Summary
        passed_tests = sum(1 for r in results.values() if r["passed"])
        total_tests = len(results)
        
        print("Test Summary:")
        print(f"  Passed: {passed_tests}/{total_tests}")
        print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Categorize effects
        working_effects = [
            'damage', 'heal', 'block', 'draw_cards', 'gain_sand',
            'apply_vulnerable', 'apply_weak', 'apply_strength', 
            'apply_dexterity', 'max_health_increase'
        ]
        
        missing_effects = results['unimplemented_effects'].get('missing', [])
        
        print(f"\nWorking Effects ({len(working_effects)}):")
        for effect in working_effects:
            card_count = len(effect_usage.get(effect, []))
            print(f"  * {effect} (used in {card_count} cards)")
        
        if missing_effects:
            print(f"\nMissing/Incomplete Effects ({len(missing_effects)}):")
            for effect in missing_effects:
                card_count = len(effect_usage.get(effect, []))
                print(f"  * {effect} (used in {card_count} cards)")
        
        return {
            'yaml_effects': yaml_effects,
            'effect_usage': effect_usage,
            'test_results': results,
            'working_effects': working_effects,
            'missing_effects': missing_effects,
            'success_rate': (passed_tests/total_tests)*100
        }


def main():
    """Main test execution."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run comprehensive test
    test_suite = CardEffectsTestSuite()
    results = test_suite.run_comprehensive_test()
    
    # Export results to file
    results_file = Path("card_effects_test_results.json")
    import json
    
    # Convert sets to lists for JSON serialization
    serializable_results = {
        'yaml_effects': list(results['yaml_effects']),
        'effect_usage': results['effect_usage'],
        'working_effects': results['working_effects'],
        'missing_effects': results['missing_effects'],
        'success_rate': results['success_rate'],
        'test_summary': {
            name: {
                'passed': data['passed'],
                'details_count': len(data['details']),
                'errors_count': len(data.get('errors', [])),
                'missing_count': len(data.get('missing', []))
            }
            for name, data in results['test_results'].items()
        }
    }
    
    with open(results_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\nDetailed results exported to: {results_file}")
    
    return results['success_rate'] >= 70.0  # Return True if 70%+ success rate


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)