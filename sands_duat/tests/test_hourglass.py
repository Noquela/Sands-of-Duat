"""
Hour-Glass System Tests

Tests for the core Hour-Glass Initiative timing mechanics,
ensuring accurate sand regeneration and timing precision.
"""

import unittest
import time
from unittest.mock import patch, MagicMock

from sands_duat.core.hourglass import HourGlass, SandTimer


class HourGlassTestCase(unittest.TestCase):
    """Test cases for Hour-Glass sand management system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hourglass = HourGlass()
        self.callback_calls = []
        
        def test_callback(sand_amount):
            self.callback_calls.append(sand_amount)
        
        self.hourglass.on_sand_change = test_callback
    
    def test_initial_state(self):
        """Test initial hourglass state."""
        self.assertEqual(self.hourglass.current_sand, 0)
        self.assertEqual(self.hourglass.max_sand, 6)
        self.assertFalse(self.hourglass.timer.is_paused)
    
    def test_sand_spending(self):
        """Test sand spending mechanics."""
        # Set initial sand
        self.hourglass.set_sand(3)
        
        # Test successful spending
        self.assertTrue(self.hourglass.spend_sand(2))
        self.assertEqual(self.hourglass.current_sand, 1)
        
        # Test insufficient sand
        self.assertFalse(self.hourglass.spend_sand(3))
        self.assertEqual(self.hourglass.current_sand, 1)
        
        # Test exact spending
        self.assertTrue(self.hourglass.spend_sand(1))
        self.assertEqual(self.hourglass.current_sand, 0)
    
    def test_can_afford(self):
        """Test sand cost checking."""
        self.hourglass.set_sand(3)
        
        self.assertTrue(self.hourglass.can_afford(0))
        self.assertTrue(self.hourglass.can_afford(3))
        self.assertFalse(self.hourglass.can_afford(4))
        self.assertFalse(self.hourglass.can_afford(6))
    
    def test_sand_callbacks(self):
        """Test sand change callbacks."""
        self.hourglass.set_sand(2)
        self.assertIn(2, self.callback_calls)
        
        self.hourglass.spend_sand(1)
        self.assertIn(1, self.callback_calls)
    
    def test_pause_resume(self):
        """Test pausing and resuming sand regeneration."""
        self.hourglass.pause_regeneration()
        self.assertTrue(self.hourglass.timer.is_paused)
        
        self.hourglass.resume_regeneration()
        self.assertFalse(self.hourglass.timer.is_paused)
    
    @patch('time.time')
    def test_sand_regeneration(self, mock_time):
        """Test sand regeneration over time."""
        # Mock time progression
        mock_time.side_effect = [0.0, 1.0, 2.0, 3.0]  # 0, 1, 2, 3 seconds
        
        # Start with empty hourglass
        self.hourglass.current_sand = 0
        self.hourglass.timer.last_update = 0.0
        
        # After 1 second, should have 1 sand
        mock_time.return_value = 1.0
        self.hourglass.update_sand()
        self.assertEqual(self.hourglass.current_sand, 1)
        
        # After 2 more seconds, should have 3 sand total
        mock_time.return_value = 3.0
        self.hourglass.update_sand()
        self.assertEqual(self.hourglass.current_sand, 3)
    
    @patch('time.time')
    def test_sand_regeneration_cap(self, mock_time):
        """Test that sand regeneration doesn't exceed max capacity."""
        mock_time.side_effect = [0.0, 10.0]  # 10 seconds later
        
        self.hourglass.current_sand = 0
        self.hourglass.timer.last_update = 0.0
        
        mock_time.return_value = 10.0
        self.hourglass.update_sand()
        
        # Should cap at max_sand (6), not regenerate 10 sand
        self.assertEqual(self.hourglass.current_sand, 6)
    
    @patch('time.time')
    def test_time_until_next_sand(self, mock_time):
        """Test calculation of time until next sand grain."""
        mock_time.return_value = 0.5  # 0.5 seconds after last update
        
        self.hourglass.current_sand = 3
        self.hourglass.timer.last_update = 0.0
        
        time_until_next = self.hourglass.get_time_until_next_sand()
        self.assertAlmostEqual(time_until_next, 0.5, places=2)
        
        # When at max sand, should return infinity
        self.hourglass.current_sand = 6
        time_until_next = self.hourglass.get_time_until_next_sand()
        self.assertEqual(time_until_next, float('inf'))
    
    def test_sand_bounds(self):
        """Test sand amount bounds validation."""
        # Test setting sand within bounds
        self.hourglass.set_sand(3)
        self.assertEqual(self.hourglass.current_sand, 3)
        
        # Test setting sand above max
        self.hourglass.set_sand(10)
        self.assertEqual(self.hourglass.current_sand, 6)
        
        # Test setting negative sand
        self.hourglass.set_sand(-5)
        self.assertEqual(self.hourglass.current_sand, 0)
    
    def test_paused_regeneration(self):
        """Test that paused regeneration doesn't update sand."""
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0.0, 5.0]  # 5 seconds later
            
            self.hourglass.current_sand = 0
            self.hourglass.timer.last_update = 0.0
            self.hourglass.pause_regeneration()
            
            mock_time.return_value = 5.0
            self.hourglass.update_sand()
            
            # Should still be 0 because regeneration is paused
            self.assertEqual(self.hourglass.current_sand, 0)


class SandTimerTestCase(unittest.TestCase):
    """Test cases for SandTimer precision timing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.timer = SandTimer()
    
    def test_initial_state(self):
        """Test initial timer state."""
        self.assertFalse(self.timer.is_paused)
        self.assertEqual(self.timer.regeneration_rate, 1.0)
    
    @patch('time.time')
    def test_elapsed_time_calculation(self, mock_time):
        """Test elapsed time calculation."""
        mock_time.side_effect = [0.0, 2.5]
        
        self.timer.last_update = 0.0
        mock_time.return_value = 2.5
        
        elapsed = self.timer.get_elapsed_time()
        self.assertAlmostEqual(elapsed, 2.5, places=2)
    
    def test_pause_elapsed_time(self):
        """Test that paused timer returns 0 elapsed time."""
        self.timer.pause()
        elapsed = self.timer.get_elapsed_time()
        self.assertEqual(elapsed, 0.0)
    
    @patch('time.time')
    def test_resume_updates_timestamp(self, mock_time):
        """Test that resuming updates the timestamp."""
        mock_time.return_value = 5.0
        
        self.timer.pause()
        self.timer.resume()
        
        self.assertEqual(self.timer.last_update, 5.0)
        self.assertFalse(self.timer.is_paused)
    
    def test_custom_regeneration_rate(self):
        """Test custom regeneration rates."""
        timer = SandTimer(regeneration_rate=2.0)  # 2 sand per second
        self.assertEqual(timer.regeneration_rate, 2.0)
        
        timer = SandTimer(regeneration_rate=0.5)  # 0.5 sand per second
        self.assertEqual(timer.regeneration_rate, 0.5)


if __name__ == '__main__':
    unittest.main()