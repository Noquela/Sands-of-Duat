"""
Menu Screen

Main menu interface with game options, settings, and navigation.
"""

import pygame
import math
import random
from typing import Dict, Any, Optional, List, Callable
from .base import UIScreen, UIComponent
from .theme import get_theme
from .animation_system import EasingType
from sands_duat.audio.sound_effects import play_button_sound


class MenuButton(UIComponent):
    """
    Stylized button component for menu navigation.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, callback: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 32)
        
        # Visual states
        self.scale = 1.0
        self.target_scale = 1.0
        self.glow_alpha = 0
        self.target_glow = 0
        
        # Colors
        self.button_color = (60, 45, 30)
        self.button_hover_color = (80, 60, 40)
        self.button_border_color = (139, 117, 93)
        self.glow_color = (255, 215, 0)
    
    def update(self, delta_time: float) -> None:
        """Update button animations."""
        # Scale animation
        if abs(self.scale - self.target_scale) > 0.01:
            self.scale += (self.target_scale - self.scale) * delta_time * 8
        
        # Glow animation
        if abs(self.glow_alpha - self.target_glow) > 1:
            self.glow_alpha += (self.target_glow - self.glow_alpha) * delta_time * 10
        
        # Update targets based on hover state
        if self.hovered:
            self.target_scale = 1.05
            self.target_glow = 100
        else:
            self.target_scale = 1.0
            self.target_glow = 0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the menu button."""
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
        
        # Draw glow effect
        if self.glow_alpha > 0:
            glow_rect = scaled_rect.inflate(10, 10)
            glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
            glow_color = (*self.glow_color, int(self.glow_alpha))
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=8)
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Draw button background
        button_color = self.button_hover_color if self.hovered else self.button_color
        pygame.draw.rect(surface, button_color, scaled_rect, border_radius=5)
        
        # Draw button border
        pygame.draw.rect(surface, self.button_border_color, scaled_rect, 3, border_radius=5)
        
        # Draw button text
        text_color = self.glow_color if self.hovered else self.text_color
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button interaction with audio feedback."""
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Play click sound (with error handling)
                try:
                    play_button_sound("click")
                except Exception as e:
                    print(f"Audio error: {e}")
                
                print(f"Button clicked: {self.text}")
                if self.callback:
                    print(f"Executing callback for: {self.text}")
                    self.callback()
                else:
                    print(f"No callback set for button: {self.text}")
                self._trigger_event("button_clicked", {"text": self.text})
                return True
        
        elif event.type == pygame.MOUSEMOTION:
            # Handle hover with audio
            mouse_over = self.rect.collidepoint(event.pos)
            if mouse_over and not self.hovered:
                self.hovered = True
                # Play hover sound (with error handling)
                try:
                    play_button_sound("hover")
                except Exception as e:
                    print(f"Audio error: {e}")
                self._trigger_event("hover_start", {"pos": event.pos})
            elif not mouse_over and self.hovered:
                self.hovered = False
                self._trigger_event("hover_end", {"pos": event.pos})
        
        return False


class TitleDisplay(UIComponent):
    """
    Animated title display for the main menu.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.title_text = "SANDS OF DUAT"
        self.subtitle_text = "Hour-Glass Initiative"
        
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Animation properties
        self.glow_time = 0.0
        self.particle_time = 0.0
        self.particles = []
        
        # Colors
        self.title_color = (255, 215, 0)  # Gold
        self.subtitle_color = (255, 248, 220)  # Cornsilk
        self.glow_color = (255, 215, 0)
    
    def update(self, delta_time: float) -> None:
        """Update title animations."""
        self.glow_time += delta_time
        self.particle_time += delta_time
        
        # Update particles (sand grains)
        self._update_particles(delta_time)
        
        # Spawn new particles occasionally
        if self.particle_time > 0.1:  # Every 100ms
            self._spawn_particle()
            self.particle_time = 0.0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the animated title."""
        if not self.visible:
            return
        
        # Draw particles
        for particle in self.particles:
            if particle['alpha'] > 0:
                color = (*self.glow_color, int(particle['alpha']))
                particle_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                particle_surface.fill(color)
                surface.blit(particle_surface, (particle['x'], particle['y']))
        
        # Calculate glow intensity
        glow_intensity = int(50 + 30 * abs(math.sin(self.glow_time * 2)))
        
        # Draw title with glow
        title_surface = self.title_font.render(self.title_text, True, self.title_color)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.centery = self.rect.centery - 30
        
        # Glow effect
        glow_surface = self.title_font.render(self.title_text, True, (*self.glow_color, glow_intensity))
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            surface.blit(glow_surface, glow_rect)
        
        surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, self.subtitle_color)
        subtitle_rect = subtitle_surface.get_rect()
        subtitle_rect.centerx = self.rect.centerx
        subtitle_rect.top = title_rect.bottom + 10
        surface.blit(subtitle_surface, subtitle_rect)
    
    def _update_particles(self, delta_time: float) -> None:
        """Update sand particle animations."""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * delta_time * 60
            particle['y'] += particle['vy'] * delta_time * 60
            particle['life'] -= delta_time
            particle['alpha'] = max(0, 255 * (particle['life'] / particle['max_life']))
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def _spawn_particle(self) -> None:
        """Spawn a new sand particle."""
        import random
        
        particle = {
            'x': self.rect.centerx + random.randint(-200, 200),
            'y': self.rect.top - 10,
            'vx': random.uniform(-20, 20),
            'vy': random.uniform(20, 50),
            'life': random.uniform(2.0, 4.0),
            'max_life': 0,
            'alpha': 255
        }
        particle['max_life'] = particle['life']
        self.particles.append(particle)


class VersionInfo(UIComponent):
    """
    Displays version and development information.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.version_text = "Alpha v0.1.0"
        self.dev_text = "Sand of Duat Development Team"
        self.font = pygame.font.Font(None, 20)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Version info should not consume mouse events."""
        return False
    
    def update(self, delta_time: float) -> None:
        """Update version info."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render version information."""
        if not self.visible:
            return
        
        # Version text
        version_surface = self.font.render(self.version_text, True, (150, 150, 150))
        version_rect = version_surface.get_rect()
        version_rect.bottomright = (self.rect.right, self.rect.bottom - 20)
        surface.blit(version_surface, version_rect)
        
        # Development team text
        dev_surface = self.font.render(self.dev_text, True, (120, 120, 120))
        dev_rect = dev_surface.get_rect()
        dev_rect.bottomright = (self.rect.right, version_rect.top - 5)
        surface.blit(dev_surface, dev_rect)


class MenuScreen(UIScreen):
    """
    Main menu screen with navigation options.
    
    Provides access to different game modes, settings, and utilities.
    Features animated Egyptian-themed background and typography.
    """
    
    def __init__(self):
        super().__init__("menu")
        
        # UI components
        self.title_display: Optional[TitleDisplay] = None
        self.buttons: List[MenuButton] = []
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
    
    def on_exit(self) -> None:
        """Clean up main menu."""
        self.logger.info("Exiting main menu")
        self.clear_components()
    
    def update(self, delta_time: float) -> None:
        """Update menu animations."""
        super().update(delta_time)
        self.background_time += delta_time
        self._update_background(delta_time)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the main menu."""
        # Draw animated background
        self._draw_background(surface)
        
        # Render UI components
        super().render(surface)
    
    def _setup_ui_components(self) -> None:
        """Set up all menu UI components using responsive layout."""
        theme = get_theme()
        
        # Get screen dimensions from theme
        screen_width = theme.display.base_width
        screen_height = theme.display.base_height
        
# Debug removed
        
        # Title display (top center, scaled for screen)
        title_width = min(screen_width - 200, 1000)
        title_height = max(120, int(screen_height * 0.15))
        title_x = (screen_width - title_width) // 2
        title_y = max(50, int(screen_height * 0.08))
        
        self.title_display = TitleDisplay(title_x, title_y, title_width, title_height)
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
            
            button = MenuButton(
                button_x,
                button_y,
                button_width,
                button_height,
                text,
                callback
            )
            self.buttons.append(button)
            self.add_component(button)
        
        # Version info (bottom right)
        self.version_info = VersionInfo(0, 0, screen_width, screen_height)
        self.add_component(self.version_info)
    
    def _generate_background(self) -> None:
        """Generate animated background elements."""
        import random
        
        # Generate sand dunes
        for _ in range(5):
            dune = {
                'x': random.randint(0, 800),
                'y': random.randint(400, 550),
                'width': random.randint(100, 200),
                'height': random.randint(30, 60),
                'speed': random.uniform(5, 15)
            }
            self.sand_dunes.append(dune)
    
    def _update_background(self, delta_time: float) -> None:
        """Update background animations."""
        # Move sand dunes slowly
        for dune in self.sand_dunes:
            dune['x'] -= dune['speed'] * delta_time
            if dune['x'] + dune['width'] < 0:
                dune['x'] = 800 + dune['width']
    
    def _draw_background(self, surface: pygame.Surface) -> None:
        """Draw animated background."""
        # Gradient sky
        for y in range(surface.get_height()):
            # Create a gradient from dark blue at top to warm brown at bottom
            ratio = y / surface.get_height()
            r = int(15 + ratio * 45)  # 15 to 60
            g = int(10 + ratio * 35)  # 10 to 45
            b = int(5 + ratio * 25)   # 5 to 30
            
            pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
        
        # Draw sand dunes
        for dune in self.sand_dunes:
            # Create elliptical dune shape
            dune_rect = pygame.Rect(dune['x'], dune['y'], dune['width'], dune['height'])
            pygame.draw.ellipse(surface, (80, 60, 40), dune_rect)
            
            # Add highlight
            highlight_rect = pygame.Rect(dune['x'], dune['y'], dune['width'], dune['height'] // 3)
            pygame.draw.ellipse(surface, (100, 80, 60), highlight_rect)
        
        # Draw stars (simplified)
        import random
        random.seed(42)  # Fixed seed for consistent star positions
        for _ in range(50):
            x = random.randint(0, surface.get_width())
            y = random.randint(0, 200)  # Only in upper portion
            brightness = random.randint(100, 255)
            star_color = (brightness, brightness, brightness)
            
            # Twinkling effect
            twinkle = abs(math.sin(self.background_time * 3 + x + y)) * 0.5 + 0.5
            final_brightness = int(brightness * twinkle)
            final_color = (final_brightness, final_brightness, final_brightness)
            
            pygame.draw.circle(surface, final_color, (x, y), 1)
    
    # Button callback methods
    def _start_new_game(self) -> None:
        """Start a new game - begins with tutorial for new players."""
        self.logger.info("Starting new game")
        # For new players, start with tutorial which will then lead to progression
        if self.ui_manager:
            # Set tutorial context for new game flow
            tutorial_screen = self.ui_manager.screens.get("tutorial")
            if tutorial_screen and hasattr(tutorial_screen, 'set_game_flow_context'):
                tutorial_screen.set_game_flow_context(is_new_game=True, return_screen="progression")
            self.ui_manager.switch_to_screen_with_transition("tutorial", "slide_left")
        else:
            self._trigger_event("switch_screen", {"screen": "tutorial"})
    
    def _continue_game(self) -> None:
        """Continue existing game - goes to progression hub."""
        self.logger.info("Continue game")
        # For now, take players to progression screen where they can choose their path
        if self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("progression", "slide_left")
        else:
            self._trigger_event("switch_screen", {"screen": "progression"})
    
    
    def _open_tutorial(self) -> None:
        """Open tutorial system."""
        self.logger.info("Opening tutorial system")
        # Switch to tutorial with fade transition
        if self.ui_manager:
            # Set tutorial context for standalone tutorial access
            tutorial_screen = self.ui_manager.screens.get("tutorial")
            if tutorial_screen and hasattr(tutorial_screen, 'set_game_flow_context'):
                tutorial_screen.set_game_flow_context(is_new_game=False, return_screen="menu")
            self.ui_manager.switch_to_screen_with_transition("tutorial", "fade")
        else:
            self._trigger_event("switch_screen", {"screen": "tutorial"})
    
    def _open_deck_builder(self) -> None:
        """Open deck builder."""
        self.logger.info("Opening deck builder")
        # Switch to deck builder with fade transition
        if self.ui_manager:
            self.ui_manager.switch_to_screen_with_transition("deck_builder", "fade")
        else:
            self._trigger_event("switch_screen", {"screen": "deck_builder"})
    
    
    def _exit_game(self) -> None:
        """Exit the game."""
        self.logger.info("Exiting game")
        import pygame
        pygame.quit()
        import sys
        sys.exit()