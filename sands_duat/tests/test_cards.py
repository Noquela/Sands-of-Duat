"""
Card System Tests

Tests for card definitions, effects, deck management,
and card library functionality.
"""

import unittest
from unittest.mock import Mock

from core.cards import (
    Card, CardEffect, Deck, CardLibrary, 
    CardType, CardRarity, EffectType, TargetType,
    card_library
)


class CardEffectTestCase(unittest.TestCase):
    """Test cases for card effects."""
    
    def test_effect_creation(self):
        """Test creating card effects."""
        effect = CardEffect(
            effect_type=EffectType.DAMAGE,
            value=10,
            target=TargetType.ENEMY
        )
        
        self.assertEqual(effect.effect_type, EffectType.DAMAGE)
        self.assertEqual(effect.value, 10)
        self.assertEqual(effect.target, TargetType.ENEMY)
        self.assertIsNone(effect.condition)
    
    def test_effect_with_metadata(self):
        """Test effects with metadata."""
        metadata = {"duration": 3, "buff_type": "strength"}
        effect = CardEffect(
            effect_type=EffectType.BUFF,
            value=2,
            target=TargetType.SELF,
            metadata=metadata
        )
        
        self.assertEqual(effect.metadata, metadata)
    
    def test_effect_string_representation(self):
        """Test effect string representation."""
        effect = CardEffect(
            effect_type=EffectType.DAMAGE,
            value=5,
            target=TargetType.ENEMY
        )
        
        expected = "damage(5) -> enemy"
        self.assertEqual(str(effect), expected)


class CardTestCase(unittest.TestCase):
    """Test cases for card functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.basic_card = Card(
            name="Test Card",
            description="A test card for unit testing.",
            sand_cost=2,
            card_type=CardType.ATTACK,
            rarity=CardRarity.COMMON
        )
    
    def test_card_creation(self):
        """Test creating cards."""
        self.assertEqual(self.basic_card.name, "Test Card")
        self.assertEqual(self.basic_card.sand_cost, 2)
        self.assertEqual(self.basic_card.card_type, CardType.ATTACK)
        self.assertEqual(self.basic_card.rarity, CardRarity.COMMON)
        self.assertFalse(self.basic_card.upgraded)
        self.assertTrue(self.basic_card.upgradeable)
    
    def test_sand_cost_validation(self):
        """Test sand cost validation."""
        # Valid sand costs
        for cost in range(7):  # 0-6
            card = Card(
                name="Test",
                description="Test",
                sand_cost=cost,
                card_type=CardType.SKILL
            )
            self.assertEqual(card.sand_cost, cost)
        
        # Invalid sand costs should raise ValueError
        with self.assertRaises(ValueError):
            Card(
                name="Invalid",
                description="Invalid cost",
                sand_cost=-1,
                card_type=CardType.SKILL
            )
        
        with self.assertRaises(ValueError):
            Card(
                name="Invalid",
                description="Invalid cost",
                sand_cost=7,
                card_type=CardType.SKILL
            )
    
    def test_effective_cost_calculation(self):
        """Test effective cost with modifiers."""
        card = Card(
            name="Test",
            description="Test",
            sand_cost=3,
            card_type=CardType.ATTACK
        )
        
        # No modifiers
        self.assertEqual(card.get_effective_cost(), 3)
        
        # Cost increase
        modifiers = {"cost_increase": 2}
        self.assertEqual(card.get_effective_cost(modifiers), 5)
        
        # Cost reduction
        modifiers = {"cost_reduction": 1}
        self.assertEqual(card.get_effective_cost(modifiers), 2)
        
        # Set cost
        modifiers = {"set_cost": 0}
        self.assertEqual(card.get_effective_cost(modifiers), 0)
        
        # Cost clamping (below 0)
        modifiers = {"cost_reduction": 5}
        self.assertEqual(card.get_effective_cost(modifiers), 0)
        
        # Cost clamping (above 6)
        modifiers = {"cost_increase": 5}
        self.assertEqual(card.get_effective_cost(modifiers), 6)
    
    def test_keyword_management(self):
        """Test keyword functionality."""
        card = Card(
            name="Keyword Test",
            description="Test keywords",
            sand_cost=1,
            card_type=CardType.SKILL
        )
        
        # Add keywords
        card.add_keyword("defense")
        card.add_keyword("cantrip")
        
        self.assertTrue(card.has_keyword("defense"))
        self.assertTrue(card.has_keyword("cantrip"))
        self.assertFalse(card.has_keyword("attack"))
        
        # Case insensitive
        self.assertTrue(card.has_keyword("DEFENSE"))
        
        # Remove keyword
        card.remove_keyword("defense")
        self.assertFalse(card.has_keyword("defense"))
    
    def test_damage_calculations(self):
        """Test damage effect calculations."""
        damage_effect1 = CardEffect(EffectType.DAMAGE, 5, TargetType.ENEMY)
        damage_effect2 = CardEffect(EffectType.DAMAGE, 3, TargetType.ENEMY)
        heal_effect = CardEffect(EffectType.HEAL, 2, TargetType.SELF)
        
        card = Card(
            name="Multi-Effect",
            description="Multiple effects",
            sand_cost=2,
            card_type=CardType.ATTACK,
            effects=[damage_effect1, damage_effect2, heal_effect]
        )
        
        damage_effects = card.get_damage_effects()
        self.assertEqual(len(damage_effects), 2)
        
        total_damage = card.get_total_damage()
        self.assertEqual(total_damage, 8)  # 5 + 3
    
    def test_target_checking(self):
        """Test target type checking."""
        enemy_effect = CardEffect(EffectType.DAMAGE, 5, TargetType.ENEMY)
        self_effect = CardEffect(EffectType.HEAL, 3, TargetType.SELF)
        
        card = Card(
            name="Target Test",
            description="Test targeting",
            sand_cost=2,
            card_type=CardType.ATTACK,
            effects=[enemy_effect, self_effect]
        )
        
        self.assertTrue(card.can_target(TargetType.ENEMY))
        self.assertTrue(card.can_target(TargetType.SELF))
        self.assertFalse(card.can_target(TargetType.ALL_ENEMIES))
    
    def test_card_upgrade(self):
        """Test card upgrading."""
        original_card = Card(
            name="Fireball",
            description="Deal damage",
            sand_cost=2,
            card_type=CardType.ATTACK,
            effects=[CardEffect(EffectType.DAMAGE, 8, TargetType.ENEMY)]
        )
        
        upgraded = original_card.upgrade()
        
        # Check upgrade properties
        self.assertTrue(upgraded.upgraded)
        self.assertEqual(upgraded.name, "Fireball+")
        
        # Check effect was upgraded
        damage_effects = upgraded.get_damage_effects()
        self.assertEqual(len(damage_effects), 1)
        self.assertEqual(damage_effects[0].value, 11)  # 8 + 3
        
        # Original should be unchanged
        self.assertFalse(original_card.upgraded)
        self.assertEqual(original_card.get_total_damage(), 8)
    
    def test_upgrade_non_upgradeable(self):
        """Test upgrading non-upgradeable cards."""
        card = Card(
            name="Curse",
            description="Cannot be upgraded",
            sand_cost=0,
            card_type=CardType.CURSE,
            upgradeable=False
        )
        
        upgraded = card.upgrade()
        self.assertEqual(card, upgraded)  # Should return same instance
        self.assertFalse(upgraded.upgraded)
    
    def test_upgrade_already_upgraded(self):
        """Test upgrading already upgraded cards."""
        card = Card(
            name="Test",
            description="Test",
            sand_cost=1,
            card_type=CardType.SKILL,
            upgraded=True
        )
        
        upgraded = card.upgrade()
        self.assertEqual(card, upgraded)


class DeckTestCase(unittest.TestCase):
    """Test cases for deck management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.deck = Deck(name="Test Deck")
        self.sample_cards = [
            Card("Card 1", "First card", 1, CardType.ATTACK),
            Card("Card 2", "Second card", 2, CardType.SKILL),
            Card("Card 3", "Third card", 3, CardType.POWER)
        ]
    
    def test_deck_creation(self):
        """Test creating decks."""
        self.assertEqual(self.deck.name, "Test Deck")
        self.assertEqual(len(self.deck), 0)
        self.assertTrue(self.deck.is_empty())
    
    def test_add_cards(self):
        """Test adding cards to deck."""
        card = self.sample_cards[0]
        result = self.deck.add_card(card)
        
        self.assertTrue(result)
        self.assertEqual(len(self.deck), 1)
        self.assertFalse(self.deck.is_empty())
        self.assertIn(card, self.deck.cards)
    
    def test_deck_size_limits(self):
        """Test deck size limitations."""
        limited_deck = Deck(name="Limited", max_size=2)
        
        # Add cards up to limit
        for card in self.sample_cards[:2]:
            result = limited_deck.add_card(card)
            self.assertTrue(result)
        
        # Should fail to add beyond limit
        result = limited_deck.add_card(self.sample_cards[2])
        self.assertFalse(result)
        self.assertEqual(len(limited_deck), 2)
    
    def test_remove_cards(self):
        """Test removing cards from deck."""
        # Add cards
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        # Remove by ID
        removed = self.deck.remove_card(self.sample_cards[1].id)
        self.assertEqual(removed, self.sample_cards[1])
        self.assertEqual(len(self.deck), 2)
        
        # Remove by name
        removed = self.deck.remove_card_by_name("Card 1")
        self.assertEqual(removed.name, "Card 1")
        self.assertEqual(len(self.deck), 1)
        
        # Try to remove non-existent card
        removed = self.deck.remove_card("nonexistent")
        self.assertIsNone(removed)
    
    def test_deck_shuffle(self):
        """Test deck shuffling."""
        # Add cards in order
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        original_order = [card.id for card in self.deck.cards]
        
        # Shuffle with fixed seed
        self.deck.shuffle(seed=42)
        shuffled_order = [card.id for card in self.deck.cards]
        
        # Should have same cards but potentially different order
        self.assertEqual(set(original_order), set(shuffled_order))
        
        # With the same seed, should get same result
        self.deck.shuffle(seed=42)
        second_shuffle = [card.id for card in self.deck.cards]
        self.assertEqual(shuffled_order, second_shuffle)
    
    def test_draw_cards(self):
        """Test drawing cards from deck."""
        # Add cards
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        # Draw one card
        drawn = self.deck.draw(1)
        self.assertEqual(len(drawn), 1)
        self.assertEqual(len(self.deck), 2)
        
        # Draw multiple cards
        drawn = self.deck.draw(2)
        self.assertEqual(len(drawn), 2)
        self.assertEqual(len(self.deck), 0)
        
        # Try to draw from empty deck
        drawn = self.deck.draw(1)
        self.assertEqual(len(drawn), 0)
    
    def test_peek_cards(self):
        """Test peeking at top cards."""
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        # Peek at top card
        peeked = self.deck.peek(1)
        self.assertEqual(len(peeked), 1)
        self.assertEqual(len(self.deck), 3)  # Deck unchanged
        
        # Peek at multiple cards
        peeked = self.deck.peek(2)
        self.assertEqual(len(peeked), 2)
        self.assertEqual(len(self.deck), 3)  # Deck unchanged
    
    def test_deck_statistics(self):
        """Test deck statistics calculations."""
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        # Average cost: (1 + 2 + 3) / 3 = 2.0
        avg_cost = self.deck.get_average_cost()
        self.assertEqual(avg_cost, 2.0)
        
        # Card counts
        counts = self.deck.get_card_counts()
        expected = {"Card 1": 1, "Card 2": 1, "Card 3": 1}
        self.assertEqual(counts, expected)
        
        # Cards by cost
        cost_2_cards = self.deck.get_cards_by_cost(2)
        self.assertEqual(len(cost_2_cards), 1)
        self.assertEqual(cost_2_cards[0].name, "Card 2")
        
        # Cards by type
        attack_cards = self.deck.get_cards_by_type(CardType.ATTACK)
        self.assertEqual(len(attack_cards), 1)
        self.assertEqual(attack_cards[0].name, "Card 1")
    
    def test_deck_copy(self):
        """Test deck copying."""
        for card in self.sample_cards:
            self.deck.add_card(card)
        
        copy = self.deck.copy()
        
        # Should have same content but be independent
        self.assertEqual(len(copy), len(self.deck))
        self.assertEqual(copy.name, "Test Deck (Copy)")
        
        # Modifying copy shouldn't affect original
        copy.add_card(Card("New Card", "New", 0, CardType.SKILL))
        self.assertNotEqual(len(copy), len(self.deck))


class CardLibraryTestCase(unittest.TestCase):
    """Test cases for card library management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.library = CardLibrary()
        self.sample_cards = [
            Card("Fireball", "Deal damage", 3, CardType.ATTACK, CardRarity.COMMON),
            Card("Heal", "Restore health", 2, CardType.SKILL, CardRarity.COMMON),
            Card("Lightning", "Quick damage", 1, CardType.ATTACK, CardRarity.UNCOMMON)
        ]
    
    def test_library_registration(self):
        """Test registering cards in library."""
        card = self.sample_cards[0]
        self.library.register_card(card)
        
        # Should be able to retrieve by ID and name
        retrieved_by_id = self.library.get_card_by_id(card.id)
        retrieved_by_name = self.library.get_card_by_name(card.name)
        
        self.assertEqual(retrieved_by_id, card)
        self.assertEqual(retrieved_by_name, card)
    
    def test_card_creation(self):
        """Test creating new instances from library."""
        card = self.sample_cards[0]
        self.library.register_card(card)
        
        # Create new instance
        new_instance = self.library.create_card(card.id)
        self.assertIsNotNone(new_instance)
        self.assertEqual(new_instance.name, card.name)
        self.assertNotEqual(new_instance.id, card.id)  # Should have new ID
        
        # Create by name
        new_by_name = self.library.create_card_by_name(card.name)
        self.assertIsNotNone(new_by_name)
        self.assertEqual(new_by_name.name, card.name)
    
    def test_library_filtering(self):
        """Test filtering cards in library."""
        for card in self.sample_cards:
            self.library.register_card(card)
        
        # Filter by cost
        cost_2_cards = self.library.get_cards_by_cost(2)
        self.assertEqual(len(cost_2_cards), 1)
        self.assertEqual(cost_2_cards[0].name, "Heal")
        
        # Filter by type
        attack_cards = self.library.get_cards_by_type(CardType.ATTACK)
        self.assertEqual(len(attack_cards), 2)
        
        # Filter by rarity
        uncommon_cards = self.library.get_cards_by_rarity(CardRarity.UNCOMMON)
        self.assertEqual(len(uncommon_cards), 1)
        self.assertEqual(uncommon_cards[0].name, "Lightning")
    
    def test_keyword_filtering(self):
        """Test filtering by keywords."""
        card_with_keyword = Card(
            "Block", "Gain defense", 1, CardType.SKILL,
            keywords={"defense", "basic"}
        )
        
        self.library.register_card(card_with_keyword)
        
        defense_cards = self.library.get_cards_with_keyword("defense")
        self.assertEqual(len(defense_cards), 1)
        self.assertEqual(defense_cards[0].name, "Block")
        
        # Case insensitive
        defense_cards = self.library.get_cards_with_keyword("DEFENSE")
        self.assertEqual(len(defense_cards), 1)
    
    def test_library_management(self):
        """Test library management operations."""
        for card in self.sample_cards:
            self.library.register_card(card)
        
        # Check size
        self.assertEqual(self.library.size(), 3)
        
        # Get all cards
        all_cards = self.library.get_all_cards()
        self.assertEqual(len(all_cards), 3)
        
        # Clear library
        self.library.clear()
        self.assertEqual(self.library.size(), 0)


if __name__ == '__main__':
    unittest.main()