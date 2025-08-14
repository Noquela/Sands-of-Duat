"""
Deck Manager - Simple global deck persistence system
Connects deck builder to combat system.
"""

from typing import List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

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
    
    def get_default_deck(self) -> List[DeckCard]:
        """Get enhanced default deck with expansion cards."""
        return [
            # Egyptian Gods
            DeckCard("Ra, Sun God", 5, 6, 8, "legendary", "Powerful Egyptian sun deity", "god"),
            DeckCard("Anubis Judge", 4, 5, 6, "epic", "Guardian of the afterlife", "god"),
            DeckCard("Horus, Lord of the Sky", 7, 8, 10, "legendary", "Divine falcon god", "god"),
            
            # Creatures  
            DeckCard("Egyptian Warrior", 3, 4, 4, "rare", "Skilled desert fighter", "creature"),
            DeckCard("Sacred Scarab", 2, 2, 3, "common", "Divine favor beetle", "creature"),
            DeckCard("Desert Phoenix", 5, 6, 4, "epic", "Mythical firebird", "creature"),
            DeckCard("Anubis Jackal", 4, 4, 5, "rare", "Underworld guardian", "creature"),
            DeckCard("Mummy Guardian", 2, 2, 5, "common", "Undead protector", "creature"),
            
            # Spells & Artifacts
            DeckCard("Pharaoh's Wrath", 4, 0, 0, "epic", "Divine punishment", "spell"),
            DeckCard("Ankh of Eternal Life", 6, 0, 0, "legendary", "Symbol of eternity", "artifact"),
        ]
    
    def get_expansion_collection(self) -> List[DeckCard]:
        """Get complete card collection for deck building."""
        collection = []
        
        # All Egyptian Gods
        gods = [
            DeckCard("Ra, Sun God", 5, 6, 8, "legendary", "Solar deity with divine power", "god"),
            DeckCard("Anubis Judge", 4, 5, 6, "epic", "Judge of the dead", "god"),
            DeckCard("Isis Healer", 4, 2, 7, "epic", "Divine healing magic", "god"),
            DeckCard("Horus, Lord of the Sky", 7, 8, 10, "legendary", "Falcon god of sky", "god"),
            DeckCard("Bastet, Cat Goddess", 5, 6, 8, "legendary", "Feline protector", "god"),
            DeckCard("Thoth, Keeper of Wisdom", 6, 5, 9, "legendary", "God of knowledge", "god"),
        ]
        
        # Mythological Creatures
        creatures = [
            DeckCard("Egyptian Warrior", 3, 4, 4, "rare", "Elite desert fighter", "creature"),
            DeckCard("Sacred Scarab", 2, 2, 3, "common", "Divine favor insect", "creature"),
            DeckCard("Desert Phoenix", 5, 6, 4, "epic", "Reborn from flames", "creature"),
            DeckCard("Anubis Jackal", 4, 4, 5, "rare", "Death guardian", "creature"),
            DeckCard("Mummy Guardian", 2, 2, 5, "common", "Undead sentinel", "creature"),
            DeckCard("Sphinx Guardian", 3, 3, 6, "rare", "Riddle keeper", "creature"),
        ]
        
        # Powerful Spells
        spells = [
            DeckCard("Pharaoh's Wrath", 4, 0, 0, "epic", "Royal divine punishment", "spell"),
            DeckCard("Curse of the Desert", 3, 0, 0, "rare", "Sand storm curse", "spell"),
            DeckCard("Divine Blessing", 2, 0, 0, "common", "God's favor", "spell"),
        ]
        
        # Sacred Artifacts
        artifacts = [
            DeckCard("Ankh of Eternal Life", 6, 0, 0, "legendary", "Eternal resurrection", "artifact"),
            DeckCard("Eye of Horus", 4, 0, 0, "epic", "Divine protection", "artifact"),
            DeckCard("Pharaoh's Scepter", 3, 0, 0, "rare", "Royal command", "artifact"),
        ]
        
        collection.extend(gods)
        collection.extend(creatures)
        collection.extend(spells)
        collection.extend(artifacts)
        
        logger.info(f"Loaded {len(collection)} cards in expansion collection")
        return collection

# Global singleton instance
deck_manager = DeckManager()