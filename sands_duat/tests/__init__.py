"""
Automated Testing Suite

Comprehensive test suite for Sands of Duat, covering unit tests,
integration tests, and gameplay validation.

Key Features:
- Unit tests for core systems (Hour-Glass, Cards, Combat)
- Integration tests for system interactions
- Performance tests for timing accuracy
- Content validation tests for YAML data
- Mock objects for isolated testing

Test Categories:
- test_hourglass.py: Sand regeneration and timing tests
- test_combat.py: Combat engine and action queue tests
- test_cards.py: Card system and effect tests
- test_content.py: YAML content validation tests
- test_integration.py: Full system integration tests
- test_performance.py: Performance and timing tests

The test suite is designed to ensure the Hour-Glass Initiative
timing mechanics work accurately and consistently across all
game systems.
"""

import sys
import unittest
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .test_hourglass import HourGlassTestCase
from .test_combat import CombatTestCase  
from .test_cards import CardTestCase
from .test_content import ContentTestCase
from .test_integration import IntegrationTestCase
from .test_performance import PerformanceTestCase

__all__ = [
    'HourGlassTestCase',
    'CombatTestCase',
    'CardTestCase', 
    'ContentTestCase',
    'IntegrationTestCase',
    'PerformanceTestCase'
]


def create_test_suite():
    """Create a complete test suite for the project."""
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        HourGlassTestCase,
        CombatTestCase,
        CardTestCase,
        ContentTestCase,
        IntegrationTestCase,
        PerformanceTestCase
    ]
    
    for test_case in test_cases:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    
    return suite


def run_all_tests():
    """Run all tests and return results."""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    # Run tests when module is executed directly
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)