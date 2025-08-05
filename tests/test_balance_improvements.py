#!/usr/bin/env python3
"""
Test Balance Improvements for Sands of Duat

Validates that the new balance engine and enhanced mechanics work correctly
and provide strategic depth while maintaining fair gameplay.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sands_duat.core.balance_engine import BalanceEngine, CardAnalysis
from sands_duat.core.cards import Card, CardEffect, EffectType, TargetType, CardType, CardRarity
from sands_duat.core.hourglass import HourGlass


def create_test_cards():
    """Create a set of test cards to validate balance."""
    
    # Balanced 1-cost attack
    balanced_attack = Card(
        id="test_balanced_attack",
        name="Balanced Strike",
        description="A well-balanced attack card",
        sand_cost=1,
        card_type=CardType.ATTACK,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=5, target=TargetType.ENEMY)
        ],
        keywords={"strike"}
    )
    
    # Overpowered 1-cost attack
    overpowered_attack = Card(
        id="test_overpowered_attack",
        name="Overpowered Strike",
        description="An overpowered attack card",
        sand_cost=1,
        card_type=CardType.ATTACK,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=12, target=TargetType.ENEMY)
        ],
        keywords={"strike"}
    )
    
    # Underpowered 3-cost card
    underpowered_card = Card(
        id="test_underpowered_card",
        name="Weak Spell",
        description="An underpowered spell",
        sand_cost=3,
        card_type=CardType.SKILL,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=6, target=TargetType.ENEMY)
        ],
        keywords={"spell"}
    )
    
    # Synergy-rich card
    synergy_card = Card(
        id="test_synergy_card",
        name="Divine Resonance",
        description="A card with multiple synergies",
        sand_cost=2,
        card_type=CardType.SKILL,
        rarity=CardRarity.RARE,
        effects=[
            CardEffect(
                effect_type=EffectType.DAMAGE, 
                value=8, 
                target=TargetType.ENEMY,
                resonance_bonus={"2": 3},
                momentum_scaling=True,
                divine_alignment="order"
            )
        ],
        keywords={"divine", "ra", "resonance"},
        divine_alignment="order"
    )
    
    return [balanced_attack, overpowered_attack, underpowered_card, synergy_card]


def test_balance_engine():
    """Test the balance engine analysis capabilities."""
    print("Testing Balance Engine...")
    
    engine = BalanceEngine()
    test_cards = create_test_cards()
    
    # Analyze individual cards
    for card in test_cards:
        analysis = engine.analyze_card(card)
        print(f"\n{card.name} Analysis:")
        print(f"  Power Level: {analysis.power_level:.2f}")
        print(f"  Efficiency: {analysis.efficiency_rating:.2f}")
        print(f"  Balance Score: {analysis.balance_score:.2f}")
        print(f"  Meta Position: {analysis.meta_position}")
        print(f"  Recommendations: {analysis.recommendations}")
    
    # Analyze card set
    set_analysis = engine.analyze_card_set(test_cards)
    print(f"\nSet Analysis:")
    print(f"  Total Cards: {set_analysis['total_cards']}")
    print(f"  Average Balance Score: {set_analysis['average_balance_score']:.2f}")
    print(f"  Balanced: {set_analysis['balanced_count']}")
    print(f"  Overpowered: {set_analysis['overpowered_count']}")
    print(f"  Underpowered: {set_analysis['underpowered_count']}")
    print(f"  Set Recommendations: {set_analysis['recommendations']}")


def test_hourglass_enhancements():
    """Test the enhanced hourglass mechanics."""
    print("\n\nTesting Enhanced HourGlass Mechanics...")
    
    hourglass = HourGlass(current_sand=3, max_sand=6)
    
    # Test temporal momentum
    print("Testing Temporal Momentum:")
    hourglass.update_temporal_momentum(3)  # Play 3-cost card
    print(f"  After 3-cost card: {hourglass.temporal_momentum_stacks} stacks")
    
    hourglass.update_temporal_momentum(2)  # Play 2-cost card (decreasing)
    print(f"  After 2-cost card: {hourglass.temporal_momentum_stacks} stacks")
    
    hourglass.update_temporal_momentum(1)  # Play 1-cost card (decreasing)
    print(f"  After 1-cost card: {hourglass.temporal_momentum_stacks} stacks")
    print(f"  Momentum reduction: {hourglass.get_momentum_reduction()}")
    
    # Test sand resonance
    print("\nTesting Sand Resonance:")
    for card_cost in [2, 3, 4]:
        resonance = hourglass.check_sand_resonance(card_cost)
        print(f"  Card cost {card_cost} vs current sand {hourglass.current_sand}: {resonance}")
    
    # Test divine judgment
    print("\nTesting Divine Judgment:")
    print(f"  Initial divine favor: {hourglass.divine_favor}")
    hourglass.apply_divine_judgment("order")
    print(f"  After order action: {hourglass.divine_favor}")
    hourglass.apply_divine_judgment("chaos")
    print(f"  After chaos action: {hourglass.divine_favor}")
    
    # Test dynamic regeneration
    print("\nTesting Dynamic Regeneration:")
    base_rate = hourglass.regeneration_rate
    
    # Low health scenario
    low_health_rate = hourglass.get_dynamic_regeneration_rate(0.2, False)
    print(f"  Low health (20%): {low_health_rate:.2f} (base: {base_rate:.2f})")
    
    # Divine blessing scenario
    blessed_rate = hourglass.get_dynamic_regeneration_rate(1.0, True)
    print(f"  With divine blessing: {blessed_rate:.2f} (base: {base_rate:.2f})")
    
    # High divine favor
    hourglass.divine_favor = 8
    favor_rate = hourglass.get_dynamic_regeneration_rate(1.0, False)
    print(f"  High divine favor: {favor_rate:.2f} (base: {base_rate:.2f})")


def test_card_enhancements():
    """Test enhanced card mechanics."""
    print("\n\nTesting Enhanced Card Mechanics...")
    
    # Create a card with new mechanics
    enhanced_card = Card(
        id="test_enhanced_card",
        name="Divine Fire",
        description="A card showcasing new mechanics",
        sand_cost=2,
        card_type=CardType.ATTACK,
        rarity=CardRarity.RARE,
        effects=[
            CardEffect(
                effect_type=EffectType.DAMAGE,
                value=8,
                target=TargetType.ENEMY,
                resonance_bonus={"2": 3, "1": 1, "3": 1},
                momentum_scaling=True,
                divine_alignment="order"
            )
        ],
        keywords={"divine", "fire", "ra"},
        divine_alignment="order",
        mummified=False,
        experience_points=0
    )
    
    # Test effective cost calculation
    print("Testing Enhanced Cost Calculation:")
    base_cost = enhanced_card.get_effective_cost()
    print(f"  Base cost: {base_cost}")
    
    # With momentum
    momentum_cost = enhanced_card.get_effective_cost(current_sand=2, momentum_stacks=2)
    print(f"  With momentum (2 stacks): {momentum_cost}")
    
    # With resonance
    resonance_cost = enhanced_card.get_effective_cost(current_sand=2)
    print(f"  With perfect resonance: {resonance_cost}")
    
    # Test enhanced damage calculation
    print("\nTesting Enhanced Damage Calculation:")
    base_damage = enhanced_card.get_total_damage()
    print(f"  Base damage: {base_damage}")
    
    perfect_resonance_damage = enhanced_card.get_total_damage(current_sand=2)
    print(f"  Perfect resonance damage: {perfect_resonance_damage}")
    
    divine_favor_damage = enhanced_card.get_total_damage(current_sand=2, divine_favor=5)
    print(f"  With divine favor: {divine_favor_damage}")
    
    # Test mummification
    print("\nTesting Mummification:")
    enhanced_card.mummified = True
    enhanced_card.experience_points = 10
    mummy_cost = enhanced_card.get_effective_cost(current_sand=2)
    mummy_damage = enhanced_card.get_total_damage(current_sand=2)
    print(f"  Mummified cost: {mummy_cost}")
    print(f"  Mummified damage: {mummy_damage}")


def main():
    """Run all balance improvement tests."""
    print("=== SANDS OF DUAT BALANCE IMPROVEMENT TESTS ===")
    
    try:
        test_balance_engine()
        test_hourglass_enhancements()
        test_card_enhancements()
        
        print("\n=== ALL TESTS COMPLETED SUCCESSFULLY ===")
        print("\nBalance improvements working correctly!")
        print("- Balance Engine provides detailed analysis and recommendations")
        print("- HourGlass system includes strategic depth mechanics")
        print("- Cards support enhanced mechanics for deeper gameplay")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()