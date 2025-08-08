"""
Sands of Duat Card System

This module provides the complete Egyptian mythology-based card system including:
- Core card data structures and Ba-Ka soul system
- Egyptian god cards with authentic mythology
- Artifact cards representing sacred objects
- Spell cards for magical effects
- Comprehensive card database and management

The Ba-Ka system is central to gameplay, allowing separation of soul (Ba) and life force (Ka)
for complex strategic interactions based on ancient Egyptian beliefs about the afterlife.
"""

# Core card system
from .card import (
    Card,
    CardType,
    CardRarity, 
    CardElement,
    CardKeyword,
    CardStats,
    CardEffect,
    BaKaSystem
)

# Egyptian card collections
from .egyptian_gods import (
    get_all_god_cards,
    get_god_card_by_id,
    get_gods_by_element,
    get_gods_by_rarity,
    EGYPTIAN_GOD_CARDS
)

from .egyptian_artifacts import (
    get_all_artifact_cards,
    get_artifact_by_id,
    EGYPTIAN_ARTIFACT_CARDS
)

from .egyptian_spells import (
    get_all_spell_cards,
    get_spell_by_id,
    EGYPTIAN_SPELL_CARDS
)

# Database and management
from .collections.card_database import (
    CardDatabase,
    get_card_database,
    get_card,
    get_all_cards,
    search_cards
)

__all__ = [
    # Core system
    'Card',
    'CardType',
    'CardRarity',
    'CardElement', 
    'CardKeyword',
    'CardStats',
    'CardEffect',
    'BaKaSystem',
    
    # God cards
    'get_all_god_cards',
    'get_god_card_by_id', 
    'get_gods_by_element',
    'get_gods_by_rarity',
    'EGYPTIAN_GOD_CARDS',
    
    # Artifact cards
    'get_all_artifact_cards',
    'get_artifact_by_id',
    'EGYPTIAN_ARTIFACT_CARDS',
    
    # Spell cards
    'get_all_spell_cards',
    'get_spell_by_id', 
    'EGYPTIAN_SPELL_CARDS',
    
    # Database
    'CardDatabase',
    'get_card_database',
    'get_card',
    'get_all_cards',
    'search_cards'
]