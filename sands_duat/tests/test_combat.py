"""
Combat Engine Tests

Tests for the combat system, action queue, and battle mechanics
with Hour-Glass Initiative integration.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from core.combat import CombatEngine, ActionQueue, CombatAction, CombatState, ActionType, CombatPhase


class CombatActionTestCase(unittest.TestCase):
    """Test cases for combat actions."""
    
    def test_action_creation(self):
        """Test creating combat actions."""
        action = CombatAction(
            action_type=ActionType.PLAY_CARD,
            actor_id="player",
            target_id="enemy1",
            card_id="fireball",
            sand_cost=3
        )
        
        self.assertEqual(action.action_type, ActionType.PLAY_CARD)
        self.assertEqual(action.actor_id, "player")
        self.assertEqual(action.target_id, "enemy1")
        self.assertEqual(action.card_id, "fireball")
        self.assertEqual(action.sand_cost, 3)
        self.assertGreater(action.timestamp, 0)
    
    def test_action_with_data(self):
        """Test actions with additional data."""
        data = {"damage": 10, "effect": "burn"}
        action = CombatAction(
            action_type=ActionType.ABILITY,
            actor_id="enemy1",
            data=data
        )
        
        self.assertEqual(action.data, data)


class ActionQueueTestCase(unittest.TestCase):
    """Test cases for action queue management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.queue = ActionQueue()
    
    def test_initial_state(self):
        """Test initial queue state."""
        self.assertFalse(self.queue.has_actions())
        self.assertFalse(self.queue.processing)
        self.assertIsNone(self.queue.get_next_action())
    
    def test_add_actions(self):
        """Test adding actions to queue."""
        action1 = CombatAction(ActionType.PLAY_CARD, "player")
        action2 = CombatAction(ActionType.ABILITY, "enemy1")
        
        self.queue.add_action(action1)
        self.queue.add_action(action2)
        
        self.assertTrue(self.queue.has_actions())
        self.assertEqual(len(self.queue.actions), 2)
    
    def test_fifo_order(self):
        """Test that actions are processed in FIFO order."""
        action1 = CombatAction(ActionType.PLAY_CARD, "player", card_id="card1")
        action2 = CombatAction(ActionType.PLAY_CARD, "player", card_id="card2")
        action3 = CombatAction(ActionType.ABILITY, "enemy1")
        
        self.queue.add_action(action1)
        self.queue.add_action(action2)
        self.queue.add_action(action3)
        
        # Should get actions in order added
        first = self.queue.get_next_action()
        second = self.queue.get_next_action()
        third = self.queue.get_next_action()
        
        self.assertEqual(first.card_id, "card1")
        self.assertEqual(second.card_id, "card2")
        self.assertEqual(third.action_type, ActionType.ABILITY)
        self.assertIsNone(self.queue.get_next_action())
    
    def test_filter_by_actor(self):
        """Test filtering actions by actor."""
        player_action = CombatAction(ActionType.PLAY_CARD, "player")
        enemy_action = CombatAction(ActionType.ABILITY, "enemy1")
        
        self.queue.add_action(player_action)
        self.queue.add_action(enemy_action)
        
        player_actions = self.queue.get_actions_by_actor("player")
        self.assertEqual(len(player_actions), 1)
        self.assertEqual(player_actions[0].actor_id, "player")
        
        enemy_actions = self.queue.get_actions_by_actor("enemy1")
        self.assertEqual(len(enemy_actions), 1)
        self.assertEqual(enemy_actions[0].actor_id, "enemy1")
    
    def test_clear_queue(self):
        """Test clearing the action queue."""
        action = CombatAction(ActionType.PLAY_CARD, "player")
        self.queue.add_action(action)
        
        self.assertTrue(self.queue.has_actions())
        self.queue.clear()
        self.assertFalse(self.queue.has_actions())


class CombatStateTestCase(unittest.TestCase):
    """Test cases for combat state management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.state = CombatState()
    
    def test_initial_state(self):
        """Test initial combat state."""
        self.assertEqual(self.state.phase, CombatPhase.SETUP)
        self.assertEqual(len(self.state.participants), 0)
        self.assertIsNone(self.state.current_actor)
        self.assertEqual(self.state.turn_count, 0)
    
    def test_add_participants(self):
        """Test adding combat participants."""
        self.state.add_participant("player")
        self.state.add_participant("enemy1")
        
        self.assertIn("player", self.state.participants)
        self.assertIn("enemy1", self.state.participants)
        self.assertEqual(len(self.state.participants), 2)
        
        # Test duplicate prevention
        self.state.add_participant("player")
        self.assertEqual(len(self.state.participants), 2)
    
    def test_remove_participants(self):
        """Test removing combat participants."""
        self.state.add_participant("player")
        self.state.add_participant("enemy1")
        
        self.state.remove_participant("enemy1")
        self.assertNotIn("enemy1", self.state.participants)
        self.assertIn("player", self.state.participants)
    
    def test_combat_duration(self):
        """Test combat duration calculation."""
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0.0, 5.0]
            
            state = CombatState()  # Created at time 0
            mock_time.return_value = 5.0
            
            duration = state.get_combat_duration()
            self.assertEqual(duration, 5.0)
    
    def test_is_active(self):
        """Test combat active state checking."""
        self.assertFalse(self.state.is_active())  # SETUP phase
        
        self.state.phase = CombatPhase.ACTIVE
        self.assertTrue(self.state.is_active())
        
        self.state.phase = CombatPhase.ENDED
        self.assertFalse(self.state.is_active())


class CombatEngineTestCase(unittest.TestCase):
    """Test cases for the main combat engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = CombatEngine()
        self.event_calls = []
        
        def test_event_handler(event_type, event_data):
            self.event_calls.append((event_type, event_data))
        
        self.engine.on_combat_event = test_event_handler
    
    def test_initial_state(self):
        """Test initial engine state."""
        self.assertEqual(self.engine.state.phase, CombatPhase.SETUP)
        self.assertFalse(self.engine.action_queue.has_actions())
    
    def test_start_combat(self):
        """Test starting a combat encounter."""
        participants = ["player", "enemy1", "enemy2"]
        self.engine.start_combat(participants, "test_combat")
        
        self.assertEqual(self.engine.state.phase, CombatPhase.ACTIVE)
        self.assertEqual(self.engine.state.participants, participants)
        self.assertEqual(self.engine.state.combat_id, "test_combat")
        
        # Check event was triggered
        self.assertEqual(len(self.event_calls), 1)
        event_type, event_data = self.event_calls[0]
        self.assertEqual(event_type, "combat_started")
        self.assertEqual(event_data["participants"], participants)
    
    def test_end_combat(self):
        """Test ending a combat encounter."""
        self.engine.start_combat(["player", "enemy1"])
        self.event_calls.clear()  # Clear start event
        
        self.engine.end_combat("player")
        
        self.assertEqual(self.engine.state.phase, CombatPhase.ENDED)
        self.assertFalse(self.engine.action_queue.has_actions())
        
        # Check event was triggered
        self.assertEqual(len(self.event_calls), 1)
        event_type, event_data = self.event_calls[0]
        self.assertEqual(event_type, "combat_ended")
        self.assertEqual(event_data["winner"], "player")
    
    def test_queue_action_validation(self):
        """Test action queuing validation."""
        # Should fail when combat is not active
        action = CombatAction(ActionType.PLAY_CARD, "player")
        result = self.engine.queue_action(action)
        self.assertFalse(result)
        
        # Start combat and try again
        self.engine.start_combat(["player", "enemy1"])
        result = self.engine.queue_action(action)
        self.assertTrue(result)
        
        # Should fail for non-participant
        invalid_action = CombatAction(ActionType.PLAY_CARD, "unknown_actor")
        result = self.engine.queue_action(invalid_action)
        self.assertFalse(result)
    
    def test_valid_actions(self):
        """Test getting valid actions for actors."""
        # No valid actions when combat is not active
        actions = self.engine.get_valid_actions("player")
        self.assertEqual(len(actions), 0)
        
        # Start combat
        self.engine.start_combat(["player", "enemy1"])
        
        # Should have basic actions available
        actions = self.engine.get_valid_actions("player")
        self.assertIn(ActionType.END_TURN, actions)
        self.assertIn(ActionType.FLEE, actions)
        self.assertIn(ActionType.PLAY_CARD, actions)
        
        # Invalid actor should get no actions
        actions = self.engine.get_valid_actions("unknown")
        self.assertEqual(len(actions), 0)


class CombatIntegrationTestCase(unittest.TestCase):
    """Integration tests for combat system components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = CombatEngine()
        self.events = []
        
        def event_handler(event_type, event_data):
            self.events.append((event_type, event_data))
        
        self.engine.on_combat_event = event_handler
    
    def test_complete_combat_flow(self):
        """Test a complete combat encounter flow."""
        # Start combat
        participants = ["player", "enemy1"]
        self.engine.start_combat(participants, "integration_test")
        
        # Queue some actions
        player_action = CombatAction(
            ActionType.PLAY_CARD,
            "player",
            target_id="enemy1",
            card_id="attack",
            sand_cost=2
        )
        
        enemy_action = CombatAction(
            ActionType.ABILITY,
            "enemy1",
            target_id="player",
            sand_cost=1
        )
        
        self.assertTrue(self.engine.queue_action(player_action))
        self.assertTrue(self.engine.queue_action(enemy_action))
        
        # Verify actions are queued
        self.assertTrue(self.engine.action_queue.has_actions())
        
        # End combat
        self.engine.end_combat("player")
        
        # Verify final state
        self.assertEqual(self.engine.state.phase, CombatPhase.ENDED)
        self.assertFalse(self.engine.action_queue.has_actions())
        
        # Check events were fired
        event_types = [event[0] for event in self.events]
        self.assertIn("combat_started", event_types)
        self.assertIn("combat_ended", event_types)
    
    async def test_action_processing(self):
        """Test async action processing."""
        self.engine.start_combat(["player", "enemy1"])
        
        # Mock the action resolution methods
        self.engine._resolve_card_play = AsyncMock()
        self.engine._resolve_ability = AsyncMock()
        
        # Queue actions
        card_action = CombatAction(ActionType.PLAY_CARD, "player")
        ability_action = CombatAction(ActionType.ABILITY, "enemy1")
        
        self.engine.queue_action(card_action)
        self.engine.queue_action(ability_action)
        
        # Process actions
        await self.engine.process_actions()
        
        # Verify resolution methods were called
        self.engine._resolve_card_play.assert_called_once()
        self.engine._resolve_ability.assert_called_once()
        
        # Verify queue is empty
        self.assertFalse(self.engine.action_queue.has_actions())


if __name__ == '__main__':
    # Run async tests
    async def run_async_tests():
        suite = unittest.TestSuite()
        suite.addTest(CombatIntegrationTestCase('test_action_processing'))
        
        # Create a custom test runner for async tests
        for test in suite:
            await test.test_action_processing()
    
    # Run regular tests
    unittest.main(exit=False)
    
    # Run async tests
    asyncio.run(run_async_tests())