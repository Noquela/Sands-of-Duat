"""
Performance Integration Example for Sands of Duat

This example demonstrates how to integrate all performance optimizations
into the main game loop for optimal 60fps gameplay with premium visuals.
"""

import pygame
import sys
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent / "sands_duat"
sys.path.insert(0, str(project_root))

from core.performance_integration import initialize_performance_manager, get_performance_manager
from core.performance_profiler import profile_operation
from assets.optimized_asset_manager import AssetType


class OptimizedGameDemo:
    """
    Demonstration of optimized game loop with all performance enhancements.
    """
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.running = True
        
        # Initialize pygame
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Create optimized display
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("Sands of Duat - Performance Optimized")
        
        # Initialize performance manager
        self.perf_manager = initialize_performance_manager((width, height), target_fps=60.0)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        
        # Demo state
        self.demo_time = 0.0
        self.particle_spawn_timer = 0.0
        
        # Load demo assets (if available)
        self._load_demo_assets()
        
        print("Optimized Game Demo Initialized")
        print(f"Display: {width}x{height}")
        print(f"Target FPS: {self.target_fps}")
        print("Performance optimizations: ACTIVE")
    
    def _load_demo_assets(self):
        """Load demo assets for testing."""
        # Try to load some assets for demonstration
        asset_paths = [
            "game_assets/environments/menu_background.png",
            "game_assets/environments/combat_background.png",
            "game_assets/cards/sand_grain.png"
        ]
        
        self.demo_assets = {}
        
        for asset_path in asset_paths:
            full_path = Path(__file__).parent.parent / asset_path
            if full_path.exists():
                # Determine asset type
                if "background" in asset_path:
                    asset_type = AssetType.BACKGROUND
                elif "card" in asset_path:
                    asset_type = AssetType.CARD_ART
                else:
                    asset_type = AssetType.UI_ELEMENT
                
                # Load asynchronously
                future = self.perf_manager.load_asset_async(str(full_path), asset_type)
                self.demo_assets[asset_path] = future
                print(f"Loading asset: {asset_path}")
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F1:
                    # Toggle adaptive quality
                    current_state = self.perf_manager.adaptive_quality_enabled
                    self.perf_manager.set_adaptive_quality(not current_state)
                    print(f"Adaptive quality: {'ON' if not current_state else 'OFF'}")
                elif event.key == pygame.K_F2:
                    # Force quality levels
                    quality_levels = [0, 1, 2, 3]
                    current_level = self.perf_manager.theme.current_detail_level
                    next_level = (current_level + 1) % len(quality_levels)
                    self.perf_manager.force_quality_level(next_level)
                    print(f"Forced quality level: {next_level}")
                elif event.key == pygame.K_F3:
                    # Create particle burst
                    self.perf_manager.create_particle_effect(
                        "FIRE_SPARK", self.width//2, self.height//2, 
                        count=50, intensity=2.0
                    )
                    print("Created particle burst")
                elif event.key == pygame.K_F4:
                    # Export performance report
                    self.perf_manager.export_performance_data("performance_report.json")
                    print("Performance report exported")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create particle effect at mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.perf_manager.create_particle_effect(
                    "GOLDEN_AURA", mouse_x, mouse_y, 
                    count=20, intensity=1.5
                )
    
    def update(self, delta_time: float):
        """Update game logic with performance monitoring."""
        with profile_operation("game_logic_update"):
            # Update demo time
            self.demo_time += delta_time
            
            # Create periodic particle effects
            self.particle_spawn_timer += delta_time
            if self.particle_spawn_timer >= 2.0:  # Every 2 seconds
                self.particle_spawn_timer = 0.0
                
                # Create sand flow effect
                start_x = 100
                start_y = 100
                end_x = self.width - 100
                end_y = self.height - 100
                
                self.perf_manager.create_particle_effect(
                    "sand_flow", start_x, start_y,
                    end_x=end_x, end_y=end_y, intensity=1.0
                )
            
            # Update performance manager
            self.perf_manager.update(delta_time)
    
    def render(self):
        """Render game with performance optimizations."""
        with profile_operation("game_render"):
            # Clear screen
            self.screen.fill((0, 0, 0))
            
            # Render background overlay
            self.perf_manager.render_ui_element(
                self.screen, "background_overlay", alpha=100
            )
            
            # Render demo UI elements
            self._render_demo_ui()
            
            # Render particles
            self.perf_manager.render_particles(self.screen)
            
            # Render performance info
            self._render_performance_info()
            
            # Update display
            pygame.display.flip()
    
    def _render_demo_ui(self):
        """Render demonstration UI elements."""
        # Demo buttons
        button_width = 200
        button_height = 50
        button_spacing = 60
        
        buttons = [
            ("Performance Demo", "normal"),
            ("Particle Effects", "hover"),
            ("Asset Loading", "normal"),
            ("Memory Management", "active")
        ]
        
        for i, (text, state) in enumerate(buttons):
            button_rect = pygame.Rect(
                50, 50 + i * button_spacing,
                button_width, button_height
            )
            
            self.perf_manager.render_ui_element(
                self.screen, "button", button_rect, text, state
            )
        
        # Demo health orb
        health_center = (self.width - 100, 100)
        health_current = int(75 + 25 * abs(pygame.math.Vector2(1, 0).rotate(self.demo_time * 90).x))
        
        self.perf_manager.render_ui_element(
            self.screen, "health_orb", health_center, health_current, 100, 40
        )
        
        # Demo card frame
        card_rect = pygame.Rect(self.width - 250, 200, 120, 180)
        self.perf_manager.render_ui_element(
            self.screen, "card_frame", card_rect, "attack", "rare"
        )
        
        # Demo title text
        title_pos = (self.width // 2, 50)
        self.perf_manager.render_ui_element(
            self.screen, "title_text", "SANDS OF DUAT", title_pos, "title"
        )
    
    def _render_performance_info(self):
        """Render real-time performance information."""
        font = pygame.font.Font(None, 24)
        
        # Get performance metrics
        current_fps = self.perf_manager.current_fps
        particle_stats = self.perf_manager.particle_system.get_statistics()
        theme_stats = self.perf_manager.theme.get_performance_stats()
        
        # Create performance info
        info_lines = [
            f"FPS: {current_fps:.1f} / {self.perf_manager.target_fps}",
            f"Particles: {particle_stats['active_particles']}",
            f"Quality Level: {theme_stats['detail_level']}",
            f"Cache Efficiency: {theme_stats['cache_efficiency']:.1%}",
            f"Memory: {particle_stats['memory_efficiency']['estimated_memory_kb']:.1f}KB",
            "",
            "Controls:",
            "F1 - Toggle Adaptive Quality",
            "F2 - Cycle Quality Levels",
            "F3 - Create Particle Burst",
            "F4 - Export Performance Report",
            "Mouse - Create Particles",
            "ESC - Exit"
        ]
        
        # Render performance info
        y_offset = self.height - 20 * len(info_lines) - 20
        
        for i, line in enumerate(info_lines):
            if line:  # Skip empty lines
                color = (255, 255, 255)
                if "FPS:" in line:
                    # Color-code FPS
                    if current_fps >= self.perf_manager.target_fps * 0.95:
                        color = (0, 255, 0)  # Green
                    elif current_fps >= self.perf_manager.target_fps * 0.8:
                        color = (255, 255, 0)  # Yellow
                    else:
                        color = (255, 0, 0)  # Red
                
                text_surface = font.render(line, True, color)
                self.screen.blit(text_surface, (20, y_offset + i * 20))
    
    def run(self):
        """Main game loop with performance monitoring."""
        print("\nStarting optimized game loop...")
        print("Press F1-F4 for performance controls, ESC to exit")
        
        # Main game loop
        while self.running:
            # Start frame timing
            frame_start_time = self.perf_manager.start_frame()
            
            # Calculate delta time
            delta_time = self.clock.tick(self.target_fps) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update game logic
            self.update(delta_time)
            
            # Render everything
            self.render()
            
            # End frame timing and get metrics
            frame_time_ms = self.perf_manager.end_frame(frame_start_time)
            
            # Print performance warnings
            if frame_time_ms > 20.0:  # More than 20ms (under 50fps)
                print(f"Performance warning: Frame took {frame_time_ms:.1f}ms")
        
        # Shutdown
        self.shutdown()
    
    def shutdown(self):
        """Shutdown demo and export final performance report."""
        print("\nShutting down...")
        
        # Get final performance report
        report = self.perf_manager.get_performance_report()
        
        print("\nFinal Performance Report:")
        print(f"Average FPS: {report['overall_performance']['average_fps']:.1f}")
        print(f"Performance Stability: {report['overall_performance']['performance_stability']:.1%}")
        print(f"Total Particles Created: {report['session_statistics']['total_particles_created']}")
        print(f"Performance Adjustments: {report['overall_performance']['quality_adjustments']}")
        
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"- {rec}")
        
        # Export detailed report
        self.perf_manager.export_performance_data("demo_performance_final.json")
        print("\nDetailed performance data exported to demo_performance_final.json")
        
        # Shutdown systems
        self.perf_manager.shutdown()
        pygame.quit()


def main():
    """Run the performance optimization demonstration."""
    print("Sands of Duat - Performance Optimization Demo")
    print("=" * 50)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--windowed":
            demo = OptimizedGameDemo(1280, 720)
        elif sys.argv[1] == "--fullhd":
            demo = OptimizedGameDemo(1920, 1080)
        elif sys.argv[1] == "--4k":
            demo = OptimizedGameDemo(3840, 2160)
        else:
            print("Usage: python performance_integration_example.py [--windowed|--fullhd|--4k]")
            return
    else:
        # Default to ultrawide resolution
        demo = OptimizedGameDemo(3440, 1440)
    
    try:
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        demo.shutdown()
    except Exception as e:
        print(f"\nDemo error: {e}")
        import traceback
        traceback.print_exc()
        demo.shutdown()


if __name__ == "__main__":
    main()