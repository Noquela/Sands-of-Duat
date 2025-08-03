#!/usr/bin/env python3
"""
Egyptian Card Loader

Loads the comprehensive Egyptian mythology cards from YAML into the game system.
Integrates with the existing card system to provide rich thematic content.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..core.cards import Card, CardEffect, CardType, CardRarity, EffectType, TargetType, card_library


class EgyptianCardLoader:
    """Loads and processes Egyptian-themed cards from YAML configuration."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cards_path = Path(__file__).parent / "cards" / "egyptian_cards.yaml"
    
    def load_egyptian_cards(self) -> Dict[str, Card]:
        """Load all Egyptian cards from YAML file."""
        if not self.cards_path.exists():
            self.logger.error(f"Egyptian cards file not found: {self.cards_path}")
            return {}
        
        try:
            with open(self.cards_path, 'r', encoding='utf-8') as file:
                card_data = yaml.safe_load(file)
            
            cards = {}
            for card_id, card_info in card_data.items():
                if card_info:  # Skip empty entries
                    card = self._create_card_from_yaml(card_id, card_info)
                    if card:
                        cards[card_id] = card
                        # Add to global card library
                        card_library.register_card(card)
            
            self.logger.info(f"Loaded {len(cards)} Egyptian cards")
            return cards
            
        except Exception as e:
            self.logger.error(f"Error loading Egyptian cards: {e}")
            return {}
    
    def _create_card_from_yaml(self, card_id: str, card_info: Dict[str, Any]) -> Optional[Card]:
        """Create a Card object from YAML data."""
        try:
            # Map YAML fields to Card fields
            card_type = self._map_card_type(card_info.get('card_type', 'skill'))
            rarity = self._map_rarity(card_info.get('rarity', 'common'))
            
            # Create card effects
            effects = []
            if 'effects' in card_info:
                for effect_data in card_info['effects']:
                    effect = self._create_effect_from_yaml(effect_data)
                    if effect:
                        effects.append(effect)
            
            # Create the card
            card = Card(
                id=card_info['id'],
                name=card_info['name'],
                description=card_info['description'],
                sand_cost=card_info.get('sand_cost', 1),
                card_type=card_type,
                rarity=rarity,
                effects=effects,
                keywords=card_info.get('keywords', []),
                flavor_text=card_info.get('flavor_text', ''),
                exhaust=card_info.get('exhaust', False),
                retain=card_info.get('retain', False),
                ethereal=card_info.get('ethereal', False)
            )
            
            return card
            
        except Exception as e:
            self.logger.error(f"Error creating card {card_id}: {e}")
            return None
    
    def _create_effect_from_yaml(self, effect_data: Dict[str, Any]) -> Optional[CardEffect]:
        """Create a CardEffect from YAML effect data."""
        try:
            effect_type = self._map_effect_type(effect_data['effect_type'])
            target_type = self._map_target_type(effect_data.get('target', 'self'))
            
            effect = CardEffect(
                effect_type=effect_type,
                value=effect_data.get('value', 0),
                target=target_type,
                metadata=effect_data.get('metadata', {})
            )
            
            return effect
            
        except Exception as e:
            self.logger.error(f"Error creating effect: {e}")
            return None
    
    def _map_card_type(self, type_str: str) -> CardType:
        """Map YAML card type string to CardType enum."""
        type_mapping = {
            'attack': CardType.ATTACK,
            'skill': CardType.SKILL,
            'power': CardType.POWER,
            'curse': CardType.CURSE,
            'status': CardType.STATUS
        }
        return type_mapping.get(type_str.lower(), CardType.SKILL)
    
    def _map_rarity(self, rarity_str: str) -> CardRarity:
        """Map YAML rarity string to CardRarity enum."""
        rarity_mapping = {
            'common': CardRarity.COMMON,
            'uncommon': CardRarity.UNCOMMON,
            'rare': CardRarity.RARE,
            'epic': CardRarity.EPIC,
            'legendary': CardRarity.LEGENDARY
        }
        return rarity_mapping.get(rarity_str.lower(), CardRarity.COMMON)
    
    def _map_effect_type(self, effect_str: str) -> EffectType:
        """Map YAML effect type string to EffectType enum."""
        # Basic effect mappings
        effect_mapping = {
            'damage': EffectType.DAMAGE,
            'heal': EffectType.HEAL,
            'block': EffectType.BLOCK,
            'draw_cards': EffectType.DRAW_CARDS,
            'gain_sand': EffectType.GAIN_ENERGY,  # Map to existing energy system
            'apply_vulnerable': EffectType.APPLY_VULNERABLE,
            'apply_weak': EffectType.APPLY_WEAK,
            'apply_strength': EffectType.APPLY_STRENGTH,
            'apply_dexterity': EffectType.APPLY_DEXTERITY,
            'max_health_increase': EffectType.MAX_HEALTH_INCREASE
        }
        
        # Handle special Egyptian effects
        special_effects = {
            'permanent_sand_increase': EffectType.PERMANENT_SAND_INCREASE,
            'channel_divinity': EffectType.CHANNEL_DIVINITY,
            'blessing': EffectType.BLESSING,
            'discover_card': EffectType.DRAW_CARDS,
            'gain_card': EffectType.SPECIAL,
            'lose_gold': EffectType.SPECIAL,
            'upgrade_card': EffectType.SPECIAL
        }
        
        # Try basic mapping first, then special effects
        return effect_mapping.get(effect_str, special_effects.get(effect_str, EffectType.SPECIAL))
    
    def _map_target_type(self, target_str: str) -> TargetType:
        """Map YAML target string to TargetType enum."""
        target_mapping = {
            'self': TargetType.SELF,
            'enemy': TargetType.ENEMY,
            'all_enemies': TargetType.ALL_ENEMIES,
            'any': TargetType.ANY,
            'none': TargetType.NONE
        }
        return target_mapping.get(target_str.lower(), TargetType.SELF)


def initialize_egyptian_cards() -> Dict[str, Card]:
    """Initialize and load all Egyptian cards into the game."""
    loader = EgyptianCardLoader()
    return loader.load_egyptian_cards()


# Convenience function for other modules
def get_egyptian_card_by_id(card_id: str) -> Optional[Card]:
    """Get a specific Egyptian card by its ID."""
    return card_library.get_card_by_id(card_id)


def get_egyptian_cards_by_cost(sand_cost: int) -> List[Card]:
    """Get all Egyptian cards with a specific sand cost."""
    return [card for card in card_library.get_all_cards() 
            if card.sand_cost == sand_cost and 'divine' in card.keywords]


def get_egyptian_cards_by_rarity(rarity: CardRarity) -> List[Card]:
    """Get all Egyptian cards of a specific rarity."""
    return [card for card in card_library.get_all_cards() 
            if card.rarity == rarity and any(keyword in card.keywords for keyword in ['divine', 'pharaoh', 'egyptian'])]