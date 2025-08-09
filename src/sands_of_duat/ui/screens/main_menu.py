"""
Professional Main Menu Screen - Hades-level polish with Egyptian theming.
Features animated buttons, particle effects, and smooth transitions.
"""

import pygame
import math
from typing import List, Optional, Callable
from enum import Enum, auto

from ...core.constants import (
    Colors, Layout, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER,
    FontSizes
)
from ...core.state_manager import GameState
from ...core.asset_loader import get_asset_loader
from ...audio.simple_audio_manager import audio_manager, SoundEffect, AudioTrack
from ..components.animated_button import AnimatedButton
from ..components.title_animation import TitleAnimation

class MenuAction(Enum):
    """Main menu actions."""
    START_GAME = auto()
    DECK_BUILDER = auto()
    COLLECTION = auto()
    SETTINGS = auto()
    QUIT = auto()

class MainMenuScreen:
    """
    Professional main menu with Hades-level animations and Egyptian theming.
    Features smooth button animations, particle effects, and ultrawide support.
    """
    
    def __init__(self, on_menu_action: Optional[Callable[[MenuAction], None]] = None):
        """
        Initialize main menu screen.
        
        Args:
            on_menu_action: Callback for menu actions
        """
        self.on_menu_action = on_menu_action
        
        # Background gradient
        self.background_surface = self._create_background()
        
        # Title animation system
        self.title_animation = TitleAnimation()
        
        # Button system
        self.buttons = self._create_buttons()
        self.selected_button_index = 0
        
        # Animation state
        self.menu_animation_time = 0.0
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        
        # Input handling
        self.key_repeat_time = 0.0
        self.last_mouse_pos = (0, 0)
    
    def _create_background(self) -> pygame.Surface:
        """Load generated background asset with fallback."""
        # Try to load the generated menu background
        asset_loader = get_asset_loader()
        menu_bg = asset_loader.load_background('menu')
        
        if menu_bg:
            # Scale to screen size if needed
            if menu_bg.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return menu_bg
        
        # Fallback: Create gradient if asset loading fails
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create gradient effect
        for y in range(SCREEN_HEIGHT):
            # Egyptian night sky gradient
            ratio = y / SCREEN_HEIGHT
            
            # Interpolate between dark blue (top) and darker blue (bottom)
            r = int(Colors.DARK_BLUE[0] * (1 - ratio * 0.3))
            g = int(Colors.DARK_BLUE[1] * (1 - ratio * 0.3))
            b = int(Colors.DARK_BLUE[2] * (1 + ratio * 0.2))
            
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        return background
    
    def _create_buttons(self) -> List[AnimatedButton]:
        """Create animated menu buttons with Egyptian styling."""
        buttons = []
        
        # Button configuration
        button_configs = [
            ("ENTER THE UNDERWORLD", MenuAction.START_GAME),
            ("BUILD YOUR DECK", MenuAction.DECK_BUILDER), 
            ("HALL OF GODS", MenuAction.COLLECTION),
            ("TEMPLE SETTINGS", MenuAction.SETTINGS),
            ("RETURN TO MORTAL REALM", MenuAction.QUIT)
        ]
        
        # Layout calculation
        button_width = Layout.BUTTON_WIDTH_WIDE
        button_height = Layout.BUTTON_HEIGHT
        button_spacing = 20
        
        # Center buttons in content area
        total_height = len(button_configs) * button_height + (len(button_configs) - 1) * button_spacing
        start_y = SCREEN_CENTER[1] + 50  # Below title
        
        # Adjust for ultrawide
        center_x = SCREEN_CENTER[0]
        
        for i, (text, action) in enumerate(button_configs):
            y = start_y + i * (button_height + button_spacing)
            x = center_x - button_width // 2
            
            button = AnimatedButton(
                x, y, button_width, button_height,
                text, FontSizes.BUTTON,
                action=lambda a=action: self._handle_button_action(a)
            )
            buttons.append(button)
        
        return buttons
    
    def _handle_button_action(self, action: MenuAction):
        """Handle button click actions."""
        if self.on_menu_action:
            self.on_menu_action(action)
    
    def update(self, dt: float, events: List[pygame.event.Event], 
               mouse_pos: tuple, mouse_pressed: bool):
        """
        Update menu animations and handle input.
        
        Args:
            dt: Delta time in seconds
            events: Pygame events this frame
            mouse_pos: Current mouse position
            mouse_pressed: Whether mouse is pressed
        """
        # Update animation timers
        self.menu_animation_time += dt
        
        # Handle fade-in animation
        if not self.fade_in_complete:
            self.fade_in_progress = min(1.0, self.fade_in_progress + dt * 2.0)
            if self.fade_in_progress >= 1.0:
                self.fade_in_complete = True
        
        # Update title animation
        self.title_animation.update(dt)
        
        # Update buttons
        for i, button in enumerate(self.buttons):
            # Check for hover state change for sound effects
            was_hovered = button.is_hovered
            button.update(dt, mouse_pos, mouse_pressed)
            
            # Play hover sound when button becomes hovered
            if button.is_hovered and not was_hovered:
                audio_manager.play_sound(SoundEffect.BUTTON_HOVER, 0.3)
            
            # Update selected button based on mouse position
            if button.rect.collidepoint(mouse_pos):
                self.selected_button_index = i
        
        # Handle events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for button in self.buttons:
                        if button.handle_click(mouse_pos):
                            audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
                            break
        
        self.last_mouse_pos = mouse_pos
    
    def _handle_keyboard_input(self, key: int):
        """Handle keyboard navigation and actions."""
        if key == pygame.K_UP:
            self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
        elif key == pygame.K_DOWN:
            self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            # Simulate click on selected button
            selected_button = self.buttons[self.selected_button_index]
            if selected_button.action:
                audio_manager.play_sound(SoundEffect.BUTTON_CLICK, 0.6)
                selected_button.action()
        elif key == pygame.K_ESCAPE:
            # Quick quit
            self._handle_button_action(MenuAction.QUIT)
    
    def render(self, surface: pygame.Surface):
        """
        Render the main menu with all animations and effects.
        
        Args:
            surface: Surface to render to
        """
        # Clear surface
        surface.blit(self.background_surface, (0, 0))
        
        # Draw ultrawide side bars with Egyptian pattern
        if Layout.IS_ULTRAWIDE:
            self._render_ultrawide_bars(surface)
        
        # Apply fade-in effect
        if not self.fade_in_complete:
            fade_surface = surface.copy()
            fade_surface.set_alpha(int(255 * self.fade_in_progress))
            surface.fill(Colors.BLACK)
            surface.blit(fade_surface, (0, 0))
        
        # Render title animation
        self.title_animation.render(surface)
        
        # Render version/sprint info
        self._render_version_info(surface)
        
        # Render buttons
        for i, button in enumerate(self.buttons):
            # Highlight selected button for keyboard navigation
            if i == self.selected_button_index and self.last_mouse_pos != pygame.mouse.get_pos():
                # Draw selection indicator
                indicator_rect = button.rect.inflate(8, 8)
                pygame.draw.rect(surface, Colors.GOLD, indicator_rect, 2)
            
            button.render(surface)
        
        # Render control hints
        self._render_control_hints(surface)
    
    def _render_ultrawide_bars(self, surface: pygame.Surface):
        """Render Egyptian-themed side bars for ultrawide displays."""
        if not Layout.IS_ULTRAWIDE:
            return
        
        # Left and right bar areas
        left_bar = pygame.Rect(0, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        right_bar = pygame.Rect(Layout.UI_SAFE_RIGHT, 0, Layout.CONTENT_X_OFFSET, SCREEN_HEIGHT)
        
        # Fill with darker Egyptian pattern
        pattern_color = (15, 15, 50)
        pygame.draw.rect(surface, pattern_color, left_bar)
        pygame.draw.rect(surface, pattern_color, right_bar)
        
        # Add subtle Egyptian border pattern
        border_color = Colors.GOLD
        border_alpha = int(100 + 50 * abs(math.sin(self.menu_animation_time)))
        
        # Create pattern surface
        pattern_surface = pygame.Surface((4, SCREEN_HEIGHT))
        pattern_surface.set_alpha(border_alpha)
        pattern_surface.fill(border_color)
        
        # Draw pattern lines
        surface.blit(pattern_surface, (Layout.CONTENT_X_OFFSET - 4, 0))
        surface.blit(pattern_surface, (Layout.UI_SAFE_RIGHT, 0))
    
    def _render_version_info(self, surface: pygame.Surface):
        """Render version and sprint information."""
        font = pygame.font.Font(None, FontSizes.DEBUG)
        
        # Version info
        version_text = "SPRINT 3: Game State Flow & Transitions - IN PROGRESS"
        version_surface = font.render(version_text, True, Colors.DESERT_SAND)
        version_rect = version_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 50))
        surface.blit(version_surface, version_rect)
        
        # Resolution info
        if Layout.IS_ULTRAWIDE:
            res_text = f"Optimized for Ultrawide {SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            res_surface = font.render(res_text, True, Colors.GOLD)
            res_rect = res_surface.get_rect(center=(SCREEN_CENTER[0], SCREEN_HEIGHT - 30))
            surface.blit(res_surface, res_rect)
    
    def _render_control_hints(self, surface: pygame.Surface):
        """Render control hints for better UX."""
        font = pygame.font.Font(None, FontSizes.CARD_TEXT)
        
        hints = [
            "↑↓ Navigate  ENTER Select  ESC Quit",
            "F11 Fullscreen  F1 Debug Info"
        ]
        
        y_offset = 20
        for hint in hints:
            hint_surface = font.render(hint, True, Colors.DESERT_SAND)
            surface.blit(hint_surface, (20, y_offset))
            y_offset += 25
    
    def reset_animations(self):
        """Reset all animations for clean menu entry."""
        self.fade_in_progress = 0.0
        self.fade_in_complete = False
        self.menu_animation_time = 0.0
        
        # Reset button states
        for button in self.buttons:
            button.hover_progress = 0.0
            button.press_progress = 0.0
        
        # Start menu music
        audio_manager.play_music(AudioTrack.MENU, fade_in=2.0)