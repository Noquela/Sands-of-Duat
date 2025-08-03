"""
Player Collection System

Manages player's owned cards, unlocks, and deck building progression.
Integrates with the save system for persistent card ownership.
"""

import logging
from typing import Dict, Set, List, Optional, Tuple
from collections import defaultdict
from .cards import Card, CardLibrary, CardRarity, CardType


class PlayerCollection:
    """Manages player's card collection and ownership."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Card ownership tracking
        self.owned_cards: Dict[str, int] = defaultdict(int)  # card_id -> count
        self.unlocked_cards: Set[str] = set()  # Available card pool
        self.total_cards_seen: int = 0
        self.card_discovery_order: List[str] = []  # Track discovery order
        
        # Collection statistics
        self.cards_unlocked_today: int = 0
        self.total_cards_unlocked: int = 0
        self.favorite_cards: Set[str] = set()
        
        # Initialize with starter cards
        self._initialize_starter_collection()
    
    def _initialize_starter_collection(self) -> None:
        """Initialize collection with basic starter cards."""
        # Use actual Egyptian card IDs from the card library
        starter_cards = [
            "whisper_of_thoth",
            "anubis_judgment", 
            "isis_protection",
            "desert_meditation",
            "ra_solar_flare",
            "mummification_ritual"
        ]
        
        for card_id in starter_cards:
            self.add_card(card_id, 3)  # 3 copies of each starter
            self.unlock_card(card_id)
        
        self.logger.info(f"Initialized starter collection with {len(starter_cards)} card types")
    
    def add_card(self, card_id: str, count: int = 1) -> bool:
        """Add cards to collection."""
        if count <= 0:
            return False
        
        old_count = self.owned_cards[card_id]
        self.owned_cards[card_id] += count
        
        # Track discovery
        if old_count == 0:
            self.total_cards_seen += 1
            self.card_discovery_order.append(card_id)
            self.cards_unlocked_today += 1
            self.total_cards_unlocked += 1
            self.logger.info(f"Discovered new card: {card_id}")
        
        self.logger.debug(f"Added {count} copies of {card_id} (total: {self.owned_cards[card_id]})")
        return True
    
    def remove_card(self, card_id: str, count: int = 1) -> bool:
        """Remove cards from collection (for crafting, etc.)."""
        if count <= 0:
            return False
        
        current_count = self.owned_cards.get(card_id, 0)
        if current_count < count:
            return False
        
        self.owned_cards[card_id] -= count
        if self.owned_cards[card_id] == 0:
            del self.owned_cards[card_id]
        
        self.logger.debug(f"Removed {count} copies of {card_id}")
        return True
    
    def unlock_card(self, card_id: str) -> None:
        """Unlock a card for potential acquisition."""
        if card_id not in self.unlocked_cards:
            self.unlocked_cards.add(card_id)
            self.logger.debug(f"Unlocked card: {card_id}")
    
    def can_afford_card(self, card_id: str, count: int = 1) -> bool:
        """Check if player can afford to use this many copies."""
        return self.owned_cards.get(card_id, 0) >= count
    
    def get_card_count(self, card_id: str) -> int:
        """Get number of owned copies of a card."""
        return self.owned_cards.get(card_id, 0)
    
    def get_available_cards(self) -> List[Card]:
        """Get all cards available in player's collection."""
        from .cards import card_library
        available_cards = []
        
        for card_id in self.owned_cards:
            card = card_library.get_card_by_id(card_id)
            if card:
                available_cards.append(card)
        
        return available_cards
    
    def get_unlocked_cards(self) -> List[Card]:
        """Get all unlocked cards (owned or not)."""
        from .cards import card_library
        unlocked_cards = []
        
        for card_id in self.unlocked_cards:
            card = card_library.get_card_by_id(card_id)
            if card:
                unlocked_cards.append(card)
        
        return unlocked_cards
    
    def get_collection_stats(self) -> Dict[str, any]:
        """Get collection statistics."""
        card_library = CardLibrary()
        total_possible_cards = len(card_library.get_all_cards())
        
        # Rarity distribution
        rarity_counts = defaultdict(int)
        rarity_owned = defaultdict(int)
        
        for card in card_library.get_all_cards():
            rarity_counts[card.rarity] += 1
            if card.id in self.owned_cards:
                rarity_owned[card.rarity] += 1
        
        # Type distribution
        type_counts = defaultdict(int)
        type_owned = defaultdict(int)
        
        for card in card_library.get_all_cards():
            type_counts[card.type] += 1
            if card.id in self.owned_cards:
                type_owned[card.type] += 1
        
        return {
            "total_unique_owned": len(self.owned_cards),
            "total_possible_cards": total_possible_cards,
            "completion_percentage": (len(self.owned_cards) / total_possible_cards) * 100,
            "total_cards_count": sum(self.owned_cards.values()),
            "unlocked_count": len(self.unlocked_cards),
            "cards_seen": self.total_cards_seen,
            "cards_unlocked_today": self.cards_unlocked_today,
            "rarity_distribution": {
                "owned": dict(rarity_owned),
                "total": dict(rarity_counts)
            },
            "type_distribution": {
                "owned": dict(type_owned),
                "total": dict(type_counts)
            },
            "favorite_cards": len(self.favorite_cards)
        }
    
    def toggle_favorite(self, card_id: str) -> bool:
        """Toggle favorite status of a card."""
        if card_id in self.favorite_cards:
            self.favorite_cards.remove(card_id)
            return False
        else:
            self.favorite_cards.add(card_id)
            return True
    
    def is_favorite(self, card_id: str) -> bool:
        """Check if card is marked as favorite."""
        return card_id in self.favorite_cards
    
    def get_recently_discovered(self, count: int = 5) -> List[str]:
        """Get recently discovered cards."""
        return self.card_discovery_order[-count:] if self.card_discovery_order else []
    
    def filter_cards(self, 
                    rarity: Optional[CardRarity] = None,
                    card_type: Optional[CardType] = None,
                    cost_min: Optional[int] = None,
                    cost_max: Optional[int] = None,
                    owned_only: bool = True,
                    favorites_only: bool = False) -> List[Card]:
        """Filter cards based on criteria."""
        card_library = CardLibrary()
        
        # Start with appropriate pool
        if owned_only:
            card_pool = self.get_available_cards()
        else:
            card_pool = self.get_unlocked_cards()
        
        # Apply filters
        filtered_cards = []
        
        for card in card_pool:
            # Rarity filter
            if rarity and card.rarity != rarity:
                continue
            
            # Type filter
            if card_type and card.type != card_type:
                continue
            
            # Cost filters
            if cost_min is not None and card.sand_cost < cost_min:
                continue
            if cost_max is not None and card.sand_cost > cost_max:
                continue
            
            # Favorites filter
            if favorites_only and not self.is_favorite(card.id):
                continue
            
            filtered_cards.append(card)
        
        return filtered_cards
    
    def to_dict(self) -> Dict[str, any]:
        """Serialize collection to dictionary for saving."""
        return {
            "owned_cards": dict(self.owned_cards),
            "unlocked_cards": list(self.unlocked_cards),
            "total_cards_seen": self.total_cards_seen,
            "card_discovery_order": self.card_discovery_order,
            "cards_unlocked_today": self.cards_unlocked_today,
            "total_cards_unlocked": self.total_cards_unlocked,
            "favorite_cards": list(self.favorite_cards)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'PlayerCollection':
        """Create collection from dictionary (loading from save)."""
        collection = cls()
        
        # Don't initialize starter collection if loading from save
        collection.owned_cards.clear()
        collection.unlocked_cards.clear()
        collection.card_discovery_order.clear()
        
        # Load data
        collection.owned_cards = defaultdict(int, data.get("owned_cards", {}))
        collection.unlocked_cards = set(data.get("unlocked_cards", []))
        collection.total_cards_seen = data.get("total_cards_seen", 0)
        collection.card_discovery_order = data.get("card_discovery_order", [])
        collection.cards_unlocked_today = data.get("cards_unlocked_today", 0)
        collection.total_cards_unlocked = data.get("total_cards_unlocked", 0)
        collection.favorite_cards = set(data.get("favorite_cards", []))
        
        collection.logger.info(f"Loaded collection with {len(collection.owned_cards)} unique cards")
        return collection


class CardRewardSystem:
    """Manages card acquisition and rewards."""
    
    def __init__(self, player_collection: PlayerCollection):
        self.collection = player_collection
        self.logger = logging.getLogger(__name__)
    
    def generate_combat_rewards(self, difficulty: int = 1, count: int = 3) -> List[Card]:
        """Generate random card rewards after combat."""
        card_library = CardLibrary()
        all_cards = card_library.get_all_cards()
        
        # Filter based on rarity weights and difficulty
        available_cards = []
        
        for card in all_cards:
            if card.id in self.collection.unlocked_cards:
                # Weight based on rarity and difficulty
                rarity_weights = {
                    CardRarity.COMMON: 70,
                    CardRarity.UNCOMMON: 25,
                    CardRarity.RARE: 4,
                    CardRarity.LEGENDARY: 1
                }
                
                # Increase rare chances with difficulty
                if difficulty > 3:
                    rarity_weights[CardRarity.RARE] += 3
                    rarity_weights[CardRarity.LEGENDARY] += 1
                
                weight = rarity_weights.get(card.rarity, 10)
                
                # Reduce weight for cards already owned (encourage variety)
                owned_count = self.collection.get_card_count(card.id)
                if owned_count > 0:
                    weight = max(1, weight // (owned_count + 1))
                
                available_cards.extend([card] * weight)
        
        # Select random cards
        import random
        rewards = []
        for _ in range(count):
            if available_cards:
                reward_card = random.choice(available_cards)
                rewards.append(reward_card)
                # Remove selected card to avoid duplicates in this reward
                available_cards = [c for c in available_cards if c.id != reward_card.id]
        
        self.logger.info(f"Generated {len(rewards)} combat rewards")
        return rewards
    
    def award_cards(self, cards: List[Card]) -> None:
        """Award cards to player collection."""
        for card in cards:
            self.collection.add_card(card.id, 1)
            self.logger.info(f"Awarded card: {card.name}")
    
    def unlock_card_pool(self, pool_name: str) -> None:
        """Unlock a pool of cards (e.g., after boss defeat)."""
        # This would load from content files in a full implementation
        card_library = CardLibrary()
        
        # For now, unlock a few cards based on pool name
        unlock_pools = {
            "desert_pool": ["anubis_judgment", "desert_mirage", "sand_storm"],
            "temple_pool": ["sacred_scarab", "pharaoh_blessing", "mummy_wrap"],
            "endgame_pool": ["ra_fury", "osiris_resurrection", "isis_protection"]
        }
        
        cards_to_unlock = unlock_pools.get(pool_name, [])
        for card_id in cards_to_unlock:
            self.collection.unlock_card(card_id)
        
        self.logger.info(f"Unlocked {len(cards_to_unlock)} cards from {pool_name}")