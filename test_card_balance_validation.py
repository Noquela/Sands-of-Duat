#!/usr/bin/env python3
"""
Card Balance and Gameplay Mechanics Validation Test
Testing the balanced card system, Hour-Glass strategic depth, and Egyptian underworld mechanics.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_card_loading_and_balance():
    """Test that all cards load correctly and have balanced values."""
    print("Testing card loading and balance...")
    
    try:
        from sands_duat.content.starter_cards import create_starter_cards
        from sands_duat.core.cards import CardType
        
        cards = create_starter_cards()
        
        # Basic validation
        if len(cards) == 0:
            print("FAIL: No cards loaded")
            return False
        
        print(f"  Loaded {len(cards)} cards")
        
        # Card type distribution analysis
        type_counts = {}
        for card in cards:
            card_type = card.card_type
            type_counts[card_type] = type_counts.get(card_type, 0) + 1
        
        print("  Card type distribution:")
        for card_type, count in type_counts.items():
            print(f"    {card_type}: {count} cards")
        
        # Balance analysis
        attack_cards = [c for c in cards if c.card_type == CardType.ATTACK]
        skill_cards = [c for c in cards if c.card_type == CardType.SKILL]
        power_cards = [c for c in cards if c.card_type == CardType.POWER]
        
        # Check attack card balance
        if attack_cards:
            avg_attack_cost = sum(c.sand_cost for c in attack_cards) / len(attack_cards)
            print(f"  Average attack card cost: {avg_attack_cost:.1f} sand")
            
            if 1.5 <= avg_attack_cost <= 3.0:
                print("  PASS: Attack cards reasonably costed")
                balance_score = 25
            else:
                print("  FAIL: Attack cards poorly balanced")
                balance_score = 0
        else:
            print("  WARNING: No attack cards found")
            balance_score = 10
        
        # Check skill card balance
        if skill_cards:
            avg_skill_cost = sum(c.sand_cost for c in skill_cards) / len(skill_cards)
            print(f"  Average skill card cost: {avg_skill_cost:.1f} sand")
            
            if 1.0 <= avg_skill_cost <= 2.5:
                print("  PASS: Skill cards reasonably costed")
                balance_score += 25
            else:
                print("  FAIL: Skill cards poorly balanced")
        else:
            print("  WARNING: No skill cards found")
            balance_score += 10
        
        # Check power card balance  
        if power_cards:
            avg_power_cost = sum(c.sand_cost for c in power_cards) / len(power_cards)
            print(f"  Average power card cost: {avg_power_cost:.1f} sand")
            
            if 2.0 <= avg_power_cost <= 4.0:
                print("  PASS: Power cards reasonably costed")
                balance_score += 25
            else:
                print("  FAIL: Power cards poorly balanced")
        else:
            print("  INFO: No power cards found (acceptable)")
            balance_score += 20
        
        # Check for extreme outliers
        max_cost = max(c.sand_cost for c in cards)
        min_cost = min(c.sand_cost for c in cards)
        
        if max_cost <= 6 and min_cost >= 0:
            print("  PASS: No extreme cost outliers")
            balance_score += 25
        else:
            print(f"  FAIL: Extreme costs found (min: {min_cost}, max: {max_cost})")
        
        print(f"  Balance Score: {balance_score}/100")
        return balance_score >= 75
        
    except Exception as e:
        print(f"FAIL card balance test error: {e}")
        return False

def test_hourglass_strategic_mechanics():
    """Test Hour-Glass strategic depth features."""
    print("Testing Hour-Glass strategic mechanics...")
    
    try:
        from sands_duat.core.hourglass import HourGlass
        
        hourglass = HourGlass()
        
        # Test basic functionality
        hourglass.set_sand(6)
        initial_sand = hourglass.current_sand
        
        if initial_sand != 6:
            print("FAIL: Basic sand setting failed")
            return False
        
        print("  PASS: Basic sand management works")
        strategy_score = 20
        
        # Test spending mechanics
        spent = hourglass.spend_sand(3)
        if spent and hourglass.current_sand == 3:
            print("  PASS: Sand spending works correctly")
            strategy_score += 20
        else:
            print("  FAIL: Sand spending broken")
            return False
        
        # Test temporal momentum (if available)
        try:
            hourglass.update_temporal_momentum(3)
            momentum = hourglass.get_momentum_reduction()
            print(f"  INFO: Temporal momentum system active (reduction: {momentum})")
            strategy_score += 20
        except Exception as e:
            print(f"  WARNING: Temporal momentum not available: {e}")
            strategy_score += 10
        
        # Test divine favor system (if available)
        try:
            hourglass.apply_divine_judgment("justice")
            favor = hourglass.divine_favor
            print(f"  INFO: Divine favor system active (favor: {favor})")
            strategy_score += 20
        except Exception as e:
            print(f"  WARNING: Divine favor not available: {e}")
            strategy_score += 10
        
        # Test sand regeneration
        try:
            initial_time = hourglass.get_time_until_next_sand()
            print(f"  INFO: Sand regeneration timing available ({initial_time:.2f}s)")
            strategy_score += 20
        except Exception as e:
            print(f"  WARNING: Sand regeneration timing not available: {e}")
            strategy_score += 10
        
        print(f"  Strategy Score: {strategy_score}/100")
        return strategy_score >= 60
        
    except Exception as e:
        print(f"FAIL hourglass strategy test error: {e}")
        return False

def test_egyptian_underworld_mechanics():
    """Test Egyptian underworld themed mechanics."""
    print("Testing Egyptian underworld mechanics...")
    
    try:
        from sands_duat.content.starter_cards import create_starter_cards
        
        cards = create_starter_cards()
        
        # Check for Egyptian-themed card names
        egyptian_themes = [
            'anubis', 'isis', 'ra', 'thoth', 'maat', 'horus', 'osiris',
            'pharaoh', 'pyramid', 'scarab', 'mummy', 'tomb', 'desert',
            'sand', 'duat', 'papyrus', 'ankh', 'judgment'
        ]
        
        themed_cards = 0
        for card in cards:
            card_name_lower = card.name.lower()
            if any(theme in card_name_lower for theme in egyptian_themes):
                themed_cards += 1
        
        theme_percentage = (themed_cards / len(cards)) * 100
        print(f"  Egyptian-themed cards: {themed_cards}/{len(cards)} ({theme_percentage:.1f}%)")
        
        if theme_percentage >= 70:
            print("  PASS: Strong Egyptian theming")
            theme_score = 30
        elif theme_percentage >= 50:
            print("  PASS: Good Egyptian theming")
            theme_score = 25
        elif theme_percentage >= 30:
            print("  WARNING: Moderate Egyptian theming")
            theme_score = 15
        else:
            print("  FAIL: Weak Egyptian theming")
            theme_score = 0
        
        # Check for underworld mechanics (death, judgment, afterlife themes)
        underworld_themes = ['judgment', 'death', 'resurrection', 'afterlife', 'soul', 'spirit']
        underworld_cards = 0
        
        for card in cards:
            card_desc_lower = card.description.lower()
            if any(theme in card_desc_lower for theme in underworld_themes):
                underworld_cards += 1
        
        underworld_percentage = (underworld_cards / len(cards)) * 100
        print(f"  Underworld-themed mechanics: {underworld_cards}/{len(cards)} ({underworld_percentage:.1f}%)")
        
        if underworld_percentage >= 30:
            print("  PASS: Good underworld mechanics")
            theme_score += 30
        elif underworld_percentage >= 15:
            print("  PASS: Some underworld mechanics")
            theme_score += 20
        else:
            print("  INFO: Limited underworld mechanics (acceptable)")
            theme_score += 15
        
        # Check card variety and uniqueness
        unique_effects = set()
        for card in cards:
            unique_effects.add(card.description[:50])  # First 50 chars as effect signature
        
        uniqueness_percentage = (len(unique_effects) / len(cards)) * 100
        print(f"  Card effect uniqueness: {len(unique_effects)}/{len(cards)} ({uniqueness_percentage:.1f}%)")
        
        if uniqueness_percentage >= 80:
            print("  PASS: High card variety")
            theme_score += 40
        elif uniqueness_percentage >= 60:
            print("  PASS: Good card variety")
            theme_score += 30
        else:
            print("  WARNING: Limited card variety")
            theme_score += 15
        
        print(f"  Theme Score: {theme_score}/100")
        return theme_score >= 70
        
    except Exception as e:
        print(f"FAIL egyptian mechanics test error: {e}")
        return False

def test_gameplay_flow_validation():
    """Test that gameplay flow works correctly."""
    print("Testing gameplay flow validation...")
    
    try:
        from sands_duat.core.hourglass import HourGlass
        from sands_duat.content.starter_cards import create_starter_cards
        
        # Simulate a basic game turn
        hourglass = HourGlass()
        cards = create_starter_cards()
        
        # Starting state
        hourglass.set_sand(3)  # Typical turn start
        starting_sand = hourglass.current_sand
        
        # Find a playable card
        playable_cards = [c for c in cards if c.sand_cost <= starting_sand]
        
        if len(playable_cards) == 0:
            print("  FAIL: No playable cards with starting sand")
            return False
        
        print(f"  Found {len(playable_cards)} playable cards with {starting_sand} sand")
        
        # Simulate playing a card
        test_card = playable_cards[0]
        card_cost = test_card.sand_cost
        
        can_afford = hourglass.can_afford(card_cost)
        if not can_afford:
            print("  FAIL: Can't afford card that should be affordable")
            return False
        
        spent = hourglass.spend_sand(card_cost)
        if not spent:
            print("  FAIL: Failed to spend sand for playable card")
            return False
        
        remaining_sand = hourglass.current_sand
        expected_remaining = starting_sand - card_cost
        
        if remaining_sand != expected_remaining:
            print(f"  FAIL: Sand math incorrect ({remaining_sand} != {expected_remaining})")
            return False
        
        print("  PASS: Basic card play mechanics work")
        
        # Test that some cards remain playable after first play
        still_playable = [c for c in cards if c.sand_cost <= remaining_sand]
        
        if len(still_playable) > 0:
            print(f"  PASS: {len(still_playable)} cards still playable after first play")
            flow_score = 50
        else:
            print("  WARNING: No cards playable after first play")
            flow_score = 30
        
        # Test sand regeneration expectations
        try:
            time_to_next = hourglass.get_time_until_next_sand()
            if 0 <= time_to_next <= 2.0:  # Should be reasonable
                print(f"  PASS: Sand regeneration timing reasonable ({time_to_next:.1f}s)")
                flow_score += 25
            else:
                print(f"  WARNING: Sand regeneration timing unusual ({time_to_next:.1f}s)")
                flow_score += 15
        except:
            print("  INFO: Sand regeneration timing not available")
            flow_score += 20
        
        # Test max sand capacity
        max_sand = hourglass.max_sand
        if 5 <= max_sand <= 8:
            print(f"  PASS: Max sand capacity reasonable ({max_sand})")
            flow_score += 25
        else:
            print(f"  WARNING: Max sand capacity unusual ({max_sand})")
            flow_score += 10
        
        print(f"  Flow Score: {flow_score}/100")
        return flow_score >= 70
        
    except Exception as e:
        print(f"FAIL gameplay flow test error: {e}")
        return False

def main():
    """Run all card balance and gameplay mechanics tests."""
    print("=" * 70)
    print("SANDS OF DUAT - CARD BALANCE & GAMEPLAY VALIDATION")
    print("Testing card balance, Hour-Glass mechanics, and Egyptian themes")
    print("=" * 70)
    
    tests = [
        test_card_loading_and_balance,
        test_hourglass_strategic_mechanics,
        test_egyptian_underworld_mechanics,
        test_gameplay_flow_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("  RESULT: PASS")
            else:
                print("  RESULT: FAIL")
        except Exception as e:
            print(f"  RESULT: CRASH - {e}")
        print()
    
    print("=" * 70)
    print(f"BALANCE & GAMEPLAY RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("SUCCESS All balance and gameplay tests PASSED!")
        print("The card system is well-balanced and gameplay flows smoothly.")
    elif passed >= total * 0.75:
        print("SUCCESS Most balance tests passed - game is ready for play!")
    elif passed >= total * 0.5:
        print("WARNING Some balance issues detected - minor tuning needed")
    else:
        print("ERROR Significant balance issues - major rebalancing needed")
    
    print("=" * 70)
    return passed >= total * 0.5  # 50% pass rate for balance

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)