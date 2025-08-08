"""
Card Database - Central system for loading, managing, and accessing all cards.
Integrates with high-quality Egyptian artwork and provides comprehensive card management.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Callable
from dataclasses import asdict

from ..card import Card, CardType, CardRarity, CardElement, CardKeyword
from ..egyptian_gods import EGYPTIAN_GOD_CARDS, get_all_god_cards
from ..egyptian_artifacts import EGYPTIAN_ARTIFACT_CARDS, get_all_artifact_cards
from ..egyptian_spells import EGYPTIAN_SPELL_CARDS, get_all_spell_cards


class CardDatabase:
    """
    Central database for all cards in Sands of Duat.
    Handles loading, caching, filtering, and asset management.
    """
    
    def __init__(self, assets_path: Optional[Path] = None):
        """Initialize the card database."""
        self.assets_path = assets_path or Path("assets/images/lora_training/final_dataset")
        self._cards: Dict[str, Card] = {}
        self._card_factories: Dict[str, Callable[[], Card]] = {}
        self._loaded = False
        
        # Register all card factories
        self._register_card_factories()
    
    def _register_card_factories(self):
        """Register all card creation functions."""
        # Register god cards
        self._card_factories.update(EGYPTIAN_GOD_CARDS)
        
        # Register artifact cards
        self._card_factories.update(EGYPTIAN_ARTIFACT_CARDS)
        
        # Register spell cards
        self._card_factories.update(EGYPTIAN_SPELL_CARDS)
    
    def load_all_cards(self) -> bool:
        """Load all cards into memory."""
        try:
            self._cards.clear()
            
            # Load all registered cards
            for card_id, factory in self._card_factories.items():
                card = factory()
                self._cards[card_id] = card
            
            self._loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading cards: {e}")
            return False
    
    def get_card(self, card_id: str) -> Optional[Card]:
        """Get a card by ID, loading it if necessary."""
        if not self._loaded:
            self.load_all_cards()
        
        if card_id in self._cards:
            # Return a fresh instance to avoid shared state issues
            return self._card_factories[card_id]()
        
        return None
    
    def get_all_cards(self) -> List[Card]:
        """Get all available cards."""
        if not self._loaded:
            self.load_all_cards()
        
        # Return fresh instances
        return [factory() for factory in self._card_factories.values()]
    
    def get_cards_by_type(self, card_type: CardType) -> List[Card]:
        """Get all cards of a specific type."""
        return [card for card in self.get_all_cards() if card.card_type == card_type]
    
    def get_cards_by_element(self, element: CardElement) -> List[Card]:
        """Get all cards of a specific element."""
        return [card for card in self.get_all_cards() if card.element == element]
    
    def get_cards_by_rarity(self, rarity: CardRarity) -> List[Card]:
        """Get all cards of a specific rarity."""
        return [card for card in self.get_all_cards() if card.rarity == rarity]
    
    def get_cards_with_keyword(self, keyword: CardKeyword) -> List[Card]:
        """Get all cards with a specific keyword."""
        return [card for card in self.get_all_cards() if keyword in card.keywords]
    
    def get_cards_by_name(self, name_pattern: str) -> List[Card]:
        """Get cards whose names contain the given pattern (case-insensitive)."""
        pattern = name_pattern.lower()
        return [card for card in self.get_all_cards() if pattern in card.name.lower()]
    
    def get_divine_cards(self) -> List[Card]:
        """Get all divine-tier cards (gods and legendary artifacts)."""
        return [
            card for card in self.get_all_cards() 
            if card.rarity in [CardRarity.LEGENDARY, CardRarity.MYTHIC, CardRarity.DIVINE]
        ]
    
    def get_ba_ka_cards(self) -> List[Card]:
        """Get all cards that interact with the Ba-Ka system."""
        ba_ka_keywords = {
            CardKeyword.BA_SEPARATION,
            CardKeyword.KA_BINDING,
            CardKeyword.SOUL_LINK,
            CardKeyword.AFTERLIFE,
            CardKeyword.JUDGMENT
        }
        
        return [
            card for card in self.get_all_cards()
            if any(keyword in card.keywords for keyword in ba_ka_keywords) or
            any(effect.ba_ka_interaction for effect in card.effects)
        ]
    
    def get_cards_for_deck_building(self, 
                                   max_cost: int = 10,
                                   elements: Optional[Set[CardElement]] = None,
                                   rarities: Optional[Set[CardRarity]] = None) -> List[Card]:
        """Get cards suitable for deck building with filters."""
        cards = self.get_all_cards()
        
        # Filter by mana cost
        cards = [card for card in cards if card.stats.mana_cost <= max_cost]
        
        # Filter by elements
        if elements:
            cards = [card for card in cards if card.element in elements]
        
        # Filter by rarities
        if rarities:
            cards = [card for card in cards if card.rarity in rarities]
        
        return sorted(cards, key=lambda c: (c.stats.mana_cost, c.name))
    
    def get_card_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the card collection."""
        all_cards = self.get_all_cards()
        
        if not all_cards:
            return {}
        
        # Count by type
        type_counts = {}
        for card_type in CardType:
            type_counts[card_type.value] = len(self.get_cards_by_type(card_type))
        
        # Count by rarity
        rarity_counts = {}
        for rarity in CardRarity:
            rarity_counts[rarity.value] = len(self.get_cards_by_rarity(rarity))
        
        # Count by element
        element_counts = {}
        for element in CardElement:
            element_counts[element.value] = len(self.get_cards_by_element(element))
        
        # Mana cost distribution
        mana_costs = [card.stats.mana_cost for card in all_cards]
        avg_mana_cost = sum(mana_costs) / len(mana_costs) if mana_costs else 0
        
        # Ba-Ka system usage
        ba_ka_cards = len(self.get_ba_ka_cards())
        
        return {
            "total_cards": len(all_cards),
            "by_type": type_counts,
            "by_rarity": rarity_counts,
            "by_element": element_counts,
            "average_mana_cost": round(avg_mana_cost, 2),
            "ba_ka_system_cards": ba_ka_cards,
            "ba_ka_percentage": round((ba_ka_cards / len(all_cards)) * 100, 1)
        }
    
    def validate_card_assets(self) -> Dict[str, Any]:
        """Validate that all cards have proper asset files."""
        validation_report = {
            "total_cards": 0,
            "cards_with_assets": 0,
            "missing_assets": [],
            "asset_qualities": {},
            "validation_passed": True
        }
        
        all_cards = self.get_all_cards()
        validation_report["total_cards"] = len(all_cards)
        
        for card in all_cards:
            if card.image_path and card.image_path.exists():
                validation_report["cards_with_assets"] += 1
                if card.image_quality:
                    quality_range = f"{card.image_quality//10*10}-{card.image_quality//10*10+9}"
                    validation_report["asset_qualities"][quality_range] = \
                        validation_report["asset_qualities"].get(quality_range, 0) + 1
            else:
                validation_report["missing_assets"].append({
                    "card_id": card.card_id,
                    "name": card.name,
                    "expected_path": str(card.image_path) if card.image_path else "No path specified"
                })
                validation_report["validation_passed"] = False
        
        return validation_report
    
    def export_to_json(self, output_path: Path) -> bool:
        """Export all cards to JSON format."""
        try:
            all_cards = self.get_all_cards()
            cards_data = {
                "metadata": {
                    "game": "Sands of Duat",
                    "total_cards": len(all_cards),
                    "export_timestamp": "2025-08-08",  # Current date from env
                    "version": "1.0.0"
                },
                "cards": [card.to_dict() for card in all_cards]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cards_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting cards to JSON: {e}")
            return False
    
    def import_from_json(self, json_path: Path) -> bool:
        """Import cards from JSON format (for custom cards or updates)."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cards_data = data.get("cards", [])
            
            for card_data in cards_data:
                card = Card.from_dict(card_data)
                # Create a factory function for this card
                self._card_factories[card.card_id] = lambda c=card: Card.from_dict(c.to_dict())
            
            # Reload all cards
            return self.load_all_cards()
            
        except Exception as e:
            print(f"Error importing cards from JSON: {e}")
            return False
    
    def search_cards(self, 
                    query: str,
                    search_fields: Optional[List[str]] = None) -> List[Card]:
        """
        Advanced card search across multiple fields.
        
        Args:
            query: Search query string
            search_fields: Fields to search in ['name', 'description', 'flavor_text', 'mythology_source']
        """
        if search_fields is None:
            search_fields = ['name', 'description', 'flavor_text']
        
        query = query.lower()
        matching_cards = []
        
        for card in self.get_all_cards():
            for field in search_fields:
                field_value = getattr(card, field, "").lower()
                if query in field_value:
                    matching_cards.append(card)
                    break  # Avoid duplicate matches
        
        return matching_cards
    
    def get_card_synergies(self, card: Card) -> List[Card]:
        """Find cards that synergize well with the given card."""
        synergistic_cards = []
        all_cards = [c for c in self.get_all_cards() if c.card_id != card.card_id]
        
        for other_card in all_cards:
            synergy_score = 0
            
            # Same element bonus
            if card.element == other_card.element:
                synergy_score += 1
            
            # Elemental synergy bonus
            synergy_multiplier = card.get_element_synergy(other_card.element)
            if synergy_multiplier > 1.0:
                synergy_score += 2
            
            # Keyword synergies
            shared_keywords = card.keywords.intersection(other_card.keywords)
            synergy_score += len(shared_keywords)
            
            # Ba-Ka system interactions
            if any(effect.ba_ka_interaction for effect in card.effects + other_card.effects):
                synergy_score += 1
            
            # Special synergies (e.g., pharaoh bonds, divine protection)
            if CardKeyword.PHARAOH_BOND in card.keywords or CardKeyword.PHARAOH_BOND in other_card.keywords:
                if card.card_type == CardType.DEITY or other_card.card_type == CardType.DEITY:
                    synergy_score += 2
            
            # Add to synergistic cards if score is high enough
            if synergy_score >= 2:
                synergistic_cards.append(other_card)
        
        # Sort by synergy potential (element, keywords, etc.)
        return sorted(synergistic_cards, 
                     key=lambda c: (c.element == card.element, len(c.keywords.intersection(card.keywords))),
                     reverse=True)


# Global card database instance
_card_database = None

def get_card_database() -> CardDatabase:
    """Get the global card database instance."""
    global _card_database
    if _card_database is None:
        _card_database = CardDatabase()
    return _card_database


# Convenience functions for easy access
def get_card(card_id: str) -> Optional[Card]:
    """Get a card by ID."""
    return get_card_database().get_card(card_id)


def get_all_cards() -> List[Card]:
    """Get all available cards."""
    return get_card_database().get_all_cards()


def search_cards(query: str) -> List[Card]:
    """Search for cards by name, description, or flavor text."""
    return get_card_database().search_cards(query)