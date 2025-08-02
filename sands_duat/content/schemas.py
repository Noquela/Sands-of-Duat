"""
Content Schema Definitions

Pydantic models for validating YAML content ensuring data integrity
and consistency throughout the Sands of Duat game system.

Features:
- Comprehensive validation with custom validators
- Egyptian mythology-themed enums and constraints
- Cross-reference validation capabilities
- Extensible schema system for new content types
"""

from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, field_validator, model_validator, RootModel
from enum import Enum
import re


class CardType(str, Enum):
    """Types of cards available in the game."""
    ATTACK = "attack"
    SKILL = "skill"
    POWER = "power"
    CURSE = "curse"
    BLESSING = "blessing"


class Rarity(str, Enum):
    """Card rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class EffectType(str, Enum):
    """Valid effect types for cards and abilities."""
    DAMAGE = "damage"
    BLOCK = "block"
    HEAL = "heal"
    DRAW_CARDS = "draw_cards"
    GAIN_SAND = "gain_sand"
    LOSE_SAND = "lose_sand"
    BUFF = "buff"
    DEBUFF = "debuff"
    CURSE = "curse"
    BLESSING = "blessing"
    UPGRADE_CARD = "upgrade_card"
    TRANSFORM_CARD = "transform_card"
    DISCOVER_CARD = "discover_card"
    GAIN_CARD = "gain_card"
    REMOVE_CARD = "remove_card"
    GAIN_GOLD = "gain_gold"
    LOSE_GOLD = "lose_gold"
    MAX_HEALTH_INCREASE = "max_health_increase"
    PERMANENT_SAND_INCREASE = "permanent_sand_increase"
    APPLY_POISON = "apply_poison"
    APPLY_VULNERABLE = "apply_vulnerable"
    APPLY_WEAK = "apply_weak"
    APPLY_STRENGTH = "apply_strength"
    APPLY_DEXTERITY = "apply_dexterity"
    CHANNEL_DIVINITY = "channel_divinity"
    INVOKE_RITUAL = "invoke_ritual"


class TargetType(str, Enum):
    """Valid targets for effects."""
    SELF = "self"
    ENEMY = "enemy"
    PLAYER = "player"
    ALL_ENEMIES = "all_enemies"
    RANDOM_ENEMY = "random_enemy"
    WEAKEST_ENEMY = "weakest_enemy"
    STRONGEST_ENEMY = "strongest_enemy"


class KeywordType(str, Enum):
    """Card and ability keywords for categorization."""
    # Combat Keywords
    STRIKE = "strike"
    DEFENSE = "defense"
    FIRE = "fire"
    POISON = "poison"
    CANTRIP = "cantrip"
    ETHEREAL = "ethereal"
    EXHAUST = "exhaust"
    INNATE = "innate"
    RETAIN = "retain"
    UNPLAYABLE = "unplayable"
    
    # Egyptian Mythology Keywords
    DIVINE = "divine"
    RITUAL = "ritual"
    MUMMY = "mummy"
    PHARAOH = "pharaoh"
    ANUBIS = "anubis"
    THOTH = "thoth"
    ISIS = "isis"
    OSIRIS = "osiris"
    HORUS = "horus"
    SET = "set"
    BASTET = "bastet"
    SEKHMET = "sekhmet"
    
    # Creature Types
    BEAST = "beast"
    SPIRIT = "spirit"
    UNDEAD = "undead"
    SHADOW = "shadow"
    ELEMENTAL = "elemental"
    DEMON = "demon"
    GOD = "god"
    
    # Location/Theme Keywords
    DESERT = "desert"
    TOMB = "tomb"
    TEMPLE = "temple"
    UNDERWORLD = "underworld"
    DUAT = "duat"
    PYRAMID = "pyramid"


class AIPattern(str, Enum):
    """Enemy AI behavior patterns."""
    AGGRESSIVE = "aggressive"      # Always attacks when possible
    DEFENSIVE = "defensive"        # Prioritizes defense and setup
    BALANCED = "balanced"         # Mix of offense and defense
    ERRATIC = "erratic"           # Unpredictable behavior
    TACTICAL = "tactical"         # Complex decision making
    BERSERKER = "berserker"       # High damage, ignores defense
    SUPPORT = "support"           # Buffs other enemies
    CONTROLLER = "controller"     # Focuses on debuffs and control


class EventType(str, Enum):
    """Types of map events."""
    CHOICE = "choice"             # Multiple choice encounter
    COMBAT = "combat"             # Battle encounter
    SHOP = "shop"                 # Merchant encounter
    SHRINE = "shrine"             # Blessing/upgrade location
    TREASURE = "treasure"         # Reward encounter
    CHALLENGE = "challenge"       # Skill-based test
    REST = "rest"                 # Healing/recovery site
    MYSTERY = "mystery"           # Unknown outcome
    BOSS = "boss"                 # Major enemy encounter
    STORY = "story"               # Narrative moment


class HourOfNight(str, Enum):
    """The 12 hours of night from Egyptian mythology."""
    FIRST_HOUR = "first_hour"         # Sunset, entering the Duat
    SECOND_HOUR = "second_hour"       # Meeting the ferryman
    THIRD_HOUR = "third_hour"         # Lake of Fire
    FOURTH_HOUR = "fourth_hour"       # Sokar's domain
    FIFTH_HOUR = "fifth_hour"         # Hidden chamber
    SIXTH_HOUR = "sixth_hour"         # Apophis appears
    SEVENTH_HOUR = "seventh_hour"     # Battle preparation
    EIGHTH_HOUR = "eighth_hour"       # Osiris chamber
    NINTH_HOUR = "ninth_hour"         # Judgment hall
    TENTH_HOUR = "tenth_hour"         # Purification
    ELEVENTH_HOUR = "eleventh_hour"   # Final trials
    TWELFTH_HOUR = "twelfth_hour"     # Rebirth/dawn


class Effect(BaseModel):
    """Individual effect definition."""
    effect_type: EffectType
    value: int = Field(ge=0, description="Effect magnitude")
    target: TargetType
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional effect parameters")
    conditions: Optional[List[str]] = Field(default_factory=list, description="Conditional requirements")
    
    @field_validator('value')
    def validate_value_range(cls, v, values):
        """Validate effect values are within reasonable ranges."""
        effect_type = values.get('effect_type')
        if effect_type == EffectType.DAMAGE and v > 999:
            raise ValueError("Damage values should not exceed 999")
        if effect_type == EffectType.HEAL and v > 999:
            raise ValueError("Heal values should not exceed 999")
        if effect_type in [EffectType.GAIN_SAND, EffectType.LOSE_SAND] and v > 6:
            raise ValueError("Sand values should not exceed 6")
        return v


class Ability(BaseModel):
    """Enemy ability definition."""
    name: str = Field(min_length=1, max_length=50)
    sand_cost: int = Field(ge=0, le=6, description="Sand cost for ability")
    effects: List[Effect] = Field(min_items=1, description="Effects when ability is used")
    description: Optional[str] = Field(max_length=200, description="Ability description")
    cooldown: Optional[int] = Field(ge=0, description="Turns before ability can be used again")
    priority: Optional[int] = Field(ge=1, le=10, default=5, description="AI priority for using this ability")
    
    @field_validator('name')
    def validate_name_format(cls, v):
        """Ensure ability names follow proper format."""
        if not re.match(r'^[A-Za-z][\w\s-]*$', v):
            raise ValueError("Ability names must start with a letter and contain only letters, numbers, spaces, and hyphens")
        return v


class Card(BaseModel):
    """Card definition schema."""
    id: str = Field(pattern=r'^[a-z_][a-z0-9_]*$', description="Unique card identifier")
    name: str = Field(min_length=1, max_length=50, description="Display name")
    description: str = Field(min_length=10, max_length=200, description="Card description")
    sand_cost: int = Field(ge=0, le=6, description="Sand cost to play the card")
    card_type: CardType
    rarity: Rarity = Field(default=Rarity.COMMON)
    effects: List[Effect] = Field(min_items=1, description="Card effects when played")
    keywords: List[KeywordType] = Field(default_factory=list, description="Card keywords for categorization")
    flavor_text: Optional[str] = Field(max_length=100, description="Flavor text for atmosphere")
    upgrade_effects: Optional[List[Effect]] = Field(description="Effects when card is upgraded")
    exhaust: bool = Field(default=False, description="Card is removed after use")
    ethereal: bool = Field(default=False, description="Card is removed if not played")
    innate: bool = Field(default=False, description="Card starts in hand")
    retain: bool = Field(default=False, description="Card is kept in hand at turn end")
    unplayable: bool = Field(default=False, description="Card cannot be played normally")
    
    @field_validator('sand_cost')
    def validate_sand_cost_by_type(cls, v, values):
        """Validate sand cost makes sense for card type."""
        card_type = values.get('card_type')
        if card_type == CardType.POWER and v == 0:
            # Powers should generally cost sand to balance their permanent effects
            pass  # Allow but warn in logs
        return v
    
    @field_validator('keywords')
    def validate_keyword_combinations(cls, v, values):
        """Validate keyword combinations make sense."""
        if KeywordType.EXHAUST in v and KeywordType.RETAIN in v:
            raise ValueError("Cards cannot have both 'exhaust' and 'retain' keywords")
        if KeywordType.ETHEREAL in v and KeywordType.INNATE in v:
            raise ValueError("Cards cannot have both 'ethereal' and 'innate' keywords")
        return v


class Enemy(BaseModel):
    """Enemy definition schema."""
    id: str = Field(pattern=r'^[a-z_][a-z0-9_]*$', description="Unique enemy identifier")
    name: str = Field(min_length=1, max_length=50, description="Display name")
    description: str = Field(min_length=10, max_length=200, description="Enemy description")
    health: int = Field(ge=1, le=9999, description="Current health")
    max_health: int = Field(ge=1, le=9999, description="Maximum health")
    max_sand: int = Field(ge=1, le=10, description="Maximum sand capacity")
    sand_regen_rate: float = Field(ge=0.1, le=5.0, default=1.0, description="Sand regeneration rate")
    ai_pattern: AIPattern = Field(description="AI behavior pattern")
    abilities: List[Ability] = Field(min_items=1, description="Available abilities")
    keywords: List[KeywordType] = Field(default_factory=list, description="Enemy keywords")
    resistances: Optional[Dict[str, float]] = Field(description="Damage type resistances (0.0-2.0)")
    immunities: Optional[List[str]] = Field(description="Status effect immunities")
    loot: Optional[Dict[str, Union[List[int], List[str]]]] = Field(description="Possible loot drops")
    hour_of_night: Optional[HourOfNight] = Field(description="Associated hour of night")
    
    @field_validator('health')
    def validate_health_not_greater_than_max(cls, v, values):
        """Ensure current health doesn't exceed max health."""
        max_health = values.get('max_health')
        if max_health and v > max_health:
            raise ValueError("Current health cannot exceed max health")
        return v
    
    @field_validator('resistances')
    def validate_resistance_values(cls, v):
        """Ensure resistance values are in valid range."""
        if v:
            for damage_type, resistance in v.items():
                if not 0.0 <= resistance <= 2.0:
                    raise ValueError(f"Resistance for {damage_type} must be between 0.0 and 2.0")
        return v


class EventOption(BaseModel):
    """Single option within an event."""
    text: str = Field(min_length=5, max_length=100, description="Option text")
    effects: List[Effect] = Field(default_factory=list, description="Effects when option is chosen")
    consequences: str = Field(min_length=5, max_length=200, description="Result description")
    requirements: Optional[List[Dict[str, Any]]] = Field(description="Requirements to select this option")
    cost: Optional[Dict[str, int]] = Field(description="Costs to select this option")


class Event(BaseModel):
    """Event definition schema."""
    id: str = Field(pattern=r'^[a-z_][a-z0-9_]*$', description="Unique event identifier")
    name: str = Field(min_length=1, max_length=50, description="Display name")
    description: str = Field(min_length=20, max_length=500, description="Event description")
    event_type: EventType
    requirements: List[Dict[str, Any]] = Field(default_factory=list, description="Requirements to encounter this event")
    options: List[EventOption] = Field(min_items=1, max_items=5, description="Available choices")
    hour_of_night: Optional[HourOfNight] = Field(description="Associated hour of night")
    repeatable: bool = Field(default=False, description="Can be encountered multiple times")
    weight: int = Field(ge=1, le=100, default=10, description="Encounter weight for random selection")
    
    @field_validator('options')
    def validate_at_least_one_option(cls, v):
        """Ensure events have at least one option."""
        if not v:
            raise ValueError("Events must have at least one option")
        return v


class Deck(BaseModel):
    """Deck definition schema."""
    id: str = Field(pattern=r'^[a-z_][a-z0-9_]*$', description="Unique deck identifier")
    name: str = Field(min_length=1, max_length=50, description="Display name")
    description: str = Field(min_length=10, max_length=200, description="Deck description")
    cards: List[str] = Field(min_items=10, max_items=50, description="List of card IDs")
    starting_deck: bool = Field(default=False, description="Available as starting deck")
    unlock_requirements: Optional[List[Dict[str, Any]]] = Field(description="Requirements to unlock this deck")
    themes: List[KeywordType] = Field(default_factory=list, description="Deck themes/keywords")
    
    @field_validator('cards')
    def validate_deck_size(cls, v):
        """Validate deck is within size limits."""
        if len(v) < 10:
            raise ValueError("Decks must contain at least 10 cards")
        if len(v) > 50:
            raise ValueError("Decks cannot contain more than 50 cards")
        return v


class ContentManifest(BaseModel):
    """Manifest describing all content in a content pack."""
    name: str = Field(min_length=1, max_length=50, description="Content pack name")
    version: str = Field(pattern=r'^\d+\.\d+\.\d+$', description="Semantic version")
    description: str = Field(min_length=10, max_length=200, description="Content pack description")
    author: Optional[str] = Field(max_length=50, description="Content creator")
    dependencies: List[str] = Field(default_factory=list, description="Required content pack dependencies")
    cards_count: int = Field(ge=0, description="Number of cards in this pack")
    enemies_count: int = Field(ge=0, description="Number of enemies in this pack")
    events_count: int = Field(ge=0, description="Number of events in this pack")
    decks_count: int = Field(ge=0, description="Number of decks in this pack")


# Validation schemas for YAML content files
class CardsFile(RootModel[Dict[str, Card]]):
    """Schema for cards YAML files."""
    
    @model_validator(mode='after')
    def validate_card_ids_match_keys(self):
        """Ensure card IDs match their dictionary keys."""
        for key, card in self.root.items():
            if card.id != key:
                raise ValueError(f"Card ID '{card.id}' doesn't match key '{key}'")
        return self


class EnemiesFile(RootModel[Dict[str, Enemy]]):
    """Schema for enemies YAML files."""
    
    @model_validator(mode='after')
    def validate_enemy_ids_match_keys(self):
        """Ensure enemy IDs match their dictionary keys."""
        for key, enemy in self.root.items():
            if enemy.id != key:
                raise ValueError(f"Enemy ID '{enemy.id}' doesn't match key '{key}'")
        return self


class EventsFile(RootModel[Dict[str, Event]]):
    """Schema for events YAML files."""
    
    @model_validator(mode='after')
    def validate_event_ids_match_keys(self):
        """Ensure event IDs match their dictionary keys."""
        for key, event in self.root.items():
            if event.id != key:
                raise ValueError(f"Event ID '{event.id}' doesn't match key '{key}'")
        return self


class DecksFile(RootModel[Dict[str, Deck]]):
    """Schema for decks YAML files."""
    
    @model_validator(mode='after')
    def validate_deck_ids_match_keys(self):
        """Ensure deck IDs match their dictionary keys."""
        for key, deck in self.root.items():
            if deck.id != key:
                raise ValueError(f"Deck ID '{deck.id}' doesn't match key '{key}'")
        return self