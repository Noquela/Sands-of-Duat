#!/usr/bin/env python3
"""
Premium Asset Integration Example for Sands of Duat

Demonstrates how to integrate the high-performance asset system into the main game
for smooth 60fps performance with premium visual quality.
"""

import pygame
import sys
import time
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from sands_duat.graphics.premium_asset_integration import (
    PremiumAssetIntegrator, SystemConfiguration, IntegrationMode,
    initialize_premium_system, create_game_ready_config
)
from sands_duat.graphics.adaptive_performance_manager import QualityPreset
from sands_duat.graphics.asset_manager import AssetType, LoadingPriority


class PremiumGameExample:
    """Example game using the premium asset integration system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Sands of Duat - Premium Asset Integration Demo")
        self.clock = pygame.time.Clock()
        
        # Initialize premium asset system
        self.integrator = self._initialize_premium_system()
        
        # Game state
        self.running = True
        self.current_screen = "menu"
        self.show_debug = True
        self.last_perf_report = time.time()
        
        # Performance tracking
        self.frame_times = []
        self.fps_history = []
        
        self.logger.info("Premium Game Example initialized")
    
    def _initialize_premium_system(self) -> PremiumAssetIntegrator:
        """Initialize the premium asset integration system"""
        # Create optimized configuration
        config = create_game_ready_config("auto")  # Auto-detect hardware
        
        # Customize for demo
        config.debug_mode = True
        config.performance_monitoring = True
        config.adaptive_quality = True
        
        # Initialize system
        integrator = initialize_premium_system(config, 1920, 1080)
        
        # Add callbacks for monitoring
        integrator.add_performance_callback(self._on_performance_update)
        integrator.add_quality_callback(self._on_quality_change)
        
        self.logger.info("Premium asset system initialized")
        return integrator
    
    def _on_performance_update(self, performance_data):
        """Handle performance updates"""
        fps = performance_data['fps']
        self.fps_history.append(fps)
        
        # Keep only recent history
        if len(self.fps_history) > 300:  # 5 seconds at 60fps
            self.fps_history.pop(0)
        
        # Log performance issues
        if fps < 45:
            self.logger.warning(f"Performance issue detected: {fps:.1f} FPS")
    
    def _on_quality_change(self, quality_settings):
        """Handle quality setting changes"""
        self.logger.info(f"Quality changed: render_scale={quality_settings.render_scale:.2f}, "
                        f"texture_quality={quality_settings.texture_quality:.2f}")
    
    def run(self):
        """Main game loop"""
        self.logger.info("Starting premium game loop")
        
        # Initial screen setup
        self.integrator.switch_screen(self.current_screen, "game_assets")
        
        while self.running:
            frame_start = time.perf_counter()
            
            # Handle events
            self._handle_events()
            
            # Update game
            dt = self.clock.tick(60) / 1000.0  # 60 FPS target
            self._update(dt)
            
            # Render
            self._render(dt)
            
            # Update display
            pygame.display.flip()
            
            # Track performance
            frame_time = time.perf_counter() - frame_start
            self.frame_times.append(frame_time)
            
            # Keep recent frame times only
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
            
            # Periodic performance reporting
            if time.time() - self.last_perf_report > 5.0:
                self._report_performance()
                self.last_perf_report = time.time()
        
        self._shutdown()
    
    def _handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_F1:
                    # Toggle debug display
                    self.show_debug = not self.show_debug
                
                elif event.key == pygame.K_F2:
                    # Force memory cleanup
                    result = self.integrator.force_memory_cleanup()
                    self.logger.info(f"Manual cleanup: {result}")
                
                elif event.key == pygame.K_F3:
                    # Run performance benchmark
                    self._run_benchmark()
                
                elif event.key == pygame.K_1:
                    # Switch to menu screen
                    self._switch_screen("menu")
                
                elif event.key == pygame.K_2:
                    # Switch to combat screen
                    self._switch_screen("combat")
                
                elif event.key == pygame.K_3:
                    # Switch to deck builder screen
                    self._switch_screen("deck_builder")
                
                elif event.key == pygame.K_4:
                    # Switch to map screen
                    self._switch_screen("map")
                
                elif event.key == pygame.K_q:
                    # Set quality to minimal
                    self.integrator.set_quality_mode(QualityPreset.MINIMAL)
                
                elif event.key == pygame.K_w:
                    # Set quality to low
                    self.integrator.set_quality_mode(QualityPreset.LOW)
                
                elif event.key == pygame.K_e:
                    # Set quality to medium
                    self.integrator.set_quality_mode(QualityPreset.MEDIUM)
                
                elif event.key == pygame.K_r:
                    # Set quality to high
                    self.integrator.set_quality_mode(QualityPreset.HIGH)
                
                elif event.key == pygame.K_t:
                    # Set quality to ultra
                    self.integrator.set_quality_mode(QualityPreset.ULTRA)
                
                elif event.key == pygame.K_a:
                    # Toggle adaptive quality
                    current_adaptive = self.integrator.performance_manager.quality_controller.adaptive_mode
                    self.integrator.set_adaptive_mode(not current_adaptive)
                    self.logger.info(f"Adaptive quality: {not current_adaptive}")
    
    def _switch_screen(self, screen_name: str):
        """Switch to a different screen"""
        if screen_name != self.current_screen:
            self.logger.info(f"Switching from {self.current_screen} to {screen_name}")
            
            # Measure transition time
            start_time = time.perf_counter()
            success = self.integrator.switch_screen(screen_name, "game_assets")
            transition_time = time.perf_counter() - start_time
            
            if success:
                self.current_screen = screen_name
                self.logger.info(f"Screen transition completed in {transition_time:.3f}s")
            else:
                self.logger.error(f"Failed to switch to {screen_name}")
    
    def _update(self, dt: float):
        """Update game logic"""
        # Simulate loading premium assets occasionally
        if int(time.time()) % 10 == 0 and int(time.time() * 10) % 10 == 0:
            # Load a premium card asset
            card_id = f"premium_card_{int(time.time()) % 10}"
            asset = self.integrator.load_premium_asset(
                card_id, AssetType.CARD_ART, LoadingPriority.MEDIUM
            )
            if asset:
                self.logger.debug(f"Loaded premium asset: {card_id}")
    
    def _render(self, dt: float):
        """Render the game frame"""
        # Clear screen
        self.screen.fill((20, 15, 10))  # Dark Egyptian theme
        
        # Render through premium integration system
        render_result = self.integrator.render_frame(self.screen, dt)
        
        # Add demo content
        self._render_demo_content()
        
        # Show debug info if enabled
        if self.show_debug:
            self._render_debug_info(render_result)
    
    def _render_demo_content(self):
        """Render demo content overlay"""
        font = pygame.font.Font(None, 36)
        
        # Screen title
        title_text = f"Current Screen: {self.current_screen.title()}"
        title_surface = font.render(title_text, True, (255, 215, 0))  # Gold
        self.screen.blit(title_surface, (50, 50))
        
        # Instructions
        instructions = [
            "Controls:",
            "1-4: Switch screens (Menu, Combat, Deck Builder, Map)",
            "Q-T: Quality presets (Minimal, Low, Medium, High, Ultra)",
            "A: Toggle adaptive quality",
            "F1: Toggle debug display",
            "F2: Force memory cleanup",
            "F3: Run benchmark",
            "ESC: Exit"
        ]
        
        small_font = pygame.font.Font(None, 24)
        y_offset = 100
        
        for instruction in instructions:
            color = (255, 255, 255) if instruction == "Controls:" else (200, 200, 200)
            text_surface = small_font.render(instruction, True, color)
            self.screen.blit(text_surface, (50, y_offset))
            y_offset += 25
    
    def _render_debug_info(self, render_result):
        """Render debug information"""
        debug_font = pygame.font.Font(None, 20)
        
        # Get performance summary
        perf_summary = self.integrator.get_performance_summary()
        
        # Calculate current FPS
        current_fps = 0.0
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            current_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        # Debug info
        debug_info = [
            f"FPS: {current_fps:.1f}",
            f"Frame Time: {render_result.get('frame_time_ms', 0):.2f}ms",
            f"Frame Count: {render_result.get('frame_count', 0)}",
            f"Memory: {perf_summary['memory']['system']['total_allocated_mb']:.1f}MB",
            f"Quality: {perf_summary['performance']['quality']['preset_equivalent']}",
            f"Adaptive: {'ON' if perf_summary['performance']['quality']['adaptive_mode'] else 'OFF'}",
            f"Render Stats: {render_result.get('render_stats', {})}",
        ]
        
        # Render debug info in top-right corner
        x_offset = self.screen.get_width() - 300
        y_offset = 20
        
        # Semi-transparent background
        debug_bg = pygame.Surface((280, len(debug_info) * 22 + 10))
        debug_bg.set_alpha(128)
        debug_bg.fill((0, 0, 0))
        self.screen.blit(debug_bg, (x_offset - 10, y_offset - 5))
        
        for info in debug_info:
            text_surface = debug_font.render(str(info), True, (0, 255, 0))
            self.screen.blit(text_surface, (x_offset, y_offset))
            y_offset += 22
    
    def _run_benchmark(self):
        """Run performance benchmark"""
        self.logger.info("Running performance benchmark...")
        
        benchmark_result = self.integrator.benchmark_performance(5.0)
        
        self.logger.info(f"Benchmark Results:")
        self.logger.info(f"  Average FPS: {benchmark_result['avg_fps']:.1f}")
        self.logger.info(f"  Min FPS: {benchmark_result['min_fps']:.1f}")
        self.logger.info(f"  Max FPS: {benchmark_result['max_fps']:.1f}")
        self.logger.info(f"  Performance Score: {benchmark_result['performance_score']:.1f}%")
        self.logger.info(f"  Target Met: {'YES' if benchmark_result['target_met'] else 'NO'}")
    
    def _report_performance(self):
        """Report current performance metrics"""
        if not self.fps_history:
            return
        
        avg_fps = sum(self.fps_history) / len(self.fps_history)
        min_fps = min(self.fps_history)
        max_fps = max(self.fps_history)
        
        # Get system summary
        summary = self.integrator.get_performance_summary()
        memory_mb = summary['memory']['system']['total_allocated_mb']
        
        self.logger.info(f"Performance Report - FPS: {avg_fps:.1f} (min: {min_fps:.1f}, max: {max_fps:.1f}), "
                        f"Memory: {memory_mb:.1f}MB")
    
    def _shutdown(self):
        """Clean shutdown"""
        self.logger.info("Shutting down premium game example")
        
        # Final performance report
        self._report_performance()
        
        # Shutdown premium system
        self.integrator.shutdown()
        
        # Shutdown pygame
        pygame.quit()
        
        self.logger.info("Shutdown complete")


def main():
    """Main function"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Premium Asset Integration Example")
    
    try:
        # Create and run the example
        game = PremiumGameExample()
        game.run()
        
    except Exception as e:
        logger.error(f"Error in premium game example: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())