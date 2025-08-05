"""
Performance Optimization Showcase for Sands of Duat

This example demonstrates how to integrate and use all the advanced
performance optimization systems to achieve Hades-level visual quality
while maintaining 60fps on RTX 5070 and scaling for lower-end hardware.

Run this example to see:
- Smart asset streaming in action
- Dynamic quality adjustment
- Advanced particle effects
- Parallax backgrounds with atmospheric effects
- Real-time performance monitoring
- Memory optimization
"""

import pygame
import sys
import time
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sands_duat.graphics.performance_integration import (
    initialize_performance_systems, 
    get_performance_coordinator,
    set_current_screen,
    update_performance_systems,
    render_optimized_visuals,
    ScreenType,
    PerformanceMode
)
from sands_duat.graphics.comprehensive_profiler import (
    start_frame_profiling,
    end_frame_profiling,
    get_performance_dashboard
)


class PerformanceShowcase:
    """Showcase application demonstrating all performance optimizations."""
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sands of Duat - Performance Optimization Showcase")
        
        # Initialize performance systems
        self.coordinator = initialize_performance_systems(width, height)
        
        # Demo state
        self.current_demo = 0
        self.demo_screens = [
            ScreenType.MENU,
            ScreenType.COMBAT,
            ScreenType.DECK_BUILDER,
            ScreenType.MAP,
            ScreenType.PROGRESSION
        ]
        self.demo_timer = 0.0
        self.demo_duration = 10.0  # 10 seconds per demo
        
        # Performance tracking
        self.frame_count = 0
        self.last_fps_update = time.time()
        self.current_fps = 0.0
        
        # UI elements
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        print("Performance Optimization Showcase Initialized")
        print(f"Screen Resolution: {width}x{height}")
        print("="*60)
    
    def run(self):
        """Main showcase loop."""
        self.coordinator.set_performance_mode(PerformanceMode.ADAPTIVE)
        
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # 60 FPS target
            
            # Start frame profiling
            start_frame_profiling()
            
            try:
                self.handle_events()
                self.update(delta_time)
                self.render()
                
                self.frame_count += 1
                
                # Update FPS counter
                current_time = time.time()
                if current_time - self.last_fps_update >= 1.0:
                    self.current_fps = self.frame_count / (current_time - self.last_fps_update)
                    self.frame_count = 0
                    self.last_fps_update = current_time
                
            finally:
                # End frame profiling
                end_frame_profiling()
        
        self.cleanup()
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Skip to next demo
                    self.next_demo()
                elif event.key == pygame.K_1:
                    self.coordinator.set_performance_mode(PerformanceMode.QUALITY_FIRST)
                elif event.key == pygame.K_2:
                    self.coordinator.set_performance_mode(PerformanceMode.BALANCED)
                elif event.key == pygame.K_3:
                    self.coordinator.set_performance_mode(PerformanceMode.PERFORMANCE_FIRST)
                elif event.key == pygame.K_4:
                    self.coordinator.set_performance_mode(PerformanceMode.ADAPTIVE)
                elif event.key == pygame.K_p:
                    # Generate performance report
                    self.generate_report()
    
    def update(self, delta_time: float):
        """Update showcase state."""
        # Update demo timer
        self.demo_timer += delta_time
        if self.demo_timer >= self.demo_duration:
            self.next_demo()
        
        # Update all performance systems
        update_performance_systems(delta_time)
        
        # Demo-specific updates
        self.update_demo_effects(delta_time)
    
    def next_demo(self):
        """Switch to next demo screen."""
        self.current_demo = (self.current_demo + 1) % len(self.demo_screens)
        self.demo_timer = 0.0
        
        screen_type = self.demo_screens[self.current_demo]
        set_current_screen(screen_type)
        
        print(f"Switched to {screen_type.value} demo")
    
    def update_demo_effects(self, delta_time: float):
        """Update demo-specific visual effects."""
        screen_type = self.demo_screens[self.current_demo]
        
        if screen_type == ScreenType.COMBAT:
            # Add combat particles
            if self.frame_count % 10 == 0:  # Every 10 frames
                self.coordinator.particle_system.create_card_effect(
                    "attack", 
                    400 + (self.demo_timer * 50) % 400, 
                    300 + (self.demo_timer * 30) % 200
                )
        
        elif screen_type == ScreenType.DECK_BUILDER:
            # Add magical sparkles
            if self.frame_count % 15 == 0:
                self.coordinator.particle_system.create_card_effect(
                    "power",
                    600 + (self.demo_timer * 100) % 300,
                    400 + (self.demo_timer * 80) % 200
                )
    
    def render(self):
        """Render the showcase."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Render optimized visual systems
        render_optimized_visuals(self.screen)
        
        # Render UI overlay
        self.render_ui()
        
        # Update display
        pygame.display.flip()
    
    def render_ui(self):
        """Render UI overlay with performance information."""
        # Get performance data
        dashboard = get_performance_dashboard()
        
        # Background for UI
        ui_surface = pygame.Surface((400, 300), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 180))
        self.screen.blit(ui_surface, (10, 10))
        
        y_offset = 20
        
        # Title
        title_text = self.font.render("Performance Optimization Showcase", True, (255, 255, 255))
        self.screen.blit(title_text, (20, y_offset))
        y_offset += 35
        
        # Current demo
        screen_name = self.demo_screens[self.current_demo].value.title()
        demo_text = self.small_font.render(f"Demo: {screen_name} ({self.demo_timer:.1f}s)", True, (255, 215, 0))
        self.screen.blit(demo_text, (20, y_offset))
        y_offset += 25
        
        # Performance metrics
        fps_text = self.small_font.render(f"FPS: {self.current_fps:.1f}", True, (0, 255, 0))
        self.screen.blit(fps_text, (20, y_offset))
        y_offset += 20
        
        if "real_time_metrics" in dashboard:
            metrics = dashboard["real_time_metrics"]
            
            frame_time_text = self.small_font.render(
                f"Frame Time: {metrics.get('current_frame_time_ms', 0):.2f}ms", 
                True, (0, 255, 255)
            )
            self.screen.blit(frame_time_text, (20, y_offset))
            y_offset += 20
            
            memory_text = self.small_font.render(
                f"Memory: {metrics.get('memory_usage_mb', 0):.1f}MB", 
                True, (255, 255, 0)
            )
            self.screen.blit(memory_text, (20, y_offset))
            y_offset += 20
            
            bottleneck_text = self.small_font.render(
                f"Bottleneck: {metrics.get('bottleneck', 'unknown').title()}", 
                True, (255, 128, 0)
            )
            self.screen.blit(bottleneck_text, (20, y_offset))
            y_offset += 25
        
        # Performance mode
        mode_text = self.small_font.render(
            f"Mode: {dashboard.get('performance_mode', 'unknown').title()}", 
            True, (128, 255, 128)
        )
        self.screen.blit(mode_text, (20, y_offset))
        y_offset += 25
        
        # Quality settings
        if "quality_settings" in dashboard:
            quality = dashboard["quality_settings"]
            particles_text = self.small_font.render(
                f"Max Particles: {quality.get('max_particles', 0)}", 
                True, (255, 128, 255)
            )
            self.screen.blit(particles_text, (20, y_offset))
            y_offset += 20
            
            texture_quality_text = self.small_font.render(
                f"Texture Quality: {quality.get('texture_quality', 1.0):.1f}", 
                True, (128, 255, 255)
            )
            self.screen.blit(texture_quality_text, (20, y_offset))
            y_offset += 25
        
        # Controls
        controls = [
            "Controls:",
            "SPACE - Next Demo",
            "1 - Quality First",
            "2 - Balanced", 
            "3 - Performance First",
            "4 - Adaptive",
            "P - Generate Report",
            "ESC - Exit"
        ]
        
        for i, control in enumerate(controls):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            control_text = self.small_font.render(control, True, color)
            self.screen.blit(control_text, (20, y_offset + i * 15))
    
    def generate_report(self):
        """Generate and save performance report."""
        print("\nGenerating performance report...")
        
        try:
            report = self.coordinator.generate_performance_report()
            print("Performance report generated successfully!")
            print("Check the 'reports' folder for detailed analysis.")
        except Exception as e:
            print(f"Failed to generate report: {e}")
    
    def cleanup(self):
        """Cleanup resources."""
        print("\nShutdown Performance Showcase")
        print("="*60)
        
        # Print final statistics
        dashboard = get_performance_dashboard()
        if "real_time_metrics" in dashboard:
            metrics = dashboard["real_time_metrics"]
            print(f"Final FPS: {self.current_fps:.1f}")
            print(f"Final Frame Time: {metrics.get('current_frame_time_ms', 0):.2f}ms")
            print(f"Memory Usage: {metrics.get('memory_usage_mb', 0):.1f}MB")
        
        pygame.quit()


def main():
    """Main entry point for the showcase."""
    print("Sands of Duat - Performance Optimization Showcase")
    print("="*60)
    print("This showcase demonstrates:")
    print("• Smart asset streaming and preloading")
    print("• Dynamic quality adjustment based on performance")
    print("• Advanced particle systems with LOD")
    print("• Parallax backgrounds with atmospheric effects")
    print("• Real-time memory management")
    print("• Comprehensive performance profiling")
    print("="*60)
    
    # Check for command line arguments
    width = 1920
    height = 1080
    
    if len(sys.argv) >= 3:
        try:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
        except ValueError:
            print("Invalid resolution arguments, using default 1920x1080")
    
    # Create and run showcase
    showcase = PerformanceShowcase(width, height)
    showcase.run()


if __name__ == "__main__":
    main()