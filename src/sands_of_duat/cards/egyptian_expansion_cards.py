#!/usr/bin/env python3
"""
SANDS OF DUAT - EGYPTIAN EXPANSION CARDS
========================================

Expanded collection of Egyptian mythology cards with advanced mechanics.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import pygame

from .egyptian_cards import EgyptianCard, CardType, CardRarity, CardStats

class AdvancedCardMechanics(Enum):
    """Advanced card mechanics for Egyptian expansion."""
    DIVINE_FAVOR = "divine_favor"      # Gains power from other gods
    MUMMIFICATION = "mummification"    # Returns from death
    PHARAOHS_BLESSING = "blessing"     # Buffs all cards
    CURSE_OF_SET = "curse"            # Debuffs enemy
    ANKH_RESURRECTION = "resurrection" # Revive fallen cards
    HIEROGLYPH_SYNERGY = "synergy"    # Combos with specific cards

@dataclass
class AdvancedCardEffect:
    """Advanced card effect system."""
    effect_type: AdvancedCardMechanics
    power: int
    duration: int = 1
    description: str = ""

class EgyptianExpansionCard(EgyptianCard):
    """Expanded Egyptian card with advanced mechanics."""
    
    def __init__(self, name: str, card_type: CardType, rarity: CardRarity, 
                 stats: CardStats, description: str, 
                 advanced_effects: List[AdvancedCardEffect] = None,
                 artwork_name: str = None):
        super().__init__(name, card_type, rarity, stats, description, artwork_name)
        self.advanced_effects = advanced_effects or []
        self.synergy_tags = set()  # Tags for synergy effects
    
    def add_synergy_tag(self, tag: str):
        """Add synergy tag for card interactions."""
        self.synergy_tags.add(tag)
    
    def has_synergy_with(self, other_card: 'EgyptianExpansionCard') -> bool:
        """Check if this card has synergy with another."""
        return bool(self.synergy_tags.intersection(other_card.synergy_tags))

# EGYPTIAN GODS EXPANSION
class HorusLordOfSky(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Horus, Lord of the Sky",
            card_type=CardType.GOD,
            rarity=CardRarity.LEGENDARY,
            stats=CardStats(attack=8, health=10, cost=7),
            description="Divine falcon god who rules the heavens. When played, all creature cards gain +1/+1.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.PHARAOHS_BLESSING,
                    power=1,
                    description="All creatures gain +1/+1"
                )
            ],
            artwork_name="horus_lord_of_sky"
        )
        self.add_synergy_tag("sky")
        self.add_synergy_tag("divine")

class BastetCatGoddess(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Bastet, Cat Goddess",
            card_type=CardType.GOD,
            rarity=CardRarity.LEGENDARY,
            stats=CardStats(attack=6, health=8, cost=5),
            description="Protector goddess with feline grace. Returns to hand when destroyed.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.ANKH_RESURRECTION,
                    power=1,
                    description="Returns to hand when destroyed"
                )
            ],
            artwork_name="bastet_cat_goddess"
        )
        self.add_synergy_tag("protection")
        self.add_synergy_tag("divine")

class ThothWisdomKeeper(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Thoth, Keeper of Wisdom",
            card_type=CardType.GOD,
            rarity=CardRarity.LEGENDARY,
            stats=CardStats(attack=5, health=9, cost=6),
            description="Ibis-headed god of knowledge. Draw 2 cards when played.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.HIEROGLYPH_SYNERGY,
                    power=2,
                    description="Draw 2 cards when played"
                )
            ],
            artwork_name="thoth_wisdom_keeper"
        )
        self.add_synergy_tag("wisdom")
        self.add_synergy_tag("divine")

# MYTHOLOGICAL CREATURES
class SacredScarab(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Sacred Scarab",
            card_type=CardType.CREATURE,
            rarity=CardRarity.COMMON,
            stats=CardStats(attack=2, health=3, cost=2),
            description="Golden beetle that brings divine favor. Gains +1/+1 for each god on the field.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.DIVINE_FAVOR,
                    power=1,
                    description="+1/+1 for each god"
                )
            ],
            artwork_name="sacred_scarab"
        )
        self.add_synergy_tag("divine")
        self.add_synergy_tag("insect")

class DesertPhoenix(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Desert Phoenix",
            card_type=CardType.CREATURE,
            rarity=CardRarity.EPIC,
            stats=CardStats(attack=6, health=4, cost=5),
            description="Mythical firebird that rises from sand. When destroyed, deal 3 damage to all enemies.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.MUMMIFICATION,
                    power=3,
                    description="Deal 3 damage to all enemies when destroyed"
                )
            ],
            artwork_name="desert_phoenix"
        )
        self.add_synergy_tag("fire")
        self.add_synergy_tag("mythical")

class AnubisJackal(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Anubis Jackal",
            card_type=CardType.CREATURE,
            rarity=CardRarity.RARE,
            stats=CardStats(attack=4, health=5, cost=4),
            description="Sacred guardian of the underworld. Can resurrect one fallen creature.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.ANKH_RESURRECTION,
                    power=1,
                    description="Resurrect one fallen creature"
                )
            ],
            artwork_name="anubis_jackal"
        )
        self.add_synergy_tag("death")
        self.add_synergy_tag("guardian")

# POWERFUL SPELLS
class PharaohsWrath(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Pharaoh's Wrath",
            card_type=CardType.SPELL,
            rarity=CardRarity.EPIC,
            stats=CardStats(cost=4),
            description="Divine punishment from the pharaoh. Deal 5 damage to all enemy creatures.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.PHARAOHS_BLESSING,
                    power=5,
                    description="Deal 5 damage to all enemies"
                )
            ],
            artwork_name="pharaohs_wrath"
        )
        self.add_synergy_tag("royal")
        self.add_synergy_tag("damage")

class CurseOfTheDesert(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Curse of the Desert",
            card_type=CardType.SPELL,
            rarity=CardRarity.RARE,
            stats=CardStats(cost=3),
            description="Ancient desert curse. All enemy creatures lose -2/-2 this turn.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.CURSE_OF_SET,
                    power=2,
                    duration=1,
                    description="All enemies lose -2/-2"
                )
            ],
            artwork_name="curse_of_desert"
        )
        self.add_synergy_tag("curse")
        self.add_synergy_tag("desert")

# SACRED ARTIFACTS
class AnkhOfEternalLife(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Ankh of Eternal Life",
            card_type=CardType.ARTIFACT,
            rarity=CardRarity.LEGENDARY,
            stats=CardStats(cost=6),
            description="Symbol of eternal life. All your creatures gain +2 health and return when destroyed.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.ANKH_RESURRECTION,
                    power=2,
                    description="All creatures return when destroyed"
                )
            ],
            artwork_name="ankh_eternal_life"
        )
        self.add_synergy_tag("eternal")
        self.add_synergy_tag("artifact")

class EyeOfHorus(EgyptianExpansionCard):
    def __init__(self):
        super().__init__(
            name="Eye of Horus",
            card_type=CardType.ARTIFACT,
            rarity=CardRarity.EPIC,
            stats=CardStats(cost=4),
            description="All-seeing eye of protection. Your creatures cannot be targeted by spells.",
            advanced_effects=[
                AdvancedCardEffect(
                    effect_type=AdvancedCardMechanics.PHARAOHS_BLESSING,
                    power=0,
                    description="Creatures immune to spells"
                )
            ],
            artwork_name="eye_of_horus"
        )
        self.add_synergy_tag("protection")
        self.add_synergy_tag("artifact")

# EXPANSION CARD COLLECTION
EGYPTIAN_EXPANSION_CARDS = [
    # Gods
    HorusLordOfSky(),
    BastetCatGoddess(), 
    ThothWisdomKeeper(),
    
    # Creatures
    SacredScarab(),
    DesertPhoenix(),
    AnubisJackal(),
    
    # Spells
    PharaohsWrath(),
    CurseOfTheDesert(),
    
    # Artifacts
    AnkhOfEternalLife(),
    EyeOfHorus(),
]

def get_expansion_cards_by_rarity(rarity: CardRarity) -> List[EgyptianExpansionCard]:
    """Get all expansion cards of a specific rarity."""
    return [card for card in EGYPTIAN_EXPANSION_CARDS if card.rarity == rarity]

def get_expansion_cards_by_type(card_type: CardType) -> List[EgyptianExpansionCard]:
    """Get all expansion cards of a specific type.""" 
    return [card for card in EGYPTIAN_EXPANSION_CARDS if card.card_type == card_type]

def get_cards_with_synergy(tag: str) -> List[EgyptianExpansionCard]:
    """Get all cards that have a specific synergy tag."""
    return [card for card in EGYPTIAN_EXPANSION_CARDS if tag in card.synergy_tags]