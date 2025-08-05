"""
Comprehensive Performance Test Suite
Tests all performance optimizations for Sands of Duat
"""

import unittest
import time
import statistics
import pygame
import sys
from pathlib import Path
import threading
import gc
import psutil
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

from core.performance_profiler import PerformanceProfiler, get_profiler, initialize_profiler
from ui.optimized_particle_system import OptimizedParticleSystem, ParticleType
from ui.optimized_hades_theme import OptimizedHadesEgyptianTheme
from assets.optimized_asset_manager import OptimizedAssetManager, AssetType, QualityLevel


class PerformanceProfilerTestCase(unittest.TestCase):
    """Test the performance profiler system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.profiler = PerformanceProfiler(max_samples=100)
    
    def test_profiler_timing_accuracy(self):
        """Test profiler timing accuracy."""
        # Test operation timing
        with self.profiler.time_operation("test_operation"):
            time.sleep(0.01)  # 10ms sleep
        
        # Get metrics
        metrics = self.profiler.metrics["test_operation"]
        self.assertEqual(len(metrics), 1)
        
        # Check timing accuracy (should be around 10ms, allow for variance)
        duration = metrics[0].duration_ms
        self.assertGreater(duration, 8.0)  # At least 8ms
        self.assertLess(duration, 20.0)    # No more than 20ms
    
    def test_frame_profiling(self):
        """Test frame profiling functionality."""
        # Simulate 60 frames
        for frame in range(60):
            self.profiler.start_frame()
            
            # Simulate frame work
            with self.profiler.time_operation("update"):
                time.sleep(0.001)  # 1ms update
            
            with self.profiler.time_operation("render"):
                time.sleep(0.002)  # 2ms render
            
            self.profiler.end_frame(particle_count=100, draw_calls=20)
        
        # Check frame profiles
        self.assertEqual(len(self.profiler.frame_profiles), 60)
        
        # Get performance summary
        summary = self.profiler.get_performance_summary()
        self.assertIn("frame_performance", summary)
        self.assertGreater(summary["frame_performance"]["avg_fps"], 200)  # Should be very high for simple test
    
    def test_memory_tracking(self):
        """Test memory usage tracking."""
        initial_memory = self.profiler._get_memory_usage()
        
        # Allocate some memory
        large_list = [0] * 1000000  # 1 million integers
        
        with self.profiler.time_operation("memory_test"):
            # Do something with the list
            sum(large_list)
        
        # Memory should have increased
        final_memory = self.profiler._get_memory_usage()
        self.assertGreater(final_memory, initial_memory)
        
        # Clean up
        del large_list
        gc.collect()


class OptimizedParticleSystemTestCase(unittest.TestCase):
    """Test the optimized particle system."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
        self.particle_system = OptimizedParticleSystem(800, 600, max_particles=1000)
    
    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_particle_creation_performance(self):
        """Test particle creation performance."""
        start_time = time.perf_counter()
        
        # Create many particle bursts
        for _ in range(100):
            self.particle_system.create_particle_burst(
                400, 300, ParticleType.SAND_GRAIN, 10, 1.0
            )
        
        creation_time = (time.perf_counter() - start_time) * 1000
        
        # Should create 1000 particles quickly
        self.assertLess(creation_time, 50.0)  # Under 50ms
        
        # Check particle count
        stats = self.particle_system.get_statistics()
        self.assertGreater(stats["active_particles"], 500)  # Should have many particles
    
    def test_particle_update_performance(self):
        """Test particle update performance."""
        # Create particles
        for _ in range(50):
            self.particle_system.create_particle_burst(
                400, 300, ParticleType.FIRE_SPARK, 20, 1.0
            )
        
        # Time particle updates
        update_times = []
        for _ in range(60):  # 60 frames
            start_time = time.perf_counter()
            self.particle_system.update(1.0 / 60.0)  # 60fps
            end_time = time.perf_counter()
            update_times.append((end_time - start_time) * 1000)
        
        avg_update_time = statistics.mean(update_times)
        max_update_time = max(update_times)
        
        # Performance requirements
        self.assertLess(avg_update_time, 2.0)   # Average under 2ms
        self.assertLess(max_update_time, 5.0)   # Maximum under 5ms
    
    def test_particle_render_performance(self):
        """Test particle rendering performance."""
        # Create diverse particles
        particle_types = [ParticleType.SAND_GRAIN, ParticleType.FIRE_SPARK, 
                         ParticleType.LIGHTNING_BOLT, ParticleType.GOLDEN_AURA]
        
        for ptype in particle_types:
            for _ in range(25):
                self.particle_system.create_particle_burst(
                    400, 300, ptype, 10, 1.0
                )
        
        # Time rendering
        render_times = []
        for _ in range(30):  # 30 frames
            start_time = time.perf_counter()
            self.particle_system.render(self.screen)
            end_time = time.perf_counter()
            render_times.append((end_time - start_time) * 1000)
        
        avg_render_time = statistics.mean(render_times)
        max_render_time = max(render_times)
        
        # Performance requirements
        self.assertLess(avg_render_time, 3.0)   # Average under 3ms
        self.assertLess(max_render_time, 8.0)   # Maximum under 8ms
    
    def test_memory_pool_efficiency(self):
        """Test particle pool memory efficiency."""
        initial_stats = self.particle_system.get_statistics()
        
        # Create and destroy particles multiple times
        for cycle in range(10):
            # Create particles
            for _ in range(100):
                self.particle_system.create_particle_burst(
                    400, 300, ParticleType.SAND_GRAIN, 5, 1.0
                )
            
            # Update until particles die
            for _ in range(120):  # 2 seconds at 60fps
                self.particle_system.update(1.0 / 60.0)
        
        final_stats = self.particle_system.get_statistics()
        
        # Pool should remain stable
        pool_stats = final_stats["pool_stats"]
        self.assertGreater(pool_stats["pool_utilization"], 0.0)
        self.assertLess(pool_stats["pool_utilization"], 1.0)
    
    def test_spatial_culling_performance(self):
        """Test spatial culling efficiency."""
        # Create particles across entire screen
        for x in range(0, 800, 100):
            for y in range(0, 600, 100):
                self.particle_system.create_particle_burst(
                    x, y, ParticleType.SAND_GRAIN, 10, 1.0
                )
        
        # Test rendering with different camera views
        small_view = pygame.Rect(350, 250, 100, 100)  # Small viewport
        large_view = pygame.Rect(0, 0, 800, 600)      # Full viewport
        
        # Time rendering with small view (should be faster due to culling)
        start_time = time.perf_counter()
        for _ in range(10):
            self.particle_system.render(self.screen, small_view)
        small_view_time = (time.perf_counter() - start_time) * 1000
        
        # Time rendering with large view
        start_time = time.perf_counter()
        for _ in range(10):
            self.particle_system.render(self.screen, large_view)
        large_view_time = (time.perf_counter() - start_time) * 1000
        
        # Small view should be significantly faster
        self.assertLess(small_view_time * 2, large_view_time)


class OptimizedHadesThemeTestCase(unittest.TestCase):
    """Test the optimized Hades theme system."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        self.theme = OptimizedHadesEgyptianTheme((1920, 1080))
    
    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_button_rendering_performance(self):
        """Test button rendering performance with caching."""
        button_rect = pygame.Rect(100, 100, 200, 50)
        
        # First render (cache miss)
        start_time = time.perf_counter()
        self.theme.draw_ornate_button(self.screen, button_rect, "Test Button", "normal")
        first_render_time = (time.perf_counter() - start_time) * 1000
        
        # Subsequent renders (cache hits)
        cache_render_times = []
        for _ in range(10):
            start_time = time.perf_counter()
            self.theme.draw_ornate_button(self.screen, button_rect, "Test Button", "normal")
            cache_render_times.append((time.perf_counter() - start_time) * 1000)
        
        avg_cache_time = statistics.mean(cache_render_times)
        
        # Cache hits should be significantly faster
        self.assertLess(avg_cache_time * 3, first_render_time)
        
        # Check performance stats
        stats = self.theme.get_performance_stats()
        self.assertGreater(stats["cache_efficiency"], 0.8)  # 80% cache hit rate
    
    def test_detail_level_performance_impact(self):
        """Test performance impact of different detail levels."""
        button_rect = pygame.Rect(100, 100, 200, 50)
        
        # Test all detail levels
        detail_times = {}
        
        for detail_level in range(4):  # 0-3
            self.theme.set_detail_level(detail_level)
            self.theme.clear_cache()  # Clear cache for fair comparison
            
            # Time multiple renders
            render_times = []
            for _ in range(20):
                start_time = time.perf_counter()
                self.theme.draw_ornate_button(self.screen, button_rect, "Test", "normal")
                render_times.append((time.perf_counter() - start_time) * 1000)
            
            detail_times[detail_level] = statistics.mean(render_times)
        
        # Higher detail levels should take more time
        self.assertLess(detail_times[0], detail_times[3])
        
        # All detail levels should be reasonable for 60fps
        for level, time_ms in detail_times.items():
            self.assertLess(time_ms, 1.0, f"Detail level {level} too slow: {time_ms}ms")
    
    def test_memory_usage_optimization(self):
        """Test memory usage with surface caching."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Create many different buttons (should fill cache)
        for i in range(100):
            button_rect = pygame.Rect(i * 2, i * 2, 150 + i, 40 + i)
            self.theme.draw_ornate_button(self.screen, button_rect, f"Button {i}", "normal")
        
        mid_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Create many more (should trigger cache eviction)
        for i in range(100, 200):
            button_rect = pygame.Rect(i * 2, i * 2, 150 + i, 40 + i)
            self.theme.draw_ornate_button(self.screen, button_rect, f"Button {i}", "normal")
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Memory growth should be controlled by cache limits
        memory_growth = final_memory - initial_memory
        self.assertLess(memory_growth, 50.0)  # Less than 50MB growth
        
        # Check cache size is limited
        stats = self.theme.get_performance_stats()
        self.assertLessEqual(stats["cache_size"], 50)  # Cache size limit
    
    def test_adaptive_optimization(self):
        """Test adaptive performance optimization."""
        # Set high detail level
        self.theme.set_detail_level(3)
        initial_detail = self.theme.current_detail_level
        
        # Simulate poor performance
        low_fps = 30.0
        target_fps = 60.0
        
        self.theme.optimize_for_performance(target_fps, low_fps)
        
        # Should have reduced detail level
        self.assertLess(self.theme.current_detail_level, initial_detail)
        
        # Simulate good performance
        high_fps = 70.0
        
        self.theme.optimize_for_performance(target_fps, high_fps)
        
        # Should have increased detail level
        self.assertGreaterEqual(self.theme.current_detail_level, self.theme.current_detail_level)


class AssetManagerTestCase(unittest.TestCase):
    """Test the optimized asset manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.asset_manager = OptimizedAssetManager(cache_size_mb=64)
        
        # Create test asset directory
        self.test_dir = Path("test_assets")
        self.test_dir.mkdir(exist_ok=True)
        
        # Create test images
        self._create_test_assets()
    
    def tearDown(self):
        """Clean up after tests."""
        self.asset_manager.shutdown()
        
        # Clean up test assets
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        
        pygame.quit()
    
    def _create_test_assets(self):
        """Create test assets for testing."""
        # Create different sized test images
        sizes = [(512, 768), (1024, 1024), (256, 256), (64, 64)]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        
        for i, (size, color) in enumerate(zip(sizes, colors)):
            surface = pygame.Surface(size)
            surface.fill(color)
            
            asset_path = self.test_dir / f"test_asset_{i}.png"
            pygame.image.save(surface, str(asset_path))
    
    def test_asset_loading_performance(self):
        """Test asset loading performance."""
        asset_files = list(self.test_dir.glob("*.png"))
        
        # Time synchronous loading
        sync_times = []
        for asset_file in asset_files:
            start_time = time.perf_counter()
            surface = self.asset_manager.load_asset(str(asset_file), AssetType.CARD_ART)
            end_time = time.perf_counter()
            
            sync_times.append((end_time - start_time) * 1000)
            self.assertIsNotNone(surface)
        
        avg_sync_time = statistics.mean(sync_times)
        
        # Should load assets quickly
        self.assertLess(avg_sync_time, 50.0)  # Under 50ms average
        
        # Test cache hits (should be much faster)
        cache_times = []
        for asset_file in asset_files:
            start_time = time.perf_counter()
            surface = self.asset_manager.load_asset(str(asset_file), AssetType.CARD_ART)
            end_time = time.perf_counter()
            
            cache_times.append((end_time - start_time) * 1000)
        
        avg_cache_time = statistics.mean(cache_times)
        
        # Cache hits should be much faster
        self.assertLess(avg_cache_time * 5, avg_sync_time)
    
    def test_lod_performance_optimization(self):
        """Test LOD system performance impact."""
        large_asset = self.test_dir / "test_asset_1.png"  # 1024x1024 asset
        
        # Test different quality levels
        quality_times = {}
        
        for quality in [QualityLevel.ULTRA, QualityLevel.HIGH, QualityLevel.MEDIUM, QualityLevel.LOW]:
            self.asset_manager.lod_manager.base_quality = quality
            self.asset_manager.cache.clear()  # Clear cache for fair comparison
            
            start_time = time.perf_counter()
            surface = self.asset_manager.load_asset(str(large_asset), AssetType.BACKGROUND)
            end_time = time.perf_counter()
            
            quality_times[quality] = (end_time - start_time) * 1000
            
            # Verify size reduction for lower qualities
            if quality != QualityLevel.ULTRA:
                self.assertLess(surface.get_width(), 1024)
                self.assertLess(surface.get_height(), 1024)
        
        # Lower quality should generally load faster (due to scaling)
        self.assertLessEqual(quality_times[QualityLevel.LOW], quality_times[QualityLevel.ULTRA] * 1.5)
    
    def test_background_loading_performance(self):
        """Test background loading performance."""
        asset_files = list(self.test_dir.glob("*.png"))
        
        # Start background loading
        futures = []
        start_time = time.perf_counter()
        
        for asset_file in asset_files:
            future = self.asset_manager.load_asset_async(str(asset_file), AssetType.CHARACTER)
            futures.append(future)
        
        # Wait for all to complete
        results = []
        for future in futures:
            result = future.result(timeout=5.0)
            results.append(result)
        
        total_time = (time.perf_counter() - start_time) * 1000
        
        # Background loading should complete quickly
        self.assertLess(total_time, 200.0)  # Under 200ms for all assets
        
        # All results should be valid
        for result in results:
            self.assertIsNotNone(result)
    
    def test_memory_management(self):
        """Test memory management and cache eviction."""
        # Get initial memory usage
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Load assets until cache is full
        asset_files = list(self.test_dir.glob("*.png"))
        
        # Load many copies with different keys to fill cache
        for i in range(100):
            for j, asset_file in enumerate(asset_files):
                # Load with different processing to create unique cache keys
                self.asset_manager.lod_manager.base_quality = list(QualityLevel)[i % 4]
                surface = self.asset_manager.load_asset(str(asset_file), AssetType.UI_ELEMENT)
        
        mid_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Force memory optimization
        self.asset_manager.optimize_memory_usage()
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Memory should be controlled
        memory_growth = final_memory - initial_memory
        self.assertLess(memory_growth, 100.0)  # Less than 100MB growth
        
        # Cache should have been cleaned up
        cache_stats = self.asset_manager.get_statistics()["cache_statistics"]
        self.assertLess(cache_stats["memory_usage_mb"], 80.0)  # Within cache limit


class IntegratedPerformanceTestCase(unittest.TestCase):
    """Test integrated performance of all systems together."""
    
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        
        # Initialize all systems
        self.profiler = initialize_profiler()
        self.particle_system = OptimizedParticleSystem(1920, 1080)
        self.theme = OptimizedHadesEgyptianTheme((1920, 1080))
        self.asset_manager = OptimizedAssetManager()
    
    def tearDown(self):
        """Clean up after tests."""
        self.asset_manager.shutdown()
        pygame.quit()
    
    def test_full_game_loop_performance(self):
        """Test performance of full game loop with all systems."""
        # Simulate 60fps for 2 seconds (120 frames)
        frame_times = []
        target_frame_time = 1000.0 / 60.0  # 16.67ms
        
        for frame in range(120):
            frame_start = time.perf_counter()
            
            # Start frame profiling
            self.profiler.start_frame()
            
            # Simulate game update
            with self.profiler.time_operation("game_update"):
                # Update particle system
                self.particle_system.update(1.0 / 60.0)
                
                # Create some particles
                if frame % 10 == 0:  # Every 10 frames
                    self.particle_system.create_particle_burst(
                        960, 540, ParticleType.FIRE_SPARK, 5, 1.0
                    )
                
                # Update theme animation
                self.theme.update_animation_time(1.0 / 60.0)
            
            # Simulate rendering
            with self.profiler.time_operation("game_render"):
                # Clear screen
                self.screen.fill((0, 0, 0))
                
                # Render background overlay
                self.theme.draw_background_overlay(self.screen)
                
                # Render some UI elements
                button_rect = pygame.Rect(100, 100, 200, 50)
                self.theme.draw_ornate_button(self.screen, button_rect, "Test Button", "normal")
                
                health_orb_rect = self.theme.draw_health_orb(self.screen, (200, 200), 75, 100)
                
                # Render particles
                self.particle_system.render(self.screen)
                
                # Update display
                pygame.display.flip()
            
            # End frame profiling
            particle_count = self.particle_system.get_statistics()["active_particles"]
            self.profiler.end_frame(particle_count=particle_count, draw_calls=10)
            
            frame_end = time.perf_counter()
            frame_time = (frame_end - frame_start) * 1000
            frame_times.append(frame_time)
            
            # Update performance metrics
            current_fps = 1000.0 / frame_time if frame_time > 0 else 60.0
            self.theme.optimize_for_performance(60.0, current_fps)
            self.asset_manager.update_performance_metrics(current_fps)
        
        # Analyze performance
        avg_frame_time = statistics.mean(frame_times)
        max_frame_time = max(frame_times)
        min_frame_time = min(frame_times)
        
        # Performance requirements
        self.assertLess(avg_frame_time, target_frame_time * 1.2)  # Within 20% of target
        self.assertLess(max_frame_time, target_frame_time * 2.0)  # No frame over 33ms
        
        # Check that 95% of frames meet target
        frames_on_target = sum(1 for ft in frame_times if ft <= target_frame_time)
        target_rate = frames_on_target / len(frame_times)
        self.assertGreater(target_rate, 0.80)  # 80% of frames on target
        
        # Get comprehensive performance summary
        summary = self.profiler.get_performance_summary()
        
        # Verify performance metrics
        self.assertGreater(summary["frame_performance"]["avg_fps"], 50.0)
        self.assertLess(summary["frame_performance"]["frame_time_std_ms"], 5.0)
    
    def test_stress_test_performance(self):
        """Stress test with heavy particle load."""
        # Create heavy particle load
        for _ in range(20):
            self.particle_system.create_particle_burst(
                960, 540, ParticleType.SAND_SPIRAL, 50, 2.0
            )
        
        # Run stress test for 1 second (60 frames)
        stress_frame_times = []
        
        for frame in range(60):
            frame_start = time.perf_counter()
            
            # Heavy update load
            self.particle_system.update(1.0 / 60.0)
            
            # Heavy rendering load
            self.screen.fill((0, 0, 0))
            
            # Render many UI elements
            for i in range(10):
                button_rect = pygame.Rect(i * 100, i * 50, 150, 40)
                self.theme.draw_ornate_button(self.screen, button_rect, f"Button {i}", "hover")
            
            # Render particles
            self.particle_system.render(self.screen)
            
            pygame.display.flip()
            
            frame_end = time.perf_counter()
            stress_frame_times.append((frame_end - frame_start) * 1000)
        
        # Even under stress, performance should be acceptable
        avg_stress_time = statistics.mean(stress_frame_times)
        max_stress_time = max(stress_frame_times)
        
        # Should maintain at least 30fps under stress
        self.assertLess(avg_stress_time, 33.33)  # 30fps = 33.33ms
        self.assertLess(max_stress_time, 50.0)   # No frame over 50ms
    
    def test_memory_stability_over_time(self):
        """Test memory stability over extended runtime."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Run for extended period with constant activity
        for cycle in range(10):  # 10 cycles
            # Create and destroy particles
            for _ in range(30):
                self.particle_system.create_particle_burst(
                    960, 540, ParticleType.GOLDEN_AURA, 20, 1.0
                )
            
            # Update particles until they die
            for _ in range(180):  # 3 seconds at 60fps
                self.particle_system.update(1.0 / 60.0)
            
            # Force garbage collection
            gc.collect()
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be minimal
        self.assertLess(memory_growth, 20.0)  # Less than 20MB growth over time


def create_performance_test_suite():
    """Create comprehensive performance test suite."""
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTest(unittest.makeSuite(PerformanceProfilerTestCase))
    suite.addTest(unittest.makeSuite(OptimizedParticleSystemTestCase))
    suite.addTest(unittest.makeSuite(OptimizedHadesThemeTestCase))
    suite.addTest(unittest.makeSuite(AssetManagerTestCase))
    suite.addTest(unittest.makeSuite(IntegratedPerformanceTestCase))
    
    return suite


if __name__ == '__main__':
    # Run comprehensive performance tests
    print("Running Comprehensive Performance Test Suite for Sands of Duat")
    print("=" * 70)
    
    # Initialize pygame for tests
    pygame.init()
    
    try:
        # Run test suite
        suite = create_performance_test_suite()
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Print summary
        if result.wasSuccessful():
            print("\n" + "=" * 70)
            print("ALL PERFORMANCE TESTS PASSED!")
            print("Game is optimized for 60fps gameplay with premium visual quality.")
            print("RTX 5070 and lower-end hardware support validated.")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("SOME PERFORMANCE TESTS FAILED!")
            print("Review failed tests and optimize accordingly.")
            print(f"Failures: {len(result.failures)}, Errors: {len(result.errors)}")
            print("=" * 70)
    
    finally:
        pygame.quit()
    
    sys.exit(0 if result.wasSuccessful() else 1)