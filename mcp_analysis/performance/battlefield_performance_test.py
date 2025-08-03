#!/usr/bin/env python3
"""
Battlefield Performance Analysis
Tests the performance impact of atmospheric elements.
"""

import sys
import pygame
import time
import statistics
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

from core.engine import GameEngine
from ui.ui_manager import UIManager
from ui.theme import initialize_theme
from content.starter_cards import create_starter_cards
from audio.audio_manager import initialize_audio_manager

def run_performance_test(enable_atmospheric_elements: bool = True, test_duration: int = 10) -> dict:
    """Run performance test with or without atmospheric elements."""
    try:
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Create display
        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption(f"Performance Test - Atmospheric: {enable_atmospheric_elements}")
        
        # Initialize game systems
        engine = GameEngine()
        engine.initialize()
        
        theme = initialize_theme(1920, 1080)
        create_starter_cards()
        audio_manager = initialize_audio_manager()
        
        # Set up UI manager
        ui_manager = UIManager(screen)
        
        # Import and add screens
        from ui.ui_manager import get_combat_screen
        combat_screen = get_combat_screen()()
        
        # Temporarily disable atmospheric elements if needed
        if not enable_atmospheric_elements:
            original_method = combat_screen._draw_battlefield_elements
            combat_screen._draw_battlefield_elements = lambda surface: None
        
        ui_manager.add_screen(combat_screen)
        ui_manager.switch_to_screen("combat")
        
        # Performance monitoring
        frame_times = []
        clock = pygame.time.Clock()
        
        # Let the screen initialize
        for _ in range(30):
            delta_time = 1/60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"error": "Test interrupted"}
                ui_manager.handle_event(event)
            
            engine.update(delta_time)
            ui_manager.update(delta_time)
            ui_manager.render()
            pygame.display.flip()
            clock.tick(60)
        
        # Run performance test
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < test_duration:
            frame_start = time.time()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                ui_manager.handle_event(event)
            
            # Update and render
            delta_time = clock.tick(60) / 1000.0
            engine.update(delta_time)
            ui_manager.update(delta_time)
            ui_manager.render()
            pygame.display.flip()
            
            frame_end = time.time()
            frame_times.append(frame_end - frame_start)
            frame_count += 1
        
        # Calculate statistics
        if frame_times:
            avg_frame_time = statistics.mean(frame_times)
            avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            min_fps = 1.0 / max(frame_times) if frame_times else 0
            max_fps = 1.0 / min(frame_times) if frame_times else 0
            
            percentile_95 = statistics.quantiles(frame_times, n=20)[18]  # 95th percentile
            fps_95th = 1.0 / percentile_95 if percentile_95 > 0 else 0
            
            return {
                "atmospheric_elements": enable_atmospheric_elements,
                "test_duration": test_duration,
                "frame_count": frame_count,
                "avg_fps": avg_fps,
                "min_fps": min_fps,
                "max_fps": max_fps,
                "fps_95th_percentile": fps_95th,
                "avg_frame_time_ms": avg_frame_time * 1000,
                "frame_time_std_ms": statistics.stdev(frame_times) * 1000 if len(frame_times) > 1 else 0
            }
        else:
            return {"error": "No frame data collected"}
        
    except Exception as e:
        return {"error": f"Test failed: {e}"}
        
    finally:
        try:
            pygame.quit()
        except:
            pass

def main():
    """Run comprehensive performance analysis."""
    print("Running Battlefield Atmospheric Elements Performance Analysis...")
    
    # Test with atmospheric elements
    print("Testing WITH atmospheric elements...")
    results_with = run_performance_test(enable_atmospheric_elements=True, test_duration=15)
    
    # Small break between tests
    time.sleep(2)
    
    # Test without atmospheric elements  
    print("Testing WITHOUT atmospheric elements...")
    results_without = run_performance_test(enable_atmospheric_elements=False, test_duration=15)
    
    # Calculate performance impact
    if "error" not in results_with and "error" not in results_without:
        fps_impact = results_without["avg_fps"] - results_with["avg_fps"]
        fps_impact_percent = (fps_impact / results_without["avg_fps"]) * 100 if results_without["avg_fps"] > 0 else 0
        
        frame_time_impact = results_with["avg_frame_time_ms"] - results_without["avg_frame_time_ms"]
        
        analysis = {
            "with_atmospheric": results_with,
            "without_atmospheric": results_without,
            "performance_impact": {
                "fps_reduction": fps_impact,
                "fps_reduction_percent": fps_impact_percent,
                "frame_time_increase_ms": frame_time_impact,
                "performance_category": "negligible" if abs(fps_impact_percent) < 5 else 
                                      "minor" if abs(fps_impact_percent) < 10 else
                                      "moderate" if abs(fps_impact_percent) < 20 else "significant"
            }
        }
    else:
        analysis = {
            "with_atmospheric": results_with,
            "without_atmospheric": results_without,
            "error": "Could not complete performance comparison"
        }
    
    # Save results
    timestamp = int(time.time())
    results_path = Path(__file__).parent / f"battlefield_performance_{timestamp}.json"
    
    with open(results_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Performance analysis saved to: {results_path}")
    
    # Print summary
    if "performance_impact" in analysis:
        impact = analysis["performance_impact"]
        print(f"\nPerformance Impact Summary:")
        print(f"- FPS with atmospheric elements: {results_with['avg_fps']:.1f}")
        print(f"- FPS without atmospheric elements: {results_without['avg_fps']:.1f}")
        print(f"- FPS reduction: {impact['fps_reduction']:.1f} ({impact['fps_reduction_percent']:.1f}%)")
        print(f"- Performance category: {impact['performance_category']}")
    
    return analysis

if __name__ == "__main__":
    main()