#!/usr/bin/env python3
"""
High-Performance Asset Integration Test Suite

Comprehensive performance testing and benchmarking for the premium asset integration
system with validation of 60fps targets and smooth gameplay performance.
"""

import unittest
import time
import threading
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import statistics
import json
import logging

import pygame
import psutil

# Import the high-performance systems
import sys
sys.path.append(str(Path(__file__).parent.parent))

from sands_duat.graphics.high_performance_asset_system import (
    HighPerformanceAssetSystem, PerformanceMode, initialize_hp_asset_system
)
from sands_duat.graphics.optimized_parallax_renderer import (
    OptimizedParallaxRenderer, RenderTechnique, benchmark_parallax_performance
)
from sands_duat.graphics.adaptive_performance_manager import (
    AdaptivePerformanceManager, QualityPreset, initialize_performance_system
)
from sands_duat.graphics.advanced_memory_system import (
    AdvancedMemoryManager, GCStrategy, MemoryPriority, MemoryTier, initialize_memory_system
)
from sands_duat.graphics.parallax_system import ParallaxSystem


class PerformanceBenchmark:
    """Performance benchmarking utilities"""
    
    def __init__(self, name: str):
        self.name = name
        self.measurements: List[float] = []
        self.start_time = 0.0
        
    def start(self):
        """Start timing measurement"""
        self.start_time = time.perf_counter()
    
    def stop(self) -> float:
        """Stop timing and record measurement"""
        elapsed = time.perf_counter() - self.start_time
        self.measurements.append(elapsed)
        return elapsed
    
    def get_stats(self) -> Dict[str, float]:
        """Get statistical summary"""
        if not self.measurements:
            return {'count': 0, 'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
        
        return {
            'count': len(self.measurements),
            'avg': statistics.mean(self.measurements),
            'min': min(self.measurements),
            'max': max(self.measurements),
            'std': statistics.stdev(self.measurements) if len(self.measurements) > 1 else 0.0
        }


class PerformanceTestCase(unittest.TestCase):
    """Base class for performance tests"""
    
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        
        self.logger = logging.getLogger(__name__)
        self.performance_reports: List[Dict[str, Any]] = []
        
        # Target performance metrics
        self.target_fps = 60.0
        self.min_acceptable_fps = 30.0
        self.target_frame_time_ms = 16.67
        self.max_memory_mb = 1024
    
    def tearDown(self):
        """Clean up after test"""
        pygame.quit()
        
        # Save performance reports
        if self.performance_reports:
            report_file = Path("performance_test_results.json")
            with open(report_file, 'w') as f:
                json.dump(self.performance_reports, f, indent=2)
    
    def measure_fps(self, test_function, duration_seconds: float = 5.0) -> Dict[str, float]:
        """Measure FPS for a test function"""
        frame_times = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            frame_start = time.perf_counter()
            test_function()
            frame_end = time.perf_counter()
            
            frame_time = frame_end - frame_start
            frame_times.append(frame_time)
        
        # Calculate FPS statistics
        if not frame_times:
            return {'fps': 0.0, 'avg_frame_time_ms': 0.0, 'min_fps': 0.0, 'max_fps': 0.0}
        
        avg_frame_time = statistics.mean(frame_times)
        min_frame_time = min(frame_times)
        max_frame_time = max(frame_times)
        
        return {
            'fps': 1.0 / avg_frame_time,
            'avg_frame_time_ms': avg_frame_time * 1000,
            'min_fps': 1.0 / max_frame_time,
            'max_fps': 1.0 / min_frame_time,
            'frame_count': len(frame_times),
            'std_dev_ms': statistics.stdev(frame_times) * 1000 if len(frame_times) > 1 else 0.0
        }


class AssetSystemPerformanceTest(PerformanceTestCase):
    """Test high-performance asset system"""
    
    def test_asset_loading_performance(self):
        """Test asset loading performance under different conditions"""
        system = HighPerformanceAssetSystem(max_memory_mb=512, target_fps=60.0)
        
        # Create test assets
        test_assets = []
        for i in range(100):
            surface = pygame.Surface((512, 512))
            surface.fill((i % 255, (i * 2) % 255, (i * 3) % 255))
            test_assets.append((f"test_asset_{i}", surface))
        
        # Benchmark loading performance
        benchmark = PerformanceBenchmark("asset_loading")
        
        for asset_id, surface in test_assets:
            benchmark.start()
            # Simulate asset registration and optimization
            system.memory_manager.register_asset(asset_id, surface, {
                'asset_id': asset_id,
                'file_path': Path(f"{asset_id}.png"),
                'size_bytes': surface.get_width() * surface.get_height() * 4,
                'memory_tier': MemoryTier.MEDIUM,
                'last_accessed': time.time(),
                'access_count': 1,
                'load_time_ms': 10.0
            })
            benchmark.stop()
        
        stats = benchmark.get_stats()
        
        # Performance requirements
        self.assertLess(stats['avg'], 0.001, "Asset loading should average under 1ms")
        self.assertLess(stats['max'], 0.01, "No single asset should take over 10ms")
        
        # Test memory optimization
        memory_before = system.memory_manager.get_memory_usage()
        system.force_memory_optimization()
        memory_after = system.memory_manager.get_memory_usage()
        
        self.assertLessEqual(memory_after, memory_before, "Memory optimization should reduce usage")
        
        # Save performance report
        self.performance_reports.append({
            'test': 'asset_loading_performance',
            'stats': stats,
            'memory_before_mb': memory_before,
            'memory_after_mb': memory_after,
            'assets_tested': len(test_assets)
        })
    
    def test_texture_compression_performance(self):
        """Test texture compression performance across quality modes"""
        system = HighPerformanceAssetSystem()
        
        # Create test textures of various sizes
        test_textures = [
            pygame.Surface((256, 256)),
            pygame.Surface((512, 512)),
            pygame.Surface((1024, 1024)),
            pygame.Surface((2048, 2048))
        ]
        
        compression_results = {}
        
        for mode in PerformanceMode:
            if mode == PerformanceMode.AUTO:
                continue
                
            benchmark = PerformanceBenchmark(f"compression_{mode.value}")
            
            for i, texture in enumerate(test_textures):
                benchmark.start()
                compressed = system.texture_compressor.compress_surface(texture, mode)
                benchmark.stop()
                
                # Verify compression worked
                if mode != PerformanceMode.ULTRA:
                    orig_size = texture.get_width() * texture.get_height()
                    comp_size = compressed.get_width() * compressed.get_height()
                    self.assertLess(comp_size, orig_size, f"Texture should be compressed in {mode.value} mode")
            
            compression_results[mode.value] = benchmark.get_stats()
        
        # Performance requirements
        for mode, stats in compression_results.items():
            self.assertLess(stats['avg'], 0.05, f"Compression in {mode} mode should average under 50ms")
        
        self.performance_reports.append({
            'test': 'texture_compression_performance',
            'results': compression_results
        })
    
    def test_memory_management_under_pressure(self):
        """Test memory management under high memory pressure"""
        system = AdvancedMemoryManager(max_memory_mb=128)  # Low limit for testing
        system.start_monitoring()
        
        try:
            # Create objects to fill memory
            objects = []
            for i in range(200):
                surface = pygame.Surface((256, 256))
                object_id = f"pressure_test_{i}"
                
                # Register with different priorities and tiers
                priority = MemoryPriority.LOW if i % 3 == 0 else MemoryPriority.MEDIUM
                tier = MemoryTier.TRANSIENT if i % 2 == 0 else MemoryTier.SCREEN
                
                system.register_object(surface, object_id, "test_surface", priority, tier)
                objects.append(surface)
                
                # Simulate some usage
                if i % 10 == 0:
                    system.access_object(object_id)
            
            # Force memory pressure
            initial_count = system.tracker.stats.allocation_count
            cleanup_result = system.cleanup_memory(force=True)
            final_count = system.tracker.stats.allocation_count
            
            # Verify cleanup worked
            self.assertGreater(cleanup_result['objects_freed'], 0, "Should have freed some objects")
            self.assertLess(final_count, initial_count, "Object count should decrease")
            
            # Test garbage collection performance
            gc_benchmark = PerformanceBenchmark("gc_performance")
            for _ in range(10):
                gc_benchmark.start()
                gc_result = system.force_garbage_collection()
                gc_benchmark.stop()
            
            gc_stats = gc_benchmark.get_stats()
            self.assertLess(gc_stats['avg'], 0.01, "GC should average under 10ms")
            
            self.performance_reports.append({
                'test': 'memory_management_under_pressure',
                'initial_objects': initial_count,
                'final_objects': final_count,
                'cleanup_result': cleanup_result,
                'gc_stats': gc_stats
            })
            
        finally:
            system.shutdown()
    
    def test_adaptive_quality_scaling(self):
        """Test adaptive quality scaling performance"""
        manager = AdaptivePerformanceManager(target_fps=60.0)
        manager.initialize(auto_detect=False)
        
        try:
            # Test quality transitions
            transition_times = []
            
            presets = [QualityPreset.LOW, QualityPreset.MEDIUM, 
                      QualityPreset.HIGH, QualityPreset.ULTRA]
            
            for preset in presets:
                start_time = time.perf_counter()
                manager.set_quality_preset(preset)
                end_time = time.perf_counter()
                
                transition_time = end_time - start_time
                transition_times.append(transition_time)
                
                # Verify settings applied
                settings = manager.get_current_quality_settings()
                self.assertIsNotNone(settings)
            
            # Performance requirements
            avg_transition_time = statistics.mean(transition_times)
            max_transition_time = max(transition_times)
            
            self.assertLess(avg_transition_time, 0.001, "Quality transitions should average under 1ms")
            self.assertLess(max_transition_time, 0.005, "No transition should take over 5ms")
            
            # Test adaptive behavior
            manager.set_adaptive_mode(True)
            
            # Simulate poor performance
            from sands_duat.graphics.adaptive_performance_manager import PerformanceMetrics
            poor_metrics = PerformanceMetrics()
            poor_metrics.update(25.0, 40.0)  # 25 FPS, 40ms frame time
            poor_metrics.fps_history.extend([25.0] * 60)  # Consistently poor
            
            quality_changed = manager.quality_controller.update_quality(poor_metrics)
            self.assertTrue(quality_changed, "Should reduce quality with poor performance")
            
            self.performance_reports.append({
                'test': 'adaptive_quality_scaling',
                'transition_times': transition_times,
                'avg_transition_ms': avg_transition_time * 1000,
                'max_transition_ms': max_transition_time * 1000,
                'adaptive_response': quality_changed
            })
            
        finally:
            manager.shutdown()


class ParallaxRenderingPerformanceTest(PerformanceTestCase):
    """Test optimized parallax rendering performance"""
    
    def test_parallax_rendering_techniques(self):
        """Test different parallax rendering techniques"""
        # Create test parallax system
        parallax = ParallaxSystem(1920, 1080)
        
        # Add test layers (using placeholder surfaces)
        for i in range(5):
            layer_surface = pygame.Surface((1920, 1080))
            layer_surface.fill((50 * i, 100, 150))
            
            # Create temporary file for layer
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pygame.image.save(layer_surface, temp_file.name)
                
                parallax.add_layer(
                    temp_file.name,
                    scroll_speed=0.2 + (i * 0.2),
                    alpha=200,
                    auto_scroll_x=-5.0 * (i + 1)
                )
        
        # Test different rendering techniques
        techniques = [RenderTechnique.BASIC, RenderTechnique.BATCHED,
                     RenderTechnique.CULLED, RenderTechnique.OPTIMIZED]
        
        results = {}
        test_surface = pygame.Surface((1920, 1080))
        
        for technique in techniques:
            renderer = OptimizedParallaxRenderer(1920, 1080, technique)
            renderer.register_parallax_system(parallax)
            
            # Benchmark rendering
            fps_result = self.measure_fps(
                lambda: renderer.render_parallax_system(test_surface, parallax),
                duration_seconds=3.0
            )
            
            results[technique.value] = {
                'fps': fps_result,
                'renderer_stats': renderer.get_performance_stats()
            }
            
            # Performance requirements
            self.assertGreater(fps_result['fps'], self.min_acceptable_fps,
                             f"{technique.value} should achieve minimum FPS")
            
            renderer.shutdown()
        
        # Verify optimization effectiveness
        basic_fps = results[RenderTechnique.BASIC.value]['fps']['fps']
        optimized_fps = results[RenderTechnique.OPTIMIZED.value]['fps']['fps']
        
        self.assertGreaterEqual(optimized_fps, basic_fps,
                               "Optimized technique should not be slower than basic")
        
        self.performance_reports.append({
            'test': 'parallax_rendering_techniques',
            'results': results,
            'optimization_improvement': (optimized_fps - basic_fps) / basic_fps * 100
        })
    
    def test_layer_culling_performance(self):
        """Test layer culling performance with many layers"""
        renderer = OptimizedParallaxRenderer(1920, 1080, RenderTechnique.CULLED)
        parallax = ParallaxSystem(1920, 1080)
        
        # Create many layers to stress test culling
        layer_count = 20
        for i in range(layer_count):
            layer_surface = pygame.Surface((512, 512))
            layer_surface.fill((i * 10 % 255, (i * 20) % 255, (i * 30) % 255))
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pygame.image.save(layer_surface, temp_file.name)
                
                parallax.add_layer(
                    temp_file.name,
                    scroll_speed=0.1 + (i * 0.05),
                    alpha=150
                )
        
        renderer.register_parallax_system(parallax)
        
        # Test culling with different camera positions
        test_surface = pygame.Surface((1920, 1080))
        culling_results = []
        
        camera_positions = [(0, 0), (1000, 0), (2000, 0), (5000, 0)]
        
        for camera_x, camera_y in camera_positions:
            renderer.update_camera(camera_x, camera_y)
            
            # Measure rendering performance
            start_time = time.perf_counter()
            render_result = renderer.render_parallax_system(test_surface, parallax)
            end_time = time.perf_counter()
            
            render_time_ms = (end_time - start_time) * 1000
            
            culling_results.append({
                'camera_position': (camera_x, camera_y),
                'render_time_ms': render_time_ms,
                'rendered_layers': render_result['rendered_layers'],
                'culled_layers': render_result['culled_layers'],
                'total_operations': render_result['total_operations']
            })
            
            # Performance requirement
            self.assertLess(render_time_ms, self.target_frame_time_ms,
                           f"Rendering should complete within frame budget at {camera_x}, {camera_y}")
        
        # Verify culling is working
        total_culled = sum(result['culled_layers'] for result in culling_results)
        self.assertGreater(total_culled, 0, "Culling should eliminate some layers")
        
        self.performance_reports.append({
            'test': 'layer_culling_performance',
            'layer_count': layer_count,
            'culling_results': culling_results,
            'total_culled': total_culled
        })
        
        renderer.shutdown()
    
    def test_memory_usage_during_rendering(self):
        """Test memory usage during intensive rendering"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        renderer = OptimizedParallaxRenderer(1920, 1080, RenderTechnique.OPTIMIZED)
        parallax = ParallaxSystem(1920, 1080)
        
        # Create memory-intensive layers
        for i in range(10):
            large_surface = pygame.Surface((1024, 1024))
            large_surface.fill((i * 25, 128, 255 - i * 25))
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pygame.image.save(large_surface, temp_file.name)
                
                parallax.add_layer(
                    temp_file.name,
                    scroll_speed=0.3 + (i * 0.1),
                    alpha=200
                )
        
        renderer.register_parallax_system(parallax)
        test_surface = pygame.Surface((1920, 1080))
        
        # Render continuously and monitor memory
        memory_samples = []
        frame_count = 300  # 5 seconds at 60fps
        
        for frame in range(frame_count):
            # Simulate camera movement
            camera_x = frame * 2
            renderer.update_camera(camera_x, 0)
            
            # Render frame
            renderer.render_parallax_system(test_surface, parallax)
            
            # Sample memory every 30 frames
            if frame % 30 == 0:
                current_memory = process.memory_info().rss / (1024 * 1024)
                memory_samples.append(current_memory)
        
        final_memory = process.memory_info().rss / (1024 * 1024)
        max_memory = max(memory_samples)
        memory_growth = final_memory - initial_memory
        
        # Performance requirements
        self.assertLess(memory_growth, 200, "Memory growth should be under 200MB")
        self.assertLess(max_memory, self.max_memory_mb, f"Peak memory should not exceed {self.max_memory_mb}MB")
        
        self.performance_reports.append({
            'test': 'memory_usage_during_rendering',
            'initial_memory_mb': initial_memory,
            'final_memory_mb': final_memory,
            'max_memory_mb': max_memory,
            'memory_growth_mb': memory_growth,
            'memory_samples': memory_samples,
            'frames_rendered': frame_count
        })
        
        renderer.shutdown()


class IntegrationPerformanceTest(PerformanceTestCase):
    """Test integrated system performance"""
    
    def test_full_system_integration(self):
        """Test complete system integration under load"""
        # Initialize all systems
        hp_system = initialize_hp_asset_system(max_memory_mb=512, target_fps=60.0)
        perf_manager = initialize_performance_system(target_fps=60.0, auto_detect=False)
        memory_manager = initialize_memory_system(max_memory_mb=512)
        
        try:
            # Create complex test scenario
            test_surface = pygame.Surface((1920, 1080))
            
            # Setup parallax system
            parallax = hp_system.setup_parallax_for_screen("combat", "game_assets")
            
            # Load many assets
            asset_loading_times = []
            for i in range(50):
                start_time = time.perf_counter()
                
                # Create and load test asset
                surface = pygame.Surface((512, 512))
                surface.fill((i * 5 % 255, (i * 10) % 255, (i * 15) % 255))
                
                asset_id = f"integration_test_{i}"
                from sands_duat.graphics.asset_manager import AssetType
                optimized_asset = hp_system.load_asset_optimized(
                    asset_id, AssetType.CARD_ART, PerformanceMode.HIGH
                )
                
                end_time = time.perf_counter()
                asset_loading_times.append(end_time - start_time)
            
            # Simulate intensive gameplay loop
            gameplay_stats = self.measure_fps(
                lambda: self._simulate_gameplay_frame(hp_system, perf_manager, test_surface),
                duration_seconds=10.0
            )
            
            # Get system statistics
            hp_stats = hp_system.get_performance_stats()
            perf_stats = perf_manager.get_status_summary()
            memory_stats = memory_manager.get_memory_report()
            
            # Performance requirements
            self.assertGreater(gameplay_stats['fps'], self.min_acceptable_fps,
                             "Integrated system should maintain minimum FPS")
            self.assertLess(gameplay_stats['avg_frame_time_ms'], self.target_frame_time_ms * 1.5,
                           "Frame time should be reasonable")
            
            # Memory requirements
            self.assertLess(memory_stats['system']['total_allocated_mb'], self.max_memory_mb,
                           "Memory usage should stay within limits")
            
            self.performance_reports.append({
                'test': 'full_system_integration',
                'gameplay_stats': gameplay_stats,
                'asset_loading_times': {
                    'avg_ms': statistics.mean(asset_loading_times) * 1000,
                    'max_ms': max(asset_loading_times) * 1000,
                    'count': len(asset_loading_times)
                },
                'hp_system_stats': hp_stats,
                'performance_manager_stats': perf_stats,
                'memory_stats': memory_stats
            })
            
        finally:
            # Cleanup
            hp_system.shutdown()
            perf_manager.shutdown()
            memory_manager.shutdown()
    
    def _simulate_gameplay_frame(self, hp_system, perf_manager, surface):
        """Simulate a typical gameplay frame"""
        # Update systems
        dt = 1.0 / 60.0  # 60 FPS target
        hp_system.update(dt)
        perf_manager.update(dt)
        
        # Simulate rendering
        surface.fill((0, 0, 0))
        
        # Simulate asset access
        import random
        if random.random() < 0.1:  # 10% chance to access asset
            asset_id = f"integration_test_{random.randint(0, 49)}"
            from sands_duat.graphics.asset_manager import AssetType
            hp_system.load_asset_optimized(asset_id, AssetType.CARD_ART)
        
        # Simulate screen transitions
        if random.random() < 0.01:  # 1% chance to preload for transition
            hp_system.preload_for_screen_transition("deck_builder")
    
    def test_stress_conditions(self):
        """Test system performance under stress conditions"""
        # Initialize systems with reduced limits for stress testing
        hp_system = initialize_hp_asset_system(max_memory_mb=256, target_fps=60.0)
        memory_manager = initialize_memory_system(max_memory_mb=256, gc_strategy=GCStrategy.AGGRESSIVE)
        
        try:
            stress_results = {}
            
            # Test 1: High asset churn
            stress_results['asset_churn'] = self._test_asset_churn(hp_system)
            
            # Test 2: Memory pressure
            stress_results['memory_pressure'] = self._test_memory_pressure(memory_manager)
            
            # Test 3: Rapid quality changes
            stress_results['quality_changes'] = self._test_rapid_quality_changes(hp_system)
            
            self.performance_reports.append({
                'test': 'stress_conditions',
                'results': stress_results
            })
            
        finally:
            hp_system.shutdown()
            memory_manager.shutdown()
    
    def _test_asset_churn(self, hp_system) -> Dict[str, Any]:
        """Test rapid asset loading/unloading"""
        start_time = time.time()
        iterations = 100
        
        for i in range(iterations):
            # Load asset
            surface = pygame.Surface((256, 256))
            asset_id = f"churn_test_{i}"
            
            from sands_duat.graphics.asset_manager import AssetType
            hp_system.load_asset_optimized(asset_id, AssetType.CARD_ART)
            
            # Force memory optimization periodically
            if i % 20 == 0:
                hp_system.force_memory_optimization()
        
        total_time = time.time() - start_time
        return {
            'iterations': iterations,
            'total_time_s': total_time,
            'avg_time_per_iteration_ms': (total_time / iterations) * 1000
        }
    
    def _test_memory_pressure(self, memory_manager) -> Dict[str, Any]:
        """Test system behavior under memory pressure"""
        # Fill memory with objects
        objects = []
        initial_memory = memory_manager.tracker.stats.game_allocated_mb
        
        for i in range(200):
            surface = pygame.Surface((512, 512))
            object_id = f"pressure_{i}"
            memory_manager.register_object(
                surface, object_id, "pressure_test",
                MemoryPriority.LOW, MemoryTier.TRANSIENT
            )
            objects.append(surface)
        
        peak_memory = memory_manager.tracker.stats.game_allocated_mb
        
        # Force cleanup
        cleanup_result = memory_manager.cleanup_memory(force=True)
        final_memory = memory_manager.tracker.stats.game_allocated_mb
        
        return {
            'initial_memory_mb': initial_memory,
            'peak_memory_mb': peak_memory,
            'final_memory_mb': final_memory,
            'cleanup_result': cleanup_result,
            'memory_freed_mb': peak_memory - final_memory
        }
    
    def _test_rapid_quality_changes(self, hp_system) -> Dict[str, Any]:
        """Test rapid quality setting changes"""
        modes = list(PerformanceMode)
        modes.remove(PerformanceMode.AUTO)  # Skip auto mode
        
        change_times = []
        
        for _ in range(50):  # 50 rapid changes
            mode = modes[_ % len(modes)]
            
            start_time = time.perf_counter()
            hp_system.set_quality_mode(mode)
            end_time = time.perf_counter()
            
            change_times.append(end_time - start_time)
        
        return {
            'change_count': len(change_times),
            'avg_change_time_ms': statistics.mean(change_times) * 1000,
            'max_change_time_ms': max(change_times) * 1000,
            'total_time_ms': sum(change_times) * 1000
        }


class PerformanceTestSuite:
    """Complete performance test suite runner"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        self.logger.info("Starting comprehensive performance test suite")
        
        # Run test suites
        test_suites = [
            AssetSystemPerformanceTest,
            ParallaxRenderingPerformanceTest,
            IntegrationPerformanceTest
        ]
        
        for suite_class in test_suites:
            suite_name = suite_class.__name__
            self.logger.info(f"Running {suite_name}")
            
            suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
            runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
            result = runner.run(suite)
            
            self.results[suite_name] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success_rate': (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
            }
        
        # Generate summary report
        summary = self._generate_summary()
        
        self.logger.info("Performance test suite completed")
        return summary
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = sum(r['tests_run'] for r in self.results.values())
        total_failures = sum(r['failures'] for r in self.results.values())
        total_errors = sum(r['errors'] for r in self.results.values())
        
        overall_success_rate = (total_tests - total_failures - total_errors) / total_tests * 100
        
        return {
            'timestamp': time.time(),
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'overall_success_rate': overall_success_rate,
            'suite_results': self.results,
            'system_info': {
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': psutil.virtual_memory().total / (1024**3),
                'python_version': sys.version,
                'pygame_version': pygame.version.ver
            }
        }


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run performance test suite
    suite = PerformanceTestSuite()
    results = suite.run_all_tests()
    
    # Save results
    results_file = Path("comprehensive_performance_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nPerformance Test Summary:")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Success Rate: {results['overall_success_rate']:.1f}%")
    print(f"Results saved to: {results_file}")
    
    if results['overall_success_rate'] >= 95:
        print("✅ EXCELLENT: All performance targets met!")
    elif results['overall_success_rate'] >= 85:
        print("✅ GOOD: Most performance targets met")
    elif results['overall_success_rate'] >= 70:
        print("⚠️  FAIR: Some performance issues detected")
    else:
        print("❌ POOR: Significant performance issues found")