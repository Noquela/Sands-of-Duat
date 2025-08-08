"""
Core card system for Sands of Duat - Egyptian mythology card game.
Implements the fundamental card data structures, enums, and Ba-Ka soul system.
"""

from enum import Enum, auto
from typing import List, Dict, Optional, Set, Any
from dataclasses import dataclass, field
from pathlib import Path
import json


class CardType(Enum):
    """Types of cards in the Egyptian mythology system."""
    DEITY = "deity"           # Egyptian gods and goddesses
    MORTAL = "mortal"         # Human characters, pharaohs, priests
    ARTIFACT = "artifact"     # Sacred objects, weapons, tools
    SPELL = "spell"           # Magic spells and incantations
    LOCATION = "location"     # Places of power, temples, underworld
    CREATURE = "creature"     # Mythical beasts, demons, spirits
    EVENT = "event"           # Historical or mythological events


class CardRarity(Enum):
    """Card rarity system based on Egyptian hierarchy."""
    COMMON = "common"         # Basic cards
    UNCOMMON = "uncommon"     # Improved cards
    RARE = "rare"             # Powerful cards
    EPIC = "epic"             # Very powerful cards
    LEGENDARY = "legendary"   # Extremely rare cards
    MYTHIC = "mythic"         # Ultimate power level
    DIVINE = "divine"         # Reserved for major gods


class CardElement(Enum):
    """Egyptian elemental and conceptual affinities."""
    SUN = "sun"               # Ra's domain - fire, light, life
    DEATH = "death"           # Anubis/Osiris - mortality, judgment
    MAGIC = "magic"           # Thoth/Isis - knowledge, spells
    ORDER = "order"           # Ma'at - justice, balance, truth
    CHAOS = "chaos"           # Set - destruction, storms, disorder
    PROTECTION = "protection" # Bastet/Taweret - defense, healing
    WATER = "water"           # Sobek/Khnum - rivers, fertility
    EARTH = "earth"           # Ptah - creation, craftsmanship
    AIR = "air"               # Shu - wind, breath, atmosphere
    NEUTRAL = "neutral"       # No specific elemental affinity


class CardKeyword(Enum):
    """Ba-Ka system keywords and special abilities."""
    # Ba-Ka Soul System
    BA_SEPARATION = "ba_separation"       # Can separate Ba (soul) from Ka (life force)
    KA_BINDING = "ka_binding"             # Binds to Ka energy permanently
    SOUL_LINK = "soul_link"               # Links multiple cards' Ba-Ka states
    AFTERLIFE = "afterlife"               # Effects that trigger in underworld
    JUDGMENT = "judgment"                 # Cards that evaluate other cards
    
    # Egyptian Powers
    DIVINE_PROTECTION = "divine_protection"  # Immunity to certain effects
    PHARAOH_BOND = "pharaoh_bond"           # Stronger when pharaoh present
    TEMPLE_POWER = "temple_power"           # Bonus in temple locations
    MUMMY_WRAP = "mummy_wrap"               # Gradually disable opponents
    HIEROGLYPH = "hieroglyph"               # Written magic effects
    ANKH_LIFE = "ankh_life"                 # Life restoration abilities
    
    # Combat Keywords
    CHARGE = "charge"                       # Can attack immediately
    GUARD = "guard"                         # Must be attacked first
    STEALTH = "stealth"                     # Cannot be targeted
    REGENERATE = "regenerate"               # Heals over time
    PIERCE = "pierce"                       # Ignores armor
    RITUAL = "ritual"                       # Requires setup turn


@dataclass
class CardStats:
    """Base statistics for cards."""
    attack: int = 0
    defense: int = 0
    health: int = 0
    mana_cost: int = 0
    sand_cost: int = 0  # Special Egyptian resource
    ba_power: int = 0   # Soul energy
    ka_power: int = 0   # Life force energy
    divine_favor: int = 0  # Divine approval rating


@dataclass
class CardEffect:
    """Represents a card's effect or ability."""
    name: str
    description: str
    effect_type: str  # "trigger", "passive", "activated", "ba_ka"
    target: str = "self"  # "self", "enemy", "all", "choice"
    cost: Dict[str, int] = field(default_factory=dict)
    conditions: List[str] = field(default_factory=list)
    ba_ka_interaction: Optional[str] = None  # Special Ba-Ka system effects


@dataclass
class Card:
    """Complete card representation for Egyptian mythology game."""
    
    # Core Identity
    card_id: str
    name: str
    card_type: CardType
    rarity: CardRarity
    element: CardElement
    
    # Gameplay Stats
    stats: CardStats
    
    # Abilities and Effects
    keywords: Set[CardKeyword] = field(default_factory=set)
    effects: List[CardEffect] = field(default_factory=list)
    
    # Flavor and Lore
    description: str = ""
    flavor_text: str = ""
    mythology_source: str = ""
    
    # Asset Information
    image_path: Optional[Path] = None
    image_quality: Optional[int] = None
    
    # Ba-Ka System State
    ba_separated: bool = False
    ka_bound: bool = False
    soul_link_targets: Set[str] = field(default_factory=set)
    
    # Game State
    is_summoned: bool = False
    current_health: Optional[int] = None
    status_effects: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize derived values after creation."""
        if self.current_health is None:
            self.current_health = self.stats.health
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization."""
        return {
            "card_id": self.card_id,
            "name": self.name,
            "card_type": self.card_type.value,
            "rarity": self.rarity.value,
            "element": self.element.value,
            "stats": {
                "attack": self.stats.attack,
                "defense": self.stats.defense,
                "health": self.stats.health,
                "mana_cost": self.stats.mana_cost,
                "sand_cost": self.stats.sand_cost,
                "ba_power": self.stats.ba_power,
                "ka_power": self.stats.ka_power
            },
            "keywords": [kw.value for kw in self.keywords],
            "effects": [
                {
                    "name": effect.name,
                    "description": effect.description,
                    "effect_type": effect.effect_type,
                    "target": effect.target,
                    "cost": effect.cost,
                    "conditions": effect.conditions,
                    "ba_ka_interaction": effect.ba_ka_interaction
                }
                for effect in self.effects
            ],
            "description": self.description,
            "flavor_text": self.flavor_text,
            "mythology_source": self.mythology_source,
            "image_path": str(self.image_path) if self.image_path else None,
            "image_quality": self.image_quality
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Card':
        """Create card from dictionary."""
        stats = CardStats(**data["stats"])
        
        effects = [
            CardEffect(**effect_data)
            for effect_data in data.get("effects", [])
        ]
        
        keywords = {CardKeyword(kw) for kw in data.get("keywords", [])}
        
        image_path = Path(data["image_path"]) if data.get("image_path") else None
        
        return cls(
            card_id=data["card_id"],
            name=data["name"],
            card_type=CardType(data["card_type"]),
            rarity=CardRarity(data["rarity"]),
            element=CardElement(data["element"]),
            stats=stats,
            keywords=keywords,
            effects=effects,
            description=data.get("description", ""),
            flavor_text=data.get("flavor_text", ""),
            mythology_source=data.get("mythology_source", ""),
            image_path=image_path,
            image_quality=data.get("image_quality")
        )
    
    def has_keyword(self, keyword: CardKeyword) -> bool:
        """Check if card has specific keyword."""
        return keyword in self.keywords
    
    def get_ba_ka_power(self) -> tuple[int, int]:
        """Get current Ba and Ka power levels."""
        ba_modifier = 0.5 if self.ba_separated else 1.0
        ka_modifier = 0.5 if self.ka_bound else 1.0
        
        current_ba = int(self.stats.ba_power * ba_modifier)
        current_ka = int(self.stats.ka_power * ka_modifier)
        
        return current_ba, current_ka
    
    def can_use_effect(self, effect_index: int, available_resources: Dict[str, int]) -> bool:
        """Check if card can use a specific effect given available resources."""
        if effect_index >= len(self.effects):
            return False
            
        effect = self.effects[effect_index]
        
        # Check resource costs
        for resource, cost in effect.cost.items():
            if available_resources.get(resource, 0) < cost:
                return False
        
        # Check Ba-Ka requirements
        if effect.ba_ka_interaction:
            ba_power, ka_power = self.get_ba_ka_power()
            if effect.ba_ka_interaction == "require_ba" and ba_power <= 0:
                return False
            elif effect.ba_ka_interaction == "require_ka" and ka_power <= 0:
                return False
            elif effect.ba_ka_interaction == "require_both" and (ba_power <= 0 or ka_power <= 0):
                return False
        
        return True
    
    def is_divine(self) -> bool:
        """Check if this card represents a major Egyptian deity."""
        return (self.card_type == CardType.DEITY and 
                self.rarity in [CardRarity.LEGENDARY, CardRarity.MYTHIC, CardRarity.DIVINE])
    
    def get_element_synergy(self, other_element: CardElement) -> float:
        """Calculate elemental synergy bonus with another element."""
        synergies = {
            CardElement.SUN: {
                CardElement.ORDER: 1.2,
                CardElement.PROTECTION: 1.1,
                CardElement.CHAOS: 0.8
            },
            CardElement.DEATH: {
                CardElement.ORDER: 1.2,
                CardElement.MAGIC: 1.1,
                CardElement.SUN: 0.9
            },
            CardElement.MAGIC: {
                CardElement.DEATH: 1.1,
                CardElement.ORDER: 1.1,
                CardElement.CHAOS: 1.3
            },
            CardElement.ORDER: {
                CardElement.SUN: 1.2,
                CardElement.DEATH: 1.2,
                CardElement.CHAOS: 0.7
            },
            CardElement.CHAOS: {
                CardElement.MAGIC: 1.3,
                CardElement.ORDER: 0.7,
                CardElement.PROTECTION: 0.8
            },
            CardElement.PROTECTION: {
                CardElement.SUN: 1.1,
                CardElement.ORDER: 1.1,
                CardElement.CHAOS: 0.8
            }
        }
        
        return synergies.get(self.element, {}).get(other_element, 1.0)


class BaKaSystem:
    """
    The Ba-Ka soul system is central to Egyptian mythology and this card game.
    
    Ba (soul) - The personality, emotions, and spiritual essence
    Ka (life force) - The vital energy that animates the body
    
    Cards can have their Ba and Ka separated, bound, or linked, creating
    complex strategic interactions based on ancient Egyptian beliefs.
    """
    
    @staticmethod
    def separate_ba(card: Card) -> bool:
        """Separate Ba from Ka, reducing both but enabling special effects."""
        if card.ba_separated:
            return False
            
        card.ba_separated = True
        # Ba separation enables certain powerful effects but reduces base power
        return True
    
    @staticmethod
    def bind_ka(card: Card) -> bool:
        """Bind Ka permanently, trading flexibility for stability."""
        if card.ka_bound:
            return False
            
        card.ka_bound = True
        # Ka binding provides stability but limits certain interactions
        return True
    
    @staticmethod
    def create_soul_link(card1: Card, card2: Card) -> bool:
        """Create a soul link between two cards."""
        if card1.card_id in card2.soul_link_targets or card2.card_id in card1.soul_link_targets:
            return False
            
        card1.soul_link_targets.add(card2.card_id)
        card2.soul_link_targets.add(card1.card_id)
        return True
    
    @staticmethod
    def calculate_afterlife_power(card: Card) -> int:
        """Calculate power level in the afterlife/underworld."""
        base_power = card.stats.attack + card.stats.defense
        
        # Ba-separated cards are more powerful in afterlife
        if card.ba_separated:
            base_power *= 1.5
            
        # Cards with afterlife keyword get bonus
        if CardKeyword.AFTERLIFE in card.keywords:
            base_power *= 1.3
            
        return int(base_power)