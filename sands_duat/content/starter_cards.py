"""
Starter Card Definitions

Basic set of cards for the Sands of Duat game, designed around
the Hour-Glass Initiative system with Egyptian theming.

Cards are balanced around the 6-sand maximum with meaningful
tactical decisions at each cost level.
"""

from sands_duat.core.cards import Card, CardEffect, CardType, CardRarity, EffectType, TargetType, card_library
from .egyptian_card_loader import initialize_egyptian_cards
import logging


def create_starter_cards():
    """Create and register all starter cards in the card library."""
    logger = logging.getLogger(__name__)
    
    # Load Egyptian cards first
    try:
        egyptian_cards = initialize_egyptian_cards()
        logger.info(f"Loaded {len(egyptian_cards)} Egyptian cards")
    except Exception as e:
        logger.error(f"Failed to load Egyptian cards: {e}")
        egyptian_cards = {}
    
    # === 0-Cost Cards (Free Actions) ===
    
    # Desert Whisper (0 cost)
    desert_whisper = Card(
        name="Desert Whisper",
        description="Draw a card. The desert spirits guide your hand.",
        sand_cost=0,
        card_type=CardType.SKILL,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DRAW_CARDS, value=1, target=TargetType.SELF)
        ],
        keywords={"cantrip"},
        flavor_text="The winds carry secrets from the ancient tombs."
    )
    
    # Sand Grain (0 cost)
    sand_grain = Card(
        name="Sand Grain",
        description="Gain 1 sand. Every grain matters in the desert.",
        sand_cost=0,
        card_type=CardType.SKILL,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.GAIN_SAND, value=1, target=TargetType.SELF)
        ],
        keywords={"sand"},
        flavor_text="From a single grain, dunes are born."
    )
    
    # === 1-Cost Cards (Basic Actions) ===
    
    # Tomb Strike (1 cost)
    tomb_strike = Card(
        name="Tomb Strike",
        description="Deal 6 damage. A swift strike from the shadows.",
        sand_cost=1,
        card_type=CardType.ATTACK,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=6, target=TargetType.ENEMY)
        ],
        keywords={"strike"},
        flavor_text="Swift as the desert wind, silent as the tomb."
    )
    
    # Ankh Blessing (1 cost)
    ankh_blessing = Card(
        name="Ankh Blessing",
        description="Heal 5 health. The ankh's power flows through you.",
        sand_cost=1,
        card_type=CardType.SKILL,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.HEAL, value=5, target=TargetType.SELF)
        ],
        keywords={"heal"},
        flavor_text="Life eternal flows through the sacred symbol."
    )
    
    # === 2-Cost Cards (Efficient Actions) ===
    
    # Scarab Swarm (2 cost)
    scarab_swarm = Card(
        name="Scarab Swarm",
        description="Deal 9 damage. Countless scarabs overwhelm your foe.",
        sand_cost=2,
        card_type=CardType.ATTACK,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=9, target=TargetType.ENEMY)
        ],
        keywords={"swarm"},
        flavor_text="The desert's children answer your call."
    )
    
    # Papyrus Scroll (2 cost)
    papyrus_scroll = Card(
        name="Papyrus Scroll",
        description="Draw 2 cards. Ancient knowledge unfolds.",
        sand_cost=2,
        card_type=CardType.SKILL,
        rarity=CardRarity.COMMON,
        effects=[
            CardEffect(effect_type=EffectType.DRAW_CARDS, value=2, target=TargetType.SELF)
        ],
        keywords={"knowledge"},
        flavor_text="The scribes' wisdom transcends time."
    )
    
    # === 3-Cost Cards (Powerful Actions) ===
    
    # Mummy's Wrath (3 cost)
    mummys_wrath = Card(
        name="Mummy's Wrath",
        description="Deal 14 damage. The undead's fury knows no bounds.",
        sand_cost=3,
        card_type=CardType.ATTACK,
        rarity=CardRarity.UNCOMMON,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=14, target=TargetType.ENEMY)
        ],
        keywords={"undead", "wrath"},
        flavor_text="Disturb the dead, face their eternal rage."
    )
    
    # Isis's Grace (3 cost)
    isis_grace = Card(
        name="Isis's Grace",
        description="Heal 8 health and draw a card. The goddess blesses you.",
        sand_cost=3,
        card_type=CardType.SKILL,
        rarity=CardRarity.UNCOMMON,
        effects=[
            CardEffect(effect_type=EffectType.HEAL, value=8, target=TargetType.SELF),
            CardEffect(effect_type=EffectType.DRAW_CARDS, value=1, target=TargetType.SELF)
        ],
        keywords={"blessing", "divine"},
        flavor_text="Mother of magic, protector of the faithful."
    )
    
    # === 4-Cost Cards (Major Actions) ===
    
    # Pyramid Power (4 cost)
    pyramid_power = Card(
        name="Pyramid Power",
        description="Deal 18 damage. Channel the might of the pharaohs.",
        sand_cost=4,
        card_type=CardType.ATTACK,
        rarity=CardRarity.RARE,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=18, target=TargetType.ENEMY)
        ],
        keywords={"pharaoh", "power"},
        flavor_text="The eternal monuments channel ancient power."
    )
    
    # Thoth's Wisdom (4 cost)
    thoth_wisdom = Card(
        name="Thoth's Wisdom",
        description="Draw 3 cards and gain 2 sand. Knowledge is power.",
        sand_cost=4,
        card_type=CardType.SKILL,
        rarity=CardRarity.RARE,
        effects=[
            CardEffect(effect_type=EffectType.DRAW_CARDS, value=3, target=TargetType.SELF),
            CardEffect(effect_type=EffectType.GAIN_SAND, value=2, target=TargetType.SELF)
        ],
        keywords={"wisdom", "divine"},
        flavor_text="The ibis-headed god shares his infinite knowledge."
    )
    
    # === 5-Cost Cards (Epic Actions) ===
    
    # Anubis Judgment (5 cost)
    anubis_judgment = Card(
        name="Anubis Judgment",
        description="Deal 25 damage. The jackal god weighs your enemy's soul.",
        sand_cost=5,
        card_type=CardType.ATTACK,
        rarity=CardRarity.RARE,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=25, target=TargetType.ENEMY)
        ],
        keywords={"judgment", "divine", "death"},
        flavor_text="Your heart is weighed against a feather... and found wanting."
    )
    
    # === 6-Cost Cards (Ultimate Actions) ===
    
    # Ra's Solar Flare (6 cost)
    ra_solar_flare = Card(
        name="Ra's Solar Flare",
        description="Deal 30 damage. The sun god's fury incinerates all.",
        sand_cost=6,
        card_type=CardType.ATTACK,
        rarity=CardRarity.LEGENDARY,
        effects=[
            CardEffect(effect_type=EffectType.DAMAGE, value=30, target=TargetType.ENEMY)
        ],
        keywords={"solar", "divine", "fire"},
        flavor_text="Behold the radiance that birthed civilization."
    )
    
    # Pharaoh's Resurrection (6 cost)
    pharaoh_resurrection = Card(
        name="Pharaoh's Resurrection",
        description="Heal to full health and gain 3 sand. Death is not the end.",
        sand_cost=6,
        card_type=CardType.SKILL,
        rarity=CardRarity.LEGENDARY,
        effects=[
            CardEffect(effect_type=EffectType.HEAL, value=100, target=TargetType.SELF),  # High value for full heal
            CardEffect(effect_type=EffectType.GAIN_SAND, value=3, target=TargetType.SELF)
        ],
        keywords={"resurrection", "divine", "pharaoh"},
        flavor_text="Even death bows before the eternal pharaoh."
    )
    
    # Register all cards
    cards = [
        desert_whisper, sand_grain, tomb_strike, ankh_blessing,
        scarab_swarm, papyrus_scroll, mummys_wrath, isis_grace,
        pyramid_power, thoth_wisdom, anubis_judgment, ra_solar_flare,
        pharaoh_resurrection
    ]
    
    for card in cards:
        card_library.register_card(card)
    
    return cards


def get_starter_deck(deck_type: str = "wanderer"):
    """Create a balanced starter deck for new players with Egyptian cards.
    
    Args:
        deck_type: Type of starter deck (wanderer, mystic, warrior)
    """
    from sands_duat.core.cards import Deck
    
    # Ensure cards are created
    create_starter_cards()
    
    deck = Deck(name="Desert Wanderer Starter")
    
    # Add Egyptian cards from YAML to the deck
    egyptian_deck_composition = [
        # 0-cost cards
        ("whisper_of_thoth", 2),      # 0-cost draw + sand
        ("desert_meditation", 2),     # 0-cost draw
        
        # 1-cost cards
        ("anubis_judgment", 3),       # 1-cost attack with vulnerable
        ("isis_protection", 3),       # 1-cost block + heal
        
        # 2-cost cards
        ("ra_solar_flare", 2),        # 2-cost attack with weak
        ("mummification_ritual", 2),  # 2-cost heal + block
        
        # 3-cost cards
        ("horus_divine_sight", 1),    # 3-cost utility
        ("eye_of_horus", 2),          # 1-cost block + discover
        
        # Basic starter cards (fallback if Egyptian cards not found)
        ("Desert Whisper", 1),        # 0-cost utility
        ("Tomb Strike", 2),           # 1-cost attacks
        ("Ankh Blessing", 2),         # 1-cost heals
    ]
    
    for card_id, count in egyptian_deck_composition:
        # Try to get by ID first (for Egyptian cards), then by name (for starter cards)
        card_template = card_library.get_card_by_id(card_id)
        if not card_template:
            card_template = card_library.get_card_by_name(card_id)
        
        if card_template:
            for _ in range(count):
                new_card = card_template.copy(deep=True)
                deck.add_card(new_card)
        else:
            logger.warning(f"Card not found: {card_id}")
    
    return deck


# Initialize cards when module is imported
if __name__ == "__main__":
    cards = create_starter_cards()
    print(f"Created {len(cards)} starter cards")
    
    deck = get_starter_deck()
    print(f"Created starter deck with {len(deck)} cards")
    print(f"Average sand cost: {deck.get_average_cost():.1f}")