"""
Deck Collection Manager - Enhanced deck persistence with multiple saved decks.
Integrates with the save system to provide persistent deck collections.
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

from .deck_manager import DeckCard
from .save_system import save_system

@dataclass
class SavedDeck:
    """A saved deck with metadata."""
    name: str
    cards: List[DeckCard]
    created_date: str
    last_modified: str
    total_cards: int
    win_rate: float = 0.0
    games_played: int = 0
    description: str = ""
    favorite: bool = False

class DeckCollectionManager:
    """
    Enhanced deck management with multiple saved decks.
    Provides persistent storage and collection management.
    """
    
    def __init__(self):
        """Initialize the deck collection manager."""
        self.collection: Dict[str, SavedDeck] = {}
        self.current_deck_name: Optional[str] = None
        
        # Create decks directory
        self.decks_dir = Path("save_games") / "decks"
        self.decks_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing decks
        self.load_all_decks()
        
        # Create default starter deck if none exist
        if not self.collection:
            self._create_starter_deck()
        
        print(f"Deck Collection Manager initialized with {len(self.collection)} saved decks")
    
    def save_deck(self, name: str, cards: List[DeckCard], description: str = "") -> bool:
        """
        Save a deck to the collection.
        
        Args:
            name: Name of the deck
            cards: List of cards in the deck
            description: Optional description
            
        Returns:
            True if saved successfully
        """
        try:
            current_time = datetime.now().isoformat()
            
            # Create or update deck
            if name in self.collection:
                deck = self.collection[name]
                deck.cards = cards.copy()
                deck.last_modified = current_time
                deck.total_cards = len(cards)
                deck.description = description
                print(f"Updated existing deck: {name}")
            else:
                deck = SavedDeck(
                    name=name,
                    cards=cards.copy(),
                    created_date=current_time,
                    last_modified=current_time,
                    total_cards=len(cards),
                    description=description
                )
                self.collection[name] = deck
                print(f"Created new deck: {name}")
            
            # Save to file
            self._save_deck_to_file(deck)
            
            # Set as current deck
            self.current_deck_name = name
            
            return True
            
        except Exception as e:
            print(f"Failed to save deck '{name}': {e}")
            return False
    
    def load_deck(self, name: str) -> Optional[List[DeckCard]]:
        """
        Load a deck from the collection.
        
        Args:
            name: Name of the deck to load
            
        Returns:
            List of cards or None if not found
        """
        if name not in self.collection:
            print(f"Deck not found: {name}")
            return None
        
        self.current_deck_name = name
        deck = self.collection[name]
        print(f"Loaded deck: {name} ({len(deck.cards)} cards)")
        return deck.cards.copy()
    
    def delete_deck(self, name: str) -> bool:
        """
        Delete a deck from the collection.
        
        Args:
            name: Name of the deck to delete
            
        Returns:
            True if deleted successfully
        """
        if name not in self.collection:
            return False
        
        try:
            # Remove from collection
            del self.collection[name]
            
            # Remove file
            deck_file = self.decks_dir / f"{name.replace(' ', '_').lower()}.json"
            if deck_file.exists():
                deck_file.unlink()
            
            # Clear current deck if it was deleted
            if self.current_deck_name == name:
                self.current_deck_name = None
            
            print(f"Deleted deck: {name}")
            return True
            
        except Exception as e:
            print(f"Failed to delete deck '{name}': {e}")
            return False
    
    def get_all_deck_names(self) -> List[str]:
        """Get names of all saved decks."""
        return list(self.collection.keys())
    
    def get_deck_info(self, name: str) -> Optional[SavedDeck]:
        """Get information about a specific deck."""
        return self.collection.get(name)
    
    def get_current_deck(self) -> Optional[List[DeckCard]]:
        """Get the currently selected deck."""
        if not self.current_deck_name:
            return None
        return self.load_deck(self.current_deck_name)
    
    def update_deck_stats(self, name: str, won: bool):
        """
        Update win/loss statistics for a deck.
        
        Args:
            name: Name of the deck
            won: Whether the game was won
        """
        if name not in self.collection:
            return
        
        deck = self.collection[name]
        deck.games_played += 1
        
        if won:
            deck.win_rate = ((deck.win_rate * (deck.games_played - 1)) + 1.0) / deck.games_played
        else:
            deck.win_rate = (deck.win_rate * (deck.games_played - 1)) / deck.games_played
        
        deck.last_modified = datetime.now().isoformat()
        self._save_deck_to_file(deck)
    
    def toggle_favorite(self, name: str) -> bool:
        """
        Toggle favorite status of a deck.
        
        Args:
            name: Name of the deck
            
        Returns:
            New favorite status
        """
        if name not in self.collection:
            return False
        
        deck = self.collection[name]
        deck.favorite = not deck.favorite
        deck.last_modified = datetime.now().isoformat()
        self._save_deck_to_file(deck)
        
        return deck.favorite
    
    def get_deck_summary(self) -> Dict[str, int]:
        """Get summary statistics of the deck collection."""
        total_decks = len(self.collection)
        favorite_decks = len([d for d in self.collection.values() if d.favorite])
        total_cards = sum(d.total_cards for d in self.collection.values())
        avg_win_rate = sum(d.win_rate for d in self.collection.values()) / max(1, total_decks)
        
        return {
            'total_decks': total_decks,
            'favorite_decks': favorite_decks,
            'total_cards': total_cards,
            'average_win_rate': avg_win_rate
        }
    
    def load_all_decks(self):
        """Load all saved decks from disk."""
        try:
            if not self.decks_dir.exists():
                return
            
            for deck_file in self.decks_dir.glob("*.json"):
                try:
                    with open(deck_file, 'r') as f:
                        deck_data = json.load(f)
                    
                    # Convert card data back to DeckCard objects
                    cards = []
                    for card_data in deck_data['cards']:
                        cards.append(DeckCard(**card_data))
                    
                    deck = SavedDeck(
                        name=deck_data['name'],
                        cards=cards,
                        created_date=deck_data['created_date'],
                        last_modified=deck_data['last_modified'],
                        total_cards=deck_data['total_cards'],
                        win_rate=deck_data.get('win_rate', 0.0),
                        games_played=deck_data.get('games_played', 0),
                        description=deck_data.get('description', ''),
                        favorite=deck_data.get('favorite', False)
                    )
                    
                    self.collection[deck.name] = deck
                    
                except Exception as e:
                    print(f"Failed to load deck from {deck_file}: {e}")
                    
        except Exception as e:
            print(f"Failed to load decks: {e}")
    
    def _save_deck_to_file(self, deck: SavedDeck):
        """Save a single deck to its file."""
        try:
            deck_file = self.decks_dir / f"{deck.name.replace(' ', '_').lower()}.json"
            
            deck_data = {
                'name': deck.name,
                'cards': [asdict(card) for card in deck.cards],
                'created_date': deck.created_date,
                'last_modified': deck.last_modified,
                'total_cards': deck.total_cards,
                'win_rate': deck.win_rate,
                'games_played': deck.games_played,
                'description': deck.description,
                'favorite': deck.favorite
            }
            
            with open(deck_file, 'w') as f:
                json.dump(deck_data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save deck to file: {e}")
    
    def _create_starter_deck(self):
        """Create a default starter deck."""
        starter_cards = [
            DeckCard("EGYPTIAN WARRIOR", 3, 4, 4, "common", "Steadfast defender of the pharaoh"),
            DeckCard("HEALING BLESSING", 2, 0, 0, "common", "Restore 8 health to target"),
            DeckCard("EGYPTIAN WARRIOR", 3, 4, 4, "common", "Steadfast defender of the pharaoh"),
            DeckCard("HEALING BLESSING", 2, 0, 0, "common", "Restore 8 health to target"),
            DeckCard("MUMMY GUARDIAN", 4, 3, 7, "rare", "Returns to hand when destroyed"),
            DeckCard("JUDGMENT SCALE", 4, 3, 6, "rare", "Destroy target creature with cost 4 or less"),
            DeckCard("PYRAMID POWER", 5, 6, 4, "epic", "Gain +2/+2 for each pyramid on field"),
            DeckCard("ISIS - DIVINE MOTHER", 7, 5, 10, "legendary", "Restore 5 health to all friendly creatures"),
        ]
        
        current_time = datetime.now().isoformat()
        starter_deck = SavedDeck(
            name="Starter Deck",
            cards=starter_cards,
            created_date=current_time,
            last_modified=current_time,
            total_cards=len(starter_cards),
            description="A balanced deck for new players featuring Egyptian gods and creatures."
        )
        
        self.collection["Starter Deck"] = starter_deck
        self.current_deck_name = "Starter Deck"
        self._save_deck_to_file(starter_deck)
        print("Created starter deck")

# Global deck collection manager instance
deck_collection_manager = DeckCollectionManager()