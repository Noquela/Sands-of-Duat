"""
Example Usage of Hour-Glass Initiative System

Demonstrates how to use the complete Hour-Glass Initiative system
with all components working together in a real game scenario.

This example shows:
- Setting up hourglasses for player and enemies
- Integrating with Pygame for visual feedback
- Using the enhanced combat system
- Implementing enemy AI
- Debug and monitoring capabilities
"""

import pygame
import asyncio
import logging
import time
from typing import Dict, Any

from .hourglass import HourGlass, TimingAccuracy
from .combat_enhanced import EnhancedCombatEngine, EnhancedCombatAction, ActionType, ActionPriority
from .sand_visuals import sand_visualizer, VisualTheme
from .animation_coordinator import animation_coordinator, AnimationType, AnimationPriority
from .enemy_ai import enemy_ai_manager, AIDifficultyLevel, SandStrategy
from .pygame_integration import PygameHourGlassManager, RenderQuality
from .debug_logger import debug_logger, DebugCategory


class HourGlassDemo:
    """
    Complete demonstration of the Hour-Glass Initiative system.
    
    Shows all features working together in a playable demo.
    """
    
    def __init__(self, screen_width: int = 1024, screen_height: int = 768):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hour-Glass Initiative Demo")
        self.clock = pygame.time.Clock()
        
        # Core systems
        self.combat_engine = EnhancedCombatEngine()
        self.pygame_manager = PygameHourGlassManager(screen_width, screen_height)
        
        # Game state
        self.running = False
        self.entities: Dict[str, Dict[str, Any]] = {}
        
        # Demo settings
        self.debug_mode = True
        self.target_fps = 60
        
        logging.info("Hour-Glass Demo initialized")
    
    def initialize(self) -> None:
        """Initialize the demo."""
        # Initialize Pygame integration
        self.pygame_manager.initialize(self.combat_engine)
        
        # Enable debug mode
        if self.debug_mode:
            debug_logger.enable_full_debugging()
            debug_logger.start_performance_profiling()
            self.pygame_manager.enable_debug_overlay()
        
        # Create player hourglass
        self._create_player()
        
        # Create enemies
        self._create_enemy("enemy_1", AIDifficultyLevel.NORMAL, SandStrategy.BALANCED)
        self._create_enemy("enemy_2", AIDifficultyLevel.HARD, SandStrategy.AGGRESSIVE)
        
        # Start combat
        self.combat_engine.start_combat(["player", "enemy_1", "enemy_2"])
        
        # Set visual themes
        sand_visualizer.set_global_theme(VisualTheme.DESERT)
        
        logging.info("Demo initialized successfully")
    
    def _create_player(self) -> None:
        """Create player entity with hourglass."""
        # Create hourglass with high precision timing
        hourglass = HourGlass(current_sand=3, max_sand=6)
        hourglass.set_timing_accuracy(TimingAccuracy.HIGH)
        
        # Register with all systems
        self.combat_engine.register_combatant_hourglass("player", hourglass)
        self.pygame_manager.register_entity(
            "player", hourglass,
            position=(50, 100), size=(200, 120), is_enemy=False
        )
        
        # Store entity data
        self.entities["player"] = {
            "hourglass": hourglass,
            "type": "player",
            "position": (50, 100),
            "size": (200, 120)
        }
        
        logging.info("Player created")
    
    def _create_enemy(self, entity_id: str, difficulty: AIDifficultyLevel, 
                     strategy: SandStrategy) -> None:
        """Create enemy entity with AI."""
        # Create hourglass
        hourglass = HourGlass(current_sand=2, max_sand=6)
        hourglass.set_timing_accuracy(TimingAccuracy.HIGH)
        
        # Register with combat system
        self.combat_engine.register_combatant_hourglass(entity_id, hourglass)
        
        # Register AI
        ai = enemy_ai_manager.register_enemy_ai(
            entity_id, hourglass, self.combat_engine, difficulty
        )
        ai.strategy = strategy
        
        # Calculate position based on enemy number
        enemy_num = int(entity_id.split("_")[1])
        x_pos = 400 + (enemy_num - 1) * 220
        y_pos = 100 + (enemy_num - 1) * 150
        
        # Register with visual system
        self.pygame_manager.register_entity(
            entity_id, hourglass,
            position=(x_pos, y_pos), size=(180, 100), is_enemy=True
        )
        
        # Store entity data
        self.entities[entity_id] = {
            "hourglass": hourglass,
            "ai": ai,
            "type": "enemy",
            "difficulty": difficulty,
            "strategy": strategy,
            "position": (x_pos, y_pos),
            "size": (180, 100)
        }
        
        logging.info(f"Enemy {entity_id} created with {difficulty.value} difficulty")
    
    async def run(self) -> None:
        """Run the demo."""
        self.running = True
        last_time = time.time()
        
        logging.info("Starting Hour-Glass Initiative demo")
        
        try:
            while self.running:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                # Handle Pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_F1:
                            self._toggle_debug()
                        elif event.key == pygame.K_F2:
                            self._generate_report()
                        else:
                            # Handle combat input
                            self.pygame_manager.handle_event(event)
                
                # Update systems
                await self._update(delta_time)
                
                # Render
                self._render()
                
                # Control frame rate
                self.clock.tick(self.target_fps)
                
        except KeyboardInterrupt:
            logging.info("Demo interrupted by user")
        finally:
            self._cleanup()
    
    async def _update(self, delta_time: float) -> None:
        """Update all systems."""
        # Update Pygame manager (handles hourglasses, visuals, etc.)
        self.pygame_manager.update(delta_time)
        
        # Process combat actions
        await self.combat_engine.process_actions()
        
        # Check for combat end conditions
        self._check_combat_end()
    
    def _render(self) -> None:
        """Render the demo."""
        # Clear screen
        self.screen.fill((40, 40, 40))  # Dark gray background
        
        # Render Hour-Glass visuals
        self.pygame_manager.render(self.screen)
        
        # Render UI
        self._render_ui()
        
        # Update display
        pygame.display.flip()
    
    def _render_ui(self) -> None:
        """Render additional UI elements."""
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)
        
        # Title
        title = font.render("Hour-Glass Initiative System Demo", True, (255, 255, 255))
        self.screen.blit(title, (10, 10))
        
        # Instructions
        instructions = [
            "Controls:",
            "1 - Play Card (1 sand)",
            "2 - Use Ability (2 sand)",
            "Space - End Turn",
            "F1 - Toggle Debug",
            "F2 - Generate Report",
            "ESC - Quit"
        ]
        
        y_offset = 40
        for instruction in instructions:
            text = small_font.render(instruction, True, (200, 200, 200))
            self.screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # Combat status
        if self.combat_engine.state.is_active():
            status_text = f"Combat Active - Turn {self.combat_engine.state.turn_count}"
            status = font.render(status_text, True, (255, 255, 0))
            self.screen.blit(status, (10, self.screen_height - 30))
        
        # Entity information
        self._render_entity_info()
    
    def _render_entity_info(self) -> None:
        """Render information about entities."""
        font = pygame.font.Font(None, 16)
        y_start = 200
        
        for entity_id, entity_data in self.entities.items():
            hourglass = entity_data["hourglass"]
            x_pos = entity_data["position"][0]
            y_pos = entity_data["position"][1] + entity_data["size"][1] + 10
            
            # Sand count
            sand_text = f"{hourglass.current_sand}/{hourglass.max_sand}"
            sand_surface = font.render(sand_text, True, (255, 255, 255))
            self.screen.blit(sand_surface, (x_pos, y_pos))
            
            # Time until next sand
            if hourglass.current_sand < hourglass.max_sand:
                time_remaining = hourglass.get_time_until_next_sand()
                if time_remaining != float('inf'):
                    time_text = f"Next: {time_remaining:.1f}s"
                    time_surface = font.render(time_text, True, (200, 200, 200))
                    self.screen.blit(time_surface, (x_pos, y_pos + 15))
            
            # AI info for enemies
            if "ai" in entity_data:
                ai = entity_data["ai"]
                strategy_text = f"Strategy: {ai.strategy.value}"
                strategy_surface = font.render(strategy_text, True, (150, 150, 255))
                self.screen.blit(strategy_surface, (x_pos, y_pos + 30))
                
                actions_text = f"Actions: {ai.actions_taken}"
                actions_surface = font.render(actions_text, True, (150, 255, 150))
                self.screen.blit(actions_surface, (x_pos, y_pos + 45))
    
    def _check_combat_end(self) -> None:
        """Check if combat should end."""
        # Simple victory condition: player survives 50 turns
        if self.combat_engine.state.turn_count >= 50:
            self.combat_engine.end_combat(winner="player")
            logging.info("Demo completed - Player survived 50 turns!")
    
    def _toggle_debug(self) -> None:
        """Toggle debug mode."""
        if self.debug_mode:
            debug_logger.disable_all_debugging()
            self.pygame_manager.disable_debug_overlay()
            self.debug_mode = False
            logging.info("Debug mode disabled")
        else:
            debug_logger.enable_full_debugging()
            self.pygame_manager.enable_debug_overlay()
            self.debug_mode = True
            logging.info("Debug mode enabled")
    
    def _generate_report(self) -> None:
        """Generate and save debug report."""
        if self.debug_mode:
            filename = debug_logger.save_report_to_file()
            logging.info(f"Debug report saved to {filename}")
        else:
            logging.info("Debug mode not enabled")
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        logging.info("Cleaning up demo...")
        
        # Stop profiling
        debug_logger.stop_performance_profiling()
        
        # End combat
        if self.combat_engine.state.is_active():
            self.combat_engine.end_combat()
        
        # Quit pygame
        pygame.quit()
        
        logging.info("Demo cleanup complete")


class SimpleExample:
    """
    Simple example showing basic Hour-Glass functionality.
    
    Demonstrates core sand mechanics without full game integration.
    """
    
    def __init__(self):
        self.player_hourglass = HourGlass(current_sand=3)
        self.enemy_hourglass = HourGlass(current_sand=2)
        
        # Setup callbacks for monitoring
        self.player_hourglass.on_sand_change = self._on_player_sand_change
        self.enemy_hourglass.on_sand_change = self._on_enemy_sand_change
    
    def _on_player_sand_change(self, new_amount: int) -> None:
        """Callback for player sand changes."""
        print(f"Player sand: {new_amount}")
    
    def _on_enemy_sand_change(self, new_amount: int) -> None:
        """Callback for enemy sand changes."""
        print(f"Enemy sand: {new_amount}")
    
    async def run_simulation(self, duration: float = 30.0) -> None:
        """Run a simple simulation."""
        print("Starting Hour-Glass simulation...")
        print(f"Player starts with {self.player_hourglass.current_sand} sand")
        print(f"Enemy starts with {self.enemy_hourglass.current_sand} sand")
        print()
        
        start_time = time.time()
        last_update = start_time
        
        while time.time() - start_time < duration:
            current_time = time.time()
            delta_time = current_time - last_update
            last_update = current_time
            
            # Update hourglasses
            self.player_hourglass.update_with_frame_time(delta_time)
            self.enemy_hourglass.update_with_frame_time(delta_time)
            
            # Simulate some actions
            if time.time() - start_time > 5 and self.player_hourglass.can_afford(2):
                self.player_hourglass.spend_sand(2)
                print("Player used ability (cost: 2)")
            
            if time.time() - start_time > 8 and self.enemy_hourglass.can_afford(1):
                self.enemy_hourglass.spend_sand(1)
                print("Enemy played card (cost: 1)")
            
            # Sleep briefly to simulate frame timing
            await asyncio.sleep(0.016)  # ~60 FPS
        
        print()
        print("Simulation complete!")
        print(f"Final player sand: {self.player_hourglass.current_sand}")
        print(f"Final enemy sand: {self.enemy_hourglass.current_sand}")


async def run_demo():
    """Run the full Hour-Glass Initiative demo."""
    demo = HourGlassDemo()
    demo.initialize()
    await demo.run()


async def run_simple_example():
    """Run the simple example."""
    example = SimpleExample()
    await example.run_simulation()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        # Run simple example
        asyncio.run(run_simple_example())
    else:
        # Run full demo
        asyncio.run(run_demo())