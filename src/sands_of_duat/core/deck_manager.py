"""
Deck Manager - Simple global deck persistence system
Connects deck builder to combat system.
"""

from typing import List, Optional
from dataclasses import dataclass

@dataclass
class DeckCard:
    """Simple deck card data for persistence."""
    name: str
    cost: int
    attack: int
    health: int
    rarity: str
    description: str
    card_type: str = "creature"

class DeckManager:
    """Global deck persistence manager."""
    
    _instance: Optional['DeckManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialized', False):
            self.player_deck: List[DeckCard] = []
            self.has_custom_deck = False
            self._initialized = True
    
    def save_deck(self, deck_cards: List) -> bool:
        """Save deck from deck builder."""
        try:
            self.player_deck.clear()
            
            for card in deck_cards:
                deck_card = DeckCard(
                    name=card.data.name,
                    cost=card.data.cost,
                    attack=card.data.attack,
                    health=card.data.health,
                    rarity=card.data.rarity,
                    description=card.data.description,
                    card_type=getattr(card.data, 'card_type', 'creature')
                )
                self.player_deck.append(deck_card)
            
            self.has_custom_deck = len(self.player_deck) > 0
            print(f"Deck saved: {len(self.player_deck)} cards")
            return True
            
        except Exception as e:
            print(f"Failed to save deck: {e}")
            return False
    
    def get_player_deck(self) -> List[DeckCard]:
        """Get saved player deck."""
        return self.player_deck.copy()
    
    def has_saved_deck(self) -> bool:
        """Check if player has a saved deck."""
        return self.has_custom_deck and len(self.player_deck) > 0
    
    def clear_deck(self):
        """Clear saved deck."""
        self.player_deck.clear()
        self.has_custom_deck = False
        print("Deck cleared")
    
    def get_deck_summary(self) -> str:
        """Get deck summary for display."""
        if not self.has_saved_deck():
            return "No custom deck"
        
        return f"Custom deck: {len(self.player_deck)} cards"

# Global singleton instance
deck_manager = DeckManager()