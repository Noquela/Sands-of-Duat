"""
Pygame Integration for Hour-Glass Initiative System

Integrates the Hour-Glass Initiative system with Pygame's game loop,
providing real-time updates, visual rendering, and input handling
for the sand-based combat mechanics.

Key Features:
- Frame-rate independent sand updates
- Pygame event integration
- Visual rendering coordination
- Input handling for combat actions
- Performance monitoring and optimization

Classes:
- PygameHourGlassManager: Main integration manager
- SandRenderer: Pygame-specific sand visualization
- InputHandler: Combat input handling
- PerformanceMonitor: FPS and timing analysis
"""

import pygame
import logging
import time
import math
from enum import Enum
from typing import Dict, List, Optional, Any, Callable, Tuple
from pydantic import BaseModel, Field
from dataclasses import dataclass

from .hourglass import HourGlass, TimingAccuracy
from .sand_visuals import SandVisualizer, HourGlassWidget, SandState, ColorScheme
from .animation_coordinator import AnimationCoordinator, AnimationType, AnimationPriority
from .combat_enhanced import EnhancedCombatEngine, EnhancedCombatAction, ActionType
from .enemy_ai import EnemyAIManager


class RenderQuality(Enum):
    """Rendering quality levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


@dataclass
class SandGrainSprite:
    """Visual representation of a sand grain in Pygame."""
    rect: pygame.Rect
    state: SandState
    alpha: int = 255
    pulse_phase: float = 0.0
    animation_progress: float = 0.0
    
    def update(self, delta_time: float) -> None:
        """Update sprite animation."""
        self.pulse_phase += delta_time * 4  # Pulse frequency
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase -= 2 * math.pi


class SandRenderer:
    """
    Pygame-specific renderer for sand visualization.
    
    Handles all visual rendering of hourglasses, sand grains,
    and regeneration indicators using Pygame surfaces.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = None
        self.small_font = None
        self.surfaces_cache: Dict[str, pygame.Surface] = {}
        self.render_quality = RenderQuality.HIGH
        
        # Initialize fonts
        self._init_fonts()
        
        # Sand grain sprites
        self.sand_sprites: Dict[str, List[SandGrainSprite]] = {}  # entity_id -> sprites
        
        # Colors
        self.color_schemes: Dict[str, ColorScheme] = {}
        
        logging.info("Sand renderer initialized")
    
    def _init_fonts(self) -> None:
        """Initialize Pygame fonts."""
        try:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 16)
        except pygame.error as e:
            logging.warning(f"Failed to initialize fonts: {e}")
            self.font = None
            self.small_font = None
    
    def register_entity(self, entity_id: str, widget: HourGlassWidget, 
                       position: Tuple[int, int], size: Tuple[int, int]) -> None:
        """Register an entity for rendering."""
        # Create sand grain sprites
        sprites = []
        grain_size = min(size[0] // 6, size[1] // 2) // widget.hourglass.max_sand
        
        for i in range(widget.hourglass.max_sand):
            x = position[0] + (i % 3) * grain_size
            y = position[1] + (i // 3) * grain_size
            
            sprite = SandGrainSprite(
                rect=pygame.Rect(x, y, grain_size, grain_size),
                state=SandState.EMPTY
            )
            sprites.append(sprite)
        
        self.sand_sprites[entity_id] = sprites
        self.color_schemes[entity_id] = widget.color_scheme
        
        logging.debug(f"Registered entity for rendering: {entity_id}")
    
    def update_entity(self, entity_id: str, widget: HourGlassWidget, delta_time: float) -> None:
        """Update entity visual state."""
        sprites = self.sand_sprites.get(entity_id)
        if not sprites:
            return
        
        display_data = widget.get_display_data()
        sand_elements = display_data['sand_elements']
        
        # Update sprite states
        for i, sprite in enumerate(sprites):
            if i < len(sand_elements):
                element_data = sand_elements[i]
                sprite.state = SandState(element_data['state'])
                sprite.alpha = int(element_data['alpha'] * 255)
                sprite.animation_progress = 1.0 if element_data['animation_complete'] else 0.5
            
            sprite.update(delta_time)
    
    def render_hourglass(self, screen: pygame.Surface, entity_id: str, 
                        widget: HourGlassWidget, position: Tuple[int, int], 
                        size: Tuple[int, int]) -> None:
        """Render a complete hourglass widget."""
        display_data = widget.get_display_data()
        color_scheme = self.color_schemes.get(entity_id, widget.color_scheme)
        
        # Draw background
        bg_rect = pygame.Rect(position[0], position[1], size[0], size[1])
        pygame.draw.rect(screen, color_scheme.background, bg_rect)
        pygame.draw.rect(screen, color_scheme.border, bg_rect, 2)
        
        # Draw sand grains
        sprites = self.sand_sprites.get(entity_id, [])
        for sprite in sprites:
            self._render_sand_grain(screen, sprite, color_scheme)
        
        # Draw regeneration indicator
        if display_data['regeneration']['is_visible']:
            self._render_regeneration_indicator(
                screen, position, size, display_data['regeneration'], color_scheme
            )
        
        # Draw text info
        if self.font and not widget.is_enemy:  # Don't show exact info for enemies
            self._render_text_info(screen, position, size, display_data)
    
    def _render_sand_grain(self, screen: pygame.Surface, sprite: SandGrainSprite, 
                          color_scheme: ColorScheme) -> None:
        """Render a single sand grain."""
        color = color_scheme.empty
        
        if sprite.state == SandState.FULL:
            color = color_scheme.full
        elif sprite.state == SandState.REGENERATING:
            # Pulsing effect
            pulse = math.sin(sprite.pulse_phase) * 0.3 + 0.7
            color = tuple(int(c * pulse) for c in color_scheme.regenerating)
        elif sprite.state == SandState.SPENDING:
            color = color_scheme.spending
        
        # Apply alpha
        if sprite.alpha < 255:
            # Create a surface with per-pixel alpha
            grain_surface = pygame.Surface((sprite.rect.width, sprite.rect.height), pygame.SRCALPHA)
            grain_surface.fill((*color, sprite.alpha))
            screen.blit(grain_surface, sprite.rect)
        else:
            # Simple filled rectangle
            pygame.draw.rect(screen, color, sprite.rect)
            
            # Add border for better visibility
            if self.render_quality in [RenderQuality.HIGH, RenderQuality.ULTRA]:
                pygame.draw.rect(screen, (255, 255, 255), sprite.rect, 1)
    
    def _render_regeneration_indicator(self, screen: pygame.Surface, 
                                     position: Tuple[int, int], size: Tuple[int, int],
                                     regen_data: Dict[str, Any], color_scheme: ColorScheme) -> None:
        """Render sand regeneration progress indicator."""
        progress = regen_data['progress']
        pulse_intensity = regen_data['pulse_intensity']
        
        # Progress bar
        bar_width = size[0] - 10
        bar_height = 8
        bar_x = position[0] + 5
        bar_y = position[1] + size[1] - bar_height - 5
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, color_scheme.progress_bg, bg_rect)
        
        # Progress fill
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            fill_color = tuple(int(c * pulse_intensity) for c in color_scheme.progress_fill)
            pygame.draw.rect(screen, fill_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, color_scheme.border, bg_rect, 1)
    
    def _render_text_info(self, screen: pygame.Surface, position: Tuple[int, int], 
                         size: Tuple[int, int], display_data: Dict[str, Any]) -> None:
        """Render text information."""
        if not self.small_font:
            return
        
        sand_count = display_data['sand_count']
        max_sand = display_data['max_sand']
        time_remaining = display_data['regeneration']['time_remaining']
        
        # Sand count
        text = f"{sand_count}/{max_sand}"
        text_surface = self.small_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (position[0] + 5, position[1] + 5)
        screen.blit(text_surface, text_rect)
        
        # Time until next sand (if applicable)
        if time_remaining != float('inf') and time_remaining > 0:
            time_text = f"{time_remaining:.1f}s"
            time_surface = self.small_font.render(time_text, True, (200, 200, 200))
            time_rect = time_surface.get_rect()
            time_rect.topright = (position[0] + size[0] - 5, position[1] + 5)
            screen.blit(time_surface, time_rect)
    
    def render_action_preview(self, screen: pygame.Surface, entity_id: str,
                            action_type: ActionType, sand_cost: int,
                            position: Tuple[int, int], size: Tuple[int, int]) -> None:
        """Render preview of action sand cost."""
        sprites = self.sand_sprites.get(entity_id, [])
        color_scheme = self.color_schemes.get(entity_id)
        
        if not sprites or not color_scheme:
            return
        
        # Highlight affected sand grains
        for i in range(min(sand_cost, len(sprites))):
            sprite_index = len(sprites) - 1 - i  # Start from the last grain
            if sprite_index >= 0:
                sprite = sprites[sprite_index]
                
                # Draw preview overlay
                overlay_surface = pygame.Surface((sprite.rect.width, sprite.rect.height), pygame.SRCALPHA)
                overlay_surface.fill((255, 255, 0, 128))  # Yellow with transparency
                screen.blit(overlay_surface, sprite.rect)
    
    def set_render_quality(self, quality: RenderQuality) -> None:
        """Set rendering quality level."""
        self.render_quality = quality
        logging.info(f"Render quality set to {quality.value}")


class InputHandler:
    """
    Handles input for Hour-Glass Initiative combat.
    
    Manages keyboard and mouse input for combat actions,
    with sand cost validation and visual feedback.
    """
    
    def __init__(self, combat_engine: EnhancedCombatEngine):
        self.combat_engine = combat_engine
        self.key_bindings: Dict[int, ActionType] = {}
        self.mouse_enabled = True
        self.input_blocked = False
        
        # Default key bindings
        self._init_default_bindings()
        
        logging.info("Input handler initialized")
    
    def _init_default_bindings(self) -> None:
        """Initialize default key bindings."""
        self.key_bindings = {
            pygame.K_1: ActionType.PLAY_CARD,
            pygame.K_2: ActionType.ABILITY,
            pygame.K_SPACE: ActionType.END_TURN,
            pygame.K_ESCAPE: ActionType.FLEE
        }
    
    def handle_event(self, event: pygame.event.Event, player_id: str = "player") -> bool:
        """
        Handle a Pygame event for combat input.
        
        Returns True if the event was handled.
        """
        if self.input_blocked:
            return False
        
        if event.type == pygame.KEYDOWN:
            return self._handle_keydown(event, player_id)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.mouse_enabled:
            return self._handle_mousedown(event, player_id)
        
        return False
    
    def _handle_keydown(self, event: pygame.event.Event, player_id: str) -> bool:
        """Handle keyboard input."""
        action_type = self.key_bindings.get(event.key)
        if not action_type:
            return False
        
        return self._attempt_action(action_type, player_id)
    
    def _handle_mousedown(self, event: pygame.event.Event, player_id: str) -> bool:
        """Handle mouse input."""
        # Mouse handling can be implemented for UI elements
        # For now, just return False
        return False
    
    def _attempt_action(self, action_type: ActionType, player_id: str) -> bool:
        """Attempt to perform an action."""
        # Check if action is valid
        valid_actions = self.combat_engine.get_valid_actions(player_id)
        if action_type not in valid_actions:
            logging.debug(f"Invalid action: {action_type.value} for {player_id}")
            return False
        
        # Check sand cost
        if not self.combat_engine.can_actor_afford_action(player_id, action_type):
            time_until = self.combat_engine.get_time_until_affordable(player_id, action_type)
            logging.debug(f"Cannot afford {action_type.value}, need to wait {time_until:.1f}s")
            return False
        
        # Create and queue action
        action_costs = self.combat_engine.get_action_costs(player_id)
        sand_cost = action_costs.get(action_type, 0)
        
        action = EnhancedCombatAction(
            action_type=action_type,
            actor_id=player_id,
            sand_cost=sand_cost,
            priority=50  # Player actions have medium priority
        )
        
        success = self.combat_engine.queue_action(action)
        if success:
            logging.info(f"Player queued action: {action_type.value} (cost: {sand_cost})")
        
        return success
    
    def block_input(self) -> None:
        """Block all input (during animations, etc.)."""
        self.input_blocked = True
    
    def unblock_input(self) -> None:
        """Allow input again."""
        self.input_blocked = False
    
    def set_key_binding(self, key: int, action_type: ActionType) -> None:
        """Set a custom key binding."""
        self.key_bindings[key] = action_type
    
    def get_action_for_key(self, key: int) -> Optional[ActionType]:
        """Get the action bound to a key."""
        return self.key_bindings.get(key)


class PerformanceMonitor:
    """
    Monitors performance of the Hour-Glass Initiative system.
    
    Tracks FPS, sand update timing, and system performance
    to ensure smooth gameplay.
    """
    
    def __init__(self):
        self.fps_samples: List[float] = []
        self.sand_update_times: List[float] = []
        self.frame_times: List[float] = []
        self.max_samples = 60  # 1 second at 60 FPS
        
        self.last_update = time.time()
        self.frame_count = 0
        self.current_fps = 0.0
        
        # Performance targets
        self.target_fps = 60
        self.target_frame_time = 1.0 / self.target_fps
        
        logging.info("Performance monitor initialized")
    
    def update(self) -> None:
        """Update performance monitoring."""
        current_time = time.time()
        frame_time = current_time - self.last_update
        self.last_update = current_time
        
        # Record frame time
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)
        
        # Calculate FPS
        self.frame_count += 1
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1.0 / max(avg_frame_time, 0.001)  # Avoid division by zero
    
    def record_sand_update_time(self, update_time: float) -> None:
        """Record time taken for sand updates."""
        self.sand_update_times.append(update_time)
        if len(self.sand_update_times) > self.max_samples:
            self.sand_update_times.pop(0)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        stats = {
            'fps': self.current_fps,
            'target_fps': self.target_fps,
            'frame_count': self.frame_count
        }
        
        if self.frame_times:
            stats.update({
                'avg_frame_time': sum(self.frame_times) / len(self.frame_times),
                'min_frame_time': min(self.frame_times),
                'max_frame_time': max(self.frame_times),
                'frame_time_variance': self._calculate_variance(self.frame_times)
            })
        
        if self.sand_update_times:
            stats.update({
                'avg_sand_update_time': sum(self.sand_update_times) / len(self.sand_update_times),
                'max_sand_update_time': max(self.sand_update_times)
            })
        
        return stats
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def is_performance_acceptable(self) -> bool:
        """Check if current performance meets targets."""
        return self.current_fps >= self.target_fps * 0.9  # 90% of target FPS


class PygameHourGlassManager:
    """
    Main integration manager for Hour-Glass Initiative system with Pygame.
    
    Coordinates all components to provide seamless integration with
    Pygame's event loop and rendering system.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Core components
        self.sand_visualizer = SandVisualizer()
        self.animation_coordinator = AnimationCoordinator()
        self.enemy_ai_manager = EnemyAIManager()
        
        # Pygame-specific components
        self.sand_renderer = SandRenderer(screen_width, screen_height)
        self.performance_monitor = PerformanceMonitor()
        self.input_handler: Optional[InputHandler] = None
        
        # Entity management
        self.registered_entities: Dict[str, Dict[str, Any]] = {}  # entity_id -> data
        
        # Settings
        self.auto_quality_adjustment = True
        self.debug_overlay = False
        
        logging.info("Pygame HourGlass Manager initialized")
    
    def initialize(self, combat_engine: EnhancedCombatEngine) -> None:
        """Initialize with combat engine."""
        self.input_handler = InputHandler(combat_engine)
        
        # Register event callbacks
        combat_engine.on_combat_event = self._on_combat_event
        
        logging.info("Pygame integration initialized with combat engine")
    
    def register_entity(self, entity_id: str, hourglass: HourGlass, 
                       position: Tuple[int, int], size: Tuple[int, int],
                       is_enemy: bool = False) -> None:
        """Register an entity for full integration."""
        # Register with all systems
        widget = self.sand_visualizer.register_hourglass(entity_id, hourglass, is_enemy)
        self.animation_coordinator.register_hourglass(entity_id, hourglass)
        self.sand_renderer.register_entity(entity_id, widget, position, size)
        
        # Store entity data
        self.registered_entities[entity_id] = {
            'hourglass': hourglass,
            'widget': widget,
            'position': position,
            'size': size,
            'is_enemy': is_enemy
        }
        
        logging.info(f"Registered entity: {entity_id} (enemy: {is_enemy})")
    
    def unregister_entity(self, entity_id: str) -> None:
        """Unregister an entity from all systems."""
        self.sand_visualizer.unregister_hourglass(entity_id)
        self.animation_coordinator.unregister_hourglass(entity_id)
        
        if entity_id in self.registered_entities:
            del self.registered_entities[entity_id]
        
        logging.info(f"Unregistered entity: {entity_id}")
    
    def update(self, delta_time: float) -> None:
        """Update all systems."""
        # Update performance monitoring
        self.performance_monitor.update()
        
        # Update sand systems
        sand_update_start = time.time()
        
        for entity_data in self.registered_entities.values():
            hourglass = entity_data['hourglass']
            
            # Use frame-based updates for consistency
            hourglass.update_with_frame_time(delta_time)
        
        sand_update_time = time.time() - sand_update_start
        self.performance_monitor.record_sand_update_time(sand_update_time)
        
        # Update visual systems
        self.sand_visualizer.update_all()
        self.animation_coordinator.update()
        
        # Update enemy AI
        player_entity = self.registered_entities.get("player")
        if player_entity:
            player_sand = player_entity['hourglass'].current_sand
            self.enemy_ai_manager.update_all(player_sand)
        
        # Update renderer
        for entity_id, entity_data in self.registered_entities.items():
            self.sand_renderer.update_entity(entity_id, entity_data['widget'], delta_time)
        
        # Auto-adjust quality based on performance
        if self.auto_quality_adjustment:
            self._adjust_quality_based_on_performance()
    
    def render(self, screen: pygame.Surface) -> None:
        """Render all Hour-Glass related visuals."""
        for entity_id, entity_data in self.registered_entities.items():
            self.sand_renderer.render_hourglass(
                screen, entity_id, entity_data['widget'],
                entity_data['position'], entity_data['size']
            )
        
        # Render debug overlay if enabled
        if self.debug_overlay:
            self._render_debug_overlay(screen)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle Pygame events."""
        if self.input_handler:
            return self.input_handler.handle_event(event)
        return False
    
    def _on_combat_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle combat events."""
        if event_type == "action_resolving":
            # Start animation for action
            actor_id = event_data.get('actor_id')
            action_type = event_data.get('action_type')
            
            if actor_id and action_type:
                animation_type = self._get_animation_type_for_action(action_type)
                self.animation_coordinator.start_animation(
                    animation_type, actor_id, 0.8,  # 0.8 second animation
                    AnimationPriority.HIGH, blocks_sand_regen=True
                )
        
        elif event_type == "action_queued":
            # Visual feedback for queued action
            actor_id = event_data.get('actor_id')
            sand_cost = event_data.get('sand_cost', 0)
            
            if actor_id and sand_cost > 0:
                self.sand_visualizer.trigger_sand_spending(actor_id, sand_cost)
    
    def _get_animation_type_for_action(self, action_type: str) -> AnimationType:
        """Map action types to animation types."""
        mapping = {
            'play_card': AnimationType.CARD_PLAY,
            'ability': AnimationType.ABILITY_USE,
            'end_turn': AnimationType.UI_TRANSITION,
            'flee': AnimationType.UI_TRANSITION
        }
        return mapping.get(action_type, AnimationType.UI_TRANSITION)
    
    def _adjust_quality_based_on_performance(self) -> None:
        """Automatically adjust quality based on performance."""
        if not self.performance_monitor.is_performance_acceptable():
            # Reduce quality
            current_quality = self.animation_coordinator.animation_quality
            new_quality = max(0.5, current_quality - 0.1)
            self.animation_coordinator.set_animation_quality(new_quality)
            
            # Reduce render quality
            if self.sand_renderer.render_quality == RenderQuality.ULTRA:
                self.sand_renderer.set_render_quality(RenderQuality.HIGH)
            elif self.sand_renderer.render_quality == RenderQuality.HIGH:
                self.sand_renderer.set_render_quality(RenderQuality.MEDIUM)
    
    def _render_debug_overlay(self, screen: pygame.Surface) -> None:
        """Render debug information overlay."""
        if not self.sand_renderer.font:
            return
        
        # Performance stats
        stats = self.performance_monitor.get_performance_stats()
        y_offset = 10
        
        for key, value in stats.items():
            if isinstance(value, float):
                text = f"{key}: {value:.2f}"
            else:
                text = f"{key}: {value}"
            
            text_surface = self.sand_renderer.font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        # Animation status
        anim_status = self.animation_coordinator.get_animation_status()
        text = f"Animations: {anim_status['active_animations']}/{anim_status['max_concurrent']}"
        text_surface = self.sand_renderer.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, y_offset))
    
    def enable_debug_overlay(self) -> None:
        """Enable debug information overlay."""
        self.debug_overlay = True
        self.sand_visualizer.enable_debug_overlay()
    
    def disable_debug_overlay(self) -> None:
        """Disable debug information overlay."""
        self.debug_overlay = False
        self.sand_visualizer.disable_debug_overlay()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'registered_entities': len(self.registered_entities),
            'performance': self.performance_monitor.get_performance_stats(),
            'animations': self.animation_coordinator.get_animation_status(),
            'sand_visuals': self.sand_visualizer.get_debug_info() if self.debug_overlay else {},
            'auto_quality': self.auto_quality_adjustment,
            'debug_overlay': self.debug_overlay
        }