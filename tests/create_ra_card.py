#!/usr/bin/env python3
"""
Demonstration of the complete Egyptian card system.
Shows Ra card creation, Ba-Ka system, and card database functionality.
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from sands_of_duat.cards import (
    get_card_database, 
    get_all_cards, 
    get_god_card_by_id,
    CardElement,
    CardRarity,
    BaKaSystem
)


def demonstrate_ra_card():
    """Demonstrate Ra card with full Egyptian mythology implementation."""
    print("=" * 60)
    print("SANDS OF DUAT - EGYPTIAN CARD SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Get Ra card
    ra_card = get_god_card_by_id("god_ra_01")
    if not ra_card:
        print("ERROR: Could not load Ra card!")
        return
    
    print(f"\n[SUN] {ra_card.name}")
    print("-" * 40)
    print(f"Type: {ra_card.card_type.value.title()}")
    print(f"Rarity: {ra_card.rarity.value.title()}")
    print(f"Element: {ra_card.element.value.title()}")
    print(f"\nStats:")
    print(f"  Attack: {ra_card.stats.attack}")
    print(f"  Defense: {ra_card.stats.defense}")
    print(f"  Health: {ra_card.stats.health}")
    print(f"  Mana Cost: {ra_card.stats.mana_cost}")
    print(f"  Sand Cost: {ra_card.stats.sand_cost}")
    print(f"  Ba Power: {ra_card.stats.ba_power}")
    print(f"  Ka Power: {ra_card.stats.ka_power}")
    
    print(f"\nKeywords:")
    for keyword in ra_card.keywords:
        print(f"  • {keyword.value.replace('_', ' ').title()}")
    
    print(f"\nAbilities:")
    for i, effect in enumerate(ra_card.effects, 1):
        print(f"  {i}. {effect.name}")
        print(f"     {effect.description}")
        if effect.ba_ka_interaction:
            print(f"     Ba-Ka Effect: {effect.ba_ka_interaction}")
    
    print(f"\nDescription:")
    print(f"  {ra_card.description}")
    
    print(f"\nFlavor Text:")
    print(f"  {ra_card.flavor_text}")
    
    print(f"\nMythology Source: {ra_card.mythology_source}")
    print(f"Asset: {ra_card.image_path.name} (Quality: {ra_card.image_quality})")
    
    # Demonstrate Ba-Ka system
    print(f"\n" + "=" * 40)
    print("BA-KA SOUL SYSTEM DEMONSTRATION")
    print("=" * 40)
    
    print(f"\nOriginal Ba-Ka Power: {ra_card.get_ba_ka_power()}")
    
    # Separate Ba
    if BaKaSystem.separate_ba(ra_card):
        print("[*] Ba successfully separated from Ka!")
        print(f"New Ba-Ka Power: {ra_card.get_ba_ka_power()}")
        print("Ra can now use enhanced afterlife abilities but at reduced base power.")
    
    # Check if Ra is divine
    if ra_card.is_divine():
        print(f"[CROWN] {ra_card.name} is a Divine-tier card!")


def demonstrate_card_database():
    """Demonstrate the comprehensive card database system."""
    print(f"\n" + "=" * 40)
    print("CARD DATABASE DEMONSTRATION")
    print("=" * 40)
    
    db = get_card_database()
    
    # Get all cards
    all_cards = get_all_cards()
    print(f"\nTotal cards loaded: {len(all_cards)}")
    
    # Show statistics
    stats = db.get_card_statistics()
    print(f"\nCard Statistics:")
    print(f"  • Total Cards: {stats['total_cards']}")
    print(f"  • Average Mana Cost: {stats['average_mana_cost']}")
    print(f"  • Ba-Ka System Cards: {stats['ba_ka_system_cards']} ({stats['ba_ka_percentage']}%)")
    
    print(f"\nCards by Type:")
    for card_type, count in stats['by_type'].items():
        if count > 0:
            print(f"  • {card_type.title()}: {count}")
    
    print(f"\nCards by Element:")
    for element, count in stats['by_element'].items():
        if count > 0:
            print(f"  • {element.title()}: {count}")
    
    print(f"\nCards by Rarity:")
    for rarity, count in stats['by_rarity'].items():
        if count > 0:
            print(f"  • {rarity.title()}: {count}")
    
    # Show some sample cards from each category
    print(f"\n" + "-" * 40)
    print("SAMPLE CARDS BY CATEGORY")
    print("-" * 40)
    
    # Divine cards
    divine_cards = db.get_divine_cards()
    print(f"\nDivine Cards ({len(divine_cards)}):")
    for card in divine_cards[:3]:  # Show first 3
        print(f"  • {card.name} ({card.element.value})")
    
    # Sun element cards
    sun_cards = db.get_cards_by_element(CardElement.SUN)
    print(f"\nSun Element Cards ({len(sun_cards)}):")
    for card in sun_cards:
        print(f"  • {card.name}")
    
    # Ba-Ka system cards
    ba_ka_cards = db.get_ba_ka_cards()
    print(f"\nBa-Ka System Cards ({len(ba_ka_cards)}):")
    for card in ba_ka_cards[:5]:  # Show first 5
        keywords = [kw.value for kw in card.keywords if 'ba' in kw.value or 'ka' in kw.value or 'soul' in kw.value or 'afterlife' in kw.value]
        print(f"  • {card.name} - {', '.join(keywords) if keywords else 'Ba-Ka effects'}")


def demonstrate_card_search():
    """Demonstrate card search and synergy features."""
    print(f"\n" + "=" * 40)
    print("CARD SEARCH & SYNERGY DEMONSTRATION") 
    print("=" * 40)
    
    db = get_card_database()
    
    # Search for magic-related cards
    magic_cards = db.search_cards("magic")
    print(f"\nCards containing 'magic' ({len(magic_cards)}):")
    for card in magic_cards:
        print(f"  • {card.name} ({card.card_type.value})")
    
    # Search for death/underworld cards
    death_cards = db.search_cards("death")
    print(f"\nCards containing 'death' ({len(death_cards)}):")
    for card in death_cards:
        print(f"  • {card.name} ({card.card_type.value})")
    
    # Show synergies for Ra
    ra_card = get_god_card_by_id("god_ra_01")
    if ra_card:
        synergies = db.get_card_synergies(ra_card)
        print(f"\nCards that synergize with {ra_card.name} ({len(synergies)}):")
        for card in synergies[:5]:  # Show top 5 synergies
            synergy_bonus = ra_card.get_element_synergy(card.element)
            synergy_text = f" (Synergy: {synergy_bonus:.1f}x)" if synergy_bonus != 1.0 else ""
            print(f"  • {card.name} ({card.element.value}){synergy_text}")


def demonstrate_asset_validation():
    """Demonstrate asset validation system."""
    print(f"\n" + "=" * 40)
    print("ASSET VALIDATION DEMONSTRATION")
    print("=" * 40)
    
    db = get_card_database()
    
    # Validate assets
    validation = db.validate_card_assets()
    
    print(f"Asset Validation Results:")
    print(f"  • Total Cards: {validation['total_cards']}")
    print(f"  • Cards with Assets: {validation['cards_with_assets']}")
    print(f"  • Validation Passed: {'[YES]' if validation['validation_passed'] else '[NO]'}")
    
    if validation['asset_qualities']:
        print(f"\nAsset Quality Distribution:")
        for quality_range, count in validation['asset_qualities'].items():
            print(f"  • Quality {quality_range}: {count} cards")
    
    if validation['missing_assets']:
        print(f"\nMissing Assets ({len(validation['missing_assets'])}):")
        for missing in validation['missing_assets'][:3]:  # Show first 3
            print(f"  • {missing['name']}: {missing['expected_path']}")


if __name__ == "__main__":
    try:
        # Run all demonstrations
        demonstrate_ra_card()
        demonstrate_card_database()
        demonstrate_card_search()
        demonstrate_asset_validation()
        
        print(f"\n" + "=" * 60)
        print("[SUCCESS] EGYPTIAN CARD SYSTEM DEMONSTRATION COMPLETE!")
        print("All systems functional with authentic Egyptian mythology.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)