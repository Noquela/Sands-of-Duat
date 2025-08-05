"""
Test Suite for Performance Optimization Systems

Tests that all optimization systems can be imported and initialized correctly.
Run this to verify the performance optimization suite is properly integrated.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test imports
try:
    from sands_duat.graphics.enhanced_asset_streaming import get_asset_streaming_manager
    from sands_duat.graphics.parallax_background_system import get_parallax_renderer
    from sands_duat.graphics.dynamic_quality_manager import get_quality_manager
    from sands_duat.graphics.advanced_memory_manager import get_memory_manager
    from sands_duat.graphics.comprehensive_profiler import get_comprehensive_profiler
    from sands_duat.graphics.performance_integration import get_performance_coordinator
    print("✓ All performance optimization modules imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)


class TestPerformanceOptimization(unittest.TestCase):
    """Test performance optimization systems."""
    
    def setUp(self):
        """Setup test environment."""
        self.screen_width = 1920
        self.screen_height = 1080
    
    def test_asset_streaming_manager(self):
        """Test asset streaming manager initialization."""
        try:
            manager = get_asset_streaming_manager()
            self.assertIsNotNone(manager)
            
            # Test basic functionality
            stats = manager.get_comprehensive_stats()
            self.assertIsInstance(stats, dict)
            
            print("✓ Asset Streaming Manager: OK")
        except Exception as e:
            self.fail(f"Asset Streaming Manager failed: {e}")
    
    def test_parallax_renderer(self):
        """Test parallax renderer initialization."""
        try:
            renderer = get_parallax_renderer(self.screen_width, self.screen_height)
            self.assertIsNotNone(renderer)
            
            # Test basic functionality
            stats = renderer.get_render_statistics()
            self.assertIsInstance(stats, dict)
            
            print("✓ Parallax Renderer: OK")
        except Exception as e:
            self.fail(f"Parallax Renderer failed: {e}")
    
    def test_quality_manager(self):
        """Test quality manager initialization."""
        try:
            manager = get_quality_manager()
            self.assertIsNotNone(manager)
            
            # Test basic functionality
            settings = manager.get_current_settings()
            self.assertIsNotNone(settings)
            
            report = manager.get_performance_report()
            self.assertIsInstance(report, dict)
            
            print("✓ Quality Manager: OK")
        except Exception as e:
            self.fail(f"Quality Manager failed: {e}")
    
    def test_memory_manager(self):
        """Test memory manager initialization."""
        try:
            manager = get_memory_manager()
            self.assertIsNotNone(manager)
            
            # Test basic functionality
            report = manager.get_memory_report()
            self.assertIsInstance(report, dict)
            
            print("✓ Memory Manager: OK")
        except Exception as e:
            self.fail(f"Memory Manager failed: {e}")
    
    def test_comprehensive_profiler(self):
        """Test comprehensive profiler initialization."""
        try:
            profiler = get_comprehensive_profiler()
            self.assertIsNotNone(profiler)
            
            # Test basic functionality
            metrics = profiler.get_real_time_metrics()
            self.assertIsInstance(metrics, dict)
            
            print("✓ Comprehensive Profiler: OK")
        except Exception as e:
            self.fail(f"Comprehensive Profiler failed: {e}")
    
    def test_performance_coordinator(self):
        """Test performance coordinator initialization."""
        try:
            coordinator = get_performance_coordinator(self.screen_width, self.screen_height)
            self.assertIsNotNone(coordinator)
            
            # Test basic functionality
            dashboard = coordinator.get_performance_dashboard()
            self.assertIsInstance(dashboard, dict)
            
            print("✓ Performance Coordinator: OK")
        except Exception as e:
            self.fail(f"Performance Coordinator failed: {e}")
    
    def test_integration_systems(self):
        """Test that all systems can work together."""
        try:
            from sands_duat.graphics.performance_integration import (
                initialize_performance_systems,
                ScreenType,
                PerformanceMode
            )
            
            # Initialize integrated systems
            coordinator = initialize_performance_systems(self.screen_width, self.screen_height)
            self.assertIsNotNone(coordinator)
            
            # Test screen switching
            coordinator.set_screen(ScreenType.COMBAT)
            coordinator.set_screen(ScreenType.MENU)
            
            # Test performance mode switching
            coordinator.set_performance_mode(PerformanceMode.ADAPTIVE)
            coordinator.set_performance_mode(PerformanceMode.BALANCED)
            
            print("✓ Integration Systems: OK")
        except Exception as e:
            self.fail(f"Integration Systems failed: {e}")
    
    def test_performance_targets(self):
        """Test that performance targets are reasonable."""
        try:
            coordinator = get_performance_coordinator()
            
            # Check that performance targets exist for all screen types
            from sands_duat.graphics.performance_integration import ScreenType
            
            for screen_type in ScreenType:
                target = coordinator.performance_targets.get(screen_type)
                self.assertIsNotNone(target, f"No performance target for {screen_type}")
                self.assertGreater(target.target_fps, 0)
                self.assertGreater(target.memory_budget_mb, 0)
            
            print("✓ Performance Targets: OK")
        except Exception as e:
            self.fail(f"Performance Targets failed: {e}")


def main():
    """Run performance optimization tests."""
    print("Sands of Duat - Performance Optimization Test Suite")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("Performance optimization systems ready!")
    print("\nTo see the systems in action, run:")
    print("python examples/performance_optimization_showcase.py")


if __name__ == "__main__":
    main()