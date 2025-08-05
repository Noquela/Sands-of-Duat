"""
Menu Screen - Fixed Version
Main menu interface with Hades-style Egyptian theming.
"""

import pygame
import math
import random
import time
from typing import Dict, Any, Optional, List, Callable, Tuple
from .base import UIScreen, UIComponent
from .theme import get_theme
from .hades_theme import HadesEgyptianTheme
from .animation_system import EasingType
from sands_duat.audio.sound_effects import play_button_sound

# Import advanced visual effects and parallax systems
try:
    from sands_duat.graphics.master_visual_effects import get_visual_effects_manager, ScreenType
    from sands_duat.graphics.interactive_parallax_system import (
        get_interactive_parallax_system, InteractionType, trigger_ui_interaction, handle_mouse_parallax
    )
    from sands_duat.graphics.egyptian_atmospheric_effects import get_atmospheric_manager
    VFX_AVAILABLE = True
except ImportError:
    VFX_AVAILABLE = False


class HadesMenuButton(UIComponent):
    """Hades-style ornate button component for menu navigation."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, hades_theme: HadesEgyptianTheme, callback: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hades_theme = hades_theme
        
        # Visual states
        self.state = 'normal'  # normal, hover, active, disabled
        self.scale = 1.0
        self.target_scale = 1.0
        self.animation_time = 0.0
    
    def update(self, delta_time: float) -> None:
        """Update button animations."""
        self.animation_time += delta_time
        
        # Update state based on interaction
        if self.hovered:
            self.state = 'hover'
            self.target_scale = 1.05
        else:
            self.state = 'normal'
            self.target_scale = 1.0
        
        # Smooth scale animation
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * delta_time * 8
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Hades-style menu button."""
        if not self.visible:
            return
        
        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Use Hades theme to draw ornate button
        self.hades_theme.draw_ornate_button(surface, scaled_rect, self.text, self.state)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button interaction with audio feedback and parallax effects."""
        if not self.visible or not self.enabled:
            return False
        
        # Handle mouse motion for hover effects
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos) and not self.hovered:
                # Button hover effect
                try:
                    trigger_ui_interaction(InteractionType.BUTTON_HOVER, event.pos[0], event.pos[1])
                except:
                    pass  # Fallback if parallax not available
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = 'active'
                # Button click effect
                try:
                    trigger_ui_interaction(InteractionType.BUTTON_CLICK, event.pos[0], event.pos[1])
                except:
                    pass  # Fallback if parallax not available
                if self.callback:
                    play_button_sound()
                    self.callback()
                return True
        
        return False


class HadesTitleDisplay(UIComponent):
    """Hades-style animated title display for the main menu."""
    
    def __init__(self, x: int, y: int, width: int, height: int, hades_theme: HadesEgyptianTheme):
        super().__init__(x, y, width, height)
        self.hades_theme = hades_theme
        self.title_text = "SANDS OF DUAT"
        self.subtitle_text = "Egyptian Underworld"
        
        # Animation properties
        self.glow_time = 0.0
        self.hieroglyph_time = 0.0
        self.sand_particles = []
        
        # Initialize sand particles for atmospheric effect
        self._create_sand_particles()
    
    def _create_sand_particles(self):
        """Create floating sand particles for atmosphere."""
        import random
        for _ in range(20):
            particle = {
                'x': random.randint(self.rect.left, self.rect.right),
                'y': random.randint(self.rect.top, self.rect.bottom),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.2, 0.2),
                'size': random.randint(1, 3),
                'alpha': random.randint(30, 80)
            }
            self.sand_particles.append(particle)
    
    def update(self, delta_time: float) -> None:
        """Update Hades-style title animations."""
        self.glow_time += delta_time
        self.hieroglyph_time += delta_time
        
        # Update sand particles
        for particle in self.sand_particles:
            particle['x'] += particle['vx'] * delta_time * 60
            particle['y'] += particle['vy'] * delta_time * 60
            
            # Wrap particles around screen
            if particle['x'] < self.rect.left - 10:
                particle['x'] = self.rect.right + 10
            elif particle['x'] > self.rect.right + 10:
                particle['x'] = self.rect.left - 10
            
            if particle['y'] < self.rect.top - 10:
                particle['y'] = self.rect.bottom + 10
            elif particle['y'] > self.rect.bottom + 10:
                particle['y'] = self.rect.top - 10
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the Hades-style animated title."""
        if not self.visible:
            return
        
        # Draw floating sand particles
        for particle in self.sand_particles:
            color = (*self.hades_theme.get_color('desert_amber'), particle['alpha'])
            particle_surface = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            surface.blit(particle_surface, (int(particle['x']), int(particle['y'])))
        
        # Draw main title with Hades styling
        title_pos = (self.rect.centerx, self.rect.centery - 20)
        self.hades_theme.draw_title_text(surface, self.title_text, title_pos, 'title')
        
        # Draw subtitle
        subtitle_pos = (self.rect.centerx, self.rect.centery + 40)
        self.hades_theme.draw_title_text(surface, self.subtitle_text, subtitle_pos, 'body')
        
        # Draw decorative hieroglyphs around title
        self._draw_decorative_hieroglyphs(surface)
    
    def _draw_decorative_hieroglyphs(self, surface: pygame.Surface):
        """Draw animated Egyptian hieroglyphs around the title."""
        # Simple hieroglyph-like decorations
        gold_color = self.hades_theme.get_color('duat_gold')
        
        # Animated glow effect
        glow_alpha = int(50 + 30 * abs(math.sin(self.hieroglyph_time * 1.5)))
        glow_color = (*gold_color, min(glow_alpha, 255))
        
        # Left side ankh
        left_x = self.rect.centerx - 200
        left_y = self.rect.centery
        self._draw_ankh_symbol(surface, (left_x, left_y), 20, glow_color)
        
        # Right side eye of horus
        right_x = self.rect.centerx + 200  
        right_y = self.rect.centery
        self._draw_eye_of_horus(surface, (right_x, right_y), 15, glow_color)
    
    def _draw_ankh_symbol(self, surface: pygame.Surface, center: Tuple[int, int], size: int, color: Tuple[int, int, int, int]):
        """Draw an ankh symbol."""
        x, y = center
        
        # Create surface for ankh with alpha
        ankh_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        
        # Ankh loop (oval at top)
        pygame.draw.ellipse(ankh_surface, color, (size//2, 0, size, size//2), 3)
        
        # Ankh vertical line
        pygame.draw.line(ankh_surface, color, (size, size//4), (size, size*1.8), 4)
        
        # Ankh horizontal line
        pygame.draw.line(ankh_surface, color, (size//2, size//2), (size*1.5, size//2), 4)
        
        surface.blit(ankh_surface, (x - size, y - size))
    
    def _draw_eye_of_horus(self, surface: pygame.Surface, center: Tuple[int, int], size: int, color: Tuple[int, int, int, int]):
        """Draw Eye of Horus symbol."""
        x, y = center
        
        # Create surface for eye
        eye_surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        
        # Eye outline
        pygame.draw.arc(eye_surface, color, (0, size//2, size*2, size), 0, math.pi, 3)
        
        # Eye pupil
        pygame.draw.circle(eye_surface, color, (size, size//2 + size//4), size//4)
        
        # Eye decoration line
        pygame.draw.line(eye_surface, color, (size*1.2, size), (size*1.5, size*1.3), 3)
        
        surface.blit(eye_surface, (x - size, y - size))


class VersionInfo(UIComponent):
    """Display version and development information."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.version_text = "v1.0.0"
        self.dev_text = "Development Build"
        self.font = pygame.font.Font(None, 24)
    
    def update(self, delta_time: float) -> None:
        """Update version info (no animation needed)."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render version information."""
        if not self.visible:
            return
        
        # Version text
        version_surface = self.font.render(self.version_text, True, (139, 117, 93))
        version_rect = version_surface.get_rect()
        version_rect.bottomright = (self.rect.right, self.rect.bottom)
        surface.blit(version_surface, version_rect)
        
        # Development text
        dev_surface = self.font.render(self.dev_text, True, (100, 85, 70))
        dev_rect = dev_surface.get_rect()
        dev_rect.bottomright = (self.rect.right, version_rect.top - 5)
        surface.blit(dev_surface, dev_rect)


class MenuScreen(UIScreen):
    """Main menu screen with Hades-style Egyptian theming."""
    
    def __init__(self):
        super().__init__("menu")
        
        # Initialize Hades-style theme
        display_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (1920, 1080)
        self.hades_theme = HadesEgyptianTheme(display_size)
        
        # Initialize advanced visual effects and parallax
        self.vfx_manager = None
        self.parallax_system = None
        self.atmospheric_manager = None
        
        if VFX_AVAILABLE:
            try:
                self.vfx_manager = get_visual_effects_manager(display_size[0], display_size[1])
                self.vfx_manager.initialize_screen_effects("menu", {"time_of_day": "dusk", "atmosphere": "mystical"})
                
                # Initialize interactive parallax system
                self.parallax_system = get_interactive_parallax_system(display_size[0], display_size[1])
                self.parallax_system.set_current_screen("menu")
                
                # Initialize atmospheric effects
                self.atmospheric_manager = get_atmospheric_manager(display_size[0], display_size[1])
                self.atmospheric_manager.setup_screen_atmosphere("menu")
                
            except Exception as e:
                print(f"VFX initialization failed: {e}")
                self.vfx_manager = None
                self.parallax_system = None
                self.atmospheric_manager = None
        
        # UI components
        self.title_display: Optional[HadesTitleDisplay] = None
        self.buttons: List[HadesMenuButton] = []
        self.version_info: Optional[VersionInfo] = None
        self.ui_manager = None  # Will be set by the UI manager
        
        # Background animation
        self.background_time = 0.0
        self.sand_dunes = []
        
    def on_enter(self) -> None:
        """Initialize main menu."""
        self.logger.info("Entering main menu")
        self._setup_ui_components()
        self._generate_background()
        
        # Setup parallax for menu screen
        if self.parallax_system:
            self.parallax_system.set_current_screen("menu")
        if self.atmospheric_manager:
            self.atmospheric_manager.setup_screen_atmosphere("menu")
    
    def on_exit(self) -> None:
        """Clean up main menu."""
        self.logger.info("Exiting main menu")
        self.clear_components()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle screen-level events including mouse movement for parallax."""
        # Handle mouse movement for parallax effects
        if event.type == pygame.MOUSEMOTION and self.parallax_system:
            try:
                handle_mouse_parallax(event.pos[0], event.pos[1])
            except:
                pass  # Fallback if parallax not available
        
        # Let base class handle other events
        return super().handle_event(event)
    
    def on_frame_start(self):
        """Called at the start of each frame for performance tracking."""
        if self.parallax_system:
            self.frame_start_time = time.time()
    
    def on_frame_end(self):
        """Called at the end of each frame for performance tracking."""
        if self.parallax_system and hasattr(self, 'frame_start_time'):
            frame_time = time.time() - self.frame_start_time
            self.parallax_system.performance_optimizer.record_frame_time(frame_time)
    
    def update(self, delta_time: float) -> None:
        """Update menu animations and visual effects."""
        super().update(delta_time)
        self.background_time += delta_time
        self._update_background(delta_time)
        
        # Update advanced visual effects
        if self.vfx_manager:
            try:
                self.vfx_manager.update(delta_time)
            except Exception as e:
                print(f"VFX update error: {e}")
        
        # Update parallax system
        if self.parallax_system:
            try:
                self.parallax_system.update(delta_time)
            except Exception as e:
                print(f"Parallax update error: {e}")
        
        # Update atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.update(delta_time)
            except Exception as e:
                print(f"Atmospheric update error: {e}")
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the main menu with advanced visual effects."""
        # Render parallax background first
        if self.parallax_system:
            try:
                camera_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
                self.parallax_system.render(surface, camera_rect)
            except Exception as e:
                print(f"Parallax render error: {e}")
                # Fallback: Draw simple animated background
                self._draw_background(surface)
        else:
            # Fallback: Draw simple animated background
            self._draw_background(surface)
        
        # Render atmospheric effects
        if self.atmospheric_manager:
            try:
                self.atmospheric_manager.render(surface)
            except Exception as e:
                print(f"Atmospheric render error: {e}")
        
        # Render advanced visual effects (background layers)
        if self.vfx_manager:
            try:
                camera_rect = pygame.Rect(0, 0, surface.get_width(), surface.get_height())
                self.vfx_manager.render_background_layers(surface, camera_rect)
                self.vfx_manager.render_atmospheric_effects(surface)
            except Exception as e:
                print(f"VFX background render error: {e}")
        
        # Render UI components
        super().render(surface)
        
        # Render advanced visual effects (foreground layers)
        if self.vfx_manager:
            try:
                self.vfx_manager.render_lighting_effects(surface)
                self.vfx_manager.render_screen_effects(surface)
            except Exception as e:
                print(f"VFX foreground render error: {e}")
    
    def _setup_ui_components(self) -> None:
        """Set up all menu UI components using responsive layout."""
        theme = get_theme()
        
        # Get screen dimensions from theme
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
        # Title display (top center, scaled for screen)
        title_width = min(screen_width - 200, 1000)
        title_height = max(120, int(screen_height * 0.15))
        title_x = (screen_width - title_width) // 2
        title_y = max(50, int(screen_height * 0.08))
        
        self.title_display = HadesTitleDisplay(title_x, title_y, title_width, title_height, self.hades_theme)
        self.add_component(self.title_display)
        
        # Menu buttons (center, scaled for screen)
        button_width = min(300, int(screen_width * 0.12))
        button_height = max(50, int(screen_height * 0.05))
        button_spacing = max(15, int(screen_height * 0.02))
        start_y = title_y + title_height + max(50, int(screen_height * 0.08))
        
        buttons_data = [
            ("New Game", self._start_new_game),
            ("Continue", self._continue_game),
            ("Tutorial", self._open_tutorial),
            ("Deck Builder", self._open_deck_builder),
            ("Exit", self._exit_game)
        ]
        
        for i, (text, callback) in enumerate(buttons_data):
            button_x = screen_width // 2 - button_width // 2
            button_y = start_y + i * (button_height + button_spacing)
            
            button = HadesMenuButton(
                button_x,
                button_y,
                button_width,
                button_height,
                text,
                self.hades_theme,
                callback
            )
            self.buttons.append(button)
            self.add_component(button)
        
        # Version info (bottom right)
        version_width = 200
        version_height = 50
        version_x = screen_width - version_width - 20
        version_y = screen_height - version_height - 20
        
        self.version_info = VersionInfo(version_x, version_y, version_width, version_height)
        self.add_component(self.version_info)
    
    def _generate_background(self) -> None:
        """Generate animated sand dune background."""
        for i in range(5):
            dune = {
                'x': random.randint(0, 1920),
                'y': random.randint(800, 1000),
                'width': random.randint(200, 400),
                'height': random.randint(50, 100),
                'speed': random.uniform(0.1, 0.3)
            }
            self.sand_dunes.append(dune)
    
    def _update_background(self, delta_time: float) -> None:
        """Update background animations."""
        for dune in self.sand_dunes:
            dune['x'] += dune['speed'] * delta_time * 60
            if dune['x'] > 2000:
                dune['x'] = -dune['width']
    
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw animated background."""
        # Apply background overlay for atmosphere
        self.hades_theme.draw_background_overlay(surface, 80)
        
        # Draw sand dunes
        for dune in self.sand_dunes:
            color = self.hades_theme.get_color('desert_sand')
            points = [
                (dune['x'], dune['y'] + dune['height']),
                (dune['x'] + dune['width'] // 3, dune['y']),
                (dune['x'] + 2 * dune['width'] // 3, dune['y']),
                (dune['x'] + dune['width'], dune['y'] + dune['height'])
            ]
            pygame.draw.polygon(surface, color, points)
    
    # Button callback methods
    def _start_new_game(self) -> None:
        """Start a new game."""
        self.logger.info("Starting new game")
        if self.ui_manager:
            self.ui_manager.switch_to_screen("progression")
    
    def _continue_game(self) -> None:
        """Continue existing game."""
        self.logger.info("Continue game requested")
        # TODO: Implement save loading
    
    def _open_tutorial(self) -> None:
        """Open tutorial screen."""
        self.logger.info("Opening tutorial")
        if self.ui_manager:
            self.ui_manager.switch_to_screen("tutorial")
    
    def _open_deck_builder(self) -> None:
        """Open deck builder screen."""
        self.logger.info("Opening deck builder")
        if self.ui_manager:
            self.ui_manager.switch_to_screen("deck_builder")
    
    def _exit_game(self) -> None:
        """Exit the game."""
        self.logger.info("Exit game requested")
        pygame.event.post(pygame.event.Event(pygame.QUIT))


# Compatibility wrapper for other screens that still use MenuButton
class MenuButton(HadesMenuButton):
    """Compatibility wrapper for HadesMenuButton."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, callback: Optional[Callable] = None):
        # Create a default theme if none provided
        display_size = (1920, 1080)
        default_theme = HadesEgyptianTheme(display_size)
        super().__init__(x, y, width, height, text, default_theme, callback)