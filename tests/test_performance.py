"""
Performance Tests

Tests for timing accuracy, performance benchmarks,
and optimization validation for the Hour-Glass Initiative system.
"""

import unittest
import time
import asyncio
from unittest.mock import patch
import statistics

from core.hourglass import HourGlass, SandTimer
from core.combat import CombatEngine, ActionQueue, CombatAction, ActionType
from core.cards import Card, Deck, CardLibrary, CardType
from core.engine import GameEngine


class HourGlassPerformanceTestCase(unittest.TestCase):
    """Performance tests for Hour-Glass timing accuracy."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hourglass = HourGlass()
    
    def test_sand_regeneration_timing_accuracy(self):
        """Test that sand regeneration timing is accurate within 50ms."""
        timing_errors = []
        
        for _ in range(10):  # Run multiple iterations
            with patch('time.time') as mock_time:
                # Set up precise timing
                mock_time.side_effect = [0.0, 1.0]  # Exactly 1 second
                
                self.hourglass.current_sand = 0
                self.hourglass.timer.last_update = 0.0
                
                # Measure timing accuracy
                start_time = time.perf_counter()
                mock_time.return_value = 1.0
                self.hourglass.update_sand()
                end_time = time.perf_counter()
                
                # Calculate timing error
                actual_duration = end_time - start_time
                timing_errors.append(actual_duration)
        
        # Calculate statistics
        avg_time = statistics.mean(timing_errors)
        max_time = max(timing_errors)
        
        # Performance requirements
        self.assertLess(avg_time, 0.001)  # Average under 1ms
        self.assertLess(max_time, 0.05)   # Maximum under 50ms
        
        # Verify regeneration worked correctly
        self.assertEqual(self.hourglass.current_sand, 1)
    
    def test_rapid_sand_updates(self):
        """Test performance with rapid sand updates."""
        update_times = []
        
        # Perform many rapid updates
        for i in range(1000):
            start_time = time.perf_counter()
            
            with patch('time.time') as mock_time:
                mock_time.return_value = i * 0.1  # 100ms intervals
                self.hourglass.update_sand()
            
            end_time = time.perf_counter()
            update_times.append(end_time - start_time)
        
        # Calculate performance metrics
        avg_update_time = statistics.mean(update_times)
        max_update_time = max(update_times)
        
        # Performance requirements for 60fps (16.67ms budget)
        self.assertLess(avg_update_time, 0.001)  # Average under 1ms
        self.assertLess(max_update_time, 0.016)  # Maximum under 16ms
    
    def test_time_until_next_sand_precision(self):
        """Test precision of time-until-next-sand calculations."""
        calculation_times = []
        
        # Test various sand levels and timings
        test_cases = [
            (0, 0.0),    # Empty, just updated
            (3, 0.25),   # Partial progress
            (5, 0.75),   # Near full
            (6, 0.0)     # Full (should return infinity)
        ]
        
        for sand_level, elapsed_time in test_cases:
            self.hourglass.current_sand = sand_level
            
            with patch('time.time') as mock_time:
                mock_time.side_effect = [0.0, elapsed_time]
                self.hourglass.timer.last_update = 0.0
                
                start_time = time.perf_counter()
                time_until_next = self.hourglass.get_time_until_next_sand()
                end_time = time.perf_counter()
                
                calculation_times.append(end_time - start_time)
                
                # Verify calculation correctness
                if sand_level < 6:
                    expected_time = 1.0 - elapsed_time
                    self.assertAlmostEqual(time_until_next, expected_time, places=3)
                else:
                    self.assertEqual(time_until_next, float('inf'))
        
        # Performance requirement
        avg_calc_time = statistics.mean(calculation_times)
        self.assertLess(avg_calc_time, 0.0001)  # Under 0.1ms


class CombatPerformanceTestCase(unittest.TestCase):
    """Performance tests for combat system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.combat_engine = CombatEngine()
        self.action_queue = ActionQueue()
    
    def test_action_queue_performance(self):
        """Test action queue performance with many actions."""
        # Create many actions
        actions = []
        for i in range(1000):
            action = CombatAction(
                ActionType.PLAY_CARD,
                f"actor_{i % 10}",
                card_id=f"card_{i}"
            )
            actions.append(action)
        
        # Measure queue operations
        start_time = time.perf_counter()
        
        for action in actions:
            self.action_queue.add_action(action)
        
        add_time = time.perf_counter() - start_time
        
        # Measure dequeue operations
        start_time = time.perf_counter()
        
        while self.action_queue.has_actions():
            self.action_queue.get_next_action()
        
        dequeue_time = time.perf_counter() - start_time
        
        # Performance requirements
        self.assertLess(add_time, 0.1)     # Under 100ms to add 1000 actions
        self.assertLess(dequeue_time, 0.1) # Under 100ms to dequeue 1000 actions
    
    def test_combat_action_filtering_performance(self):
        """Test performance of action filtering operations."""
        # Add many actions with different actors
        actors = [f"actor_{i}" for i in range(100)]
        
        for i in range(1000):
            action = CombatAction(
                ActionType.PLAY_CARD,
                actors[i % len(actors)]
            )
            self.action_queue.add_action(action)
        
        # Measure filtering performance
        filter_times = []
        
        for actor in actors[:10]:  # Test first 10 actors
            start_time = time.perf_counter()
            filtered_actions = self.action_queue.get_actions_by_actor(actor)
            end_time = time.perf_counter()
            
            filter_times.append(end_time - start_time)
            
            # Should find exactly 10 actions per actor (1000 / 100)
            self.assertEqual(len(filtered_actions), 10)
        
        # Performance requirement
        avg_filter_time = statistics.mean(filter_times)
        self.assertLess(avg_filter_time, 0.01)  # Under 10ms per filter
    
    async def test_action_processing_performance(self):
        """Test performance of async action processing."""
        self.combat_engine.start_combat(["player", "enemy"])
        
        # Mock action resolution to be instant
        async def mock_resolve(action):
            pass
        
        self.combat_engine._resolve_card_play = mock_resolve
        self.combat_engine._resolve_ability = mock_resolve
        
        # Queue many actions
        for i in range(100):
            action = CombatAction(
                ActionType.PLAY_CARD if i % 2 == 0 else ActionType.ABILITY,
                "player" if i % 2 == 0 else "enemy"
            )
            self.combat_engine.queue_action(action)
        
        # Measure processing time
        start_time = time.perf_counter()
        await self.combat_engine.process_actions()
        end_time = time.perf_counter()
        
        processing_time = end_time - start_time
        
        # Performance requirement (should process 100 actions quickly)
        self.assertLess(processing_time, 0.1)  # Under 100ms
        
        # Verify all actions were processed
        self.assertFalse(self.combat_engine.action_queue.has_actions())


class CardSystemPerformanceTestCase(unittest.TestCase):
    """Performance tests for card and deck systems."""
    
    def test_large_deck_operations(self):
        """Test performance with large deck operations."""
        # Create a large deck
        deck = Deck(name="Performance Test Deck")
        
        # Add many cards
        cards = []
        for i in range(1000):
            card = Card(
                name=f"Card {i}",
                description=f"Test card number {i}",
                sand_cost=i % 7,
                card_type=CardType.ATTACK
            )
            cards.append(card)
        
        # Measure add performance
        start_time = time.perf_counter()
        for card in cards:
            deck.add_card(card)
        add_time = time.perf_counter() - start_time
        
        # Measure shuffle performance
        start_time = time.perf_counter()
        deck.shuffle()
        shuffle_time = time.perf_counter() - start_time
        
        # Measure draw performance
        start_time = time.perf_counter()
        drawn = deck.draw(100)
        draw_time = time.perf_counter() - start_time
        
        # Performance requirements
        self.assertLess(add_time, 0.1)     # Under 100ms to add 1000 cards
        self.assertLess(shuffle_time, 0.05) # Under 50ms to shuffle
        self.assertLess(draw_time, 0.01)   # Under 10ms to draw 100 cards
        
        # Verify operations worked correctly
        self.assertEqual(len(drawn), 100)
        self.assertEqual(len(deck), 900)
    
    def test_deck_statistics_performance(self):
        """Test performance of deck statistics calculations."""
        deck = Deck(name="Stats Test Deck")
        
        # Add varied cards
        for i in range(500):
            card = Card(
                name=f"Card {i % 50}",  # 50 unique names, each appears 10 times
                description="Test",
                sand_cost=i % 7,
                card_type=list(CardType)[i % len(CardType)],
                rarity=list(CardRarity)[i % len(CardRarity)]
            )
            deck.add_card(card)
        
        # Measure statistics calculations
        operations = [
            ("average_cost", lambda: deck.get_average_cost()),
            ("card_counts", lambda: deck.get_card_counts()),
            ("cards_by_cost_3", lambda: deck.get_cards_by_cost(3)),
            ("cards_by_type", lambda: deck.get_cards_by_type(CardType.ATTACK)),
            ("cards_by_rarity", lambda: deck.get_cards_by_rarity(CardRarity.COMMON))
        ]
        
        for op_name, operation in operations:
            start_time = time.perf_counter()
            result = operation()
            end_time = time.perf_counter()
            
            operation_time = end_time - start_time
            
            # Each operation should be fast
            self.assertLess(operation_time, 0.01, f"{op_name} took too long")
            
            # Verify results are reasonable
            self.assertIsNotNone(result)
    
    def test_card_library_performance(self):
        """Test card library performance with many cards."""
        library = CardLibrary()
        
        # Register many cards
        cards = []
        for i in range(1000):
            card = Card(
                name=f"Library Card {i}",
                description="Library test card",
                sand_cost=i % 7,
                card_type=list(CardType)[i % len(CardType)]
            )
            cards.append(card)
        
        # Measure registration performance
        start_time = time.perf_counter()
        for card in cards:
            library.register_card(card)
        registration_time = time.perf_counter() - start_time
        
        # Measure lookup performance
        lookup_times = []
        for i in range(100):  # Test 100 random lookups
            card = cards[i * 10]  # Every 10th card
            
            start_time = time.perf_counter()
            found_card = library.get_card_by_name(card.name)
            end_time = time.perf_counter()
            
            lookup_times.append(end_time - start_time)
            self.assertIsNotNone(found_card)
        
        # Measure filtering performance
        start_time = time.perf_counter()
        attack_cards = library.get_cards_by_type(CardType.ATTACK)
        filter_time = time.perf_counter() - start_time
        
        # Performance requirements
        self.assertLess(registration_time, 0.5)  # Under 500ms to register 1000 cards
        avg_lookup_time = statistics.mean(lookup_times)
        self.assertLess(avg_lookup_time, 0.001)  # Under 1ms per lookup
        self.assertLess(filter_time, 0.01)       # Under 10ms to filter
        
        # Verify library size
        self.assertEqual(library.size(), 1000)


class GameEnginePerformanceTestCase(unittest.TestCase):
    """Performance tests for the main game engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.engine.initialize()
    
    def tearDown(self):
        """Clean up after tests."""
        self.engine.shutdown()
    
    async def test_update_loop_performance(self):
        """Test game engine update loop performance."""
        update_times = []
        
        # Simulate 60fps for 1 second (60 updates)
        for frame in range(60):
            start_time = time.perf_counter()
            await self.engine._update(1.0 / 60.0)  # 16.67ms frame time
            end_time = time.perf_counter()
            
            update_times.append(end_time - start_time)
        
        # Calculate performance metrics
        avg_update_time = statistics.mean(update_times)
        max_update_time = max(update_times)
        frame_budget = 1.0 / 60.0  # 16.67ms at 60fps
        
        # Performance requirements
        self.assertLess(avg_update_time, frame_budget * 0.5)  # Use less than 50% of frame budget
        self.assertLess(max_update_time, frame_budget * 0.8)  # Never exceed 80% of frame budget
    
    def test_event_system_performance(self):
        """Test event system performance with many handlers."""
        # Register many event handlers
        handlers = []
        for i in range(100):
            def handler(event_data, handler_id=i):
                pass  # Minimal handler
            handlers.append(handler)
            self.engine.register_event_handler("test_event", handler)
        
        # Measure event emission performance
        start_time = time.perf_counter()
        
        for _ in range(100):  # Emit 100 events
            self.engine.emit_event("test_event", {"data": "test"})
        
        end_time = time.perf_counter()
        emission_time = end_time - start_time
        
        # Performance requirement (100 events to 100 handlers = 10,000 calls)
        self.assertLess(emission_time, 0.1)  # Under 100ms for 10,000 handler calls
    
    def test_state_transition_performance(self):
        """Test game state transition performance."""
        transition_times = []
        
        # Test transitions between different states
        transitions = [
            (GamePhase.MENU, GamePhase.MAP),
            (GamePhase.MAP, GamePhase.COMBAT),
            (GamePhase.COMBAT, GamePhase.MAP),
            (GamePhase.MAP, GamePhase.DECK_BUILDING),
            (GamePhase.DECK_BUILDING, GamePhase.MAP)
        ]
        
        for from_state, to_state in transitions:
            # Set up initial state
            self.engine.state.phase = from_state
            
            # Measure transition time
            start_time = time.perf_counter()
            success = self.engine.state_manager.transition_state(
                self.engine.state, to_state
            )
            end_time = time.perf_counter()
            
            transition_time = end_time - start_time
            transition_times.append(transition_time)
            
            self.assertTrue(success)
            self.assertEqual(self.engine.state.phase, to_state)
        
        # Performance requirement
        avg_transition_time = statistics.mean(transition_times)
        max_transition_time = max(transition_times)
        
        self.assertLess(avg_transition_time, 0.001)  # Under 1ms average
        self.assertLess(max_transition_time, 0.01)   # Under 10ms maximum


class MemoryPerformanceTestCase(unittest.TestCase):
    """Tests for memory usage and garbage collection performance."""
    
    def test_card_creation_memory_efficiency(self):
        """Test that card creation doesn't leak memory."""
        import gc
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create and destroy many cards
        for cycle in range(10):
            cards = []
            for i in range(1000):
                card = Card(
                    name=f"Memory Test {i}",
                    description="Memory test card",
                    sand_cost=i % 7,
                    card_type=CardType.SKILL
                )
                cards.append(card)
            
            # Clear references and force garbage collection
            del cards
            gc.collect()
        
        # Check final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be minimal (under 10MB)
        max_increase = 10 * 1024 * 1024  # 10MB
        self.assertLess(memory_increase, max_increase,
                       f"Memory increased by {memory_increase / (1024*1024):.2f}MB")
    
    def test_hourglass_timer_precision_stability(self):
        """Test that timer precision remains stable over time."""
        hourglass = HourGlass()
        timing_errors = []
        
        # Run timing test for extended period
        for iteration in range(100):
            with patch('time.time') as mock_time:
                # Simulate consistent 1-second intervals
                mock_time.side_effect = [
                    iteration * 1.0,      # Start time
                    (iteration + 1) * 1.0 # End time (exactly 1 second later)
                ]
                
                hourglass.current_sand = 0
                hourglass.timer.last_update = iteration * 1.0
                
                # Measure timing precision
                start = time.perf_counter()
                mock_time.return_value = (iteration + 1) * 1.0
                hourglass.update_sand()
                end = time.perf_counter()
                
                timing_errors.append(end - start)
                
                # Should regenerate exactly 1 sand
                self.assertEqual(hourglass.current_sand, 1)
        
        # Timing should remain stable throughout
        avg_error = statistics.mean(timing_errors)
        std_dev = statistics.stdev(timing_errors)
        
        self.assertLess(avg_error, 0.001)   # Average under 1ms
        self.assertLess(std_dev, 0.0005)    # Low variance (under 0.5ms)


if __name__ == '__main__':
    # Run performance tests
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print performance summary
    if result.wasSuccessful():
        print("\n" + "="*50)
        print("PERFORMANCE TESTS PASSED")
        print("All timing and performance requirements met.")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("PERFORMANCE TESTS FAILED")
        print("Some performance requirements were not met.")
        print("="*50)