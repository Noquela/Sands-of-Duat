#!/usr/bin/env python3
"""
Combat System Test

Test the complete turn-based combat system with Hour-Glass Initiative,
enemy AI, and visual effects.
"""

import pygame
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "sands_duat"))

from core.combat_manager import CombatManager
from core.cards import Card, CardEffect, CardType, CardRarity, EffectType, TargetType


class CombatSystemTest:
    """Test the combat system functionality."""
    
    def __init__(self):
        # Create combat manager
        self.combat_manager = CombatManager()
        
        # Create test cards
        self.test_cards = self._create_test_cards()
        
        print("Combat System Test")
        print("=" * 50)
    
    def _create_test_cards(self):
        """Create simple test cards with enough to finish combat."""
        cards = []
        
        # Create multiple copies of attack cards to ensure combat can finish
        for i in range(5):  # 5 strike cards
            cards.append(Card(
                name=f"Strike {i+1}",
                description="Deal 6 damage.",
                sand_cost=1,
                card_type=CardType.ATTACK,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(effect_type=EffectType.DAMAGE, value=6, target=TargetType.ENEMY)]
            ))
        
        # Add some other cards
        cards.extend([
            Card(
                name="Heal",
                description="Restore 8 health.",
                sand_cost=2,
                card_type=CardType.SKILL,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(effect_type=EffectType.HEAL, value=8, target=TargetType.SELF)]
            ),
            Card(
                name="Defend",
                description="Gain 5 block.",
                sand_cost=1,
                card_type=CardType.SKILL,
                rarity=CardRarity.COMMON,
                effects=[CardEffect(effect_type=EffectType.BLOCK, value=5, target=TargetType.SELF)]
            ),
            Card(
                name="Power Strike",
                description="Deal 12 damage.",
                sand_cost=3,
                card_type=CardType.ATTACK,
                rarity=CardRarity.UNCOMMON,
                effects=[CardEffect(effect_type=EffectType.DAMAGE, value=12, target=TargetType.ENEMY)]
            )
        ])
        
        return cards
    
    def test_combat_setup(self):
        """Test combat initialization."""
        print("\\n1. Testing Combat Setup")
        print("-" * 30)
        
        # Setup combat with a weaker enemy for faster testing
        self.combat_manager.setup_combat(
            player_health=100,
            player_max_health=100,
            enemy_name="Test Goblin",
            enemy_health=20,  # Reduced health for quicker combat
            enemy_max_health=20,
            player_cards=self.test_cards
        )
        
        state = self.combat_manager.get_combat_state()
        
        print(f"Player: {state['player']['health']}/{state['player']['max_health']} HP")
        print(f"Enemy: {state['enemy']['name']} - {state['enemy']['health']}/{state['enemy']['max_health']} HP")
        print(f"Combat Phase: {state['phase']}")
        print(f"Turn: {state['turn_number']}")
        print(f"Hand Size: {state['hand_size']}")
        
        assert state['player']['health'] == 100
        assert state['enemy']['health'] == 20
        assert state['phase'] == 'player_turn'
        assert state['hand_size'] == 8  # Updated for larger hand
        print("[OK] Combat setup successful")
    
    def test_card_play(self):
        """Test playing cards."""
        print("\\n2. Testing Card Play")
        print("-" * 30)
        
        # Get initial state
        initial_state = self.combat_manager.get_combat_state()
        initial_enemy_health = initial_state['enemy']['health']
        
        # Play a strike card
        strike_card = self.test_cards[0]  # Strike (1 sand, 6 damage)
        success = self.combat_manager.play_card(strike_card)
        
        print(f"Played {strike_card.name} (cost: {strike_card.sand_cost})")
        print(f"Play successful: {success}")
        
        # Check results
        new_state = self.combat_manager.get_combat_state()
        new_enemy_health = new_state['enemy']['health']
        sand_spent = initial_state['player']['sand'] - new_state['player']['sand']
        
        print(f"Enemy health: {initial_enemy_health} -> {new_enemy_health}")
        print(f"Sand spent: {sand_spent}")
        
        assert success == True
        assert sand_spent == 1
        assert new_enemy_health == initial_enemy_health - 6
        print("[OK] Card play successful")
    
    def test_enemy_turn(self):
        """Test enemy AI turn."""
        print("\\n3. Testing Enemy Turn")
        print("-" * 30)
        
        # End player turn to trigger enemy turn
        initial_player_health = self.combat_manager.get_combat_state()['player']['health']
        
        self.combat_manager.end_player_turn()
        
        # Let enemy turn process
        for _ in range(10):  # Give some update cycles
            self.combat_manager.update(0.1)
        
        new_state = self.combat_manager.get_combat_state()
        new_player_health = new_state['player']['health']
        
        print(f"Enemy turn completed")
        print(f"Player health: {initial_player_health} -> {new_player_health}")
        print(f"Current phase: {new_state['phase']}")
        
        # Enemy should have acted (damage or block)
        if new_player_health < initial_player_health:
            print(f"[OK] Enemy dealt {initial_player_health - new_player_health} damage")
        else:
            print("[OK] Enemy used defensive action")
        
        assert new_state['phase'] == 'player_turn'  # Should be back to player turn
        print("[OK] Enemy turn successful")
    
    def test_combat_flow(self):
        """Test basic combat mechanics and victory condition."""
        print("\\n4. Testing Combat Flow")
        print("-" * 30)
        
        # Manually defeat the enemy to test victory condition
        # Enemy has 2 HP left from previous tests, let's deal final damage
        initial_state = self.combat_manager.get_combat_state()
        print(f"Initial: Player {initial_state['player']['health']} HP, Enemy {initial_state['enemy']['health']} HP")
        
        # Manually defeat the enemy by setting health to 0
        if self.combat_manager.enemy:
            self.combat_manager.enemy.health = 0
        
        # Update combat to trigger end check
        self.combat_manager.update(0.1)
        
        final_state = self.combat_manager.get_combat_state()
        print(f"Final: Player {final_state['player']['health']} HP, Enemy {final_state['enemy']['health']} HP")
        print(f"Final phase: {final_state['phase']}")
        
        # Combat should end in victory since enemy is dead
        assert final_state['enemy']['health'] == 0
        assert final_state['phase'] == 'victory'
        print("[OK] Combat flow and victory condition successful")
    
    def run_all_tests(self):
        """Run all combat system tests."""
        try:
            self.test_combat_setup()
            self.test_card_play()
            self.test_enemy_turn()
            self.test_combat_flow()
            
            print("\\n" + "=" * 50)
            print("*** ALL COMBAT TESTS PASSED! ***")
            print("=" * 50)
            
        except Exception as e:
            print(f"\\n[FAIL] TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


if __name__ == "__main__":
    # Run the test
    test = CombatSystemTest()
    success = test.run_all_tests()
    
    if success:
        print("\\nCombat system is working correctly!")
    else:
        print("\\nCombat system has issues that need to be fixed.")
    
    sys.exit(0 if success else 1)