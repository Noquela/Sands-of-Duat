"""
Integration Tests

Tests for interactions between different game systems,
ensuring they work together correctly.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch

from core.engine import GameEngine, GameState, GamePhase
from core.hourglass import HourGlass
from core.combat import CombatEngine, CombatAction, ActionType
from core.cards import Card, CardType, CardEffect, EffectType, TargetType, Deck


class HourGlassCombatIntegrationTestCase(unittest.TestCase):
    """Test integration between Hour-Glass and combat systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hourglass = HourGlass()
        self.combat_engine = CombatEngine()
        
    def test_sand_cost_validation_in_combat(self):
        """Test that combat validates sand costs against hourglass."""
        # Set up combat
        self.combat_engine.start_combat(["player", "enemy"])
        
        # Set player sand
        self.hourglass.set_sand(2)
        
        # Create actions with different costs
        affordable_action = CombatAction(
            ActionType.PLAY_CARD,
            "player",
            sand_cost=2
        )
        
        expensive_action = CombatAction(
            ActionType.PLAY_CARD,
            "player", 
            sand_cost=3
        )
        
        # Should be able to queue affordable action
        self.assertTrue(self.combat_engine.queue_action(affordable_action))
        
        # Should be able to queue expensive action (validation happens during resolution)
        self.assertTrue(self.combat_engine.queue_action(expensive_action))
    
    def test_sand_spending_during_combat(self):
        """Test sand spending during combat action resolution."""
        # Start with some sand
        self.hourglass.set_sand(4)
        
        # Create a card that costs 2 sand
        card = Card(
            name="Lightning Bolt",
            description="Quick attack",
            sand_cost=2,
            card_type=CardType.ATTACK,
            effects=[CardEffect(EffectType.DAMAGE, 6, TargetType.ENEMY)]
        )
        
        # Simulate playing the card
        initial_sand = self.hourglass.current_sand
        success = self.hourglass.spend_sand(card.sand_cost)
        
        self.assertTrue(success)
        self.assertEqual(self.hourglass.current_sand, initial_sand - card.sand_cost)
    
    @patch('time.time')
    def test_sand_regeneration_during_combat(self, mock_time):
        """Test that sand regenerates during combat."""
        mock_time.side_effect = [0.0, 1.0, 2.0, 3.0]
        
        # Start with empty hourglass
        self.hourglass.current_sand = 0
        self.hourglass.timer.last_update = 0.0
        
        # Simulate time passing during combat
        mock_time.return_value = 2.0
        self.hourglass.update_sand()
        
        # Should have regenerated 2 sand
        self.assertEqual(self.hourglass.current_sand, 2)


class CardCombatIntegrationTestCase(unittest.TestCase):
    """Test integration between card and combat systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.combat_engine = CombatEngine()
        self.deck = Deck(name="Test Deck")
        
        # Create test cards
        self.attack_card = Card(
            name="Sword Strike",
            description="Deal 8 damage",
            sand_cost=2,
            card_type=CardType.ATTACK,
            effects=[CardEffect(EffectType.DAMAGE, 8, TargetType.ENEMY)]
        )
        
        self.skill_card = Card(
            name="Shield Block",
            description="Gain 6 block",
            sand_cost=1,
            card_type=CardType.SKILL,
            effects=[CardEffect(EffectType.BLOCK, 6, TargetType.SELF)]
        )
        
        self.deck.add_card(self.attack_card)
        self.deck.add_card(self.skill_card)
    
    def test_card_to_combat_action_conversion(self):
        """Test converting card plays to combat actions."""
        # Draw a card
        drawn_cards = self.deck.draw(1)
        card = drawn_cards[0]
        
        # Create combat action for playing the card
        action = CombatAction(
            action_type=ActionType.PLAY_CARD,
            actor_id="player",
            target_id="enemy",
            card_id=card.id,
            sand_cost=card.sand_cost
        )
        
        self.assertEqual(action.card_id, card.id)
        self.assertEqual(action.sand_cost, card.sand_cost)
        self.assertEqual(action.action_type, ActionType.PLAY_CARD)
    
    def test_card_effects_in_combat(self):
        """Test that card effects are properly represented."""
        # Test damage card
        damage_effects = self.attack_card.get_damage_effects()
        self.assertEqual(len(damage_effects), 1)
        self.assertEqual(damage_effects[0].value, 8)
        self.assertEqual(damage_effects[0].target, TargetType.ENEMY)
        
        # Test block card
        block_effects = [e for e in self.skill_card.effects if e.effect_type == EffectType.BLOCK]
        self.assertEqual(len(block_effects), 1)
        self.assertEqual(block_effects[0].value, 6)
        self.assertEqual(block_effects[0].target, TargetType.SELF)
    
    def test_deck_draw_in_combat_context(self):
        """Test deck operations in combat context."""
        # Simulate drawing starting hand
        hand = self.deck.draw(5)  # Standard starting hand size
        
        # Should be able to draw cards
        self.assertGreater(len(hand), 0)
        self.assertLessEqual(len(hand), 5)  # Can't draw more than available
        
        # Remaining deck should be smaller
        self.assertEqual(len(self.deck), 2 - len(hand))


class GameEngineIntegrationTestCase(unittest.TestCase):
    """Test integration of all systems through the game engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.engine.initialize()
    
    def tearDown(self):
        """Clean up after tests."""
        self.engine.shutdown()
    
    def test_engine_initialization(self):
        """Test that engine initializes all systems."""
        self.assertIsNotNone(self.engine.world)
        self.assertIsNotNone(self.engine.state)
        self.assertIsNotNone(self.engine.combat_engine)
        self.assertIsNotNone(self.engine.hourglass)
    
    def test_game_state_transitions(self):
        """Test game state transitions through the engine."""
        initial_phase = self.engine.state.phase
        
        # Transition to combat
        success = self.engine.state_manager.transition_state(
            self.engine.state, 
            GamePhase.COMBAT
        )
        
        self.assertTrue(success)
        self.assertEqual(self.engine.state.phase, GamePhase.COMBAT)
        self.assertNotEqual(self.engine.state.phase, initial_phase)
    
    def test_event_system_integration(self):
        """Test that events flow through the system."""
        events_received = []
        
        def test_handler(event_data):
            events_received.append(event_data)
        
        # Register event handler
        self.engine.register_event_handler("test_event", test_handler)
        
        # Emit event
        test_data = {"test": "data"}
        self.engine.emit_event("test_event", test_data)
        
        # Should have received the event
        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0], test_data)
    
    def test_combat_initialization_through_engine(self):
        """Test combat initialization via game engine."""
        # Transition to combat phase
        self.engine.state_manager.transition_state(
            self.engine.state,
            GamePhase.COMBAT
        )
        
        # Engine should set up hour-glass for combat
        self.assertIsNotNone(self.engine.hourglass)
        self.assertGreaterEqual(self.engine.hourglass.current_sand, 0)
    
    async def test_main_loop_integration(self):
        """Test that main loop updates all systems."""
        # Mock the systems to track update calls
        world_update_called = False
        hourglass_update_called = False
        
        original_world_update = self.engine.world.update
        original_hourglass_update = self.engine.hourglass.update_sand
        
        def mock_world_update(delta_time):
            nonlocal world_update_called
            world_update_called = True
            return original_world_update(delta_time)
        
        def mock_hourglass_update():
            nonlocal hourglass_update_called
            hourglass_update_called = True
            return original_hourglass_update()
        
        self.engine.world.update = mock_world_update
        self.engine.hourglass.update_sand = mock_hourglass_update
        
        # Transition to combat to enable hourglass updates
        self.engine.state_manager.transition_state(
            self.engine.state,
            GamePhase.COMBAT
        )
        
        # Run one update cycle
        await self.engine._update(0.016)  # 16ms frame time
        
        # Both systems should have been updated
        self.assertTrue(world_update_called)
        self.assertTrue(hourglass_update_called)


class ContentIntegrationTestCase(unittest.TestCase):
    """Test integration between content system and game systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.engine.initialize()
    
    def tearDown(self):
        """Clean up after tests."""
        self.engine.shutdown()
    
    def test_card_library_integration(self):
        """Test that card library integrates with game systems."""
        from core.cards import card_library
        
        # Create a test card
        test_card = Card(
            name="Test Integration Card",
            description="For testing integration",
            sand_cost=1,
            card_type=CardType.SKILL
        )
        
        # Register in library
        card_library.register_card(test_card)
        
        # Should be able to create instances
        new_instance = card_library.create_card(test_card.id)
        self.assertIsNotNone(new_instance)
        self.assertEqual(new_instance.name, test_card.name)
        
        # Should be able to use in deck
        deck = Deck(name="Integration Test Deck")
        success = deck.add_card(new_instance)
        self.assertTrue(success)
    
    def test_hourglass_card_cost_integration(self):
        """Test integration between hourglass and card costs."""
        # Set up hourglass with some sand
        self.engine.hourglass.set_sand(3)
        
        # Create cards with different costs
        cheap_card = Card("Cheap", "Low cost", 1, CardType.SKILL)
        expensive_card = Card("Expensive", "High cost", 4, CardType.SKILL)
        
        # Should be able to afford cheap card
        self.assertTrue(self.engine.hourglass.can_afford(cheap_card.sand_cost))
        
        # Should not be able to afford expensive card
        self.assertFalse(self.engine.hourglass.can_afford(expensive_card.sand_cost))
    
    def test_combat_card_interaction(self):
        """Test interaction between combat and card systems."""
        # Start combat
        self.engine.combat_engine.start_combat(["player", "enemy"])
        
        # Create a card action
        test_card = Card("Test", "Test card", 2, CardType.ATTACK)
        action = CombatAction(
            ActionType.PLAY_CARD,
            "player",
            card_id=test_card.id,
            sand_cost=test_card.sand_cost
        )
        
        # Should be able to queue the action
        success = self.engine.combat_engine.queue_action(action)
        self.assertTrue(success)
        
        # Action should be in queue
        self.assertTrue(self.engine.combat_engine.action_queue.has_actions())


class PerformanceIntegrationTestCase(unittest.TestCase):
    """Test performance aspects of system integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.engine.initialize()
    
    def tearDown(self):
        """Clean up after tests."""
        self.engine.shutdown()
    
    @patch('time.time')
    def test_timing_precision_integration(self, mock_time):
        """Test that timing precision is maintained across systems."""
        # Mock precise time progression
        mock_time.side_effect = [0.0, 0.5, 1.0, 1.5, 2.0]
        
        # Start with empty hourglass
        self.engine.hourglass.current_sand = 0
        self.engine.hourglass.timer.last_update = 0.0
        
        # Simulate precise timing updates
        mock_time.return_value = 1.0
        self.engine.hourglass.update_sand()
        
        # Should have exactly 1 sand after 1 second
        self.assertEqual(self.engine.hourglass.current_sand, 1)
        
        # Test fractional regeneration doesn't round up
        mock_time.return_value = 1.5
        self.engine.hourglass.update_sand()
        
        # Should still have 1 sand (1.5 seconds total)
        self.assertEqual(self.engine.hourglass.current_sand, 1)
    
    def test_large_deck_performance(self):
        """Test performance with large deck operations."""
        # Create a large deck
        large_deck = Deck(name="Large Deck")
        
        # Add many cards
        for i in range(100):
            card = Card(f"Card {i}", f"Card number {i}", i % 7, CardType.SKILL)
            large_deck.add_card(card)
        
        # Operations should still be fast
        import time
        
        start_time = time.time()
        large_deck.shuffle()
        shuffle_time = time.time() - start_time
        
        start_time = time.time()
        drawn = large_deck.draw(10)
        draw_time = time.time() - start_time
        
        # Operations should complete quickly (under 10ms)
        self.assertLess(shuffle_time, 0.01)
        self.assertLess(draw_time, 0.01)
        self.assertEqual(len(drawn), 10)


if __name__ == '__main__':
    unittest.main()