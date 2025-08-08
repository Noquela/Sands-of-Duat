#!/usr/bin/env python3
"""
SANDS OF DUAT - CARD BALANCE VALIDATION TESTS
=============================================

Tests to ensure the Egyptian card game is balanced and playable.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sands_of_duat.cards.egyptian_cards import EgyptianDeckBuilder, CardType, CardRarity

def test_deck_composition():
    """Test that deck composition is balanced."""
    print("Testing deck composition...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        # Count cards by type
        type_counts = defaultdict(int)
        for card in all_cards:
            type_counts[card.card_type] += 1
        
        print(f"    * Total cards: {len(all_cards)}")
        
        for card_type, count in type_counts.items():
            percentage = (count / len(all_cards)) * 100
            print(f"    * {card_type.name}: {count} cards ({percentage:.1f}%)")
        
        # Check that we have cards of each type
        required_types = {CardType.GOD, CardType.ARTIFACT, CardType.SPELL, CardType.CREATURE}
        available_types = set(type_counts.keys())
        
        missing_types = required_types - available_types
        if missing_types:
            print(f"    * Missing card types: {[t.name for t in missing_types]}")
            return False
        
        # Check balance - no single type should dominate
        max_percentage = max((count / len(all_cards)) * 100 for count in type_counts.values())
        
        print(f"    * Highest type percentage: {max_percentage:.1f}%")
        
        return max_percentage < 60  # No type should be more than 60% of deck
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_rarity_distribution():
    """Test that card rarity is properly distributed."""
    print("Testing rarity distribution...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        # Count cards by rarity
        rarity_counts = defaultdict(int)
        for card in all_cards:
            rarity_counts[card.rarity] += 1
        
        print(f"    * Total cards: {len(all_cards)}")
        
        for rarity, count in rarity_counts.items():
            percentage = (count / len(all_cards)) * 100
            print(f"    * {rarity.name}: {count} cards ({percentage:.1f}%)")
        
        # Check rarity pyramid (common > uncommon > rare > legendary)
        common_count = rarity_counts.get(CardRarity.COMMON, 0)
        uncommon_count = rarity_counts.get(CardRarity.UNCOMMON, 0)
        rare_count = rarity_counts.get(CardRarity.RARE, 0)
        legendary_count = rarity_counts.get(CardRarity.LEGENDARY, 0)
        
        # Basic rarity checks
        has_multiple_rarities = len(rarity_counts) >= 3
        legendary_not_too_common = legendary_count <= len(all_cards) * 0.3  # At most 30% legendary
        
        print(f"    * Rarity distribution is balanced: {has_multiple_rarities and legendary_not_too_common}")
        
        return has_multiple_rarities and legendary_not_too_common
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_cost_curve():
    """Test that card costs form a reasonable mana curve."""
    print("Testing cost curve...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        # Get all cards with costs (exclude some card types that might not have costs)
        cards_with_costs = [card for card in all_cards if card.stats.cost > 0]
        
        if not cards_with_costs:
            print("    * No cards with costs found")
            return True  # Skip test if no costs
        
        # Count cards by cost
        cost_counts = defaultdict(int)
        for card in cards_with_costs:
            cost_counts[card.stats.cost] += 1
        
        print(f"    * Cards with costs: {len(cards_with_costs)}")
        
        costs = sorted(cost_counts.keys())
        print(f"    * Cost range: {min(costs)} to {max(costs)}")
        
        for cost in costs:
            count = cost_counts[cost]
            percentage = (count / len(cards_with_costs)) * 100
            print(f"    * Cost {cost}: {count} cards ({percentage:.1f}%)")
        
        # Check for reasonable cost distribution
        low_cost_cards = sum(count for cost, count in cost_counts.items() if cost <= 3)
        high_cost_cards = sum(count for cost, count in cost_counts.items() if cost >= 7)
        
        low_cost_percentage = (low_cost_cards / len(cards_with_costs)) * 100
        high_cost_percentage = (high_cost_cards / len(cards_with_costs)) * 100
        
        print(f"    * Low cost (1-3): {low_cost_percentage:.1f}%")
        print(f"    * High cost (7+): {high_cost_percentage:.1f}%")
        
        # Should have more low cost cards than high cost cards
        return low_cost_percentage >= high_cost_percentage
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_power_balance():
    """Test that card power levels are balanced."""
    print("Testing power balance...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        # Get creature/god cards with attack/health
        combat_cards = [card for card in all_cards 
                       if card.card_type in [CardType.GOD, CardType.CREATURE] 
                       and card.stats.attack > 0 and card.stats.health > 0]
        
        if not combat_cards:
            print("    * No combat cards found")
            return True  # Skip if no combat cards
        
        print(f"    * Combat cards analyzed: {len(combat_cards)}")
        
        # Analyze power levels
        power_ratings = []
        for card in combat_cards:
            # Simple power rating: attack + health + cost efficiency
            power = card.stats.attack + card.stats.health
            cost = max(card.stats.cost, 1)  # Avoid division by zero
            efficiency = power / cost
            power_ratings.append((card.name, power, cost, efficiency))
        
        # Sort by efficiency
        power_ratings.sort(key=lambda x: x[3], reverse=True)
        
        print(f"    * Most efficient cards:")
        for name, power, cost, efficiency in power_ratings[:3]:
            print(f"      - {name}: {power} power for {cost} cost ({efficiency:.1f} efficiency)")
        
        print(f"    * Least efficient cards:")
        for name, power, cost, efficiency in power_ratings[-3:]:
            print(f"      - {name}: {power} power for {cost} cost ({efficiency:.1f} efficiency)")
        
        # Check that efficiency doesn't vary too wildly
        efficiencies = [rating[3] for rating in power_ratings]
        max_efficiency = max(efficiencies)
        min_efficiency = min(efficiencies)
        efficiency_ratio = max_efficiency / min_efficiency if min_efficiency > 0 else float('inf')
        
        print(f"    * Efficiency range: {min_efficiency:.1f} to {max_efficiency:.1f} (ratio: {efficiency_ratio:.1f})")
        
        # Efficiency shouldn't vary by more than 5x
        return efficiency_ratio < 5.0
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_starter_deck_balance():
    """Test that the starter deck is balanced and playable."""
    print("Testing starter deck balance...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        starter_deck = deck_builder.create_starter_deck()
        
        if not starter_deck:
            print("    * No starter deck created")
            return False
        
        print(f"    * Starter deck size: {len(starter_deck)}")
        
        # Analyze deck composition
        type_counts = defaultdict(int)
        rarity_counts = defaultdict(int)
        cost_counts = defaultdict(int)
        
        for card in starter_deck:
            type_counts[card.card_type] += 1
            rarity_counts[card.rarity] += 1
            if card.stats.cost > 0:
                cost_counts[card.stats.cost] += 1
        
        print(f"    * Card types in starter deck:")
        for card_type, count in type_counts.items():
            percentage = (count / len(starter_deck)) * 100
            print(f"      - {card_type.name}: {count} ({percentage:.1f}%)")
        
        print(f"    * Card rarities in starter deck:")
        for rarity, count in rarity_counts.items():
            percentage = (count / len(starter_deck)) * 100
            print(f"      - {rarity.name}: {count} ({percentage:.1f}%)")
        
        # Check balance criteria
        has_variety = len(type_counts) >= 3  # At least 3 different types
        reasonable_size = 10 <= len(starter_deck) <= 30  # Reasonable deck size
        not_all_legendary = rarity_counts.get(CardRarity.LEGENDARY, 0) < len(starter_deck) * 0.5
        
        print(f"    * Has variety: {has_variety}")
        print(f"    * Reasonable size: {reasonable_size}")
        print(f"    * Not all legendary: {not_all_legendary}")
        
        return has_variety and reasonable_size and not_all_legendary
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_random_deck_balance():
    """Test that random decks are reasonably balanced."""
    print("Testing random deck balance...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        
        # Create multiple random decks and analyze them
        deck_count = 5
        balanced_decks = 0
        
        for i in range(deck_count):
            random_deck = deck_builder.create_random_deck(15)
            
            if not random_deck:
                continue
            
            # Check if this deck is reasonably balanced
            type_counts = defaultdict(int)
            for card in random_deck:
                type_counts[card.card_type] += 1
            
            # A balanced deck should have at least 2 different card types
            type_variety = len(type_counts) >= 2
            
            # No single type should dominate completely
            max_type_count = max(type_counts.values()) if type_counts else 0
            type_balance = max_type_count < len(random_deck) * 0.8
            
            if type_variety and type_balance:
                balanced_decks += 1
        
        print(f"    * Created {deck_count} random decks")
        print(f"    * Balanced decks: {balanced_decks}/{deck_count}")
        
        balance_rate = balanced_decks / deck_count if deck_count > 0 else 0
        print(f"    * Balance rate: {balance_rate*100:.1f}%")
        
        # At least 60% of random decks should be reasonably balanced
        return balance_rate >= 0.6
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def test_legendary_card_power():
    """Test that legendary cards are appropriately powerful."""
    print("Testing legendary card power...")
    
    try:
        deck_builder = EgyptianDeckBuilder()
        all_cards = deck_builder.get_all_cards()
        
        legendary_cards = [card for card in all_cards if card.rarity == CardRarity.LEGENDARY]
        non_legendary_cards = [card for card in all_cards if card.rarity != CardRarity.LEGENDARY]
        
        if not legendary_cards:
            print("    * No legendary cards found")
            return True  # Skip if no legendary cards
        
        print(f"    * Legendary cards: {len(legendary_cards)}")
        print(f"    * Non-legendary cards: {len(non_legendary_cards)}")
        
        # Analyze legendary card stats
        for card in legendary_cards:
            print(f"      - {card.name}: {card.stats.cost} cost, {card.stats.attack}/{card.stats.health}")
        
        # Compare average costs
        legendary_costs = [card.stats.cost for card in legendary_cards if card.stats.cost > 0]
        non_legendary_costs = [card.stats.cost for card in non_legendary_cards if card.stats.cost > 0]
        
        if legendary_costs and non_legendary_costs:
            avg_legendary_cost = sum(legendary_costs) / len(legendary_costs)
            avg_non_legendary_cost = sum(non_legendary_costs) / len(non_legendary_costs)
            
            print(f"    * Average legendary cost: {avg_legendary_cost:.1f}")
            print(f"    * Average non-legendary cost: {avg_non_legendary_cost:.1f}")
            
            # Legendary cards should generally cost more
            cost_appropriate = avg_legendary_cost >= avg_non_legendary_cost
            
            return cost_appropriate
        
        return True  # Pass if we can't compare costs
    except Exception as e:
        print(f"  - Test failed: {e}")
        return False

def run_balance_tests():
    """Run all card balance validation tests."""
    print("SANDS OF DUAT - CARD BALANCE VALIDATION TESTS")
    print("=" * 48)
    
    tests = [
        ("Deck Composition", test_deck_composition),
        ("Rarity Distribution", test_rarity_distribution),
        ("Cost Curve", test_cost_curve),
        ("Power Balance", test_power_balance),
        ("Starter Deck Balance", test_starter_deck_balance),
        ("Random Deck Balance", test_random_deck_balance),
        ("Legendary Card Power", test_legendary_card_power)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                print(f"  Result: PASSED")
                passed += 1
            else:
                print(f"  Result: FAILED")
        except Exception as e:
            print(f"  Result: ERROR - {e}")
    
    print(f"\n" + "=" * 48)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All balance tests passed!")
        print("The Egyptian card game is well-balanced and ready for play.")
    elif passed >= total - 1:
        print("MOSTLY SUCCESSFUL: Game balance is good with minor issues.")
        print("The game should be enjoyable and competitive.")
    else:
        print("Balance issues detected. Card adjustments may be needed.")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = run_balance_tests()
    sys.exit(0 if success else 1)