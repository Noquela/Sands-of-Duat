#!/usr/bin/env python3
"""
Performance Validation Test for Sands of Duat
Testing frame rates and performance metrics to ensure 60fps target is achieved.
"""

import sys
import os
import time
import pygame
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_pygame_performance():
    """Test basic pygame rendering performance."""
    print("Testing pygame rendering performance...")
    
    try:
        pygame.init()
        
        # Create test display
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        
        # Performance metrics
        frame_times = []
        particle_count = 100
        
        # Create test particles
        particles = []
        for i in range(particle_count):
            particles.append({
                'x': i * 12,
                'y': 360,
                'vx': 2,
                'vy': 1,
                'color': (255, 215, 0)  # Gold
            })
        
        # Run performance test
        start_time = time.time()
        frame_count = 0
        max_frames = 300  # 5 seconds at 60fps
        
        running = True
        while running and frame_count < max_frames:
            dt = clock.tick(60) / 1000.0  # Target 60fps
            frame_start = time.time()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Clear screen
            screen.fill((40, 30, 20))  # Dark brown background
            
            # Update and render particles
            for particle in particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Wrap around screen
                if particle['x'] > 1280:
                    particle['x'] = 0
                if particle['y'] > 720:
                    particle['y'] = 0
                
                # Render particle
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 3)
            
            # Draw some test rectangles
            for i in range(50):
                rect = pygame.Rect(i * 25, 100 + i * 2, 20, 20)
                color = (194, 154, 108)  # Sandstone
                pygame.draw.rect(screen, color, rect)
            
            pygame.display.flip()
            
            frame_end = time.time()
            frame_time = frame_end - frame_start
            frame_times.append(frame_time)
            frame_count += 1
        
        pygame.quit()
        
        # Calculate performance metrics
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time
        avg_frame_time = sum(frame_times) / len(frame_times)
        min_frame_time = min(frame_times)
        max_frame_time = max(frame_times)
        
        print(f"Performance Results:")
        print(f"  Average FPS: {avg_fps:.1f}")
        print(f"  Average frame time: {avg_frame_time*1000:.2f}ms")
        print(f"  Min frame time: {min_frame_time*1000:.2f}ms")
        print(f"  Max frame time: {max_frame_time*1000:.2f}ms")
        print(f"  Particles rendered: {particle_count}")
        
        # Performance criteria
        target_fps = 60
        target_frame_time = 1.0 / target_fps  # 16.67ms
        
        performance_score = 0
        if avg_fps >= target_fps * 0.95:  # At least 95% of target
            performance_score += 25
            print("  PASS: Average FPS meets target")
        else:
            print(f"  FAIL: Average FPS ({avg_fps:.1f}) below target ({target_fps})")
        
        if avg_frame_time <= target_frame_time * 1.1:  # Within 110% of target
            performance_score += 25
            print("  PASS: Average frame time acceptable")
        else:
            print(f"  FAIL: Average frame time too high")
        
        if max_frame_time <= target_frame_time * 2:  # No frame takes more than 2x target
            performance_score += 25
            print("  PASS: No major frame drops")
        else:
            print(f"  FAIL: Some frames took too long ({max_frame_time*1000:.2f}ms)")
        
        if len([t for t in frame_times if t > target_frame_time * 1.5]) <= len(frame_times) * 0.05:
            performance_score += 25
            print("  PASS: Less than 5% of frames dropped")
        else:
            print("  FAIL: Too many dropped frames")
        
        print(f"  Overall Performance Score: {performance_score}/100")
        
        return performance_score >= 75
        
    except Exception as e:
        print(f"FAIL pygame performance test error: {e}")
        return False

def test_theme_rendering_performance():
    """Test theme system rendering performance."""
    print("Testing theme rendering performance...")
    
    try:
        from sands_duat.ui.theme import initialize_theme
        from sands_duat.ui.hades_theme import HadesEgyptianTheme
        
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        
        theme = initialize_theme(1280, 720)
        hades_theme = HadesEgyptianTheme((1280, 720))
        
        # Performance test
        start_time = time.time()
        iterations = 100
        
        for i in range(iterations):
            # Test button rendering
            button_rect = pygame.Rect(100 + i, 100, 200, 50)
            hades_theme.draw_ornate_button(screen, button_rect, f"Button {i}", 'normal')
            
            # Test text rendering
            text_pos = (200, 200 + i)
            hades_theme.draw_title_text(screen, "Performance Test", text_pos, 'body')
        
        end_time = time.time()
        total_time = end_time - start_time
        
        pygame.quit()
        
        operations_per_second = iterations / total_time
        
        print(f"Theme Rendering Results:")
        print(f"  Operations: {iterations}")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Operations per second: {operations_per_second:.1f}")
        
        # Should be able to render at least 1000 operations per second
        if operations_per_second >= 1000:
            print("  PASS: Theme rendering performance acceptable")
            return True
        else:
            print("  FAIL: Theme rendering too slow")
            return False
            
    except Exception as e:
        print(f"FAIL theme rendering test error: {e}")
        return False

def test_card_system_performance():
    """Test card system performance."""
    print("Testing card system performance...")
    
    try:
        from sands_duat.content.starter_cards import create_starter_cards
        from sands_duat.core.hourglass import HourGlass
        
        # Performance test: card creation and manipulation
        start_time = time.time()
        iterations = 1000
        
        for i in range(iterations):
            cards = create_starter_cards()
            hourglass = HourGlass()
            hourglass.set_sand(5)
            hourglass.spend_sand(2)
            hourglass.update_sand()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        operations_per_second = iterations / total_time
        
        print(f"Card System Performance Results:")
        print(f"  Operations: {iterations}")
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Operations per second: {operations_per_second:.1f}")
        
        # Should be able to perform at least 500 operations per second
        if operations_per_second >= 500:
            print("  PASS: Card system performance acceptable")
            return True
        else:
            print("  FAIL: Card system too slow")
            return False
            
    except Exception as e:
        print(f"FAIL card system test error: {e}")
        return False

def test_memory_usage():
    """Test memory usage during operations."""
    print("Testing memory usage...")
    
    try:
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Memory stress test
        objects = []
        for i in range(1000):
            # Create various game objects
            from sands_duat.core.hourglass import HourGlass
            hourglass = HourGlass()
            objects.append(hourglass)
            
            if i % 100 == 0:
                # Check memory periodically
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                if memory_increase > 100:  # More than 100MB increase
                    print(f"  WARNING: High memory usage at iteration {i}: {memory_increase:.1f}MB")
        
        peak_memory = process.memory_info().rss / 1024 / 1024
        
        # Clear objects and force garbage collection
        objects.clear()
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        total_increase = peak_memory - initial_memory
        cleanup_reduction = peak_memory - final_memory
        
        print(f"Memory Usage Results:")
        print(f"  Initial memory: {initial_memory:.1f}MB")
        print(f"  Peak memory: {peak_memory:.1f}MB")
        print(f"  Final memory: {final_memory:.1f}MB")
        print(f"  Total increase: {total_increase:.1f}MB")
        print(f"  Cleanup reduction: {cleanup_reduction:.1f}MB")
        
        # Memory criteria
        if total_increase < 50:  # Less than 50MB increase is good
            print("  PASS: Memory usage acceptable")
            return True
        elif cleanup_reduction > total_increase * 0.8:  # Good cleanup
            print("  PASS: Good memory cleanup")
            return True
        else:
            print("  FAIL: High memory usage or poor cleanup")
            return False
            
    except Exception as e:
        print(f"FAIL memory test error: {e}")
        return False

def main():
    """Run all performance validation tests."""
    print("=" * 70)
    print("SANDS OF DUAT - PERFORMANCE VALIDATION TEST")
    print("Validating 60fps target and performance requirements")
    print("=" * 70)
    
    tests = [
        test_pygame_performance,
        test_theme_rendering_performance,
        test_card_system_performance,
        test_memory_usage
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("  RESULT: PASS")
            else:
                print("  RESULT: FAIL")
        except Exception as e:
            print(f"  RESULT: CRASH - {e}")
        print()
    
    print("=" * 70)
    print(f"PERFORMANCE RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("SUCCESS All performance tests PASSED!")
        print("The game meets the 60fps target and performance requirements.")
    elif passed >= total * 0.75:
        print("WARNING Most performance tests passed - minor optimizations needed")
    elif passed >= total * 0.5:
        print("WARNING Some performance issues detected - optimization required")
    else:
        print("ERROR Significant performance issues - major optimization needed")
    
    print("=" * 70)
    return passed >= total * 0.75  # 75% pass rate for performance

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)