"""
Card System and Effects

Comprehensive card management system for the deck-builder mechanics,
including card definitions, effects, and deck management.

Key Features:
- Card data models with sand cost integration
- Effect system for card abilities
- Deck management and manipulation
- Card validation and balancing support

Classes:
- Card: Individual card definition
- CardEffect: Modular card effect system
- Deck: Collection of cards with manipulation methods
- CardLibrary: Central registry for all available cards
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Callable, Union, Set
from pydantic import BaseModel, Field, validator
import uuid
import random


class CardType(Enum):
    """Types of cards in the game."""
    ATTACK = "attack"
    SKILL = "skill"
    POWER = "power"
    CURSE = "curse"
    STATUS = "status"


class TargetType(Enum):
    """Valid targets for card effects."""
    SELF = "self"
    ENEMY = "enemy"
    ALL_ENEMIES = "all_enemies"
    ANY = "any"
    NONE = "none"


class EffectType(Enum):
    """Types of card effects."""
    DAMAGE = "damage"
    HEAL = "heal"
    BLOCK = "block"
    DRAW_CARDS = "draw_cards"
    GAIN_SAND = "gain_sand"
    BUFF = "buff"
    DEBUFF = "debuff"
    TRANSFORM = "transform"
    DISCOVER = "discover"


class CardRarity(Enum):
    """Card rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"


class CardEffect(BaseModel):
    """
    Represents a single effect that a card can have.
    
    Effects are modular and can be combined to create
    complex card behaviors.
    """
    
    effect_type: EffectType
    value: int = 0
    target: TargetType = TargetType.NONE
    condition: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def __str__(self) -> str:
        return f"{self.effect_type.value}({self.value}) -> {self.target.value}"


class Card(BaseModel):
    """
    Core card definition with Hour-Glass integration.
    
    Cards are the primary interaction method in combat,
    with sand costs determining their timing in the
    Hour-Glass Initiative system.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    sand_cost: int = Field(ge=0, le=6, description="Sand cost (0-6 grains)")
    card_type: CardType
    rarity: CardRarity = CardRarity.COMMON
    effects: List[CardEffect] = Field(default_factory=list)
    keywords: Set[str] = Field(default_factory=set)
    art_id: Optional[str] = None
    flavor_text: Optional[str] = None
    upgradeable: bool = True
    upgraded: bool = False
    
    @validator('sand_cost')
    def validate_sand_cost(cls, v):
        """Ensure sand cost is within valid range."""
        if not 0 <= v <= 6:
            raise ValueError('Sand cost must be between 0 and 6')
        return v
    
    def get_effective_cost(self, modifiers: Optional[Dict[str, int]] = None) -> int:
        """
        Get the effective sand cost after applying modifiers.
        
        Modifiers can come from powers, relics, or temporary effects.
        """
        cost = self.sand_cost
        
        if modifiers:
            cost += modifiers.get('cost_increase', 0)
            cost -= modifiers.get('cost_reduction', 0)
            
            if 'set_cost' in modifiers:
                cost = modifiers['set_cost']
        
        return max(0, min(6, cost))  # Clamp to valid range
    
    def has_keyword(self, keyword: str) -> bool:
        """Check if the card has a specific keyword."""
        return keyword.lower() in {kw.lower() for kw in self.keywords}
    
    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the card."""
        self.keywords.add(keyword.lower())
    
    def remove_keyword(self, keyword: str) -> None:
        """Remove a keyword from the card."""
        self.keywords.discard(keyword.lower())
    
    def get_damage_effects(self) -> List[CardEffect]:
        """Get all damage effects from this card."""
        return [effect for effect in self.effects if effect.effect_type == EffectType.DAMAGE]
    
    def get_total_damage(self) -> int:
        """Calculate total damage this card can deal."""
        return sum(effect.value for effect in self.get_damage_effects())
    
    def can_target(self, target_type: TargetType) -> bool:
        """Check if this card can target a specific target type."""
        return any(effect.target == target_type for effect in self.effects)
    
    def upgrade(self) -> 'Card':
        """
        Create an upgraded version of this card.
        
        Returns a new Card instance with upgraded stats.
        """
        if not self.upgradeable or self.upgraded:
            return self
        
        upgraded_card = self.copy(deep=True)
        upgraded_card.upgraded = True
        upgraded_card.name = f"{self.name}+"
        
        # Basic upgrade logic - can be customized per card
        for effect in upgraded_card.effects:
            if effect.effect_type in [EffectType.DAMAGE, EffectType.HEAL, EffectType.BLOCK]:
                effect.value += 3
            elif effect.effect_type == EffectType.DRAW_CARDS:
                effect.value += 1
        
        return upgraded_card
    
    def __str__(self) -> str:
        return f"{self.name} ({self.sand_cost} sand)"
    
    def __repr__(self) -> str:
        return f"Card(id='{self.id}', name='{self.name}', cost={self.sand_cost})"


class Deck(BaseModel):
    """
    Collection of cards with manipulation methods.
    
    Handles deck building, shuffling, drawing, and
    other card collection operations.
    """
    
    cards: List[Card] = Field(default_factory=list)
    name: str = "Unnamed Deck"
    max_size: Optional[int] = None
    min_size: Optional[int] = None
    
    def add_card(self, card: Card) -> bool:
        """
        Add a card to the deck.
        
        Returns True if successful, False if deck size limits prevent addition.
        """
        if self.max_size and len(self.cards) >= self.max_size:
            return False
        
        self.cards.append(card)
        return True
    
    def remove_card(self, card_id: str) -> Optional[Card]:
        """
        Remove a card from the deck by ID.
        
        Returns the removed card if found, None otherwise.
        """
        for i, card in enumerate(self.cards):
            if card.id == card_id:
                return self.cards.pop(i)
        return None
    
    def remove_card_by_name(self, name: str) -> Optional[Card]:
        """Remove the first card with the given name."""
        for i, card in enumerate(self.cards):
            if card.name == name:
                return self.cards.pop(i)
        return None
    
    def shuffle(self, seed: Optional[int] = None) -> None:
        """Shuffle the deck."""
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
    
    def draw(self, count: int = 1) -> List[Card]:
        """
        Draw cards from the top of the deck.
        
        Returns a list of drawn cards (may be fewer than requested).
        """
        drawn = []
        for _ in range(min(count, len(self.cards))):
            if self.cards:
                drawn.append(self.cards.pop(0))
        return drawn
    
    def peek(self, count: int = 1) -> List[Card]:
        """Look at the top cards without removing them."""
        return self.cards[:count]
    
    def size(self) -> int:
        """Get the number of cards in the deck."""
        return len(self.cards)
    
    def is_empty(self) -> bool:
        """Check if the deck is empty."""
        return len(self.cards) == 0
    
    def get_card_counts(self) -> Dict[str, int]:
        """Get a count of each unique card name in the deck."""
        counts = {}
        for card in self.cards:
            counts[card.name] = counts.get(card.name, 0) + 1
        return counts
    
    def get_average_cost(self) -> float:
        """Calculate the average sand cost of cards in the deck."""
        if not self.cards:
            return 0.0
        return sum(card.sand_cost for card in self.cards) / len(self.cards)
    
    def get_cards_by_cost(self, cost: int) -> List[Card]:
        """Get all cards with a specific sand cost."""
        return [card for card in self.cards if card.sand_cost == cost]
    
    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """Get all cards of a specific type."""
        return [card for card in self.cards if card.card_type == card_type]
    
    def get_cards_by_rarity(self, rarity: CardRarity) -> List[Card]:
        """Get all cards of a specific rarity."""
        return [card for card in self.cards if card.rarity == rarity]
    
    def copy(self) -> 'Deck':
        """Create a deep copy of the deck."""
        return Deck(
            cards=[card.copy(deep=True) for card in self.cards],
            name=f"{self.name} (Copy)",
            max_size=self.max_size,
            min_size=self.min_size
        )
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self):
        return iter(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]


class CardLibrary:
    """
    Central registry for all available cards in the game.
    
    Manages card definitions, provides factory methods,
    and handles card discovery and filtering.
    """
    
    def __init__(self):
        self._cards: Dict[str, Card] = {}
        self._cards_by_name: Dict[str, Card] = {}
    
    def register_card(self, card: Card) -> None:
        """Register a card in the library."""
        self._cards[card.id] = card
        self._cards_by_name[card.name] = card
    
    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """Get a card by its ID."""
        return self._cards.get(card_id)
    
    def get_card_by_name(self, name: str) -> Optional[Card]:
        """Get a card by its name."""
        return self._cards_by_name.get(name)
    
    def create_card(self, card_id: str) -> Optional[Card]:
        """Create a new instance of a card by ID."""
        template = self.get_card_by_id(card_id)
        return template.copy(deep=True) if template else None
    
    def create_card_by_name(self, name: str) -> Optional[Card]:
        """Create a new instance of a card by name."""
        template = self.get_card_by_name(name)
        return template.copy(deep=True) if template else None
    
    def get_all_cards(self) -> List[Card]:
        """Get all registered cards."""
        return list(self._cards.values())
    
    def get_cards_by_cost(self, cost: int) -> List[Card]:
        """Get all cards with a specific sand cost."""
        return [card for card in self._cards.values() if card.sand_cost == cost]
    
    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """Get all cards of a specific type."""
        return [card for card in self._cards.values() if card.card_type == card_type]
    
    def get_cards_by_rarity(self, rarity: CardRarity) -> List[Card]:
        """Get all cards of a specific rarity."""
        return [card for card in self._cards.values() if card.rarity == rarity]
    
    def get_cards_with_keyword(self, keyword: str) -> List[Card]:
        """Get all cards that have a specific keyword."""
        return [card for card in self._cards.values() if card.has_keyword(keyword)]
    
    def clear(self) -> None:
        """Clear all registered cards."""
        self._cards.clear()
        self._cards_by_name.clear()
    
    def size(self) -> int:
        """Get the number of registered cards."""
        return len(self._cards)


# Global card library instance
card_library = CardLibrary()